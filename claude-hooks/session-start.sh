#!/usr/bin/env bash
# Claude Code only (Codex, Cursor and Grok read hooks/hooks.json, not this folder).
# 1. Says Revnu is installed, so growth requests reach its skill instead of a generic answer.
# 2. Keeps an install from Revnu's own marketplace current: Claude Code leaves
#    auto-update off for third-party marketplaces. At most once a day, in the background.

case "${CLAUDE_PLUGIN_ROOT:-}" in
  */cache/revnu/revnu/*)
    data="${CLAUDE_PLUGIN_DATA:-}"
    if [ -n "$data" ] && command -v claude >/dev/null 2>&1; then
      stamp="$data/last-update-check"
      if [ -z "$(find "$stamp" -mmin -1440 2>/dev/null)" ]; then
        mkdir -p "$data" && touch "$stamp"
        (claude plugin marketplace update revnu && claude plugin update revnu@revnu) \
          </dev/null >/dev/null 2>&1 &
        disown 2>/dev/null || true
      fi
    fi
    ;;
esac

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Revnu is installed in this session. Revnu is the user'"'"'s growth agent: it finds customers and leads, runs cold email, LinkedIn outreach and ads, writes marketing copy and blog posts into Revnu'"'"'s CMS, and reports results. Requests about getting customers or signups, leads, sales, marketing, SEO or AI search visibility, ads, or marketing copy and blog posts are handled with the `revnu` skill or the matching `revnu-*` skill. Coding work is not."}}'
