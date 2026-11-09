#!/usr/bin/env python3
"""AUTO-EARN ENGINE — moteur unique, sans API OpenAI."""

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

API = "https://api.github.com"

TOKEN = os.getenv("AUTONOMOUS_GITHUB_TOKEN", "")
FORK = os.getenv("AUTONOMOUS_FORK", "")

MIN_REWARD = float(os.getenv("MIN_REWARD_USD", "10"))
MAX_ISSUES = int(os.getenv("MAX_ISSUES", "30"))

REPORT = Path("engine-reports")
REPORT.mkdir(exist_ok=True)

CONTRACT = re.compile(
    r"<!--\s*AUTO-EARN-AUTOFIX\s*(\{.*?\})\s*-->",
    re.S
)

REWARD = re.compile(
    r"(?:\$|USD\s*)(\d+(?:[.,]\d{1,2})?)",
    re.I
)

BLOCKED = (
    "seed phrase",
    "private key",
    "password",
    "captcha bypass",
    "malware",
    "send crypto",
    "deposit to unlock"
)


def api(url, token=""):
    headers = {
        "User-Agent": "AutoEarnEngine/1.0",
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = "Bearer " + token

    request = urllib.request.Request(
        url,
        headers=headers
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def reward(text):
    values = [
        float(value.replace(",", "."))
        for value in REWARD.findall(text or "")
    ]

    return max(values or [0])


def screen(issue):
    body = issue.get("body") or ""

    blob = (
        issue.get("title", "") + " " + body
    ).lower()

    if issue.get("state") != "open":
        return None, "not an open issue"

    if issue.get("pull_request"):
        return None, "not an issue"

    if any(word in blob for word in BLOCKED):
        return None, "unsafe task"

    if reward(blob) < MIN_REWARD:
        return None, "no explicit USD reward"

    match = CONTRACT.search(body)

    if not match:
        return None, "no supported execution contract"

    try:
        spec = json.loads(match.group(1))
    except Exception:
        return None, "invalid contract JSON"

    path = Path(str(spec.get("path", "")))

    if spec.get("type") != "replace_text":
        return None, "unsupported adapter"

    if path.is_absolute() or ".." in path.parts or not path.parts:
        return None, "unsafe path"

    if path.suffix.lower() not in (
        ".md", ".txt", ".rst"
    ):
        return None, "only documentation files supported"

    if not isinstance(spec.get("old"), str) or not spec["old"]:
        return None, "invalid old text"

    if not isinstance(spec.get("new"), str):
        return None, "invalid replacement text"

    if len(spec["old"]) > 5000 or len(spec["new"]) > 5000:
        return None, "patch too large"

    return spec, "eligible"


def git(cwd, *args):
    process = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=60
    )

    if process.returncode:
        raise RuntimeError(
            (process.stderr or process.stdout)[-2000:]
        )

    return process.stdout.strip()


def execute(issue, spec, repo, default_branch):

    if not TOKEN or not FORK:
        raise RuntimeError(
            "Missing AUTONOMOUS_GITHUB_TOKEN or AUTONOMOUS_FORK"
        )

    with tempfile.TemporaryDirectory(
        prefix="autoearn-"
    ) as temporary:

        directory = Path(temporary)
        archive = directory / "source.zip"

        url = (
            f"{API}/repos/{repo}/zipball/"
            f"{urllib.parse.quote(default_branch)}"
        )

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "AutoEarnEngine/1.0"}
        )

        with urllib.request.urlopen(
            request, timeout=60
        ) as response:
            archive.write_bytes(response.read())

        extracted = directory / "extract"
        extracted.mkdir()

        with zipfile.ZipFile(archive) as zip_file:

            for name in zip_file.namelist():

                target = (extracted / name).resolve()

                if extracted.resolve() not in target.parents:
                    raise RuntimeError("Unsafe archive path")

            zip_file.extractall(extracted)

        roots = [
            item for item in extracted.iterdir()
            if item.is_dir()
        ]

        if len(roots) != 1:
            raise RuntimeError("Unexpected archive")

        work = directory / "repo"

        shutil.copytree(roots[0], work)

        target = (work / spec["path"]).resolve()

        if work.resolve() not in target.parents:
            raise RuntimeError("Invalid target path")

        if not target.is_file():
            raise RuntimeError("Target file does not exist")

        original = target.read_text(encoding="utf-8")

        if original.count(spec["old"]) != 1:
            raise RuntimeError(
                "Old text must match exactly once"
            )

        updated = original.replace(
            spec["old"],
            spec["new"],
            1
        )

        target.write_text(
            updated,
            encoding="utf-8"
        )

        if spec["new"] not in target.read_text(
            encoding="utf-8"
        ):
            raise RuntimeError("Verification failed")

        branch = (
            f"auto-earn/issue-{issue['number']}-"
            f"{int(time.time())}"
        )

        git(work, "init")

        git(
            work,
            "config",
            "user.name",
            "auto-earn-engine[bot]"
        )

        git(
            work,
            "config",
            "user.email",
            "auto-earn-engine[bot]@users.noreply.github.com"
        )

        git(work, "add", ".")
        git(
            work,
            "commit",
            "-m",
            f"Documentation fix for issue #{issue['number']}"
        )

        git(work, "branch", "-M", branch)

        remote = (
            "https://x-access-token:"
            + urllib.parse.quote(TOKEN)
            + f"@github.com/{FORK}.git"
        )

        git(work, "remote", "add", "fork", remote)
        git(work, "push", "-u", "fork", branch)

        payload = {
            "title": (
                f"Automated documentation fix "
                f"for issue #{issue['number']}"
            ),
            "head": FORK.split("/")[0] + ":" + branch,
            "base": default_branch,
            "body": (
                f"Deterministic documentation patch for "
                f"{issue['html_url']}\n\n"
                "The patch was checked before submission. "
                "This PR does not guarantee bounty eligibility, "
                "acceptance, or payment."
            )
        }

        request = urllib.request.Request(
            f"{API}/repos/{repo}/pulls",
            data=json.dumps(payload).encode(),
            headers={
                "User-Agent": "AutoEarnEngine/1.0",
                "Authorization": "Bearer " + TOKEN,
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(
            request, timeout=30
        ) as response:

            result = json.loads(
                response.read().decode()
            )

            return result["html_url"]


def main():

    found = {}

    searches = [
        'is:issue is:open bounty "$"',
        'is:issue is:open reward "$"',
        'is:issue is:open paid "$"'
    ]

    for query in searches:

        try:

            url = (
                f"{API}/search/issues?q="
                f"{urllib.parse.quote(query)}"
                "&sort=updated&order=desc&per_page=30"
            )

            results = api(
                url,
                os.getenv("GITHUB_TOKEN", "")
            )

            for issue in results.get("items", []):
                found[issue["html_url"]] = issue

        except Exception as error:
            print("SEARCH WARNING:", error)

    rows = []
    submitted = 0

    for issue in list(found.values())[:MAX_ISSUES]:

        spec, reason = screen(issue)

        row = {
            "issue": issue.get("html_url"),
            "title": issue.get("title"),
            "reward_usd": reward(
                (issue.get("title") or "")
                + " "
                + (issue.get("body") or "")
            ),
            "status": reason
        }

        if spec:

            try:

                repo = issue["repository_url"].replace(
                    API + "/repos/", ""
                )

                info = api(
                    issue["repository_url"],
                    os.getenv("GITHUB_TOKEN", "")
                )

                pr = execute(
                    issue,
                    spec,
                    repo,
                    info.get("default_branch") or "main"
                )

                row["status"] = "PR submitted"
                row["pr_url"] = pr

                submitted += 1

            except Exception as error:

                row["status"] = (
                    "not submitted: " + str(error)
                )

        rows.append(row)

    result = {
        "engine": "AUTO-EARN ENGINE",
        "version": "1.0",
        "discovered": len(found),
        "reviewed": len(rows),
        "pull_requests_submitted": submitted,
        "results": rows,
        "notice": (
            "A PR is not proof of acceptance or payment."
        )
    }

    (REPORT / "run.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8"
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()