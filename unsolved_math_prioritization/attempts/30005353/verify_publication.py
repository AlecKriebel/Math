#!/usr/bin/env python3
"""Source-free integrity and isolated exact-control replay. Not formal proof verification."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def check_pin(root, name, pin):
    p = root / name
    require(p.is_file() and not p.is_symlink(), 'Missing or linked file: ' + name)
    data = p.read_bytes()
    require(len(data) == pin['bytes'] and digest(data) == pin['sha256'], 'Pin mismatch: ' + name)

def apply_patch(original, patch):
    lines = patch.splitlines(keepends=True)
    require(lines[:2] == ['--- authored/PROOF.md\n', '+++ authored/PROOF.md\n'], 'Unexpected patch paths')
    old = original.splitlines(keepends=True)
    out, cursor, hunks = [], 0, 0
    i = 2
    while i < len(lines):
        m = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[i])
        require(m is not None, 'Bad hunk header')
        start, count, new_start, new_count = map(int, m.groups())
        require(start - 1 >= cursor, 'Overlapping patch hunks')
        out.extend(old[cursor:start - 1]); cursor = start - 1
        require(len(out) == new_start - 1, 'New hunk offset mismatch')
        consumed = produced = 0
        i += 1
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]
            require(line[:1] in (' ', '-', '+'), 'Unsupported patch operation')
            if line[0] in (' ', '-'):
                require(cursor < len(old) and old[cursor] == line[1:], 'Patch context mismatch')
                cursor += 1; consumed += 1
            if line[0] in (' ', '+'):
                out.append(line[1:]); produced += 1
            i += 1
        require((consumed, produced) == (count, new_count), 'Hunk length mismatch')
        hunks += 1
    require(hunks == 1, 'Correction must be exactly one hunk')
    out.extend(old[cursor:])
    return ''.join(out)

def verify():
    manifest = json.loads((ROOT / 'PUBLIC_MANIFEST.json').read_text())
    expected = set(manifest['files']) | {'PUBLIC_MANIFEST.json'}
    present = set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink in packet: ' + str(p.relative_to(ROOT)))
        if p.is_file():
            present.add(p.relative_to(ROOT).as_posix())
    require(present == expected, 'Packet inventory mismatch: ' + repr(sorted(present ^ expected)))
    for name, pin in manifest['files'].items():
        check_pin(ROOT, name, pin)
    author = json.loads((ROOT / 'AUTHOR_MANIFEST.json').read_text())
    audit = json.loads((ROOT / 'audit/AUDIT_MANIFEST.json').read_text())
    require(len(author['files']) == 12, 'Wrong original file count')
    require(author['files'] == audit['original_inputs'], 'Original manifest disagreement')
    check_pin(ROOT, 'AUTHOR_MANIFEST.json', audit['original_manifest'])
    for name, pin in {**author['files'], **audit['files']}.items():
        check_pin(ROOT, name, pin)
    old = (ROOT / 'authored/PROOF.md').read_text()
    reviewed = (ROOT / 'audit/PROOF.reviewed.md').read_text()
    needle = 'More generally, a finite quotient Q'
    require(old.count(needle) == 1, 'Correction target not unique')
    require(old.replace(needle, 'More generally, a nontrivial finite quotient Q') == reviewed,
            'Correction is not the exact one-word insertion')
    require(apply_patch(old, (ROOT / 'audit/PROOF_SCOPE_CORRECTION.patch').read_text()) == reviewed,
            'Preserved patch does not produce reviewed proof')
    runs = [
        ('checks/verify.py', 'checks/CHECK_RESULTS.json'),
        ('checks/degree_checks.py', 'checks/DEGREE_RESULTS.json'),
        ('checks/deletion_checks.py', 'checks/DELETION_RESULTS.json'),
        ('audit/independent_checks.py', 'audit/INDEPENDENT_RESULTS.json'),
        ('audit/independent_graph_checks.py', 'audit/INDEPENDENT_GRAPH_RESULTS.json'),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix='cycle-filling-replay-') as tmp:
        work = Path(tmp) / 'packet'
        shutil.copytree(ROOT, work)
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        env.pop('PYTHONPATH', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        for script, result in runs:
            completed = subprocess.run([sys.executable, '-B', script], cwd=work, env=env,
                                       text=True, capture_output=True, timeout=600)
            require(completed.returncode == 0, 'Control failed: ' + script + '\n' + completed.stderr)
            data = (work / result).read_bytes()
            require(data == (ROOT / result).read_bytes(), 'Replay differs: ' + result)
            require(json.loads(data)['status'] == 'pass', 'Nonpassing result: ' + result)
            results.append({'script': script, 'result': result, 'bytes': len(data), 'sha256': digest(data), 'byte_identical': True})
        for name, pin in manifest['files'].items():
            check_pin(work, name, pin)
    return {'status': 'pass', 'packet_files': len(expected), 'manifest_pins_verified': len(manifest['files']),
            'exact_one_word_correction': True, 'preserved_patch_applies': True, 'isolated_replay': results,
            'scope': 'Integrity and finite exact controls only; full ratio question unresolved, 5/5.'}

if __name__ == '__main__':
    try:
        print(json.dumps(verify(), indent=2))
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        raise SystemExit('FAIL: ' + str(exc))
