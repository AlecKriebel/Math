#!/usr/bin/env python3
"""Source-free integrity and finite controls. Not a formal/asymptotic proof checker."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
AUTHOR = '78b14d14c630370528d17eda1cc82dd7a4f707f7643288fb85153ba52ac09866'
AUDIT = '426fff16e27b5c475602d0dad26e7c25018ebda7fed6aa97f521362086e12bcf'
ARCHIVES = {
    'AUTHOR_FREEZE.zip': ('author', 'MANIFEST.json', 19670, 'aefc84ee9e468a4c39bdf06a4938948f34e98c939365023bba30f903cd771a4f'),
    'AUDIT_PACKET.zip': ('audit', 'AUDIT_MANIFEST.json', 22883, '48960aa6f74cd82e7329283b17a3f48fa0a484080ab26d99d356069cc5a35043'),
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe(name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name and name != '.', 'Unsafe inventory path')

def anchored(path, anchor):
    raw = path.read_bytes()
    require(digest(raw) == anchor, 'External manifest anchor mismatch: ' + path.name)
    return json.loads(raw)

def pin(path, meta):
    require(path.is_file() and not path.is_symlink(), 'Missing or linked file: ' + path.name)
    raw = path.read_bytes()
    require(len(raw) == meta['bytes'] and digest(raw) == meta['sha256'], 'Payload mismatch: ' + path.name)

def replay(script, expected, optimized):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env.pop('PYTHONPATH', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(ROOT / script)]
    result = subprocess.run(command, cwd=ROOT.parent, env=env, capture_output=True, timeout=240)
    require(result.returncode == 0, 'Replay failed: ' + script + '\n' + result.stderr.decode(errors='replace'))
    require(result.stdout == (ROOT / expected).read_bytes(), 'Replay output differs from frozen bytes: ' + script)
    return json.loads(result.stdout)

def verify(anchor):
    manifest = anchored(ROOT / 'PUBLIC_MANIFEST.json', anchor)
    require(manifest['problem_id'] == 30005926 and manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Disposition mismatch')
    expected = set(manifest['files']) | {'PUBLIC_MANIFEST.json'}
    expected_dirs = set()
    for name in expected:
        safe(name)
        expected_dirs.update(str(p) for p in PurePosixPath(name).parents if str(p) != '.')
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
    author = anchored(ROOT / 'author/MANIFEST.json', AUTHOR)
    audit = anchored(ROOT / 'audit/AUDIT_MANIFEST.json', AUDIT)
    for directory, nested in [('author', author), ('audit', audit)]:
        names = [m['path'] for m in nested['files']]
        require(len(names) == len(set(names)), 'Duplicate nested manifest path')
        for meta in nested['files']:
            safe(meta['path'])
            pin(ROOT / directory / meta['path'], meta)
    require(audit['author_report_sha256'] == '6bb6b843148e43497d4be8cc1ab8734c9f96b22e9a8215d1c16002037fb2419a', 'Audit report anchor disagreement')
    for name, (directory, inner_manifest, size, sha) in ARCHIVES.items():
        pin(ROOT / name, {'bytes': size, 'sha256': sha})
        nested = author if directory == 'author' else audit
        wanted = {m['path'] for m in nested['files']} | {inner_manifest}
        with zipfile.ZipFile(ROOT / name) as z:
            names = z.namelist()
            require(len(names) == len(set(names)) and set(names) == wanted, 'Archive inventory mismatch')
            for member in names:
                require(z.read(member) == (ROOT / directory / member).read_bytes(), 'Archive and loose bytes differ')
    verdict = json.loads((ROOT / 'audit/AUDIT_VERDICT.json').read_bytes())
    require(verdict['verdict'] == 'scoped_acceptance_no_correction_required', 'Audit acceptance mismatch')
    require(len(verdict['claims']) == 12 and all(c['verdict'] == 'accepted_with_stated_scope' for c in verdict['claims']), 'Claim count or scope mismatch')
    require(not verdict['full_target_solved'] and not verdict['diameter_constant_proved'] and not verdict['ratio_three_proved'] and not verdict['mathematical_patch_required'], 'Claim boundary mismatch')
    require(verdict['author_manifest_sha256'] == AUTHOR and verdict['author_freeze_sha256'] == ARCHIVES['AUTHOR_FREEZE.zip'][3], 'Audit freeze disagreement')
    runs = []
    for optimized in (False, True):
        a = replay('author/verify.py', 'author/RESULTS.json', optimized)
        b = replay('audit/checks/independent_checks.py', 'audit/checks/INDEPENDENT_RESULTS.json', optimized)
        require(a['all_controls_passed'] and a['total_control_checks'] == 57304 and not a['full_target_solved'], 'Author control mismatch')
        require(b['all_checks_passed'] and b['total_checks'] == 15042 and not b['full_target_solved'], 'Independent control mismatch')
        require(verdict['author_exact_controls'] == 57292 and verdict['author_decimal_diagnostics'] == 12, 'Exact/Decimal split mismatch')
        runs.append({'optimized': optimized, 'author_exact_controls': 57292, 'author_decimal_diagnostics': 12, 'independent_controls': 15042, 'byte_identical_replay': True})
    return {'result': 'PASS_SOURCE_FREE_PUBLICATION', 'problem_id': 30005926, 'status': 'unsolved', 'turns': '5/5', 'accepted_scoped_results': 12, 'mathematical_changes': 0, 'manifest_sha256': anchor, 'packet_files': len(expected), 'archives_byte_identical': True, 'runs': runs, 'scope': 'Anchored integrity and finite controls only; diameter constant and ratio three remain unresolved.'}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest-sha256', required=True)
    args = ap.parse_args()
    try:
        print(json.dumps(verify(args.manifest_sha256), sort_keys=True, indent=2))
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        raise SystemExit('FAIL: ' + str(exc))
