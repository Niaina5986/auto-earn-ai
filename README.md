# AUTO-EARN AI ULTRA v1.0.0

## Install and run
Python 3.10+; no external packages needed. Run `python agent.py`.

## Sources currently integrated
- Jobbi public gigs feed: https://jobbi.org/gigs.json
- Himalayas public jobs API: https://himalayas.app/jobs/api
- Remote OK public API: https://remoteok.com/api
- GitHub Search Issues API (optional `GITHUB_TOKEN` for higher limits)
- CoinGecko public market data for selected crypto assets

This searches multiple public sources, not literally every website. Some services require accounts, API keys, eligibility, and terms compliance. It does not scrape login-protected sites.

## Outputs
- `reports/report.md`, `reports/report.json`
- `reports/publication_queue.json`
- `reports/revenue_ledger.json`
- `reports/improvement_proposals.json`
- `products/` generated drafts
- `data/auto_earn.sqlite3` SQLite database

## Important limits
No guaranteed earnings. The product drafts are not automatically sold. Live crypto trades, wallet access, payments, applications, and external publishing are not implemented. Arbitrage requires timestamped quotes from multiple exchanges and all fees, slippage, network/withdrawal costs; default behavior does not claim arbitrage exists. Never enter seed phrases/private keys. Review any opportunity for Madagascar eligibility and payout access.

## GitHub Actions
Run the workflow manually from Actions or wait for its daily schedule. Download the workflow artifact to get reports/products. Artifacts expire after 30 days and are not automatically committed to the repository.

## Versioning / self-improvement
The agent proposes changes based on run results; it does not rewrite its own production code automatically. Promote a new version only after review and tests.
