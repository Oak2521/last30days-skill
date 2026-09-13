### Step 0.5e: Decide the Amazon Buyer-Signal Lane (if `brightdata` is available)

**Availability first.** This lane exists only when the Bright Data CLI is on PATH and logged in (`--diagnose` reports `brightdata_installed` and `brightdata_authenticated`). If either is false the source does not exist, nothing changes, and you should skip this step entirely — do not mention it, do not suggest installing it mid-run.

**The one question to ask:** *would recent Amazon buyer sentiment materially inform this report?* Not "is this shopping" — the test is whether buyer evidence is real evidence for this topic.

| Topic | Fires? | `--amazon-query` |
|---|---|---|
| "Weber Grills" | Yes — brand topic where review signal is core evidence | `Weber grill` |
| "best bluetooth speaker under $100" | Yes — buying question, the whole point | `bluetooth speaker` |
| "Bentgo Box" | Yes — brand line | `Bentgo lunch box` |
| "Matt Van Horn" (CEO of June) | Yes — **and the keyword is the company's product, not the person** | `June Oven` |
| "Kanye West" | No — person/culture topic, buyer reviews are noise | — |
| "the 2026 election" | No — nothing to buy | — |

**Two mechanics that matter:**

1. **The keyword is yours to choose and is often not the topic.** Map person → company → product line using what you know plus what Step 0.55 surfaced. A "Matt Van Horn" run that searches Amazon for his name returns nothing; searching `June Oven` returns his company's product reviews, which is the actual signal.
2. **Phrase it as brand plus category, never bare brand.** A bare brand keyword lands on Amazon's ad-heavy page 1 and can miss the brand's own bestsellers — a live `Bentgo` search returned 57 competitor ads and missed the flagship, while `Bentgo lunch box` surfaced it. Say `Weber grill`, not `Weber`.

**`--search` is replace-not-add.** Passing `--search` narrows the run to exactly the sources listed, so include the full intended set: `--search reddit,x,youtube,amazon` — never a bare `--search amazon`, which would silently drop every other source.

**Cost and latency, so you can set expectations:** one credit for the product search plus one per review pull, 4 per typical run against a 5,000/month free tier. Review sampling adds roughly 30 seconds to 2 minutes at default depth. Quick depth pulls no reviews at all.

Store: `AMAZON_QUERY = {product keyword or empty}` — pass as `--amazon-query="{AMAZON_QUERY}"` and add `amazon` to `--search`.

**Skip this step if:** the CLI is unavailable, the topic has no consumer-product dimension, or the user set `EXCLUDE_SOURCES=amazon`.

---
