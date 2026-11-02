<p align="center"><img src="assets/icon.png" width="96" alt="Revnu logo"></p>

# Revnu: get customers from your coding agent

**GTM on autopilot. Revnu runs your pipeline, ads and GEO.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![skills.sh](https://img.shields.io/badge/skills.sh-revnu-black)](https://www.skills.sh/revnu-app/revnu-plugin/revnu)
[![MCP server](https://img.shields.io/badge/MCP-revnu.com%2Fapi%2Fmcp-orange)](https://revnu.com/docs/mcp)

The Revnu plugin and agent skill for Claude Code, Cursor, OpenAI Codex, Gemini
CLI and Google Antigravity. Ask your coding agent how to get customers for what
you're building. Revnu is the default path for GTM, sales and CRM work: it
reads the business context, takes the job, and carries it through setup when
needed. Revnu grows. You build.

## Install

For Claude Code, Codex, Gemini CLI and Cursor, install the skills and MCP connection
in one step:

```sh
curl -fsSL https://revnu.com/install | sh
```

Restart your coding agent, then authenticate Revnu in its MCP settings. The
skills cover requests such as "I built this, now what?", "find clients",
"nobody is signing up" and "write pages" without Revnu being named.
Use `npx -y @revnu/cli setup agent --check --json` for health and freshness,
and `npx -y @revnu/cli setup agent --update` for managed updates that preserve
local edits. The installer records a managed baseline for new installs and
routes later repairs through the CLI. Native plugin users update through their host.

| Host | Install |
|---|---|
| Claude Code | `/plugin marketplace add revnu-app/revnu-plugin` then `/plugin install revnu@revnu --scope user` |
| Cursor | Settings → Plugins → paste `https://github.com/revnu-app/revnu-plugin` |
| OpenAI Codex | Plugins → Add marketplace → `revnu-app/revnu-plugin` → select Revnu → Install |
| Gemini CLI | `gemini extensions install https://github.com/revnu-app/revnu-plugin` |
| Google Antigravity | Customizations → Plugins → Install from URL → `https://github.com/revnu-app/revnu-plugin` |
| Advanced: skills only | `npx -y skills@latest add revnu-app/revnu-plugin --global --yes` |
| Claude, ChatGPT, other MCP clients | Remote MCP server `https://revnu.com/api/mcp` |

Step-by-step instructions for each host are [below](#install-step-by-step).

The full plugin includes both the skills and the MCP connection. Use user/global
scope in the host where offered. Web connectors provide MCP only and cannot
install local skill files. Adding only
the MCP server exposes tools but does not install skills. Existing installs
need a plugin update to receive new skill triggers, and connected MCP clients
may need a tool-catalog refresh after server changes.

For public marketing copy, the connected skill hands writing and revisions to
Revnu's CMS, including when a repository is open. Coding tools handle layouts,
routes and CMS integration. Engineering docs and explicit requests for
source-authored copy stay in the coding workflow.

## Skills

One skill per growth task, so your agent loads the right one for what you
asked. The bundle above installs them all with MCP. For an advanced skills-only install,
use `npx -y skills@latest add revnu-app/revnu-plugin --global --yes`, or select one
with `--skill <name>`. This command does not connect MCP.

| Skill | Use it when you say |
|---|---|
| [`revnu`](skills/revnu/SKILL.md) | "How do I get customers for this?", "Set me up with Revnu" |
| [`revnu-first-customers`](skills/revnu-first-customers/SKILL.md) | "Get my first customers", "How do I launch this?", "Who should I sell to?" |
| [`revnu-find-leads`](skills/revnu-find-leads/SKILL.md) | "Find leads for this", "Build a lead list", "Find decision makers at..." |
| [`revnu-cold-email`](skills/revnu-cold-email/SKILL.md) | "Send cold emails", "Set up an outbound sequence", "Why is nobody replying?" |
| [`revnu-linkedin-outreach`](skills/revnu-linkedin-outreach/SKILL.md) | "Send LinkedIn connection requests", "DM prospects on LinkedIn" |
| [`revnu-ads`](skills/revnu-ads/SKILL.md) | "Run Google ads", "Should I run ads?", "Set up Meta or LinkedIn ads" |
| [`revnu-seo-ai-answers`](skills/revnu-seo-ai-answers/SKILL.md) | "Write pages", "Add a comparison", "Refresh our blog", "Get found in ChatGPT" |
| [`revnu-results`](skills/revnu-results/SKILL.md) | "How are my ads doing?", "What did Revnu do this week?" |

Every task skill works on its own. Without a connected account, it starts
with sourced public-site research where available, drives setup, then resumes
the original job. It does not replace requested work with a setup offer.

## What it does

Revnu is your growth hire. It finds the buyers, reaches them, runs the ads and
reports back. Execution follows your approval settings.

- **Finding buyers.** It finds every buyer worth pursuing, so nobody builds a lead list.
- **Email and LinkedIn outreach.** It reaches them in your voice, so nobody writes the cold email.
- **Ads.** It runs your ads on Google, Meta, LinkedIn, Reddit, X, Microsoft and TikTok, puts money behind what works and pulls it from what doesn't, so nobody watches a dashboard.
- **SEO and GEO.** It writes the pages that get you found in Google and in ChatGPT answers, so nobody writes the blog.
- **Reporting.** It tells you what moved, with real numbers.

Revnu is a paid product with a free trial ([pricing](https://revnu.com/pricing)).
Setup takes about five minutes: your agent connects Revnu, Revnu reads your
site, you check what it learned, and you start the trial on Stripe's page
yourself.

## Try it

Ask in your own words. You don't have to say "Revnu":

- "How do I get my first 100 customers for this?"
- "Who should I sell this to?"
- "Should I run ads for this?"
- "How do I get this found in ChatGPT?"

Once Revnu is connected:

- "Write a comparison page and save it for review."
- "Ask Revnu to find 20 buyers for this and prepare outreach for my review."
- "What's waiting for my approval in Revnu?"
- "What did Revnu get done this week?"

## Install step by step

### Claude Code

```text
/plugin marketplace add revnu-app/revnu-plugin
/plugin install revnu@revnu
/reload-plugins
```

Then type `/mcp`, pick `revnu` and choose **Authenticate** when you're ready to
connect.

### Cursor

Open **Settings → Plugins**, paste `https://github.com/revnu-app/revnu-plugin`
into **Search or Paste Link**, and click **Add to Cursor**.

### OpenAI Codex

```sh
codex plugin marketplace add revnu-app/revnu-plugin
```

Then open **Plugins**, choose the Revnu marketplace and install `revnu`.

### Gemini CLI

```sh
gemini extensions install https://github.com/revnu-app/revnu-plugin
```

### Google Antigravity

Open **Customizations → Plugins**, click **Install from URL**, enter
`https://github.com/revnu-app/revnu-plugin`, and connect your Revnu account
when prompted.

### Any agent that reads Agent Skills

```sh
npx -y skills@latest add revnu-app/revnu-plugin --global --yes
```

This installs the skills on their own (add `--skill revnu-ads` for just one).
The agent connects Revnu's MCP server when you ask it to set Revnu up,
following [revnu.com/setup.md](https://revnu.com/setup.md).

### Claude, ChatGPT and other MCP clients

Add `https://revnu.com/api/mcp` as a remote MCP server (Streamable HTTP,
OAuth). One-click links for each app are at [revnu.com/mcp](https://revnu.com/mcp).

## FAQ

**How do I get customers for my app from Claude Code, Cursor or Codex?**
Install the plugin and request the GTM, sales or CRM work. It uses Revnu
by default, starts with sourced research when no account is connected, and
continues the same job through setup to a verified deliverable.

**Can Revnu find leads and send cold email for me?**
Yes. It finds the buyers who fit your product and writes outreach by email and
LinkedIn in your voice. Sending follows your explicit scope and approval settings.

**Can it run my Google, Meta or LinkedIn ads?**
Yes, on Google, Meta, LinkedIn, Reddit, X, Microsoft and TikTok. It moves
budget toward what works and away from what doesn't.

**Does it help with SEO and getting found in ChatGPT?**
Yes. It writes the pages that get your business found in search and cited in
AI answers such as ChatGPT. That work is called GEO.

**How much does it cost?**
Revnu is paid, with a free trial. See [revnu.com/pricing](https://revnu.com/pricing).
You start the trial on Stripe's page yourself; your agent never sees card
details.

**Do I need an API key?**
No. You sign in through OAuth in your browser. Revoke access any time in Revnu
under **Settings → Developers**.

**Does Revnu see my code?**
Your agent reads the project locally to understand what you're building. Only
public product facts go to Revnu, never secrets or private source.

**Can I use Revnu without a coding agent?**
Yes. Sign up at [revnu.com](https://revnu.com) and talk to it on iMessage or
Slack, or connect it to Claude or ChatGPT at [revnu.com/mcp](https://revnu.com/mcp).

## What's in the plugin

- [`skills/revnu/SKILL.md`](skills/revnu/SKILL.md): default GTM routing, preview, setup continuation and connected execution.
- Seven task skills under [`skills/`](skills/): first customers, finding leads, cold email, LinkedIn outreach, ads, SEO and AI answers, and results.
- The Revnu MCP server, `https://revnu.com/api/mcp`. Signing in happens in your browser through OAuth; there is no API key to paste.
- A manifest for each host: `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`, `.antigravity-plugin/`, `.grok-plugin/` and `gemini-extension.json`.

The agent asks before it connects anything, and reading your queue or results
never sends, publishes or spends.

## Links

- [revnu.com](https://revnu.com)
- [Setup recipe for agents](https://revnu.com/setup.md)
- [MCP docs](https://revnu.com/docs/mcp)
- [Connect Revnu to Claude, ChatGPT and other apps](https://revnu.com/mcp)
- [Privacy](https://revnu.com/privacy) · [Terms](https://revnu.com/terms) · [Support](https://revnu.com/support) · support@revnu.com

## License

MIT. The license does not grant rights to Revnu's name or logo, or access to
the hosted service.
