#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AUTO-EARN AI ULTRA — Version 3.0
Objectifs :
- Détecter des opportunités de travail en ligne.
- Évaluer leur qualité avec un score sur 100.
- Réduire les faux positifs.
- Identifier les récompenses annoncées sans inventer de paiement.
- Classer les opportunités par catégorie.
- Préparer la future génération de produits numériques.
- Générer report.json et report.md.
- Utiliser uniquement la bibliothèque standard de Python.
"""

import json
import os
import re
import time
import urllib.parse
import urllib.request
import urllib.error

from datetime import datetime, timezone


# ============================================================
# CONFIGURATION
# ============================================================

VERSION = "3.0"

MAX_RESULTS = 50
REQUEST_TIMEOUT = 20

REPORT_JSON = "report.json"
REPORT_MD = "report.md"

GITHUB_API = "https://api.github.com"
REMOTEOK_API = "https://remoteok.com/api"

HEADERS = {
    "User-Agent": "AUTO-EARN-AI-ULTRA/3.0",
    "Accept": "application/vnd.github+json",
}

# Facultatif : ajouter un token dans les secrets GitHub Actions.
# Ne jamais écrire directement son token dans le code.
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ============================================================
# CATÉGORIES
# ============================================================

CATEGORIES = {
    "annotation_images": [
        "image annotation", "image labeling", "image labelling",
        "data annotation", "bounding box", "image segmentation",
        "computer vision annotation", "image classification",
    ],
    "donnees": [
        "data labeling", "data entry", "data collection",
        "data cleaning", "data processing", "spreadsheet",
        "dataset", "data categorization",
    ],
    "programmation": [
        "python", "javascript", "typescript", "software developer",
        "programming", "coding task", "bug bounty", "api development",
        "web development", "automation script",
    ],
    "redaction": [
        "writing", "copywriting", "technical writing",
        "article writing", "blog post", "content writing",
        "proofreading", "editing",
    ],
    "traduction": [
        "translation", "translator", "localization",
        "proofreading translation",
    ],
    "audio": [
        "audio transcription", "transcription", "voice recording",
        "speech recording", "audio annotation", "voice over",
        "voiceover", "speech dataset",
    ],
    "video": [
        "video annotation", "video editing", "video transcription",
        "subtitle", "subtitling", "video production",
    ],
    "design": [
        "graphic design", "illustration", "logo design",
        "design assets", "visual design", "presentation design",
    ],
    "tests": [
        "software testing", "qa testing", "quality assurance",
        "bug report", "website testing", "usability testing",
    ],
    "recherche": [
        "research assistant", "web research", "market research",
        "research task", "information gathering",
    ],
    "produit_numerique": [
        "ebook", "digital product", "printable", "digital download",
        "template", "notion template", "sell digital products",
        "book publishing", "online course",
    ],
    "autre": [],
}


# ============================================================
# INDICES DE PAIEMENT
# ============================================================

PAYMENT_PHRASES = [
    "paid task",
    "paid opportunity",
    "cash reward",
    "bounty",
    "reward of",
    "prize of",
    "payment for",
    "paid project",
    "paid freelance",
    "compensation",
    "hourly rate",
    "salary",
    "stipend",
    "usd",
    "eur",
    "payment available",
    "paid position",
]

# Recherche d'un montant explicite.
# Ce motif détecte un montant possible, pas une preuve de paiement.
MONEY_PATTERN = re.compile(
    r"(?<!\w)"
    r"(?:US\$|USD|EUR|€|\$|£)"
    r"\s?\d[\d,]*(?:\.\d{1,2})?"
    r"|"
    r"\b\d[\d,]*(?:\.\d{1,2})?\s?"
    r"(?:USD|EUR|GBP|€|\$|£)\b",
    re.IGNORECASE,
)


# ============================================================
# FILTRES ANTI-FAUX-POSITIFS
# ============================================================

NEGATIVE_PHRASES = [
    "this is not a task",
    "not a task",
    "no payment",
    "not paid",
    "unpaid",
    "volunteer only",
    "no reward",
    "no bounty",
    "no compensation",
    "payment is not available",
    "not accepting applications",
    "position has been filled",
    "job has been filled",
    "closed to applications",
]

SCAM_WARNINGS = [
    "pay to apply",
    "registration fee required",
    "deposit required",
    "send your private key",
    "share your seed phrase",
    "guaranteed profit",
    "pay a fee to withdraw",
    "pay upfront to unlock work",
]

LOW_QUALITY_PHRASES = [
    "workflow log",
    "this is a log written by a workflow",
    "test issue",
    "example issue",
    "sample issue",
    "placeholder",
    "automated test",
    "dummy data",
    "hello world",
    "discussion only",
]


# ============================================================
# OUTILS
# ============================================================

def utc_now():
    return datetime.now(timezone.utc).isoformat()


def clean_text(value):
    if not value:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def contains_any(text, phrases):
    text = text.lower()
    return any(phrase.lower() in text for phrase in phrases)


def http_json(url, headers=None):
    request_headers = dict(HEADERS)

    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(
        url,
        headers=request_headers,
        method="GET",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return json.loads(raw)

    except urllib.error.HTTPError as exc:
        print(f"[HTTP] {exc.code}: {url}")
        return None

    except (
        urllib.error.URLError,
        TimeoutError,
        OSError,
        json.JSONDecodeError,
    ) as exc:
        print(f"[ERREUR] {url}: {exc}")
        return None


def parse_date(value):
    if not value:
        return None

    try:
        normalized = str(value).replace("Z", "+00:00")
        date = datetime.fromisoformat(normalized)

        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        return date.astimezone(timezone.utc)

    except (ValueError, TypeError):
        return None


def days_since(value):
    date = parse_date(value)

    if not date:
        return None

    return max(
        0,
        (datetime.now(timezone.utc) - date).days,
    )


def detect_category(text):
    text = text.lower()

    for category, keywords in CATEGORIES.items():
        if category == "autre":
            continue

        if contains_any(text, keywords):
            return category

    return "autre"


# ============================================================
# ANALYSE ET SCORE SUR 100
# ============================================================

def analyze_opportunity(item):
    title = clean_text(item.get("title", ""))
    description = clean_text(item.get("description", ""))

    combined = f"{title}\n{description}".lower()

    score = 0
    reasons = []
    warnings = []

    # 1. Une mission concrète est-elle décrite ?
    task_terms = [
        "annotate", "annotation", "label data", "label images",
        "transcribe", "translate", "write", "develop",
        "implement", "fix bug", "test website", "create script",
        "design", "edit video", "record audio", "dataset",
        "deliverable", "freelance task", "project",
    ]

    if contains_any(combined, task_terms):
        score += 20
        reasons.append("Description d'une tâche potentiellement concrète")
    else:
        warnings.append("Tâche concrète non clairement identifiée")

    # 2. Catégorie de travail identifiable.
    category = detect_category(combined)

    if category != "autre":
        score += 15
        reasons.append(f"Catégorie identifiée : {category}")

    # 3. Indices de rémunération.
    money_matches = MONEY_PATTERN.findall(combined)
    payment_language = contains_any(combined, PAYMENT_PHRASES)

    if money_matches:
        score += 20
        reasons.append("Montant monétaire mentionné")
        warnings.append(
            "Montant détecté : vérifier la devise, les conditions "
            "et la réalité du paiement"
        )

    elif payment_language:
        score += 12
        reasons.append("Mention de rémunération détectée")
        warnings.append("Montant ou modalités de paiement non confirmés")

    else:
        warnings.append("Aucune rémunération claire détectée")

    # 4. Le résultat attendu est-il suffisamment clair ?
    deliverable_terms = [
        "submit", "submission", "deliver", "deliverable",
        "requirements", "acceptance criteria", "dataset",
        "source code", "report", "transcript", "final file",
    ]

    if contains_any(combined, deliverable_terms):
        score += 10
        reasons.append("Livrable ou critères de réalisation mentionnés")

    # 5. Fraîcheur.
    age = days_since(item.get("posted_at"))

    if age is not None:
        if age <= 7:
            score += 15
            reasons.append("Publication récente")
        elif age <= 30:
            score += 10
            reasons.append("Publication datant de moins d'un mois")
        elif age <= 90:
            score += 4
            warnings.append("Publication relativement ancienne")
        else:
            warnings.append("Publication ancienne : vérifier si elle est active")
    else:
        warnings.append("Date de publication inconnue")

    # 6. Source et informations disponibles.
    if item.get("url", "").startswith("https://"):
        score += 5
        reasons.append("Lien source disponible")

    # 7. État ouvert ou actif.
    if item.get("is_open") is True:
        score += 10
        reasons.append("Opportunité signalée comme ouverte")
    elif item.get("is_open") is False:
        score -= 30
        warnings.append("Opportunité fermée ou inactive")
    else:
        warnings.append("État de disponibilité non confirmé")

    # 8. Pénalités pour les annonces explicitement négatives.
    if contains_any(combined, NEGATIVE_PHRASES):
        score -= 45
        warnings.append(
            "Le texte contient un indice de mission non rémunérée "
            "ou d'absence de paiement"
        )

    # 9. Bruit, exemples et faux positifs.
    if contains_any(combined, LOW_QUALITY_PHRASES):
        score -= 50
        warnings.append("Annonce probablement non exploitable")

    # 10. Risques potentiels.
    if contains_any(combined, SCAM_WARNINGS):
        score -= 60
        warnings.append(
            "Alerte de sécurité : ne pas payer pour accéder à une mission "
            "et ne jamais communiquer de clés privées"
        )

    score = max(0, min(100, score))

    # Le score mesure l'intérêt potentiel, pas une probabilité de paiement.
    if score >= 70:
        priority = "HAUTE"
    elif score >= 45:
        priority = "MOYENNE"
    else:
        priority = "FAIBLE"

    # Les informations inconnues restent explicitement inconnues.
    payment_status = "NON VÉRIFIÉ"

    if contains_any(combined, NEGATIVE_PHRASES):
        payment_status = "PAIEMENT NON CONFIRMÉ / INDICE NÉGATIF"
    elif money_matches:
        payment_status = "MONTANT ANNONCÉ — À VÉRIFIER"
    elif payment_language:
        payment_status = "RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER"
    else:
        payment_status = "AUCUNE PREUVE DE PAIEMENT DÉTECTÉE"

    item["score"] = score
    item["priority"] = priority
    item["category"] = category
    item["reasons"] = reasons
    item["warnings"] = warnings
    item["payment"] = payment_status
    item["eligibility"] = "À vérifier pour Madagascar"
    item["automation"] = "À vérifier selon les règles de la plateforme"
    item["status"] = "NON VÉRIFIÉ"
    item["reward_amount"] = money_matches[:3]

    return item


# ============================================================
# SOURCE 1 : GITHUB ISSUES
# ============================================================

GITHUB_QUERIES = [
    '"bounty" is:issue is:open',
    '"cash reward" is:issue is:open',
    '"paid task" is:issue is:open',
    '"reward" is:issue is:open',
    'label:bounty is:issue is:open',
    '"data annotation" is:issue is:open',
    '"transcription" "paid" is:issue is:open',
    '"good first issue" is:issue is:open',
]


def github_opportunities():
    results = []
    seen_urls = set()

    for query in GITHUB_QUERIES:
        params = urllib.parse.urlencode({
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": 20,
        })

        url = f"{GITHUB_API}/search/issues?{params}"

        data = http_json(url)

        if not data:
            time.sleep(1)
            continue

        for entry in data.get("items", []):
            issue_url = entry.get("html_url", "")

            if not issue_url or issue_url in seen_urls:
                continue

            seen_urls.add(issue_url)

            # Ignorer les pull requests pour cette version.
            if "pull_request" in entry:
                continue

            body = clean_text(entry.get("body", ""))

            labels = [
                label.get("name", "")
                for label in entry.get("labels", [])
            ]

            text = f"{entry.get('title', '')} {body} {' '.join(labels)}"

            # GitHub peut retourner des discussions non rémunérées.
            # On conserve les résultats pour analyse, sans prétendre
            # qu'une récompense existe.
            item = {
                "source": "GitHub Issues",
                "title": clean_text(entry.get("title", "")),
                "url": issue_url,
                "description": body[:5000],
                "posted_at": entry.get("created_at"),
                "updated_at": entry.get("updated_at"),
                "is_open": (
                    entry.get("state") == "open"
                    and entry.get("state_reason") != "not_planned"
                ),
                "labels": labels,
                "payment": "NON VÉRIFIÉ",
                "eligibility": "À vérifier pour Madagascar",
                "automation": "À vérifier",
                "status": "NON VÉRIFIÉ",
            }

            results.append(analyze_opportunity(item))

        # Réduire le risque de requêtes trop rapprochées.
        time.sleep(1)

    print(f"[GitHub] Opportunités analysées : {len(results)}")
    return results


# ============================================================
# SOURCE 2 : REMOTE OK
# ============================================================

def remoteok_opportunities():
    results = []

    data = http_json(REMOTEOK_API)

    if not isinstance(data, list):
        print("[Remote OK] Source indisponible.")
        return results

    for entry in data:
        if not isinstance(entry, dict):
            continue

        title = clean_text(entry.get("position", ""))
        company = clean_text(entry.get("company", ""))
        description = clean_text(entry.get("description", ""))

        tags = entry.get("tags", [])
        if not isinstance(tags, list):
            tags = []

        tags_text = " ".join(str(tag) for tag in tags)

        combined = f"{title} {company} {description} {tags_text}"

        if not title:
            continue

        # Les offres d'emploi sont gardées si leur contenu correspond
        # à une catégorie que nous surveillons.
        category = detect_category(combined)

        if category == "autre":
            continue

        url = clean_text(entry.get("url", ""))

        if not url and entry.get("slug"):
            url = "https://remoteok.com/remote-jobs/" + str(entry["slug"])

        salary_min = entry.get("salary_min")
        salary_max = entry.get("salary_max")

        salary_text = ""

        if salary_min or salary_max:
            salary_text = (
                f"Salary range listed: {salary_min or '?'}"
                f" - {salary_max or '?'}"
            )

        full_description = " ".join(
            part for part in [description, salary_text] if part
        )

        item = {
            "source": "Remote OK",
            "title": title,
            "company": company,
            "url": url,
            "description": full_description[:5000],
            "posted_at": entry.get("date"),
            "updated_at": entry.get("date"),
            "is_open": None,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "tags": tags,
            "payment": "NON VÉRIFIÉ",
            "eligibility": "À vérifier pour Madagascar",
            "automation": "À vérifier",
            "status": "NON VÉRIFIÉ",
        }

        # Une offre publiée ne prouve pas qu'elle accepte des candidats
        # de Madagascar ni que le paiement sera effectivement reçu.
        results.append(analyze_opportunity(item))

    print(f"[Remote OK] Opportunités analysées : {len(results)}")
    return results


# ============================================================
# FUTUR MODULE : PRODUITS NUMÉRIQUES
# ============================================================

def create_product_ideas():
    """
    Prépare des idées de produits numériques.

    Cette fonction ne prétend pas produire des ebooks, vidéos ou audios
    de qualité commerciale à elle seule. Elle prépare une liste d'idées
    qui sera utilisée par le futur moteur de création.
    """

    ideas = [
        {
            "type": "ebook",
            "title": "Guide pratique pour débuter en programmation",
            "format": "Markdown puis PDF/EPUB",
            "status": "IDÉE À DÉVELOPPER",
            "requires_quality_check": True,
            "requires_original_content": True,
        },
        {
            "type": "ebook",
            "title": "Guide pratique des outils numériques gratuits",
            "format": "Markdown puis PDF/EPUB",
            "status": "IDÉE À DÉVELOPPER",
            "requires_quality_check": True,
            "requires_original_content": True,
        },
        {
            "type": "template",
            "title": "Modèle de suivi de budget personnel",
            "format": "CSV ou XLSX",
            "status": "IDÉE À DÉVELOPPER",
            "requires_quality_check": True,
            "requires_original_content": True,
        },
        {
            "type": "script",
            "title": "Script Python de classement automatique de fichiers",
            "format": "Python avec documentation",
            "status": "IDÉE À DÉVELOPPER",
            "requires_quality_check": True,
            "requires_original_content": True,
        },
        {
            "type": "video",
            "title": "Mini-cours sur un outil numérique gratuit",
            "format": "Script, storyboard et vidéo",
            "status": "IDÉE À DÉVELOPPER",
            "requires_quality_check": True,
            "requires_original_content": True,
        },
        {
            "type": "audio",
            "title": "Guide audio d'initiation à la technologie",
            "format": "Script puis audio",
            "status": "IDÉE À DÉVELOPPER",
            "requires_quality_check": True,
            "requires_original_content": True,
        },
    ]

    return ideas


# ============================================================
# RAPPORTS
# ============================================================

def save_json(data, path):
    temporary_path = path + ".tmp"

    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    os.replace(temporary_path, path)


def save_markdown(report, path):
    lines = [
        "# AUTO-EARN AI ULTRA",
        "",
        f"- Version : {report['version']}",
        f"- Généré le : {report['generated_at']}",
        f"- Opportunités analysées : {report['total_opportunities']}",
        f"- Opportunités prioritaires : {report['high_priority']}",
        "",
        "> Le score est un indicateur de tri, pas une garantie de revenu.",
        "> Les paiements et l'éligibilité doivent être vérifiés.",
        "",
        "## Opportunités",
        "",
    ]

    for item in report["opportunities"]:
        lines.extend([
            f"### [{item['title']}]({item['url']})",
            "",
            f"- Source : {item['source']}",
            f"- Score : {item['score']}/100",
            f"- Priorité : {item['priority']}",
            f"- Catégorie : {item['category']}",
            f"- Paiement : {item['payment']}",
            f"- Éligibilité : {item['eligibility']}",
            f"- Automatisation : {item['automation']}",
            f"- Statut : {item['status']}",
            "",
        ])

        if item.get("reasons"):
            lines.append("**Points positifs :**")
            for reason in item["reasons"]:
                lines.append(f"- {reason}")
            lines.append("")

        if item.get("warnings"):
            lines.append("**Vérifications nécessaires :**")
            for warning in item["warnings"]:
                lines.append(f"- {warning}")
            lines.append("")

        if item.get("description"):
            lines.extend([
                "**Description :**",
                "",
                item["description"][:1000],
                "",
            ])

    lines.extend([
        "## Produits numériques à développer",
        "",
    ])

    for product in report["product_ideas"]:
        lines.append(
            f"- **{product['type']} :** {product['title']} "
            f"— {product['status']}"
        )

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():
    started_at = utc_now()

    print("=" * 60)
    print("AUTO-EARN AI ULTRA", VERSION)
    print("=" * 60)

    all_opportunities = []

    # Recherche des missions.
    all_opportunities.extend(github_opportunities())
    all_opportunities.extend(remoteok_opportunities())

    # Éliminer les doublons.
    unique = {}

    for item in all_opportunities:
        url = item.get("url", "").strip()

        if not url:
            continue

        if url not in unique:
            unique[url] = item
        elif item.get("score", 0) > unique[url].get("score", 0):
            unique[url] = item

    opportunities = list(unique.values())

    # Exclure les annonces dont le score est très faible.
    opportunities = [
        item for item in opportunities
        if item.get("score", 0) >= 15
    ]

    opportunities.sort(
        key=lambda item: (
            item.get("score", 0),
            item.get("posted_at") or "",
        ),
        reverse=True,
    )

    opportunities = opportunities[:MAX_RESULTS]

    high_priority = sum(
        1 for item in opportunities
        if item.get("priority") == "HAUTE"
    )

    report = {
        "version": VERSION,
        "generated_at": started_at,
        "total_opportunities": len(opportunities),
        "high_priority": high_priority,
        "opportunities": opportunities,
        "product_ideas": create_product_ideas(),
        "execution": {
            "search_completed": True,
            "digital_product_creation": "NOT IMPLEMENTED YET",
            "automatic_publication": "NOT IMPLEMENTED YET",
            "verified_revenue": 0,
            "note": (
                "0 signifie qu'aucun revenu n'a été enregistré "
                "par ce programme. Cela ne prouve pas qu'aucune "
                "vente externe n'a eu lieu."
            ),
        },
    }

    save_json(report, REPORT_JSON)
    save_markdown(report, REPORT_MD)

    print("")
    print("=" * 60)
    print("RAPPORT TERMINÉ")
    print(f"Opportunités retenues : {len(opportunities)}")
    print(f"Priorité haute : {high_priority}")
    print(f"Fichier JSON : {REPORT_JSON}")
    print(f"Fichier Markdown : {REPORT_MD}")
    print("=" * 60)


if __name__ == "__main__":
    main()
