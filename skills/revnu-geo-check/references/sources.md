# Sources

Checked **as of 2026-11-05**. API shapes, model names and prices change
often; the skill tells the agent to re-open these pages before calling.

| Fact | Source | As of |
|---|---|---|
| OpenAI Responses API `web_search` tool: request shape, `tool_choice: "required"` to force a search, `user_location`, `url_citation` annotations, `include: ["web_search_call.action.sources"]` for all consulted URLs; the doc makes no claim of parity with ChatGPT search | https://developers.openai.com/api/docs/guides/tools-web-search | 2026-11-05 |
| OpenAI built-in tool pricing | https://developers.openai.com/api/docs/pricing#built-in-tools | link checked 2026-11-05; amounts not recorded here |
| Perplexity Agent API endpoint `https://api.perplexity.ai/v1/agent`, Bearer auth, `perplexity/sonar` described as "Perplexity's grounded search model", token prices $0.25 in / $2.50 out per 1M, `max_output_tokens`, `search_results` + `message` output with `[web:n]` markers | https://docs.perplexity.ai/docs/agent-api/models.md and https://docs.perplexity.ai/getting-started/quickstart | 2026-11-05 |
| Perplexity pricing page | https://docs.perplexity.ai/docs/getting-started/pricing.md | link from quickstart, 2026-11-05; per-request fees not recorded |
| Gemini Grounding with Google Search: Interactions endpoint, `x-goog-api-key`, `Api-Revision: 2026-05-20`, `tools: [{"type": "google_search"}]`, `url_citation` annotations, billing per search query for Gemini 3+, 5,000 free/month then $14 per 1,000, 1,500/day default cap | https://aistudio.google.com/docs/google-search | 2026-11-05 |
| Google AI Overviews and AI Mode are fed by Google Search systems; page must be indexed and snippet-eligible (context for why Gemini API grounding is not the same as AI Overviews) | https://developers.google.com/search/docs/appearance/ai-features | 2026-11-05 |
| ChatGPT search inclusion is controlled by OAI-SearchBot (context for why a site blocked there won't be cited) | https://developers.openai.com/api/docs/bots | 2026-11-05 |

## Could not verify

- **How closely any API result matches the consumer app** (ChatGPT,
  Perplexity, Gemini, Copilot, AI Overviews). No provider documents parity,
  so the skill treats them as different surfaces.
- **Which search index or ranking ChatGPT or Perplexity use for grounding.**
  Not documented in the pages checked; the skill doesn't name one.
- **Exact OpenAI and Perplexity per-request search fees.** The skill sends
  the agent to the pricing pages instead of quoting amounts.
- **Microsoft Copilot and Google AI Overviews via API.** No public API
  that reproduces either was checked; they are sampled only through answers
  the user pastes.

## Method notes (own reasoning, not platform facts)

- Positive and negative controls, repeated runs, Wilson 95% intervals and
  comparing only shared prompt ids are standard measurement practice, not
  platform claims.
- Ideas credited: diagnostic control prompts and a versioned prompt set
  (coreyhaines31/marketingskills `ai-seo` prompt-portfolio reference, MIT);
  logging one row per claim made about the business, including unprompted
  ones (same repo's answer-accuracy reference, MIT); reporting a platform as
  "not measured" unless a tool measured it (agricidaniel/claude-seo, MIT).
