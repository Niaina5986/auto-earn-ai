#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AUTO-EARN AI ULTRA
Moteur initial de création de produits numériques.

Formats produits :
- Markdown (.md)
- HTML (.html)
- Scripts Python (.py)
- Fiches commerciales (.json)

Aucune dépendance externe nécessaire.
"""

import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# CONFIGURATION
# ============================================================

VERSION = "1.0"

ROOT = Path(__file__).resolve().parent
PRODUCTS_DIR = ROOT / "products"
CATALOG_FILE = PRODUCTS_DIR / "catalog.json"

PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# OUTILS
# ============================================================

def now():
    return datetime.now(timezone.utc).isoformat()


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:70] or "produit"


def save_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def file_hash(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_catalog():
    if not CATALOG_FILE.exists():
        return []

    try:
        data = json.loads(
            CATALOG_FILE.read_text(encoding="utf-8")
        )
        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_catalog(products):
    temporary = CATALOG_FILE.with_suffix(".tmp")

    temporary.write_text(
        json.dumps(
            products,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    temporary.replace(CATALOG_FILE)


# ============================================================
# MODÈLE DE PRODUIT : EBOOK
# ============================================================

def build_ebook():
    title = "Les outils numériques gratuits pour débuter"

    sections = [
        (
            "Introduction",
            """
Les outils numériques peuvent aider à apprendre, organiser son travail
et créer des projets avec un budget limité.

Ce guide propose une méthode de départ. Les fonctionnalités, tarifs et
conditions des services peuvent évoluer : vérifiez toujours les
informations sur les sites officiels avant de les utiliser.
"""
        ),
        (
            "1. Organiser son travail",
            """
Commencez par définir un objectif concret. Divisez-le en petites tâches,
fixez une échéance et conservez une trace de vos progrès.

Un dossier bien organisé peut contenir les documents, les ressources,
les versions successives et les résultats du projet.

Évitez de conserver des mots de passe ou des informations confidentielles
dans des fichiers accessibles publiquement.
"""
        ),
        (
            "2. Créer des documents",
            """
Un document utile répond à un besoin précis. Il doit présenter un titre
clair, un objectif, des explications, des exemples et une conclusion.

Avant de le partager, vérifiez l'orthographe, les liens, la lisibilité
et les droits d'utilisation des ressources intégrées.
"""
        ),
        (
            "3. Apprendre la programmation",
            """
La programmation permet d'automatiser certaines tâches répétitives.

Pour débuter, choisissez un petit projet : classer des fichiers,
transformer un texte ou produire un rapport.

Testez votre code avec des données non sensibles avant de l'utiliser
sur des fichiers importants.
"""
        ),
        (
            "4. Préparer un produit numérique",
            """
Un produit numérique doit résoudre un problème concret.

Vous pouvez créer un guide, un modèle de document, une fiche pratique
ou un petit outil informatique.

Décrivez précisément le public visé, le problème traité, le contenu,
les limites du produit et les formats livrés.
"""
        ),
        (
            "5. Vérifier la qualité",
            """
Contrôlez le contenu, les liens, la mise en page et les éventuelles
erreurs techniques.

N'affirmez pas qu'un produit est professionnel ou exhaustif si vous
ne l'avez pas vérifié.

Si vous utilisez des outils d'intelligence artificielle, relisez les
résultats et vérifiez les faits importants.
"""
        ),
        (
            "Conclusion",
            """
Commencez par un produit simple et améliorez-le à partir des retours
réels des utilisateurs.

La création d'un fichier ne garantit ni sa publication ni sa vente.
La valeur dépend de son utilité, de sa qualité et de la demande.
"""
        ),
    ]

    content = [
        f"# {title}",
        "",
        "**Édition :** première version",
        f"**Créé le :** {now()}",
        "",
        "> Guide d'initiation. Vérifiez les informations avant toute utilisation.",
        "",
    ]

    for heading, body in sections:
        content.extend([
            f"## {heading}",
            "",
            body.strip(),
            "",
        ])

    return title, "\n".join(content)


# ============================================================
# MODÈLE DE PRODUIT : SCRIPT PYTHON
# ============================================================

def build_python_tool():
    title = "Outil simple de classement de fichiers"

    content = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Outil simple de classement de fichiers.

Utilisation :
    python organize_files.py /chemin/du/dossier

Par défaut, le programme effectue une simulation.
Pour appliquer les déplacements, ajouter --apply.

Attention :
- Faites une sauvegarde avant toute modification.
- Le programme ne traite que les fichiers du dossier indiqué.
- Il ne remplace pas un système complet de sauvegarde.
"""

import argparse
import shutil
from pathlib import Path


CATEGORIES = {
    "images": {
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"
    },
    "documents": {
        ".pdf", ".doc", ".docx", ".txt", ".md", ".odt"
    },
    "tableurs": {
        ".csv", ".xls", ".xlsx", ".ods"
    },
    "audio": {
        ".mp3", ".wav", ".ogg", ".m4a", ".flac"
    },
    "video": {
        ".mp4", ".mkv", ".mov", ".avi", ".webm"
    },
    "archives": {
        ".zip", ".tar", ".gz", ".7z", ".rar"
    },
    "code": {
        ".py", ".js", ".html", ".css", ".json",
        ".php", ".java", ".c", ".cpp"
    },
}


def category_for(path):
    extension = path.suffix.lower()

    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "autres"


def main():
    parser = argparse.ArgumentParser(
        description="Classe les fichiers par catégorie."
    )

    parser.add_argument("directory", help="Dossier à organiser")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Appliquer réellement les déplacements",
    )

    args = parser.parse_args()

    root = Path(args.directory).expanduser().resolve()

    if not root.is_dir():
        raise SystemExit("Erreur : le dossier n'existe pas.")

    for source in root.iterdir():
        if not source.is_file():
            continue

        category = category_for(source)
        destination_dir = root / category
        destination = destination_dir / source.name

        print(f"{source.name} -> {category}/")

        if not args.apply:
            continue

        if destination.exists():
            print("  Ignoré : le fichier de destination existe déjà.")
            continue

        destination_dir.mkdir(exist_ok=True)
        shutil.move(str(source), str(destination))

    if not args.apply:
        print("\\nSimulation terminée. Aucun fichier déplacé.")
        print("Ajoutez --apply pour appliquer les changements.")


if __name__ == "__main__":
    main()
'''

    return title, content


# ============================================================
# CRÉATION ET CONTRÔLE QUALITÉ
# ============================================================

def create_product(product_type, title, content, extension):
    slug = slugify(title)
    path = PRODUCTS_DIR / f"{slug}.{extension}"

    save_text(path, content)

    text = path.read_text(encoding="utf-8")

    if not text.strip():
        raise RuntimeError(f"Produit vide : {path}")

    if len(text) < 100:
        raise RuntimeError(f"Produit trop court : {path}")

    product = {
        "id": hashlib.sha256(
            f"{product_type}:{slug}".encode("utf-8")
        ).hexdigest()[:12],
        "type": product_type,
        "title": title,
        "file": str(path.relative_to(ROOT)),
        "format": extension,
        "created_at": now(),
        "size_bytes": path.stat().st_size,
        "sha256": file_hash(path),
        "quality_check": "FICHIER NON VIDE — CONTRÔLE TECHNIQUE INITIAL",
        "content_review": "À RELIRE",
        "commercial_status": "NON PUBLIÉ",
        "sales": 0,
        "verified_revenue": 0,
        "suggested_price_usd": None,
        "description": (
            "Description commerciale à finaliser après "
            "vérification du contenu."
        ),
    }

    catalog = load_catalog()

    existing = [
        item for item in catalog
        if item.get("id") != product["id"]
    ]

    existing.append(product)
    save_catalog(existing)

    print(f"[OK] Produit créé : {path}")

    return product


# ============================================================
# CATALOGUE
# ============================================================

def generate_products():
    products = []

    # 1. Ebook
    title, content = build_ebook()

    products.append(
        create_product(
            "ebook",
            title,
            content,
            "md",
        )
    )

    # 2. Outil Python
    title, content = build_python_tool()

    products.append(
        create_product(
            "script",
            title,
            content,
            "py",
        )
    )

    return products


def main():
    print("=" * 55)
    print("AUTO-EARN AI ULTRA — PRODUCT ENGINE")
    print("=" * 55)

    products = generate_products()

    print("")
    print(f"Produits créés : {len(products)}")
    print(f"Dossier : {PRODUCTS_DIR}")
    print(f"Catalogue : {CATALOG_FILE}")

    print("")
    print("RAPPEL :")
    print("- Les fichiers doivent être relus.")
    print("- Aucune publication n'est effectuée.")
    print("- Aucune vente n'est garantie.")
    print("- Le contrôle technique ne remplace pas une")
    print("  vérification du contenu et des droits commerciaux.")


if __name__ == "__main__":
    main()
