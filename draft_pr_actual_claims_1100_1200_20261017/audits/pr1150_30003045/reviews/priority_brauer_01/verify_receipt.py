#!/usr/bin/env python3
"""Read-only integrity verification; this is not a mathematical verifier."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    receipt = args.receipt or base / 'READ_RECEIPT.json'
    value = json.loads(receipt.read_text())
    count = 0
    seen = set()
    for group in ('artifacts', 'inputs'):
        rows = value.get(group)
        if not isinstance(rows, list) or not rows:
            raise ValueError(f'missing nonempty {group}')
        for row in rows:
            name = row['path']
            if name in seen:
                raise ValueError(f'duplicate path: {name}')
            seen.add(name)
            path = base / name
            if path.is_symlink() or not path.is_file():
                raise ValueError(f'not a regular nonsymlink file: {name}')
            content = path.read_bytes()
            if type(row['bytes']) is not int or len(content) != row['bytes']:
                raise ValueError(f'byte count mismatch: {name}')
            if hashlib.sha256(content).hexdigest() != row['sha256']:
                raise ValueError(f'SHA256 mismatch: {name}')
            count += 1
    print(json.dumps({'status': 'PASS', 'files_checked': count,
                      'scope': 'file custody only; no mathematical proof claim'},
                     sort_keys=True))


if __name__ == '__main__':
    main()
