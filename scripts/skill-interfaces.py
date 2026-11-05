#!/usr/bin/env python3
"""Generate the Codex skill cards, or check that they match with --check."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = {
    'revnu': ('Revnu', 'Get customers and move deals forward with Revnu', 'Use $revnu to execute the GTM, sales or CRM work for this business.'),
    'first-customers': ('Revnu: First customers', 'Find your first buyers and launch a growth experiment', 'Use $first-customers to get the first customers for this project.'),
    'find-leads': ('Revnu: Find leads', 'Find buyers with verified contacts and reasons they fit', 'Use $find-leads to find the right buyers for this project.'),
    'cold-email': ('Revnu: Cold email', 'Write outreach and follow-ups in your voice', 'Use $cold-email to prepare outreach for this project.'),
    'linkedin-outreach': ('Revnu: LinkedIn outreach', 'Reach buyers through LinkedIn invites and messages', 'Use $linkedin-outreach to prepare the requested LinkedIn outreach.'),
    'ads': ('Revnu: Paid ads', 'Build campaigns and measure what your budget produces', 'Use $ads to prepare the requested ads within my approved budget.'),
    'seo-ai-answers': ('Revnu: SEO and AI answers', 'Get found in Google, ChatGPT and other AI answers', 'Use $seo-ai-answers to create the requested marketing pages in Revnu.'),
    'results': ('Revnu: Growth results', 'Read growth results and work waiting for approval', 'Use $results to show recent results and what needs my approval.'),
    'revnu-geo-check': ('Revnu: GEO check', 'See whether AI answers name you, and who they cite instead', 'Use $revnu-geo-check to see whether AI answers recommend this business.'),
    'revnu-ai-crawler-access': ('Revnu: AI crawler access', 'Check that ChatGPT, Claude and Perplexity can reach your site', 'Use $revnu-ai-crawler-access to check which AI crawlers can reach this site.'),
    'revnu-ai-readiness-audit': ('Revnu: AI readiness audit', 'Make your pages easy for AI answers to quote', 'Use $revnu-ai-readiness-audit to audit this site for AI answers and fix it.'),
    'revnu-fix-ai-claims': ('Revnu: Fix AI claims', 'Correct what AI answers get wrong about you', 'Use $revnu-fix-ai-claims to find and fix wrong claims AI answers make about us.'),
    'revnu-get-listed': ('Revnu: Get listed', 'Get onto the lists and directories AI answers cite', 'Use $revnu-get-listed to find and draft the listings that get us recommended.'),
    'revnu-landing-page-audit': ('Revnu: Landing page audit', 'Fix the page your ads and posts send people to', 'Use $revnu-landing-page-audit to audit this landing page against its traffic.'),
    'revnu-growth-context': ('Revnu: Growth context', 'Write down who buys, why, and what has worked', 'Use $revnu-growth-context to create or update this business\'s growth context file.'),
}


def generate(check):
    skills = {path.name for path in (ROOT / 'skills').iterdir() if (path / 'SKILL.md').is_file()}
    if skills != CARDS.keys():
        raise SystemExit(f'Skill cards differ from skill folders: {skills ^ CARDS.keys()}')
    failures = []
    for name, (title, description, prompt) in CARDS.items():
        assert 25 <= len(description) <= 64, name
        interface = {
            'display_name': title,
            'short_description': description,
            'icon_small': './assets/icon.png',
            'icon_large': './assets/icon.png',
            'brand_color': '#1C8F4C',
            'default_prompt': prompt,
        }
        metadata = 'interface:\n' + ''.join(f'  {key}: {json.dumps(value)}\n' for key, value in interface.items())
        folder = ROOT / 'skills' / name
        outputs = {
            folder / 'agents/openai.yaml': metadata.encode(),
            folder / 'assets/icon.png': (ROOT / 'assets/icon.png').read_bytes(),
        }
        for path, content in outputs.items():
            if check:
                if not path.is_file() or path.read_bytes() != content:
                    failures.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
    if failures:
        raise SystemExit('Run python3 scripts/skill-interfaces.py to update: ' + ', '.join(failures))
    print(f'{len(CARDS)}/{len(CARDS)} skill cards {"checked" if check else "generated"}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated metadata or icons have drifted')
    generate(parser.parse_args().check)
