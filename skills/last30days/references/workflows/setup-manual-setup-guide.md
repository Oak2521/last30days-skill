### Manual Setup Guide

Shown when a Claude Code user picks "Manual setup", or for anyone who wants to configure by hand. Present as plain text (not blockquoted).

The magic of /last30days is Reddit comments + X posts together - and both are free. Add these to `~/.config/last30days/.env`:

**X/Twitter (pick one - the most important source):**
- `X_BEARER_TOKEN=xxx` - the official X API v2 (`api.x.com`) with an app-only bearer from the X developer console. Recent posts, about a week back on the Basic tier, unless your X developer project has full-archive access. Persist it with `setup --store-key X_BEARER_TOKEN` (value on stdin, masked in output). Outside a Grok Bot host also add `LAST30DAYS_X_BACKEND=xapi` so the engine selects it (`doctor` says so when the bearer is set without it).
- **Grok CLI (no X credential):** install with `curl -fsSL https://x.ai/cli/install.sh | bash`, then `grok login`. No X account, no cookies, no API key. Needs a Grok plan; calls draw on it.
- `FROM_BROWSER=auto` - free. Reads your x.com login cookies live at search time (Firefox/Safari, never saved to disk).
- `XAI_API_KEY=xxx` - no browser access needed. Get a key at api.x.ai. Best for servers.
- `XQUIK_API_KEY=xxx` - keyless-style X via Xquik.
- `AUTH_TOKEN=xxx` + `CT0=xxx` - paste your X cookies manually (x.com → F12 → Application → Cookies).

**X on a Grok Bot (repair).** On a `LAST30DAYS_HOST=grok-bot` host X runs only through official access, so if X returns nothing there: add the "X for Grok Bot" plugin and connect X inside Grok Bot (the X connector lane; full 30-day coverage on the included credits), or add `X_BEARER_TOKEN` (recent posts, about the last week, unless your X developer project has full-archive access) or `XAI_API_KEY` from console.x.ai through `setup --store-key <NAME>`, or, when the footer reports X API credits exhausted (`payment-required`), top up credits in the X developer console. Nothing in the Linux / Mac mini repair section below applies on a Grok Bot.

**X on Linux / Mac mini (repair).** These hosts (never a `LAST30DAYS_HOST=grok-bot` host) can't decrypt a local Chrome cookie store, so if X returns nothing there, feed bird a cookie pair one of these ways (a MacBook does NOT do any of this — it uses its Keychain / Firefox / Safari extract; do not launch box-chrome on a MacBook):
- **agentcookie sidecar:** install the `agentcookie` CLI so the engine can read your `auth_token`/`ct0` from it automatically. Nothing to configure; `AGENTCOOKIE=off` disables it.
- **Live Chrome login over CDP (the proven extras-host path).** The engine reads a live signed-in Chrome over the DevTools Protocol, but you must LAUNCH that Chrome on the extras port and log in first — `setup --allow-browser-cookies` alone opens no window. Steps (a MacBook skips all of this):
  1. Set `AGENTCOOKIE=off` for this harvest so a sidecar can't mix in a different pair (leave it unset again after success).
  2. Launch a throwaway login Chrome on the last30days extras port **18800** — this port is the last30days convention (`SAND_CHROME_REMOTE_DEBUG_PORT=18800`), NOT box-chrome's built-in default (`9222` + the display number). **Launch via the host `box-chrome` wrapper** (which sets `--class=box-chrome`); do NOT launch raw `google-chrome-stable`, and in particular do NOT launch raw Chrome with a custom `--class` — a raw Chrome with `--class=l30d-…` failed where `box-chrome` (class `box-chrome`) succeeded. Do NOT rely on any `GrokAgent` user-agent token: it is not required and may be disabled on the host (`/tmp/sand-ua-token-disabled`), so never tell users it must be present. Run `"${LAST30DAYS_PYTHON:-python3}" skills/last30days/scripts/box_chrome_login.py` to print the exact host-correct command (add `--exec` to launch it); on a MacBook it prints "no launch needed" and spawns nothing. When `box-chrome` is on PATH the command is:
     ```
     mkdir -p /tmp/last30days-x-chrome
     CHROME_USER_DATA_DIR=/tmp/last30days-x-chrome SAND_CHROME_REMOTE_DEBUG_PORT=18800 box-chrome --new-window https://x.com/login
     ```
     If `box-chrome` is missing, do NOT invent a google-chrome flag soup (a raw Chrome with a custom `--class` is what failed) — sign into x.com in a Chrome that already exposes a remote-debugging port and pin `BROWSER_CDP_URL` to that endpoint instead.
  3. Do NOT fill the login form and do NOT drive the page (no Playwright/Puppeteer/computerUse/xdotool, no typing credentials). Wait until the x.com login page is actually visible, THEN hand the desktop / computer-preview to the human: "Log into X in this Chrome window." (A HUD over the login is OK only as a handoff, never to click the page.)
  4. After they hand back, confirm the window is signed in (x.com/home). Append `BROWSER_CDP_URL=http://127.0.0.1:<port>` to `~/.config/last30days/.env` (append-only), using the debug port the Chrome actually listens on — `18800` if you launched with the command above, or the real port otherwise (a live harvest pinned `http://127.0.0.1:9334`). Do NOT write `AUTH_TOKEN` or `CT0` — the pair is read live each run. Then run `setup --allow-browser-cookies`; extras CDP reads the live pair. Pinning `BROWSER_CDP_URL` after login is also the guard if a stale/logged-out Chrome happens to answer on `18800`.
  5. If X shows a block / challenge / rate-limit, STOP — tell them to wait and retry later. Do not keep launching Chromes.
- **`XAI_API_KEY=xxx`** - key-based X, no browser at all.
- **Grok CLI** - run `grok login`, then pin `LAST30DAYS_X_BACKEND=grok` (pin-only; a leftover grok login never auto-steals the X lane). Needs a Grok plan.

**Reddit (free, works out of the box):**
- Free keyless discovery (RSS + shreddit listings) gives threads + top comments with upvote counts. No setup required.
- `SCRAPECREATORS_API_KEY=xxx` - optional Reddit search backup when the free path returns **no items** (default). A non-empty free scrape does **not** escalate — set `LAST30DAYS_REDDIT_SC_MIN_ITEMS` or `LAST30DAYS_REDDIT_BACKEND=scrapecreators` if you want paid backfill/primary (see Reddit backend pin).

**YouTube (free, open source):**
- Run `brew install yt-dlp` (or `pip install yt-dlp`) - enables YouTube search + transcripts.
- `SCRAPECREATORS_API_KEY=xxx` - optional server-side transcript fallback, used only when yt-dlp is rate-limited/bot-gated.

**Digg (free, keyless):**
- Run `npx @mvanhorn/printing-press-library install digg --cli-only` - installs the Digg CLI for trending news, GitHub stars, and pipeline feeds. Activates when `digg-pp-cli` is on your PATH (typically `$HOME/.local/bin`).

**GitHub Issues/PRs (free, no key needed):**
- If the `gh` CLI is installed and authed (`brew install gh && gh auth login`), GitHub search is automatic. No API key required.

**Bonus: TikTok, Instagram, YouTube comments (ScrapeCreators):**
- `SCRAPECREATORS_API_KEY=xxx` - 10,000 free calls at scrapecreators.com.
- After adding your key, set `INCLUDE_SOURCES=tiktok,instagram` to turn on the popular ones. (Threads, Pinterest, and LinkedIn are also available via `INCLUDE_SOURCES=threads,pinterest,linkedin` for power users.)

**Other optional sources (add anytime):**
- `PERPLEXITY_API_KEY=xxx` - preferred Agent/Search API path with citations; set `INCLUDE_SOURCES=perplexity`. Existing `OPENROUTER_API_KEY` installs keep the synchronous Sonar fallback.
- `XIAOHONGSHU_API_BASE=http://localhost:18060` - Xiaohongshu/RED via a logged-in x-mcp browser plugin or `xiaohongshu-mcp` service; optional unless the local service runs on a custom URL. Opt in per run with `--search xhs`, or persistently via `INCLUDE_SOURCES=xiaohongshu`.
- DripStack (premium financial newsletter search) is opt-in only: per run with `--search dripstack`, or persistently via `INCLUDE_SOURCES=dripstack`. Free public search API, no key; never active without the opt-in.
- Telegram (public channels) is opt-in via `--telegram-sources=handle1,handle2` (auto-activates for that run) or persistently via `TELEGRAM_SOURCES=handles` + `INCLUDE_SOURCES=telegram`. Requires `SCRAPECREATORS_API_KEY`. Named public channels only; no keyword discovery.
- `BSKY_HANDLE=you.bsky.social` + `BSKY_APP_PASSWORD=xxx` - Bluesky (free app password).
- `BRAVE_API_KEY=xxx` or `EXA_API_KEY=xxx` - web search backends.

**CRITICAL: NEVER overwrite an existing `.env`.** Before writing ANY key:
1. Check if the file exists: `test -f ~/.config/last30days/.env`
2. If it exists, READ it, then APPEND only missing keys with `>>` (double redirect).
3. NEVER use `>` (single redirect) - it destroys existing content.
4. If it doesn't exist: `mkdir -p ~/.config/last30days && touch ~/.config/last30days/.env`

Always add this last line: `SETUP_COMPLETE=true`. Then proceed to research.

The setup wizard's mechanical work lives in a Python module so it runs across all hosts (Claude Code, Codex, Cursor, etc.) while you drive the consent conversation above. The common-case (already set up) path through this file stays short.

---
