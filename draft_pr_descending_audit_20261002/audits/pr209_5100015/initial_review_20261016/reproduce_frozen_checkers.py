#!/usr/bin/env python3
"""Replay reviewed frozen programs in an owned copy; never modify the submission."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

D = Path(__file__).resolve().parent
S = D / 'submitted/unsolved_math_prioritization/attempts/5100015'
R = D / 'root_reproduction_01'
PY = Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def check_frozen():
    intake = json.loads((D / 'INTAKE.json').read_text())
    rows = intake['original_source_files']
    prefix = intake['native_source_prefix']
    expected = set()
    for row in rows:
        rel = row['native_path'].removeprefix(prefix)
        assert rel != row['native_path'] and '..' not in Path(rel).parts
        expected.add(rel)
        data = (S / rel).read_bytes()
        assert len(data) == row['bytes'] and digest(data) == row['sha256'], rel
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['native_blob'], rel
    assert {str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()} == expected
    author = json.loads((S / 'FROZEN_MANIFEST.json').read_text())
    for rel, row in author['files'].items():
        data = (S / rel).read_bytes()
        assert len(data) == row['bytes'] and digest(data) == row['sha256'], rel
    inherited = json.loads((S / 'independent_review/REVIEW_SHA256SUMS.json').read_text())
    for rel, sha in inherited.items():
        assert digest((S / 'independent_review' / rel).read_bytes()) == sha, rel
    iv = json.loads((S / 'independent_review/FROZEN_INPUT_VERIFICATION.json').read_text())
    assert iv['frozen_files'] == author['files'] and iv['author_file_count'] == len(author['files']) == 16
    assert iv['author_manifest_sha256'] == digest((S / 'FROZEN_MANIFEST.json').read_bytes())
    return {'native_files': len(rows), 'author_frozen_files': len(author['files']), 'inherited_manifest_files': len(inherited), 'all_actual_bytes_match': True}

def run_job(spec):
    name, source, expected_path, args = spec
    target = R / name
    target.mkdir()
    shutil.copyfile(S / source, target / Path(source).name)
    if name == 'author':
        shutil.copyfile(S / 'PROOF.md', target / 'PROOF.md')
    cmd = [str(PY), '-B', str(target / Path(source).name), *args]
    began = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (target / 'stdout.txt').open('wb') as out, (target / 'stderr.txt').open('wb') as err:
        result = subprocess.run(cmd, cwd=target, stdout=out, stderr=err, timeout=900, check=False)
    assert result.returncode == 0, (name, result.returncode)
    assert not (target / 'stderr.txt').read_bytes(), name
    receipt = {'job': name, 'began_utc': began, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'command': cmd, 'exit_code': result.returncode, 'source_sha256': digest((S / source).read_bytes()), 'stdout_sha256': digest((target / 'stdout.txt').read_bytes()), 'stderr_bytes': 0}
    if expected_path:
        actual = json.loads((target / 'stdout.txt').read_text())
        expected = json.loads((S / expected_path).read_text())
        assert actual == expected, (name, actual, expected)
        if name == 'author':
            assert json.loads((target / 'verification.json').read_text()) == expected
            receipt['self_written_receipt_identical_bytes'] = (target / 'verification.json').read_bytes() == (S / expected_path).read_bytes()
        receipt['all_receipt_fields_exactly_reproduced'] = True
        receipt['actual_receipt'] = actual
    else:
        receipt['scope'] = 'Exploratory probe replay only; no original receipt to compare.'
    (target / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'job': name, 'exit_code': result.returncode, 'receipt': str(target / 'REPLAY_RECEIPT.json')}), flush=True)
    return receipt

def main():
    before = check_frozen()
    R.mkdir()
    jobs = [
        ('author', 'verify.py', 'verification.json', []),
        ('inherited_review', 'independent_review/independent_check.py', 'independent_review/INDEPENDENT_CHECKS.json', []),
        ('exploratory_probe', 'probe_outer_pedal.py', None, []),
    ]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run_job, spec) for spec in jobs]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    after = check_frozen()
    assert after == before
    receipt = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS', 'source_before': before, 'source_after': after, 'jobs': sorted(results, key=lambda x: x['job']), 'limitations': 'Reproduction is finite evidence. Neither high precision nor exact finite controls replace the analytic proof. No network, shared database, Git, index, ref, or submitted-file writes.'}
    (R / 'REPRODUCTION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'jobs': len(results), 'receipt': str(R / 'REPRODUCTION.json')}), flush=True)

if __name__ == '__main__':
    main()
