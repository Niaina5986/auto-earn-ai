#!/usr/bin/env python3
"""
Collecteur historique Boom 1000 (Deriv) — lecture seule.
- Découvre le symbole API via active_symbols (ne suppose pas son code).
- Demande jusqu'à 100 000 ticks.
- Enregistre les ticks reçus en CSV.
Aucun ordre de trading n'est envoyé.

Installation:
    python -m pip install websocket-client

Exécution:
    python collect_boom1000.py

Si Deriv limite la taille de la réponse, le script indique le nombre réellement reçu.
"""

import csv
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import websocket

APP_ID = "1089"  # App ID public de démonstration; remplaçable par votre propre App ID Deriv
WS_URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"
TARGET_COUNT = 100_000
OUTPUT = Path("boom1000_ticks.csv")
TIMEOUT_SECONDS = 30


def request(ws, payload, expected_msg_type=None):
    ws.send(json.dumps(payload))
    deadline = time.time() + TIMEOUT_SECONDS

    while time.time() < deadline:
        raw = ws.recv()
        message = json.loads(raw)

        if "error" in message:
            err = message["error"]
            raise RuntimeError(f"Erreur API Deriv: {err.get('code')} — {err.get('message')}")

        if expected_msg_type is None or message.get("msg_type") == expected_msg_type:
            return message

    raise TimeoutError("Délai dépassé en attendant la réponse de Deriv.")


def find_boom1000_symbol(ws):
    response = request(
        ws,
        {"active_symbols": "brief", "product_type": "basic"},
        "active_symbols",
    )
    symbols = response.get("active_symbols", [])

    # Cherche d'abord un nom d'affichage explicite; évite de confondre Boom 500/1000.
    matches = [
        item for item in symbols
        if "boom 1000" in item.get("display_name", "").lower()
    ]

    if not matches:
        # Certains flux renvoient un nom différent; affiche des candidats à vérifier.
        candidates = [
            (item.get("symbol"), item.get("display_name"))
            for item in symbols
            if "boom" in item.get("display_name", "").lower()
        ]
        raise RuntimeError(
            "Symbole Boom 1000 introuvable dans active_symbols. "
            f"Candidats Boom reçus: {candidates[:20]}"
        )

    # Si plusieurs variantes existent, prendre la première et l'afficher pour contrôle.
    chosen = matches[0]
    return chosen["symbol"], chosen.get("display_name", "")


def main():
    print("Connexion à l'API publique Deriv (lecture seule)...")
    ws = websocket.create_connection(WS_URL, timeout=TIMEOUT_SECONDS)

    try:
        symbol, display_name = find_boom1000_symbol(ws)
        print(f"Marché détecté : {display_name} | code API : {symbol}")
        print(f"Demande de {TARGET_COUNT:,} ticks...")

        response = request(
            ws,
            {
                "ticks_history": symbol,
                "end": "latest",
                "count": TARGET_COUNT,
                "style": "ticks",
            },
            "history",
        )

        history = response.get("history", {})
        prices = history.get("prices", [])
        times = history.get("times", [])

        if not prices or not times:
            raise RuntimeError("Deriv n'a renvoyé aucun historique de ticks.")

        rows = []
        for epoch, price in zip(times, prices):
            epoch = int(epoch)
            rows.append((
                epoch,
                datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat(),
                price,
            ))

        # L'API renvoie normalement les données dans l'ordre chronologique.
        # On conserve les répétitions: plusieurs ticks peuvent partager la même seconde.
        with OUTPUT.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["epoch", "datetime_utc", "quote"])
            writer.writerows(rows)

        print(f"\nTerminé : {len(rows):,} ticks enregistrés.")
        print(f"Fichier : {OUTPUT.resolve()}")
        if len(rows) < TARGET_COUNT:
            print(
                "Note : l'API a renvoyé moins de 100 000 ticks que demandé. "
                "Le CSV contient uniquement les données réellement reçues; "
                "cela peut venir d'une limite de réponse ou de l'historique disponible."
            )
        print("Aucun trade, achat ou vente n'a été exécuté.")

    finally:
        ws.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nÉCHEC : {exc}", file=sys.stderr)
        sys.exit(1)
