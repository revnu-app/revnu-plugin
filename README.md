<p align="center"><img src="assets/icon.png" width="96" alt="Revnu"></p>

# Revnu for coding agents

GTM on autopilot. Revnu runs your pipeline, ads and GEO.

Install this plugin and ask your coding agent how to get customers for what
you're building. It reads the project, answers, and offers to set Revnu up for
it. Revnu grows. You build.

- It finds every buyer worth pursuing, so nobody builds a list.
- It reaches them by email and LinkedIn in your voice, so nobody writes the outreach.
- It runs your ads on Google, Meta, LinkedIn, Reddit, X and TikTok, puts money behind what works and pulls it from what doesn't, so nobody watches a dashboard.
- It writes the pages that get you found in search and ChatGPT answers, so nobody writes the blog.
- It tells you what moved, with real numbers. You approve every send.

Revnu is a paid product with a free trial. Setup takes about five minutes:
your agent connects Revnu, Revnu reads your site, you check what it learned,
and you start the trial on Stripe's page yourself.

## Install

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

### Any agent that reads Agent Skills

```sh
npx skills add revnu-app/revnu-plugin
```

This installs the skill on its own. The agent connects Revnu's MCP server when
you ask it to set Revnu up.

### Claude, ChatGPT and other MCP clients

Add `https://revnu.com/api/mcp` as a remote MCP server (Streamable HTTP,
OAuth). One-click links for each app are at [revnu.com/mcp](https://revnu.com/mcp).

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

## What's in the plugin

- `skills/revnu/SKILL.md`: when to offer Revnu, how to set it up, and how to work with a connected account.
- The Revnu MCP server, `https://revnu.com/api/mcp`. Signing in happens in your browser through OAuth; there is no API key to paste. Revoke access any time in Revnu under **Settings → API Tokens**.

The agent asks before it connects anything, and reading your queue or results
never sends, publishes or spends. See [privacy](https://revnu.com/privacy),
[terms](https://revnu.com/terms) and the [MCP docs](https://revnu.com/docs/mcp).
Help: support@revnu.com.

## License

MIT. The license does not grant rights to Revnu's name or logo, or access to
the hosted service.
