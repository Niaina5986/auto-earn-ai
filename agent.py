"""
AUTO-EARN AI ULTRA 3.0
Automated opportunity research and digital product preparation.

Outputs:
- report.json
- report.md

Optional integration:
- product_engine.py
- GitHub Actions
"""

import json
import os
import re
import time
import logging

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ============================================================
# CONFIGURATION
# ============================================================

AGENT_NAME = "AUTO-EARN AI ULTRA"
AGENT_VERSION = "3.0.0"

BASE_DIR = Path(__file__).resolve().parent

JSON_REPORT = BASE_DIR / "report.json"
MARKDOWN_REPORT = BASE_DIR / "report.md"

REQUEST_TIMEOUT = 20
MAX_OPPORTUNITIES = 40

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()

USER_AGENT = "AutoEarnAIUltra/3.0"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(AGENT_NAME)


# ============================================================
# HTTP UTILITIES
# ============================================================

def fetch_json(url, headers=None):
    """Download and decode a JSON response."""

    request_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    if headers:
        request_headers.update(headers)

    request = Request(
        url,
        headers=request_headers,
        method="GET"
    )

    try:
        with urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            raw_data = response.read().decode("utf-8")
            return json.loads(raw_data)

    except HTTPError as exc:
        logger.warning(
            "HTTP error %s while accessing %s",
            exc.code,
            url
        )

    except (URLError, TimeoutError, OSError) as exc:
        logger.warning(
            "Network error while accessing %s: %s",
            url,
            exc
        )

    except json.JSONDecodeError:
        logger.warning("Invalid JSON received from %s", url)

    return None


# ============================================================
# OPPORTUNITY SCORING
# ============================================================

POSITIVE_KEYWORDS = {
    "paid": 15,
    "payment": 12,
    "reward": 10,
    "bounty": 18,
    "cash": 12,
    "freelance": 8,
    "contract": 8,
    "remote": 5,
    "beginner": 5,
    "entry level": 5,
    "open source": 4,
    "documentation": 5,
    "automation": 5,
    "python": 4,
    "api": 4,
    "writing": 4,
    "research": 4,
    "microtask": 8,
}

NEGATIVE_KEYWORDS = {
    "unpaid": 25,
    "volunteer only": 30,
    "investment required": 35,
    "pay to apply": 40,
    "deposit required": 40,
    "pyramid scheme": 50,
    "get rich quick": 30,
    "guaranteed income": 25,
    "crypto doubling": 50,
    "send your password": 50,
}


def score_opportunity(title, description="", url=""):
    """
    Score an opportunity from 0 to 100.

    This is a relevance estimate, not a guarantee of payment
    or legitimacy.
    """

    text = (
        f"{title} {description} {url}"
    ).lower()

    score = 35
    matched_positive = []
    matched_negative = []

    for keyword, points in POSITIVE_KEYWORDS.items():
        if keyword in text:
            score += points
            matched_positive.append(keyword)

    for keyword, penalty in NEGATIVE_KEYWORDS.items():
        if keyword in text:
            score -= penalty
            matched_negative.append(keyword)

    # A direct link is useful, but does not prove legitimacy.
    if url.startswith("https://"):
        score += 5

    if matched_negative:
        score -= 10

    score = max(0, min(100, score))

    return {
        "score": score,
        "positive_signals": matched_positive,
        "risk_signals": matched_negative,
    }


# ============================================================
# SOURCE 1: GITHUB ISSUES
# ============================================================

GITHUB_SEARCH_QUERIES = [
    'is:issue is:open bounty',
    'is:issue is:open "good first issue" paid',
    'is:issue is:open "paid" python',
    'is:issue is:open reward automation',
]


def search_github():
    """Search public GitHub issues for potentially useful tasks."""

    results = []

    headers = {
        "Accept": "application/vnd.github+json",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    for query in GITHUB_SEARCH_QUERIES:

        encoded_query = quote(query)

        url = (
            "https://api.github.com/search/issues"
            f"?q={encoded_query}&sort=created&order=desc&per_page=10"
        )

        data = fetch_json(url, headers=headers)

        if not isinstance(data, dict):
            continue

        items = data.get("items", [])

        for item in items:

            title = item.get("title", "").strip()
            description = (
                item.get("body") or ""
            ).strip()

            html_url = item.get("html_url", "")

            if not title or not html_url:
                continue

            if "pull_request" in item:
                continue

            scoring = score_opportunity(
                title,
                description,
                html_url
            )

            results.append({
                "source": "GitHub Issues",
                "title": title,
                "description": description[:1500],
                "url": html_url,
                "score": scoring["score"],
                "positive_signals": scoring["positive_signals"],
                "risk_signals": scoring["risk_signals"],
                "created_at": item.get("created_at"),
                "verified_payment": False,
                "status": "Needs manual verification",
            })

        # Avoid sending requests too quickly.
        time.sleep(1)

    return results


# ============================================================
# SOURCE 2: REMOTE OK
# ============================================================

def search_remoteok():
    """Search the public Remote OK job feed."""

    url = "https://remoteok.com/api"

    data = fetch_json(url)

    if not isinstance(data, list):
        return []

    results = []

    # The first element may contain legal/API information.
    for item in data:

        if not isinstance(item, dict):
            continue

        title = item.get("position", "").strip()

        company = item.get("company", "").strip()

        description = (
            item.get("description") or ""
        ).strip()

        slug = item.get("slug", "")

        job_url = item.get("url", "")

        if not job_url and slug:
            job_url = f"https://remoteok.com/remote-jobs/{slug}"

        if not job_url:
            continue

        if not title:
            continue

        full_title = title

        if company:
            full_title = f"{title} — {company}"

        scoring = score_opportunity(
            full_title,
            description,
            job_url
        )

        results.append({
            "source": "Remote OK",
            "title": full_title,
            "description": description[:1500],
            "url": job_url,
            "score": scoring["score"],
            "positive_signals": scoring["positive_signals"],
            "risk_signals": scoring["risk_signals"],
            "created_at": item.get("date"),
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "verified_payment": False,
            "status": "Needs manual verification",
        })

    return results


# ============================================================
# OPPORTUNITY FILTERING
# ============================================================

def filter_opportunities(opportunities):
    """
    Remove duplicates and sort opportunities by score.

    Scores indicate relevance, not confirmed earnings.
    """

    unique = {}
    blocked_count = 0

    for item in opportunities:

        url = item.get("url", "").strip()

        if not url:
            continue

        if not url.startswith("https://"):
            continue

        risk_signals = item.get("risk_signals", [])

        if risk_signals:
            blocked_count += 1
            continue

        key = url.lower()

        if key not in unique:
            unique[key] = item

    filtered = list(unique.values())

    filtered.sort(
        key=lambda item: item.get("score", 0),
        reverse=True
    )

    logger.info(
        "Opportunities after filtering: %s; removed for risk signals: %s",
        len(filtered),
        blocked_count
    )

    return filtered[:MAX_OPPORTUNITIES]


# ============================================================
# DIGITAL PRODUCT IDEAS
# ============================================================

def create_product_ideas():
    """
    Prepare ideas for digital products.

    These are ideas, not confirmed sales.
    """

    return [
        {
            "name": "Python File Organizer",
            "type": "Python script",
            "description": (
                "A tool that organizes files into folders "
                "based on file extensions."
            ),
            "target_audience": (
                "Students, office workers and computer users"
            ),
            "status": "Idea prepared",
            "estimated_price_usd": 5,
            "sales": 0,
            "revenue_usd": 0,
        },
        {
            "name": "Personal Budget Planner",
            "type": "Digital template",
            "description": (
                "A simple template to track income, expenses "
                "and savings."
            ),
            "target_audience": (
                "Individuals and small businesses"
            ),
            "status": "Idea prepared",
            "estimated_price_usd": 3,
            "sales": 0,
            "revenue_usd": 0,
        },
        {
            "name": "Beginner Python Guide",
            "type": "Ebook",
            "description": (
                "A practical introduction to Python "
                "programming with simple exercises."
            ),
            "target_audience": "Programming beginners",
            "status": "Idea prepared",
            "estimated_price_usd": 5,
            "sales": 0,
            "revenue_usd": 0,
        },
    ]


# ============================================================
# PRODUCT ENGINE INTEGRATION
# ============================================================

def run_product_engine():
    """
    Run product_engine.py when it is available.

    If it fails, the opportunity agent continues running.
    """

    try:
        from product_engine import generate_products

        products = generate_products()

        if not isinstance(products, list):
            logger.warning(
                "product_engine.py did not return a list."
            )
            return []

        logger.info(
            "Products generated: %s",
            len(products)
        )

        return products

    except ImportError:
        logger.warning(
            "product_engine.py is not available. "
            "Using product ideas only."
        )

    except Exception as exc:
        logger.exception(
            "Product engine failed: %s",
            exc
        )

    return []


# ============================================================
# REPORT GENERATION
# ============================================================

def create_report(
    opportunities,
    product_ideas,
    generated_products,
    source_status
):
    """Build the JSON report."""

    total = len(opportunities)

    high_priority = [
        item
        for item in opportunities
        if item.get("score", 0) >= 70
    ]

    report = {
        "agent": AGENT_NAME,
        "version": AGENT_VERSION,
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "status": "completed",

        "summary": {
            "opportunities_found": total,
            "high_priority_opportunities": len(high_priority),
            "product_ideas": len(product_ideas),
            "products_generated": len(generated_products),
            "verified_sales": 0,
            "verified_revenue_usd": 0,
        },

        "source_status": source_status,

        "opportunities": opportunities,

        "product_ideas": product_ideas,

        "generated_products": generated_products,

        "notice": (
            "Opportunity scores are estimates. "
            "Payments, legitimacy, eligibility and sales "
            "must be independently verified."
        ),
    }

    return report


def save_json_report(report):
    """Save report.json."""

    with JSON_REPORT.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2
        )

    logger.info("Saved %s", JSON_REPORT)


def save_markdown_report(report):
    """Save a readable Markdown report."""

    summary = report["summary"]

    lines = [
        f"# {report['agent']}",
        "",
        f"**Version:** {report['version']}",
        "",
        f"**Generated:** {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Opportunities found: {summary['opportunities_found']}",
        f"- High-priority opportunities: {summary['high_priority_opportunities']}",
        f"- Product ideas: {summary['product_ideas']}",
        f"- Products generated: {summary['products_generated']}",
        "- Verified sales: 0",
        "- Verified revenue: $0",
        "",
        "## Source status",
        "",
    ]

    for source, status in report["source_status"].items():
        lines.append(f"- **{source}:** {status}")

    lines.extend([
        "",
        "## Top opportunities",
        "",
    ])

    opportunities = report["opportunities"]

    if not opportunities:
        lines.append(
            "No opportunities were found during this run."
        )

    for index, item in enumerate(
        opportunities[:20],
        start=1
    ):

        lines.extend([
            f"### {index}. {item['title']}",
            "",
            f"- **Source:** {item['source']}",
            f"- **Score:** {item['score']}/100",
            f"- **URL:** {item['url']}",
            f"- **Status:** {item['status']}",
            "",
        ])

        if item.get("description"):
            description = re.sub(
                r"\s+",
                " ",
                item["description"]
            )

            lines.extend([
                description[:400],
                "",
            ])

    lines.extend([
        "",
        "## Digital product ideas",
        "",
    ])

    for product in report["product_ideas"]:

        lines.extend([
            f"### {product['name']}",
            "",
            f"- **Type:** {product['type']}",
            f"- **Status:** {product['status']}",
            f"- **Estimated price:** "
            f"${product['estimated_price_usd']}",
            "",
            product["description"],
            "",
        ])

    lines.extend([
        "",
        "## Generated products",
        "",
    ])

    if not report["generated_products"]:
        lines.append(
            "No products were generated by product_engine.py."
        )
    else:
        for product in report["generated_products"]:
            lines.append(
                f"- {json.dumps(product, ensure_ascii=False)}"
            )

    lines.extend([
        "",
        "---",
        "",
        "**Important:** Scores are estimates. "
        "No income or sales are guaranteed. "
        "Verify every opportunity before acting.",
        "",
    ])

    with MARKDOWN_REPORT.open(
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(lines))

    logger.info("Saved %s", MARKDOWN_REPORT)


# ============================================================
# MAIN
# ============================================================

def main():

    logger.info(
        "Starting %s version %s",
        AGENT_NAME,
        AGENT_VERSION
    )

    source_status = {}

    # 1. Search GitHub.
    logger.info("Searching GitHub Issues...")

    try:
        github_opportunities = search_github()

        source_status["GitHub Issues"] = (
            f"OK: {len(github_opportunities)} results"
        )

    except Exception as exc:
        logger.exception("GitHub search failed: %s", exc)

        github_opportunities = []

        source_status["GitHub Issues"] = (
            f"Error: {str(exc)[:200]}"
        )

    # 2. Search Remote OK.
    logger.info("Searching Remote OK...")

    try:
        remoteok_opportunities = search_remoteok()

        source_status["Remote OK"] = (
            f"OK: {len(remoteok_opportunities)} results"
        )

    except Exception as exc:
        logger.exception("Remote OK search failed: %s", exc)

        remoteok_opportunities = []

        source_status["Remote OK"] = (
            f"Error: {str(exc)[:200]}"
        )

    # 3. Combine and filter opportunities.
    combined = (
        github_opportunities
        + remoteok_opportunities
    )

    opportunities = filter_opportunities(combined)

    # 4. Prepare digital product ideas.
    product_ideas = create_product_ideas()

    # 5. Run the optional product engine.
    generated_products = run_product_engine()

    # 6. Build and save reports.
    report = create_report(
        opportunities=opportunities,
        product_ideas=product_ideas,
        generated_products=generated_products,
        source_status=source_status,
    )

    save_json_report(report)

    save_markdown_report(report)

    logger.info("Agent execution completed.")

    logger.info(
        "Found %s opportunities.",
        len(opportunities)
    )

    logger.info(
        "Generated %s products.",
        len(generated_products)
    )

    return report


if __name__ == "__main__":

    try:
        main()

    except Exception as exc:
        logger.exception(
            "Fatal agent error: %s",
            exc
        )

        raise
