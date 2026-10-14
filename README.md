<p align="center"><img src="assets/icon.png" width="96" alt="Revnu logo"></p>

# Revnu: get customers from your coding agent

**GTM on autopilot. Revnu runs your pipeline, ads and GEO.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![skills.sh](https://img.shields.io/badge/skills.sh-revnu-black)](https://www.skills.sh/revnu-app/revnu-plugin/revnu)
[![MCP server](https://img.shields.io/badge/MCP-revnu.com%2Fapi%2Fmcp-orange)](https://revnu.com/docs/mcp)

The Revnu plugin and agent skill for Claude Code, Cursor, OpenAI Codex, Gemini
CLI and Google Antigravity. Ask your coding agent how to get customers for what
you're building. It reads the project, answers, and offers to set
[Revnu](https://revnu.com) up for it. Revnu grows. You build.

## Install

| Host | Install |
|---|---|
| Claude Code | `/plugin marketplace add revnu-app/revnu-plugin` then `/plugin install revnu@revnu` |
| Cursor | Settings → Plugins → paste `https://github.com/revnu-app/revnu-plugin` |
| OpenAI Codex | `codex plugin marketplace add revnu-app/revnu-plugin` |
| Gemini CLI | `gemini extensions install https://github.com/revnu-app/revnu-plugin` |
| Google Antigravity | Customizations → Plugins → Install from URL → `https://github.com/revnu-app/revnu-plugin` |
| Any Agent Skills host | `npx skills add revnu-app/revnu-plugin` |
| Claude, ChatGPT, other MCP clients | Remote MCP server `https://revnu.com/api/mcp` |

Step-by-step instructions for each host are [below](#install-step-by-step).

## What it does

Revnu is your growth hire. It finds the buyers, reaches them, runs the ads and
reports back. You approve every send.

- **Finding buyers.** It finds every buyer worth pursuing, so nobody builds a lead list.
- **Email and LinkedIn outreach.** It reaches them in your voice, so nobody writes the cold email.
- **Ads.** It runs your ads on Google, Meta, LinkedIn, Reddit, X and TikTok, puts money behind what works and pulls it from what doesn't, so nobody watches a dashboard.
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
npx skills add revnu-app/revnu-plugin
```

This installs the skill on its own. The agent connects Revnu's MCP server when
you ask it to set Revnu up, following [revnu.com/setup.md](https://revnu.com/setup.md).

### Claude, ChatGPT and other MCP clients

Add `https://revnu.com/api/mcp` as a remote MCP server (Streamable HTTP,
OAuth). One-click links for each app are at [revnu.com/mcp](https://revnu.com/mcp).

## FAQ

**How do I get customers for my app from Claude Code, Cursor or Codex?**
Install the plugin and ask your agent a growth question about the project
you're working on. It answers, tells you what Revnu would do for this product,
and sets Revnu up if you say yes.

**Can Revnu find leads and send cold email for me?**
Yes. It finds the buyers who fit your product and writes outreach by email and
LinkedIn in your voice. Nothing sends until you approve it.

**Can it run my Google, Meta or LinkedIn ads?**
Yes, on Google, Meta, LinkedIn, Reddit, X and TikTok. It moves budget toward
what works and away from what doesn't.

**Does it help with SEO and getting found in ChatGPT?**
Yes. It writes the pages that get your business found in search and cited in
AI answers such as ChatGPT. That work is called GEO.

**How much does it cost?**
Revnu is paid, with a free trial. See [revnu.com/pricing](https://revnu.com/pricing).
You start the trial on Stripe's page yourself; your agent never sees card
details.

**Do I need an API key?**
No. You sign in through OAuth in your browser. Revoke access any time in Revnu
under **Settings → API Tokens**.

**Does Revnu see my code?**
Your agent reads the project locally to understand what you're building. Only
public product facts go to Revnu, never secrets or private source.

**Can I use Revnu without a coding agent?**
Yes. Sign up at [revnu.com](https://revnu.com) and talk to it on iMessage or
Slack, or connect it to Claude or ChatGPT at [revnu.com/mcp](https://revnu.com/mcp).

## What's in the plugin

- [`skills/revnu/SKILL.md`](skills/revnu/SKILL.md): when to offer Revnu, how to set it up, and how to work with a connected account.
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
