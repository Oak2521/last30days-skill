### Grok Bot Prose Flow

For a Grok Bot host. The Grok Bot host rule in HOW TO INVOKE applies throughout: `LAST30DAYS_HOST=grok-bot` is exported in every shell that runs the engine, including every command below. Same conversational shape as the Non-Modal Prose Flow, no modals, and the X connector comes first: on this host the engine never reads a browser session and X runs only through official access. Run in order; wait where it says to wait.

**1. Host key + welcome.** Persist the host signal so later runs and `doctor` see it: if `~/.config/last30days/.env` is missing, `mkdir -p ~/.config/last30days && touch ~/.config/last30days/.env`; then append one line `LAST30DAYS_HOST=grok-bot` (append-only with `>>`; never `>`). Then run `"${LAST30DAYS_PYTHON:-python3}" "${SKILL_DIR}/scripts/last30days.py" --welcome` and show its stdout VERBATIM.

**2. Permission preflight.** Run `"${LAST30DAYS_PYTHON:-python3}" "${SKILL_DIR}/scripts/last30days.py" --preflight` and summarize the human-readable result (config source, planned writes, optional commands). It reads nothing from a browser and runs no research.

**3. X connector (primary - check this BEFORE offering any key).** Look for an X post-search tool from the X connector in this session: the "X for Grok Bot" plugin (search posts, read timelines, check mentions), for example `search_posts_all`. Any of its search tools counts; use the one that searches posts by query.
   - **Present** → tell the user: `X search runs through your X connector on the credits included with Grok Bot, with full 30-day coverage - nothing to configure.` Export `LAST30DAYS_X_HOST_LANE=1` next to `LAST30DAYS_HOST=grok-bot` in every engine shell for this session, and on every research run follow the X connector recipe in Research Execution: one `topic` call sized 10 / 30 / 60 by depth (`--quick` / default / `--deep`) with `-is:retweet` and the window; per `--x-handle`, a `from` call of 8 and a `mention` call of 5; per `--x-related` handle, a `related` call of 3; written to a `last30days-x-posts/1` envelope (`generated_at`, `topic`, `window`, `status`, `calls` tagged `topic` / `from` / `mention` / `related`, each post exactly `id`, `author_handle`, `created_at`, `text`, `likes`, `reposts`, `replies`, `quotes` and nothing else); if the tool rejects the window or count parameters, omit them and write `status: partial` with `error: window-unsupported`; pass the file as `--x-posts <file>`. Skip step 4.
   - **Absent** → continue to step 4.

**4. Backup key (only when the connector is absent).** Say, then WAIT: `This session has no X connector, so X needs a key. Best fix: add the "X for Grok Bot" plugin and connect X inside Grok Bot (it provisions an X developer account for you, with credits included). Otherwise paste an X_BEARER_TOKEN from the X developer console - recent posts, about the last week, unless your X developer project has full-archive access - or an XAI_API_KEY from console.x.ai. Or skip X for now. (bearer / xai / skip)`
   - On a pasted key → persist it ONLY through the engine's key-write path, feeding stdin from a single-quoted heredoc. Never an ad-hoc shell write of the value, never interpolate it into a command line:

     ```bash
     "${LAST30DAYS_PYTHON:-python3}" "${SKILL_DIR}/scripts/last30days.py" setup --store-key X_BEARER_TOKEN <<'KEY_EOF'
     {PASTED_VALUE}
     KEY_EOF
     ```

     Use `setup --store-key XAI_API_KEY` for an xAI key. The engine prints `X_BEARER_TOKEN=****` (or `XAI_API_KEY=****`) plus a JSON `persisted` line; never echo the value back, and confirm only in the masked `NAME=****` form. Running it again with a new value replaces the stored one (that is how a rejected key is rotated). A `"persisted": false` means the write failed: say so and do not claim X is active.
   - On **skip** → append `X_DECLINED=grok-bot` to `~/.config/last30days/.env` (append-only) so later runs stay quiet about X: no unlock pitch, no second key question. If the invocation already includes a topic, research it right after step 5 and resume steps 6-7 after the findings.

**5. Setup (free CLIs, no browser reads).** Run `"${LAST30DAYS_PYTHON:-python3}" "${SKILL_DIR}/scripts/last30days.py" setup` (the plain form; on this host it reads nothing from a browser). It best-effort installs yt-dlp (YouTube), the Digg CLI, arXiv, and Techmeme and writes `SETUP_COMPLETE=true`. Show what was installed, including whether Digg landed on PATH.

**6. ScrapeCreators offer and source tier.** Run steps 5 and 5b of the Non-Modal Prose Flow exactly as written there (GitHub device-code signup with `setup --github-start` then `setup --github-poll`; the engine persists the key and masks it).

**7. Complete.** Confirm `SETUP_COMPLETE=true` is in `~/.config/last30days/.env` (append it if `setup` did not run), briefly confirm which sources are active (re-run `--preflight`, or safe `--diagnose`, with the host signal and, when the connector is present, `LAST30DAYS_X_HOST_LANE=1` exported; `--diagnose` then lists `x` as served by the connector), and proceed to research.

---
