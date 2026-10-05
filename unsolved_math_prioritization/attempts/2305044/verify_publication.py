#!/usr/bin/env python3
"""Strict portable integrity and finite replay; not a formal proof certificate."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def safe_path(name):
    need(isinstance(name, str) and name and '\\' not in name, 'unsafe path')
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts
         and name == p.as_posix(), 'unsafe path')
    return p


def entries(rows):
    result = {}
    for row in rows:
        name = row['path']
        safe_path(name)
        need(name not in result, 'duplicate manifest path')
        need(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid byte count')
        need(isinstance(row['sha256'], str) and len(row['sha256']) == 64
             and all(c in '0123456789abcdef' for c in row['sha256']), 'invalid hash')
        result[name] = row
    return result


def check_files(root, expected):
    for name, row in expected.items():
        data = (root / name).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'],
             'content mismatch: ' + name)


def inventory():
    need(not any(p.is_symlink() for p in ROOT.rglob('*')), 'symlink in packet')
    expected = entries(read_json(ROOT / 'PUBLICATION_MANIFEST.json')['files'])
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    need(actual == set(expected) | {'PUBLICATION_MANIFEST.json'}, 'strict inventory mismatch')
    check_files(ROOT, expected)
    return len(expected)


def check_archive(folder, filename, expected_hash, expected_size, members):
    p = ROOT / folder / filename
    data = p.read_bytes()
    need(sha(data) == expected_hash and len(data) == expected_size, 'frozen ZIP identity')
    with zipfile.ZipFile(p) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)) and set(names) == members, 'ZIP inventory')
        need(archive.testzip() is None, 'ZIP CRC')
        for info in archive.infolist():
            safe_path(info.filename)
            need(not stat.S_ISLNK(info.external_attr >> 16), 'ZIP symlink')
            need(archive.read(info.filename) == (ROOT / folder / info.filename).read_bytes(),
                 'ZIP member mismatch: ' + info.filename)


# Frozen code uses asserts. optimize=0 explicitly retains them even when the
# verifier or subprocess host runs under -O. No frozen program is rewritten.
RUNNER = '''import pathlib,sys
p=pathlib.Path(sys.argv[1])
source=p.read_bytes()
if len(sys.argv)>2:
    source += b'\\nassert False, "assertion negative control"\\n'
exec(compile(source,str(p),'exec',optimize=0),{'__name__':'__main__','__file__':str(p)})
'''


def main():
    need(sys.argv[1:] in ([], ['--integrity-only']), 'unknown arguments')
    count = inventory()
    author = read_json(ROOT / 'freeze/FROZEN_MANIFEST.json')
    expected = entries(author['files'])
    check_files(ROOT / 'freeze', expected)
    need(sha((ROOT / 'freeze/FROZEN_MANIFEST.json').read_bytes()) ==
         'e66e5ab5db186297c965c68f1c073cfc3598bdf4f9c58c5efd8496f19c56d98b',
         'frozen author manifest identity')
    check_archive('freeze', 'SAFE_AUDIT_PACKET.zip',
                  '3d0a57a4fce83269bd76bf9f0d879ce02892f732a12d4088af9923c4f76adb2e',
                  21085, set(expected) | {'FROZEN_MANIFEST.json'})
    audit = read_json(ROOT / 'independent_audit/AUDIT_RECEIPT.json')
    checked = entries(audit['files'])
    check_files(ROOT / 'independent_audit', checked)
    check_archive('independent_audit', 'SAFE_INDEPENDENT_AUDIT.zip',
                  '462d1e51bc68dd9416262f70774c96bc913bca21aba062aa06c099e9b51a01d2',
                  9753, set(checked) | {'AUDIT_RECEIPT.json'})
    need(audit['verdict'] == 'PASS_SCOPED' and not audit['blocking_defects'], 'scoped audit gate')
    for key in ('dunster_global_numerics_certified', 'full_beta1_literature_proof_audit',
                'historical_raw_dataset_equality_certified', 'novelty_claim_approved'):
        need(audit[key] is False, 'audit limit changed: ' + key)
    result = {'result': 'PASS', 'strict_inventory': True, 'files_verified': count,
              'frozen_archives_verified': 2, 'frozen_archive_members_verified': 20,
              'full_beta1_proof_independently_audited': False,
              'global_numerics_certified': False, 'historical_corpora_verified': False,
              'novelty_claim': False, 'analytic_proofs_formalized': False}
    if sys.argv[1:] == ['--integrity-only']:
        result['replay'] = 'not requested'
    else:
        jobs = [('freeze/verify_exact.py', 'freeze/EXACT_CHECKS.json'),
                ('freeze/check_bernstein.py', 'freeze/BERNSTEIN_CHECKS.json'),
                ('freeze/check_sector_numerical.py', 'freeze/SECTOR_NUMERICAL_CHECKS.json'),
                ('independent_audit/independent_checks.py', 'independent_audit/INDEPENDENT_CHECKS.json')]
        for flags in ([], ['-O']):
            for script, output in jobs:
                run = subprocess.run([sys.executable, *flags, '-B', '-c', RUNNER,
                                      str(ROOT / script)], capture_output=True)
                need(run.returncode == 0, 'replay failed: ' + script + '\n' + run.stderr.decode())
                need(run.stdout == (ROOT / output).read_bytes(), 'replay output differs: ' + output)
            control = subprocess.run([sys.executable, *flags, '-B', '-c', RUNNER,
                                      str(ROOT / 'freeze/verify_exact.py'), 'negative'],
                                     capture_output=True)
            need(control.returncode != 0 and b'assertion negative control' in control.stderr,
                 'frozen assertions were disabled')
        result.update(replay='PASS', programs_per_mode=4, python_modes=2,
                      frozen_assertions_active=True, assertion_negative_controls=2,
                      independent_recurrence_convolution_cases=1080,
                      candidate_cubic_cases=616, candidate_endpoint_cases=496,
                      candidate_recurrence_cases=192, prior_construction_cases=38,
                      independent_existence_endpoint_cases=30,
                      sector_sanity_cases=80, sector_sanity_is_rigorous=False)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
