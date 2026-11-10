#!/usr/bin/env python3
# ============================================================
# OPTIMUS V3 - EXECUTION ET RAPPORT CENTRAL
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
import base64

from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent

TASK_FILE = ROOT / "optimus-missions.json"
WORK_DIR = ROOT / "optimus-v3-workspaces"
REPORT_DIR = ROOT / "optimus-v3-reports"
REPORT_FILE = REPORT_DIR / "latest.json"

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

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def current_date():

    return datetime.now(timezone.utc).isoformat()


# ============================================================
# 2. ENREGISTREMENT DU RAPPORT
# ============================================================

def save_report(report):

    initialize()

    temporary_file = REPORT_DIR / "latest.tmp"

    temporary_file.write_text(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    temporary_file.replace(REPORT_FILE)

    print(json.dumps(
        report,
        indent=4,
        ensure_ascii=False
    ))


def create_error_report(status, message):

    return {
        "system": "OPTIMUS AI",
        "version": "3.0",
        "date": current_date(),
        "status": status,
        "error": str(message),
        "total": 0,
        "successful": 0,
        "failed": 0,
        "missions": []
    }


# ============================================================
# 3. SECURITE DES FICHIERS
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
# 4. CREATION DES LIVRABLES
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
# 5. EXECUTION DES PROGRAMMES PYTHON
# ============================================================

def execute_python(path):

    if path.suffix != ".py":

        return {
            "file": path.name,
            "status": "NOT_EXECUTABLE"
        }

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
            "status": "TIMEOUT",
            "error": "Temps maximal dépassé."
        }

    except Exception as error:

        return {
            "file": path.name,
            "status": "ERROR",
            "error": str(error)
        }


# ============================================================
# 6. CONTROLE QUALITE
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
                    path.read_text(encoding="utf-8")
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
# 7. SOUMISSION GITHUB
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

        for path in files:

            relative = path.relative_to(folder)

            destination = (
                "optimus-deliverables/"
                + mission_id
                + "/"
                + str(relative)
            )

            encoded_content = base64.b64encode(
                path.read_bytes()
            ).decode("ascii")

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
                "content=" + encoded_content
            ])

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
            "error": (error.stderr or str(error))[-3000:]
        }

    except Exception as error:

        return {
            "status": "SUBMISSION_FAILED",
            "error": str(error)
        }


# ============================================================
# 8. EXECUTION D'UNE MISSION
# ============================================================

def execute_mission(mission):

    started = time.time()

    report = {
        "mission_id": mission.get("id"),
        "title": mission.get("title"),
        "status": "STARTED"
    }

    try:

        if not isinstance(mission, dict):
            raise ValueError("Mission invalide.")

        generated = mission.get("generated")

        if not generated:
            raise ValueError(
                "Aucun livrable généré dans la mission."
            )

        folder, files = save_generated_files(
            mission,
            generated
        )

        tests = test_programs(files)

        report["tests"] = tests

        report["files"] = [
            str(path.relative_to(ROOT))
            for path in files
        ]

        if not quality_passed(tests):

            report["status"] = "TEST_FAILED"

        else:

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
# 9. CONTROLEUR CENTRAL
# ============================================================

def main():

    initialize()

    # --------------------------------------------------------
    # CAS 1 : FICHIER DES MISSIONS ABSENT
    # --------------------------------------------------------

    if not TASK_FILE.exists():

        report = create_error_report(
            "WAITING_FOR_MISSIONS",
            "Fichier optimus-missions.json absent."
        )

        save_report(report)
        return

    # --------------------------------------------------------
    # CAS 2 : LECTURE DU FICHIER DES MISSIONS
    # --------------------------------------------------------

    try:

        data = json.loads(
            TASK_FILE.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, dict):
            raise ValueError("Format JSON invalide.")

        missions = data.get("missions", [])

        if not isinstance(missions, list):
            raise ValueError(
                "Le champ missions doit être une liste."
            )

    except Exception as error:

        report = create_error_report(
            "INPUT_ERROR",
            error
        )

        save_report(report)
        return

    # --------------------------------------------------------
    # CAS 3 : AUCUNE MISSION
    # --------------------------------------------------------

    if not missions:

        report = {
            "system": "OPTIMUS AI",
            "version": "3.0",
            "date": current_date(),
            "status": "NO_MISSIONS",
            "total": 0,
            "successful": 0,
            "failed": 0,
            "missions": []
        }

        save_report(report)
        return

    # --------------------------------------------------------
    # CAS 4 : EXECUTION DES MISSIONS
    # --------------------------------------------------------

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

            try:

                reports.append(future.result())

            except Exception as error:

                reports.append({
                    "status": "FAILED",
                    "error": str(error)
                })

    # --------------------------------------------------------
    # CAS 5 : RAPPORT FINAL
    # --------------------------------------------------------

    successful = sum(
        r.get("status") == "SUCCESS"
        for r in reports
    )

    failed = sum(
        r.get("status") in (
            "FAILED",
            "TEST_FAILED"
        )
        for r in reports
    )

    final_report = {

        "system": "OPTIMUS AI",

        "version": "3.0",

        "date": current_date(),

        "status": (
            "SUCCESS"
            if failed == 0
            else "PARTIAL_FAILURE"
        ),

        "total": len(reports),

        "successful": successful,

        "failed": failed,

        "missions": reports

    }

    save_report(final_report)


# ============================================================
# 10. DEMARRAGE
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as error:

        initialize()

        report = create_error_report(
            "FATAL_ERROR",
            error
        )

        save_report(report)

        sys.exit(1)