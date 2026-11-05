#!/usr/bin/env python3
"""Turn a log of AI-answer runs into mention and citation rates.

No network. Python 3.8+, standard library only.

Input: a JSONL file, one object per run:
  {"surface": "openai-api", "prompt_id": "p03", "family": "category",
   "control": null, "run": 1, "date": "2026-11-05", "model": "...",
   "prompt": "...", "answer": "full answer text",
   "citations": ["https://..."]}
`control` is null for real prompts, "positive" for prompts where the brand
must appear, "negative" for prompts where it must not.

Usage:
  python3 tally.py runs.jsonl --brand "Acme" --alias "Acme Invoicing" \
      --domain acme.com --competitor "Zoho Invoice=zoho.com" \
      --competitor "FreshBooks=freshbooks.com" [--json]

Exit codes: 0 ok, 2 bad input.
"""

import argparse
import json
import math
import re
import sys
import urllib.parse
from collections import Counter, defaultdict


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - m) / d), min(1.0, (c + m) / d))


def rate(k, n):
    if n == 0:
        return "n/a (0 runs)"
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({k / n:.0%}; 95% CI {lo:.0%}-{hi:.0%})"


def host(url):
    try:
        h = urllib.parse.urlsplit(url if "://" in url else "https://" + url).hostname or ""
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def on_domain(h, domain):
    return h == domain or h.endswith("." + domain)


def name_rx(names):
    parts = [re.escape(n.strip()) for n in names if n and n.strip()]
    if not parts:
        return None
    return re.compile(r"(?<![\w-])(" + "|".join(parts) + r")(?![\w-])", re.I)


class Entity:
    def __init__(self, label, names, domain):
        self.label = label
        self.domain = host(domain) if domain else ""
        self.rx = name_rx(names + ([self.domain] if self.domain else []))

    def mentioned(self, run):
        return bool(self.rx and self.rx.search(run.get("answer") or ""))

    def cited(self, run):
        return bool(self.domain) and any(on_domain(host(u), self.domain) for u in run.get("citations") or [])


FAILED = Counter()


def load(path):
    runs = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"line {i}: invalid JSON ({e})")
            if r.get("error"):
                FAILED[r.get("surface", "?")] += 1
                continue
            for key in ("surface", "prompt_id", "answer"):
                if key not in r:
                    raise ValueError(f"line {i}: missing '{key}'")
            r.setdefault("family", "unlabelled")
            r.setdefault("control", None)
            r.setdefault("citations", [])
            runs.append(r)
    if not runs:
        raise ValueError("no runs in file")
    return runs


def analyse(runs, brand, competitors):
    out = {"surfaces": {}, "notes": []}
    by_surface = defaultdict(list)
    for r in runs:
        by_surface[r["surface"]].append(r)
    for surface, rs in sorted(by_surface.items()):
        real = [r for r in rs if not r["control"]]
        pos = [r for r in rs if r["control"] == "positive"]
        neg = [r for r in rs if r["control"] == "negative"]
        s = {
            "runs": len(rs), "prompts": len({r["prompt_id"] for r in real}),
            "brand_mentioned": rate(sum(brand.mentioned(r) for r in real), len(real)),
            "brand_cited": rate(sum(brand.cited(r) for r in real), len(real)) if brand.domain else "n/a (no --domain)",
            "families": {}, "competitors": {}, "controls": {}, "top_cited_domains": [],
            "gaps": [],
        }
        fam = defaultdict(list)
        for r in real:
            fam[r["family"]].append(r)
        for f, frs in sorted(fam.items()):
            s["families"][f] = {
                "brand_mentioned": rate(sum(brand.mentioned(r) for r in frs), len(frs)),
                "brand_cited": rate(sum(brand.cited(r) for r in frs), len(frs)) if brand.domain else "n/a",
            }
        for c in competitors:
            s["competitors"][c.label] = {
                "mentioned": rate(sum(c.mentioned(r) for r in real), len(real)),
                "cited": rate(sum(c.cited(r) for r in real), len(real)) if c.domain else "n/a",
            }
        if pos:
            k = sum(brand.mentioned(r) for r in pos)
            s["controls"]["positive"] = rate(k, len(pos))
            if k < len(pos):
                out["notes"].append(
                    f"{surface}: positive control missed {len(pos) - k} of {len(pos)} runs. Either the brand "
                    "names/aliases don't match how answers write it, or this surface doesn't know the business. "
                    "Fix matching before trusting the other rates.")
        else:
            out["notes"].append(f"{surface}: no positive control runs; rates can't be sanity-checked.")
        if neg:
            k = sum(brand.mentioned(r) for r in neg)
            s["controls"]["negative"] = rate(k, len(neg))
            if k:
                out["notes"].append(
                    f"{surface}: negative control mentioned the brand in {k} of {len(neg)} runs. The name probably "
                    "matches a common word or another company; tighten --brand/--alias and read those answers.")
        else:
            out["notes"].append(f"{surface}: no negative control runs.")
        dom = Counter()
        for r in real:
            for h in {host(u) for u in r.get("citations") or [] if host(u)}:
                dom[h] += 1
        s["top_cited_domains"] = [f"{h}: cited in {n}/{len(real)} runs" for h, n in dom.most_common(15)]
        by_prompt = defaultdict(list)
        for r in real:
            by_prompt[r["prompt_id"]].append(r)
        for pid, prs in sorted(by_prompt.items()):
            b = sum(brand.mentioned(r) for r in prs)
            comp = {c.label: sum(c.mentioned(r) for r in prs) for c in competitors}
            if b == 0 and any(comp.values()):
                shown = ", ".join(f"{k} {v}/{len(prs)}" for k, v in comp.items() if v)
                s["gaps"].append(f"{pid} ({prs[0].get('family')}): brand 0/{len(prs)}; {shown}")
        out["surfaces"][surface] = s
    for surface, n in sorted(FAILED.items()):
        out["notes"].append(f"{surface}: {n} failed run(s) excluded from every denominator.")
    small = [k for k, v in out["surfaces"].items() if v["runs"] and min(
        Counter(r["prompt_id"] for r in by_surface[k] if not r["control"]).values() or [0]) < 3]
    if small:
        out["notes"].append("Some prompts have fewer than 3 runs on " + ", ".join(small) +
                            "; treat their per-prompt results as anecdotes, not rates.")
    return out


def print_text(res, brand):
    w = sys.stdout.write
    for surface, s in res["surfaces"].items():
        w(f"\n## {surface}  ({s['runs']} runs, {s['prompts']} real prompts)\n")
        w(f"{brand.label} mentioned: {s['brand_mentioned']}\n")
        w(f"{brand.label} cited (own domain in sources): {s['brand_cited']}\n")
        if s["controls"]:
            w("controls: " + "; ".join(f"{k} {v}" for k, v in s["controls"].items()) + "\n")
        if s["families"]:
            w("by prompt family:\n")
            for f, v in s["families"].items():
                w(f"  {f:<14} mentioned {v['brand_mentioned']} | cited {v['brand_cited']}\n")
        if s["competitors"]:
            w("competitors:\n")
            for c, v in s["competitors"].items():
                w(f"  {c:<20} mentioned {v['mentioned']} | cited {v['cited']}\n")
        if s["top_cited_domains"]:
            w("most-cited domains:\n")
            for d in s["top_cited_domains"]:
                w(f"  {d}\n")
        if s["gaps"]:
            w("prompts where competitors appear and the brand never does:\n")
            for g in s["gaps"]:
                w(f"  {g}\n")
    for n in res["notes"]:
        w(f"\nNote: {n}\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mention and citation rates from a JSONL log of AI-answer runs.")
    ap.add_argument("log")
    ap.add_argument("--brand", required=True, help="brand name as written in answers")
    ap.add_argument("--alias", action="append", default=[], help="other names for the brand (repeatable)")
    ap.add_argument("--domain", default="", help="the brand's own domain, e.g. acme.com")
    ap.add_argument("--competitor", action="append", default=[],
                    help='"Name=domain.com" or "Name" (repeatable)')
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        runs = load(a.log)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    brand = Entity(a.brand, [a.brand] + a.alias, a.domain)
    comps = []
    for c in a.competitor:
        name, _, dom = c.partition("=")
        comps.append(Entity(name.strip(), [name.strip()], dom.strip()))
    res = analyse(runs, brand, comps)
    if a.json:
        json.dump(res, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_text(res, brand)
    return 0


if __name__ == "__main__":
    sys.exit(main())
