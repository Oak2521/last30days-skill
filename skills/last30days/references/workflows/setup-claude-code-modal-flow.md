### Claude Code Modal Flow

**Follow these steps IN ORDER unless the Research Continuation Override routes a waiting topic directly to research.** The normal sequence is: (1) welcome (built into the setup modal) → (2) setup modal → (3) run setup if chosen → (4) ScrapeCreators offer modal → (5) source opt-in modal → (6) first-topic picker. Start at step 1.

**Step 1 - Welcome.** The welcome pitch is delivered INSIDE the Step 2 setup modal, NOT as a separate message. Claude Code folds Bash/tool output behind "ctrl+o to expand", so a separate welcome message - or a `--welcome` command run - gets buried and the user never sees it. The AskUserQuestion modal is the only always-fully-visible surface, so the pitch lives in its question text. Do NOT run a separate `--welcome` command in this modal flow, and do NOT try to print the welcome as a chat message before the modal; go straight to Step 2. (The `--welcome` command still exists for the Non-Modal Prose Flow below, where there is no modal.)

**Step 2 - Welcome + setup choice (one modal).** Call AskUserQuestion with EXACTLY this question and these options. Reproduce the question verbatim, including the welcome pitch on the first lines:

Question:
"Welcome to /last30days! I research any topic across Reddit, X, YouTube, TikTok, Digg, arXiv, Techmeme, HN, Polymarket & more - pulling what people actually said in the last 30 days.

How would you like to set up?"

Options:
- "Auto setup (~30s)" - description: "Scan browser cookies for X + install yt-dlp (YouTube), Digg, arXiv, Techmeme. Reddit/HN/Polymarket/GitHub/Web work out of the box. Add TikTok + Instagram after via ScrapeCreators (10k free calls)."
- "Manual setup" - description: "Show me each source and credential to configure by hand."
- "Skip for now" - description: "Just the free no-setup sources: Reddit (with comments), HN, Polymarket, GitHub, Web."

**Step 3 - Run setup based on the choice.**

**If the user picks Skip for now:** write `SETUP_COMPLETE=true` to `~/.config/last30days/.env` (append-only; run `mkdir -p ~/.config/last30days && touch ~/.config/last30days/.env` first if the file does not exist) so the wizard does NOT re-fire on every subsequent run. Do not run any `setup` command - the always-on sources (Reddit, HN, Polymarket, GitHub, Web) need no setup. If the invocation already includes a topic, research it immediately, then resume Step 4 (and Step 5 if a key is saved) in the same run after the findings; Step 6 stays skipped because the topic was supplied. Otherwise continue to Step 6.

**If the user picks Auto setup:**

Get cookie consent first. Check if `BROWSER_CONSENT=true` already exists in `~/.config/last30days/.env`; if so, skip the consent prompt and run `setup --allow-browser-cookies` directly. Otherwise **call AskUserQuestion:**
Question: "Auto setup installs the free CLIs either way - yt-dlp (YouTube), Digg, arXiv, and Techmeme. The only thing that needs your OK is reading your browser's x.com cookies to authenticate X/Twitter search: I check Chrome first (a one-time macOS Keychain prompt may appear; click Always Allow), then Firefox and Safari. Cookies are read live, never saved to disk. Include X?"
Options (give each option the description shown):
- "Yes - X cookies + all CLIs" - description: "Read x.com cookies for X/Twitter search AND install yt-dlp (YouTube), Digg, arXiv, and Techmeme." Run `"${LAST30DAYS_PYTHON:-python3}" skills/last30days/scripts/last30days.py setup --allow-browser-cookies` (relative to the skill root). Append `BROWSER_CONSENT=true` to `.env` after setup completes.
- "Skip X - just the CLIs" - description: "No cookie reads. Still installs yt-dlp (YouTube), Digg, arXiv, and Techmeme." Run `FROM_BROWSER=off "${LAST30DAYS_PYTHON:-python3}" skills/last30days/scripts/last30days.py setup`. If the invocation already includes a topic, immediately research it with `--no-browser-cookies`, then resume Step 4 (and Step 5 if a key is saved) in the same run after the findings; Step 6 stays skipped because the topic was supplied.
- "xAI API key for X instead" - description: "Use an api.x.ai key for X search (no cookie read), plus install yt-dlp (YouTube), Digg, arXiv, and Techmeme." Ask them to paste it, write `XAI_API_KEY` to `.env`, then run `FROM_BROWSER=off "${LAST30DAYS_PYTHON:-python3}" skills/last30days/scripts/last30days.py setup`.

**Grok CLI is an opt-in backup, not a setup-time recommendation.** Do NOT check for grok first or offer it as a primary option during setup. A leftover `~/.grok/auth.json` must never steal the X lane. If the user mentions having a Grok account, tell them: "You can use the Grok CLI by pinning `LAST30DAYS_X_BACKEND=grok` in your `.env` after running `grok login`. This is opt-in because a leftover grok login should not take over X automatically." Do not call it free — it needs a Grok plan.

The consented `setup --allow-browser-cookies` run extracts cookies (Chrome/Chromium family first via the Keychain with no Full Disk Access, then Firefox and Safari as fallbacks; the winning browser is pinned for future runs only when it is Firefox or Safari, so Chrome never re-triggers the Keychain prompt on later runs) and best-effort installs yt-dlp (YouTube), the free keyless Digg CLI (`digg-pp-cli` via `@mvanhorn/printing-press-library install digg --cli-only`; Digg activates only when the binary is on the **agent subprocess PATH**, typically `$HOME/.local/bin`; setup reports honestly if installed off-PATH; recommend-only if `npx` is unavailable), plus the free keyless arXiv and Techmeme CLIs. Show the user what was found and installed - including whether Digg landed on PATH (active) or off-PATH (installed but not yet active).

**Extras-host X login (Linux / Mac mini / Darwin agentcookie sink — a MacBook SKIPS this, and so does a `LAST30DAYS_HOST=grok-bot` host, which never runs it).** On a MacBook the Keychain/Firefox/Safari extract above is all X needs. On an extras host the local Chrome store can't be decrypted, so that extract finds nothing and X stays empty unless you also capture a LIVE login over CDP. After the cookie-consent setup run: run `"${LAST30DAYS_PYTHON:-python3}" skills/last30days/scripts/box_chrome_login.py` — it prints the exact host-correct command (or launches it with `--exec`), and on a MacBook it prints "no launch needed" and spawns nothing. When `box-chrome` is on PATH it launches a throwaway profile on the last30days extras port **18800** (the last30days convention `SAND_CHROME_REMOTE_DEBUG_PORT=18800`, not box-chrome's default): `CHROME_USER_DATA_DIR=/tmp/last30days-x-chrome SAND_CHROME_REMOTE_DEBUG_PORT=18800 box-chrome --new-window https://x.com/login`. Wait for the x.com login page, then HAND THE DESKTOP to the human to type — do NOT fill or drive the form. After they sign in, append `BROWSER_CDP_URL=http://127.0.0.1:18800` to `.env` (never `AUTH_TOKEN`/`CT0`; keep `AGENTCOOKIE=off` during the harvest), then re-run `setup --allow-browser-cookies` so extras CDP reads the live pair. Full steps and the block/rate-limit stop rule are in **X on Linux / Mac mini** below. This extras-host login only runs on the consented "Yes - X cookies" path; the Research Continuation Override never skips it when the user said yes to X.

**macOS Full Disk Access remediation (Safari fallback only).** Chrome and Firefox need no Full Disk Access; only the Safari fallback does. After the `setup` run, inspect its stderr. If it contains `Permission denied reading Cookies.binarycookies` and the platform is macOS, the OS blocked the Safari read - surface the fix instead of swallowing it: `macOS blocked the Safari cookie read. If your x.com login is in Chrome, you don't need this. To use Safari: System Settings > Privacy & Security > Full Disk Access > enable your terminal (or the Claude app), then I can retry.` Offer ONE retry only when no research topic is waiting. If a topic is already waiting or the user skips, continue immediately with available sources.

**Step 4: ScrapeCreators offer (every first run unless the Research Continuation Override already started a waiting topic).** Show this as plain text, then a modal:

ScrapeCreators adds TikTok and Instagram - posts AND top comments - plus YouTube comments, all on by default. 10,000 free calls, no credit card. Your key also backfills Reddit **search** when the free path returns no items (empty-only by default; Reddit comments already come free via shreddit), and backstops YouTube transcripts if yt-dlp gets throttled. (We don't get a cut.) You can widen coverage even further in the next step.

Before the modal, run `which gh` via Bash silently; store as gh_available.

**Call AskUserQuestion:**
Question: "Want to add TikTok and Instagram? Your key also backfills empty Reddit search and backs up YouTube when yt-dlp is throttled. (We don't get a cut.)"
Options:
- "ScrapeCreators via GitHub (recommended - most free calls)" - description: "Opens GitHub - we copy your code to your clipboard automatically, so you just paste it (Cmd+V), ~20-30s. Grants the full 10,000 free calls - more than the web signup." (Recommend this over the web option because the GitHub path grants more free calls.) This is a **two-command flow** - `--github-start` returns the code fast (foreground), then `--github-poll` waits for you to authorize. The code comes back in the command output, so it can't be missed:
   1. **Run `--github-start` in the FOREGROUND** (it returns in ~1-2s, it does NOT block-poll): `"${LAST30DAYS_PYTHON:-python3}" skills/last30days/scripts/last30days.py setup --github-start`. It submits the device flow, copies the code to the clipboard, opens the browser, and returns a JSON blob plus a plain `Your GitHub code: XXXX-XXXX` line on stdout.
      - If the returned `status == "already_registered"` (a key was already saved): tell the user "You're already set up - your existing ScrapeCreators key is active" and STOP (do not run poll).
      - If `status == "error"`: show the message and offer the web option below.
   2. **SHOW THE CODE.** Read the `user_code` from the output and output ONE chat message: "Enter this code on the GitHub page: **XXXX-XXXX** - it's already on your clipboard, so just paste (Cmd+V) and click Continue." (If the output said the clipboard copy failed, tell them to type it instead.) The code is right there in step 1's output - surfacing it is the whole point.
   3. **Run `--github-poll`** (background with a 5-minute timeout, or foreground): `"${LAST30DAYS_PYTHON:-python3}" skills/last30days/scripts/last30days.py setup --github-poll`. Parse the **LAST** JSON line of its stdout for the final status:
      - `status == "success"`: the engine persisted the key (`"persisted": true`, MASKED `api_key` - never ask for or echo the raw key); confirm "You're in! 10,000 free calls. TikTok, Instagram, empty-path Reddit search backup, and YouTube transcript fallback are now active."
      - `status == "success"` but `"persisted": false` (key write failed): do NOT claim sources are active - tell the user signup worked but saving the key failed, and have them add `SCRAPECREATORS_API_KEY=<key>` to `~/.config/last30days/.env` manually.
      - `status == "error"` **with `message == "Authorized but failed to fetch API key"`** (exact match; often also `"reason": "no_api_key"`): GitHub authorized fine - do NOT say auth failed. This usually means your GitHub is **already linked** to a ScrapeCreators account. Tell the user: "GitHub authorized, but I couldn't auto-grab your ScrapeCreators key - your GitHub is probably already linked to an account. Get your key at scrapecreators.com and paste it here, or Skip." Then accept a pasted key (write `SCRAPECREATORS_API_KEY` to `.env`) or offer the web/skip options.
      - `status == "error"` **with `message` containing `ScrapeCreators profile failed`** (or `"reason": "upstream_error"`): GitHub authorized fine - do NOT say auth failed, and do **NOT** say the GitHub is already linked. ScrapeCreators returned a server error after auth. Tell the user: "GitHub authorized, but ScrapeCreators had a server error minting your key - this is on their side, not yours. Sign up or log in at scrapecreators.com, grab a key there, and paste it, or Skip / retry later." Accept a pasted key or offer web/skip. Do not imply they already have a working linked account.
      - `status == "timeout"`, or any other `status == "error"` message: show "GitHub auth didn't complete - no worries, sign up at scrapecreators.com or try again later," then offer the web option below.
   - **One-shot fallback:** hosts that prefer a single call can still run `setup --github` (foreground), which chains start+poll; tell the user first that a code will appear on their clipboard to paste.
- "Open scrapecreators.com (Google sign-in)" - run `open https://scrapecreators.com` via Bash, then ask them to paste the API key. Write `SCRAPECREATORS_API_KEY={key}` to `~/.config/last30days/.env`.
- "I have a key" - accept the key, write to `.env`.
- "Skip for now" - proceed without ScrapeCreators. No TikTok/Instagram, no empty-path Reddit search backup, and no YouTube transcript fallback when yt-dlp is throttled (your free sources still work, including keyless Reddit comments via shreddit).

**Step 5: Source opt-in (only if a ScrapeCreators key was saved, not if skipped).** Comments are the DEFAULT, never an opt-in - there is no posts-only tier. Plain text then modal:

Your key is set. On by default: TikTok + Instagram (posts AND top comments), and YouTube comments. Reddit search stays on the free keyless path (with empty-only ScrapeCreators search backup); Reddit comments stay free via shreddit. Want the widest net?

**Call AskUserQuestion:**
Question: "Which ScrapeCreators sources?"
Options:
- "TikTok + Instagram + all comments (recommended)" - the default: posts AND top comments (ranked by votes) for TikTok + Instagram, plus YouTube comments. Append `INCLUDE_SOURCES=tiktok,instagram,youtube_comments,tiktok_comments,instagram_comments` to `~/.config/last30days/.env` (the list must include `tiktok,instagram` so they are not treated as excluded). Confirm: "TikTok, Instagram, and top YouTube/TikTok/Instagram comments are on."
- "Everything (also Threads + Pinterest)" - everything above plus Threads and Pinterest searches. Most coverage, most credits. Append `INCLUDE_SOURCES=tiktok,instagram,youtube_comments,tiktok_comments,instagram_comments,threads,pinterest`. Confirm: "Everything's on: posts + comments for TikTok/Instagram/YouTube, plus Threads and Pinterest."

**Step 6: First-topic picker.** Once `SETUP_COMPLETE=true` is written, **call AskUserQuestion:**
Question: "What do you want to research first?"
Options:
- "Claude Code vs Codex" - tech comparison
- "Sam Altman" - person in the news
- "Warriors Basketball" - sports
- "AI Legal Prompting Techniques" - niche/professional
- "Type my own topic"

If the user picks an example, run research with it. If "Type my own", ask what they want. **If the user already supplied a topic with the command (e.g. `/last30days Mercer Island`), SKIP this picker and use their topic directly.**

**END OF FIRST-RUN WIZARD.** Everything in the Modal Flow ONLY runs on first run. If `SETUP_COMPLETE=true` exists, skip ALL of it - no welcome, no modals, no topic picker - and go straight to research (Parse User Intent).

**If the user picked Manual setup** at Step 2, follow the **Manual Setup Guide** below instead of the Auto branch (the guide writes `SETUP_COMPLETE=true` itself), then continue to Step 6.

---
