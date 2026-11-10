#!/usr/bin/env python3
"""
OPTIMUS V3 - Mission Validator
Vérifie optimus-missions.json avant son utilisation.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MISSIONS_FILE = ROOT / "optimus-missions.json"

ALLOWED_FILES = {
    "mission.json",
    "mission.md"
}

MAX_FILE_SIZE = 256_000


def validate():
    if not MISSIONS_FILE.exists():
        raise FileNotFoundError(
            "optimus-missions.json est absent."
        )

    data = json.loads(
        MISSIONS_FILE.read_text(encoding="utf-8")
    )

    missions = data.get("missions")

    if not isinstance(missions, list):
        raise ValueError(
            "Le champ missions doit être une liste."
        )

    errors = []
    identifiers = set()

    for index, mission in enumerate(missions, start=1):

        label = f"Mission #{index}"

        if not isinstance(mission, dict):
            errors.append(f"{label}: format invalide.")
            continue

        mission_id = mission.get("id")

        if not mission_id:
            errors.append(
                f"{label}: identifiant absent."
            )

        elif mission_id in identifiers:
            errors.append(
                f"{label}: identifiant en double."
            )

        identifiers.add(mission_id)

        if mission.get("status") != "PREPARATION_ONLY":
            errors.append(
                f"{label}: statut incorrect."
            )

        if mission.get("submit_github") is not False:
            errors.append(
                f"{label}: soumission automatique interdite."
            )

        generated = mission.get("generated", {})

        files = generated.get("files", [])

        if not isinstance(files, list) or not files:
            errors.append(
                f"{label}: aucun fichier généré."
            )
            continue

        for file in files:

            name = file.get("name", "")
            content = file.get("content", "")

            if name not in ALLOWED_FILES:
                errors.append(
                    f"{label}: fichier interdit ({name})."
                )
                continue

            if not isinstance(content, str):
                errors.append(
                    f"{label}: contenu invalide ({name})."
                )
                continue

            size = len(content.encode("utf-8"))

            if size > MAX_FILE_SIZE:
                errors.append(
                    f"{label}: fichier trop volumineux ({name})."
                )

    if errors:
        print("VALIDATION ÉCHOUÉE")

        for error in errors:
            print("- " + error)

        return False

    print("================================")
    print("      OPTIMUS VALIDATOR")
    print("================================")
    print(f"Missions vérifiées : {len(missions)}")
    print("Doublons : aucun")
    print("Fichiers interdits : aucun")
    print("Validation : RÉUSSIE")
    print("Aucun code de mission exécuté.")
    print("================================")

    return True


if __name__ == "__main__":
    try:
        sys.exit(0 if validate() else 1)

    except Exception as error:
        print(f"ERREUR : {error}")
        sys.exit(1)