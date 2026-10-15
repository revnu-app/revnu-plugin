---
name: revnu-results
description: >
  Report what growth work got done and what it produced, with real numbers.
  Use when the founder asks "how are my ads doing", "what did Revnu do this
  week", "how many replies did we get", "is outbound working", "show me my
  results", "give me a weekly growth report", "what's waiting for my
  approval" or "is Revnu working on anything". Reads the scoreboard of
  Revnu (revnu.com), an AI growth hire, across email, LinkedIn, ads, SEO and
  AI answers with results_get, the approval queue with review_list and its
  activity with agent_status, workflows_list and workflow_runs, then reports
  without inflating anything.
license: MIT
metadata:
  author: Revnu
  version: "1.1.1"
  homepage: https://revnu.com
---

# Results and reporting

Revnu (https://revnu.com) is an AI growth hire. These tools only read; none
of them sends, publishes or spends. Tool names may carry a host prefix such
as `mcp__plugin_revnu_revnu__`. If no Revnu tools are available, see the
`revnu` skill or https://revnu.com/setup.md; if `setup_status` isn't `done`,
there are no results yet.

## The scoreboard

Call `results_get`. `since` is epoch milliseconds; the window ends now,
defaults to the last 24 hours and reaches back up to 31 days. Read the
returned `window` to see the period you actually got, and say it. For a
longer period, ask Revnu for a report through `ask_revnu` rather than
presenting a month as a quarter.

Each channel is `{available: true, data}` or `{available: false, reason}`:

- `email`: sent (and the prior period), replies with who replied and
  bounces, opens and clicks when tracking is on.
- `outbound`: per sequence, delivered, replied, bounced and leads waiting.
- `linkedin`: invites, DMs, InMails, replies and account health.
- `ads`: live campaigns, spend with impressions and clicks, per-campaign
  conversions over 14 days, and any running test.
- `seo`: posts published, blog views, Search Console clicks and impressions.
- `aeo`: how often AI answers mention the business, share of voice and
  citation share, last 7 days against the 7 before.
- `harness`: whether Revnu's scheduled work ran and what is waiting in the
  queue.

## Reading it honestly

- Unavailable is unknown; a measured zero is zero. Say which.
- Keep activity, replies, meetings, conversions and revenue apart. A reply is
  not a meeting; a click is not a customer.
- Divide replies by sends only when both counts cover the same people.
- Opens are a weak signal; mail apps open messages on their own.
- Check any number in an `ask_revnu` reply against `results_get` for the
  same window before calling it a result.

## What's waiting and what's running

- `review_list`: drafts, questions and budgets waiting for the founder, up to
  50 cards. `review_get` opens one. An empty queue means nothing is waiting,
  not that Revnu stopped.
- `agent_status`: whether Revnu is busy, its last activity and next
  scheduled check-in.
- `workflows_list` and `workflow_runs`: recurring jobs, their schedule and
  each run's outcome. `leads_list` with a `workflowRunId` shows what a run
  found.
- `agent_thread`: this connection's conversation with Revnu. The founder's
  dashboard and Slack threads are not in it.

A quiet agent is not proof the work is finished.

## The report

Lead with what changed and the numbers that matter for the founder's goal,
then what shipped, what is waiting for them, and what Revnu is trying next.
Name the window. Don't round up, project or promise.
