#!/usr/bin/env python3
# ============================================================
# OPTIMUS AI - DEPARTEMENTS D'EXECUTION
# Version 1.0
# Fichier indépendant des autres fichiers du projet
# ============================================================

import os
import re
import csv
import ast
import json
import time
import argparse
import traceback
import concurrent.futures

from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent

TASK_FILE = ROOT / "optimus-tasks.json"
WORK_DIR = ROOT / "optimus-workspaces"
REPORT_DIR = ROOT / "optimus-department-reports"

MAX_WORKERS = 8
MAX_TASKS = 100


# ============================================================
# 1. ORGANISATION DES DEPARTEMENTS
# ============================================================

DEPARTMENTS = {
    "RECHERCHE": "Recherche des missions",
    "ANALYSE": "Analyse des opportunités",
    "PLANIFICATION": "Préparation des travaux",
    "PROGRAMMATION": "Développement informatique",
    "PRODUCTION": "Production des livrables",
    "TESTS": "Vérification et tests",
    "QUALITE": "Contrôle des résultats",
    "LIVRAISON": "Préparation des soumissions",
    "PAIEMENT": "Suivi des paiements",
    "AMELIORATION": "Analyse des erreurs"
}


# ============================================================
# 2. CONFIGURATION INITIALE
# ============================================================

SAMPLE_TASKS = {
    "tasks": [
        {
            "id": "TASK001",
            "department": "PRODUCTION",
            "type": "create_text",
            "title": "Créer un document",
            "output": "documents/resultat.txt",
            "content": "Travail réalisé par le département Production OPTIMUS."
        },
        {
            "id": "TASK002",
            "department": "ANALYSE",
            "type": "analyze_text",
            "title": "Analyser un texte",
            "text": "OPTIMUS recherche, analyse, produit et teste des travaux."
        }
    ]
}


def initialize():

    WORK_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    if not TASK_FILE.exists():

        TASK_FILE.write_text(
            json.dumps(
                SAMPLE_TASKS,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        print("[INIT] Fichier optimus-tasks.json créé.")


# ============================================================
# 3. SECURITE DES FICHIERS
# ============================================================

def safe_path(relative_path):

    path = Path(relative_path)

    if path.is_absolute():
        raise ValueError("Chemin absolu interdit.")

    if ".." in path.parts:
        raise ValueError("Chemin interdit.")

    destination = (WORK_DIR / path).resolve()

    if WORK_DIR.resolve() not in destination.parents:
        raise ValueError("Accès hors du dossier de travail interdit.")

    return destination


# ============================================================
# 4. DEPARTEMENT PRODUCTION
# ============================================================

def create_text(task):

    content = task.get("content", "")

    if not isinstance(content, str):
        raise ValueError("Contenu invalide.")

    if len(content) > 200000:
        raise ValueError("Document trop volumineux.")

    output = safe_path(task["output"])

    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        content,
        encoding="utf-8"
    )

    return {
        "file": str(output.relative_to(WORK_DIR)),
        "characters": len(content)
    }


# ============================================================
# 5. DEPARTEMENT ANALYSE
# ============================================================

def analyze_text(task):

    text = task.get("text", "")

    if not isinstance(text, str):
        raise ValueError("Texte invalide.")

    words = re.findall(
        r"\b[\wÀ-ÿ'-]+\b",
        text
    )

    sentences = [
        s for s in re.split(r"[.!?]+", text)
        if s.strip()
    ]

    return {
        "characters": len(text),
        "words": len(words),
        "sentences": len(sentences),
        "average_word_length": round(
            sum(len(w) for w in words) / len(words),
            2
        ) if words else 0
    }


# ============================================================
# 6. DEPARTEMENT PROGRAMMATION
# ============================================================

def check_python(task):

    source = safe_path(task["input"])

    if not source.exists():
        raise FileNotFoundError("Fichier Python introuvable.")

    if source.suffix != ".py":
        raise ValueError("Le fichier doit être un .py.")

    if source.stat().st_size > 5_000_000:
        raise ValueError("Fichier trop volumineux.")

    code = source.read_text(encoding="utf-8")

    # Analyse syntaxique uniquement.
    # Aucun code inconnu n'est exécuté.

    ast.parse(code)

    return {
        "file": str(source.relative_to(WORK_DIR)),
        "syntax": "OK"
    }


# ============================================================
# 7. DEPARTEMENT PRODUCTION - CSV
# ============================================================

def analyze_csv(task):

    source = safe_path(task["input"])

    if not source.exists():
        raise FileNotFoundError("CSV introuvable.")

    if source.stat().st_size > 5_000_000:
        raise ValueError("CSV trop volumineux.")

    with source.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        headers = reader.fieldnames or []

        rows = list(reader)

    return {
        "file": str(source.relative_to(WORK_DIR)),
        "rows": len(rows),
        "columns": headers
    }


# ============================================================
# 8. MOTEUR CENTRAL D'EXECUTION
# ============================================================

EXECUTORS = {

    "create_text": create_text,

    "analyze_text": analyze_text,

    "check_python": check_python,

    "analyze_csv": analyze_csv

}


def execute_task(task):

    task_id = task.get("id", "UNKNOWN")

    department = task.get(
        "department",
        "NON_AFFECTE"
    )

    start = time.time()

    print(
        f"[DEBUT] {department} | {task_id}"
    )

    result = {
        "id": task_id,
        "department": department,
        "title": task.get("title", ""),
        "started_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    try:

        task_type = task.get("type")

        if task_type not in EXECUTORS:
            raise ValueError(
                f"Type de tâche non pris en charge : {task_type}"
            )

        output = EXECUTORS[task_type](task)

        result["status"] = "SUCCESS"

        result["result"] = output

    except Exception as error:

        result["status"] = "FAILED"

        result["error"] = str(error)

        result["traceback"] = traceback.format_exc(
            limit=5
        )

    result["duration"] = round(
        time.time() - start,
        3
    )

    result["finished_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    print(
        f"[{result['status']}] {department} | {task_id}"
    )

    return result


# ============================================================
# 9. DEPARTEMENT QUALITE
# ============================================================

def quality_control(results):

    for result in results:

        if result["status"] != "SUCCESS":
            result["quality"] = "ECHEC"

        elif result.get("result") is None:
            result["quality"] = "A_VERIFIER"

        else:
            result["quality"] = "PRODUIT_GENERE"


# ============================================================
# 10. DEPARTEMENT AMELIORATION
# ============================================================

def improvement_report(results):

    successful = sum(
        1 for r in results
        if r["status"] == "SUCCESS"
    )

    failed = sum(
        1 for r in results
        if r["status"] == "FAILED"
    )

    return {
        "total": len(results),
        "successful": successful,
        "failed": failed,
        "success_rate": round(
            successful / len(results) * 100,
            2
        ) if results else 0
    }


# ============================================================
# 11. CONTROLEUR OPTIMUS
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--workers",
        type=int,
        default=4
    )

    args = parser.parse_args()

    workers = max(
        1,
        min(args.workers, MAX_WORKERS)
    )

    initialize()

    try:

        data = json.loads(
            TASK_FILE.read_text(
                encoding="utf-8"
            )
        )

        tasks = data.get("tasks", [])

        if not isinstance(tasks, list):
            raise ValueError("'tasks' doit être une liste.")

        if len(tasks) > MAX_TASKS:
            raise ValueError("Trop de tâches.")

    except Exception as error:

        print("[ERREUR CONFIGURATION]", error)

        return

    print("\n")
    print("======================================")
    print("       OPTIMUS AI CENTRAL")
    print("======================================")

    print("Départements disponibles :")

    for name, description in DEPARTMENTS.items():

        print(f"- {name}: {description}")

    print("--------------------------------------")

    print("Nombre de tâches :", len(tasks))

    print("Travailleurs parallèles :", workers)

    print("--------------------------------------")

    results = []

    # Plusieurs départements peuvent travailler
    # simultanément.

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        futures = [
            executor.submit(execute_task, task)
            for task in tasks
        ]

        for future in concurrent.futures.as_completed(futures):

            results.append(future.result())

    # Contrôle qualité

    quality_control(results)

    # Amélioration et statistiques

    statistics = improvement_report(results)

    report = {

        "system": "OPTIMUS AI",

        "version": "1.0",

        "date": datetime.now(
            timezone.utc
        ).isoformat(),

        "statistics": statistics,

        "results": results

    }

    # Enregistrement du rapport

    filename = (
        "report-"
        + datetime.now().strftime("%Y%m%d-%H%M%S")
        + ".json"
    )

    report_path = REPORT_DIR / filename

    report_path.write_text(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    latest_path = REPORT_DIR / "latest.json"

    latest_path.write_text(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    # Résultat final

    print("\n")
    print("======================================")
    print("          BILAN OPTIMUS")
    print("======================================")

    print("Total :", statistics["total"])

    print("Réussites :", statistics["successful"])

    print("Échecs :", statistics["failed"])

    print("Taux de réussite :", statistics["success_rate"], "%")

    print("Rapport :", report_path)

    print("======================================")


# ============================================================
# 12. DEMARRAGE
# ============================================================

if __name__ == "__main__":

    main()