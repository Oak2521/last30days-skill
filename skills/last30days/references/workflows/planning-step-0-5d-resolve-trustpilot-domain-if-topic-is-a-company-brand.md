### Step 0.5d: Resolve Trustpilot Domain (if topic is a company/brand)

When TOPIC is a company, brand, or service and you want Trustpilot review evidence, resolve its Trustpilot review-page domain. Trustpilot pages are keyed by domain (`www.thriftbooks.com`), not company name — a bare name 404s. Passing `--trustpilot-domain` (or a per-entity `trustpilot_domain` in `--competitors-plan`) auto-activates the opt-in Trustpilot source for that run — you do not also need `INCLUDE_SOURCES=trustpilot`.

**You usually already have it.** Step 0.55 item 6 (first-party positioning) fetches the official site — capture the bare hostname while you're there. When positioning wasn't fetched, one lookup covers it:

```
WebSearch("{TOPIC} official site")
```

Pass to the CLI: `--trustpilot-domain={domain}` (e.g., `--trustpilot-domain=www.thriftbooks.com`)

The flag is used verbatim, bypasses the engine's brand-shape gate, and auto-activates Trustpilot for the run, so it also unlocks Trustpilot for multi-word company names ("Stanley Steemer carpet cleaning"). For comparisons, put a per-entity `trustpilot_domain` in each PEER entity's `--competitors-plan` entry; the MAIN topic's domain must ride the outer `--trustpilot-domain` flag (the engine does not read a main-topic entry out of the plan).

**A miss is not fatal.** When the flag is absent, the engine resolves name → domain itself via the CLI's search **only when Trustpilot is already active** (`INCLUDE_SOURCES=trustpilot` or `--search` includes it); headless `--auto-resolve` fills a hint the engine verifies, but that hint alone does not activate the source. Resolve the flag when the domain is already in hand or the company name is ambiguous (lookalike or same-named companies) — an explicit domain is the only way to guarantee the right company *and* turn the source on.

**Skip this step if:**
- TOPIC is a person, event, or abstract concept (no company reviews to fetch)
- You intentionally want Trustpilot off for this run (`EXCLUDE_SOURCES=trustpilot`)

Store: `RESOLVED_TRUSTPILOT_DOMAIN = {domain or empty}`

---
