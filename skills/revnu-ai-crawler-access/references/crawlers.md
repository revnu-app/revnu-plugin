# AI crawlers by job (as of 2026-11-05)

Each row is from the vendor's own documentation unless marked unverified.
URLs are in [sources.md](sources.md). Vendors change these pages; if a
decision depends on a row, re-open the source.

## Search: decides whether the site can be shown and cited

| Token | Owner | What it controls | Blocking it means | robots.txt |
|---|---|---|---|---|
| `OAI-SearchBot` | OpenAI | Sites shown in ChatGPT's search features | Not shown in ChatGPT search answers (may still appear as a navigational link) | Honored; ~24h to take effect |
| `Claude-SearchBot` | Anthropic | Indexing to improve Claude's search results | Content not indexed for Claude's search; less visible and less accurate there | Honored, plus `Crawl-delay` |
| `PerplexityBot` | Perplexity | Finding and linking sites in Perplexity search results; Perplexity says it is not used for foundation-model training | Not surfaced in Perplexity search results | Perplexity says to allow it in robots.txt to appear; changes up to 24h |
| `Googlebot` | Google | Google Search, including AI Overviews and AI Mode (a page must be indexed and snippet-eligible) | Out of Google Search and its AI features | Honored |
| `Bingbot` | Microsoft | Bing search; Copilot and Bing's AI answers use the same index | Out of Bing and, with it, Copilot answers | Honored |
| `Applebot` | Apple | Spotlight, Siri and Safari search; Apple says the data may also train its models | Out of Apple search features | Honored; if Applebot isn't named but Googlebot is, it follows Googlebot's rules; ignores crawl-delay |
| `Meta-WebIndexer` | Meta | Citing and linking content in Meta AI answers | Meta AI less able to cite the site | Honored |

## Training: decides whether content may train models

| Token | Owner | What it controls | Blocking it does NOT do | Notes |
|---|---|---|---|---|
| `GPTBot` | OpenAI | Content that may train OpenAI foundation models | Does not remove the site from ChatGPT search (`OAI-SearchBot` is separate; OpenAI says each setting is independent) | If both are allowed, OpenAI may use one crawl for both |
| `ClaudeBot` | Anthropic | Future content excluded from Anthropic training data | Does not affect Claude-SearchBot or Claude-User | Set per subdomain |
| `Google-Extended` | Google | Gemini training, and grounding in Gemini Apps and Vertex AI | Does not affect Google Search inclusion or ranking, and so not AI Overviews or AI Mode | robots.txt token only; Google has no `Google-Extended` user agent |
| `Applebot-Extended` | Apple | Whether Applebot-crawled pages train Apple's generative models | Pages stay in Spotlight, Siri and Safari search; Apple says it doesn't stop use as live context in answers (use `nosnippet` for that) | Token only; it never crawls |
| `Meta-ExternalAgent` | Meta | Training foundation models and indexing for Meta products | Not documented as affecting Meta-WebIndexer | |
| `CCBot` | Common Crawl | An open web archive that many model builders train on | Doesn't remove copies already in past crawls | Common Crawl warns that fake CCBot traffic exists; verify by IP |

## User-triggered: a person asked the assistant to open a page

| Token | Owner | robots.txt per the vendor | Notes |
|---|---|---|---|
| `ChatGPT-User` | OpenAI | "may not apply" because a user started it | Not used to decide what appears in ChatGPT search |
| `Claude-User` | Anthropic | Honored (Anthropic says all its bots honor robots.txt) | Blocking it stops Claude retrieving the page for a user's question |
| `Perplexity-User` | Perplexity | "generally ignores" robots.txt | Doesn't crawl or collect training data |
| `Meta-ExternalFetcher` | Meta | "may bypass" robots.txt | Fetches single links on request, including agentic tasks |
| `Google-Agent`, `Google-GeminiNotebook` | Google | Google's user-triggered fetchers "generally ignore" robots.txt | Not checked by the script; listed so a log line isn't a surprise |

Anthropic also names `Claude-Agent` for its hosted browsers, documented in a
separate article not reviewed here (unverified). `anthropic-ai` is not on
Anthropic's current page; don't recommend rules for it.

## Unverified

| Token | Owner | Status |
|---|---|---|
| `Bytespider` | ByteDance | ByteDance's Chinese webmaster page titled "About Bytespider" exists, but its content could not be read from here. Purpose and robots.txt behaviour are unverified. Third-party server-log reports say it often ignores robots.txt. If it matters, block it at the CDN as well. |

## Signals that are not per-crawler

- **`__usage_ai-training`**, a shared robots.txt group for an AI-training
  preference, defined in an individual IETF draft from 2026-10-30 (Anthropic
  author; no formal IETF standing yet). Anthropic recognises it since
  2026-10-30, and a rule naming ClaudeBot takes priority. OpenAI announced
  it will honor it (the announcement page could not be fetched from here;
  seen via search). Microsoft will honor it from 2027-02-01, and Google says
  it plans to support it in early 2027. The draft says `User-agent: *` never
  counts as this token, and it is not a crawl directive.
- **Bing AI preferences** (announced 2026-10-30): from 2027-02-01 Bing reads
  `ai-training:disallow` (meta `name="Bingbot"`, `X-Robots-Tag: Bingbot: ...`
  or the shared robots token) and `ai-grounding:disallow` or
  `ai-grounding:disallowextended` (page level only; no robots.txt form).
  These replace `NOARCHIVE`/`NOCACHE` for training and grounding; after
  2027-03-01 those two tags stop being read for that purpose. Until then,
  `NOARCHIVE` keeps a page out of Copilot answers and `NOCACHE` limits it to
  URL, title and snippet. Neither preference changes eligibility for normal
  Bing results.
- **Google Search generative AI control**: a site-wide setting in Search
  Console that manages inclusion in AI Overviews and AI Mode. Page-level
  limits stay `nosnippet`, `data-nosnippet`, `max-snippet` and `noindex`.
- **`Content-Signal:` lines** (Cloudflare's Content Signals Policy): state
  `search`, `ai-input` and `ai-train` preferences inside robots.txt. They are
  preferences, not blocks. Cloudflare's managed robots.txt adds
  `ai-train=no`. No AI vendor page checked here says it reads them.
- **`noai` / `noimageai` meta values**: not documented by any vendor checked.
  Meta says it prefers standard robots.txt over such tags.

## How robots.txt is read

RFC 9309, which the major crawlers follow:

- A crawler uses the group whose `User-agent` matches its token
  (case-insensitive). Several groups for the same token are merged. Only if no
  group names it does it fall back to `User-agent: *`. A named group therefore
  replaces the `*` rules for that crawler.
- Within the group, the longest matching path wins; if an `Allow` and a
  `Disallow` match equally, `Allow` wins. `*` matches any run of characters
  and `$` anchors the end. No matching rule means allowed.
- No robots.txt (any 4xx) means everything is allowed. A 5xx or network
  failure means a compliant crawler assumes everything is disallowed, which
  makes a flaky robots.txt endpoint a quiet way to vanish.
- Crawlers follow at least five redirects for robots.txt, may cache it for up
  to 24 hours and read at least the first 500 KiB.
- `/robots.txt` itself is always allowed.

## Verifying a real crawler in logs

User agents are easy to fake. Match the source IP against the vendor list:
OpenAI `openai.com/searchbot.json`, `gptbot.json`, `chatgpt-user.json`;
Anthropic `claude.com/crawling/bots.json`; Perplexity
`perplexity.ai/perplexitybot.json`, `perplexity-user.json`; Apple
`search.developer.apple.com/applebot.json` or reverse DNS
`*.applebot.apple.com`; Common Crawl `index.commoncrawl.org/ccbot.json`;
Google: reverse DNS or the IP ranges Google publishes for its crawlers
and fetchers (its crawler docs link them). For Bing, third-party guides point to a `bingbot.json` list and a
Verify Bingbot tool in Bing Webmaster Tools; Bing's help pages could not be
read from here, so treat that as unverified.
