import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CONFIG = {
    "queries": [
        '"bounty" is:issue is:open',
        '"cash reward" is:issue is:open',
        '"paid task" is:issue is:open',
        'label:bounty is:issue is:open',
        '"good first issue" is:issue is:open'
    ],
    "max_results": 15
}


def search_github(query):
    url = (
        "https://api.github.com/search/issues?q="
        + urllib.parse.quote(query)
        + "&sort=updated&order=desc&per_page="
        + str(CONFIG["max_results"])
    )

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "AUTO-EARN-AI"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(
                response.read().decode("utf-8")
            ).get("items", [])
    except Exception as error:
        print("Erreur de recherche :", error)
        return []


def evaluate_task(task):
    title = task.get("title", "")
    body = task.get("body") or ""
    text = (title + " " + body).lower()

    score = 0
    reasons = []

    payment_words = [
        "cash reward",
        "paid task",
        "bounty",
        "reward",
        "prize",
        "usd",
        "€",
        "$"
    ]

    task_words = [
        "bug bounty",
        "help wanted",
        "good first issue",
        "contribution"
    ]

    risk_words = [
        "deposit required",
        "pay to participate",
        "guaranteed profit",
        "send your private key"
    ]

    for word in payment_words:
        if word in text:
            score += 3
            reasons.append("Mention possible de paiement")
            break

    for word in task_words:
        if word in text:
            score += 2
            reasons.append("Mission potentiellement réalisable")
            break

    if any(word in text for word in risk_words):
        score -= 10
        reasons.append("Signal de risque")

    return score, reasons


def main():
    print("=" * 50)
    print("       AUTO-EARN AI : TASK HUNTER")
    print("=" * 50)

    opportunities = {}

    for query in CONFIG["queries"]:
        print("\nRecherche :", query)

        for task in search_github(query):
            if task.get("pull_request"):
                continue

            link = task.get("html_url")

            if not link or link in opportunities:
                continue

            score, reasons = evaluate_task(task)

            if score >= 2:
                opportunities[link] = {
                    "title": task.get("title", ""),
                    "url": link,
                    "repository": task.get(
                        "repository_url", ""
                    ).replace(
                        "https://api.github.com/repos/", ""
                    ),
                    "score": score,
                    "reasons": reasons,
                    "updated": task.get("updated_at"),
                    "status": "À vérifier : paiement et conditions"
                }

    results = sorted(
        opportunities.values(),
        key=lambda item: item["score"],
        reverse=True
    )

    report = {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "total": len(results),
        "opportunities": results
    }

    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2
        )

    with open("report.md", "w", encoding="utf-8") as file:
        file.write("# AUTO-EARN AI — Rapport\n\n")
        file.write(
            "Généré le : "
            + report["generated_at"]
            + "\n\n"
        )
        file.write(
            f"Opportunités détectées : {len(results)}\n\n"
        )

        for number, item in enumerate(results, 1):
            file.write(
                f"## {number}. {item['title']}\n\n"
            )
            file.write(f"- Score : {item['score']}\n")
            file.write(f"- Dépôt : {item['repository']}\n")
            file.write(f"- Lien : {item['url']}\n")
            file.write(
                f"- Indices : {', '.join(item['reasons'])}\n"
            )
            file.write(
                "- Statut : paiement non confirmé\n\n"
            )

    print("\nRecherche terminée !")
    print("Opportunités trouvées :", len(results))
    print("Rapports créés : report.json et report.md")


if __name__ == "__main__":
    main()
