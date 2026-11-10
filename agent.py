import time
import traceback
import json
import os
import shutil

from pathlib import Path

from database import (
    init_db,
    save_opportunity,
    record_run
)

from research_agent import discover_opportunities
from analysis_agent import analyze_opportunities
from market_agent import crypto_market_snapshot, scan_arbitrage
from product_engine import generate_products
from execution_agent import execute_local_tasks
from publishing_agent import prepare_publication_queue
from payment_tracker import create_revenue_ledger
from improvement_agent import propose_improvements
from report_agent import write_reports

# Synchronisation Supabase
from supabase_store import sync_opportunities


VERSION = "1.2.0"

ROOT = Path(__file__).resolve().parent

REPORT_SOURCE = ROOT / "reports" / "report.json"

DASHBOARD_DIR = ROOT / "optimus-v3-reports"

DASHBOARD_REPORT = DASHBOARD_DIR / "latest.json"


def log(message):
    print(
        time.strftime("[%Y-%m-%d %H:%M:%S]"),
        message,
        flush=True
    )


# ============================================================
# 1. SYNCHRONISATION SUPABASE
# ============================================================

def synchronize_supabase():

    """Envoie les opportunités locales vers Supabase."""

    if not all([
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        os.getenv("SUPABASE_OWNER_ID")
    ]):

        log(
            "[SUPABASE] Configuration absente. "
            "Synchronisation ignorée."
        )

        return 0

    try:

        result = sync_opportunities()

        log(
            f"[SUPABASE] Synchronisation terminée : {result}"
        )

        return result

    except Exception as error:

        log(f"[SUPABASE] Erreur : {error}")

        traceback.print_exc()

        return 0


# ============================================================
# 2. PUBLICATION DU RAPPORT POUR LE DASHBOARD
# ============================================================

def publish_dashboard_report():

    """
    Copie le rapport complet vers l'emplacement
    utilisé par l'interface InfinityFree.
    """

    try:

        if not REPORT_SOURCE.exists():

            raise FileNotFoundError(
                "reports/report.json introuvable."
            )

        # Vérification du JSON source

        with REPORT_SOURCE.open(
            "r",
            encoding="utf-8"
        ) as file:

            report_data = json.load(file)

        if not isinstance(report_data, dict):

            raise ValueError(
                "Le rapport source doit être un objet JSON."
            )

        # Création du dossier dashboard

        DASHBOARD_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        temporary_file = (
            DASHBOARD_DIR / "latest.tmp"
        )

        # Écriture temporaire

        temporary_file.write_text(
            json.dumps(
                report_data,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        # Vérification du fichier temporaire

        with temporary_file.open(
            "r",
            encoding="utf-8"
        ) as file:

            json.load(file)

        # Remplacement atomique

        temporary_file.replace(
            DASHBOARD_REPORT
        )

        log(
            "[DASHBOARD] Rapport publié : "
            + str(DASHBOARD_REPORT)
        )

        return {
            "status": "SUCCESS",
            "path": str(DASHBOARD_REPORT),
            "opportunities": (
                report_data.get("summary", {})
                .get("opportunities_found", 0)
            )
        }

    except Exception as error:

        log(
            f"[DASHBOARD] Échec de publication : {error}"
        )

        traceback.print_exc()

        return {
            "status": "FAILED",
            "error": str(error)
        }


# ============================================================
# 3. CONTROLEUR PRINCIPAL
# ============================================================

def main():

    start = int(time.time())

    log("=" * 55)

    log("AUTO-EARN AI ULTRA v" + VERSION)

    log("Démarrage du système")

    log("=" * 55)

    # --------------------------------------------------------
    # 1. INITIALISATION
    # --------------------------------------------------------

    init_db()

    log(
        "[INIT] Base de données locale initialisée."
    )

    # --------------------------------------------------------
    # 2. RECHERCHE DES OPPORTUNITÉS - R1
    # --------------------------------------------------------

    log(
        "[R1] Recherche des opportunités..."
    )

    raw_opportunities = discover_opportunities()

    if raw_opportunities is None:

        raw_opportunities = []

    log(
        f"[R1] Résultats collectés : "
        f"{len(raw_opportunities)}"
    )

    # --------------------------------------------------------
    # 3. ANALYSE ET NOTATION - R3
    # --------------------------------------------------------

    log(
        "[R3] Analyse des opportunités..."
    )

    opportunities = analyze_opportunities(
        raw_opportunities
    )

    if opportunities is None:

        opportunities = []

    log(
        f"[R3] Opportunités analysées : "
        f"{len(opportunities)}"
    )

    # --------------------------------------------------------
    # 4. ENREGISTREMENT LOCAL
    # --------------------------------------------------------

    saved = 0

    for opportunity in opportunities:

        try:

            save_opportunity(opportunity)

            saved += 1

        except Exception as error:

            log(
                f"[DATABASE] Échec d'enregistrement : {error}"
            )

    log(
        f"[DATABASE] Opportunités enregistrées : {saved}"
    )

    # --------------------------------------------------------
    # 5. SYNCHRONISATION SUPABASE
    # --------------------------------------------------------

    log(
        "[SUPABASE] Synchronisation en cours..."
    )

    synced = synchronize_supabase()

    # --------------------------------------------------------
    # 6. ANALYSE DU MARCHÉ CRYPTO
    # --------------------------------------------------------

    log(
        "[MARKET] Analyse du marché..."
    )

    try:

        crypto = crypto_market_snapshot()

    except Exception as error:

        log(
            f"[MARKET] Erreur snapshot : {error}"
        )

        crypto = {}

    try:

        arbitrage = scan_arbitrage()

    except Exception as error:

        log(
            f"[MARKET] Erreur arbitrage : {error}"
        )

        arbitrage = {
            "status": "error",
            "error": str(error)
        }

    # --------------------------------------------------------
    # 7. CRÉATION DE PRODUITS - R5
    # --------------------------------------------------------

    log(
        "[R5] Création des produits..."
    )

    try:

        products = generate_products() or []

    except Exception as error:

        log(
            f"[PRODUCTS] Erreur : {error}"
        )

        products = []

    # --------------------------------------------------------
    # 8. EXÉCUTION DES TÂCHES LOCALES - R4
    # --------------------------------------------------------

    log(
        "[R4] Exécution des tâches locales..."
    )

    try:

        execution = execute_local_tasks(
            products
        )

    except Exception as error:

        log(
            f"[EXECUTION] Erreur : {error}"
        )

        execution = {
            "status": "error",
            "error": str(error)
        }

    # --------------------------------------------------------
    # 9. PRÉPARATION DES PUBLICATIONS - R5
    # --------------------------------------------------------

    log(
        "[R5] Préparation des publications..."
    )

    try:

        publishing = prepare_publication_queue(
            products
        )

    except Exception as error:

        log(
            f"[PUBLISHING] Erreur : {error}"
        )

        publishing = {
            "status": "error",
            "error": str(error)
        }

    # --------------------------------------------------------
    # 10. SUIVI DES REVENUS - R6
    # --------------------------------------------------------

    log(
        "[R6] Suivi des revenus..."
    )

    try:

        revenue = create_revenue_ledger()

    except Exception as error:

        log(
            f"[REVENUE] Erreur : {error}"
        )

        revenue = {
            "verified_revenue_total": 0,
            "status": "error",
            "error": str(error)
        }

    # --------------------------------------------------------
    # 11. STATISTIQUES GÉNÉRALES
    # --------------------------------------------------------

    recommended_count = sum(
        1
        for item in opportunities
        if item.get("recommended")
    )

    summary = {

        "version": VERSION,

        "opportunities_found": len(opportunities),

        "opportunities_saved": saved,

        "opportunities_synced": synced,

        "recommended_count": recommended_count,

        "products_created": len(products),

        "arbitrage_status": arbitrage.get(
            "status",
            "unknown"
        ),

        "live_trading_enabled": False,

        "external_actions_enabled": False,

        "automatic_publication_enabled": False,

        "supabase_enabled": bool(synced)

    }

    # --------------------------------------------------------
    # 12. AMÉLIORATION DU SYSTÈME - R6
    # --------------------------------------------------------

    log(
        "[R6] Analyse des améliorations..."
    )

    try:

        improvements = propose_improvements(
            summary
        )

    except Exception as error:

        log(
            f"[IMPROVEMENT] Erreur : {error}"
        )

        improvements = []

    # --------------------------------------------------------
    # 13. GÉNÉRATION DES RAPPORTS
    # --------------------------------------------------------

    log(
        "[REPORT] Génération des rapports..."
    )

    try:

        report = write_reports(
            summary,
            opportunities,
            crypto,
            execution,
            products,
            publishing,
            revenue,
            improvements
        )

    except Exception as error:

        log(
            f"[REPORT] Erreur : {error}"
        )

        report = None

    # --------------------------------------------------------
    # 14. PUBLICATION POUR L'INTERFACE
    # --------------------------------------------------------

    dashboard = publish_dashboard_report()

    # --------------------------------------------------------
    # 15. HISTORIQUE DES EXÉCUTIONS
    # --------------------------------------------------------

    end = int(time.time())

    try:

        record_run(
            VERSION,
            start,
            end,
            summary
        )

    except Exception as error:

        log(
            f"[DATABASE] Erreur historique : {error}"
        )

    # --------------------------------------------------------
    # 16. RAPPORT FINAL
    # --------------------------------------------------------

    duration = end - start

    log("=" * 55)

    log("RAPPORT FINAL")

    log("=" * 55)

    log(
        f"Opportunités trouvées : "
        f"{len(opportunities)}"
    )

    log(
        f"Opportunités enregistrées : {saved}"
    )

    log(
        f"Opportunités synchronisées : {synced}"
    )

    log(
        f"Opportunités recommandées : "
        f"{recommended_count}"
    )

    log(
        f"Produits créés : {len(products)}"
    )

    log(
        "Revenus vérifiés : $"
        + str(
            revenue.get(
                "verified_revenue_total",
                0
            )
        )
    )

    log(
        f"Dashboard : {dashboard.get('status')}"
    )

    log(
        f"Durée : {duration} secondes"
    )

    log(
        f"Rapport : {report}"
    )

    log("=" * 55)

    log(
        "AUTO-EARN AI ULTRA : TERMINÉ"
    )

    log("=" * 55)

    return summary


# ============================================================
# 4. DÉMARRAGE
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        log(
            "Arrêt demandé."
        )

    except Exception:

        log(
            "ERREUR CRITIQUE"
        )

        traceback.print_exc()

        raise
