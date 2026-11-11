import os
import re
import json
import time
import hashlib
import logging
import subprocess
import requests

from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

# ==========================================================
# OCTOPUS ULTRA
# R1 Scout | R2 Analyst | R3 Planner | R4 Builder
# R5 Coder | R6 Improver | R7 Tester | R8 Submitter
# R9 Tracker | R10 Payment Tracker
# ==========================================================

VERSION = "1.0.0"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USER = os.getenv("GITHUB_USER", "Niaina5986")

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_KEY = os.getenv("GROQ_API_KEY", "")
CLOUDFLARE_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL", "gemini-2.5-flash"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL", "llama-3.3-70b-versatile"
)

CLOUDFLARE_MODEL = os.getenv(
    "CLOUDFLARE_MODEL",
    "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
)

MAX_MISSIONS = int(os.getenv("MAX_MISSIONS", "15"))
MAX_AI_ATTEMPTS = 3

AUTO_SUBMIT = os.getenv(
    "OCTOPUS_AUTO_SUBMIT", "false"
).lower() == "true"

BASE = Path("octopus-data")
REPORTS = BASE / "reports"
SOLUTIONS = BASE / "solutions"

BASE.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)
SOLUTIONS.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | OCTOPUS | %(levelname)s | %(message)s"
)

GITHUB_API = "https://api.github.com"

session = requests.Session()
session.headers.update({
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Octopus-Ultra"
})

if GITHUB_TOKEN:
    session.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ==========================================================
# UTILITIES
# ==========================================================

def now():
    return datetime.now(timezone.utc).isoformat()


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def load_json(path, default=None):
    if not path.exists():
        return default if default is not None else {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def issue_id(issue):
    return hashlib.sha256(
        issue["html_url"].encode()
    ).hexdigest()[:16]


def github_get(url, params=None):
    response = session.get(
        url,
        params=params,
        timeout=30
    )

    if response.status_code == 403:
        raise RuntimeError(
            "GitHub rate limit ou permission insuffisante."
        )

    response.raise_for_status()
    return response.json()


# ==========================================================
# R1 — SCOUT
# Recherche de missions GitHub
# ==========================================================

SEARCH_QUERIES = [
    'is:issue is:open "bounty"',
    'is:issue is:open "reward"',
    'is:issue is:open "paid"',
    'is:issue is:open "help wanted"',
    'is:issue is:open "good first issue"',
    'is:issue is:open "cash reward"',
    'is:issue is:open "sponsorship"'
]


def scout():
    logging.info("R1: Recherche des missions.")

    missions = {}

    for query in SEARCH_QUERIES:

        try:
            data = github_get(
                f"{GITHUB_API}/search/issues",
                {
                    "q": query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": 30
                }
            )

            for issue in data.get("items", []):

                if "pull_request" in issue:
                    continue

                if issue.get("locked"):
                    continue

                if issue.get("state") != "open":
                    continue

                identifier = issue_id(issue)

                missions[identifier] = issue

            time.sleep(1)

        except Exception as error:
            logging.warning(
                f"Recherche échouée: {error}"
            )

    result = list(missions.values())

    logging.info(
        f"R1: {len(result)} missions découvertes."
    )

    return result


# ==========================================================
# R2 — ANALYST
# Évaluation des missions
# ==========================================================

PAYMENT_WORDS = [
    "bounty", "reward", "paid", "payment",
    "usd", "dollar", "$", "sponsor",
    "cash", "prize"
]

TASK_WORDS = [
    "implement", "fix", "build", "create",
    "develop", "improve", "bug", "feature",
    "documentation", "test", "code"
]


def analyze(issue):

    title = issue.get("title", "")
    body = issue.get("body") or ""

    text = f"{title}\n{body}".lower()

    score = 0

    for word in PAYMENT_WORDS:
        if word in text:
            score += 2

    for word in TASK_WORDS:
        if word in text:
            score += 1

    if issue.get("comments", 0) > 0:
        score += 1

    if len(body) > 200:
        score += 1

    labels = [
        label.get("name", "").lower()
        for label in issue.get("labels", [])
    ]

    if "help wanted" in labels:
        score += 2

    if "good first issue" in labels:
        score += 1

    payment_detected = any(
        word in text for word in PAYMENT_WORDS
    )

    return {
        "score": min(score, 15),
        "payment_detected": payment_detected,
        "payment_verified": False,
        "status": (
            "POTENTIELLEMENT_PAYEE"
            if payment_detected
            else "REMUNERATION_NON_CONFIRMEE"
        )
    }


# ==========================================================
# R3 — PLANNER
# Préparation du travail
# ==========================================================

def planner(issue, analysis):

    return {
        "objective": issue.get("title"),
        "repository": issue["repository_url"],
        "issue_url": issue["html_url"],
        "requirements": issue.get("body") or "",
        "score": analysis["score"],
        "payment_status": analysis["status"],
        "created_at": now()
    }


# ==========================================================
# AI PROVIDERS
# Gemini -> Groq -> Cloudflare
# ==========================================================

def ask_gemini(prompt):

    if not GEMINI_KEY:
        raise RuntimeError("Gemini indisponible")

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{GEMINI_MODEL}:generateContent"
    )

    response = requests.post(
        url,
        params={"key": GEMINI_KEY},
        json={
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 6000
            }
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]


def ask_groq(prompt):

    if not GROQ_KEY:
        raise RuntimeError("Groq indisponible")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}"
        },
        json={
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a careful software engineer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 6000
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def ask_cloudflare(prompt):

    if not CLOUDFLARE_TOKEN or not CLOUDFLARE_ACCOUNT:
        raise RuntimeError("Cloudflare indisponible")

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT}/ai/run/{CLOUDFLARE_MODEL}"
    )

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {CLOUDFLARE_TOKEN}"
        },
        json={
            "messages": [
                {
                    "role": "system",
                    "content": "You are a careful software engineer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        raise RuntimeError("Cloudflare AI a échoué")

    return data["result"]["response"]


def ask_ai(prompt):

    providers = [
        ("Gemini", ask_gemini),
        ("Groq", ask_groq),
        ("Cloudflare", ask_cloudflare)
    ]

    errors = []

    for name, provider in providers:

        for attempt in range(MAX_AI_ATTEMPTS):

            try:
                logging.info(
                    f"IA: tentative {name}, essai {attempt + 1}"
                )

                result = provider(prompt)

                if result and len(result.strip()) > 20:
                    logging.info(f"IA utilisée: {name}")
                    return result, name

            except Exception as error:

                errors.append(
                    f"{name}: {str(error)[:300]}"
                )

                logging.warning(
                    f"{name}: {error}"
                )

                time.sleep(2 ** attempt)

                break

    raise RuntimeError(
        "Tous les moteurs IA ont échoué: "
        + " | ".join(errors)
    )


# ==========================================================
# R4 — BUILDER
# Génération d'une solution
# ==========================================================

def builder(plan):

    prompt = f"""
You are a senior open-source software engineer.

Analyze this GitHub issue and propose a real solution.

ISSUE:
{plan['objective']}

REPOSITORY:
{plan['repository']}

REQUIREMENTS:
{plan['requirements']}

IMPORTANT RULES:
- Do not invent requirements.
- Do not claim that tests passed when they were not run.
- Do not expose credentials or secrets.
- Never modify GitHub Actions workflows.
- Never modify authentication or security files.
- Prefer a small, focused change.
- If the task is unclear, explain why it cannot be solved safely.

Return ONLY valid JSON in this format:

{{
  "can_solve": true,
  "reason": "Explanation",
  "files": [
    {{
      "path": "src/example.py",
      "content": "Complete file content"
    }}
  ],
  "tests": [
    "python -m py_compile src/example.py"
  ],
  "summary": "Description of the solution"
}}

Do not use Markdown code fences.
"""

    answer, provider = ask_ai(prompt)

    return answer, provider


# ==========================================================
# R5 — CODER
# Extraction et création des fichiers
# ==========================================================

def extract_json(text):

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```$",
        "",
        text
    )

    start = text.find("{")
    end = text.rfind("}")

    if start < 0 or end < start:
        raise ValueError("JSON IA invalide")

    return json.loads(text[start:end + 1])


FORBIDDEN_PATHS = [
    ".github/workflows/",
    ".git/",
    ".env",
    "secrets",
    "credentials",
    "id_rsa",
    "id_ed25519"
]


def valid_path(path):

    path = str(path).replace("\\", "/")

    if path.startswith("/"):
        return False

    parts = Path(path).parts

    if ".." in parts:
        return False

    lowered = path.lower()

    if any(
        forbidden in lowered
        for forbidden in FORBIDDEN_PATHS
    ):
        return False

    if not re.fullmatch(
        r"[A-Za-z0-9_./ -]+",
        path
    ):
        return False

    return True


def coder(solution, identifier):

    if not solution.get("can_solve"):
        raise RuntimeError(
            solution.get("reason", "Mission non résoluble")
        )

    files = solution.get("files", [])

    if not files or len(files) > 10:
        raise RuntimeError("Nombre de fichiers invalide")

    destination = SOLUTIONS / identifier

    destination.mkdir(
        parents=True,
        exist_ok=True
    )

    saved = []

    for item in files:

        path = item.get("path", "")
        content = item.get("content", "")

        if not valid_path(path):
            raise RuntimeError(
                f"Chemin interdit: {path}"
            )

        if not isinstance(content, str):
            raise RuntimeError("Contenu de fichier invalide")

        if len(content) > 100000:
            raise RuntimeError("Fichier trop volumineux")

        target = destination / path

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target.write_text(
            content,
            encoding="utf-8"
        )

        saved.append(path)

    return saved


# ==========================================================
# R6 — IMPROVER
# Vérification et amélioration
# ==========================================================

def improver(plan, files):

    prompt = f"""
Review the following proposed software changes.

TASK:
{plan['objective']}

FILES:
{json.dumps(files, ensure_ascii=False)}

Identify:
- obvious bugs
- incomplete requirements
- security problems
- unnecessary changes

Return JSON only:

{{
  "approved_for_testing": true,
  "problems": [],
  "improvements": [],
  "explanation": "..."
}}

Do not claim that tests were executed.
"""

    answer, provider = ask_ai(prompt)

    return extract_json(answer), provider


# ==========================================================
# R7 — TESTER
# Contrôles locaux sans exécuter du code non fiable
# ==========================================================

def tester(identifier, files):

    directory = SOLUTIONS / identifier

    results = {
        "passed": True,
        "checks": [],
        "warnings": []
    }

    for path in files:

        file_path = directory / path

        if not file_path.exists():
            results["passed"] = False
            results["checks"].append(
                f"Fichier manquant: {path}"
            )
            continue

        if file_path.stat().st_size == 0:
            results["passed"] = False
            results["checks"].append(
                f"Fichier vide: {path}"
            )
            continue

        if file_path.suffix == ".py":

            try:
                import ast

                ast.parse(
                    file_path.read_text(
                        encoding="utf-8"
                    )
                )

                results["checks"].append(
                    f"Syntaxe Python valide: {path}"
                )

            except Exception as error:

                results["passed"] = False

                results["checks"].append(
                    f"Erreur Python: {path}: {error}"
                )

    results["warnings"].append(
        "Les tests fonctionnels du projet n'ont pas été exécutés."
    )

    return results


# ==========================================================
# R8 — SUBMITTER
# Préparation des soumissions
# ==========================================================

def submitter(issue, identifier, solution, tests):

    result = {
        "submitted": False,
        "status": "PREPARED",
        "message": "Soumission non activée.",
        "issue_url": issue["html_url"]
    }

    if not AUTO_SUBMIT:
        return result

    result["status"] = "MANUAL_REVIEW_REQUIRED"

    result["message"] = (
        "Soumission automatique non disponible pour cette "
        "mission dans cette version. Vérifier les permissions "
        "du dépôt cible et les conditions de contribution."
    )

    return result


# ==========================================================
# R9 — TRACKER
# Suivi des missions et des résultats
# ==========================================================

def tracker(record):

    history_path = BASE / "history.json"

    history = load_json(
        history_path,
        []
    )

    if not isinstance(history, list):
        history = []

    history.append(record)

    save_json(
        history_path,
        history[-2000:]
    )


# ==========================================================
# R10 — PAYMENT TRACKER
# Suivi des récompenses
# ==========================================================

def payment_tracker(issue, analysis):

    return {
        "payment_detected": analysis["payment_detected"],
        "payment_verified": False,
        "amount": None,
        "currency": None,
        "payment_received": False,
        "verification": (
            "À vérifier manuellement auprès de l'organisateur."
        )
    }


# ==========================================================
# COMPLETE MISSION PIPELINE
# ==========================================================

def process_mission(issue):

    identifier = issue_id(issue)

    logging.info(
        f"Traitement: {issue.get('title')}"
    )

    # R2
    analysis = analyze(issue)

    if analysis["score"] < 3:
        logging.info("Mission ignorée: score insuffisant.")
        return None

    # R3
    plan = planner(issue, analysis)

    # R4
    raw_solution, provider = builder(plan)

    solution = extract_json(raw_solution)

    if not solution.get("can_solve"):
        raise RuntimeError(
            solution.get("reason", "Solution refusée")
        )

    # R5
    files = coder(solution, identifier)

    # R6
    improvement, improvement_provider = improver(
        plan,
        solution.get("files", [])
    )

    # R7
    tests = tester(identifier, files)

    if not tests["passed"]:
        raise RuntimeError("Les contrôles ont échoué.")

    if not improvement.get("approved_for_testing"):
        raise RuntimeError(
            "L'IA recommande de ne pas valider cette solution."
        )

    # R8
    submission = submitter(
        issue,
        identifier,
        solution,
        tests
    )

    # R10
    payment = payment_tracker(
        issue,
        analysis
    )

    record = {
        "id": identifier,
        "title": issue["title"],
        "url": issue["html_url"],
        "repository": issue["repository_url"],
        "score": analysis["score"],
        "provider": provider,
        "improvement_provider": improvement_provider,
        "files": files,
        "summary": solution.get("summary"),
        "analysis": analysis,
        "improvement": improvement,
        "tests": tests,
        "submission": submission,
        "payment": payment,
        "created_at": now()
    }

    save_json(
        REPORTS / f"{identifier}.json",
        record
    )

    tracker(record)

    return record


# ==========================================================
# MAIN
# ==========================================================

def main():

    logging.info(
        f"========== OCTOPUS ULTRA {VERSION} =========="
    )

    missions = scout()

    missions.sort(
        key=lambda item: analyze(item)["score"],
        reverse=True
    )

    processed = 0

    for issue in missions:

        if processed >= MAX_MISSIONS:
            break

        identifier = issue_id(issue)

        report_path = REPORTS / f"{identifier}.json"

        if report_path.exists():
            continue

        try:

            result = process_mission(issue)

            if result:
                processed += 1

        except Exception as error:

            logging.exception(
                f"Mission échouée: {issue.get('html_url')}"
            )

            failure = {
                "id": identifier,
                "title": issue.get("title"),
                "url": issue.get("html_url"),
                "status": "FAILED_OR_REQUIRES_REVIEW",
                "error": str(error),
                "created_at": now()
            }

            save_json(
                REPORTS / f"{identifier}_error.json",
                failure
            )

        time.sleep(2)

    summary = {
        "version": VERSION,
        "date": now(),
        "discovered": len(missions),
        "processed": processed,
        "auto_submit": AUTO_SUBMIT,
        "providers": {
            "gemini": bool(GEMINI_KEY),
            "groq": bool(GROQ_KEY),
            "cloudflare": bool(CLOUDFLARE_TOKEN)
        }
    }

    save_json(
        REPORTS / "latest.json",
        summary
    )

    logging.info(
        "========== OCTOPUS TERMINÉ =========="
    )

    logging.info(
        json.dumps(summary, indent=2)
    )


if __name__ == "__main__":
    main()
