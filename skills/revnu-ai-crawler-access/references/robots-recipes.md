# robots.txt recipes for the three usual policies

Start from the site's current file. Keep its private-path disallows; the
`/admin/`, `/account/` and `/api/` lines below stand in for whatever the site
already protects. Show the user a diff, never a blind replacement.

## A. Be found everywhere (most businesses that want customers)

The simplest file that works. Every crawler falls through to `*`.

```text
User-agent: *
Disallow: /admin/
Disallow: /account/
Disallow: /api/

Sitemap: https://example.com/sitemap.xml
```

Don't add named groups to say "allowed" unless something else forces it: each
named group replaces `*` for that crawler, and the private-path lines are
easy to forget in it. A wildcard also covers agent search tools that run
their own crawlers under names no list keeps up with.

## B. Show up in AI answers, opt out of training

Search and user-triggered crawlers fall through to `*`. Training crawlers and
tokens get their own groups.

```text
User-agent: *
Disallow: /admin/
Disallow: /account/
Disallow: /api/

# Training opt-outs. These do not affect ChatGPT, Claude, Perplexity,
# Google or Apple search visibility.
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Meta-ExternalAgent
User-agent: CCBot
Disallow: /

# Shared AI-training preference (IETF aipref draft). Honored by Anthropic
# today; OpenAI, Microsoft (from 2027-02-01) and Google (planned early 2027)
# have said they will.
User-agent: __usage_ai-training
Disallow: /

Sitemap: https://example.com/sitemap.xml
```

Several `User-agent` lines in a row form one group, so the six training
tokens share the single `Disallow: /`.

Caveats to tell the user:

- `Applebot` itself also feeds Apple's model training, and Apple's
  `Applebot-Extended` is the documented opt-out; Apple search stays.
- Bing has no robots token for Copilot alone. Today `NOARCHIVE` keeps pages
  out of Copilot answers but also out of Bing's training; from 2027-02-01 the
  page-level `ai-training:disallow` (meta `name="Bingbot"` or
  `X-Robots-Tag: Bingbot: ai-training:disallow`) is the training-only
  control.
- Training opt-outs apply going forward; they don't recall past crawls.

## C. Stay out of AI products entirely

Only when the owner asks for it, after saying what it costs: no citations in
ChatGPT, Claude, Perplexity or Meta AI search.

```text
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Meta-ExternalAgent
User-agent: Meta-WebIndexer
User-agent: Meta-ExternalFetcher
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: Bytespider
Disallow: /

User-agent: *
Disallow: /admin/
Disallow: /account/
Disallow: /api/
```

User-triggered fetchers (`ChatGPT-User`, `Perplexity-User`,
`Meta-ExternalFetcher`) may ignore robots.txt by their vendors' own
statements, and `Bytespider`'s behaviour is unverified; a CDN rule is the
only enforcement. Leaving Google Search and AI Overviews is a separate,
bigger decision (`Googlebot`, `noindex`, or Search Console's generative AI
control), so don't fold it into this recipe.

## One page or section only

Use the path in the group rather than a page tag where possible:

```text
User-agent: GPTBot
Disallow: /research/
```

For page-level limits on what's shown in Google and Bing answers:
`<meta name="robots" content="nosnippet">`, `data-nosnippet` on an element,
or `max-snippet:<n>`. These also limit normal search snippets, so name that
trade-off.

## Where the file lives

| Stack | Source of robots.txt |
|---|---|
| Static / Vite / CRA | `public/robots.txt` |
| Next.js App Router | `app/robots.ts` (returns rules) or `public/robots.txt`; don't keep both |
| Nuxt / Astro / SvelteKit | `public/` or `static/`, or a robots module in config |
| WordPress | generated; SEO plugins (Yoast, Rank Math) own it, or a physical file in the web root overrides |
| Shopify | `robots.txt.liquid` theme template |
| Webflow, Framer, Squarespace, Wix | site settings in the builder's dashboard |
| Cloudflare managed robots.txt | Cloudflare dashboard; it adds Cloudflare-managed lines to what visitors get, so check the served file, not just the repo |

Next.js `app/robots.ts` for recipe B, as an example of editing generated
config rather than a static file:

```ts
import type { MetadataRoute } from "next";

const privatePaths = ["/admin/", "/account/", "/api/"];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", disallow: privatePaths },
      {
        userAgent: [
          "GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended",
          "Meta-ExternalAgent", "CCBot", "__usage_ai-training",
        ],
        disallow: "/",
      },
    ],
    sitemap: "https://example.com/sitemap.xml",
  };
}
```

After the user deploys, re-run `scripts/check_ai_crawlers.py` on the same
URLs and compare.

## Firewall and CDN blocks

When robots.txt allows a crawler but it gets 403/429/503 or a challenge page,
the block is upstream. Give the user the setting, not a workaround:

- **Cloudflare:** AI Crawl Control (per-crawler allow/block), the
  "block AI bots" setting, bot-fighting modes and custom WAF rules on user
  agents. AI Crawl Control lets the owner allow search crawlers while
  blocking training crawlers.
- **Vercel / Netlify:** firewall or bot-protection rules in the dashboard,
  and any `middleware.ts` that returns 403 on user-agent matches.
- **Origin servers:** nginx/Apache rules on `$http_user_agent`, rate limits
  that hit crawlers, security plugins.

When allowing a crawler at the firewall, match its user agent and its
published IP ranges together, as Perplexity and OpenAI recommend. A
user-agent-only allow rule lets anyone in by faking the header.
