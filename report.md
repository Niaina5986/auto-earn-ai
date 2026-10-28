# AUTO-EARN AI ULTRA

- Version : 3.0
- Généré le : 2026-10-28T05:33:56.760199+00:00
- Opportunités analysées : 50
- Opportunités prioritaires : 50

> Le score est un indicateur de tri, pas une garantie de revenu.
> Les paiements et l'éligibilité doivent être vérifiés.

## Opportunités

### [[$450] One command to run the full SpaceApp stack from source for contributors](https://github.com/oll4com/spaceapp/issues/65)

- Source : GitHub Issues
- Score : 90/100
- Priorité : HAUTE
- Catégorie : produit_numerique
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : produit_numerique
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

## Context A contributor can build SpaceApp, run its test suites and run a simulated CLI task (`npm run smoke:offline`), but cannot easily run the **whole application from source**. `CONTRIBUTING.md` has no instructions for it. The root scripts `dev:api`, `dev:web` and `dev:worker` each start one process and expect everything else to be there already. In an installed SpaceApp, the containers wire that up (`deploy/docker/*-entrypoint.sh`, `core-supervisor.mjs`, `packages/run-spaceapp/templates/compose.yml`): - PostgreSQL with pgvector, and the migrations; - Temporal for the worker; - the CLI host on a Unix socket, with the `*-vscode-parity` wrapper commands it launches; - a session secret, the one-time owner setup token, and a few dozen `SPACE_*` paths. So anyone who wants to change a pane, the Room Agent or the memory graph and see the result in a browser must rebuild Docker images, or reverse-engineer the entrypoints. [`KNOWN_LIMITATIONS.md`](https://github.com/oll4com/spaceapp/blob/m

### [[$600] Support rootless Podman as a container engine in the run-spaceapp launcher](https://github.com/oll4com/spaceapp/issues/63)

- Source : GitHub Issues
- Score : 90/100
- Priorité : HAUTE
- Catégorie : produit_numerique
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : produit_numerique
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

## Context The `run-spaceapp` launcher (`packages/run-spaceapp`) installs and runs SpaceApp as a Docker Compose stack (`templates/compose.yml`: core, CLI, browser, PostgreSQL/pgvector, Temporal). Docker is the only supported engine. The launcher detects Docker and installs it if missing, and every lifecycle command (`install`, `up`, `down`, `status`, `logs`, `update`, `rollback`, `backup`, `restore`, `doctor`, `repair`, `uninstall`, `factory-reset`, `provider install`, `credentials set`, `owner …`) runs `docker compose …` or `docker …` (`composeCommand` in `src/index.mjs`, `spawnTrustedCommand` in `src/cli.mjs`, probes in `src/prerequisites.mjs` and `src/storage.mjs`). Many developers cannot or will not run a root Docker daemon: Fedora, RHEL and openSUSE ship Podman, some companies do not license Docker Desktop, and rootless containers are the safer default on a shared workstation. Today these users cannot install SpaceApp at all. ## Goal `run-spaceapp` runs the full stack on **rootles

### [[HYDRA] Paid work lead watch](https://github.com/p1ngtoohigh/Jarvus-Pub/issues/1)

- Source : GitHub Issues
- Score : 90/100
- Priorité : HAUTE
- Catégorie : produit_numerique
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : produit_numerique
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

HYDRA lead watch. Public candidate links only; no automatic proposals, purchases, or contracts. - [[BOUNTY $50] SKILL: Generate a structured CHANGELOG from git history](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/1) — updated 2026-10-14T23:06:44Z - [[BOUNTY $75] TEMPLATE: CLAUDE.md for a Next.js + SQLite SaaS project](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/2) — updated 2026-10-14T23:04:46Z - [[BOUNTY $200] WORKFLOW: n8n + Claude Code — automated weekly dev summary](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/5) — updated 2026-10-14T23:01:02Z - [[BOUNTY $150] AGENT: Claude Code sub-agent that reviews a PR and posts a structured comment](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/4) — updated 2026-10-14T22:56:18Z - [[Bounty $1,000] FP32 ttnn.cumsum returns NaN after infinity or overflow](https://github.com/tenstorrent/tt-metal/issues/58986) — updated 2026-10-14T22:49:26Z 

### [BOOTSTRAP-001: paid AI work and resource access, then human earnings](https://github.com/scottonchain/microcredit-agent-testbed/issues/17)

- Source : GitHub Issues
- Score : 90/100
- Priorité : HAUTE
- Catégorie : recherche
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : recherche
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

AI disclosure: the operator's ChatGPT assistant. **BOOTSTRAP-001 v2 — 2026-10-06.** Updated at the operator's request after current-market research. [Evidence and primary sources](https://github.com/scottonchain/microcredit-agent-testbed/issues/17#issuecomment-6016218420). This body is the current strategy; older comments remain historical evidence. The withdrawn real-device testing proposal stays withdrawn. ## Outcome Build an AI-operated route from a real customer's useful task to paid delivery, then give a person access to that route without requiring them to buy AI tools upfront. Poverty reduction is the purpose; the first human outcome is **positive spendable earnings from useful work, with no upfront personal payment or personal debt**. No human MFI partnership or further broad MFI discovery is required. AI-operated work can serve agent or ordinary business customers; this does not expand anyone's existing contact authority. Do not require every economic participant to be an AI o

### [SUCCESSOR Ω: Build the Next Discovery Lab — public integration checklist](https://github.com/MontrealAI/AGI-Alpha-Agent-v0/issues/4850)

- Source : GitHub Issues
- Score : 87/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

Build one connected bounded synthetic discovery lab across Alpha, Manager, Jobs and Fleet under the supplied2026-10-21 specification. No credential/security-setting changes, spending or wallet actions. Integration lead: Codex root. Work owners cover Alpha runtime/checkers, Alpha UI/history, currency receiver seams and Fleet admission, with separate same-session research and source reviewers. These are work roles, not maintainer or organizational independence claims. | Repository | Public work | Current scope | | --- | --- | --- | | Alpha | #4851 | Six constructors, finite checks, strict artifacts, existing-history v2 extension, UI and source-qualified evidence | | Manager | [#1613](https://github.com/MontrealAI/AGIJobManager/pull/1613) | Alternative USDC6 zero-cap local inspection; native release integration pending | | Jobs | [#4010](https://github.com/MontrealAI/AGIJobsv0/pull/4010) | Alternative AGIALPHA18 inspection; preserve publisher/telemetry baselines | | Fleet | [#64](https://

### [[Bounty] [STEAM VAULT] 🎮 Exchange 100,000 DOOM ($wDOOM) for a $10 Steam Digital Gift Card](https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/4114)

- Source : GitHub Issues
- Score : 85/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Montant monétaire mentionné
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

### 赏金平台 / Platform GitHub ### 原始链接 / Source URL https://github.com/doomsday-network/doomsday/issues/39 ### 漏洞描述 / Description [STEAM VAULT] 🎮 Exchange 100,000 DOOM ($wDOOM) for a $10 Steam Digital Gift Card! (10 / 10 Available — $100 USD Vault) ### 🎮 DoomVault — Redeem `100,000 DOOM` (`$wDOOM`) for a `$10 USD` Steam Digital Gift Card! **Vault Inventory:** 🟢 **`10 / 10 Cards Available` (`$100 USD` Total Vault)** **Exchange Rate:** **`100,000.0 DOOM` (Layer-1) or `100,000.0 wDOOM` (Base Mainnet)** = **`1x $10.00 USD Steam Digital Gift Card Code`** **Limit:** `1` redemption per verified GPU miner / GitHub developer (`10` total redemptions available). --- ### ⚡ How It Works (Mine Idle on Your Gaming PC $\to$ Buy Steam Games) 1. **Accumulate `100,000 DOOM` (or `wDOOM` on Base Mainnet):** - **Mine with your GPU (`0% Pool Fee`):** Download **[`Doomsday.exe`](https://doomsday.network/download/desktop)** or run `python mine_pool.py --wallet YOUR_DOOM_ADDRESS` at **[`https://doomsday.network`](

### [[Bounty] [STEAM VAULT] 🎮 Exchange 100,000 DOOM ($wDOOM) for a $10 Steam Digital Gift Card](https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/4113)

- Source : GitHub Issues
- Score : 85/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Montant monétaire mentionné
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

### 赏金平台 / Platform GitHub ### 原始链接 / Source URL https://github.com/doomsday-network/doom-pay/issues/4 ### 漏洞描述 / Description [STEAM VAULT] 🎮 Exchange 100,000 DOOM ($wDOOM) for a $10 Steam Digital Gift Card! (10 / 10 Available — $100 USD Vault) ### 🎮 DoomVault — Redeem `100,000 DOOM` (`$wDOOM`) for a `$10 USD` Steam Digital Gift Card! **Vault Inventory:** 🟢 **`10 / 10 Cards Available` (`$100 USD` Total Vault)** **Exchange Rate:** **`100,000.0 DOOM` (Layer-1) or `100,000.0 wDOOM` (Base Mainnet)** = **`1x $10.00 USD Steam Digital Gift Card Code`** **Limit:** `1` redemption per verified GPU miner / GitHub developer (`10` total redemptions available). --- ### ⚡ How It Works (Mine Idle on Your Gaming PC $\to$ Buy Steam Games) 1. **Accumulate `100,000 DOOM` (or `wDOOM` on Base Mainnet):** - **Mine with your GPU (`0% Pool Fee`):** Download **[`Doomsday.exe`](https://doomsday.network/download/desktop)** or run `python mine_pool.py --wallet YOUR_DOOM_ADDRESS` at **[`https://doomsday.network`](h

### [Senior Backend Engineer](https://remoteOK.com/remote-jobs/remote-senior-backend-engineer-duckduckgo-1137551)

- Source : Remote OK
- Score : 85/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- État de disponibilité non confirmé

**Description :**

<h1><strong>Who We Are </strong></h1><p>Hi, we're DuckDuckGo, the online protection company and remote-first team of 400+ on a mission to raise the standard of trust online. Founded in 2008 and profitable since 2014, our annual revenue is in the hundreds of millions USD and millions use our browser on <a class="ProsemirrorEditor-link" href="https://spreadprivacy.com/introducing-duckduckgo-for-mac/">Mac</a>, <a class="ProsemirrorEditor-link" href="https://spreadprivacy.com/windows-browser-open-beta/">Windows</a>, <a class="ProsemirrorEditor-link" href="https://spreadprivacy.com/duckduckgo-privacy-browser-ios14/">iOS</a>, and <a class="ProsemirrorEditor-link" href="https://spreadprivacy.com/introducing-app-tracking-protection/">Android</a>, our <a class="ProsemirrorEditor-link" href="https://duckduckgo.com/">search engine</a>, and the <a class="ProsemirrorEditor-link" href="https://duckduckgo.com/pro">DuckDuckGo subscription</a>. We also offer private, useful, and optional AI, including 

### [[wildcard] Compile fixed-rate task networks away: certified periodic Go kernels with explicit buffer budgets](https://github.com/limitlessprojects/Go-Hybrid/issues/378)

- Source : GitHub Issues
- Score : 82/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

### The idea, in a paragraph Offer an opt-in backend for **closed, fixed-rate, scalar-value task networks**: compile the network into a periodic sequential Go kernel with fixed-size ring buffers, instead of emitting one goroutine and Go channels for every logical actor. Emit a schedule certificate with production/consumption rates, initial tokens, actor firing counts and per-edge high-water marks. A small independent checker must replay the witness, reject underflow/overflow and require the final token counts to equal the initial counts before accepting a byte budget. This gives an admitted kernel a new, narrow guarantee: bounded FIFO token storage and no channel-token deadlock under the certified periodic schedule. Allocation-free step execution additionally requires a closed allocation-free actor registry. Unmodeled effects reject admission; ordinary Hybrid remains available outside the kernel. This is established synchronous dataflow applied to Hybrid, not a claim to have invented t

### [Director of Product Management and IT Operations](https://remoteOK.com/remote-jobs/remote-director-of-product-management-and-it-operations-self-bill-pro-1137536)

- Source : Remote OK
- Score : 80/100
- Priorité : HAUTE
- Catégorie : redaction
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : redaction
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- État de disponibilité non confirmé

**Description :**

<h4><strong><span style="color: #000000">About Self Bill Pro:</span></strong></h4><p><span style="color: #000000">Self Bill Pro is a rapidly growing startup dedicated to solving one of the most persistent challenges in the employee benefits ecosystem: the complexity of monthly benefits billing. We provide a tech-enabled service where our dedicated team leverages proprietary software to eliminate the administrative burdens of manual invoice audits and costly billing errors. Our mission is to streamline this critical operation, freeing up employers, brokers, and carriers to focus on their strategic priorities.</span></p><p style="min-height: 1.7em;"></p><p><strong><span style="color: #1B1C1D">About the Role: Compensation - $130,000 - 160,000<br /></span></strong><span style="color: #1B1C1D">We are seeking a highly motivated and experienced Director of Product Management and IT Operations to lead the strategic direction and operational execution of our proprietary software platform. This 

### [Contracts Manager Federal](https://remoteOK.com/remote-jobs/remote-contracts-manager-federal-akicita-federal-llc-1137522)

- Source : Remote OK
- Score : 80/100
- Priorité : HAUTE
- Catégorie : redaction
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : redaction
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- État de disponibilité non confirmé

**Description :**

\n<p></p><p><br></p><p></p>\n<div>$100,000 - $120,000 a year</div><small><div> <p style="margin: 0in 0in 6pt; line-height: 125%; font-size: 11pt; font-family: Calibri, sans-serif;">Akicita Federal, LLC is a growing 8(a) small business that delivers healthcare, professional, and administrative services to federal agencies. We're adding a contracts manager to help us grow beyond our current work. The job is to find opportunities, write winning proposals quickly, and build lasting relationships with agencies and teaming partners.</p> <h2 style="margin: 14pt 0in 6pt; font-size: 13pt; font-family: Calibri, sans-serif; color: #1f3864;">What you'll do</h2> <ul style="margin-top: 0in; margin-bottom: 4.0pt;"> <li style="margin: 0in 0in 4pt 0px; font-size: 11pt; font-family: Calibri, sans-serif;">Find and respond to federal opportunities, focusing on small business and 8(a) set-asides</li> <li style="margin: 0in 0in 4pt 0px; font-size: 11pt; font-family: Calibri, sans-serif;">Write, assemble, an

### [Senior React Full stack Developer](https://remoteOK.com/remote-jobs/remote-senior-react-full-stack-developer-lemon-io-1137475)

- Source : Remote OK
- Score : 80/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- État de disponibilité non confirmé

**Description :**

<p>Are you a talented Senior Developer looking for a remote job that lets you show your skills and get decent compensation? Look no further than <a href="https://lemon.io/for-developers/?utm_source=remoteok&amp;utm_medium=job_ad&amp;utm_campaign=supply_en_react_node/python/ruby_oct_2026_job_ad">Lemon.io</a> â the marketplace that connects you with hand-picked startups in the US and Europe.</p><p><strong>What we offer:</strong></p><ul><li>The rate depends on your seniority level, skills and experience. We've already paid out over $11M to our engineers.</li><li>No more hunting for clients or negotiating rates â let us handle the business side of things so you can focus on what you do best.</li><li>We'll manually find the best project for you according to your skills and preferences.</li><li>Choose a schedule that works best for you. Itâs possible to communicate async or minimally overlap within team working hours.</li><li>We respect your seniority so you can expect no micromanageme

### [Bounty: end-to-end test copperhead create (brief → clean full run) + findings report](https://github.com/copperheadhq/copperhead/issues/66)

- Source : GitHub Issues
- Score : 80/100
- Priorité : HAUTE
- Catégorie : redaction
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : redaction
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- Publication ancienne : vérifier si elle est active

**Description :**

> 💰 **BOUNTY — $50 USD** > Tracked in **#💰・bounties**. Claim by commenting below. **First mergeable PR wins; paid on merge, not on submission.** Claims expire after 2 days without visible progress. Keep fix discussion on this issue, not in the channel. Discord: https://discord.com/channels/1527265832730628136/1529900631735799828/1530129559868149800 ## Summary `copperhead create` is an **8-stage pipeline** (spec-seed → architecture → part-selection → schematic → layout-draft → outputs → firmware → dev-plan) that turns a natural-language brief into manufacturable KiCad artifacts. Each stage is committed independently, and a full board is built over multiple invocations. There is rich per-stage instrumentation but **no end-to-end coverage that proves the whole pipeline runs clean from a brief to a committed final stage.** Manual driving of the pipeline has repeatedly wedged mid-run (most recently at stage 4, schematic) and surfaced a string of blockers, defects, and inefficiencies. We wan

### [[BOUNTY $50] SKILL: Generate a structured CHANGELOG from git history](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/1)

- Source : GitHub Issues
- Score : 80/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- Publication ancienne : vérifier si elle est active

**Description :**

## 💰 Bounty: $50 — powered by [Opire](https://opire.dev) ## Description Create a Claude Code skill (`SKILL.md`) or a bash script that automatically generates a structured `CHANGELOG.md` from a project's git history. ## Acceptance Criteria - [ ] Works via `/generate-changelog` command or `bash changelog.sh` - [ ] Fetches commits since the last git tag - [ ] Auto-categorizes into: `Added` / `Fixed` / `Changed` / `Removed` - [ ] Outputs a properly formatted `CHANGELOG.md` - [ ] Tested on a real GitHub repo (include a sample output in the PR) - [ ] README with setup instructions in 3 steps or fewer ## How to Claim 1. Comment `/opire try` in this issue 2. Submit a PR with your solution 3. Payment is released automatically on merge ✅ ## Accepted Stack Bash, Python, or native Claude Code `SKILL.md`.

### [Senior Software Engineer](https://remoteOK.com/remote-jobs/remote-senior-software-engineer-klardaten-1137571)

- Source : Remote OK
- Score : 77/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés
- État de disponibilité non confirmé

**Description :**

<p>Klardaten connects DATEV with other software and AI applications. Weâre hiring 1â2 senior engineers to own product development, DATEV integrations and automation.</p><p><strong>Based in the EU Â· Remote or Berlin Â· Full time Â· Permanent or contract Â· Start as soon as possible</strong></p><h2>Own the outcome</h2><p>Once we agree on a general goal, you independently work out what to build and how to deliver it. You investigate the problem, define the scope, make technical decisions and carry the work through implementation, testing, deployment and follow-up.</p><h2>What you will do</h2><ul><li>Turn general product goals into clear requirements, a practical scope and technical decisions.</li><li>Build product features, DATEV integrations and automations across frontend and backend.</li><li>Own testing, deployment and ongoing improvement, including resolving problems in production.</li><li>Find answers, resolve blockers and keep the founders informed. Raise decisions that need di

### [Senior DevOps Engineer](https://remoteOK.com/remote-jobs/remote-senior-devops-engineer-lemon-io-1137557)

- Source : Remote OK
- Score : 77/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés
- État de disponibilité non confirmé

**Description :**

<p><a href="https://lemon.io/for-developers/?utm_source=remoteok&amp;utm_medium=job_ad&amp;utm_campaign=supply_en_devops_oct_2026_job_ad">Lemon.io</a> helps companies in the US and Europe hire experienced engineers, from funded startups to teams like Klarna, Retool, and Pinterest. Weâve been doing this since 2015, and more than 1,500 companies have hired engineers through us.</p><p>New roles for Senior DevOps Engineers come in all the time, and several are open right now.</p><p><strong>Two ways to work with clients</strong></p><ul><li><strong>Contract:</strong> most roles are contract-based. You join the clientâs team and work as part of it.</li><li><strong>Direct hire:</strong> some clients hire engineers full-time, and we support you through the process.</li></ul><p>Because companies trust our vetting, applying through <a href="https://lemon.io/for-developers/?utm_source=remoteok&amp;utm_medium=job_ad&amp;utm_campaign=supply_en_devops_oct_2026_job_ad">Lemon.io</a> is often a shor

### [[good first issue, hacktoberfest] 🪭 Hacktoberfest Task - Add new Japan Fact 3085 (good-first-issue)](https://github.com/lingdojo/kana-dojo/issues/33244)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## 🟢 Good First Issue: Add Japan Fact #308 — Beginner-Friendly Open Source Contribution ![Time: <1 minute](https://img.shields.io/badge/Time-<1_minute-brightgreen) ![Difficulty: Beginner](https://img.shields.io/badge/Difficulty-Beginner-blue) ![No Code Required](https://img.shields.io/badge/No_Code-Required-orange) > 🟢 **No prerequisites needed!** You don't need to clone the repo, install anything, or write code. > This entire contribution can be done from your browser in under 60 seconds. **Labels:** good first issue, help wanted, hacktoberfest **Language:** JSON (no coding required) **Time:** < 1 minute **Skill Level:** Absolute beginner --- ## 🎋 Add New Japan Fact **Category:** Community Contribution - Fun Fact **Difficulty:** Easy (good first issue!) **Estimated Time:** <1 min --- ### 🎯 Your Task Add this interesting fact about Japan to our collection! ### The Fact > 'Furoshiki' are reusable cloth wraps used to carry goods or wrap gifts, often with artistic patterns. ### 📝 Instruct

### [Uppercase ISBN and LCC search fields are not normalized before Solr queries](https://github.com/internetarchive/openlibrary/issues/14142)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## Summary Open Library accepts search field names case-insensitively, but `WorkSearchScheme` does not consistently normalize recognized field names before emitting Solr queries. For example, lowercase `isbn:` and `lcc:` queries work with the indexed fixture, while their uppercase equivalents (`ISBN:` and `LCC:`) retain the uppercase field names and produce undefined-field errors in Solr. The field-recognition path uses case-insensitive matching, but `transform_user_query()` preserves field names that are not explicitly rewritten through `field_name_map`. Consequently, uppercase `ISBN` and `LCC` also bypass their corresponding lowercase-specific transformations. ## Version and environment - Repository: https://github.com/internetarchive/openlibrary - Checked commit: `6d66f877b83af3d4557d766f4f156165add8e405` (source checked on 2026-10-25). - Linux; Python 3.14.5 and the checkout’s test requirements. The parsing checks use luqum 0.11.0. Building psycopg2 requires PostgreSQL development 

### [[Fleet V1 四线总收口] serverosd / Device Ability / CloudCLI-Node-Hub / Commander Skills：功能+目录+CI+发布一口气并行](https://github.com/ProfessorZhi/serveros/issues/434)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

# Four-pillar V1 closure / owner-approved one-shot Fleet delegation **Owner 2026-10-28: 一口气让 Fleet 四线齐头并进，把 V1 功能、目录/仓库收敛、独立构建发布与跨设备可验收收口。** This is a bounded long-horizon autonomous *development* handoff, not permission for GPT to hold a stream open and not automatic main merge or production deployment. Source-of-truth taxonomy: [#409](https://github.com/ProfessorZhi/serveros/issues/409), D1–D10 path convergence [#429](https://github.com/ProfessorZhi/serveros/issues/429), assembled RC [#425](https://github.com/ProfessorZhi/serveros/issues/425), out-of-GPT milestone delivery [#417](https://github.com/ProfessorZhi/serveros/issues/417). **Exactly FOUR deliverable components**, in the owner's order: | Pillar | Independent artifact and authoritative paths | Functional & directory closure DoD | Source candidates to integrate | |---|---|---|---| | **① serverosd / L1** | One C++-first resident daemon, native monitor + bounded recovery, package+source-of-truth owner map; `serverosd/` / `native

### [Handoff: finish and verify HW2 Basic A/B and Bonus Option B](https://github.com/chijenpeng/26-fall-DeepMIR-HW2/issues/5)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : redaction
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : redaction
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## Objective and deadline Finish the code, final models, generation, evaluation, and reviewable local result package for DeepMIR HW2 Basic A, Basic B, and Bonus **Option B** by **2026-10-29 23:59 Asia/Taipei**. **The student will write the report, handle the cloud link, and submit/comment on NTU COOL personally.** Assignment: `Homework_2.pdf` in the local workspace. Student ID R14725022. Keep this issue current for the next agent. Do not mark a planned command or development output as a completed deliverable. ## Code and review state (2026-10-27 ~22:30 Asia/Taipei) - Training source: immutable [tag `training-source-2026-10-27`](https://github.com/chijenpeng/26-fall-DeepMIR-HW2/tree/training-source-2026-10-27) at commit `63c4a55ba2962c95674eccbf687eec20c431279c` (fresh all-song provenance/configs). The tag keeps the exact launched code reachable after PR #4 was squash-merged. - Generation, export, audit, and documentation review: PR #4, https://github.com/chijenpeng/26-fall-DeepMIR-HW2/

### [ML startup fails on v3.3.0+ without CUDA memory-pool support](https://github.com/immich-app/immich/issues/32767)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

### I have searched the existing issues, both open and closed, to make sure this is not a duplicate report. - [x] Yes ### The bug Since v3.3.0, the CUDA ML container fails during startup which previously worked. Not being familiar with the codebase I used Codex to assist in troubleshooting and it seems related to the fact that I am using vGPU configurations on the box rather than raw driver access so the memory pool allocation fails. General configuration: Hypervisor: Proxmox VM: Rocky 10 Runtime: k3s (Podman) GPU: A2-4Q (time-sliced vGPU profile on VM. The raw GPU is shared with other VM's) ### The OS that Immich Server is running on Rocky 10 ### Version of Immich Server v3.3.5 ### Version of Immich Mobile App v3.3.5 ### Platform with the issue - [x] Server - [ ] Web - [ ] Mobile ### Device make and model _No response_ ### Your docker-compose.yml content ```YAML Helm values file: controllers: main: containers: main: image: tag: v3.3.5 env: REDIS_HOSTNAME: '{{ printf "%s-valkey" .Relea

### [DEADLINE Wed Oct 28 8PM PDT — Gate0.5 label-source recheck + YSSY 6+6 delivery-gap forensics before scale](https://github.com/HKcode22/ReplitTranvr/issues/173)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

# Immediate investigation and hardening — Gate 0.5 + YSSY **IMMEDIATE EXECUTION STATUS (no day-by-day waiting):** Gate0.5 local FIDS nested-field instrumentation and source-admission tests **already merged** [PR #174](https://github.com/HKcode22/ReplitTranvr/pull/174), 4/4 CI passed. Provider [OpenAPI 1.15.4.0](https://doc.aerodatabox.com/docs/openapi-rapidapi-v1.json) confirms `runwayTime` actual **or estimated**, `scheduledTime` departure not specifically scheduled wheels-off; identical paid GETs cannot prove original runway-delay estimand. [Immediate determination](https://github.com/HKcode22/ReplitTranvr/issues/173#issuecomment-6435300974). Proceeded directly to YSSY forensic drift-warning implementation [PR #175](https://github.com/HKcode22/ReplitTranvr/pull/175), undergoing offline CI; no provider calls/credits, no deployed monitoring yet. Wed Oct28 8pm remains the **latest checkpoint deadline**, not a planned work start. **Start:** Monday, **October 26, 2026, 10:53 PM PDT** (202

### [feedback: Python trial findings on rule precision and large-repo triage](https://github.com/sheepfling/alphus/issues/48)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## Trial context I ran the Python policy and review profiles against a large consumer repository (roughly 492 Python files), with Alphus pinned at `1d36ab0dae903ee2990163ec4a504b52b60afd71`. This is consolidated feedback from the trial log, not a claim that every finding was a false positive. The first broad scan reported 14,325 findings: 8,204 structure/style, 2,298 runtime-type, 813 JSON-decode, 231 path, 27 output-escaping, and 2,752 line-length findings. A later configured cleanup baseline tracked 10,171 findings. After 598 focused fix/review batches, the configured Python-policy, review, and default profiles all passed with zero findings (9/9, 4/4, and 2/2 steps). Many findings were useful and led to real improvements; the pain was separating those from pattern matches and understanding the implications of each fix. This complements [#44](https://github.com/sheepfling/alphus/issues/44)'s broader adoption/reporting work with rule-level observations from a long Python trial. ## Find

### [AI COMS health: board needs attention](https://github.com/0xSneaks/ai-coms/issues/13)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## AI COMS board check **Needs attention:** - stale claim (62h, may be taken): - [codex] muse-tune-up · INTENT standalone fomo-monitor deliverable (new local files only), tests + ai-coms sign-off; existing chatgpt advisory area untouched · started 2026-10-25 11:15 ET · ETA same session - OPEN request 46h old: - [codex → muse] musepad · v2 is indexed MUSEINU/FARTCOIN; post finalized creator-buy receipt, decoded reward config, dual-mint site preview and build-funding ledger; no unverified earnings claims · OPEN · 2026-10-26 → [handoff](handoffs/2026-10-26_0313_codex_musepad.md) · nudged 2026-10-27 · nudged 2026-10-28 - OPEN request 46h old: - [codex → muse] musepad · draft site copy preview and public treasury ledger format from evidence-led [brief](handoffs/2026-10-26_0240_codex_musepad.md); reconcile v1/v2 and holder-reward claims; no publish without Sneaks's go · OPEN · 2026-10-26 · nudged 2026-10-27 · nudged 2026-10-28 - OPEN request 49h old: - [chatgpt → codex] fomo-monitor · existi

### [[good first issue, hacktoberfest] 🍡 Hacktoberfest Task - Add new Learner Mistake 520 (good-first-issue)](https://github.com/lingdojo/kana-dojo/issues/33098)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## 🟢 Good First Issue: Add Learner Mistake #52 — Beginner-Friendly Open Source Contribution ![Time: <1 minute](https://img.shields.io/badge/Time-<1_minute-brightgreen) ![Difficulty: Beginner](https://img.shields.io/badge/Difficulty-Beginner-blue) ![No Code Required](https://img.shields.io/badge/No_Code-Required-orange) > 🟢 **No prerequisites needed!** You don't need to clone the repo, install anything, or write code. > This entire contribution can be done from your browser in under 60 seconds. **Labels:** good first issue, help wanted, hacktoberfest **Language:** JSON (no coding required) **Time:** < 1 minute **Skill Level:** Absolute beginner --- ## Add Common Japanese Learner Mistake **Category:** Community Contribution - Common Mistake **Difficulty:** Easy (good first issue!) **Estimated Time:** <1 min --- ### Your Task Add this common learner mistake pair to help others avoid frequent Japanese errors! ### The Common Mistake **Wrong:** もし雨が降ります、行きません。 **Correct:** もし雨が降ったら、行きません。 > 

### [[good first issue, hacktoberfest] 🥢 Hacktoberfest Task - Add new False Friend Pair 513 (good-first-issue)](https://github.com/lingdojo/kana-dojo/issues/33096)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## 🟢 Good First Issue: Add False Friend Pair #51 — Beginner-Friendly Open Source Contribution ![Time: <1 minute](https://img.shields.io/badge/Time-<1_minute-brightgreen) ![Difficulty: Beginner](https://img.shields.io/badge/Difficulty-Beginner-blue) ![No Code Required](https://img.shields.io/badge/No_Code-Required-orange) > 🟢 **No prerequisites needed!** You don't need to clone the repo, install anything, or write code. > This entire contribution can be done from your browser in under 60 seconds. **Labels:** good first issue, help wanted, hacktoberfest **Language:** JSON (no coding required) **Time:** < 1 minute **Skill Level:** Absolute beginner --- ## Add Japanese False Friend **Category:** Community Contribution - False Friend **Difficulty:** Easy (good first issue!) **Estimated Time:** <1 min --- ### Your Task Add this confusion pair to help learners avoid common Japanese mixups! ### The False Friend Pair **Term A:** シール (shiiru) **Term B:** seal (animal) > **Explanation:** シール usua

### [[Integration] M15–M17 workstream ledger — baseline 943deb6](https://github.com/zsoltacsai/wpcaregrid/issues/174)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : produit_numerique
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : produit_numerique
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

# M15–M17 integration ledger This issue is the durable integration ledger for the parallel workstreams. Update it with dated, evidence-linked comments as branches, PRs, checks, or staging releases change. The master contract remains [docs/MASTER_ROADMAP_AND_INTEGRATION_PLAN.md](https://github.com/zsoltacsai/wpcaregrid/blob/943deb62558940181b948771b7abdf70e76ae516/docs/MASTER_ROADMAP_AND_INTEGRATION_PLAN.md). This ledger does not change milestone status or authorize customer, staging, production, billing, credential, or infrastructure operations. ## Initial verified snapshot — 2026-10-24 20:31 UTC - Authoritative branch: `claude/ecstatic-wozniak-oemyuf` - Primary SHA: `943deb62558940181b948771b7abdf70e76ae516` (PR #173 merge; signed commit verified) - Exact-SHA CI: [run 40128417134](https://github.com/zsoltacsai/wpcaregrid/actions/runs/40128417134), 37/37 jobs successful; mandatory Server MySQL process-concurrency gate passed. - Active ruleset: [Authoritative primary release controls](h

### [Mingla Creators program: host discounts everywhere, creator gigs hosts book through Mingla, and paid Mingla Locals](https://github.com/Mingla-LLC/mingla-main/issues/3872)

- Source : GitHub Issues
- Score : 75/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

## Goal One revenue program with three parts: 1. **Host discounts and pricing** across trips, experiences, events and venues: codes, automatic discounts and sale prices. Per listing, the host chooses whether discounts apply at all; per discount, how it combines with others. 2. **Creator gigs.** Hosts turn on "Promote with creators" for a listing. Verified creators (who sign up in the Host app) register interest and quote their rates. The brand shapes the script, a Mingla representative approves and locks it, and after that the only revisions allowed are for sound and picture. The creator must post with the required tags, and Mingla verifies the post. The fee is held at hire and released when the post is verified. The creator's share of sales through their tracked link is split automatically on every sale. 3. **Mingla Locals.** Explorer users paid $150 a month per city by Mingla to visit one place a month. Their videos appear on a public profile that every user can see, and under "Local

### [Senior Growth Product Manager AI Native](https://remoteOK.com/remote-jobs/remote-senior-growth-product-manager-ai-native-magic-eden-1137414)

- Source : Remote OK
- Score : 74/100
- Priorité : HAUTE
- Catégorie : redaction
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : redaction
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- Publication relativement ancienne
- État de disponibilité non confirmé

**Description :**

<p style="min-height:1.5em"><strong>About Magic Eden and Dicey</strong><br />Magic Eden reached unicorn status in just 9 months after launch, one of the fastest in history. We built a category-defining NFT marketplace from scratch and proved we know how to move fast. Now we're doing it again. Dicey is our crypto casino and sportsbook platform, targeting the $180B+ iGaming and sports betting markets.</p><p style="min-height:1.5em">We're a small, fully remote team. We ship fast, we're hands-on with our data, and we're rebuilding how a growth team operates around AI from the ground up.</p><p style="min-height:1.5em"><strong>The role</strong><br />Most of the iGaming industry competes on acquisition. Almost nobody has figured out personalized retention, knowing who a player is, what they need right now, and what would actually change their behavior this week. That's the problem you'll own.</p><p style="min-height:1.5em">This role focuses on the full post-signup journey: expanding our playe

### [Renewables Project Scheduler](https://remoteOK.com/remote-jobs/remote-renewables-project-scheduler-transportation-partners-amp-logistics-1137194)

- Source : Remote OK
- Score : 74/100
- Priorité : HAUTE
- Catégorie : produit_numerique
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : produit_numerique
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- Publication relativement ancienne
- État de disponibilité non confirmé

**Description :**

Apply<br><br><strong>Description<br><br></strong><strong>Job Summary:<br><br></strong>The BESS Project Scheduler is responsible for developing, maintaining, and analyzing detailed project schedules for Battery Energy Storage System (BESS) projects. This role plays a critical part in ensuring projects are delivered on time by providing accurate schedule forecasts, identifying risks, and supporting project teams with data-driven insights across engineering, procurement, construction, commissioning, and energization phases. This role requires a strong leader that will take ownership of driving accurate and up to date scheduling across multiple projects as well as taking initiative to drive process improvements where there is an opportunity to improve.<br><br><strong>Job Responsibilities<br><br></strong><ul><li>Develop and maintain integrated project schedules for BESS projects from NTP through COD </li><li>Build schedules covering engineering, procurement, manufacturing, logistics, civil,

### [Senior Specialist Global QMS](https://remoteOK.com/remote-jobs/remote-senior-specialist-global-qms-orca-bio-1137072)

- Source : Remote OK
- Score : 74/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- Publication relativement ancienne
- État de disponibilité non confirmé

**Description :**

<p>More than one million people in the United States today are fighting blood cancer. While a traditional allogeneic stem cell transplant has been the best hope for many, the transplant itself can prove fatal or lead to serious conditions, such as graft vs. host disease. Orca Bio is a commercial-stage biotechnology company redefining the transplant process by developing next-generation cell therapies with the goal of providing significantly better survival rates with dramatically fewer risks.<strong>&nbsp;</strong><span style="font-size: inherit;">With our purified, high-precision cell therapies we hope to not only replace patients' blood and immune systems with healthy ones, but also restore their lives.</span></p><p><br></p><p>The <strong>Senior Specialist, Global QMS</strong> will help implement Orca Bioâs global quality management system across all sites. This role will support and lead the internal audit program, supplier management program, and inspection readiness. This role w

### [Java/Kotlin: request params with wrong names or locations, or missing (@JsonNaming, custom resolvers, JAX-RS sub-resources)](https://github.com/owasp-noir/noir/issues/3271)

- Source : GitHub Issues
- Score : 72/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

## Summary The Spring and JAX-RS analyzers report wrong request inputs in six cases. Some fields get the Java name instead of the wire name. Some values that the server injects are reported as client input. Some inputs get the wrong location, and some DTO fields are lost. Tools that build requests from `noir scan` output (curl, OAS, fuzzers) then send fields the server ignores and miss fields it reads. `--ai-context` and `noir query` show the same wrong inputs. Open #3254 covers `Map`/`JsonNode` bodies and form-as-query on Kotlin Spring. This issue does not repeat those cases. ### [ ] `@JsonNaming` and `spring.jackson.property-naming-strategy` are ignored Kotlin, class annotation: ```kotlin @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class) data class MessageRequest( val firstName: String, val orderId: Long, ) @RestController class MessageController { @PostMapping("/messages") fun send(@RequestBody req: MessageRequest): String = "ok" } ``` Kotlin, global setting (same contr

### [connector: light tool, sun, moon, twilight and Milky Way windows with a cloud verdict](https://github.com/jomcgi-org/homelab/issues/7367)

- Source : GitHub Issues
- Score : 72/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

Part of #7240 and #7359 (Astra lane). Effort: Astra medium to high. ## What A third question people bring to a Scottish trip, after "what should I do" (`plan`) and "is my plan on" (`check`): "when is the light". A `light` tool answering, for a point and a date range (same caps as `plan`): sunrise, sunset, civil, nautical and astronomical twilight, golden hour and blue hour windows, moonrise, moonset, phase and illumination, and the hours when the Milky Way core is above the horizon in the dark. Every window carries the cloud verdict from the existing stars snapshot where a site is within reach, otherwise `unknown`, so a photographer or stargazer gets "golden hour 16:42 to 17:31, clear" rather than times alone. No new data source: `internal/astro` already has `SunTimes`, `SunElevation`, `MoonAt`, `MoonAltitude` and `MoonIllumination`, tested against ephem and the hikes app. Galactic centre position is a fixed RA/Dec (17h45m, -29 deg) through the same sidereal-time path the moon code use

### [Honor the lines argument in MCPManager.Logs](https://github.com/hanzoai/agents/issues/9)

- Source : GitHub Issues
- Score : 72/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

## Summary `MCPManager.Logs` and `ProcessManager.GetProcessLogs` both take `follow` and `lines` and ignore both: they return the whole log file. The same body is copied in two places. ## Evidence Checked at `6ab6811`, under `control-plane/internal/mcp/`. - `manager.go:328` `func (m *MCPManager) Logs(alias string, follow bool, lines int)`; the body at `:336` says `// TODO: Implement follow and lines functionality` and returns `os.Open(logFile)`. - `process.go:401` `func (pm *ProcessManager) GetProcessLogs(alias string, follow bool, lines int)` has the same body and the same TODO (line 409). - `ls internal/mcp/*_test.go` finds no test file, so neither is covered. ## What to do Put the log-file lookup and the `lines` handling in one helper that both methods call. When `lines > 0`, return only the last `lines` lines of the file; when `lines <= 0`, return the whole file as today. Leave `follow` out of scope: say in the doc comment that it is not supported yet and narrow the TODO to `follow`

### [Make the agent counts in README.md match the files](https://github.com/hanzoai/agents/issues/8)

- Source : GitHub Issues
- Score : 72/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

## Summary `README.md` gives two different counts for the same thing (88 and 83 specialized agents), and none matches the files. Its structure tree also shows folders at the repo root that live under `.hanzo/agents/`. ## Evidence Checked at `6ab6811`. - "88 specialized agents": `README.md:22`, `:37`, `:60`, `:763`, `:772`. "83 specialized AI agents": `:49` and the tree comment at `:269`. - `ls .hanzo/agents/definitions | grep -v '^README' | wc -l` prints `108`. The role-based table at `README.md:326-366` lists 16 of them, which leaves 92, not 88 or 83. - "42 development tools": `README.md:49`, `:62`, `:278`, `:765`. `ls .hanzo/agents/tools | wc -l` prints `43`. - "15 workflows" is right: `ls .hanzo/agents/workflows | wc -l` prints `15`. - The tree at `README.md:266-281` draws `agents/`, `workflows/` and `tools/` at the root; `ls agents workflows tools` finds none of them. ## What to do Pick one counting rule and write it down in the README (for example: specialized = files in `.hanzo/a

### [Fix README: it documents sqlite APIs that do not exist](https://github.com/hanzoai/sqlite/issues/3)

- Source : GitHub Issues
- Score : 72/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

## Summary The README names four symbols that are not in the package and says the pure-Go build cannot encrypt, while the code and its tests encrypt on every build. Copying the "Encryption" snippet gives a compile error. ## Evidence Checked at `af225db`. - `README.md:73` calls `sqlite.WithPrincipalKey(...)`, `:76` calls `sqlite.DeriveKey(...)`, both with `sqlite.PrincipalOrg`, and `:86` documents `DeriveKey`. `grep -rnw --include=*.go -e WithPrincipalKey -e DeriveKey -e PrincipalOrg .` prints nothing. They lived in `cek.go`, which commit `53fc753` ("The driver opens a file under a key and owns no policy") deleted. - `README.md:22-25` says the pure-Go backend "cannot encrypt" and returns `ErrEncryptionUnavailable`; `:12` lists encryption as "none" for `CGO_ENABLED=0`. `grep -rnw --include=*.go ErrEncryptionUnavailable .` prints nothing. - The package doc in `sqlite.go:1-38` says a keyed store is encrypted on every build, and `CGO_ENABLED=0 go test -count=1 -run TestEncryptionProof ./...

### [Factory replay | Port proven 349 teacher, retention, graduation and dashboard improvements onto current Factory](https://github.com/Entif-AI/Bilqis-MLX/issues/337)

- Source : GitHub Issues
- Score : 72/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

## Durable outcome Selectively replay the proven teacher, retention, scheduler, graduation-sweep and dashboard improvements from branch `349-bouta-tree-fitty` onto the current Factory-v2 stack without merging the divergent branch wholesale and without mutating the frozen #324 qualification specimen. Parents / related authority: - #104 teacher control-loop repair - #321 Teacher vNext portable contract - #324 retained-learning qualification - #320 typed model topology - #333 replayable teacher observations ## Why this is a replay, not a merge `349-bouta-tree-fitty` contains valuable later operator/teacher behavior, but its history diverges from the #290 → #334 → #335 → #336 Factory stack. A direct merge/cherry-pick train can delete or bypass topology, observation, qualification, release-admission, and current Factory owners. Treat 349 as evidence/source material. Port behavior into current owners deliberately. ## Immutable control boundary The active #324 v3 specimen remains frozen: - ex

### [Cross-repo benchmark scorecard & competitive learning ledger [v0.1]](https://github.com/mahmood726-cyber/meta-harness/issues/148)

- Source : GitHub Issues
- Score : 72/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés

**Description :**

# Public cross-repository benchmark oversight / external-learning ledger — v0.1 **Observation date:** 2026-10-24 (Europe/London). **Record type:** evidence-based oversight, **not** completed validation, clinical accuracy, external review, or a comparative performance claim. Maintain one dated entry per distinct external-project practice and an auditable coverage scorecard. The public transport manifest is still a draft PR, not on `main`. ## Frozen benchmark-source snapshot, distinct from moving PR heads From the [draft v0.1 manifest](https://github.com/mahmood726-cyber/meta-harness/blob/30e8803cb00e171e6114308dbf8a542ad7d1e2fd/benchmarks/cross_repo/v0.1/manifest.json): | Repository | Frozen benchmark source commit | Most recent inspected relevant draft head | | --- | --- | --- | | meta-harness | `a62cbc43416a94561b7bee3ec48bb659ac3286e2` | integration [#146](https://github.com/mahmood726-cyber/meta-harness/pull/146): `30e8803cb00e171e6114308dbf8a542ad7d1e2fd`; prospective [#147](https:

### [Customer Support Consultant hospitality](https://remoteOK.com/remote-jobs/remote-customer-support-consultant-hospitality-supportyourapp-1137547)

- Source : Remote OK
- Score : 72/100
- Priorité : HAUTE
- Catégorie : produit_numerique
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : produit_numerique
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés
- État de disponibilité non confirmé

**Description :**

<p>Who are we?</p><p>SupportYourApp is a global Intelligent Support-as-a-Service leader, partnering with tech companies and industry leaders like MasterCard, Calm and MacPaw in 30+ countries since 2010 to deliver secure customer and technical support. We operate globally, supporting clients in 60 languages across diverse industries. So what if you had a chance to be a part of the worldâs leading SaaS, software, or hardware solutions?</p><p>Join our community as a Customer Support Consultant today and thrive in a multicultural and multilingual environment while enjoying your home office. Unlock your potential by mastering new skills and achieving challenging goals in cooperation with our People First management approach. Excited? Letâs see what it takes.</p><p>What you will do:</p><ul><li>Deliver outstanding customer support via phone calls, chats, and emails;</li><li>Build strong and lasting customer relationships;</li><li>Keep up with evolving tools and technology;</li><li>Handle 

### [Associate Data Scientist](https://remoteOK.com/remote-jobs/remote-associate-data-scientist-algaecal-1137531)

- Source : Remote OK
- Score : 72/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés
- État de disponibilité non confirmé

**Description :**

<p></p><p>Description</p><p>Machine Learning Maestro: You donât just work with data - you decode it, predict the future with it, and turn it into action. Your models donât just sit on a shelf - they shape strategy, optimize efficiency, and fuel company growth. You thrive on uncovering hidden patterns, validating hypotheses, and embedding machine learning models into real-world AI applications. If that sounds like you - read on.</p><p>AlgaeCal is looking for a top-tier Associate Data Scientist who can turn raw information into strategies that drive measurable results.</p><p></p><p>This job will give you ALL the feels:</p><p></p><p>At AlgaeCal, weâre driven by a single idea. To end the fear of bone loss. In the United States, an estimated 54 million people have low bone density.</p><p>The good news? AlgaeCal has the worldâs only clinically-backed natural solution to this problem. We give hope to everyone worried about bone loss. If that excites you, youâll find no better place 

### [Project and Quality Administrator Work From Home Dayshift](https://remoteOK.com/remote-jobs/remote-project-and-quality-administrator-work-from-home-dayshift-twoconnect-1137524)

- Source : Remote OK
- Score : 72/100
- Priorité : HAUTE
- Catégorie : tests
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : tests
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés
- État de disponibilité non confirmé

**Description :**

<p>We are seeking a Project and Quality Administrator (Quality Systems) to provide project administration and data coordination support across multiple active projects. The role will maintain accurate project records, coordinate quality documentation, monitor outstanding tasks, prepare reports, and support audit readiness while working closely with internal teams to ensure project information remains complete, accurate, and up to date.</p><p></p><ul><li>Provide project administration and data coordination support across multiple active projects.</li><li>Gather, maintain, and update project information, quality records, and supporting documentation.</li><li>Manage project data and assigned tasks using Deltek, Jira, CRM, and other project management systems.</li><li>Prepare and distribute reports, dashboards, and project performance information using available data.</li><li>Monitor outstanding documentation, actions, deadlines, and quality requirements, proactively following up with stak

### [Manager Clinical Data Management](https://remoteOK.com/remote-jobs/remote-manager-clinical-data-management-edetek-1137481)

- Source : Remote OK
- Score : 72/100
- Priorité : HAUTE
- Catégorie : redaction
- Paiement : RÉMUNÉRATION MENTIONNÉE — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : redaction
- Mention de rémunération détectée
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible

**Vérifications nécessaires :**
- Montant ou modalités de paiement non confirmés
- État de disponibilité non confirmé

**Description :**

<p>Manager, Clinical Data Management leads clinical data management team to handle project management documentation, preform clinical data management activities and system implementations for EDETEKâs CONFORM eClinical, write design specifications for the system (forms, reports, etc.), and facilitate testing of system implementations. In addition to stay hands-on with clinical data management operations and activities, Manager of Clinical Data Management oversees data management projects to ensure quality, timely delivery and ongoing client satisfaction; identifies client needs and develops creative solutions for projects, leveraging expertise, operational capabilities and technologies; communicates with clients and internal teams.</p><p>The Manager, Clinical Data Management should thoroughly understand the requirements for Good Clinical Data Management services, including its documentation; be involved in start-up or wrap-up of in-house and client-specific data management projects; 

### [💰 Bounty Seguro ($$250): [Bounty] Preserve RFC 7239 `Forwarded` host author](https://github.com/alfrexo95/bounty-bot/issues/53)

- Source : GitHub Issues
- Score : 70/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Montant monétaire mentionné
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

🤖 **Bounty con Pago Garantizado (Escrow)** - **Título:** [Bounty] Preserve RFC 7239 `Forwarded` host authority in sub-mounted ASGI `Request.scope_ - **Monto:** $$250 - **Plataforma:** GitHub Issue - **Enlace:** [Ir al Issue](https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/4143) --- ### 💰 Payment Details - BTC: bc1qt3rukpe7qp737zj5j5xpxxmcqv90cfefhg5e00 - ETH: 0xA5E6eB31868A85127B1ED82b8C760193356206ED - LTC: ltc1qdyyg99l8ehp9aj4ehzvmefglmpl9750226k7ne - Lightning: chieftrait089@walletofsatoshi.com **Note:** I am a developer from Cuba. Due to the economic blockade, traditional payment methods are often blocked. Cryptocurrency is the most stable and free way for me to receive payments. I would appreciate it if the bounty could be paid in crypto. Thank you! --- *Este issue fue creado automáticamente por tu bot. Verifica que el escrow esté activo antes de trabajar.*

### [[Bounty] 💰 Bounty Seguro ($$100): [Bounty] USDC-quoted pairs not having the correct](https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/4109)

- Source : GitHub Issues
- Score : 70/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Montant monétaire mentionné
- Publication récente
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement

**Description :**

### 赏金平台 / Platform GitHub ### 原始链接 / Source URL https://github.com/alfrexo95/bounty-bot/issues/21 ### 漏洞描述 / Description 💰 Bounty Seguro ($$100): [Bounty] USDC-quoted pairs not having the correct 🤖 **Bounty con Pago Garantizado (Escrow)** - **Título:** [Bounty] USDC-quoted pairs not having the correct marketcap displayed in tools - **Monto:** $$100 - **Plataforma:** USDC Escrow - **Enlace:** [Ir al Issue](https://github.com/zhangjiayang6835-cyber/bounty-plaza/issues/4107) --- ### 💰 Payment Details - BTC: bc1qt3rukpe7qp737zj5j5xpxxmcqv90cfefhg5e00 - ETH: 0xA5E6eB31868A85127B1ED82b8C760193356206ED - LTC: ltc1qdyyg99l8ehp9aj4ehzvmefglmpl9750226k7ne - Lightning: chieftrait089@walletofsatoshi.com **Note:** I am a developer from Cuba. Due to the economic blockade, traditional payment methods are often blocked. Cryptocurrency is the most stable and free way for me to receive payments. I would appreciate it if the bounty could be paid in crypto. Thank you! --- *Este issue fue creado automátic

### [Solutions Engineer](https://remoteOK.com/remote-jobs/remote-solutions-engineer-onebrief-1137568)

- Source : Remote OK
- Score : 70/100
- Priorité : HAUTE
- Catégorie : autre
- Paiement : MONTANT ANNONCÉ — À VÉRIFIER
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Montant monétaire mentionné
- Livrable ou critères de réalisation mentionnés
- Publication récente
- Lien source disponible

**Vérifications nécessaires :**
- Montant détecté : vérifier la devise, les conditions et la réalité du paiement
- État de disponibilité non confirmé

**Description :**

<h2><em>Consequential Work. Dedicated People.</em></h2><h2><br /><strong>About Onebrief</strong><br /></h2><p style="min-height:1.5em">Onebrief builds collaboration and AI-powered workflow software for military planning and operational coordination.</p><p style="min-height:1.5em">Military planning is complex by nature, requiring teams to coordinate information, people, and decisions across systems and locations. Onebrief brings planning, collaboration, simulation, and AI into one connected environment, helping teams test strategies, adapt to changing conditions, and make decisions with greater clarity when the stakes are real.</p><p style="min-height:1.5em">We are a distributed team of builders from military, operational, and technology backgrounds who care deeply about improving how important work gets done. Some team members work remotely, while others work directly alongside customers in operational environments around the world.</p><p style="min-height:1.5em">Founded in 2019, Onebr

### [MASTER | LiOS complete product — 206 SI workstreams, Gen AI, Finance, donors, shipping and P14](https://github.com/kiranvbiim-coder/lios-terminal/issues/91)

- Source : GitHub Issues
- Score : 70/100
- Priorité : HAUTE
- Catégorie : programmation
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : programmation
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

<!-- LIOS_MASTER_20261021 --> # MASTER PRODUCT CLOSURE — Current one-issue execution register (2026-10-21) > **Owner directive:** NO further disconnected planning cycles. Close the entire *approved* LiOS goal: Gen AI, Finance, professional terminal, research, agents, tools, donors, Home/devices, automation, trust and actual native release. **This issue #91 is the ONE product-level issue**; existing independent #16/#3/#5, PRs and their original owners remain linked here, not deleted or duplicated. > > **Evidence boundary:** protected main `1fa37cc372746b7bfd61c4f8b79093ed707c5ea0`, hosted macOS/Linux/Windows source CI **PASS**. Signed clean macOS+Windows, real authorized model and entitled financial data, complete product journey, SP01–SP07 and P14 **NOT ACCEPTED**. No speculative completion rate. This top section supersedes *dated assertions* in the preserved historical #91 body below; compare changes at exact main. **Canonical authority:** [SI-01–SI-07](https://github.com/kiranvbiim-c

### [Tracking: high-throughput Rust ingestion with a three-replica WAL](https://github.com/lance-format/lance-context/issues/378)

- Source : GitHub Issues
- Score : 70/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

## Problem Object-store WAL writes can put remote request latency and small-object overhead on the ingestion ACK path. A memory-only WAL removes that cost but cannot preserve acknowledged writes across process or node loss. We want an optional, high-throughput durable ingestion path implemented in Rust within lance-context, with minimal changes to Lance OSS. This issue tracks incremental implementation and validation. The foundational PRs below do not yet enable a distributed writer in production or replace the existing ingestion path. ## Proposed architecture ```mermaid flowchart LR I["Ingress: encode Arrow once"] --> R["Session key to virtual bucket"] R --> L subgraph G["One replication group: three durable replicas"] L["Leader + persistent WAL"] F1["Follower + persistent WAL"] F2["Follower + persistent WAL"] L --> F1 L --> F2 end L -. "ACK after durable quorum commit" .-> I L -->|Committed records| P["Fenced Lance publisher"] P --> B["Blob: Lance data files + manifest"] B --> V["Vis

### [Agent coordination requests and worker status](https://github.com/Ken0u/badminton-match-analyzer/issues/74)

- Source : GitHub Issues
- Score : 70/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

Durable automation commands live here. See docs/COLLABORATION.md. Observation mode does not grant execution. Never paste credentials or private datasets. <!-- agent-dashboard:v1 --> ## Shared agent dashboard Mode: **active**. Claims paused: **False**. | Task | Status | Owner / host | Lease (UTC) | Blocker / delivery | | --- | --- | --- | --- | --- | | #342 | needs_human | — / — | — | | | #332 | blocked | — / — | — | Issue closed by collaborator; re-plan explicitly after reopening | | #329 | verifying_main | Ken0u / MSI | 2026-10-28T08:22:52+00:00 | | | #323 | blocked | — / — | — | Issue closed by collaborator; re-plan explicitly after reopening | | #321 | blocked | — / — | — | Issue closed by collaborator; re-plan explicitly after reopening | | #279 | needs_human | — / — | — | | | #240 | blocked | — / — | — | Issue closed by collaborator; re-plan explicitly after reopening | | #195 | blocked | — / — | — | Issue closed by collaborator; re-plan explicitly after reopening | | #164 | block

### [Master roadmap: coordinate ReefVision 1.0–2.0 across five hourly development tracks](https://github.com/Rafael-Del-Valle/ReefVision/issues/76)

- Source : GitHub Issues
- Score : 70/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

# ReefVision 1.0–2.0 consolidated development coordination **Scope:** consolidate the existing five hourly development automations into five distinct workstreams covering ReefVision **1.0.x through 2.0**. Do **not** start cloud accounts/shared Internet collaboration/managed cloud hosting here; those belong to **2.1** in issue #75. ## Development ownership and branch isolation | Lane | Version range | Existing work to preserve | Key focus | | --- | --- | --- | --- | | A — Release foundation | 1.0.x–1.1 | 1.0.3 draft PR #73; 1.1 draft PR #71 | Fix 1.0.3 viewer and JPG/JPEG imports, external read-only PowerShell live training console, release gates; finish 1.1 environmental/scientific context, currents, heatmaps, computed metrics, event/environment linkage, Workflow Builder integration | | B — Ecological longitudinal science | 1.2–1.3 | 1.2 draft PR #74; isolated 1.3 development branch/PR if found | Organism identity, longitudinal coral growth and abundance, population analyses, human/mod

### [Owner directive: Aria Mission Control — Work coordinator ownership and acceptance gaps](https://github.com/caosos/Desktop-Agent/issues/3)

- Source : GitHub Issues
- Score : 70/100
- Priorité : HAUTE
- Catégorie : donnees
- Paiement : AUCUNE PREUVE DE PAIEMENT DÉTECTÉE
- Éligibilité : À vérifier pour Madagascar
- Automatisation : À vérifier selon les règles de la plateforme
- Statut : NON VÉRIFIÉ

**Points positifs :**
- Description d'une tâche potentiellement concrète
- Catégorie identifiée : donnees
- Livrable ou critères de réalisation mentionnés
- Publication datant de moins d'un mois
- Lien source disponible
- Opportunité signalée comme ouverte

**Vérifications nécessaires :**
- Aucune rémunération claire détectée

**Description :**

# Owner directive — 2026-10-08 **Source:** Michael's instruction in ChatGPT, titled "MICHAEL'S DESKTOP AGENT — OWNER EXPECTATIONS & OPERATING DIRECTIVE". This issue captures requirements for the **sole active ChatGPT Work development coordinator** to integrate into the canonical append-only `docs/OWNER_DIRECTIVES.md`. The issue is an intake/receipt, **not a second implementation authority**. PR #2 (`build/stage-1`) is active; do not race it or alter other projects. **Owner command:** **"BUILD. Keep busy until I'm needed."** ## Owner's binding expectations 1. **Persistent Linux desktop assistant / AI operating system.** A small Aria widget with natural voice and text: "Build this", "Fix this problem", "Show me what my agents are working on", "Finish this project", "Find out what's blocking progress", "Handle this and let me know when you actually need me." The widget is the interface; governed tools and the control plane execute work. No terminal babysitting. 2. **One mission control fo

## Produits numériques à développer

- **ebook :** Guide pratique pour débuter en programmation — IDÉE À DÉVELOPPER
- **ebook :** Guide pratique des outils numériques gratuits — IDÉE À DÉVELOPPER
- **template :** Modèle de suivi de budget personnel — IDÉE À DÉVELOPPER
- **script :** Script Python de classement automatique de fichiers — IDÉE À DÉVELOPPER
- **video :** Mini-cours sur un outil numérique gratuit — IDÉE À DÉVELOPPER
- **audio :** Guide audio d'initiation à la technologie — IDÉE À DÉVELOPPER