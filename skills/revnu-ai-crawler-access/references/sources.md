# Sources

Every platform fact in this skill, its references and `check_ai_crawlers.py`
was checked against these pages **as of 2026-11-05** unless the row says
otherwise. Vendors rewrite these pages; re-check before relying on one for a
decision.

## Crawler documentation

| Fact | Source | As of |
|---|---|---|
| OAI-SearchBot (ChatGPT search; opted-out sites not shown in search answers but may appear as navigational links), GPTBot (training), ChatGPT-User (user actions; "robots.txt rules may not apply"; not used for Search), settings independent, one crawl may serve both, ~24h to adjust, user agent strings, IP JSON files | https://developers.openai.com/api/docs/bots (redirect from platform.openai.com/docs/bots) | 2026-11-05 |
| ClaudeBot (training), Claude-User (user queries), Claude-SearchBot (search quality); robots.txt and Crawl-delay honored; per-subdomain; IP blocking not recommended; bots.json; `Claude-Agent` named for hosted browsers; `anthropic-ai` not listed; recognition of the aipref training signal since 2026-10-30, ClaudeBot rule takes priority | https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler | 2026-11-05 |
| PerplexityBot (search results; not for foundation-model training), Perplexity-User ("generally ignores robots.txt rules"), UA strings, IP JSON, changes up to 24h, match UA plus IP in WAF rules | https://docs.perplexity.ai/guides/bots | 2026-11-05 |
| Google-Extended: product token for Gemini training and grounding; "does not impact a site's inclusion in Google Search nor is it used as a ranking signal"; no separate HTTP user agent; Googlebot rules cover Search features; AIPREF `__usage_ai-training` support planned early 2027; Google-CloudVertexBot no effect on Search | https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers | 2026-11-05 |
| Google user-triggered fetchers (Google-Agent, Google-GeminiNotebook; Google-NotebookLM supported only until August 2026) "generally ignore robots.txt rules" | https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers | 2026-11-05 |
| AI Overviews/AI Mode: indexed and snippet-eligible, no extra requirements; controls are Googlebot robots rules plus nosnippet, data-nosnippet, max-snippet, noindex; Google-Extended separate | https://developers.google.com/search/docs/appearance/ai-features | 2026-11-05 |
| Search Console "Search generative AI control", site-wide, manages inclusion in AI Overviews and AI Mode (page undated; changelog entry 2026-10-21) | https://developers.google.com/search/docs/crawling-indexing/control-what-you-share and https://developers.google.com/search/updates | 2026-11-05 |
| Applebot (Spotlight, Siri, Safari; may train; follows Googlebot rules when not named; ignores crawl-delay; may render JS), Applebot-Extended (training opt-out; does not crawl; search unaffected; nosnippet for live-context use), verification | https://support.apple.com/en-us/119829 | 2026-11-05 |
| Meta-WebIndexer (Meta AI search citations), Meta-ExternalAgent (training/indexing), Meta-ExternalFetcher ("may bypass robots.txt"), facebookexternalhit, 24h robots cache, prefers robots.txt over NoAI tags | https://developers.facebook.com/docs/sharing/webmasters/web-crawlers/ | 2026-11-05 |
| CCBot user agent, robots.txt opt-out, fake-CCBot warning, IP JSON | https://commoncrawl.org/ccbot | 2026-11-05 |
| Bing NOARCHIVE (excluded from Bing Chat/Copilot answers and training) and NOCACHE (URL, title, snippet only); both tags = NOCACHE | https://blogs.bing.com/webmaster/september-2023/Announcing-new-options-for-webmasters-to-control-usage-of-their-content-in-Bing-Chat | 2026-11-05 (post dated 2023-09-22) |
| Bing AI Training and AI Grounding preferences, syntax, replaces NOARCHIVE/NOCACHE for training and grounding from 2027-02-01, transition dates to 2027-09-30, Bing search eligibility unchanged | https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/ | 2026-11-05 (post dated 2026-10-30) |
| `__usage_ai-training` token, example syntax, `*` never matches it, not a crawl directive, individual draft with no formal IETF standing | https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/ | 2026-11-05 |
| robots.txt group matching, longest match, allow on ties, 4xx/5xx handling, 5 redirects, 24h cache, 500 KiB | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-11-05 |
| Cloudflare Content Signals (`search`, `ai-input`, `ai-train`) are preferences in robots.txt; managed robots.txt sets `ai-train=no` | https://blog.cloudflare.com/content-signals-policy/ and https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/ | 2026-11-05 (via search results, not a full page read) |

## Could not verify (the skill says so where it matters)

- **OpenAI honoring `__usage_ai-training`.** The announcement
  (https://openai.com/index/helping-websites-express-ai-training-preferences/)
  returned 403 to our fetcher; the commitment is taken from search-result
  text quoting it. The OpenAI bots page read on 2026-11-05 did not mention it.
- **Bytespider.** ByteDance's page https://zhanzhang.toutiao.com/docs/intro/26899
  is titled "About Bytespider" but its content did not load. Purpose, user
  agent and robots.txt behaviour are unverified; the user agent in the
  script is the one widely reported by third parties.
- **Bing crawler verification and Copilot-in-guidelines wording.** Bing
  Webmaster help pages render client-side and returned only a title. The
  `bingbot.json` list, the Verify Bingbot tool and the Webmaster Guidelines'
  Copilot wording come from third-party summaries.
- **Claude-Agent.** Named on Anthropic's page; its own article was not found.
- **Exact user agent strings for Claude-SearchBot, ClaudeBot, Claude-User,
  Googlebot and Bingbot.** The vendors document the product tokens; the
  full strings in the script are built around those tokens. The token is
  what robots.txt and most bot rules match.
- **Whether AI crawlers other than Googlebot and Applebot render
  JavaScript.** No vendor page checked says either way.

## Ideas credited

- Splitting crawler advice by job and refusing to merge training and search
  access in one line: agricidaniel/claude-seo `seo-geo` (MIT).
- Warning that a named group replaces `*`, and checking the firewall layer
  separately from robots.txt: coreyhaines31/marketingskills `ai-seo` (MIT).
