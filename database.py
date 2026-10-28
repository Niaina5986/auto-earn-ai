"""Database manager for AUTO-EARN AI ULTRA."""

import json
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "auto_earn.sqlite3"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id TEXT PRIMARY KEY,
            source TEXT,
            title TEXT,
            url TEXT,
            description TEXT,
            category TEXT,
            reward_text TEXT,
            score REAL,
            risk TEXT,
            status TEXT,
            discovered_at INTEGER,
            raw_json TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            title TEXT,
            kind TEXT,
            created_at INTEGER,
            status TEXT,
            metadata_json TEXT
        );

        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset TEXT,
            quantity REAL,
            entry_price REAL,
            current_price REAL,
            note TEXT,
            created_at INTEGER,
            updated_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS portfolio_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            asset TEXT,
            quantity REAL,
            price REAL,
            note TEXT,
            created_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT,
            started_at INTEGER,
            ended_at INTEGER,
            summary_json TEXT
        );

        CREATE TABLE IF NOT EXISTS improvements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_from TEXT,
            version_to TEXT,
            proposal TEXT,
            evidence_json TEXT,
            status TEXT,
            created_at INTEGER
        );
        """)


def upsert_opportunity(item):
    with connect() as conn:
        conn.execute("""
            INSERT INTO opportunities (
                id, source, title, url, description, category,
                reward_text, score, risk, status, discovered_at, raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                description=excluded.description,
                reward_text=excluded.reward_text,
                score=excluded.score,
                risk=excluded.risk,
                raw_json=excluded.raw_json
        """, (
            item["id"],
            item.get("source", ""),
            item.get("title", ""),
            item.get("url", ""),
            item.get("description", ""),
            item.get("category", "other"),
            item.get("reward_text", ""),
            float(item.get("score", 0)),
            item.get("risk", "unknown"),
            item.get("status", "discovered"),
            int(item.get("discovered_at", time.time())),
            json.dumps(item.get("raw", {}), ensure_ascii=False),
        ))


def save_product(path, title, kind, status="draft", metadata=None):
    with connect() as conn:
        conn.execute("""
            INSERT INTO products (
                path, title, kind, created_at, status, metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(path),
            title,
            kind,
            int(time.time()),
            status,
            json.dumps(metadata or {}, ensure_ascii=False),
        ))


def record_run(version, started, ended, summary):
    with connect() as conn:
        conn.execute("""
            INSERT INTO runs (version, started_at, ended_at, summary_json)
            VALUES (?, ?, ?, ?)
        """, (
            version,
            started,
            ended,
            json.dumps(summary, ensure_ascii=False),
        ))


def list_portfolio():
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM portfolio ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def add_paper_position(asset, quantity, price, note="simulation only"):
    now = int(time.time())

    with connect() as conn:
        conn.execute("""
            INSERT INTO portfolio (
                asset, quantity, entry_price, current_price,
                note, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (asset, quantity, price, price, note, now, now))

        conn.execute("""
            INSERT INTO portfolio_events (
                event_type, asset, quantity, price, note, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("PAPER_BUY", asset, quantity, price, note, now))


def update_paper_price(asset, price):
    with connect() as conn:
        conn.execute("""
            UPDATE portfolio
            SET current_price = ?, updated_at = ?
            WHERE asset = ?
        """, (price, int(time.time()), asset))


def add_improvement(
    version_from, version_to, proposal, evidence, status="proposed"
):
    with connect() as conn:
        conn.execute("""
            INSERT INTO improvements (
                version_from, version_to, proposal,
                evidence_json, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            version_from,
            version_to,
            proposal,
            json.dumps(evidence, ensure_ascii=False),
            status,
            int(time.time()),
        ))
