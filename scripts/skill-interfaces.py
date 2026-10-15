#!/usr/bin/env python3
"""Generate the Codex skill cards, or check that they match with --check."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = {
    'revnu': ('Revnu', 'Get customers for what you are building', 'Use $revnu to work out how to get customers for this project.'),
    'revnu-first-customers': ('Revnu: First customers', 'Find your first buyers and launch a growth experiment', 'Use $revnu-first-customers to plan how to get the first customers for this project.'),
    'revnu-find-leads': ('Revnu: Find leads', 'Find buyers with verified contacts and reasons they fit', 'Use $revnu-find-leads to find the right buyers for this project.'),
    'revnu-cold-email': ('Revnu: Cold email', 'Write outreach and follow-ups in your voice', 'Use $revnu-cold-email to prepare outreach for this project.'),
    'revnu-linkedin-outreach': ('Revnu: LinkedIn outreach', 'Reach buyers through LinkedIn invites and messages', 'Use $revnu-linkedin-outreach to plan LinkedIn outreach for this project.'),
    'revnu-ads': ('Revnu: Paid ads', 'Build campaigns and measure what your budget produces', 'Use $revnu-ads to work out which ads fit this project and budget.'),
    'revnu-seo-ai-answers': ('Revnu: SEO and AI answers', 'Get found in Google, ChatGPT and other AI answers', 'Use $revnu-seo-ai-answers to plan how buyers can find this project.'),
    'revnu-results': ('Revnu: Growth results', 'Read growth results and work waiting for approval', 'Use $revnu-results to show recent results and what needs my approval.'),
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
