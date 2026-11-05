import os
import json
import sqlite3
import urllib.request
import urllib.error
from config import DB_PATH


def sync_opportunities():
    """
    Synchronise les opportunités SQLite vers Supabase.
    Les doublons sont évités grâce à external_id.
    """

    supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    owner_id = os.getenv("SUPABASE_OWNER_ID", "")

    if not all([supabase_url, service_key, owner_id]):
        print("SUPABASE: configuration manquante.")
        return 0

    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row

    rows = db.execute(
        "SELECT * FROM opportunities"
    ).fetchall()

    db.close()

    if not rows:
        print("SUPABASE: aucune opportunité à synchroniser.")
        return 0

    records = []

    for row in rows:
        item = dict(row)

        records.append({
            "owner_id": owner_id,
            "source": str(item.get("source") or "unknown"),
            "external_id": str(item.get("id") or ""),
            "title": str(item.get("title") or "Sans titre"),
            "url": item.get("url"),
            "description": item.get("description"),
            "score": int(item.get("score") or 0),
            "status": "to_review"
        })

    endpoint = (
        f"{supabase_url}/rest/v1/opportunities"
        "?on_conflict=external_id"
    )

    payload = json.dumps(records).encode("utf-8")

    request = urllib.request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(
                f"SUPABASE: {len(records)} opportunités synchronisées."
            )
            return len(records)

    except urllib.error.HTTPError as error:
        print("SUPABASE HTTP ERROR:", error.code)
        print(error.read().decode("utf-8", errors="replace"))
        return 0

    except Exception as error:
        print("SUPABASE ERROR:", str(error))
        return 0
