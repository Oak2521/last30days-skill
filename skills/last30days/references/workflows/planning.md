> Read only for the matching mode. Resolve script paths relative to the parent SKILL.md. User/host requirements govern citations, output and footer. Preserve required source links and do not replace them with hidden archives.

## CRITICAL: Parse User Intent

Before doing anything, parse the user's input for:

1. **TOPIC**: What they want to learn about (e.g., "web app mockups", "Claude Code skills", "image generation")
2. **TARGET TOOL** (if specified): Where they'll use the prompts (e.g., "Nano Banana Pro", "ChatGPT", "Midjourney")
3. **QUERY TYPE**: What kind of research they want:
   - **PROMPTING** - "X prompts", "prompting for X", "X best practices" → User wants to learn techniques and get copy-paste prompts
   - **RECOMMENDATIONS** - "best X", "top X", "what X should I use", "recommended X" → User wants a LIST of specific things
   - **NEWS** - "what's happening with X", "X news", "latest on X" → User wants current events/updates
   - **COMPARISON** - "X vs Y", "X versus Y", "compare X and Y", "X or Y which is better" → User wants a side-by-side comparison
   - **GENERAL** - anything else → User wants broad understanding of the topic

Common patterns:
- `[topic] for [tool]` → "web mockups for Nano Banana Pro" → TOOL IS SPECIFIED
- `[topic] prompts for [tool]` → "UI design prompts for Midjourney" → TOOL IS SPECIFIED
- Just `[topic]` → "iOS design mockups" → TOOL NOT SPECIFIED, that's OK
- "best [topic]" or "top [topic]" → QUERY_TYPE = RECOMMENDATIONS
- "what are the best [topic]" → QUERY_TYPE = RECOMMENDATIONS
- "X vs Y" or "X versus Y" → QUERY_TYPE = COMPARISON, TOPIC_A = X, TOPIC_B = Y (split on ` vs ` or ` versus ` with spaces)

**IMPORTANT: Do NOT ask about target tool before research.**
- If tool is specified in the query, use it
- If tool is NOT specified, run research first, then ask AFTER showing results

**Store these variables:**
- `TOPIC = [extracted topic]`
- `TARGET_TOOL = [extracted tool, or "unknown" if not specified]`
- `QUERY_TYPE = [RECOMMENDATIONS | NEWS | HOW-TO | COMPARISON | GENERAL]`
- `REGISTER = [default | exec | dev | creator | eli5]` from an explicit `--register` argument, otherwise `LAST30DAYS_REGISTER`, otherwise `default`. A legacy `ELI5_MODE=true` config means `eli5` when no register was selected. Register words are controls, not part of TOPIC.
- `TOPIC_A = [first item]` (only if COMPARISON)
- `TOPIC_B = [second item]` (only if COMPARISON)

**Confirm the topic with a branded, truthful message. Build ACTIVE_SOURCES_LIST from the engine's own source diagnostic — do NOT infer availability by checking env vars or `.env`.** The engine resolves credentials at runtime from several places (process environment, `.env`, macOS Keychain, etc.), so a config-file check silently under-reports sources whenever a key is resolved at runtime rather than written literally in `.env`. Run the engine's `--diagnose` and read its result:

```bash
SKILL_DIR="<absolute path of the directory containing the SKILL.md you just Read>"
"${LAST30DAYS_PYTHON}" "${SKILL_DIR}/scripts/last30days.py" --diagnose
```

`--diagnose` prints JSON. `ACTIVE_SOURCES_LIST` is its `available_sources` array — the engine's authoritative source set, computed after credential resolution. Map the tokens to display names: `reddit`→Reddit, `hackernews`→Hacker News, `polymarket`→Polymarket, `github`→GitHub, `digg`→Digg, `x`→X, `youtube`→YouTube, `tiktok`→TikTok, `instagram`→Instagram, `threads`→Threads, `pinterest`→Pinterest, `linkedin`→LinkedIn, `bluesky`→Bluesky, `perplexity`→Perplexity, `grounding`→Web, `jobs`→Jobs, `corpus`→Your files, `dripstack`→DripStack.

- If EXCLUDE_SOURCES is set (comma-separated, case-insensitive): drop any matching source from ACTIVE_SOURCES_LIST before displaying

**Local corpus source:** If the user asks to include their own notes/documents, preserve each supplied directory as a repeatable `--corpus <dir>` engine flag. `LAST30DAYS_CORPUS_DIRS` activates persistent registered directories automatically. Do not WebSearch, upload, quote into a hosted request, or otherwise expose those paths or contents. Corpus retrieval is an offline source lane; its candidates also bypass remote reranker/fun-scoring prompts and use deterministic local scoring. The engine renders matches under the 🔒 **From your files** badge. The normal recency window uses file modification time; add `--corpus-all-time` only when the user explicitly asks to include older files. Corpus evidence is excluded from `--publish-html`, `library feed --publish`, and agent JSON by default. `LAST30DAYS_CORPUS_IN_EXPORT=1` is the explicit agent-JSON privacy opt-in; never enable it on the user's behalf. When a corpus is configured alongside `LAST30DAYS_API_KEY`/`LAST30DAYS_API_BASE`, the engine deliberately bypasses the hosted backend and runs locally.

**Perplexity source:** use it only when the user asks for Perplexity, Deep Research, or paid grounded synthesis, or when `perplexity` is already enabled in `INCLUDE_SOURCES` / `--search`. Prefer `PERPLEXITY_API_KEY`: normal runs use the controlled Agent API path, `search` returns raw Search API rows, and `both` combines them. Existing `OPENROUTER_API_KEY` installs stay compatible through one synchronous Sonar call; `search` and `both` fall back to Sonar because those direct APIs need a Perplexity key. Every normal mode is capped at one whole-topic planner subquery per command, including competitor fanout, and is not repeated during thin-source retries. With a direct key, normal Agent mode supplies only `web_search`, forces it for citation-critical grounding, uses a bounded step count, and supplies a local instruction. `sonar` remains a deprecated direct-key alias for `agent`. `LAST30DAYS_PERPLEXITY_AGENT_PRESET` is an explicit direct-key choice only; never set it for the user. `--deep-research` requires a normal positional topic. A direct key starts at most one paid `high`-preset background run with a 600-second default wall timeout; OpenRouter preserves the synchronous `perplexity/sonar-deep-research` fallback. It cannot be combined with discovery, drill, cached-only, competitor, or vs-mode. A local timeout does not stop a direct remote run. Report safe model and response metadata, but never expose request headers or raw tool traces.

**Reddit backend pin:** Reddit defaults to the free keyless backend. When `SCRAPECREATORS_API_KEY` is available, ScrapeCreators Reddit **search** backfills only if that free path returns **no items** (empty-only — a thin but non-empty free scrape does not spend credits). If the user wants paid coverage on thin free runs, tell them to set `LAST30DAYS_REDDIT_SC_MIN_ITEMS=<N>` (backfill when free yield is below N). If they say public Reddit is shallow, bot-gated, or missing nested comments, tell them they can set `LAST30DAYS_REDDIT_BACKEND=scrapecreators` alongside `SCRAPECREATORS_API_KEY` to make ScrapeCreators primary and keep the free path as fallback. Do not set either automatically for normal runs.

**Doctor health check:** When the user asks for a health check ("is X working?", "why is a source missing?", "what's broken?", "did setup work?"), run `"${LAST30DAYS_PYTHON}" "${SKILL_DIR}/scripts/last30days.py" doctor` (append `--json` for the machine contract) and relay the audit and fix prescriptions. `doctor` renders a **four-state audit** - **WORKING** (verified this run/last run or keyless-always-on), **TURNED ON - UNVERIFIED** (configured/opted-in but no run evidence), **NOT WORKING** (configured but failing, or the last run errored), **COULD BE ON** (available, not yet configured) - one line per source, plus a **CLI-health** block for sources that need a downloaded binary and indented **backup/comment** sub-lanes. Two on-demand modes: `doctor --postmortem` reads the last run's `last-report.json` and reports what actually broke per source (Failed/Partial/Succeeded with fix hints) - reach for it right after a run that returned less than expected; `doctor --probe` runs a **bounded** live test (free HTTP + keyless CLI sources only; credit-gated sources are never probed) to verify WORKING instead of guessing, and the same bounded probe auto-fires on a plain `doctor` when there is no fresh run. Per-source probe deadline is `LAST30DAYS_DOCTOR_PROBE_TIMEOUT` (default 10s). **MANDATORY standing rule.** Before research that depends on login-backed sources (X via cookies, Reddit's ScrapeCreators backfill), consult `doctor --cached --json` — it serves the report cached at `~/.config/last30days/doctor-cache.json` within its TTL (`LAST30DAYS_DOCTOR_TTL` seconds, default 900) for the cost of one file read. Re-run live `doctor` only when the cache is stale or the previous run reported a degraded login-backed source. When X is in ACTIVE_SOURCES_LIST, announce its predicted backend from the report's `sources.x.active_backend` (e.g. "X will use: bird") in the pre-research status line.

**Grok session expiry handling:** The grok CLI backend for X reports three auth states: `ok` (non-expired credentials), `expired` (access_token `expires_at` is past), and `missing` (never signed in). When doctor reports grok as **degraded** with an expiry timestamp, say "Grok session expired at {timestamp}; will attempt refresh at run time. If refresh fails, run `grok login --device-auth`" — not "Grok CLI is not signed in" (which misrepresents the history). The refresh attempt happens automatically at research time: an expired access_token does not prove the refresh_token is dead. If the run then fails with `auth_revoked` or `invalid_grant`, the user truly needs to re-login. **Host-facing copy:** when `sources.x.run_outcome.state` is `auth-failed` and the prior run's outcome was `ok`, say "X used {fallback} after the Grok session expired — run `grok login --device-auth` to restore first-party X." Avoid "Grok CLI is not signed in" when `run_outcome` history shows it worked recently. Avoid proactively installing grok or prompting about grok unless the user asks for first-party X search; the cookie and XAI_API_KEY paths work without a Grok subscription.


Then display (use "and more" if 5+ sources, otherwise list all with Oxford comma):

For GENERAL / NEWS / RECOMMENDATIONS / PROMPTING queries:
```
/last30days - searching {ACTIVE_SOURCES_LIST} for what people are saying about {TOPIC}.
```

For COMPARISON queries:
```
/last30days - comparing {TOPIC_A} vs {TOPIC_B} across {ACTIVE_SOURCES_LIST}.
```

Do NOT show a multi-line "Parsed intent" block with TOPIC=, TARGET_TOOL=, QUERY_TYPE= variables. Do NOT promise a specific time. Do NOT list sources that aren't configured.

Then proceed immediately to Step 0.45.

---

## Step 0.45: Query Quality Pre-Flight (detect keyword-trap topics BEFORE running the engine)

**MANDATORY. Before Step 0.5, diagnose the topic for known failure classes. If the topic is a keyword trap, reframe or ask a clarifying question BEFORE calling the engine. Running the engine on a doomed query burns 5+ minutes and produces junk. Detecting the trap upfront costs one turn.**

Known keyword-trap classes and how to handle each:

**Class 1: Demographic shopping query**
- Pattern: `gift for {age} year old {gender}`, `what to buy for my {relationship}`, `present for {demographic}`, `birthday gift for {age} {gender}`.
- Why it fails: no human on Reddit posts "I bought a 42 year old man a gift." Real posts use relationship + hobbies + budget. The literal phrase is not the vocabulary of the actual discussions. The 2026-04-18 "Birthday gift for 42 year old man" run returned r/todayilearned, r/japannews crime posts, r/LivestreamFail drama - none about gifts.
- Action: **Ask ONE clarifying question upfront**:
  > "Before I research, tell me a bit more - hobbies (cooks / runs / reads / gaming / outdoors / golf / music)? Relationship (husband / dad / friend / boss / brother)? Budget range? A 'gift for a 42 year old man' is a wide net; hobbies + relationship narrow it 10x."
- If the user declines to narrow ("just run it"), reframe to generic-demographic and scope to gift subreddits:
  - Drop the literal age (age 42 reads identically to 41 or 43 in social content; the number causes keyword collisions like Jackie Robinson #42)
  - Rewrite as `gifts for men in their 40s` or `gifts for men who [hobby]`
  - Scope `--subreddits=GiftIdeas,BuyItForLife,AskMen,malefashionadvice,Dads` (plus hobby-specific subs when known)
  - Note in the Resolved block: "Reframed demographic shopping query. Dropping literal age; scoping to gift communities."

**Class 2: Numeric / age keyword trap**
- Pattern: topic contains a specific number that collides with unrelated content (42 = Jackie Robinson + Hitchhiker's + a 42" quilt; 40 = 40th anniversary posts; 50 = state-count posts; 100 = bench-press posts).
- Why it fails: the number dominates retrieval and pulls in unrelated content. A search that prominently features "42" returns jersey-number posts; a search for "the 100" returns TV-show posts.
- Action: Strip the number from the engine search query unless changing or removing it would change the topic itself (e.g., "GPT-4" yes, "40 year old man" no, "Area 51" yes, "top 10 foods" no). Keep the number in the user's original framing for context; drop it from the engine query. Document in Resolved: "Dropping '{number}' from the search query - it is a keyword trap that pulls in unrelated content. Search will cover the concept generically."

**Class 3: Overly-literal concept phrase**
- Pattern: `how to use X`, `what is Y`, `tutorial for Z`, `explain A` — tutorial-shaped phrasing where social posts are in different vocabulary.
- Why it fails: social posts about Docker do not say "how to use Docker"; they say "my Docker setup", "nginx in Docker", "my dev loop", "tip for folks using Docker Compose". Tutorial phrasing matches blog titles, not social discussions.
- Action: Reframe from tutorial phrasing to discussion phrasing: "how to use Docker" becomes "Docker tips tricks workflows" or "Docker production setups". Document the reframe in the Resolved block.

**Class 4: Generic single-noun common word**
- Pattern: topic is a single common noun with no specific hook (`bread`, `sneakers`, `coffee`, `shoes`, `headphones`).
- Why it fails: single-noun queries have no anchor — the corpus is infinite and the signal is noise.
- Action: Ask for specificity before running:
  > "{TOPIC} is a huge category - are you asking about {specific-facet-A}, {specific-facet-B}, or {specific-facet-C}? Each is a different community. Pick one or tell me the angle."

**Class 5: Non-English / non-Latin-script topic (Hebrew, Arabic, Chinese, Japanese, etc.)**
- Pattern: topic contains non-Latin characters (Hebrew [\u0590-\u05FF], Arabic [\u0600-\u06FF], CJK [\u4E00-\u9FFF], etc.).
- Why it fails without intervention: Reddit, HackerNews, GitHub, and Polymarket are English-dominant platforms. A Hebrew brand like "קפה עלית" scores zero entity-matches across all four sources and returns only English-language noise as fallback padding.
- Action: **Mandatory pre-flight steps for non-English topics:**
  1. **Force `--web-backend brave`** in the engine command. Brave indexes non-English web (Ynet/Walla/Mako for Hebrew; Haber7/Hurriyet for Turkish; etc.) and is the only available source with real-language coverage.
  2. **Skip `--subreddits` targeting unless the topic has a known English-speaking community.** Generic subreddits (r/food, r/Israel) return English noise; omit them or scope tightly to known bilingual communities.
  3. **Note in the Resolved block:** "Non-English topic detected ([language]). Routing to `--web-backend brave`; Reddit/HN/GitHub will likely return zero on-topic results."
  4. **X/Twitter and YouTube are the highest-value missing sources for non-English topics.** Surface this clearly in the output so the user knows what would unlock deeper coverage.
- Do NOT skip this class check for mixed-script queries (e.g. "קפה עלית Elite Coffee") - if any non-Latin characters are present, Class 5 applies.

**Pre-Flight decision flow (do this BEFORE any WebSearch):**
1. Read the topic. Match against Classes 1-5 above.
2. If the topic matches a class, ALWAYS emit a visible pre-flight note before the Resolved block:
   - `Pre-Flight: topic matches {Class N} ({class name}). {Action: clarifying question / reframe / specificity ask}.`
3. If the action is a clarifying question, STOP after emitting it. Wait for the user response before any engine work.
4. If the topic does NOT match any class, emit a one-liner: `Pre-Flight: topic is a {named-entity / comparison / concept} - proceeding to Step 0.5.` Then proceed.

**One-turn gate rule:** do NOT run the engine on a keyword-trap topic without either (a) explicit user confirmation to "just run it anyway", or (b) a concrete reframed query. Burning 5 minutes on a doomed run is worse than a one-turn clarifying question.

**When the user provides context inline:** if a Class 1 query already contains hobbies/relationship/budget ("gift for my cooking-obsessed husband, $200"), SKIP the clarifying question and go straight to the reframe + scope action. The clarifying question exists to fill in the gaps; if the gaps are already filled, move on.

---

## Step 0.5: Pre-Flight Resolution (handles, repos, communities)

**Pre-Flight Checklist — do NOT stop after the first flag. Every applicable flag below is MANDATORY for its topic class.**

Before running the engine, determine which flags apply to this topic and resolve them. Reading only the "X handle" subsection and stopping there is the named failure mode of the Peter Steinberger disaster #2 (2026-04-18). The model admitted on debug: "I treated the 'X handle resolution' section as the full contract for pre-flight resolution and didn't --help the script to see what else existed." The checklist below IS the full contract.

| Flag | Resolved in | Applies when |
|------|-------------|--------------|
| `--x-handle={handle}` | Step 0.5 (Section A below) | X is in `ACTIVE_SOURCES_LIST` and the topic is a person, brand, product, or creator with an X presence |
| `--x-related={h1,h2,...}` | Step 0.5 (Section A below) | X is in `ACTIVE_SOURCES_LIST` and the topic has associated entities (founders, commentators, spouse, collaborators, media handles) |
| `--github-user={user}` | Step 0.5b | Topic is a person who ships code (developer, engineer, CEO-who-codes, researcher) |
| `--github-repo={owner/repo}` | Step 0.5c | Topic is a product / project / open-source tool |
| `--trustpilot-domain={domain}` | Step 0.5d | Topic is a company / brand / service with a Trustpilot presence (passing the flag also auto-activates the opt-in Trustpilot source for this run) |
| `--amazon-query={keyword}` | Step 0.5e | Recent buyer sentiment would materially inform the report AND `brightdata` is on PATH and logged in. Keyword is brand-plus-category (`Weber grill`), and for a person topic it is their company's product line (`June Oven`), not their name. Also add `amazon` to `--search` |
| `--subreddits={sub1,sub2,...}` | Step 0.55 | Always — almost every topic has active Reddit communities |
| `--tiktok-hashtags={h1,h2,...}` | Step 0.55 | Always — inferred from topic |
| `--tiktok-creators={c1,c2,...}` | Step 0.55 | Creator / influencer / brand topics |
| `--ig-creators={c1,c2,...}` | Step 0.55 | Creator / brand topics |
| `--web-backend brave` | Step 0.45 Class 5 | **MANDATORY** for non-Latin-script topics (Hebrew, Arabic, CJK, etc.) — Brave is the only source that indexes non-English web |
| `--web-backend parallel-mcp` | Explicit user request only | Use only when the user asks to use Parallel Search MCP. This opts the run into sending its search objective and queries to `https://search.parallel.ai/mcp`; never select it automatically. Anonymous use sends no authorization header; an existing `PARALLEL_API_KEY` is sent as Bearer auth. |
| `--auto-resolve` | Fallback | WebSearch is available but Step 0.55 could not resolve everything cleanly — use as belt-and-suspenders |

**Checkpoint before running the engine:** your Bash command must include every flag from the checklist that applies to this topic. For a person who ships code (the Peter Steinberger class), that is MINIMUM `--x-handle` AND `--github-user` AND `--subreddits`, and typically `--x-related` too. A command with only `--x-handle` on a person topic is a pre-flight skip and a Step 0.5 regression.

---


## Load the relevant host/platform only

- [Section A: Resolve X Handles (only when X is active and the topic could have X accounts)](planning-section-a-resolve-x-handles-only-when-x-is-active-and-the-topic-could-have-x-accounts.md) — read only when this host/platform applies.
- [Step 0.5b: Resolve GitHub Username (if topic is a person) — MANDATORY FOR PERSON TOPICS](planning-step-0-5b-resolve-github-username-if-topic-is-a-person-mandatory-for-person-topics.md) — read only when this host/platform applies.
- [Step 0.5c: Resolve GitHub Repos (if topic is a product/project)](planning-step-0-5c-resolve-github-repos-if-topic-is-a-product-project.md) — read only when this host/platform applies.
- [Step 0.5d: Resolve Trustpilot Domain (if topic is a company/brand)](planning-step-0-5d-resolve-trustpilot-domain-if-topic-is-a-company-brand.md) — read only when this host/platform applies.
- [Step 0.5e: Decide the Amazon Buyer-Signal Lane (if `brightdata` is available)](planning-step-0-5e-decide-the-amazon-buyer-signal-lane-if-brightdata-is-available.md) — read only when this host/platform applies.
