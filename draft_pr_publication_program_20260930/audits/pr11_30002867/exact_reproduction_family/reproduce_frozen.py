#!/usr/bin/env python3
"""Verify immutable manifest and rerun both untrusted frozen suites in scratch.

No canonical source is imported or modified. The result comparison includes bytes,
parsed JSON, digests, process exit status, and the final source-manifest recheck.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[2]
SCRATCH = ROOT / 'tmp/reproduction/pr11_exact_family/frozen_copy'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_manifest():
    manifest = json.loads((AUDIT / 'snapshot_manifest.json').read_text())
    rows = []
    for entry in manifest['files']:
        p = AUDIT / entry['snapshot_path']
        got = digest(p)
        assert got == entry['sha256'], (p, got)
        assert p.stat().st_size == entry['size'], p
        rows.append({'path':entry['snapshot_path'], 'sha256':got,
                     'size':p.stat().st_size})
    checksum_rows = (AUDIT/'source_snapshot/SHA256SUMS').read_text().splitlines()
    assert len(checksum_rows) == 13
    for checksum in checksum_rows:
        expected,relative = checksum.split(None,1)
        assert digest(AUDIT/'source_snapshot'/relative.strip()) == expected
    return manifest, rows

def main():
    manifest, before = check_manifest()
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    shutil.copytree(AUDIT / 'source_snapshot', SCRATCH)
    for entry in manifest['files']:
        relative = Path(entry['snapshot_path']).relative_to('source_snapshot')
        assert digest(SCRATCH / relative) == entry['sha256']
    author = subprocess.run([sys.executable, str(SCRATCH/'check_koszul.py')],
                            capture_output=True, check=True, text=True)
    (SCRATCH/'author_stdout.json').write_text(author.stdout)
    saved = AUDIT/'source_snapshot/check_results.json'
    assert json.loads(author.stdout) == json.loads(saved.read_text())
    assert author.stdout.encode() == saved.read_bytes()
    independent = subprocess.run([sys.executable,
        str(SCRATCH/'independent_review/independent_checks.py')],
        capture_output=True, check=True, text=True)
    fresh = SCRATCH/'independent_review/independent_results.json'
    frozen = AUDIT/'source_snapshot/independent_review/independent_results.json'
    assert json.loads(fresh.read_text()) == json.loads(frozen.read_text())
    assert fresh.read_bytes() == frozen.read_bytes()
    _, after = check_manifest()
    assert before == after
    payload = {
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'frozen_head':manifest['head'], 'python':sys.version,
        'manifest_files':len(before), 'manifest_before_after_identical':True,
        'embedded_SHA256SUMS_entries':13, 'embedded_checksums_match':True,
        'scratch':str(SCRATCH), 'manifest_checks':before,
        'author_suite':{'exit_code':author.returncode,
            'case_count':json.loads(author.stdout)['case_count'],
            'json_equal':True, 'bytes_equal':True,
            'stdout_sha256':digest(SCRATCH/'author_stdout.json'),
            'frozen_sha256':digest(saved), 'stderr':author.stderr},
        'prior_independent_suite':{'exit_code':independent.returncode,
            'case_count':json.loads(fresh.read_text())['test_count'],
            'json_equal':True, 'bytes_equal':True,
            'rerun_sha256':digest(fresh), 'frozen_sha256':digest(frozen),
            'stdout':independent.stdout, 'stderr':independent.stderr},
        'scope':'Reproduction of finite examples, not verification of the general theorem.'}
    (HERE/'frozen_reproduction_results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print('PASS frozen manifest: 14 files, unchanged')
    print('PASS author suite: 13 examples, byte-identical JSON')
    print('PASS prior independent suite: 20 examples, byte-identical JSON')

if __name__ == '__main__':
    main()
