import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ==========================================
# AUTO-EARN AI 2.0
# Multi-source opportunity scanner
# ==========================================

MAX_RESULTS = 25
TIMEOUT = 20

PAYMENT_TERMS = [
    "paid", "payment", "salary", "compensation",
    "cash reward", "bounty", "reward", "prize",
    "usd", "eur", "$", "€"
]

TASK_TERMS = [
    "python", "javascript", "developer", "programming",
    "data entry", "data annotation", "data labeling",
    "transcription", "translation", "testing",
    "bug bounty", "research", "automation",
    "writing", "design", "virtual assistant",
    "customer support", "spreadsheet", "api",
    "remote", "freelance", "task"
]

RISK_TERMS = [
    "pay to apply",
    "deposit required",
    "send your private key",
    "guaranteed profit",
    "pay registration fee"
]

OUTPUT_JSON = Path("report.json")
OUTPUT_MD = Path("report.md")


def fetch_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AUTO-EARN-AI/2.0",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(
        request, timeout=TIMEOUT
    ) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


def search_github(query):
    url = (
        "https://api.github.com/search/issues?q="
        + urllib.parse.quote(query)
        + "&sort=updated&order=desc&per_page=15"
    )

    try:
        data = fetch_json(url)
        return data.get("items", [])
    except Exception as error:
        print("GitHub search error:", error)
        return []


def search_remoteok():
    try:
        data = fetch_json("https://remoteok.com/api")

        if isinstance(data, list):
            # Le flux peut commencer par un objet
            # contenant des informations légales.
            return [
                item for item in data
                if isinstance(item, dict)
                and item.get("id")
                and item.get("position")
            ]

    except Exception as error:
        print("Remote OK error:", error)

    return []


def score_opportunity(title, description, salary=""):
    text = (
        str(title) + " "
        + str(description) + " "
        + str(salary)
    ).lower()

    score = 0
    reasons = []

    if any(term in text for term in PAYMENT_TERMS):
        score += 3
        reasons.append("Indice de rémunération")

    matched_tasks = [
        term for term in TASK_TERMS if term in text
    ]

    if matched_tasks:
        score += 2
        reasons.append(
            "Catégorie : " + ", ".join(matched_tasks[:3])
        )

    risks = [
        term for term in RISK_TERMS if term in text
    ]

    if risks:
        score -= 10
        reasons.append(
            "Signal de risque : " + ", ".join(risks)
        )

    return score, reasons


def github_opportunities():
    queries = [
        '"bounty" is:issue is:open',
        '"cash reward" is:issue is:open',
        '"paid task" is:issue is:open',
        'label:bounty is:issue is:open',
        '"help wanted" is:issue is:open'
    ]

    results = []

    for query in queries:
        print("GitHub:", query)

        for item in search_github(query):
            if item.get("pull_request"):
                continue

            title = item.get("title", "")
            description = item.get("body") or ""
            url = item.get("html_url", "")

            if not url:
                continue

            score, reasons = score_opportunity(
                title, description
            )

            if score >= 2:
                results.append({
                    "source": "GitHub",
                    "title": title,
                    "url": url,
                    "description": description[:500],
                    "score": score,
                    "reasons": reasons,
                    "payment": "À confirmer",
                    "eligibility": "À vérifier",
                    "automation": "À vérifier",
                    "status": "NON VÉRIFIÉ"
                })

    return results


def remoteok_opportunities():
    results = []

    for item in search_remoteok():
        title = item.get("position", "")
        description = item.get("description") or ""
        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")

        salary = ""

        if salary_min or salary_max:
            salary = (
                str(salary_min or "")
                + " - "
                + str(salary_max or "")
            )

        score, reasons = score_opportunity(
            title, description, salary
        )

        # Les annonces avec une rémunération déclarée
        # ou des indices de travail pertinent sont retenues.
        if score < 2:
            continue

        url = item.get("url", "")

        if url and not url.startswith("http"):
            url = "https://remoteok.com" + url

        if not url:
            continue

        location = item.get("location") or "Non précisée"
        tags = item.get("tags") or []

        results.append({
            "source": "Remote OK",
            "title": title,
            "url": url,
            "description": description[:500],
            "score": score,
            "reasons": reasons,
            "salary": salary or "Non indiquée",
            "location": location,
            "tags": tags,
            "payment": "À confirmer",
            "eligibility": "Madagascar : à vérifier",
            "automation": "Candidature manuelle à ce stade",
            "status": "NON VÉRIFIÉ"
        })

    return results


def deduplicate(results):
    unique = {}

    for item in results:
        url = item.get("url")

        if not url:
            continue

        if url not in unique or (
            item["score"] > unique[url]["score"]
        ):
            unique[url] = item

    return list(unique.values())


def main():
    print("=" * 50)
    print("       AUTO-EARN AI 2.0")
    print("       MULTI-SOURCE SCANNER")
    print("=" * 50)

    results = []

    results.extend(github_opportunities())
    results.extend(remoteok_opportunities())

    results = deduplicate(results)

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    results = results[:MAX_RESULTS]

    report = {
        "agent": "AUTO-EARN AI 2.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "total": len(results),
        "sources": ["GitHub", "Remote OK"],
        "opportunities": results
    }

    OUTPUT_JSON.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    lines = [
        "# AUTO-EARN AI 2.0",
        "",
        "Rapport de recherche automatique",
        "",
        "Date UTC : " + report["generated_at"],
        "",
        "Opportunités retenues : " + str(len(results)),
        "",
        "> Le score est un indice de tri, pas une garantie "
        "de paiement. Vérifie les conditions, l'éligibilité "
        "depuis Madagascar et les règles d'automatisation.",
        ""
    ]

    for index, item in enumerate(results, 1):
        lines.extend([
            f"## {index}. {item['title']}",
            "",
            "- Source : " + item["source"],
            "- Score : " + str(item["score"]),
            "- Paiement : " + item["payment"],
            "- Éligibilité : " + item["eligibility"],
            "- Automatisation : " + item["automation"],
            "- Statut : " + item["status"],
            "- Raisons : " + ", ".join(item["reasons"]),
            "- Lien : " + item["url"],
            "",
            item.get("description", ""),
            "",
            "---",
            ""
        ])

    lines.extend([
        "",
        "Source des offres d'emploi : "
        "[Remote OK](https://remoteok.com/)",
        ""
    ])

    OUTPUT_MD.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("\nRECHERCHE TERMINÉE")
    print("Opportunités retenues :", len(results))
    print("Rapports créés : report.json et report.md")


if __name__ == "__main__":
    main()
