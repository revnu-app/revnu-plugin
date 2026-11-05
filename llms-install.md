# Installing Revnu

Revnu is a hosted MCP server at `https://revnu.com/api/mcp` (Streamable HTTP, OAuth). Nothing runs locally and there is no API key to paste.

## MCP clients that take a JSON config (Cline, Windsurf and others)

```json
{
  "mcpServers": {
    "revnu": {
      "type": "streamableHttp",
      "url": "https://revnu.com/api/mcp"
    }
  }
}
```

The first tool call opens a Revnu sign-in in the browser. Signing in with a new email creates the account. Revnu is paid (Pro is from $99 a month). The person handles any payment step themselves when setup asks for it; whether their offer starts with a free trial or needs a card up front depends on the offer. Until setup is finished a new account answers `setup_pending`, and the `setup_status` tool returns the next step.

## Claude Code, Codex, Gemini CLI and Cursor

`curl -fsSL https://revnu.com/install | sh` adds the MCP server and the Revnu skills to each of these that is installed. Per-host steps are in the [README](README.md#install).

## Without an account

`POST https://revnu.com/api/v1/preview` with `{"website": "<url>"}` starts researching the business and returns a `previewId` and a `poll` URL. Research runs in the background: `GET` the poll URL until `preview.status` is no longer `researching`. A `ready` preview has what Revnu found, with sources, and a `claim_url` that signs up and keeps the research. It needs no sign-in.
