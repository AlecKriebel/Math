"""Pure syntax, hook stdin, and absent-root gate checks. Never invokes Git."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import stat
import subprocess
import sys

ROOT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/nash-quotient-robinson-production-integration-preparation-sol-20261115')
BASE = 'e2e064c48755452a56c2a31207fb12d7e55074fb'
COMMIT = 'a'*40
URL = 'https://example.invalid/pure-hook-test'
FILES = ['exact14_lib.py', 'preflight.py', 'install_exact.py', 'hooks/pre-push']


def main():
    source = {name: (ROOT/name).read_bytes() for name in FILES}
    bindings = []
    for name, raw in source.items():
        ast.parse(raw, filename=str(ROOT/name))
        bindings.append({'path': name, 'bytes': len(raw),
                         'SHA256': hashlib.sha256(raw).hexdigest(),
                         'mode': oct(stat.S_IMODE((ROOT/name).stat().st_mode)),
                         'syntax': 'PASS'})
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
               EXACT14_APPROVED_COMMIT=COMMIT,
               EXACT14_APPROVED_PUSH_URL_SHA256=hashlib.sha256(URL.encode()).hexdigest())
    good = f'{COMMIT} {COMMIT} refs/heads/master {BASE}\n'.encode()
    cases = [
        ('approved_exact_parent', good, 'origin', URL, {}, True),
        ('remote_rewind', good.replace(BASE.encode(), b'b'*40), 'origin', URL, {}, False),
        ('remote_advance', good.replace(BASE.encode(), b'c'*40), 'origin', URL, {}, False),
        ('absent_remote_ref', good.replace(BASE.encode(), b'0'*40), 'origin', URL, {}, False),
        ('named_local_ref_same_approved_oid', f'refs/heads/master {COMMIT} refs/heads/master {BASE}\n'.encode(), 'origin', URL, {}, True),
        ('wrong_local_oid', f'{COMMIT} {"e"*40} refs/heads/master {BASE}\n'.encode(), 'origin', URL, {}, False),
        ('wrong_remote_ref', good.replace(b'refs/heads/master', b'refs/heads/other'), 'origin', URL, {}, False),
        ('extra_ref_record', good+good, 'origin', URL, {}, False),
        ('missing_ref_record', b'', 'origin', URL, {}, False),
        ('malformed_ref_record', b'one two three\n', 'origin', URL, {}, False),
        ('delete_ref_record', f'(delete) {COMMIT} refs/heads/master {BASE}\n'.encode(), 'origin', URL, {}, False),
        ('wrong_remote_name', good, 'other', URL, {}, False),
        ('wrong_remote_url', good, 'origin', URL+'/changed', {}, False),
        ('missing_commit_authority', good, 'origin', URL, {'EXACT14_APPROVED_COMMIT': ''}, False),
        ('missing_url_authority', good, 'origin', URL, {'EXACT14_APPROVED_PUSH_URL_SHA256': ''}, False),
    ]
    tests = []
    for name, data, remote, url, updates, expected in cases:
        child_env = dict(env, **updates)
        proc = subprocess.run([sys.executable, '-B', str(ROOT/'hooks/pre-push'), remote, url],
                              input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=child_env, timeout=10)
        passed = proc.returncode == 0
        tests.append({'name': name, 'expected_accept': expected, 'actual_accept': passed,
                      'returncode': proc.returncode, 'PASS': passed == expected})
    adoption = ROOT.parent/'root-nash-quotient-robinson-stage-adoption-20261115.json'
    assert not adoption.exists(), 'Absent-root tests require actual root receipt to remain absent'
    assert not (ROOT/'run-state').exists(), 'Do not run gate checks over existing runtime state'
    gate_cases = [
        ('missing_execute', ['--phase', 'install'], 'Preparation only:'),
        ('install_missing_root', ['--phase', 'install', '--execute', '--adoption-sha256', '0'*64], 'ROOT_ADOPTION_MISSING:'),
        ('publish_missing_root', ['--phase', 'publish', '--execute', '--adoption-sha256', '0'*64], 'ROOT_ADOPTION_MISSING:'),
    ]
    for name, args, expected_error in gate_cases:
        proc = subprocess.run([sys.executable, '-B', str(ROOT/'install_exact.py'), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=10)
        message = proc.stderr.decode('utf8', 'replace')
        tests.append({'name': name, 'returncode': proc.returncode,
                      'expected_error_observed': expected_error in message,
                      'run_state_absent': not (ROOT/'run-state').exists(),
                      'PASS': proc.returncode != 0 and expected_error in message and not (ROOT/'run-state').exists()})
    assert all((ROOT/name).read_bytes() == raw for name, raw in source.items()), 'Source changed during checks; rerun on stable code'
    assert all(test['PASS'] for test in tests), json.dumps(tests)
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(),
                      'status': 'PASS_PURE_CHECKS_ONLY', 'source_bindings': bindings,
                      'tests': tests, 'test_count': len(tests),
                      'Git_executed': False, 'network_used': False,
                      'website_written': False, 'runtime_created': False}, indent=2))


if __name__ == '__main__':
    main()
