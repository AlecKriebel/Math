#!/usr/bin/env python3
"""Regression tests for explicit source skips and strict frozen payload pins."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
PAYLOAD = ('REPORT.md', 'SCOPE_ADDENDUM.md', 'SOURCE_MANIFEST.json',
           'PROVENANCE_ADDENDUM.json', 'verify.py', 'CHECK_RESULTS.json')


def run_case(label, arguments, mutate=None, expected_code=0, expected_status=None):
    with tempfile.TemporaryDirectory(prefix='fractional-sde-audit-test-') as tmp:
        root = Path(tmp)
        public = root / 'public'
        public.mkdir()
        sources = root / 'private_sources'
        sources.mkdir()
        for name in PAYLOAD + ('audit_verify.py',):
            shutil.copyfile(ROOT / name, public / name)
        if mutate:
            mutate(public, sources)
        result = subprocess.run([sys.executable, str(public / 'audit_verify.py'), *arguments],
                                text=True, capture_output=True, check=False)
        out = json.loads(result.stdout)
        if result.returncode != expected_code or out.get('status') != expected_status:
            raise RuntimeError(f'{label}: unexpected result {result.returncode}, {out.get("status")}')
        if label == 'portable_explicit_skips':
            if len(out['source_checks']) != 8 or any(x['status'] != 'SKIPPED_PORTABLE_MODE' for x in out['source_checks']):
                raise RuntimeError('Portable mode did not explicitly skip all eight source inputs')
            if out['source_checks_complete']:
                raise RuntimeError('Portable mode falsely claimed source completeness')
        if label == 'source_backed_missing_inputs':
            if len(out['source_checks']) != 8 or any(x['status'] != 'MISSING_REQUIRED_INPUT' for x in out['source_checks']):
                raise RuntimeError('Missing-source mode did not identify all eight unavailable inputs')
        return {'test': label, 'status': 'PASS', 'observed_exit_code': result.returncode,
                'observed_checker_status': out['status']}


def tamper(name):
    def change(public, sources):
        p = public / name
        p.write_bytes(p.read_bytes() + b'\n')
    return change


results = [
    run_case('portable_explicit_skips', [], expected_status='PASS_ARITHMETIC_AND_PAYLOAD_ONLY'),
    run_case('source_backed_missing_inputs', ['--mode', 'source-backed'],
             expected_code=2, expected_status='INCOMPLETE_REQUIRED_SOURCES'),
    run_case('report_tampering_rejected', [], tamper('REPORT.md'), 1, 'FAIL_PAYLOAD_IDENTITY'),
    run_case('addendum_tampering_rejected', [], tamper('SCOPE_ADDENDUM.md'), 1, 'FAIL_PAYLOAD_IDENTITY'),
    run_case('missing_report_rejected', [], lambda p, s: (p / 'REPORT.md').unlink(), 1, 'FAIL_PAYLOAD_IDENTITY'),
    run_case('source_tampering_rejected', ['--mode', 'source-backed'],
             lambda p, s: (s / 'hess_childs_rowan_2604.23883.pdf').write_bytes(b'corrupt test fixture'),
             1, 'FAIL_SOURCE_MISMATCH'),
]
print(json.dumps({'status': 'PASS', 'tests': results,
                  'scope': 'Checker failure-mode tests; no mathematical theorem or source contents verified by these tests.'}, indent=2))
