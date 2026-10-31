#!/usr/bin/env python3
"""Build + upload manifest-org.json — the empire's officer roster, businesses,
agencies, departments, council, sentinel standards, and autonomy tiers.
Canonical source of truth for the org. Portal serves it at /api/org."""
import json, sys
sys.path.insert(0, '/opt/data/portal-deploy')
from storj_curl import s3_put

ORG = {
  "updated": "2026-10-26T00:00:00Z",
  "edict": {
    "who": "We are Warrior World — proof that sovereignty is possible: Web3-native, zero-subscription, open-source everything. An empire built by AI, owned by Prince.",
    "why": "Capacity, not cure. Prove it. Pass it on. We build money machines that fund warriors with invisible disabilities: jobs, re-education, mastery of AI. First we prove it HERE, then we pass it on to the world.",
    "how": "1 + 1 = 11 — we work as one. Every agent holds this edict, works ONE lane, speaks nothing outside it. Every output ships with proof; SENTINEL audits all."
  },
  "tiers": {
    "A": {"label": "Auto", "rule": "Repeatable, low-consequence: full auto. Sentinel stamps, ships, receipt always."},
    "B": {"label": "Hold for Prince", "rule": "Irreversible (money out, publishing, contracts, commitments, grant submissions): worker finishes -> Sentinel audits -> card lands on the Needs-Prince shelf -> one tap = go."}
  },
  "standing_rule": {
    "name": "ONE LANE. PROOF OR IT DIDN'T HAPPEN. LATEST INSTRUCTION WINS.",
    "one_lane": "Every agent works ONE lane and speaks nothing outside it. Workers talk only inside their own project; divisions never chat across lanes. Confinement is doctrine.",
    "proof": "Every output ships as {what, url_or_file, proof, cost, audited_by}. No receipt = not done.",
    "latest_wins": "When Prince gives a new instruction it overrides every older one, no exceptions.",
    "tiers": "Tier A (auto): repeatable, low-consequence — ships itself, receipt always. Tier B (hold for Prince): anything irreversible lands on the Needs-Prince shelf and waits for one tap."
  },
  "territory": {
    "rule_of_thumb": "WEAVER builds it. ARCHITECT owns the platform it sits on. BEACON keeps the rails on underneath. Everything else is a business that orders from them.",
    "beacon": "THE RAILS — TechOps (CTO). All 15 domains, DNS, Cloudflare, Storj, Akash leases, infra ledger, cost watch. If it is a wire, a door, or a bill — Beacon.",
    "weaver": "THE BUILDERS — Web Agency. Builds every website for every business: marketing pages, landing pages, portals, shops, tenant sites. If it renders in a browser and a business ordered it — Weaver built it.",
    "architect": "THE PLATFORM — Warrior Web + Bo$$Box. Owns the Web3 hosting platform sites live on, the Bo$$Box SaaS product line, tenant onboarding, crypto billing. If a tenant rents space or buys a Bo$$Box — Architect."
  },
  "escalation": "Any worker fails the same task 2x -> auto-elevated to Jarvis -> 'Needs decision' chip on the floor.",
  "receipt_standard": "Every deliverable ships as {what, url_or_file, proof, cost, audited_by}. No receipt = not done.",
  "sentinel": {
    "officer": "SENTINEL",
    "role": "Audit & Quality. Nothing ships without his stamp. He audits the auditors: catch-rate + escalation-rate reported every Sunday.",
    "matrix": {
      "web":   ["brand voice ok", "no unverified claims", "links verified live", "mobile check", "a11y basics"],
      "video": ["clinical not hype", "no unverified claims", "captions", "brand open/close", "license-clean assets"],
      "email": ["PARTNERS not sponsors", "personalized line", "Sage/pipeline routing", "no spam pattern"],
      "legal": ["entity correct", "deadlines filed", "privacy terms present", "grant eligibility clean"],
      "books": ["receipt attached", "GST/PST set-aside right", "ledger matches cash", "CRA-ready summary"]
    }
  },
  "council": {
    "culture": "Rigorous and loving — one family, one machine. We do not scrap; we align. Mandatory dissent, kind dissent: every seat speaks the positives AND the negatives, every i dotted, every t crossed, stars aligned. 1 + 1 = 11.",
    "convene": "Call a meeting anytime; the room stays off to the side, never in Jarvis's daily pipeline. Output: one verdict + noted dissent + go/refine/kill for Prince's stamp.",
    "primes": [
      {"seat": 1, "id": "chairman", "name": "Chairman & CEO — Koya", "angel": "The Vision", "power": "The whole machine; final word on everything; owns the why", "lane": "executive, veto, mission", "powers": ["Veto & final judgment — every verdict ends with his word", "Edict keeper — who/what/why enforced in every agent", "The unifying self — 1 + 1 = 11 cohesion"]},
      {"seat": 2, "id": "coo", "name": "Chief Operating Officer", "angel": "The Engine", "power": "Operations truth — knows every flow end to end", "lane": "operations, execution, escalation", "powers": ["End-to-end flow ownership", "Escalation — failures route here, never stall", "Execution standard — receipts or death"]},
      {"seat": 3, "id": "cfo", "name": "Chief Financial Officer", "angel": "The Ledger", "power": "Capital, treasury, the $1M math — signs every bill", "lane": "finance, treasury, tokenomics WOW/WILD/BETX", "powers": ["Cash truth — ledger, costs, projected runs", "Token & treasury fluency — WOW/WILD/BETX economics", "Cost governor — knows every nickel", "Grant & revenue financing — what funds the mission"]},
      {"seat": 4, "id": "cto", "name": "Chief Technology Officer", "angel": "The Architect", "power": "All systems — Web3 infra, doors, leases; technical sign-off", "lane": "technology, infrastructure, sovereign stack", "powers": ["Stack governor — bans anything off our Web3 rail", "Build-first — ships working systems", "Resilience — designs failure modes out", "Every deployment verified live"]},
      {"seat": 5, "id": "clo", "name": "Chief Legal Officer & General Counsel", "angel": "The Shield", "power": "Entity structure, contracts, HIPAA/GDPR, filings calendar", "lane": "legal, compliance, governance", "powers": ["Entity + governance structure", "Contracts & terms — every agreement reviewed", "Compliance calendar — filings filed, deadlines met", "Risk posture — securities/regulatory lines defended"]},
      {"seat": 6, "id": "cmo", "name": "Chief Marketing Officer", "angel": "The Voice", "power": "Brand, go-to-market, positioning, inbound", "lane": "marketing, growth, brand", "powers": ["Positioning — slots every idea into the map", "Brand everywhere — clinical precision + warrior fire", "Launch sequencing — what moves when", "Inbound engine — partners & community"]},
      {"seat": 7, "id": "cro", "name": "Chief Revenue Officer", "angel": "The Machine", "power": "Money machines, sponsors, partners, monetization rail", "lane": "revenue, partnerships, sponsors, monetization", "powers": ["Money-machine portfolio — what prints next", "Sponsor & partner engine — PARTNERS not sponsors", "Monetization rail — every asset earns", "Revenue receipts — proof on every dollar"]},
      {"seat": 8, "id": "ciso", "name": "Chief Information Security Officer", "angel": "The Gate", "power": "Threat models every plan; guards assets, data, infra", "lane": "security, audit, resilience, threat", "powers": ["Threat modeling — attacks designed out", "Access & asset protection — credentials, buckets, keys", "SENTINEL audit — nothing ships unstamped", "Containment doctrine — divisions never talk outside their lane"]},
      {"seat": 9, "id": "cpo", "name": "Chief People & Community Officer", "angel": "The Heart", "power": "Warriors, partners, re-education mission, the tribe", "lane": "people, community, mission, re-education", "powers": ["Mission north — warriors first, always", "People lens — who benefits, who gets hurt", "Community & partner glue — the tribe", "Re-education flow — jobs + mastery for invisible disabilities"]},
      {"seat": 10, "id": "cco", "name": "Chief Creative Officer", "angel": "The Muse", "power": "All creative output, content, shows, the story", "lane": "media, creative, shows, PEMF TV", "powers": ["Story alchemy — data into story that moves", "Showroom sense — catalog & series instincts", "Content standards — every publish branded + clean"]},
      {"seat": 11, "id": "cso", "name": "Chief Strategy Officer", "angel": "The Horizon", "power": "Research, intel, competitive landscape, the long game", "lane": "strategy, research, intel, foresight", "powers": ["Deep research — unknown into mastered", "INTEL — rivals, markets, ecosystem radar", "Game-theory posture — opening & defense", "Moonshot filter — bold but survivable"]}
    ]
  },
  "board": [
    {"seat": 1, "title": "Chief Executive Officer", "duty": "Sees the whole machine; final numbers owner; weekly empire review"},
    {"seat": 2, "title": "Chief Operating Officer", "duty": "Operations truth — knows every flow end to end; escalation owner"},
    {"seat": 3, "title": "Chief Financial Officer", "home": "MINT", "duty": "Numbers corrected — ledger, costs, cash truth; signs every internal bill"},
    {"seat": 4, "title": "Chief Technology Officer", "home": "BEACON", "duty": "Knows every system state — doors, leases, services; technical sign-off"},
    {"seat": 5, "title": "Chief Legal Officer & General Counsel", "home": "COUNSEL", "duty": "Entity, contracts, HIPAA/GDPR, filings"},
    {"seat": 6, "title": "Chief Marketing Officer", "home": "WEAVER + HERALD", "duty": "Brand, growth, positioning, inbound"},
    {"seat": 7, "title": "Chief Revenue Officer", "home": "VANGUARD + CRO", "duty": "Money machines, sponsors, partners, monetization"},
    {"seat": 8, "title": "Chief Information Security Officer", "home": "BEACON + SENTINEL", "duty": "Threat, access, audit, containment doctrine"},
    {"seat": 9, "title": "Chief People & Community Officer", "home": "GUARDIAN", "duty": "Warriors, partners, re-education, the tribe"},
    {"seat": 10, "title": "Chief Creative Officer", "home": "SHOWRUNNER + FORGE", "duty": "All creative; content, shows, story, standards"},
    {"seat": 11, "title": "Chief Strategy Officer", "home": "CEO + CSO", "duty": "Research, intel, competitive, long game"}
  ],
  "mma": {
    "name": "Mariam",
    "role": "MMA — Money-Making-Activity Manager. A her. Every approved $1M-grade plan is commissioned to a Mariam: she holds the Wisdom Council plan VERBATIM as standing orders, sizes her own clan (+10/+30/+60 — whatever the plan needs), hires the best for each lane, wakes workers only when their lane is open.",
    "clan": "The workers below Mariam — one lane each, sleepers at $0, wake → work → exit. They talk about NOTHING outside that lane. Divisions don't talk to each other. Confinement is doctrine."
  },
  "jarvis": {"officer": "JARVIS", "role": "COO & orchestrator. Your one voice, 24/7. Takes the Wisdom Council's $1M-grade plan, routes it down the Board line to a Mariam (MMA), and reports. Knows you: memory + 5,704 sessions + Warrior Doctrine + the Edict."},
  "businesses": [
    {"id": "vanguard", "name": "PEMF Warrior", "icon": "🎬", "type": "business", "manager": "VANGUARD", "mission": "Brand, documentary, sponsorships, memberships", "orders": ["Sponsor Engine", "Content Factory", "Shop Ops"], "officers": ["VANGUARD", "sponsor-hunter", "content-writer", "youtube-publisher", "shop-agent"]},
    {"id": "guardian", "name": "Warrior World", "icon": "🏛️", "type": "business", "manager": "GUARDIAN", "mission": "Nonprofit, grants (12-track), athlete funding, EAF Warrior House", "orders": ["Grant Engine", "community-liaison", "grant-finance"], "officers": ["GUARDIAN", "grant-researcher", "community-liaison", "grant-finance"]},
    {"id": "showrunner", "name": "PEMF TV", "icon": "📺", "type": "business", "manager": "SHOWRUNNER", "mission": "The network. S2 The Brain (concussion). Launch 2027.", "orders": ["Content Factory (TV)", "practitioner pages"], "officers": ["SHOWRUNNER", "producer", "editor", "tv-seo"]},
    {"id": "architect", "name": "Warrior Web + Bo$$Box", "icon": "🌐", "type": "business", "manager": "ARCHITECT", "mission": "Web3 hosting platform + SaaS product line for tenants", "orders": ["tenant builds", "hosting ops", "Bo$$Box product", "Bo$$Box clone-install", "tenant onboarding", "crypto billing"], "officers": ["ARCHITECT", "site-builder", "deploy-engineer", "product-worker"]},
    {"id": "merchant", "name": "Shop & Commerce", "icon": "🛍️", "type": "business", "manager": "MERCHANT", "mission": "pemfwarrior.shop — payments, fulfillment, cutover (Alavan/Elavon/ShipStation/Lee 46)", "orders": ["Shop Ops", "cutover runbook"], "officers": ["MERCHANT", "orders-worker", "payments-tester"]},
    {"id": "sovereign-web3", "name": "Sovereign Web3", "icon": "🪙", "type": "business", "tier": "B", "manager": "CHANCELLOR", "mission": "Sovereign Web3 assets: coin/token/TLD/DeFi money machines, on-chain transparency", "orders": ["on-chain transparency ledger", "tokenomics WOW + WILD coin", ".warriorweb Web3 TLD registry", "DeFi money machines", "sentinel on-chain audit row"], "officers": ["CHANCELLOR", "token-engineer", "chain-deployer", "tld-registrar", "liquidity-ops", "compliance-officer"]},
    {"id": "aibetbook", "name": "AIBETBOOK", "icon": "📈", "type": "business", "tier": "B", "manager": "BOOKMAKER", "mission": "aibetbook.com — crypto-only betting node: stake BETX, 110-550% APY, 4PM UTC payouts", "orders": ["keep aibetbook.com live", "migrate Supabase to Cloudflare D1", "wire crypto-only USDT/USDC via Solana escrow", "node model (stake BETX 110-550% APY, 4PM UTC payouts, under 2% spread)", "kill MetaX references", "1% revenue to Passive Pulse", "3 external keys needed (The Odds API + Betty/OpenAI + Solana RPC)"], "officers": ["BOOKMAKER", "platform-engineer", "odds-integration", "escrow-contract", "compliance"]}
  ],
  "agencies": [
    {"id": "forge", "name": "Production House", "icon": "🎥", "type": "agency", "manager": "FORGE", "mission": "ALL video: clips, promo, movies, TV, AI clones (GPT-SoVITS + MuseTalk)", "orders": ["Clone Stack", "video products"], "officers": ["FORGE", "script-writer", "voice-trainer", "avatar-producer", "editor", "publisher"]},
    {"id": "weaver", "name": "Web Agency", "icon": "🕸️", "type": "agency", "manager": "WEAVER", "mission": "ALL websites: marketing, landing pages, portals, shops, tenants", "orders": ["SEO Ecosystem", "site builds"], "officers": ["WEAVER", "frontend-builder", "web-deploy", "web-copywriter", "seo-worker"]},
    {"id": "counsel", "name": "Legal & Compliance", "icon": "⚖️", "type": "agency", "manager": "COUNSEL", "mission": "Entity structure, contracts, grants compliance, HIPAA/GDPR, IP, compliance calendar", "orders": ["compliance calendar", "contracts"], "officers": ["COUNSEL", "contract-drafter", "compliance-auditor", "entity-researcher"]},
    {"id": "herald", "name": "Communications & PR + Mailroom", "icon": "📣", "type": "agency", "manager": "HERALD", "mission": "One voice, one inbox router: sponsor->VANGUARD, order->MERCHANT, press->HERALD, grant->GUARDIAN, personal->CHAMBERLAIN", "orders": ["mailroom triage", "brand consistency"], "officers": ["HERALD", "brand-copywriter", "press-minder", "mailroom-triage"]}
  ],
  "departments": [
    {"id": "beacon", "name": "TechOps (CTO)", "icon": "⚙️", "type": "department", "manager": "BEACON", "mission": "All domains (15 doors), DNS, Cloudflare, Storj, Akash leases, infra ledger, cost watch", "orders": ["door sweep", "lease watch", "infra report"], "officers": ["BEACON", "domain-keeper", "dns-sweeper", "infra-watch"]},
    {"id": "mint", "name": "Treasury & Accounting", "icon": "💰", "type": "department", "manager": "MINT", "mission": "Bookkeeping, GST/PST (BC 7% + 5%), CRA-ready books, grant finance, cost governor", "orders": ["monthly close", "GST/PST calendar"], "officers": ["MINT", "bookkeeper", "gst-pst-worker", "cost-governor"]},
    {"id": "chamberlain", "name": "Personal Aide", "icon": "👤", "type": "department", "manager": "CHAMBERLAIN", "mission": "Your day: schedule, appointments, health protocol (PEMF daily, energy/pain/sleep), family dates, reminders", "orders": ["daily standup", "health watch"], "officers": ["CHAMBERLAIN", "day-planner", "health-watch"]}
  ],
  "workers": {
    "sponsor-hunter": "Warm outreach pipeline: BC gyms, disability orgs, clinics, mayors, sports brands. PARTNERS not sponsors.",
    "content-writer": "PEMF Warrior copy: emotion -> data -> sale. 'Clinical Precision + Warrior Fire'.",
    "youtube-publisher": "Channel ops: titles '[PEMF Protocol/Testimonial: Session]', arc emotion->data->CTA.",
    "shop-agent": "Rocks the shop storefront + membership, order triage.",
    "grant-researcher": "12-track grant engine: BC Gaming $20K-$250K + 11 more. Verify eligibility before filing.",
    "community-liaison": "EAF Warrior House + athlete/community relationships.",
    "grant-finance": "Expense tagging per grant. CRA audit-ready.",
    "producer": "Show packages: S2 The Brain 'Knowledge is Power'. Cast deep pages.",
    "editor": "Cuts under FORGE; receipts: file URL + still + duration.",
    "tv-seo": "PEMF TV catalog-first SEO; practitioner origin pages.",
    "site-builder": "React/Vite/Tailwind builds, Storj+CF deploys.",
    "deploy-engineer": "Cloudflare Pages/Workers, DNS, verify 200s after every deploy.",
    "product-worker": "Bo$$Box Web3 SaaS shop clones for tenants.",
    "orders-worker": "Orders, fulfillment, ShipStation XML bridge.",
    "payments-tester": "Alavan/Elavon sandbox + Lee 46 routes: test before every cutover.",
    "script-writer": "Trailers, promo, testimonials. Emotion -> data -> ask.",
    "voice-trainer": "GPT-SoVITS voice training from Prince memos.",
    "avatar-producer": "MuseTalk avatar vids into pemf-ai-generated.",
    "publisher": "Publishes rendered media; receipts: video URL + analytics snapshot.",
    "frontend-builder": "Same stack as site-builder; works FOR any business via WEAVER.",
    "web-deploy": "Deploy + verify (curl 200 / browser pass).",
    "web-copywriter": "Landing copy: invisible-disability-first framing.",
    "seo-worker": "17-site ecosystem: GSC, schema, authority mesh.",
    "contract-drafter": "Contracts + terms. Family/partners clarity.",
    "compliance-auditor": "HIPAA/GDPR/privacy hygiene + entity filings calendar.",
    "entity-researcher": "Co-op <-> society structures for grants.",
    "brand-copywriter": "One voice everywhere: clinical precision + warrior fire.",
    "press-minder": "Press statements, media Qs.",
    "mailroom-triage": "4+ inboxes -> route tag -> correct officer. Auto-reply only where safe.",
    "domain-keeper": "15 doors: registrar, NS, expiry, renewals 20d out.",
    "dns-sweeper": "CF zones + records; worker-edit rule: fetch deployed source first.",
    "infra-watch": "Akash leases ($5.04/mo floor), brain+BOOM heartbeat, GPU sleep-lock.",
    "bookkeeper": "Every expense journaled; receipts attached; monthly close.",
    "gst-pst-worker": "BC PST 7% + GST 5% calendar; CRA summaries.",
    "cost-governor": "Weekly spend > threshold or lease <20d -> alert card.",
    "day-planner": "Your calendar, appointments, commitments.",
    "health-watch": "Daily PEMF check-in (energy/pain/sleep), protocol runs, streak.",
    "token-engineer": "WOW + WILD coin tokenomics: mint/burn, supply cap, on-chain ledger rows.",
    "chain-deployer": "Solana + chain deploys: escrow contracts, RPC wiring, verify txns live.",
    "tld-registrar": ".warriorweb Web3 TLD registry: resolvers, renewals, zone health.",
    "liquidity-ops": "DeFi money machines: pools, LP positions, yield + cost watch.",
    "compliance-officer": "Crypto/TLD compliance posture: registrar rules, securities/lottery lines, audit rows.",
    "platform-engineer": "aibetbook.com stays live: guest mode, Cloudflare D1 migration, uptime.",
    "odds-integration": "The Odds API + Betty/OpenAI feeds; spread under 2%; odds math receipts.",
    "escrow-contract": "Solana escrow: USDT/USDC custody, settlement, 4PM UTC payouts.",
    "compliance": "AIBETBOOK compliance: crypto-only rails, AML/terms, kill MetaX mentions."
  }
}

# Plain-language one-liners per manager — Prince's readable view of who runs what
PLAIN = {
  "VANGUARD": "PEMF Warrior — the flagship. Brand, documentary, sponsorships, memberships. Orders: Sponsor Engine, Content Factory, Shop Ops.",
  "GUARDIAN": "Warrior World nonprofit — grants (12-track), athlete funding, EAF Warrior House.",
  "SHOWRUNNER": "PEMF TV — the network. Season 2 'The Brain' (concussion). Launches 2027.",
  "ARCHITECT": "Warrior Web + Bo$$Box — the PLATFORM: Web3 hosting + SaaS products tenants buy; runs tenant onboarding and crypto billing.",
  "MERCHANT": "Shop & Commerce — pemfwarrior.shop: payments, fulfillment, cutover.",
  "CHANCELLOR": "Sovereign Web3 — coin/token/TLD/DeFi money machines, on-chain transparency.",
  "BOOKMAKER": "AIBETBOOK — crypto-only betting node: stake BETX, 110-550% APY, 4PM UTC payouts.",
  "FORGE": "Production House — ALL video: clips, promos, movies, TV, AI clones.",
  "WEAVER": "Web Agency — THE BUILDERS: every website for every business (marketing, landing pages, portals, shops, tenants).",
  "COUNSEL": "Legal & Compliance — entity structure, contracts, HIPAA/GDPR, IP, filings calendar.",
  "HERALD": "Communications & PR + Mailroom — one voice, one inbox router.",
  "BEACON": "TechOps (CTO) — THE RAILS: 15 domains, DNS, Cloudflare, Storj, Akash leases, infra ledger, cost watch.",
  "MINT": "Treasury & Accounting — books, GST/PST (BC 7% + 5%), CRA-ready, grant finance.",
  "CHAMBERLAIN": "Personal Aide — your day: schedule, PEMF protocol, family dates, reminders."
}
for _group in ("businesses", "agencies", "departments"):
    for _e in ORG[_group]:
        _p = PLAIN.get(_e["manager"])
        if _p:
            _e["plain"] = _p

j = json.dumps(ORG, indent=1)
p = '/tmp/manifest-org.json'
open(p, 'w').write(j)
print(f"org bytes: {len(j)}")
try:
    s3_put('warrior-command', 'portal/manifest-org.json', p, 'application/json')
    print("upload: OK")
except Exception as e:
    print("upload FAIL:", str(e)[:200])