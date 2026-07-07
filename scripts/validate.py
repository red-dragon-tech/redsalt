#!/usr/bin/env python3
"""Static validation for redsalt documentation."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md',
    'docs/architecture.md',
    'docs/repositories.md',
    'docs/redsalt-master.md',
    'docs/redsalt-minion.md',
    'docs/workflow.md',
    'docs/automation.md',
    'docs/security.md',
]
LINK_RE = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
FORBIDDEN = [
    'BEGIN ' + 'OPENSSH PRIVATE KEY',
    'BEGIN ' + 'RSA PRIVATE KEY',
    'PRIVATE ' + 'KEY-----',
]


def fail(message: str) -> None:
    print(f'ERROR: {message}', file=sys.stderr)
    sys.exit(1)


def check_required() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        fail('missing required docs: ' + ', '.join(missing))


def check_links() -> None:
    for path in [ROOT / 'README.md', *sorted((ROOT / 'docs').glob('*.md'))]:
        text = path.read_text()
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            target_path, _anchor, _fragment = target.partition('#')
            candidate = (path.parent / target_path).resolve()
            if not str(candidate).startswith(str(ROOT.resolve())):
                fail(f'{path.relative_to(ROOT)} has link outside repo: {target}')
            if not candidate.exists():
                fail(f'{path.relative_to(ROOT)} has broken local link: {target}')


def check_no_private_keys() -> None:
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts or path.suffix == '.pyc':
            continue
        text = path.read_text(errors='ignore')
        for marker in FORBIDDEN:
            if marker in text:
                fail(f'private key marker found in {path.relative_to(ROOT)}')


def main() -> int:
    check_required()
    check_links()
    check_no_private_keys()
    print('redsalt documentation validation passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
