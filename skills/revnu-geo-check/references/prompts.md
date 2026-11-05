# Building the prompt set

The prompt set is the measuring instrument. Keep it small, buyer-shaped and
stable, so a later run can be compared with this one.

## Families

Write 8-12 real prompts, spread across these families. Phrase them the way
a buyer types into a chat box: full sentences, the buyer's situation, no
marketing words.

| Family | What it measures | Example for an invoicing tool for freelance designers |
|---|---|---|
| category | Does the business make the shortlist when someone names the need? | "What's the best invoicing software for a freelance designer?" |
| problem | Does it come up when the buyer describes the pain, not the category? | "I keep chasing clients for late payments. How do freelancers deal with this?" |
| comparison | Is it described fairly next to a named rival? | "Acme vs FreshBooks for a one-person design studio" |
| alternatives | Does it appear when someone is leaving a competitor? | "Good alternatives to FreshBooks that are cheaper?" |
| brand | What do answers say when asked about the business directly? | "How much does Acme cost and is it good for freelancers?" |

Rules of thumb:

- Brand name only in the comparison and brand families. Category, problem
  and alternatives prompts measure discovery; naming the brand there makes
  the result meaningless.
- At least 2 prompts each in category and problem, since those are where
  new buyers come from. Brand prompts feed the claim review more than the
  rates.
- Include the buyer's constraints that change the answer (team size,
  budget, region, industry) when real buyers state them.
- Use the user's knowledge of real buyer questions (sales calls, support
  tickets, search terms) over invented ones. Mark invented prompts as such.
- Don't write 30 near-duplicates of one question. Variety across families
  beats volume inside one.

## Controls

Two extra prompts, run exactly like the others:

- **Positive control:** names the business with its domain, e.g. "What is
  Acme (acme.com)?" Expected: mentioned in every run. If it isn't, either
  the name matching in the tally is wrong (answers write "ACME Inc." or the
  product name) or this surface doesn't know the business at all, which is
  itself a finding. Fix matching before trusting any other number.
- **Negative control:** an unrelated category where the business should
  never appear, e.g. "Best hiking boots for wide feet?" Expected: zero
  mentions. A hit means the brand name collides with a common word or
  another company, so mention counts are inflated; tighten the names passed
  to the tally and read those answers.

Controls are reported separately and never counted in the rates.

## Saving the set

Store prompts with stable ids so runs can be joined later:

```json
{
  "version": 1,
  "created": "2026-11-05",
  "brand": {"name": "Acme", "aliases": ["Acme Invoicing"], "domain": "acme.com"},
  "competitors": [{"name": "FreshBooks", "domain": "freshbooks.com"}],
  "prompts": [
    {"id": "cat-1", "family": "category", "text": "What's the best invoicing software for a freelance designer?"},
    {"id": "ctl-pos", "family": "control", "control": "positive", "text": "What is Acme (acme.com)?"},
    {"id": "ctl-neg", "family": "control", "control": "negative", "text": "Best hiking boots for wide feet?"}
  ]
}
```

When a prompt is edited, give it a new id and bump `version`, so old and new
results aren't mixed. Compare runs only on ids both runs share.

## Runs and what a number can carry

- 3 runs per prompt per surface is the floor for saying anything about a
  prompt. Per-prompt results from 3 runs are still rough; the family and
  overall rates, pooled over many runs, are the numbers to lead with.
- 5 runs when the user is asking "how often", or when a result sits near a
  decision (1/3 or 2/3).
- The tally prints a 95% interval. With 6 runs, 2 mentions is "somewhere
  between roughly 10% and 70%". Say that plainly instead of "33%".
- Treat a change between two runs as real only when the intervals don't
  overlap, or when the same direction repeats over several weekly runs.
  Otherwise report it as "no clear change".
