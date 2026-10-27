#!/usr/bin/env python3
"""Validate the RedSalt documentation hub's required pages and local links."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md',
    'docs/features.md',
    'docs/redsalt-master.md',
    'docs/redsalt-minion.md',
]
LINK_RE = re.compile(r'\[[^\]]+\]\(([^)]+)\)')


def main() -> int:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        print('ERROR: missing required docs: ' + ', '.join(missing), file=sys.stderr)
        return 1
    for source in [ROOT / 'README.md', *sorted((ROOT / 'docs').glob('*.md'))]:
        for match in LINK_RE.finditer(source.read_text()):
            target = match.group(1).strip()
            if not target or target.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            target_path, _separator, _fragment = target.partition('#')
            candidate = (source.parent / target_path).resolve()
            if not candidate.is_relative_to(ROOT.resolve()):
                print(f'ERROR: {source.relative_to(ROOT)} link escapes repo: {target}', file=sys.stderr)
                return 1
            if not candidate.exists():
                print(f'ERROR: {source.relative_to(ROOT)} has broken local link: {target}', file=sys.stderr)
                return 1
    print('redsalt documentation validation passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
