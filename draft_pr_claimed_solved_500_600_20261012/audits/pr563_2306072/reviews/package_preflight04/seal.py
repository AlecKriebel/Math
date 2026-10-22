#!/usr/bin/env python3
"""Seal/verify only this review's authored outputs, never raw scratch or inputs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCLUDED = {'MANIFEST.json', 'SEAL_CHECK.json'}


def inventory():
    return {p.name: p for p in ROOT.iterdir() if p.is_file() and
            p.name not in EXCLUDED and (p.suffix in ('.md', '.json', '.py')
                                       or p.name == '.gitignore')}


def entries():
    out = {}
    for name, p in sorted(inventory().items()):
        if p.is_symlink():
            raise RuntimeError('Authored output symlink')
        d = p.read_bytes()
        out[name] = {'bytes': len(d), 'sha256': hashlib.sha256(d).hexdigest()}
    return out


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--verify', action='store_true')
    args = a.parse_args()
    path = ROOT / 'MANIFEST.json'
    if args.verify:
        d = json.loads(path.read_text())
        if d['files'] != entries():
            raise RuntimeError('Authored review inventory/hash/size mismatch')
        result = {'status': 'PASS', 'authored_files': len(d['files']),
                  'manifest_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'scope': 'Consistency only; no authenticity, novelty, formal proof or human peer review.'}
        print(json.dumps(result, indent=2))
    else:
        d = {'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
             'scope': 'Every present top-level authored review output. Scratch cache, third-party sources, MANIFEST self-reference and terminal SEAL_CHECK.json excluded.',
             'files': entries()}
        path.write_text(json.dumps(d, indent=2) + '\n')
        print(json.dumps({'status': 'SEALED', 'authored_files': len(d['files'])}))


if __name__ == '__main__':
    main()
