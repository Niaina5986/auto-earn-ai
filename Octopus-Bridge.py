import os
import json
import pathlib
import requests
import sys

ROOT = pathlib.Path("octopus-data")

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SERVICE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
OWNER_ID = os.environ["SUPABASE_OWNER_ID"]
RUN_ID = int(os.environ["OCTOPUS_RUN_ID"])

headers = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def kind_for(path):
    p = path.as_posix()
    if "/solutions/" in "/" + p:
        return "solution_file"
    if p.endswith("history.json"):
        return "history"
    if p.endswith("latest.json"):
        return "run_summary"
    if p.endswith("_error.json"):
        return "failure"
    return "mission_report"

def upload(path, payload):
    key = path.relative_to(ROOT).as_posix()

    row = {
        "owner_id": OWNER_ID,
        "run_id": RUN_ID,
        "report_key": key,
        "report_type": kind_for(path),
        "payload": payload
    }

    url = (
        f"{SUPABASE_URL}/rest/v1/"
        "octopus_reports?on_conflict=run_id,report_key"
    )

    response = requests.post(
        url,
        headers=headers,
        json=row,
        timeout=45
    )

    response.raise_for_status()
    print(f"OK {key}")

def main():
    if not ROOT.exists():
        raise SystemExit(
            f"Artifact directory missing: {ROOT}"
        )

    files = sorted(ROOT.rglob("*.json"))

    if not files:
        raise SystemExit(
            "No JSON reports found in artifact."
        )

    uploaded = 0

    for path in files:
        try:
            data = json.loads(
                path.read_text(encoding="utf-8")
            )
            upload(path, data)
            uploaded += 1

        except Exception as exc:
            print(
                f"ERROR {path}: {exc}",
                file=sys.stderr
            )
            raise

    print(
        f"Uploaded {uploaded} JSON files "
        f"for run {RUN_ID}."
    )

if __name__ == "__main__":
    main()
