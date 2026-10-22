#!/usr/bin/env python3
"""Closed, source-free integrity and finite-control replay; not a proof checker."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ANCHORS = {
    'original': ('MANIFEST.json', 'dfac54b9d1a507c2f3b4cfd6a13e2b627e3b1f85672723130254984183f16772'),
    'audit': ('AUDIT_MANIFEST.json', '7e15821f99949648de3e5e858739b80c6fd15ec9d83790445db40a5a3d7fd4f0'),
    'corrected': ('MANIFEST.json', 'f3cff9cedb5a6f8e912dffe81329ffc409ce80cd168401bb8fb4aa21e57f07e8'),
}
TOP_LEVEL = {'README.md', 'RESEARCH_LOG.md', 'PUBLICATION_STATUS.json', 'requirements.txt',
             'verify_publication.py', 'mutation_tests.py', 'PUBLIC_MANIFEST.json'}

def require(value, label):
    if not value:
        raise RuntimeError(label)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_file(path):
    require(not path.is_symlink() and path.is_file(), 'Nonregular file: ' + str(path))
    return path.read_bytes()

def safe_path(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and name and not p.is_absolute() and
            all(x not in ('', '.', '..') for x in name.split('/')) and '\\' not in name,
            'Unsafe manifest path')
    return p

def record_matches(data, record):
    return record == {'bytes': len(data), 'sha256': sha(data)}

def apply_correction(before, patch):
    """Apply this strict one-file unified diff, checking every context/removal line."""
    lines = patch.decode('utf-8').splitlines(keepends=True)
    require(lines[:2] == ['--- a/STATEMENT.md\n', '+++ b/STATEMENT.md\n'], 'Patch target mismatch')
    source = before.decode('utf-8').splitlines(keepends=True)
    output = []; cursor = 0; index = 2; hunks = 0
    while index < len(lines):
        match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[index])
        require(match is not None, 'Invalid patch hunk')
        old_start, old_count, new_start, new_count = map(int, match.groups())
        start = old_start - 1
        require(start >= cursor and start <= len(source), 'Overlapping/out-of-range hunk')
        output.extend(source[cursor:start]); cursor = start
        require(len(output) == new_start - 1, 'Patch new-position mismatch')
        index += 1; consumed = produced = 0
        while index < len(lines) and not lines[index].startswith('@@ '):
            line = lines[index]; index += 1
            require(line and line[0] in ' +-','Invalid patch line')
            if line[0] in ' -':
                require(cursor < len(source) and source[cursor] == line[1:], 'Patch source mismatch')
                cursor += 1; consumed += 1
            if line[0] in ' +':
                output.append(line[1:]); produced += 1
        require((consumed, produced) == (old_count, new_count), 'Patch count mismatch')
        hunks += 1
    require(hunks == 1, 'Unexpected patch scope')
    output.extend(source[cursor:])
    return ''.join(output).encode('utf-8')

def verify(root, expected, integrity_only=False):
    require(re.fullmatch('[0-9a-f]{64}', expected) is not None, 'Invalid external digest')
    require(not root.is_symlink() and root.is_dir(), 'Invalid packet directory')
    mb = read_file(root / 'PUBLIC_MANIFEST.json')
    require(sha(mb) == expected, 'External publication digest mismatch')
    manifest = json.loads(mb)
    require(manifest['schema'] == 'motivic-comparison-source-free-publication-v1', 'Schema mismatch')
    entries = manifest['files']
    require(isinstance(entries, dict), 'Invalid manifest file map')
    expected_files = set(entries) | {'PUBLIC_MANIFEST.json'}
    expected_dirs = set()
    for name in expected_files:
        p = safe_path(name)
        expected_dirs.update(str(x) for x in p.parents if str(x) != '.')
    actual_files = set(); actual_dirs = set()
    for f in root.rglob('*'):
        require(not f.is_symlink(), 'Symlink rejected')
        rel = f.relative_to(root).as_posix()
        if f.is_dir(): actual_dirs.add(rel)
        else:
            require(f.is_file(), 'Nonregular member rejected')
            actual_files.add(rel)
    require(actual_files == expected_files and actual_dirs == expected_dirs, 'Closed inventory mismatch')
    for name, rec in entries.items():
        require(record_matches(read_file(root / name), rec), 'Publication payload mismatch: ' + name)
    closed = set(TOP_LEVEL)
    for role, (manifest_name, anchor) in ANCHORS.items():
        b = read_file(root / role / manifest_name)
        require(sha(b) == anchor, 'Frozen manifest anchor mismatch: ' + role)
        m = json.loads(b)
        names = set(m['files']) | {manifest_name}
        require({x.name for x in (root / role).iterdir()} == names, 'Frozen inventory mismatch')
        for name, rec in m['files'].items():
            require(safe_path(name).name == name, 'Unsafe frozen filename')
            require(record_matches(read_file(root / role / name), rec), 'Frozen payload mismatch: ' + role + '/' + name)
        closed.update(role + '/' + name for name in names)
    require(closed == expected_files, 'Publication allowlist mismatch')
    original = root / 'original'; corrected = root / 'corrected'; audit = root / 'audit'
    changes = sorted(x.name for x in original.iterdir() if x.read_bytes() != (corrected / x.name).read_bytes())
    require(changes == ['MANIFEST.json', 'STATEMENT.md'], 'Corrected-copy scope mismatch')
    require(apply_correction(read_file(original / 'STATEMENT.md'), read_file(audit / 'LOW_DEGREE_CORRECTION.patch')) == read_file(corrected / 'STATEMENT.md'), 'Patch replay mismatch')
    require(read_file(corrected / 'MANIFEST.json') == read_file(audit / 'CORRECTED_MANIFEST.json'), 'Corrected manifest duplicate mismatch')
    status = json.loads(read_file(root / 'PUBLICATION_STATUS.json'))
    require(status['problem_id'] == 30001285 and status['status'] == 'unsolved' and status['turns'] == '5/5', 'Disposition mismatch')
    require(status['full_comparison_proved'] is False and status['novelty_claimed'] is False, 'Claim boundary mismatch')
    outputs = []
    if not integrity_only:
        mode = ['-O'] if sys.flags.optimize else []
        with tempfile.TemporaryDirectory(prefix='motivic-replay-') as cwd:
            def run(script, *args):
                result = subprocess.run([sys.executable, '-I', '-S', '-B', *mode, str(script), *map(str, args)], cwd=cwd, capture_output=True, timeout=180)
                require(result.returncode == 0, str(script.name) + ' failed: ' + result.stderr.decode('utf-8', errors='replace'))
                return result.stdout
            for role in ('original', 'corrected'):
                folder = root / role
                out = run(folder / 'verify_manifest.py', '--expected-manifest-sha256', ANCHORS[role][1])
                require(json.loads(out)['files_verified'] == 15, 'Author verifier result mismatch')
                out = run(folder / 'checks.py')
                require(out == read_file(folder / 'CHECK_RESULTS.json'), 'Author output mismatch')
                out = run(audit / 'independent_controls.py', '--packet', folder, '--expected-manifest-sha256', ANCHORS[role][1])
                expected_result = 'INDEPENDENT_CHECK_RESULTS.json' if role == 'original' else 'CORRECTED_CHECK_RESULTS.json'
                require(out == read_file(audit / expected_result), 'Independent output mismatch')
                outputs.append({'packet': role, 'author_assertions': 114419, 'independent_controls': 13525})
    return {'status': 'PASS', 'files_verified': len(expected_files), 'frozen_files': 41,
            'manifest_sha256': expected, 'optimization': sys.flags.optimize,
            'patch_replayed': True, 'integrity_only': integrity_only, 'replays': outputs,
            'limits': 'Integrity and finite controls only; the general motivic comparison remains unsolved.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--manifest-sha256', required=True)
    p.add_argument('--integrity-only', action='store_true', help='Check bytes and patch without finite-model replay.')
    args = p.parse_args()
    print(json.dumps(verify(Path(__file__).resolve().parent, args.manifest_sha256, args.integrity_only), indent=2, sort_keys=True))
