"""
OPTIMUS TASK ENGINE
Version 1.0.1

Moteur polyvalent :
- Planification des tâches
- Analyse Python
- Analyse JSON
- Analyse CSV
- Analyse des documents texte
- Détection des erreurs
- Rapports automatiques
- Historique des exécutions

Sécurité :
- Aucun lancement arbitraire de commande
- Aucune modification automatique du code source
- Protection des répertoires sensibles
"""

import ast
import csv
import json
import sys
import time
import traceback
import hashlib

from pathlib import Path
from datetime import datetime, timezone


# =====================================================
# CONFIGURATION
# =====================================================

VERSION = "1.0.1"

ROOT = Path(__file__).resolve().parent

REPORT_DIR = ROOT / "task-reports"
HISTORY_FILE = ROOT / "task-history.json"

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".py",
    ".json",
    ".csv",
    ".txt",
    ".md"
}

BLOCKED_DIRECTORIES = {
    ".git",
    ".github",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules"
}


# =====================================================
# OUTILS
# =====================================================

def now():
    return datetime.now(timezone.utc).isoformat()


def file_hash(path):

    try:
        return hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

    except Exception:
        return None


def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    temporary.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    temporary.replace(path)


def load_json(path, default=None):

    if default is None:
        default = {}

    try:

        if path.exists():

            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

    except Exception:
        pass

    return default


# =====================================================
# VALIDATION DES FICHIERS
# =====================================================

def validate_path(relative_path):

    path = (
        ROOT / str(relative_path)
    ).resolve()

    try:

        path.relative_to(ROOT)

    except ValueError:

        raise ValueError(
            "Accès refusé : chemin hors du projet."
        )

    if path == ROOT:

        raise ValueError(
            "Un fichier est requis."
        )

    if any(
        part in BLOCKED_DIRECTORIES
        for part in path.relative_to(ROOT).parts
    ):

        raise ValueError(
            "Répertoire protégé."
        )

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:

        raise ValueError(
            "Extension non autorisée."
        )

    if not path.is_file():

        raise FileNotFoundError(
            f"Fichier introuvable : {relative_path}"
        )

    if path.stat().st_size > MAX_FILE_SIZE:

        raise ValueError(
            "Fichier trop volumineux."
        )

    return path


# =====================================================
# ANALYSE PYTHON
# =====================================================

def analyze_python(path):

    result = {
        "file": str(path.relative_to(ROOT)),
        "type": "python",
        "status": "unknown",
        "errors": [],
        "warnings": [],
        "functions": [],
        "classes": [],
        "lines": 0,
        "sha256": file_hash(path)
    }

    try:

        source = path.read_text(
            encoding="utf-8"
        )

        result["lines"] = len(
            source.splitlines()
        )

        tree = ast.parse(
            source,
            filename=str(path)
        )

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):

                result["functions"].append(
                    node.name
                )

            elif isinstance(node, ast.ClassDef):

                result["classes"].append(
                    node.name
                )

        result["status"] = "valid"

    except SyntaxError as error:

        result["status"] = "error"

        result["errors"].append({
            "type": "SyntaxError",
            "message": error.msg,
            "line": error.lineno,
            "column": error.offset
        })

    except Exception as error:

        result["status"] = "error"

        result["errors"].append({
            "type": type(error).__name__,
            "message": str(error)
        })

    return result


# =====================================================
# ANALYSE JSON
# =====================================================

def analyze_json(path):

    result = {
        "file": str(path.relative_to(ROOT)),
        "type": "json",
        "status": "unknown",
        "errors": [],
        "keys": [],
        "elements": 0,
        "sha256": file_hash(path)
    }

    try:

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        result["status"] = "valid"

        if isinstance(data, dict):

            result["keys"] = list(
                data.keys()
            )

            result["elements"] = len(data)

        elif isinstance(data, list):

            result["elements"] = len(data)

    except json.JSONDecodeError as error:

        result["status"] = "error"

        result["errors"].append({
            "type": "JSONDecodeError",
            "message": error.msg,
            "line": error.lineno,
            "column": error.colno
        })

    except Exception as error:

        result["status"] = "error"

        result["errors"].append({
            "type": type(error).__name__,
            "message": str(error)
        })

    return result


# =====================================================
# ANALYSE CSV
# =====================================================

def analyze_csv(path):

    result = {
        "file": str(path.relative_to(ROOT)),
        "type": "csv",
        "status": "unknown",
        "columns": [],
        "rows": 0,
        "errors": [],
        "sha256": file_hash(path)
    }

    try:

        with path.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            result["columns"] = (
                reader.fieldnames or []
            )

            for _ in reader:
                result["rows"] += 1

        result["status"] = "valid"

    except Exception as error:

        result["status"] = "error"

        result["errors"].append({
            "type": type(error).__name__,
            "message": str(error)
        })

    return result


# =====================================================
# ANALYSE TEXTE
# =====================================================

def analyze_text(path):

    result = {
        "file": str(path.relative_to(ROOT)),
        "type": "text",
        "status": "valid",
        "lines": 0,
        "characters": 0,
        "words": 0,
        "errors": [],
        "sha256": file_hash(path)
    }

    try:

        content = path.read_text(
            encoding="utf-8"
        )

        result["lines"] = len(
            content.splitlines()
        )

        result["characters"] = len(content)

        result["words"] = len(
            content.split()
        )

    except Exception as error:

        result["status"] = "error"

        result["errors"].append({
            "type": type(error).__name__,
            "message": str(error)
        })

    return result


# =====================================================
# ANALYSEUR CENTRAL
# =====================================================

def analyze_file(relative_path):

    path = validate_path(relative_path)

    extension = path.suffix.lower()

    if extension == ".py":
        return analyze_python(path)

    if extension == ".json":
        return analyze_json(path)

    if extension == ".csv":
        return analyze_csv(path)

    return analyze_text(path)


# =====================================================
# PLANIFICATEUR
# =====================================================

def create_plan(task):

    description = str(
        task.get("description", "")
    ).strip()

    task_type = str(
        task.get("type", "analysis")
    ).lower()

    steps = []

    steps.append({
        "step": 1,
        "action": "understand",
        "description": (
            "Comprendre la demande et les objectifs."
        )
    })

    if task_type == "programming":

        steps.extend([
            {
                "step": 2,
                "action": "inspect",
                "description": (
                    "Inspecter les fichiers concernés."
                )
            },
            {
                "step": 3,
                "action": "validate",
                "description": (
                    "Vérifier la syntaxe et la structure."
                )
            },
            {
                "step": 4,
                "action": "test",
                "description": (
                    "Préparer les tests autorisés."
                )
            }
        ])

    elif task_type == "data":

        steps.extend([
            {
                "step": 2,
                "action": "collect",
                "description": (
                    "Identifier les données disponibles."
                )
            },
            {
                "step": 3,
                "action": "analyze",
                "description": (
                    "Analyser et vérifier les données."
                )
            },
            {
                "step": 4,
                "action": "report",
                "description": (
                    "Produire les résultats."
                )
            }
        ])

    elif task_type == "document":

        steps.extend([
            {
                "step": 2,
                "action": "inspect",
                "description": (
                    "Lire et analyser le document."
                )
            },
            {
                "step": 3,
                "action": "process",
                "description": (
                    "Préparer le traitement demandé."
                )
            },
            {
                "step": 4,
                "action": "report",
                "description": (
                    "Produire le résultat."
                )
            }
        ])

    else:

        steps.extend([
            {
                "step": 2,
                "action": "analyze",
                "description": (
                    "Analyser les ressources disponibles."
                )
            },
            {
                "step": 3,
                "action": "execute",
                "description": (
                    "Effectuer les opérations autorisées."
                )
            }
        ])

    steps.append({
        "step": len(steps) + 1,
        "action": "verify",
        "description": (
            "Vérifier le résultat et produire un rapport."
        )
    })

    return {
        "description": description,
        "type": task_type,
        "created_at": now(),
        "steps": steps
    }


# =====================================================
# MOTEUR D'EXÉCUTION
# =====================================================

def execute_task(task):

    started = time.time()

    task_id = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d%H%M%S%f")

    report = {
        "engine": "OPTIMUS TASK ENGINE",
        "version": VERSION,
        "task_id": task_id,
        "started_at": now(),
        "status": "running",
        "task": task,
        "plan": None,
        "results": [],
        "errors": [],
        "statistics": {}
    }

    try:

        plan = create_plan(task)

        report["plan"] = plan

        files = task.get("files", [])

        if not isinstance(files, list):

            raise ValueError(
                "Le champ files doit être une liste."
            )

        for relative_path in files:

            try:

                result = analyze_file(
                    relative_path
                )

                report["results"].append(
                    result
                )

            except Exception as error:

                report["errors"].append({
                    "file": str(relative_path),
                    "error": str(error)
                })

        has_file_errors = any(
            item["status"] == "error"
            for item in report["results"]
        )

        if report["errors"] or has_file_errors:

            report["status"] = "completed_with_errors"

        else:

            report["status"] = "completed"

    except Exception as error:

        report["status"] = "failed"

        report["errors"].append({
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc()[-2000:]
        })

    report["finished_at"] = now()

    report["statistics"] = {
        "files_analyzed": len(
            report["results"]
        ),
        "files_with_errors": sum(
            1
            for item in report["results"]
            if item["status"] == "error"
        ),
        "execution_seconds": round(
            time.time() - started,
            3
        )
    }

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = (
        REPORT_DIR /
        f"{task_id}.json"
    )

    save_json(
        report_path,
        report
    )

    history = load_json(
        HISTORY_FILE,
        {"executions": []}
    )

    history.setdefault(
        "executions",
        []
    ).append({
        "task_id": task_id,
        "status": report["status"],
        "date": report["finished_at"],
        "report": str(
            report_path.relative_to(ROOT)
        )
    })

    save_json(
        HISTORY_FILE,
        history
    )

    return report


# =====================================================
# INTERFACE DE LANCEMENT
# =====================================================

def main():

    if len(sys.argv) < 2:

        print("OPTIMUS TASK ENGINE", VERSION)

        print("Utilisation :")

        print(
            "python task_engine.py task.json"
        )

        sys.exit(2)

    task_file = Path(
        sys.argv[1]
    )

    if not task_file.is_absolute():

        task_file = ROOT / task_file

    try:

        task = json.loads(
            task_file.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(task, dict):

            raise ValueError(
                "La tâche doit être un objet JSON."
            )

        report = execute_task(task)

        print(
            json.dumps(
                report,
                indent=2,
                ensure_ascii=False
            )
        )

        if report["status"] == "failed":

            sys.exit(1)

    except Exception as error:

        print(
            "ERREUR :",
            str(error)
        )

        sys.exit(1)


# =====================================================
# DÉMARRAGE
# =====================================================

if __name__ == "__main__":
    main()
