#!/usr/bin/env python3
"""Read-only replay of an adverse historical review; PASS is not publication approval."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT/'public_extracted/qss-self-duality-verification'
MANIFEST = ROOT/'OWNED_NAMESPACE_MANIFEST.json'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def pin(path):
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                mode=f'{stat.S_IMODE(path.stat().st_mode):04o}')


def inventory():
    files, directories = {}, {}
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'Symlink in reviewer namespace: '+str(p))
        name = p.relative_to(ROOT).as_posix()
        if p.is_file() and p != MANIFEST:
            files[name] = pin(p)
        elif p.is_dir():
            directories[name] = f'{stat.S_IMODE(p.stat().st_mode):04o}'
    return dict(files=files, directories=directories)


def run(code, flags=(), cwd=PACKAGE):
    argv = [sys.executable, '-B', str(code), *flags]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True)
    return result, dict(argv=argv, cwd=str(cwd), exit_code=result.returncode,
                        stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr),
                        stdout_sha256=hashlib.sha256(result.stdout).hexdigest(),
                        stderr_sha256=hashlib.sha256(result.stderr).hexdigest())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scope', choices=('public', 'full'), required=True)
    args = ap.parse_args()
    require(__debug__, 'Run without optimization; reproduced public controls use assertions')
    manifest = json.loads(MANIFEST.read_text())
    require(manifest['sealed'] is False, 'This reviewer has no self-seal authority')
    require(manifest['review_verdict'] == 'REPAIR_REQUIRED', 'Adverse verdict changed')
    before = inventory()
    public_names = {name for name in manifest['files']
                    if name.startswith('public_extracted/') or
                    (name.startswith('candidate/') and not name.endswith('/build_supplement.py')) or
                    name in ('independent_controls.py', 'verify_review.py', 'ZIP_MEMBER_MANIFEST.json', 'REPORT.md')}
    selected = set(manifest['files']) if args.scope == 'full' else public_names
    if args.scope == 'full':
        require(f'{stat.S_IMODE(ROOT.stat().st_mode):04o}' == manifest['root_mode'], 'Owned root-mode mismatch')
        require(before['files'] == manifest['files'], 'Full owned file inventory/pin mismatch')
        require(before['directories'] == manifest['directories'], 'Full owned directory-mode mismatch')
        require(pin(MANIFEST)['mode'] == '0644', 'Namespace manifest mode mismatch')
    else:
        require({n for n in before['files'] if n.startswith('public_extracted/')} ==
                {n for n in selected if n.startswith('public_extracted/')}, 'Public extracted inventory mismatch')
    for name in selected:
        require(name in before['files'] and before['files'][name] == manifest['files'][name],
                'Selected pin mismatch: '+name)
    # The stored six-input source paths are provenance only: replay uses owned copies.
    if args.scope == 'full':
        for record in json.loads((ROOT/'CANDIDATE_INPUT_MANIFEST.json').read_text())['inputs']:
            p = Path(record['snapshot'])
            require(p.is_relative_to(ROOT), 'Candidate snapshot escaped owned namespace')
            require(pin(p) == {k:record[k] for k in ('bytes','sha256','mode')}, 'Frozen candidate pin mismatch')
        for record in json.loads((ROOT/'SOURCE_INPUT_MANIFEST.json').read_text())['inputs']:
            p = Path(record['snapshot'])
            expected = dict(bytes=record['bytes'], sha256=record['sha256'], mode=f'{int(record["mode"],8):04o}')
            require(pin(p) == expected, 'Frozen initial primary pin mismatch')
        for record in json.loads((ROOT/'ADDITIONAL_PRIMARY_INPUTS.json').read_text()):
            p = ROOT/'source_snapshots'/record['name']
            require(pin(p)['bytes'] == record['bytes'] and pin(p)['sha256'] == record['sha256'], 'Additional primary pin mismatch')
    members = json.loads((ROOT/'ZIP_MEMBER_MANIFEST.json').read_text())['members']
    zpath = ROOT/'candidate/qss-self-duality-verification.zip'
    with zipfile.ZipFile(zpath) as z:
        require(len(z.infolist()) == len(members) == 32, 'Frozen ZIP member count changed')
        require(set(z.namelist()) == {r['member'] for r in members}, 'Frozen ZIP inventory changed')
        for record in members:
            name = record['member']
            require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe ZIP path')
            data = z.read(name)
            require(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], 'ZIP body mismatch')
            require(stat.S_IMODE(z.getinfo(name).external_attr >> 16) == 0o644, 'ZIP member mode changed')
            require((ROOT/'public_extracted'/name).read_bytes() == data, 'Extracted ZIP differs')
    runs = []
    result, receipt = run(PACKAGE/'verify_supplement.py')
    require(result.returncode == 0 and not result.stderr, 'Public integrity verifier failed')
    runs.append(dict(name='submitted_integrity', **receipt))
    for name, code in (('priority','priority/verify_public.py'), ('honda','controls/check_realization.py'),
                       ('semilinear','controls/verify_semilinear.py'), ('intrinsic','controls/verify_intrinsic.py'),
                       ('integral_flag','controls/check_integral_flag.py')):
        result, receipt = run(PACKAGE/code)
        require(result.returncode == 0 and not result.stderr, 'Standalone mathematical control failed: '+name)
        expected = (PACKAGE/'expected'/f'{name}.stdout').read_bytes()
        if name == 'intrinsic':
            actual, expected_json = json.loads(result.stdout), json.loads(expected)
            actual_environment = actual.pop('interpreter')
            expected_environment = expected_json.pop('interpreter')
            require(actual == expected_json, 'Intrinsic mathematics changed beyond interpreter identity')
            receipt['comparison'] = 'Complete mathematical JSON after deleting only interpreter; not submitted full-verifier success'
            receipt['interpreter_field_matches'] = actual_environment == expected_environment
        else:
            require(result.stdout == expected, 'Complete deterministic stdout changed: '+name)
            receipt['comparison'] = 'Complete stdout bytes'
        runs.append(dict(name=name, **receipt))
    result, receipt = run(ROOT/'independent_controls.py', cwd=ROOT)
    require(result.returncode == 0 and not result.stderr, 'Independent reviewer controls failed')
    require(receipt['stdout_sha256'] == '084bb55bd7e7ca555978dccf39dcbb5e64c95162bc47d45d8167143545eb9eb9', 'Independent deterministic stdout changed')
    runs.append(dict(name='reviewer_independent_controls', **receipt))
    result, full_receipt = run(PACKAGE/'verify_supplement.py', ['--full'])
    if result.returncode == 0:
        require(not result.stderr, 'Submitted full verifier emitted unexpected stderr')
    else:
        require(result.returncode == 1 and not result.stdout and
                result.stderr.rstrip().endswith(b'RuntimeError: Complete stdout mismatch: intrinsic'),
                'Submitted full verifier has an unexpected additional failure')
    historical_receipts = 0
    if args.scope == 'full':
        for p in (ROOT/'native').glob('*.receipt.json'):
            record = json.loads(p.read_text())
            base = p.name.removesuffix('.receipt.json')
            for stream in ('stdout','stderr'):
                body = (ROOT/'native'/f'{base}.{stream}').read_bytes()
                require(len(body) == record[stream+'_bytes'] and hashlib.sha256(body).hexdigest() == record[stream+'_sha256'], 'Native receipt/stream mismatch')
            require(record['argv'] and record['executable'] and record['runner_interpreter'] and
                    record['start_utc'] and record['end_utc'] and isinstance(record['exit_code'], int), 'Incomplete native receipt')
            historical_receipts += 1
        failure = json.loads((ROOT/'native/package_full_bundled.receipt.json').read_text())
        require(failure['exit_code'] == 1 and failure['stdout_bytes'] == 0 and failure['stderr_bytes'] == 967 and
                failure['stderr_sha256'] == 'e297e012951804aa0dc992b386a77778af6c69f634fa71f586cb7280ae541bac', 'Historical blocker evidence changed')
    require(inventory() == before, 'Review replay changed owned files or modes')
    print(json.dumps(dict(review_record_check='PASS', scope=args.scope, sealed=False,
                         review_verdict='REPAIR_REQUIRED', publication_ready=False,
                         checked_body_pins=len(selected), zip_members=32,
                         historical_native_receipts_checked=historical_receipts,
                         standalone_control_runs=runs, submitted_full_run=full_receipt,
                         owned_namespace_unchanged=True,
                         namespace_manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
                         limitations=['Review-record PASS does not approve the defective frozen publication packet.',
                                      'Public scope verifies public bodies and control replay; full scope also binds private source snapshots and native historical evidence.',
                                      'Source reading, proof validity and historical priority are assessed in REPORT.md; hashes and finite controls do not establish them.',
                                      'Live original source paths are provenance only; the six historical candidate copies remain the replay inputs.']), indent=2))


if __name__ == '__main__':
    main()
