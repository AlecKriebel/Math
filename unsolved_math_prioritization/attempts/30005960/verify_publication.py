#!/usr/bin/env python3
"""Offline integrity, exact patch replay, arithmetic and mutation controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

PINS = {
    'author/MANIFEST.json': 'fa8e4850f2a7c16ed5837240931896bf98e90aedc428193c476b30e6c44af624',
    'audit/AUDIT_MANIFEST.json': 'ac1aa32035cbc5ba9a7543dc6aaa36aef638cc5dd05a835b09a58a39087c9564',
    'audit/INDEPENDENT_AUDIT.md': 'de301620fcda1ef369344ddb70357ccfe5501e6307e555f35218a2bb3b7f1315',
    'audit/OPTIONAL_SOURCE_SCOPE_CLARIFICATION.patch': 'addd71df5c987b2d5dde8ca92239ad6253ac4d4253588d34e4c89100b2fc456c',
    'audit/SOURCE_AUDIT_READING_COPY.md': '5352f31a98392f5c4285bee279b5c03165e499a265b0b3b6d17ede5327039465',
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def check_manifest(base, name):
    manifest = json.loads((base / name).read_text())
    seen = set()
    for item in manifest['files']:
        rel = item['path']
        require(isinstance(rel, str) and rel not in seen and not Path(rel).is_absolute()
                and '..' not in Path(rel).parts and '\\' not in rel, 'unsafe or duplicate manifest path')
        seen.add(rel)
        path = base / rel
        require(path.is_file() and not path.is_symlink(), 'missing or nonregular file: ' + rel)
        data = path.read_bytes()
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'manifest mismatch: ' + rel)
    return seen

def apply_exact_patch(original, patch):
    source = original.decode().splitlines(keepends=True)
    lines = patch.decode().splitlines(keepends=True)
    require(lines[:2] == ['--- a/SOURCE_AUDIT.md\n', '+++ b/SOURCE_AUDIT.md\n'], 'patch headers')
    out, pos, i, hunks = [], 0, 2, 0
    while i < len(lines):
        match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[i])
        require(match is not None, 'invalid patch hunk')
        a, n, c, k = map(int, match.groups())
        i += 1
        hunks += 1
        require(a - 1 >= pos, 'overlapping patch')
        out += source[pos:a - 1]
        pos = a - 1
        require(len(out) == c - 1, 'new hunk position')
        old = new = 0
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]
            i += 1
            require(line and line[0] in ' +-', 'invalid patch line')
            if line[0] in ' -':
                require(pos < len(source) and source[pos] == line[1:], 'patch context mismatch')
                pos += 1
                old += 1
            if line[0] in ' +':
                out.append(line[1:])
                new += 1
        require((old, new) == (n, k), 'hunk counts')
    require(hunks == 1, 'unexpected hunk count')
    return ''.join(out + source[pos:]).encode()

def verify(base, run_controls=True):
    base = Path(base).resolve()
    expected = check_manifest(base, 'PUBLICATION_MANIFEST.json') | {'PUBLICATION_MANIFEST.json'}
    actual = {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == expected, 'packet inventory differs')
    require(not any(p.is_symlink() for p in base.rglob('*')), 'symlink in packet')
    for name, digest in PINS.items():
        require(sha((base / name).read_bytes()) == digest, 'frozen input differs: ' + name)
    for subdir, manifest in [('author', 'MANIFEST.json'), ('audit', 'AUDIT_MANIFEST.json')]:
        inventory = check_manifest(base / subdir, manifest) | {manifest}
        require(inventory == {p.name for p in (base / subdir).iterdir()}, 'frozen subpacket inventory')
    original = (base / 'author/SOURCE_AUDIT.md').read_bytes()
    patch = (base / 'audit/OPTIONAL_SOURCE_SCOPE_CLARIFICATION.patch').read_bytes()
    require(apply_exact_patch(original, patch) == (base / 'audit/SOURCE_AUDIT_READING_COPY.md').read_bytes(), 'patch replay differs')
    if run_controls:
        env = dict(os.environ, PYTHONOPTIMIZE='0', PYTHONDONTWRITEBYTECODE='1')
        for script, output, key, expected_count in [
                ('author/check_exact.py', 'author/CHECK_RESULTS.json', 'assertions', 1613),
                ('audit/independent_check.py', 'audit/INDEPENDENT_CHECK_RESULTS.json', 'test_groups', 17)]:
            result = subprocess.run([sys.executable, str(base / script)], capture_output=True, env=env, check=True)
            require(result.stdout == (base / output).read_bytes(), 'control output bytes differ: ' + script)
            parsed = json.loads(result.stdout)
            require(parsed['result'] == 'PASS' and parsed[key] == expected_count, 'control result differs')
        require((base / 'audit/REPLAY_RESULTS.json').read_bytes() == (base / 'author/CHECK_RESULTS.json').read_bytes(), 'audited replay identity differs')
    return {'problem_id': 30005960, 'result': 'PASS', 'files_checked': len(actual),
            'originals_preserved': True, 'optional_patch_replay_exact': True,
            'author_assertions': 1613, 'independent_test_groups': 17,
            'controls_rerun': run_controls,
            'scope': 'Packet integrity and exact arithmetic controls; categorical existence, HN, full support and convergence remain credited literature inputs.'}

def mutation_controls(base):
    cases = [
        ('original example corruption', 'author/EXPLICIT_EXAMPLE.md', 'append'),
        ('original source audit corruption', 'author/SOURCE_AUDIT.md', 'append'),
        ('reading copy corruption', 'audit/SOURCE_AUDIT_READING_COPY.md', 'append'),
        ('optional patch corruption', 'audit/OPTIONAL_SOURCE_SCOPE_CLARIFICATION.patch', 'append'),
        ('author output corruption', 'author/CHECK_RESULTS.json', 'append'),
        ('independent output corruption', 'audit/INDEPENDENT_CHECK_RESULTS.json', 'append'),
        ('missing complete audit', 'audit/INDEPENDENT_AUDIT.md', 'delete'),
        ('unexpected source file', 'unexpected_source.pdf', 'append'),
        ('frozen author manifest corruption', 'author/MANIFEST.json', 'append'),
        ('rehashed complete audit corruption', 'audit/INDEPENDENT_AUDIT.md', 'rehash'),
        ('duplicate manifest entry', 'PUBLICATION_MANIFEST.json', 'duplicate'),
        ('unlisted existing file', 'README.md', 'unlist'),
        ('unsafe manifest path', '../outside', 'unsafe'),
    ]
    results = []
    for label, rel, kind in cases:
        with tempfile.TemporaryDirectory(prefix='surface-stability-check-') as tmp:
            root = Path(tmp) / 'packet'
            shutil.copytree(base, root)
            path = root / rel
            if kind == 'delete':
                path.unlink()
            elif kind in ('append', 'rehash'):
                path.write_bytes((path.read_bytes() if path.exists() else b'') + b'corruption\n')
            manifest_path = root / 'PUBLICATION_MANIFEST.json'
            manifest = json.loads(manifest_path.read_text())
            if kind == 'rehash':
                for item in manifest['files']:
                    if item['path'] == rel:
                        item.update(bytes=len(path.read_bytes()), sha256=sha(path.read_bytes()))
            elif kind == 'duplicate':
                manifest['files'].append(manifest['files'][0])
            elif kind == 'unlist':
                manifest['files'] = [item for item in manifest['files'] if item['path'] != rel]
            elif kind == 'unsafe':
                manifest['files'][0]['path'] = rel
            if kind in ('rehash', 'duplicate', 'unlist', 'unsafe'):
                manifest_path.write_text(json.dumps(manifest))
            try:
                verify(root, False)
            except (ValueError, OSError, KeyError):
                results.append({'case': label, 'rejected': True})
            else:
                raise ValueError('mutation accepted: ' + label)
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutation-controls', action='store_true')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    result = verify(base)
    if args.mutation_controls:
        result['mutation_controls'] = mutation_controls(base)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
