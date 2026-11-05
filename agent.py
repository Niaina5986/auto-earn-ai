import time
import traceback
import json
import os

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


VERSION = "1.1.0"


def log(message):
    print(
        time.strftime("[%Y-%m-%d %H:%M:%S]"),
        message,
        flush=True
    )


def synchronize_supabase():
    """Envoie les opportunités locales vers Supabase."""

    if not all([
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        os.getenv("SUPABASE_OWNER_ID")
    ]):
        log("[SUPABASE] Configuration absente. Synchronisation ignorée.")
        return 0

    try:
        result = sync_opportunities()
        log(f"[SUPABASE] Synchronisation terminée : {result}")
        return result

    except Exception as error:
        log(f"[SUPABASE] Erreur : {error}")
        traceback.print_exc()
        return 0


def main():

    start = int(time.time())

    log("=" * 55)
    log("AUTO-EARN AI ULTRA v" + VERSION)
    log("Démarrage du système")
    log("=" * 55)

    # 1. Initialisation
    init_db()
    log("[INIT] Base de données locale initialisée.")

    # 2. Recherche des opportunités
    log("[R1] Recherche des opportunités...")

    raw_opportunities = discover_opportunities()

    if raw_opportunities is None:
        raw_opportunities = []

    log(f"[R1] Résultats collectés : {len(raw_opportunities)}")

    # 3. Analyse et notation
    log("[R3] Analyse des opportunités...")

    opportunities = analyze_opportunities(raw_opportunities)

    if opportunities is None:
        opportunities = []

    log(f"[R3] Opportunités analysées : {len(opportunities)}")

    # 4. Enregistrement local
    saved = 0

    for opportunity in opportunities:

        try:
            save_opportunity(opportunity)
            saved += 1

        except Exception as error:
            log(f"[DATABASE] Échec d'enregistrement : {error}")

    log(f"[DATABASE] Opportunités enregistrées : {saved}")

    # 5. Synchronisation Supabase
    log("[SUPABASE] Synchronisation en cours...")

    synced = synchronize_supabase()

    # 6. Analyse du marché crypto
    log("[MARKET] Analyse du marché...")

    try:
        crypto = crypto_market_snapshot()
    except Exception as error:
        log(f"[MARKET] Erreur snapshot : {error}")
        crypto = {}

    try:
        arbitrage = scan_arbitrage()
    except Exception as error:
        log(f"[MARKET] Erreur arbitrage : {error}")
        arbitrage = {"status": "error"}

    # 7. Création de produits numériques
    log("[R5] Création des produits...")

    try:
        products = generate_products() or []
    except Exception as error:
        log(f"[PRODUCTS] Erreur : {error}")
        products = []

    # 8. Exécution des tâches locales autorisées
    log("[R4] Exécution des tâches locales...")

    try:
        execution = execute_local_tasks(products)
    except Exception as error:
        log(f"[EXECUTION] Erreur : {error}")
        execution = {}

    # 9. Préparation des publications
    log("[R5] Préparation des publications...")

    try:
        publishing = prepare_publication_queue(products)
    except Exception as error:
        log(f"[PUBLISHING] Erreur : {error}")
        publishing = {}

    # 10. Suivi des revenus
    log("[R6] Suivi des revenus...")

    try:
        revenue = create_revenue_ledger()
    except Exception as error:
        log(f"[REVENUE] Erreur : {error}")
        revenue = {
            "verified_revenue_total": 0
        }

    # 11. Statistiques générales
    recommended_count = sum(
        1 for item in opportunities
        if item.get("recommended")
    )

    summary = {
        "version": VERSION,
        "opportunities_found": len(opportunities),
        "opportunities_saved": saved,
        "opportunities_synced": synced,
        "recommended_count": recommended_count,
        "products_created": len(products),
        "arbitrage_status": arbitrage.get("status", "unknown"),
        "live_trading_enabled": False,
        "external_actions_enabled": False,
        "automatic_publication_enabled": False,
        "supabase_enabled": bool(synced)
    }

    # 12. Amélioration du système
    log("[R6] Analyse des améliorations...")

    try:
        improvements = propose_improvements(summary)
    except Exception as error:
        log(f"[IMPROVEMENT] Erreur : {error}")
        improvements = []

    # 13. Génération des rapports
    log("[REPORT] Génération des rapports...")

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
        log(f"[REPORT] Erreur : {error}")
        report = None

    # 14. Enregistrement de l'exécution
    end = int(time.time())

    try:
        record_run(
            VERSION,
            start,
            end,
            summary
        )
    except Exception as error:
        log(f"[DATABASE] Erreur historique : {error}")

    # 15. Résultat final
    duration = end - start

    log("=" * 55)
    log("RAPPORT FINAL")
    log("=" * 55)

    log(f"Opportunités trouvées : {len(opportunities)}")
    log(f"Opportunités enregistrées : {saved}")
    log(f"Opportunités synchronisées : {synced}")
    log(f"Opportunités recommandées : {recommended_count}")
    log(f"Produits créés : {len(products)}")
    log(
        "Revenus vérifiés : $"
        + str(revenue.get("verified_revenue_total", 0))
    )
    log(f"Durée : {duration} secondes")
    log(f"Rapport : {report}")

    log("=" * 55)
    log("AUTO-EARN AI ULTRA : TERMINÉ")
    log("=" * 55)

    return summary


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        log("Arrêt demandé.")

    except Exception:
        log("ERREUR CRITIQUE")
        traceback.print_exc()
        raise
