#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OPTIMUS AI
Moteur central de recherche, analyse et exécution de missions GitHub.

Version : 1.0.0
Dépendances : bibliothèque standard Python uniquement.

Capacités :
- Recherche de missions avec récompense annoncée.
- Analyse des conditions de sécurité.
- Lecture de contrats d'exécution précis.
- Modification contrôlée de fichiers texte.
- Création de branches et Pull Requests.
- Exécution parallèle.
- Historique persistant.
- Tableau de bord JSON.

ATTENTION :
Une récompense annoncée n'est pas une garantie de paiement.
Un Pull Request n'est pas une preuve d'acceptation.
"""

import os
import re
import json
import time
import base64
import hashlib
import threading
import urllib.request
import urllib.error

from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================
# CONFIGURATION
# ============================================================

VERSION = "1.0.0"

GITHUB_API = "https://api.github.com"

SEARCH_TOKEN = os.getenv("GITHUB_TOKEN", "")
WRITE_TOKEN = os.getenv(
    "AUTONOMOUS_GITHUB_TOKEN",
    SEARCH_TOKEN
)

OWNER = os.getenv("GITHUB_OWNER", "")
MIN_REWARD = float(os.getenv("MIN_REWARD_USD", "10"))

MAX_ISSUES = int(os.getenv("MAX_ISSUES", "100"))
MAX_WORKERS = int(os.getenv("OPTIMUS_WORKERS", "4"))

STATE_FILE = "optimus-state.json"
REPORT_FILE = "optimus-reports/run.json"
DASHBOARD_FILE = "db.json"

USER_AGENT = "OPTIMUS-AI/1.0"

LOCK = threading.Lock()


# ============================================================
# OUTILS
# ============================================================

def now():
    return datetime.now(timezone.utc).isoformat()


def log(message):
    print(f"[{now()}] {message}", flush=True)


def safe_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def issue_id(issue):
    return f"{issue.get('repository', '')}#{issue.get('number', '')}"


def make_id(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()[:16]


def load_json(path, default):
    if not os.path.exists(path):
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    folder = os.path.dirname(path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    temporary = path + ".tmp"

    with open(temporary, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    os.replace(temporary, path)


# ============================================================
# GITHUB API
# ============================================================

def github_request(
    method,
    endpoint,
    token=None,
    payload=None,
    allow_404=False
):

    url = endpoint

    if not url.startswith("http"):
        url = GITHUB_API + endpoint

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=35
        ) as response:

            content = response.read().decode("utf-8")

            if not content:
                return {}

            return json.loads(content)

    except urllib.error.HTTPError as error:

        body = error.read().decode(
            "utf-8",
            errors="replace"
        )

        if allow_404 and error.code == 404:
            return None

        raise RuntimeError(
            f"GitHub HTTP {error.code}: {body[:500]}"
        )

    except Exception as error:
        raise RuntimeError(str(error))


# ============================================================
# RECHERCHE DE MISSIONS
# ============================================================

SEARCH_QUERIES = [
    'is:issue is:open bounty "$"',
    'is:issue is:open reward "$"',
    'is:issue is:open paid "$"',
    'is:issue is:open "$" bounty',
]


def search_issues():

    if not SEARCH_TOKEN:
        log("GITHUB_TOKEN absent : recherche publique limitée.")

    found = {}

    for query in SEARCH_QUERIES:

        endpoint = (
            "/search/issues?q="
            + urllib.parse.quote(query)
            + "&per_page=100"
            + "&sort=created"
            + "&order=desc"
        )

        try:

            result = github_request(
                "GET",
                endpoint,
                SEARCH_TOKEN or None
            )

            for item in result.get("items", []):

                if "pull_request" in item:
                    continue

                repository_url = item.get(
                    "repository_url",
                    ""
                )

                repository = repository_url.replace(
                    "https://api.github.com/repos/",
                    ""
                )

                item["repository"] = repository

                key = issue_id(item)

                found[key] = item

        except Exception as error:
            log(f"Recherche impossible : {error}")

        time.sleep(1)

    return list(found.values())[:MAX_ISSUES]


# ============================================================
# ANALYSE DES RÉCOMPENSES
# ============================================================

def extract_reward(text):

    patterns = [
        r"\$\s*([0-9]+(?:\.[0-9]{1,2})?)",
        r"([0-9]+(?:\.[0-9]{1,2})?)\s*USD",
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:
            values.append(safe_float(match))

    if not values:
        return 0

    return max(values)


# ============================================================
# FILTRES DE SÉCURITÉ
# ============================================================

UNSAFE_TERMS = [
    "steal credentials",
    "steal password",
    "private key",
    "seed phrase",
    "crypto wallet recovery",
    "phishing",
    "malware",
    "ransomware",
    "keylogger",
    "captcha bypass",
    "bypass captcha",
    "account takeover",
    "deposit to unlock",
    "send money first",
    "pay upfront",
]


def safety_check(text):

    lowered = text.lower()

    for term in UNSAFE_TERMS:

        if term in lowered:

            return False, (
                "Mission écartée : contenu à risque "
                f"({term})."
            )

    return True, "Analyse de sécurité réussie."


# ============================================================
# CONTRAT D'EXÉCUTION
# ============================================================

def extract_contract(text):

    """
    Format accepté :

    <!-- OPTIMUS-TASK
    {
      "type": "replace_text",
      "path": "docs/example.md",
      "old": "Ancien texte",
      "new": "Nouveau texte"
    }
    -->

    Ancien format accepté :

    <!-- AUTO-EARN-AUTOFIX
    {
      "type": "replace_text",
      "path": "docs/example.md",
      "old": "Ancien texte",
      "new": "Nouveau texte"
    }
    -->
    """

    patterns = [
        r"<!--\s*OPTIMUS-TASK\s*(\{.*?\})\s*-->",
        r"<!--\s*AUTO-EARN-AUTOFIX\s*(\{.*?\})\s*-->",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.DOTALL
        )

        if not match:
            continue

        try:
            contract = json.loads(match.group(1))

            return contract

        except Exception:
            return None

    return None


def validate_contract(contract):

    if not isinstance(contract, dict):
        return False, "Contrat invalide."

    if contract.get("type") != "replace_text":
        return False, "Type d'exécution non supporté."

    path = contract.get("path", "")
    old = contract.get("old")
    new = contract.get("new")

    if not isinstance(path, str):
        return False, "Chemin invalide."

    if not isinstance(old, str) or not old:
        return False, "Texte source absent."

    if not isinstance(new, str):
        return False, "Nouveau texte invalide."

    if len(old) > 20000 or len(new) > 20000:
        return False, "Modification trop volumineuse."

    if path.startswith("/"):
        return False, "Chemin absolu interdit."

    if "\\" in path:
        return False, "Chemin invalide."

    parts = path.split("/")

    if any(part in ("", ".", "..") for part in parts):
        return False, "Chemin non autorisé."

    if not path.endswith((".md", ".txt", ".rst")):
        return False, "Extension non autorisée."

    return True, "Contrat valide."


# ============================================================
# HISTORIQUE
# ============================================================

def load_state():

    return load_json(
        STATE_FILE,
        {
            "version": VERSION,
            "created_at": now(),
            "tasks": {},
            "history": []
        }
    )


def update_state(key, data):

    with LOCK:

        state = load_state()

        state["tasks"][key] = data

        state["history"].append({
            "id": key,
            "status": data.get("status"),
            "updated_at": now()
        })

        state["history"] = state["history"][-500:]

        state["updated_at"] = now()

        save_json(STATE_FILE, state)


def already_processed(key):

    state = load_state()

    previous = state.get("tasks", {}).get(key, {})

    status = previous.get("status")

    return status in [
        "submitted",
        "accepted",
        "paid"
    ]


# ============================================================
# FORK ET BRANCHES
# ============================================================

def get_or_create_fork(repository):

    if not WRITE_TOKEN:
        raise RuntimeError(
            "AUTONOMOUS_GITHUB_TOKEN absent."
        )

    configured_fork = os.getenv("AUTONOMOUS_FORK", "")

    if configured_fork:
        fork = configured_fork
    else:

        fork_data = github_request(
            "POST",
            f"/repos/{repository}/forks",
            WRITE_TOKEN,
            {}
        )

        fork = fork_data.get("full_name")

        if not fork:
            raise RuntimeError("Fork GitHub non créé.")

    # Attendre que le fork soit disponible.

    for _ in range(10):

        try:

            repo_data = github_request(
                "GET",
                f"/repos/{fork}",
                WRITE_TOKEN
            )

            if repo_data:
                return fork, repo_data

        except Exception:
            time.sleep(3)

    raise RuntimeError("Fork non accessible.")


def create_branch(fork, base_branch, branch_name):

    fork_data = github_request(
        "GET",
        f"/repos/{fork}/branches/{base_branch}",
        WRITE_TOKEN
    )

    sha = fork_data["commit"]["sha"]

    existing = github_request(
        "GET",
        f"/repos/{fork}/git/ref/heads/{branch_name}",
        WRITE_TOKEN,
        allow_404=True
    )

    if existing:
        raise RuntimeError(
            "La branche existe déjà. "
            "Nouvelle exécution bloquée."
        )

    github_request(
        "POST",
        f"/repos/{fork}/git/refs",
        WRITE_TOKEN,
        {
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
    )


# ============================================================
# LECTURE ET MODIFICATION DU FICHIER
# ============================================================

def get_file(repository, path, ref):

    encoded_path = urllib.parse.quote(
        path,
        safe="/"
    )

    result = github_request(
        "GET",
        f"/repos/{repository}/contents/{encoded_path}"
        f"?ref={urllib.parse.quote(ref)}",
        WRITE_TOKEN,
        allow_404=True
    )

    if not result:
        return None, None

    if result.get("type") != "file":
        raise RuntimeError("Le chemin ne correspond pas à un fichier.")

    content = base64.b64decode(
        result["content"]
    ).decode("utf-8")

    return content, result.get("sha")


def write_file(
    fork,
    path,
    branch,
    content,
    existing_sha
):

    encoded_path = urllib.parse.quote(
        path,
        safe="/"
    )

    payload = {
        "message": "OPTIMUS AI: automated documentation improvement",
        "content": base64.b64encode(
            content.encode("utf-8")
        ).decode("ascii"),
        "branch": branch
    }

    if existing_sha:
        payload["sha"] = existing_sha

    return github_request(
        "PUT",
        f"/repos/{fork}/contents/{encoded_path}",
        WRITE_TOKEN,
        payload
    )


# ============================================================
# EXÉCUTION D'UNE MISSION
# ============================================================

def execute_task(issue):

    repository = issue.get("repository", "")
    number = issue.get("number")
    title = issue.get("title", "")
    body = issue.get("body") or ""
    url = issue.get("html_url", "")

    key = issue_id(issue)

    result = {
        "id": key,
        "repository": repository,
        "number": number,
        "title": title,
        "url": url,
        "reward_usd": extract_reward(title + "\n" + body),
        "status": "pending",
        "updated_at": now()
    }

    try:

        if already_processed(key):

            result["status"] = "already_processed"

            return result

        # Vérifier la récompense.

        if result["reward_usd"] < MIN_REWARD:

            result["status"] = "reward_too_low"

            update_state(key, result)

            return result

        # Vérifier la sécurité.

        safe, reason = safety_check(
            title + "\n" + body
        )

        if not safe:

            result["status"] = "unsafe"
            result["message"] = reason

            update_state(key, result)

            return result

        # Lire le contrat.

        contract = extract_contract(body)

        if not contract:

            result["status"] = "no_supported_contract"

            update_state(key, result)

            return result

        valid, reason = validate_contract(contract)

        if not valid:

            result["status"] = "invalid_contract"
            result["message"] = reason

            update_state(key, result)

            return result

        if not WRITE_TOKEN:

            raise RuntimeError(
                "Token GitHub d'écriture manquant."
            )

        # Lire les informations du dépôt.

        upstream = github_request(
            "GET",
            f"/repos/{repository}",
            WRITE_TOKEN
        )

        base_branch = upstream["default_branch"]

        # Créer ou récupérer le fork.

        fork, fork_data = get_or_create_fork(
            repository
        )

        # Créer une branche indépendante.

        branch_name = (
            "optimus/"
            + str(number)
            + "-"
            + make_id(key)
        )

        create_branch(
            fork,
            fork_data["default_branch"],
            branch_name
        )

        # Lire le fichier source depuis le dépôt original.

        path = contract["path"]

        original, _ = get_file(
            repository,
            path,
            base_branch
        )

        if original is None:

            raise RuntimeError(
                "Fichier source introuvable."
            )

        old = contract["old"]
        new = contract["new"]

        if original.count(old) != 1:

            raise RuntimeError(
                "Le texte source doit apparaître "
                "exactement une fois."
            )

        modified = original.replace(
            old,
            new,
            1
        )

        # Récupérer le SHA du fichier dans le fork.

        fork_content, fork_sha = get_file(
            fork,
            path,
            fork_data["default_branch"]
        )

        if fork_content != original:

            raise RuntimeError(
                "Le fichier du fork diffère du fichier original. "
                "Modification annulée."
            )

        # Écrire le fichier modifié.

        write_file(
            fork,
            path,
            branch_name,
            modified,
            fork_sha
        )

        # Créer le Pull Request.

        pr = github_request(
            "POST",
            f"/repos/{repository}/pulls",
            WRITE_TOKEN,
            {
                "title": (
                    "[OPTIMUS AI] "
                    + title[:150]
                ),
                "head": (
                    fork.split("/")[0]
                    + ":"
                    + branch_name
                ),
                "base": base_branch,
                "body": (
                    "Modification préparée automatiquement "
                    "par OPTIMUS AI.\n\n"
                    f"Mission originale : {url}\n\n"
                    "La modification respecte le contrat "
                    "technique indiqué dans la mission.\n\n"
                    "La validation et le paiement restent "
                    "à la décision du mainteneur."
                )
            }
        )

        result["status"] = "submitted"
        result["pull_request"] = pr.get("html_url")
        result["pull_request_number"] = pr.get("number")
        result["fork"] = fork
        result["branch"] = branch_name

        update_state(key, result)

        log(
            f"PR envoyé : {key} "
            f"{result['pull_request']}"
        )

        return result

    except Exception as error:

        result["status"] = "execution_error"
        result["message"] = str(error)

        update_state(key, result)

        log(f"Erreur {key}: {error}")

        return result


# ============================================================
# TABLEAU DE BORD
# ============================================================

def build_dashboard(results):

    state = load_state()

    all_tasks = state.get(
        "tasks",
        {}
    )

    submitted = [
        task for task in all_tasks.values()
        if task.get("status") == "submitted"
    ]

    accepted = [
        task for task in all_tasks.values()
        if task.get("status") == "accepted"
    ]

    paid = [
        task for task in all_tasks.values()
        if task.get("status") == "paid"
    ]

    dashboard = {
        "engine": "OPTIMUS AI",
        "version": VERSION,
        "generated_at": now(),

        "statistics": {
            "discovered_this_run": len(results),
            "total_tracked": len(all_tasks),
            "submitted": len(submitted),
            "accepted": len(accepted),
            "paid": len(paid)
        },

        "results": results,

        "history": state.get(
            "history",
            []
        )[-100:],

        "notice": (
            "Une mission détectée n'est pas un revenu. "
            "Un Pull Request soumis n'est pas une acceptation. "
            "Un paiement est enregistré uniquement après "
            "confirmation réelle."
        )
    }

    save_json(
        DASHBOARD_FILE,
        dashboard
    )

    save_json(
        REPORT_FILE,
        dashboard
    )


# ============================================================
# MOTEUR CENTRAL
# ============================================================

def main():

    log("====================================")
    log("          OPTIMUS AI")
    log("====================================")

    log(f"Version : {VERSION}")
    log(f"Workers : {MAX_WORKERS}")
    log(f"Récompense minimale : ${MIN_REWARD}")

    issues = search_issues()

    log(f"{len(issues)} missions découvertes.")

    results = []

    if not issues:

        build_dashboard(results)

        log("Aucune mission trouvée.")

        return

    # Exécution parallèle contrôlée.

    with ThreadPoolExecutor(
        max_workers=max(1, min(MAX_WORKERS, 8))
    ) as executor:

        futures = {
            executor.submit(
                execute_task,
                issue
            ): issue
            for issue in issues
        }

        for future in as_completed(futures):

            try:

                result = future.result()

                results.append(result)

                log(
                    f"{result.get('id')} : "
                    f"{result.get('status')}"
                )

            except Exception as error:

                log(f"Erreur worker : {error}")

    build_dashboard(results)

    submitted_count = sum(
        1 for item in results
        if item.get("status") == "submitted"
    )

    log("------------------------------------")
    log(f"Missions analysées : {len(results)}")
    log(f"Pull Requests soumis : {submitted_count}")
    log("Rapports enregistrés.")
    log("OPTIMUS AI terminé.")
    log("------------------------------------")


# ============================================================
# DÉMARRAGE
# ============================================================

if __name__ == "__main__":

    import urllib.parse

    main()
