# Surfaces: how to call each, and what it stands for

Request shapes below were read from the provider docs on 2026-11-05. APIs
and model names change often: **before the first call, open the doc link
and confirm the endpoint, a current model name and the pricing.** If the
shape differs, follow the doc, not this file.

Never print, echo, log or paste a key. Pass it from the environment in the
header only. Check presence with `[ -n "$VAR" ] && echo set || echo missing`.

## 1. Host web search (no key, no cost beyond the host)

The host's own search tool (for example WebSearch in Claude Code, or a
search/browse tool in another agent).

- Run each prompt text as the query. Record the result URLs as `citations`
  and the titles and snippets, joined, as `answer`.
- **Stands for:** whether a web search for the buyer's question surfaces the
  business's pages, and which third-party pages it surfaces. That's useful
  because the AI products in this check ground answers in web search, but
  the host's search engine is not necessarily the index or ranking any of
  them uses.
- **Does not stand for:** any AI product's answer. Label the metric "search
  presence". If you also write a summary from those results, that is this
  host model's answer and must be labelled as such.
- Many host search tools are region-locked or cached; note the region if the
  tool says.

## 2. OpenAI API with web search

Doc: https://developers.openai.com/api/docs/guides/tools-web-search.
Pricing: https://developers.openai.com/api/docs/pricing#built-in-tools (a
per-call tool fee on top of model tokens). Key: `OPENAI_API_KEY`.

```bash
curl -s https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "<current model from the doc>",
       "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "US"}}],
       "tool_choice": "required",
       "input": "<prompt text>"}'
```

- `tool_choice: "required"` forces a search; with `auto` the model may answer
  from memory, which is a different measurement. Pick one per run set and
  record it.
- Set `user_location` to the buyer's market; record it.
- Answer text: the `message` item's `content[0].text`. Citations:
  `content[0].annotations` entries of type `url_citation` (`url`, `title`).
  Adding `"include": ["web_search_call.action.sources"]` returns every URL
  consulted, which is usually more than those cited; log both if you use it,
  in separate fields.
- **Stands for:** an OpenAI model answering with OpenAI's search tool.
  **Does not stand for:** the ChatGPT app, which has its own model routing,
  system prompt, memory and personalisation. The doc doesn't claim parity.

## 3. Perplexity API (Sonar)

Doc: https://docs.perplexity.ai/docs/agent-api/models.md and
https://docs.perplexity.ai/getting-started/quickstart. Pricing:
https://docs.perplexity.ai/docs/getting-started/pricing.md. Key:
`PERPLEXITY_API_KEY`.

```bash
curl -s https://api.perplexity.ai/v1/agent \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "perplexity/sonar", "input": "<prompt text>", "max_output_tokens": 800}'
```

- The models page lists `perplexity/sonar` as Perplexity's grounded search
  model (as of 2026-11-05: $0.25 input and $2.50 output per 1M tokens; check
  the pricing page for any per-request fees).
- Output: a `search_results` item (`results[]` with `id`, `url`, `title`)
  and a `message` item whose text carries markers like `[web:1]` that map to
  result ids. Log the URLs of the results actually referenced as
  `citations`; if markers are absent, log all results and say so.
- **Stands for:** Perplexity's grounded model through the API.
  **Does not stand for:** the Perplexity app's default experience, which may
  use other models and features.

## 4. Gemini API with Grounding with Google Search

Doc: https://aistudio.google.com/docs/google-search (redirect from
ai.google.dev/gemini-api/docs/google-search). Key: `GEMINI_API_KEY`.

```bash
curl -s https://generativelanguage.googleapis.com/v1beta/interactions \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -H "Api-Revision: 2026-05-20" \
  -d '{"model": "<current model from the doc>", "input": "<prompt text>",
       "tools": [{"type": "google_search"}]}'
```

- Billing (as of 2026-11-05, Gemini 3 and newer): per search query the model
  runs, not per prompt; 5,000 free search requests a month shared across
  those models, then $14 per 1,000; default cap 1,500 requests a day per
  project on the paid tier. Plus model tokens.
- Citations: `url_citation` annotations on the text in the `model_output`
  step; the queries it ran are in the `google_search_call` step.
- Google's terms set display requirements for grounded results and search
  suggestions. Read them before showing these results to anyone beyond the
  user running the check.
- **Stands for:** a Gemini model grounded on Google Search.
  **Does not stand for:** Google's AI Overviews or AI Mode, or the Gemini app.

## 5. Answers the user pastes from the apps

The only way this skill samples ChatGPT, the Perplexity app, Gemini, Copilot
or AI Overviews. Ask the user to:

- use a logged-out or fresh session, or say which account and whether memory
  is on;
- paste the full answer and the sources list for each run;
- run each prompt at least 3 times in fresh chats.

Log with `surface` set to the app name plus `-user-provided`. Report these
separately and say who collected them.

## Log format (one JSON object per line)

```json
{"surface": "openai-api", "model": "<model>", "date": "2026-11-05",
 "settings": {"tool_choice": "required", "country": "US"},
 "prompt_id": "cat-1", "family": "category", "control": null, "run": 2,
 "prompt": "What's the best invoicing software for a freelance designer?",
 "answer": "<full answer text>", "citations": ["https://..."],
 "error": null}
```

`control` is `null`, `"positive"` or `"negative"`. A failed call gets an
`error` string and no `answer`; `tally.py` skips it and prints the failure
count, which belongs in the report. `scripts/tally.py` reads `surface`, `prompt_id`, `family`,
`control`, `answer` and `citations`.

## Cost estimate, before asking

```
calls per surface = (real prompts + 2 controls) x runs
```

For each API surface, read the current per-call tool fee and token prices
from its pricing page, assume about 1-2k output tokens per answer, and give
the user one total with the arithmetic shown. If you can't find a price,
say so and give the call count alone.
