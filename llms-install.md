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

The first tool call opens a Revnu sign-in in the browser. Signing in with a new email creates the account. A new account answers `setup_pending` until setup is finished; the `setup_status` tool returns the next step.

## Claude Code, Codex, Gemini CLI and Cursor

`curl -fsSL https://revnu.com/install | sh` adds the MCP server and the Revnu skills to each of these that is installed. Per-host steps are in the [README](README.md#install).

## Without an account

`POST https://revnu.com/api/v1/preview` with `{"website": "<url>"}` researches a business and returns a `previewId`. `GET https://revnu.com/api/v1/preview/<previewId>` returns what Revnu found, with sources and a `claim_url` that signs up and keeps the research. It needs no sign-in.
