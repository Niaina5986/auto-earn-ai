#!/usr/bin/env python3
"""
OPTIMUS V3 - Mission Generator
Génère une mission pour chaque opportunité enregistrée dans SQLite.
Préparation uniquement : aucune candidature ou soumission automatique.
"""

import hashlib
import json
import sqlite3
import sys

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "optimus-missions.json"
HISTORY = ROOT / "optimus-mission-history.json"


def get_database_path():
    from config import DB_PATH
    return Path(DB_PATH)


def load_opportunities():
    db_path = get_database_path()

    if not db_path.exists():
        raise FileNotFoundError(
            f"Base de données absente : {db_path}. Lance agent.py d'abord."
        )

    with sqlite3.connect(str(db_path)) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            "SELECT * FROM opportunities "
            "ORDER BY discovered_at DESC, id ASC"
        ).fetchall()

    opportunities = []

    for row in rows:
        item = dict(row)

        raw = item.pop("raw_json", None)

        try:
            item["raw"] = json.loads(raw) if raw else {}
        except (TypeError, json.JSONDecodeError):
            item["raw"] = {}

        opportunities.append(item)

    return opportunities


def generate_id(item):
    identity = "|".join(
        str(item.get(key) or "")
        for key in ("source", "id", "url", "title")
    )

    digest = hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()[:18]

    return "opp-" + digest


def create_mission(item):
    mission_id = generate_id(item)

    title = str(
        item.get("title") or "Opportunité sans titre"
    ).strip()

    description = str(
        item.get("description") or ""
    )[:12000]

    source = str(item.get("source") or "unknown")
    url = str(item.get("url") or "")

    dossier = {
        "mission_id": mission_id,
        "title": title,
        "source": source,
        "url": url,
        "description": description,
        "category": item.get("category"),
        "reward_text": item.get("reward_text"),
        "score": item.get("score"),
        "risk": item.get("risk"),
        "original_status": item.get("status"),
        "discovered_at": item.get("discovered_at"),

        "checks": [
            "Vérifier que l'offre est toujours ouverte.",
            "Vérifier l'éligibilité depuis Madagascar.",
            "Vérifier le moyen et le seuil de paiement.",
            "Vérifier les compétences demandées.",
            "Vérifier les délais et les conditions.",
            "Obtenir l'accord humain avant toute candidature."
        ],

        "next_step": (
            "Vérification de l'offre et de ses conditions."
        ),

        "automation_limit": (
            "Préparation uniquement. Aucune candidature, "
            "dépense ou soumission externe automatique."
        )
    }

    mission_json = json.dumps(
        dossier,
        ensure_ascii=False,
        indent=2
    )

    mission_md = f"""# Dossier OPTIMUS V3

## Informations

- Mission : {title}
- Source : {source}
- URL : {url}
- Récompense annoncée : {item.get('reward_text')}
- Score : {item.get('score')}
- Risque : {item.get('risk')}

## Description

{description}

## Vérifications

- [ ] Offre toujours disponible
- [ ] Madagascar accepté
- [ ] Paiement vérifié
- [ ] Conditions vérifiées
- [ ] Compétences nécessaires vérifiées
- [ ] Autorisation humaine obtenue

## Statut

PRÉPARATION UNIQUEMENT.

Cette mission n'est pas considérée comme terminée ou payée.
"""

    return {
        "id": mission_id,
        "title": title,
        "source": source,
        "url": url,
        "score": item.get("score"),
        "risk": item.get("risk"),
        "status": "PREPARATION_ONLY",
        "submit_github": False,

        "generated": {
            "files": [
                {
                    "name": "mission.json",
                    "content": mission_json
                },
                {
                    "name": "mission.md",
                    "content": mission_md
                }
            ]
        }
    }


def load_history():
    if not HISTORY.exists():
        return {"version": 1, "missions": {}}

    try:
        data = json.loads(
            HISTORY.read_text(encoding="utf-8")
        )

        if isinstance(data.get("missions"), dict):
            return data

    except Exception:
        pass

    return {"version": 1, "missions": {}}


def main():
    opportunities = load_opportunities()
    history = load_history()

    previous = history["missions"]

    missions = []
    seen = set()

    now = datetime.now(timezone.utc).isoformat()

    for item in opportunities:
        mission = create_mission(item)

        if mission["id"] in seen:
            continue

        seen.add(mission["id"])
        missions.append(mission)

        previous.setdefault(
            mission["id"],
            {
                "title": mission["title"],
                "first_seen_at": now,
                "status": "PREPARATION_ONLY"
            }
        )

        previous[mission["id"]]["last_seen_at"] = now

    payload = {
        "system": "OPTIMUS AI",
        "version": "3.0",
        "generated_at": now,
        "mode": "PREPARATION_ONLY",
        "total_opportunities_read": len(opportunities),
        "total_unique_missions": len(missions),
        "missions": missions
    }

    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    history["updated_at"] = now
    history["total_known_missions"] = len(previous)

    HISTORY.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("===================================")
    print("       OPTIMUS MISSION GENERATOR")
    print("===================================")
    print(f"Opportunités lues : {len(opportunities)}")
    print(f"Missions créées : {len(missions)}")
    print("Fichier : optimus-missions.json")
    print("Historique : optimus-mission-history.json")
    print("Statut : PREPARATION_ONLY")
    print("===================================")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERREUR : {error}", file=sys.stderr)
        sys.exit(1)