#!/usr/bin/env python3
"""Fail-closed, portable integrity and exact replay of bounded Kato–Milne partials."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).absolute().parent
AUTHOR = 'kato_milne_30003791'
AUDIT = 'kato_milne_30003791_independent_audit'
PINS = {
    AUTHOR + '/MANIFEST.json': '84639769d8b1e76e65c4f9b146d747bc00ac78583f8dc76e93211c0a2b9e26b2',
    AUDIT + '/AUDIT_MANIFEST.json': 'e8fe667ea2aae850ee5371b8085fa05ddf317627490f3bedcf616bf5c38bcf16',
    'KATO_MILNE_30003791_SAFE_FREEZE.zip': '6ab69c7efbb362416f44de1fb8c642eaa5ce0877aec1869b67859012f2f428e5',
    'KATO_MILNE_30003791_INDEPENDENT_AUDIT.zip': '60fbfde14219d33991a5d7ad15026ca9ee3ed5cd67e5509ee5c86c423e0df32f',
    'PUBLICATION_STATUS.json': 'cc8f5fedef66b2dc76079c2cc1af43621684db21fb7fa015762f72a574d5e7dc',
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'Unsafe path')
    return p

def integrity():
    require(ROOT.is_dir() and not ROOT.is_symlink(), 'Regular packet directory required')
    mf = ROOT / 'PUBLICATION_MANIFEST.json'
    require(mf.is_file() and not mf.is_symlink(), 'Regular publication manifest required')
    before = {'PUBLICATION_MANIFEST.json': mf.read_bytes()}
    manifest = json.loads(before['PUBLICATION_MANIFEST.json'])
    require(manifest['problem_id'] == '30003791', 'Wrong problem')
    require(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong status')
    rows = manifest['files']
    records = {r['path']: r for r in rows}
    require(len(records) == len(rows) == 26, 'Wrong payload count or duplicate')
    expected_dirs = set()
    for name in records:
        for parent in safe(name).parents:
            if str(parent) != '.':
                expected_dirs.add(str(parent))
    paths = list(ROOT.rglob('*'))
    for p in paths:
        require(not p.is_symlink(), 'Symlink input: ' + p.name)
        require(p.is_file() or p.is_dir(), 'Special input')
    files = {p.relative_to(ROOT).as_posix() for p in paths if p.is_file()}
    dirs = {p.relative_to(ROOT).as_posix() for p in paths if p.is_dir()}
    require(files == set(records) | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing file')
    require(dirs == expected_dirs, 'Unexpected directory')
    for name, row in records.items():
        b = (ROOT / name).read_bytes()
        require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'File integrity: ' + name)
        before[name] = b
    for name, pin in PINS.items():
        require(digest(before[name]) == pin, 'Frozen binding: ' + name)
    for folder, mfname, archive, count, size in [
        (AUTHOR, 'MANIFEST.json', 'KATO_MILNE_30003791_SAFE_FREEZE.zip', 9, 20996),
        (AUDIT, 'AUDIT_MANIFEST.json', 'KATO_MILNE_30003791_INDEPENDENT_AUDIT.zip', 12, 20599),
    ]:
        inner = json.loads(before[folder + '/' + mfname])
        names = {mfname}
        for row in inner['files']:
            name = row['path']; safe(name)
            require(name not in names, 'Duplicate frozen entry')
            names.add(name)
            b = before[folder + '/' + name]
            require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'Frozen member')
        require(len(names) == count, 'Wrong frozen count')
        require({p.relative_to(ROOT / folder).as_posix() for p in (ROOT / folder).rglob('*') if p.is_file()} == names, 'Frozen file set')
        require(len(before[archive]) == size, 'Archive size')
        with zipfile.ZipFile(ROOT / archive) as z:
            require(len(z.infolist()) == count and set(z.namelist()) == names, 'Archive allowlist')
            for entry in z.infolist():
                safe(entry.filename)
                require(not stat.S_ISLNK(entry.external_attr >> 16), 'Archive symlink')
                require(z.read(entry.filename) == before[folder + '/' + entry.filename], 'Archive member bytes')
    verdict = json.loads(before[AUDIT + '/AUDIT_VERDICT.json'])
    require(verdict['verdict'] == 'PASS' and not verdict['required_corrections'], 'Audit gate')
    require(verdict['target_status']['novelty_certified'] is False, 'Audit novelty scope')
    require(verdict['target_status']['universal_field_counterexample_certified'] is False, 'Universal field scope')
    status = json.loads(before['PUBLICATION_STATUS.json'])
    require(status['status'] == 'unsolved' and status['turns'] == '5/5', 'Publication status')
    require(status['unrestricted_odd_prime_solution'] is False, 'Unrestricted scope')
    return before

def run(script, optimized):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    env.pop('PYTHONPATH', None); env.pop('PYTHONHOME', None)
    return subprocess.check_output([sys.executable, '-B', *(['-O'] if optimized else []), str(ROOT / script)], cwd=ROOT, env=env)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    require(sys.version_info >= (3, 9), 'Python 3.9+ required')
    before = integrity()
    result = {'result': 'PASS', 'problem_id': '30003791', 'status': 'unsolved', 'turns': '5/5', 'packet_files': 27, 'frozen_files_preserved': 21, 'archives_preserved': 2, 'publication_manifest_sha256': digest(before['PUBLICATION_MANIFEST.json'])}
    if not args.integrity_only:
        for optimized in [False, True]:
            require(run(AUTHOR + '/code/check_controls.py', optimized) == before[AUTHOR + '/verification/controls.json'], 'Author replay mismatch')
            require(json.loads(run(AUTHOR + '/code/verify_manifest.py', optimized))['status'] == 'PASS', 'Author integrity replay')
            require(run(AUDIT + '/code/independent_verify.py', optimized) == before[AUDIT + '/verification/independent_controls.json'], 'Independent replay mismatch')
            require(json.loads(run(AUDIT + '/code/verify_audit_manifest.py', optimized))['status'] == 'PASS', 'Audit integrity replay')
            require(run(AUDIT + '/code/check_tamper_controls.py', optimized) == before[AUDIT + '/verification/negative_integrity_controls.json'], 'Frozen negative controls mismatch')
        result.update(author_replay_byte_equal=True, independent_replay_byte_equal=True, frozen_integrity_negative_controls=4, normal_and_optimized=True, author_artin_schreier_controls=10140, author_exact_form_controls=38090, independent_matrix_identities=60, independent_p_basis_reconstructions=600, independent_derivation_comparisons=1800, independent_degree_cases=46)
    require(integrity() == before, 'Files changed during replay')
    result['scope'] = 'Bounded elementary partials only; no unrestricted odd-prime solution, universal-field counterexample, novelty or global-openness certification.'
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
