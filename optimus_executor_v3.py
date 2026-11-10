#!/usr/bin/env python3
# ============================================================
# OPTIMUS V3 - EXECUTION ET SOUMISSION
# ============================================================

import os
import re
import sys
import json
import time
import shutil
import hashlib
import subprocess
import concurrent.futures

from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent

TASK_FILE = ROOT / "optimus-missions.json"
WORK_DIR = ROOT / "optimus-v3-workspaces"
REPORT_DIR = ROOT / "optimus-v3-reports"

MAX_WORKERS = 2
MAX_RUNTIME = 60
MAX_FILES = 10
MAX_FILE_SIZE = 100_000

ALLOWED_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
    ".json",
    ".csv"
}


# ============================================================
# 1. INITIALISATION
# ============================================================

def initialize():

    WORK_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. SECURITE DES FICHIERS
# ============================================================

def safe_name(name):

    name = str(name)

    if not re.fullmatch(
        r"[a-zA-Z0-9_.-]+",
        name
    ):
        raise ValueError("Nom de fichier interdit.")

    if name.startswith(".") or ".." in name:
        raise ValueError("Chemin interdit.")

    return name


# ============================================================
# 3. GENERATION DES LIVRABLES
# ============================================================

def save_generated_files(mission, generated):

    mission_id = safe_name(mission["id"])

    folder = WORK_DIR / mission_id

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    files = generated.get("files", [])

    if not isinstance(files, list) or len(files) > MAX_FILES:
        raise ValueError("Liste de fichiers invalide.")

    created = []

    for item in files:

        name = safe_name(item["name"])

        path = Path(name)

        if path.suffix not in ALLOWED_EXTENSIONS:
            raise ValueError("Extension interdite.")

        content = item.get("content", "")

        if not isinstance(content, str):
            raise ValueError("Contenu invalide.")

        if len(content) > MAX_FILE_SIZE:
            raise ValueError("Fichier trop volumineux.")

        destination = folder / name

        destination.write_text(
            content,
            encoding="utf-8"
        )

        created.append(destination)

    return folder, created


# ============================================================
# 4. EXECUTION DES PROGRAMMES PYTHON
# ============================================================

def execute_python(path):

    if path.suffix != ".py":
        return {
            "file": path.name,
            "status": "NOT_EXECUTABLE"
        }

    # Ne pas transmettre les secrets GitHub ou API
    # aux programmes générés.

    safe_env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1"
    }

    try:

        result = subprocess.run(
            [sys.executable, "-I", str(path)],
            cwd=str(path.parent),
            env=safe_env,
            capture_output=True,
            text=True,
            timeout=MAX_RUNTIME,
            shell=False
        )

        return {
            "file": path.name,
            "status": (
                "SUCCESS"
                if result.returncode == 0
                else "FAILED"
            ),
            "return_code": result.returncode,
            "stdout": result.stdout[-5000:],
            "stderr": result.stderr[-5000:]
        }

    except subprocess.TimeoutExpired:

        return {
            "file": path.name,
            "status": "TIMEOUT"
        }

    except Exception as error:

        return {
            "file": path.name,
            "status": "ERROR",
            "error": str(error)
        }


# ============================================================
# 5. TESTS ET CONTROLE QUALITE
# ============================================================

def test_programs(files):

    results = []

    for path in files:

        if path.suffix == ".py":

            results.append(
                execute_python(path)
            )

        elif path.suffix == ".json":

            try:

                json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )

                results.append({
                    "file": path.name,
                    "status": "SUCCESS"
                })

            except Exception as error:

                results.append({
                    "file": path.name,
                    "status": "FAILED",
                    "error": str(error)
                })

        else:

            results.append({
                "file": path.name,
                "status": "CREATED"
            })

    return results


def quality_passed(results):

    return all(
        result["status"] in (
            "SUCCESS",
            "CREATED"
        )
        for result in results
    )


# ============================================================
# 6. SOUMISSION GITHUB
# ============================================================

def submit_github(mission, folder, files):

    token = os.environ.get("GH_SUBMIT_TOKEN")

    repository = os.environ.get(
        "OPTIMUS_TARGET_REPOSITORY"
    )

    if not token or not repository:

        return {
            "status": "WAITING_CONFIGURATION",
            "message": (
                "GH_SUBMIT_TOKEN ou "
                "OPTIMUS_TARGET_REPOSITORY absent."
            )
        }

    if not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
        repository
    ):
        raise ValueError("Dépôt GitHub invalide.")

    if not shutil.which("gh"):

        return {
            "status": "ERROR",
            "message": "GitHub CLI non installé."
        }

    mission_id = safe_name(mission["id"])

    branch = (
        "optimus/"
        + mission_id.lower()
        + "-"
        + hashlib.sha256(
            mission_id.encode()
        ).hexdigest()[:6]
    )

    safe_env = os.environ.copy()

    # Le token est transmis uniquement au processus gh,
    # jamais au programme Python généré.

    safe_env["GH_TOKEN"] = token

    def run_gh(command):

        return subprocess.run(
            ["gh"] + command,
            cwd=str(ROOT),
            env=safe_env,
            capture_output=True,
            text=True,
            timeout=60,
            check=True
        )

    try:

        # Créer une branche de travail

        run_gh([
            "api",
            "-X",
            "POST",
            f"repos/{repository}/git/refs",
            "-f",
            "ref=refs/heads/" + branch,
            "-f",
            "sha=" + os.environ["GITHUB_SHA"]
        ])

        # Ajouter les fichiers dans la branche

        for path in files:

            relative = path.relative_to(folder)

            destination = (
                "optimus-deliverables/"
                + mission_id
                + "/"
                + str(relative)
            )

            run_gh([
                "api",
                "-X",
                "PUT",
                f"repos/{repository}/contents/{destination}",
                "-f",
                "message=OPTIMUS: " + mission_id,
                "-f",
                "branch=" + branch,
                "-f",
                "content=" + path.read_text(
                    encoding="utf-8"
                )
            ])

        # Créer la Pull Request

        response = run_gh([
            "pr",
            "create",
            "--repo",
            repository,
            "--base",
            "main",
            "--head",
            branch,
            "--title",
            "OPTIMUS - " + mission.get("title", mission_id),
            "--body",
            (
                "Livrables générés et testés par OPTIMUS.\n\n"
                "Mission : " + mission_id + "\n\n"
                "Cette Pull Request nécessite une revue."
            )
        ])

        return {
            "status": "SUBMITTED",
            "pull_request": response.stdout.strip()
        }

    except subprocess.CalledProcessError as error:

        return {
            "status": "SUBMISSION_FAILED",
            "error": error.stderr[-3000:]
        }


# ============================================================
# 7. EXECUTION COMPLETE D'UNE MISSION
# ============================================================

def execute_mission(mission):

    started = time.time()

    report = {
        "mission_id": mission.get("id"),
        "title": mission.get("title"),
        "status": "STARTED"
    }

    try:

        # Les livrables doivent être fournis par V2
        # ou par un autre département de production.

        generated = mission.get("generated")

        if not generated:

            raise ValueError(
                "Aucun livrable généré dans la mission."
            )

        folder, files = save_generated_files(
            mission,
            generated
        )

        # Exécution

        tests = test_programs(files)

        report["tests"] = tests

        # Interdiction de soumettre en cas d'échec

        if not quality_passed(tests):

            report["status"] = "TEST_FAILED"

            return report

        # Soumission GitHub

        if mission.get("submit_github") is True:

            submission = submit_github(
                mission,
                folder,
                files
            )

        else:

            submission = {
                "status": "NOT_REQUESTED"
            }

        report["submission"] = submission

        report["files"] = [
            str(path.relative_to(ROOT))
            for path in files
        ]

        report["status"] = "SUCCESS"

    except Exception as error:

        report["status"] = "FAILED"

        report["error"] = str(error)

    report["duration"] = round(
        time.time() - started,
        2
    )

    return report


# ============================================================
# 8. CONTROLEUR CENTRAL
# ============================================================

def main():

    initialize()

    if not TASK_FILE.exists():

        print("Fichier optimus-missions.json absent.")

        return

    data = json.loads(
        TASK_FILE.read_text(
            encoding="utf-8"
        )
    )

    missions = data.get("missions", [])

    reports = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = [
            executor.submit(
                execute_mission,
                mission
            )
            for mission in missions
        ]

        for future in concurrent.futures.as_completed(futures):

            reports.append(future.result())

    final_report = {

        "system": "OPTIMUS AI",

        "version": "3.0",

        "date": datetime.now(
            timezone.utc
        ).isoformat(),

        "total": len(reports),

        "successful": sum(
            r["status"] == "SUCCESS"
            for r in reports
        ),

        "failed": sum(
            r["status"] == "FAILED"
            for r in reports
        ),

        "missions": reports
    }

    (REPORT_DIR / "latest.json").write_text(
        json.dumps(
            final_report,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print(json.dumps(
        final_report,
        indent=4,
        ensure_ascii=False
    ))


if __name__ == "__main__":
    main()