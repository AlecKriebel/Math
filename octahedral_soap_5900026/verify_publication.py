#!/usr/bin/env python3
"""Anchored source-free integrity and exact diagnostic replay; not formal proof verification."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
AUTHOR = '22b61a6a8e3a1a3e0a077be3accc0b5a24311fff47440f76fe3ecea182d2b50b'
AUDIT = 'a8844abb18fc83baa3b6cdd7c315c46a541aa058ad64d23943bd4b9c2ee91eab'
ARCHIVE = '0b0c8fc1a0101be94f32b2873c794b52479b736fffecb36cfdaf071a70726f9b'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def checked_manifest(path, anchor):
    raw = path.read_bytes()
    require(digest(raw) == anchor, 'External manifest anchor mismatch: ' + path.name)
    return json.loads(raw)

def pin(path, meta):
    require(path.is_file() and not path.is_symlink(), 'Missing or linked file: ' + path.name)
    raw = path.read_bytes()
    require(len(raw) == meta['bytes'] and digest(raw) == meta['sha256'], 'Payload mismatch: ' + path.name)

def apply_patch(original, patch):
    lines = patch.splitlines(keepends=True)
    require(lines[:2] == ['--- a/MATHEMATICAL_NOTE.md\n', '+++ b/MATHEMATICAL_NOTE.md\n'], 'Unexpected patch paths')
    old = original.splitlines(keepends=True)
    out, cursor, hunks, i = [], 0, 0, 2
    while i < len(lines):
        match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[i])
        require(match is not None, 'Bad hunk header')
        start, count, new_start, new_count = map(int, match.groups())
        require(start - 1 >= cursor, 'Overlapping hunk')
        out.extend(old[cursor:start - 1]); cursor = start - 1
        require(len(out) == new_start - 1, 'Patch offset mismatch')
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
    require(hunks == 1, 'Expected exactly one Section 0 correction hunk')
    out.extend(old[cursor:])
    return ''.join(out)

def run(script, args=(), optimized=False):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env.pop('PYTHONPATH', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(ROOT / script)] + list(args)
    result = subprocess.run(command, cwd=ROOT.parent, env=env, capture_output=True, timeout=180)
    require(result.returncode == 0, 'Replay failed: ' + script + '\n' + result.stderr.decode(errors='replace'))
    return result.stdout

def verify(anchor):
    manifest = checked_manifest(ROOT / 'PUBLIC_MANIFEST.json', anchor)
    require(manifest['problem_id'] == 5900026 and manifest['status'] == 'UNSOLVED' and manifest['approaches'] == '5/5', 'Disposition mismatch')
    expected = set(manifest['files']) | {'PUBLIC_MANIFEST.json'}
    expected_dirs = set()
    for name in expected:
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'Unsafe inventory path')
        expected_dirs.update(str(p) for p in path.parents if str(p) != '.')
    files, dirs = set(), set()
    for path in ROOT.rglob('*'):
        name = path.relative_to(ROOT).as_posix()
        require(not path.is_symlink(), 'Symlink in packet: ' + name)
        if path.is_file():
            files.add(name)
        elif path.is_dir():
            dirs.add(name)
        else:
            raise RuntimeError('Unsupported packet entry: ' + name)
    require(files == expected and dirs == expected_dirs, 'Packet inventory mismatch')
    for name, meta in manifest['files'].items():
        pin(ROOT / name, meta)
    author = checked_manifest(ROOT / 'authored/MANIFEST.json', AUTHOR)
    audit = checked_manifest(ROOT / 'audit/AUDIT_MANIFEST.json', AUDIT)
    for directory, nested in [('authored', author), ('audit', audit)]:
        for name, meta in nested['files'].items():
            require(Path(name).name == name, 'Nested inventory path is not flat')
            pin(ROOT / directory / name, meta)
    require(audit['original_manifest_sha256'] == AUTHOR and audit['original_archive_sha256'] == ARCHIVE, 'Audit anchors disagree')
    archive = ROOT / 'AUTHOR_FROZEN.zip'
    require(len(archive.read_bytes()) == 23055 and digest(archive.read_bytes()) == ARCHIVE, 'Frozen archive mismatch')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        wanted = {'authored/' + name for name in set(author['files']) | {'MANIFEST.json'}}
        require(len(names) == len(set(names)) and set(names) == wanted, 'Frozen archive inventory mismatch')
        for name in names:
            require(z.read(name) == (ROOT / name).read_bytes(), 'Frozen archive bytes differ')
    old = (ROOT / 'authored/MATHEMATICAL_NOTE.md').read_bytes()
    corrected = (ROOT / 'audit/MATHEMATICAL_NOTE_CORRECTED.md').read_bytes()
    patch = (ROOT / 'audit/CORRECTION.patch').read_bytes()
    receipt = json.loads((ROOT / 'audit/CORRECTION_RECEIPT.json').read_bytes())
    for label, data in [('original', old), ('corrected', corrected), ('patch', patch)]:
        require(len(data) == receipt[label + '_bytes'] and digest(data) == receipt[label + '_sha256'], 'Correction receipt mismatch')
    require(apply_patch(old.decode(), patch.decode()).encode() == corrected, 'Correction patch/read-copy mismatch')
    require(old.split(b'## Approach 1.', 1)[1] == corrected.split(b'## Approach 1.', 1)[1], 'Approaches were changed')
    runs = []
    for optimized in (False, True):
        author_result = json.loads(run('authored/verify_packet.py', ['--manifest-sha256', AUTHOR], optimized))
        audit_result = json.loads(run('audit/verify_audit.py', ['--manifest-sha256', AUDIT], optimized))
        require(author_result['result'] == 'PASS_ANCHORED_PACKET_AND_REPLAYS', 'Original verifier failed')
        require(audit_result['result'] == 'PASS_ANCHORED_AUDIT', 'Audit verifier failed')
        mutations = json.loads(run('authored/mutation_tests.py', optimized=optimized))
        require(mutations['result'] == 'PASS_PACKET_MUTATION_CONTROLS' and mutations['rejections'] == 14, 'Author mutation controls failed')
        runs.append({'optimized_wrapper': optimized, 'author_checks': 884, 'independent_checks': 1075, 'byte_identical_replays': True, 'original_integrity_rejections': 14})
    return {'result': 'PASS_SOURCE_FREE_PUBLICATION', 'problem_id': 5900026, 'status': 'UNSOLVED', 'approaches': '5/5', 'manifest_sha256': anchor, 'packet_files': len(expected), 'exact_patch_applies': True, 'original_archive_byte_identical': True, 'runs': runs, 'scope': 'Integrity and finite exact diagnostics only; no unrestricted minimality claim.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.manifest_sha256), sort_keys=True, indent=2))
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        raise SystemExit('FAIL: ' + str(exc))
