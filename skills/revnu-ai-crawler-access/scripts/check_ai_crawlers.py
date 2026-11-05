#!/usr/bin/env python3
"""Check whether AI crawlers can reach a page.

For one URL this script:
  1. fetches /robots.txt and evaluates it per crawler (RFC 9309 matching),
  2. fetches the page once with a normal browser user agent and once with each
     crawler's user agent, recording status codes, redirects and challenge pages,
  3. reads <meta name="robots"> (and bot-named meta tags) and X-Robots-Tag.

Python 3.8+, standard library only. It contacts only the site you name.

Limits, stated in the report too: requests come from this machine's IP, not the
crawler's published IP ranges, so a firewall that verifies crawler IPs may treat
these requests differently from the real crawler. A clean result here is
evidence, not proof.

Usage:
  python3 check_ai_crawlers.py https://example.com/pricing
  python3 check_ai_crawlers.py example.com --json
  python3 check_ai_crawlers.py https://example.com --robots-only

Exit codes: 0 report produced, 2 bad arguments, 3 site unreachable.
"""

import argparse
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "1.0.0"
CHECKED_AS_OF = "2026-11-05"
MAX_BODY = 2 * 1024 * 1024
ROBOTS_MAX = 500 * 1024
TIMEOUT = 20

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# token: robots.txt product token. ua: header sent (None = token only, never
# fetches). robots: what the vendor documents about robots.txt for this agent.
# Facts and sources: references/sources.md (as of CHECKED_AS_OF).
CRAWLERS = [
    {"token": "OAI-SearchBot", "owner": "OpenAI", "job": "search",
     "controls": "Being shown and cited in ChatGPT search answers",
     "robots": "honors",
     "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; "
           "OAI-SearchBot/1.4; +https://openai.com/searchbot"},
    {"token": "GPTBot", "owner": "OpenAI", "job": "training",
     "controls": "Use in training OpenAI foundation models (not ChatGPT search)",
     "robots": "honors",
     "ua": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; "
           "GPTBot/1.4; +https://openai.com/gptbot"},
    {"token": "ChatGPT-User", "owner": "OpenAI", "job": "user-fetch",
     "controls": "Pages ChatGPT opens when a user's request needs them",
     "robots": "may not apply (user-initiated)",
     "ua": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; "
           "ChatGPT-User/1.0; +https://openai.com/bot"},
    {"token": "Claude-SearchBot", "owner": "Anthropic", "job": "search",
     "controls": "Indexing for Claude's search results",
     "robots": "honors",
     "ua": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; "
           "Claude-SearchBot/1.0; +Claude-SearchBot@anthropic.com)"},
    {"token": "ClaudeBot", "owner": "Anthropic", "job": "training",
     "controls": "Use in Anthropic model training",
     "robots": "honors",
     "ua": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; "
           "ClaudeBot/1.0; +claudebot@anthropic.com)"},
    {"token": "Claude-User", "owner": "Anthropic", "job": "user-fetch",
     "controls": "Pages Claude fetches to answer a user's question",
     "robots": "honors",
     "ua": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; "
           "Claude-User/1.0; +Claude-User@anthropic.com)"},
    {"token": "PerplexityBot", "owner": "Perplexity", "job": "search",
     "controls": "Being found and linked in Perplexity search results",
     "robots": "honors",
     "ua": "Mozilla/5.0 (compatible; PerplexityBot/1.0; "
           "+https://perplexity.ai/perplexitybot)"},
    {"token": "Perplexity-User", "owner": "Perplexity", "job": "user-fetch",
     "controls": "Pages Perplexity visits to answer a user's question",
     "robots": "generally ignores (user-initiated)",
     "ua": "Mozilla/5.0 (compatible; Perplexity-User/1.0; "
           "+https://perplexity.ai/perplexity-user)"},
    {"token": "Googlebot", "owner": "Google", "job": "search",
     "controls": "Google Search, including AI Overviews and AI Mode",
     "robots": "honors",
     "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile "
           "Safari/537.36 (compatible; Googlebot/2.1; "
           "+http://www.google.com/bot.html)"},
    {"token": "Google-Extended", "owner": "Google", "job": "training+grounding",
     "controls": "Gemini model training and grounding in Gemini Apps / Vertex AI. "
                 "Does not affect Google Search inclusion or ranking",
     "robots": "token only (no crawler of its own)", "ua": None},
    {"token": "Bingbot", "owner": "Microsoft", "job": "search",
     "controls": "Bing search and Microsoft Copilot answers (one index)",
     "robots": "honors",
     "ua": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; "
           "bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/131.0.0.0 "
           "Safari/537.36"},
    {"token": "Applebot", "owner": "Apple", "job": "search",
     "controls": "Siri, Spotlight and Safari search; data may also train Apple models",
     "robots": "honors (follows Googlebot rules if Applebot is not named)",
     "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
           "(KHTML, like Gecko) Version/17.4 Safari/605.1.15 "
           "(Applebot/0.1; +http://www.apple.com/go/applebot)"},
    {"token": "Applebot-Extended", "owner": "Apple", "job": "training",
     "controls": "Use of Applebot-crawled pages to train Apple foundation models. "
                 "Does not affect Apple search",
     "robots": "token only (no crawler of its own)", "ua": None},
    {"token": "Meta-WebIndexer", "owner": "Meta", "job": "search",
     "controls": "Citing and linking the site in Meta AI answers",
     "robots": "honors",
     "ua": "meta-webindexer/1.1 (+https://developers.facebook.com/docs/sharing/"
           "webmasters/web-crawlers)"},
    {"token": "Meta-ExternalAgent", "owner": "Meta", "job": "training",
     "controls": "Training Meta AI models and indexing for Meta products",
     "robots": "honors",
     "ua": "meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/"
           "webmasters/web-crawlers)"},
    {"token": "Meta-ExternalFetcher", "owner": "Meta", "job": "user-fetch",
     "controls": "Links Meta AI fetches at a user's request",
     "robots": "may bypass (user-initiated)",
     "ua": "meta-externalfetcher/1.1 (+https://developers.facebook.com/docs/"
           "sharing/webmasters/web-crawlers)"},
    {"token": "CCBot", "owner": "Common Crawl", "job": "training",
     "controls": "Common Crawl's open web archive, widely used to train models",
     "robots": "honors (opt-out via robots.txt)",
     "ua": "CCBot/2.0 (https://commoncrawl.org/faq/)"},
    {"token": "Bytespider", "owner": "ByteDance", "job": "unverified",
     "controls": "Purpose not verified from an English primary source",
     "robots": "unverified (third-party logs report it ignoring robots.txt)",
     "ua": "Mozilla/5.0 (Linux; Android 5.0) AppleWebKit/537.36 (KHTML, like "
           "Gecko) Mobile Safari/537.36 (compatible; Bytespider; "
           "https://zhanzhang.toutiao.com/)"},
]

# Shared training-preference token (IETF aipref individual draft, 2026-10-30).
USAGE_TOKEN = "__usage_ai-training"

CHALLENGE_MARKERS = [
    ("cloudflare challenge", re.compile(r"just a moment\.\.\.|cf-challenge|challenge-platform|cf_chl_", re.I)),
    ("captcha", re.compile(r"captcha|hcaptcha|recaptcha|turnstile", re.I)),
    ("access denied page", re.compile(r"<title>\s*(access denied|attention required|403 forbidden|forbidden)", re.I)),
    ("bot management page", re.compile(r"px-captcha|_incapsula_|datadome|perimeterx|akamai.*bot", re.I)),
]
MITIGATION_HEADERS = ["cf-mitigated", "x-vercel-mitigated", "x-amzn-waf-action", "x-datadome", "x-sucuri-block"]
KNOWN_DIRECTIVES = {"unavailable_after", "max-snippet", "max-image-preview",
                    "max-video-preview", "ai-training", "ai-grounding"}
FLAG_DIRECTIVES = ["noindex", "none", "nosnippet", "noarchive", "nocache",
                   "noai", "noimageai", "max-snippet:0", "ai-training:disallow",
                   "ai-grounding:disallow", "ai-grounding:disallowextended"]


# ---------------------------------------------------------------- HTTP

class _Recorder(urllib.request.HTTPRedirectHandler):
    max_redirections = 10

    def __init__(self):
        super().__init__()
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({"status": code, "from": req.full_url,
                           "to": urllib.parse.urljoin(req.full_url, newurl)})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, ua, max_redirects=10, limit=MAX_BODY):
    """GET url. Returns dict with status, final_url, redirects, headers, body, error."""
    rec = _Recorder()
    rec.max_redirections = max_redirects
    opener = urllib.request.build_opener(rec, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.8",
        "Accept-Language": "en",
    })
    out = {"url": url, "status": None, "final_url": url, "redirects": rec.chain,
           "headers": {}, "body": "", "error": None, "ms": None}
    t0 = time.time()
    try:
        resp = opener.open(req, timeout=TIMEOUT)
        out["status"] = resp.status
        out["final_url"] = resp.geturl()
        out["headers"] = {k.lower(): v for k, v in resp.headers.items()}
        out["_header_list"] = resp.headers.get_all("X-Robots-Tag") or []
        out["body"] = _decode(resp.read(limit), resp.headers)
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        out["final_url"] = e.geturl() or url
        out["headers"] = {k.lower(): v for k, v in (e.headers or {}).items()}
        out["_header_list"] = (e.headers.get_all("X-Robots-Tag") if e.headers else None) or []
        try:
            out["body"] = _decode(e.read(limit), e.headers)
        except Exception:
            out["body"] = ""
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError, OSError) as e:
        reason = getattr(e, "reason", e)
        out["error"] = f"{type(reason).__name__}: {reason}"
    out["ms"] = int((time.time() - t0) * 1000)
    return out


def _decode(raw, headers):
    charset = None
    if headers is not None:
        charset = headers.get_content_charset()
    for enc in (charset, "utf-8", "latin-1"):
        if not enc:
            continue
        try:
            return raw.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", "replace")


# ---------------------------------------------------------------- robots.txt (RFC 9309)

_UNRESERVED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")


def _normalize(path):
    """Percent-encode per RFC 9309 2.2.2 so pattern and path compare alike."""
    out = []
    i = 0
    data = path.encode("utf-8")
    while i < len(data):
        b = data[i]
        if b == 0x25 and i + 2 < len(data) + 0 and re.match(rb"[0-9A-Fa-f]{2}", data[i + 1:i + 3]):
            val = int(data[i + 1:i + 3], 16)
            ch = chr(val)
            out.append(ch if ch in _UNRESERVED else "%%%02X" % val)
            i += 3
            continue
        if b < 0x21 or b > 0x7E:
            out.append("%%%02X" % b)
        else:
            out.append(chr(b))
        i += 1
    return "".join(out)


def parse_robots(text):
    """Return list of groups: {"agents": [...], "rules": [(kind, pattern, line)]}, plus sitemaps."""
    if text.startswith("﻿"):
        text = text[1:]
    groups, sitemaps = [], []
    current, last_was_agent = None, False
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip().lower(), value.strip()
        if key in ("user-agent", "useragent", "user agent"):
            if current is None or not last_was_agent:
                current = {"agents": [], "rules": [], "line": lineno}
                groups.append(current)
            current["agents"].append(value)
            last_was_agent = True
        elif key in ("allow", "disallow"):
            last_was_agent = False
            if current is not None and value:
                current["rules"].append((key, value, lineno))
        elif key == "sitemap":
            sitemaps.append(value)
        elif key == "content-signal":
            # Cloudflare Content Signals Policy: a stated preference, not a block.
            if current is not None:
                current.setdefault("content_signal", []).append(value)
        else:
            last_was_agent = False if key != "crawl-delay" else last_was_agent
            if current is not None and key == "crawl-delay":
                current.setdefault("crawl_delay", value)
    return groups, sitemaps


def _agent_matches(robots_agent, token):
    name = robots_agent.split("/", 1)[0].strip().lower()
    return name == token.lower()


def groups_for(groups, token):
    named = [g for g in groups if any(_agent_matches(a, token) for a in g["agents"])]
    return named


def _pattern_regex(pattern):
    pat = _normalize(pattern)
    anchored = pat.endswith("$")
    if anchored:
        pat = pat[:-1]
    rx = "".join(".*" if c == "*" else re.escape(c) for c in pat)
    return re.compile("^" + rx + ("$" if anchored else "")), len(_normalize(pattern))


def evaluate(groups, token, path, fallback_token=None):
    """Decide allow/disallow for token on path. Returns dict with verdict and why."""
    matched = groups_for(groups, token)
    via = token
    if not matched and fallback_token:
        matched = groups_for(groups, fallback_token)
        via = fallback_token if matched else via
    if not matched:
        matched = [g for g in groups if any(a.strip() == "*" for a in g["agents"])]
        via = "*" if matched else None
    if not matched:
        return {"verdict": "allowed", "group": None, "rule": None, "why": "no group applies"}
    rules = [r for g in matched for r in g["rules"]]
    target = _normalize(path)
    best = None
    for kind, pattern, lineno in rules:
        rx, length = _pattern_regex(pattern)
        if rx.match(target):
            if best is None or length > best[0] or (length == best[0] and kind == "allow" and best[1] == "disallow"):
                best = (length, kind, pattern, lineno)
    if best is None:
        return {"verdict": "allowed", "group": via, "rule": None, "why": "no rule matches this path"}
    _, kind, pattern, lineno = best
    return {"verdict": "allowed" if kind == "allow" else "blocked", "group": via,
            "rule": f"{kind.capitalize()}: {pattern} (line {lineno})", "why": "longest matching rule"}


# ---------------------------------------------------------------- page signals

META_RX = re.compile(r"<meta\b[^>]*>", re.I)
ATTR_RX = re.compile(r'([a-zA-Z_:-]+)\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))')


def meta_robots(html):
    """Return {name_lower: content} for robots-style meta tags in <head>."""
    head = html.split("</head>", 1)[0] if "</head>" in html.lower() else html[:200000]
    found = {}
    for tag in META_RX.findall(head):
        attrs = {}
        for m in ATTR_RX.finditer(tag):
            attrs[m.group(1).lower()] = m.group(3) if m.group(3) is not None else (m.group(4) if m.group(4) is not None else m.group(5))
        name = (attrs.get("name") or "").strip().lower()
        if name and "content" in attrs:
            if name == "robots" or name in BOT_META_NAMES:
                found.setdefault(name, []).append(attrs["content"])
    return found


BOT_META_NAMES = {c["token"].lower() for c in CRAWLERS} | {"bingbot", "googlebot-news", "google-extended"}


def x_robots(values):
    """Parse X-Robots-Tag header values into {agent_or_*: [directives]}."""
    result = {}
    for value in values:
        agent = "*"
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.+)$", part)
            if m and m.group(1).lower() not in KNOWN_DIRECTIVES:
                agent, part = m.group(1).lower(), m.group(2).strip()
            result.setdefault(agent, []).append(part.lower())
    return result


def flagged(directives):
    hits = []
    for d in directives:
        for token in re.split(r"[,\s]+", d.lower()):
            if token in FLAG_DIRECTIVES and token not in hits:
                hits.append(token)
    return hits


def challenge_hints(resp):
    hints = []
    for h in MITIGATION_HEADERS:
        if h in resp["headers"]:
            hints.append(f"header {h}: {resp['headers'][h]}")
    body = resp["body"][:60000]
    for label, rx in CHALLENGE_MARKERS:
        if rx.search(body):
            hints.append(label)
    return hints


def visible_words(html):
    text = re.sub(r"(?is)<(script|style|noscript|template)\b.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return len(re.findall(r"\w{2,}", text))


# ---------------------------------------------------------------- report

def classify_fetch(resp, baseline):
    if resp["error"]:
        return "error", resp["error"]
    s = resp["status"]
    hints = challenge_hints(resp)
    base_ok = baseline and baseline["status"] and 200 <= baseline["status"] < 300
    if s and 200 <= s < 300:
        if hints and not challenge_hints(baseline or {"headers": {}, "body": ""}):
            return "challenge", "200 but the body looks like a bot challenge: " + ", ".join(hints)
        words = visible_words(resp["body"])
        if base_ok:
            bw = visible_words(baseline["body"])
            if bw > 200 and words < bw * 0.5:
                return "different", f"200 but {words} visible words vs {bw} for a browser"
        return "ok", f"{s}"
    if s in (401, 403, 406, 429, 451, 503):
        detail = f"{s}" + (" (" + ", ".join(hints) + ")" if hints else "")
        if base_ok:
            return "blocked", detail + "; a browser user agent got " + str(baseline["status"])
        return "blocked-all", detail + "; a browser user agent was refused too"
    return "status", f"{s}"


def run(url, robots_only=False, delay=0.4):
    if "://" not in url:
        url = "https://" + url
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ValueError(f"not an http(s) URL: {url}")
    path = urllib.parse.urlunsplit(("", "", parts.path or "/", parts.query, ""))
    origin = f"{parts.scheme}://{parts.netloc}"
    report = {"tool": f"check_ai_crawlers.py {VERSION}", "facts_as_of": CHECKED_AS_OF,
              "url": url, "path": path, "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "robots": {}, "page": {}, "crawlers": [], "notes": []}

    # robots.txt
    r = fetch(origin + "/robots.txt", BROWSER_UA, max_redirects=5, limit=ROBOTS_MAX + 1)
    rb = {"url": origin + "/robots.txt", "status": r["status"], "final_url": r["final_url"],
          "redirects": r["redirects"], "error": r["error"], "state": None, "sitemaps": [],
          "groups": 0, "usage_ai_training": None}
    groups = []
    if r["error"]:
        rb["state"] = "unreachable"
    elif 200 <= r["status"] < 300:
        ctype = r["headers"].get("content-type", "")
        body = r["body"]
        if "html" in ctype.lower() or re.match(r"\s*<(!doctype|html)", body, re.I):
            rb["state"] = "html-not-robots"
            report["notes"].append("robots.txt returned HTML, not a robots file. Crawlers parse it as text and usually find no rules, so it allows everything; serve a real text/plain file.")
        else:
            rb["state"] = "parsed"
            if len(body.encode("utf-8")) > ROBOTS_MAX:
                report["notes"].append("robots.txt is over 500 KiB; crawlers may ignore rules past that point.")
            groups, rb["sitemaps"] = parse_robots(body)
            rb["groups"] = len(groups)
            by_value = {}
            for g in groups:
                for v in g.get("content_signal", []):
                    by_value.setdefault(v, []).extend(g["agents"])
            rb["content_signals"] = [f"{v} ({len(a)} agent line(s))" for v, a in by_value.items()]
            usage = groups_for(groups, USAGE_TOKEN)
            if usage:
                rb["usage_ai_training"] = evaluate(groups, USAGE_TOKEN, path)
    elif 400 <= r["status"] < 500:
        rb["state"] = "missing (4xx: crawlers treat everything as allowed)"
    else:
        rb["state"] = "server-error (5xx: RFC 9309 crawlers treat everything as disallowed)"
    report["robots"] = rb

    robots_state = rb["state"]
    for c in CRAWLERS:
        entry = {k: c[k] for k in ("token", "owner", "job", "controls", "robots")}
        if robots_state == "parsed":
            fb = "Googlebot" if c["token"] == "Applebot" else None
            entry["robots_txt"] = evaluate(groups, c["token"], path, fallback_token=fb)
        elif robots_state and robots_state.startswith("server-error"):
            entry["robots_txt"] = {"verdict": "blocked", "group": None, "rule": None,
                                   "why": "robots.txt answered 5xx"}
        elif robots_state == "unreachable":
            entry["robots_txt"] = {"verdict": "unknown", "group": None, "rule": None,
                                   "why": "robots.txt unreachable: " + str(rb["error"])}
        else:
            entry["robots_txt"] = {"verdict": "allowed", "group": None, "rule": None,
                                   "why": "no usable robots.txt"}
        report["crawlers"].append(entry)

    if robots_only:
        return report

    # page fetches
    baseline = fetch(url, BROWSER_UA)
    if baseline["error"] and not baseline["status"]:
        report["page"] = {"error": baseline["error"]}
        raise SystemExit(_print_unreachable(report, baseline))
    report["page"] = {
        "browser_status": baseline["status"], "final_url": baseline["final_url"],
        "redirects": baseline["redirects"],
        "meta_robots": meta_robots(baseline["body"]),
        "x_robots_tag": x_robots(baseline.get("_header_list", [])),
        "visible_words": visible_words(baseline["body"]),
        "jsonld_blocks_in_html": len(re.findall(r'<script[^>]+application/ld\+json', baseline["body"], re.I)),
        "canonical": _canonical(baseline["body"]),
        "host": detect_host(baseline.get("headers") or {}),
    }
    for entry, c in zip(report["crawlers"], CRAWLERS):
        if not c["ua"]:
            entry["fetch"] = {"result": "n/a", "detail": "robots.txt token only; never fetches"}
            continue
        time.sleep(delay)
        resp = fetch(url, c["ua"])
        result, detail = classify_fetch(resp, baseline)
        meta = meta_robots(resp["body"]) if resp["body"] else {}
        xr = x_robots(resp.get("_header_list", []))
        tok = c["token"].lower()
        directives = meta.get("robots", []) + meta.get(tok, []) + xr.get("*", []) + xr.get(tok, [])
        entry["fetch"] = {
            "result": result, "detail": detail, "status": resp["status"],
            "final_url": resp["final_url"], "redirects": resp["redirects"], "ms": resp["ms"],
            "page_directives": flagged(directives),
        }
    return report


HOST_HEADERS = [
    ("cf-ray", "Cloudflare"), ("x-vercel-id", "Vercel"), ("x-nf-request-id", "Netlify"),
    ("x-amz-cf-id", "Amazon CloudFront"), ("x-served-by", "Fastly"), ("x-akamai-transformed", "Akamai"),
    ("x-github-request-id", "GitHub Pages"), ("x-wix-request-id", "Wix"), ("x-shopid", "Shopify"),
]


def detect_host(headers):
    """Name the host/CDN from response headers, with the header that shows it."""
    found = [f"{name} ({h})" for h, name in HOST_HEADERS if h in headers]
    server = headers.get("server")
    if server:
        found.append(f"server: {server}")
    return "; ".join(found) or "not identified from headers"


def _canonical(html):
    m = re.search(r'<link\b[^>]*rel=["\']?canonical["\']?[^>]*>', html, re.I)
    if not m:
        return None
    h = re.search(r'href\s*=\s*["\']([^"\']+)', m.group(0), re.I)
    return h.group(1) if h else None


def _print_unreachable(report, baseline):
    print(f"Could not reach {report['url']}: {baseline['error']}", file=sys.stderr)
    return 3


def verdict_line(e):
    rt = e["robots_txt"]["verdict"]
    f = e.get("fetch", {}).get("result")
    dirs = e.get("fetch", {}).get("page_directives") or []
    if rt == "blocked":
        if e["job"] == "user-fetch" and "honors" not in e["robots"]:
            return "robots.txt disallows (this agent may ignore it)"
        return "BLOCKED by robots.txt"
    if f in ("blocked", "challenge"):
        return "BLOCKED at the server/CDN (robots.txt allows)"
    if f == "blocked-all":
        return "REFUSED (site refuses scripted fetches; check from logs)"
    if f == "error":
        return "ERROR fetching"
    if f == "different":
        return "ALLOWED but served thinner content"
    if any(d in ("noindex", "none") for d in dirs):
        return "ALLOWED to fetch, page says noindex"
    if rt == "unknown":
        return "UNKNOWN (robots.txt unreachable)"
    return "ALLOWED"


def print_text(rep):
    w = sys.stdout.write
    w(f"AI crawler access for {rep['url']}\n")
    w(f"checked {rep['checked_at']} | crawler facts as of {rep['facts_as_of']} | {rep['tool']}\n\n")
    rb = rep["robots"]
    w(f"robots.txt: {rb['status'] or rb['error']} -> {rb['state']}")
    if rb["redirects"]:
        w(f" (redirected to {rb['final_url']})")
    w(f"; {rb['groups']} groups; sitemaps: {len(rb['sitemaps'])}\n")
    if rb.get("usage_ai_training"):
        u = rb["usage_ai_training"]
        w(f"{USAGE_TOKEN} (shared training preference): {u['verdict']} via {u['rule']}\n")
    else:
        w(f"{USAGE_TOKEN} (shared training preference): not set\n")
    if rb.get("content_signals"):
        w("Content-Signal lines (preferences, not blocks): " + "; ".join(rb["content_signals"]) + "\n")
    pg = rep.get("page") or {}
    if pg:
        w(f"page: browser UA got {pg['browser_status']}")
        if pg["redirects"]:
            w(f", redirected to {pg['final_url']}")
        w(f"; {pg['visible_words']} visible words in raw HTML; {pg['jsonld_blocks_in_html']} JSON-LD block(s) in raw HTML")
        w(f"; canonical: {pg['canonical'] or 'none'}\n")
        w(f"host/CDN: {pg.get('host', 'not identified from headers')}\n")
        if pg["meta_robots"]:
            w(f"meta robots: {pg['meta_robots']}\n")
        if pg["x_robots_tag"]:
            w(f"X-Robots-Tag: {pg['x_robots_tag']}\n")
    w("\n")
    hdr = f"{'crawler':<21}{'owner':<13}{'job':<19}{'robots.txt':<11}{'fetch':<8}verdict\n"
    w(hdr)
    w("-" * (len(hdr) + 30) + "\n")
    for e in rep["crawlers"]:
        f = e.get("fetch", {})
        st = f.get("status") or ("-" if f.get("result") == "n/a" or not f else "err")
        w(f"{e['token']:<21}{e['owner']:<13}{e['job']:<19}{e['robots_txt']['verdict']:<11}{str(st):<8}{verdict_line(e)}\n")
    w("\nDetails (only rows that need attention):\n")
    any_detail = False
    for e in rep["crawlers"]:
        f = e.get("fetch", {})
        rt = e["robots_txt"]
        lines = []
        if rt["verdict"] != "allowed":
            lines.append(f"robots.txt {rt['verdict']} via group '{rt['group']}' {rt['rule'] or rt['why']}")
        if f and f.get("result") not in ("ok", "n/a", None):
            lines.append(f"fetch: {f['detail']}")
        if f and f.get("redirects"):
            final = f["final_url"]
            if urllib.parse.urlsplit(final).netloc != urllib.parse.urlsplit(rep["url"]).netloc:
                lines.append(f"redirected off-site to {final}")
        if f and f.get("page_directives"):
            lines.append("page directives: " + ", ".join(f["page_directives"]))
        if lines:
            any_detail = True
            w(f"- {e['token']} ({e['controls']}; robots.txt: {e['robots']}):\n")
            for ln in lines:
                w(f"    {ln}\n")
    if not any_detail:
        w("- none\n")
    for n in rep["notes"]:
        w(f"\nNote: {n}\n")
    w("\nLimits: requests came from this machine's IP with each crawler's user agent. A CDN or firewall that verifies\n"
      "crawler IPs can treat the real crawler differently in either direction; confirm in server or CDN logs.\n"
      "User-triggered agents (ChatGPT-User, Perplexity-User, Meta-ExternalFetcher) may not follow robots.txt at all.\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check AI crawler access for a URL (robots.txt, status codes, meta robots).")
    ap.add_argument("url", help="page to check, e.g. https://example.com/pricing")
    ap.add_argument("--json", action="store_true", help="print the full report as JSON")
    ap.add_argument("--robots-only", action="store_true", help="evaluate robots.txt only; no page fetches")
    ap.add_argument("--delay", type=float, default=0.4, help="seconds between page fetches (default 0.4)")
    args = ap.parse_args(argv)
    try:
        rep = run(args.url, robots_only=args.robots_only, delay=max(0.0, args.delay))
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    if args.json:
        json.dump(rep, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_text(rep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
