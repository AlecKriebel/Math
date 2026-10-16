#!/usr/bin/env python3
"""Seal complete first-party inventory and preserve noncircular verification streams."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parent
contract = root/'FINAL_VERIFICATION_CONTRACT.json'
stdout = root/'streams/final_manifest.stdout'
stderr = root/'streams/final_manifest.stderr'
# Reserve final evidence files before inventory count; the digest-bearing
# manifest itself is excluded. No receipt contains its own digest indirectly.
for p in (contract, stdout, stderr):
    p.write_bytes(b'')
count = sum(p.is_file() for p in root.rglob('*')
            if p.relative_to(root).parts[0] != 'foreign_primary_cache'
            and p.relative_to(root).as_posix() != 'artifact_manifest.json')
expected = (json.dumps({'verified': True, 'files': count,
                       'excluded': ['artifact_manifest.json', 'foreign_primary_cache/']}, indent=2)+'\n').encode()
stdout.write_bytes(expected)
stderr.write_bytes(b'')
build_command = ['/usr/bin/python3', str(root/'manifest_integrity.py'), '--build', '--no-digest']
check_command = ['/usr/bin/python3', str(root/'manifest_integrity.py'), '--no-digest']
contract.write_text(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
    'build_command': build_command, 'read_only_command': check_command,
    'expected_exit': 0, 'recursive_files': count,
    'actual_stdout_equals_preserved_bytes_required': True,
    'stdout_sha256': hashlib.sha256(expected).hexdigest(),
    'stderr_sha256': hashlib.sha256(b'').hexdigest(),
    'scope': 'Pre-reserved non-digest verification bytes avoid any recursive self-hash. Both actual executions must match all preserved stdout/stderr bytes; manifest excludes only itself and foreign cache.'}, indent=2)+'\n')
for command in (build_command, check_command):
    result = subprocess.run(command, capture_output=True)
    assert result.returncode == 0 and result.stdout == expected and result.stderr == b'', {
        'command': command, 'exit': result.returncode, 'stdout': result.stdout.decode(), 'stderr': result.stderr.decode()}
print(json.dumps({'closed': True, 'recursive_files': count,
                  'manifest_sha256': hashlib.sha256((root/'artifact_manifest.json').read_bytes()).hexdigest(),
                  'full_stdout_stderr_preserved_and_checked': True}, indent=2))
