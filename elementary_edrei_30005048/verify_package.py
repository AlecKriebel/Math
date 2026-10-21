#!/usr/bin/env python3
"""Closed-inventory and full exact-result replay; standard library only."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(value, message):
    if not value:
        raise RuntimeError(message)


def same_json(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same_json(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_json(x, y) for x, y in zip(a, b))
    return a == b


def verify(root):
    manifest_path = root / 'MANIFEST.json'
    require(not manifest_path.is_symlink(), 'integrity: manifest symlink')
    manifest = json.loads(manifest_path.read_text())
    require(set(manifest) == {'schema', 'files'} and manifest['schema'] == 1,
            'integrity: manifest schema')
    files = manifest['files']
    require(type(files) is list, 'integrity: files must be a list')
    names = []
    for item in files:
        require(type(item) is dict and set(item) == {'file', 'bytes', 'sha256'}, 'integrity: entry schema')
        name = item['file']
        require(type(name) is str and name not in ('', '.', '..', 'MANIFEST.json')
                and '/' not in name and '\\' not in name, 'integrity: unsafe path')
        require(type(item['bytes']) is int and item['bytes'] >= 0, 'integrity: invalid byte count')
        require(type(item['sha256']) is str and len(item['sha256']) == 64
                and all(c in '0123456789abcdef' for c in item['sha256']), 'integrity: invalid hash')
        names.append(name)
    require(len(names) == len(set(names)), 'integrity: duplicate path')
    actual = {x.name for x in root.iterdir()}
    require(actual == set(names) | {'MANIFEST.json'}, 'integrity: inventory mismatch')
    for item in files:
        path = root / item['file']
        require(not path.is_symlink() and path.is_file(), 'integrity: nonregular file')
        data = path.read_bytes()
        require(len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'],
                'integrity: content mismatch: ' + item['file'])
    for name in ['check_examples.py', 'verify_package.py', 'controls.py']:
        tree = ast.parse((root / name).read_text())
        require(any(isinstance(node, ast.If) and ast.dump(node.test) ==
                    ast.dump(ast.parse('__name__ == "__main__"', mode='eval').body)
                    for node in tree.body), 'guard: missing main guard: ' + name)
    expected = json.loads((root / 'EXACT_CHECKS.json').read_text())
    outcomes = []
    for flags in ([], ['-O']):
        run = subprocess.run([sys.executable, '-B', *flags, str(root / 'check_examples.py')],
                             cwd=root, capture_output=True, text=True, timeout=60)
        require(run.returncode == 0, 'examples: exact validator rejected: ' + run.stderr.strip())
        require(run.stderr == '', 'examples: unexpected stderr')
        require(same_json(json.loads(run.stdout), expected), 'examples: full result mismatch')
        outcomes.append({'mode': 'optimized' if flags else 'normal', 'complete_result_match': True})
    return {'integrity': 'PASS', 'main_guards': 'PASS', 'replay': outcomes,
            'scope': 'Exact examples and package integrity only; not a theorem or novelty certificate.'}


def main():
    require(len(sys.argv) == 1, 'path: no alternate roots or arguments accepted')
    print(json.dumps(verify(Path(__file__).resolve().parent), indent=2))


if __name__ == '__main__':
    main()
