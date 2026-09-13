> Read only for the matching mode. Resolve script paths relative to the parent SKILL.md. User/host requirements govern citations, output and footer. Preserve required source links and do not replace them with hidden archives.

## Step 0: First-Run Setup Wizard

**CRITICAL: ALWAYS execute Step 0 BEFORE Step 1, even when the user provided a topic.** If the user typed `/last30days Mercer Island`, preserve that topic while handling the first-run choice. The wizard may ask for browser-cookie consent, but declining or skipping X must never stop the requested research.

**RESEARCH CONTINUATION OVERRIDE (dominates every optional onboarding step below):** When the invocation already includes a topic and the user declines X/browser-cookie access inside Auto setup, run the cookie-free setup path, then immediately research that topic with the sources that are available. When the user chooses Skip for now, mark setup complete and immediately research without running setup. In either case, skip the ScrapeCreators offer, source-tier prompt, retry prompt, and first-topic picker until after the useful research response. Do not ask another X question in the same run. After the findings, report X once as an optional omitted source without an unlock pitch, **then RESUME the deferred onboarding in the SAME run: present the Step 4 ScrapeCreators offer, and Step 5 source opt-in if a key gets saved.** Deferred is not dropped — `SETUP_COMPLETE=true` is already written, so a later invocation skips Step 0 entirely and this run is the only chance to make the offer. The first-topic picker stays skipped (a topic was already supplied), and the resume never re-asks X/browser-cookie consent. Browser-cookie reads still require explicit consent; a skip or no answer is never consent.

**You are the conversational driver.** The Python setup script does only mechanical work (cookie reads, tool installs, the GitHub device-auth flow) - it CANNOT prompt the user, because it runs as a non-interactive subprocess. So consent happens HERE, in chat: you ask, the user answers, and you gate each subprocess call on the answer. Do NOT just run `setup` and report the result - that is the silent-onboarding regression this section exists to prevent.

**First-run detection (silent, no commands, no output to user):**
- If `SETUP_COMPLETE=true` is available from process env, project config (`.claude/last30days.env`), global config (`~/.config/last30days/.env`), or the setup check reports configured credentials, skip Step 0 entirely and go to Step 1 (CRITICAL: Parse User Intent below). Do NOT announce that setup is complete. The user does not need a status message on every run.
- Do NOT treat the absence of `~/.config/last30days/.env` alone as a first run. Credentials may live in process env, project config, macOS Keychain (`last30days-<KEY>`), pass(1), or host-provided auth.
- If no setup marker or credential source is present, this is a first run.

**Named onboarding contracts:**
- *(2026-06-22, silent-wizard regression - Fredy Montero run):* a prior version said "Run `setup` ... follow the wizard's prompts end-to-end." But `run_auto_setup()` has NO prompts - it extracts cookies, installs yt-dlp + Digg, and writes `SETUP_COMPLETE` with zero interaction. The model ran the silent path, never asked cookie consent, never surfaced the macOS Full Disk Access fix, and never offered the ScrapeCreators signup. Consent must be conversational.
- *(2026-06-22, NUX restoration):* the original v3.0.0 Claude Code wizard was a guided, modal-driven flow (welcome → Auto/Manual/Skip → cookie consent → ScrapeCreators offer → source opt-in → first-topic picker) that eroded over time. It is restored below as the **Claude Code Modal Flow**. Do NOT collapse it back into a bare prose call - the guided modals are the feature. Reference capture: `docs/reference/old-nux-wizard-v3.0.0.md`.

**Platform split - run exactly ONE branch:**
- **If you HAVE WebSearch and AskUserQuestion (Claude Code):** run the **Claude Code Modal Flow** immediately below.
- **If you do NOT (OpenClaw, Codex, Cursor, Gemini CLI, raw CLI):** run the **Non-Modal Prose Flow** further down. It does the same work conversationally, without modals.
- **If you are running as a Grok Bot** (the Grok Bot host rule in HOW TO INVOKE): run the **Grok Bot Prose Flow**, the third branch, below the Non-Modal flow. The X connector comes first, any backup key is written only through the engine, and no browser session is read. Cursor stays in the Non-Modal Prose Flow.

---


## Load the relevant host/platform only

- [Claude Code Modal Flow](setup-claude-code-modal-flow.md) — read only when this host/platform applies.
- [Non-Modal Prose Flow](setup-non-modal-prose-flow.md) — read only when this host/platform applies.
- [Grok Bot Prose Flow](setup-grok-bot-prose-flow.md) — read only when this host/platform applies.
- [Manual Setup Guide](setup-manual-setup-guide.md) — read only when this host/platform applies.
