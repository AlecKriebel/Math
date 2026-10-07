#!/usr/bin/env python3
"""Portable integrity, exact-check replay, and edition-chain verification.

Run with Python 3.10+ and SymPy installed. This is not a formal proof verifier.
Original scripts execute unchanged in an isolated temporary layout.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
PINS = {
    'PROOF.md': '657f458cf3eece42eef9c8dfd46a7c20aaaf363e3a6744f396af3c7389fa43a3',
    'PACKAGE_MANIFEST.json': '4ae078843413493dc3548e1390218ce437abd2a2dfa49049c52629432a36652c',
    'audits/INDEPENDENT_ACCEPTANCE_A.md': '58e579e656f7528c35557c70e4f3262b0ceceb3c945a9f8db11fc57413947913',
    'audits/INDEPENDENT_ACCEPTANCE_B.md': '417519fcf640c04581927d4b90263f7dc28d4ecc1dfdea29f35eddf836c96f88',
    'audits/reviewer_b/independent_checks.py': 'afeb7d7cbb80a4a3e466e2f9370a8ccd49c59bb0cda5ffb5353fe52a0720b626',
    'audits/reviewer_b/INDEPENDENT_CHECK_RESULTS.json': 'bdd982cf5ebdf55cbce62b31e1604f7ac5313fb007c47d46afe8e562b7303389',
}

def require(test, message):
    if not test:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def integrity():
    manifest = json.loads((ROOT / 'PUBLICATION_MANIFEST.json').read_text())
    entries = manifest['files']
    names = [e['file'] for e in entries]
    require(len(names) == len(set(names)), 'Duplicate manifest entry')
    expected = set(names) | {'PUBLICATION_MANIFEST.json'}
    expected_dirs = {p.as_posix() for n in expected for p in Path(n).parents if p != Path('.')}
    actual, actual_dirs = set(), set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink in packet')
        name = p.relative_to(ROOT).as_posix()
        if p.is_file():
            actual.add(name)
        elif p.is_dir():
            actual_dirs.add(name)
        else:
            raise RuntimeError('Unsupported filesystem object')
    require(actual == expected, 'Missing or extra packet file')
    require(actual_dirs == expected_dirs, 'Missing or extra packet directory')
    for e in entries:
        p = Path(e['file'])
        require(not p.is_absolute() and '..' not in p.parts, 'Unsafe manifest path')
        data = (ROOT / p).read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'Integrity failure: '+e['file'])
    for name, digest in PINS.items():
        require(sha((ROOT / name).read_bytes()) == digest, 'Frozen pin failure: '+name)
    original = json.loads((ROOT / 'PACKAGE_MANIFEST.json').read_text())
    for e in original['files']:
        data = (ROOT / e['file']).read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'Original author pin failure')
    return len(actual)

def apply_unified(data, patch, reverse=False):
    """Apply these single-file unified diffs with exact contexts and counts."""
    source = data.decode('utf-8').splitlines(keepends=True)
    lines = patch.decode('utf-8').splitlines(keepends=True)
    require(len(lines) >= 3 and lines[0].startswith('--- ') and lines[1].startswith('+++ '), 'Invalid patch header')
    out, pos, i = [], 0, 2
    while i < len(lines):
        m = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n', lines[i])
        require(m is not None, 'Invalid hunk header')
        old_start, old_count, new_start, new_count = [int(m.group(k) or 1) for k in range(1,5)]
        if reverse:
            old_start, new_start = new_start, old_start
            old_count, new_count = new_count, old_count
        start = old_start - 1 if old_count else old_start
        require(pos <= start <= len(source), 'Overlapping or out-of-range hunk')
        out.extend(source[pos:start]); pos = start; i += 1
        consumed = produced = 0
        while i < len(lines) and not lines[i].startswith('@@ '):
            sign, value = lines[i][:1], lines[i][1:]
            require(sign in (' ', '+', '-'), 'Unsupported patch line')
            if reverse and sign != ' ':
                sign = '+' if sign == '-' else '-'
            if sign in (' ', '-'):
                require(pos < len(source) and source[pos] == value, 'Patch context mismatch')
                pos += 1; consumed += 1
            if sign in (' ', '+'):
                out.append(value); produced += 1
            i += 1
        require((consumed, produced) == (old_count, new_count), 'Patch hunk counts mismatch')
    out.extend(source[pos:])
    return ''.join(out).encode('utf-8')

def editions():
    history = json.loads((ROOT / 'EDITION_HISTORY.json').read_text())
    v4 = (ROOT / 'PROOF.md').read_bytes()
    patches = {e['file']: (ROOT / 'corrections' / e['file']).read_bytes() for e in history['patches']}
    for e in history['patches']:
        data = patches[e['file']]
        require(sha(data) == e['sha256'] and len(data) == e['bytes'], 'Edition patch pin failure')
    v2 = apply_unified(v4, patches['CITATION_CORRECTION.patch'], reverse=True)
    v1 = apply_unified(v2, patches['NUMERICAL_CORRECTION_v1_to_v2.patch'], reverse=True)
    v3 = apply_unified(v4, patches['POLYSTABILITY_CITATION_v3_to_v4.patch'], reverse=True)
    versions = dict(zip([e['file'] for e in history['editions']], (v1, v2, v3, v4)))
    for e in history['editions']:
        data = versions[e['file']]
        require(sha(data) == e['sha256'] and len(data) == e['bytes'], 'Edition hash mismatch: '+e['file'])
    for record in json.loads((ROOT / 'checks/PATCH_VERIFICATION.json').read_text()):
        result = apply_unified(versions[record['applied_to']], patches[record['patch']])
        require(result == versions[record['matches']] and sha(result) == record['after_sha256'], 'Forward patch mismatch')
    return {'edition_hashes_verified': 4, 'forward_and_reverse_patches_verified': 3}

def replay():
    import sympy
    with tempfile.TemporaryDirectory(prefix='fano-exact-check-') as tmp:
        dest = Path(tmp)
        tasks = [
            ('checks/verify_construction.py', 'checks/CHECK_RESULTS.json'),
            ('audits/reviewer_b/independent_checks.py', 'audits/reviewer_b/INDEPENDENT_CHECK_RESULTS.json'),
        ]
        proof_path = dest / 'authored/PROOF_CANDIDATE_v4.md'
        proof_path.parent.mkdir(); shutil.copyfile(ROOT / 'PROOF.md', proof_path)
        for script, result in tasks:
            path = dest / script; path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / script, path)
            run = subprocess.run([sys.executable, '-B', str(path)], cwd=dest, text=True, capture_output=True, timeout=300)
            require(run.returncode == 0, 'Exact replay failed: '+script+'\n'+run.stdout+run.stderr)
            require((dest / result).read_bytes() == (ROOT / result).read_bytes(), 'Result byte mismatch: '+result)
    return {'author_results_byte_identical': True, 'independent_results_byte_identical': True,
            'python_version': sys.version.split()[0], 'sympy_version': sympy.__version__}

def main():
    require(not sys.flags.optimize, 'Run with assertions enabled, without -O or PYTHONOPTIMIZE')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    result = {'packet_files_verified': integrity(), **editions()}
    if not args.integrity_only:
        result.update(replay())
    result['scope'] = 'Integrity and auxiliary exact checks only; mathematical acceptance is in the two AI audit reports. No formal-proof or novelty certification.'
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
