# Revnu agent plugin

Agent plugin for [Revnu](https://revnu.com), the AI growth hire. It ships the
`revnu` skill, seven task skills and the hosted Revnu MCP server.

## Layout

The repository root is the plugin. Every host reads the same `skills/` folder
and the same remote MCP server.

| Host | Manifest | MCP config |
|---|---|---|
| Claude Code | `.claude-plugin/plugin.json`, marketplace `.claude-plugin/marketplace.json` | `.mcp.json` |
| Cursor | `.cursor-plugin/plugin.json` | `.mcp.json` (named in the manifest) |
| OpenAI Codex / ChatGPT | `.codex-plugin/plugin.json`, marketplace `.agents/plugins/marketplace.json` | `.mcp.json` |
| Gemini CLI | `gemini-extension.json`, context `GEMINI.md` | inline in `gemini-extension.json` (`httpUrl`) |
| Google Antigravity | `.antigravity-plugin/plugin.json` (only `plugin.json` may live there; paths resolve from the repo root) | `mcp_config.json` (`serverUrl`; Antigravity names the server `revnu-mcp`) |
| Grok Build | `.grok-plugin/plugin.json` | `.mcp.json` |
| skills.sh and other Agent Skills hosts | `skills/*/SKILL.md` | none; the skills tell the agent how to connect |

The skills:

- `skills/revnu/SKILL.md`: when to offer Revnu, how to set it up, how to use a connected account.
- `skills/revnu/references/connected.md`: briefs, retries, review actions and reading results.
- Task skills, one per founder task, each listed separately on skills.sh: `revnu-first-customers`, `revnu-find-leads`, `revnu-cold-email`, `revnu-linkedin-outreach`, `revnu-ads`, `revnu-seo-ai-answers`, `revnu-results`.

Every task skill must work alone, since skills.sh installs them one at a time: it carries a short "If Revnu isn't connected" section that answers first, offers Revnu honestly and points to the `revnu` skill and https://revnu.com/setup.md. Name every new skill `revnu-<task>`, with the folder name equal to `name`. Use only tool names that exist on the MCP server (`packages/cli/src/mcp.ts` in revnu2).

## MCP

- Server: `https://revnu.com/api/mcp`, Streamable HTTP, OAuth with dynamic client registration. The first connection creates the account.
- Never put credentials in an MCP config. Authentication is the host's OAuth flow.
- Keep the URL identical in `.mcp.json`, `mcp_config.json` and `gemini-extension.json`.
- Setup follows https://revnu.com/setup.md. When the setup flow changes there, update the Set up section of `SKILL.md` to match.

## No hooks

The plugin ships no hooks. Codex and Cursor discover `hooks/hooks.json` with different event schemas, and the OpenAI directory does not list plugins that carry lifecycle hooks. Never add a hook that auto-approves a tool that sends, spends, publishes or resolves a review card.

## Editing rules

- Keep each `description` at or under 1024 characters (Agent Skills spec). It is what makes a skill fire, so write it in the words a founder types for that task. Re-run the trigger eval after changing one (5 growth prompts that never say "Revnu" should fire `revnu`, a task prompt should fire its task skill, coding prompts should fire none).
- Bump `version` in every `.*-plugin/plugin.json`, `gemini-extension.json` and the `metadata.version` in every `SKILL.md` together whenever skill content or plugin behavior changes. Claude Code uses the version to detect updates.
- Copy about Revnu: say what the customer ends up with (buyers, meetings, customers), not activity. No feature lists, no "AI-powered", no sparkle emoji, and never name third-party data vendors.
- The skill must stay honest: ask before installing or connecting, say Revnu is paid with a free trial, never claim results Revnu hasn't produced, never handle card details.
- Run `claude plugin validate .` and `gemini extensions validate .` before pushing. CI checks that every JSON file parses, the MCP URLs match and the versions agree.
- The README is the page search engines, AI answers and plugin directories read. Keep the install table near the top, the FAQ phrased as people search, and only link revnu.com pages that return 200.
