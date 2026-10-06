#!/usr/bin/env python3
"""Strict flat-inventory verifier. Supply the manifest hash independently."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    root = Path(args.root).absolute()
    need(stat.S_ISDIR(root.lstat().st_mode), 'root is not a regular directory')
    need(re.fullmatch(r'[0-9a-f]{64}', args.manifest_sha256) is not None,
         'invalid external manifest pin')
    observed = {}
    # Classify every entry before reading any candidate payload. No symlinks,
    # sockets, FIFOs, devices, subdirectories, or bytecode caches are permitted.
    for entry in os.scandir(root):
        st = entry.stat(follow_symlinks=False)
        need(stat.S_ISREG(st.st_mode), 'nonregular inventory entry: ' + entry.name)
        need('/' not in entry.name and '\\' not in entry.name,
             'invalid inventory name')
        observed[entry.name] = st.st_size
    need('MANIFEST.json' in observed, 'missing manifest')
    manifest_raw = (root / 'MANIFEST.json').read_bytes()
    need(digest(manifest_raw) == args.manifest_sha256, 'external manifest pin mismatch')
    manifest = json.loads(manifest_raw)
    need(manifest.get('schema') == 1 and manifest.get('problem_id') == 30006162,
         'manifest schema mismatch')
    records = manifest.get('files')
    need(isinstance(records, dict) and bool(records), 'invalid manifest inventory')
    need(set(observed) == set(records) | {'MANIFEST.json'}, 'inventory mismatch')
    verified = {}
    for name, record in records.items():
        need(isinstance(name, str) and re.fullmatch(r'[A-Za-z0-9_]+\.(md|json|py)', name)
             is not None and name != 'MANIFEST.json', 'invalid manifest filename')
        data = (root / name).read_bytes()
        need(len(data) == record['bytes'], 'size mismatch: ' + name)
        need(digest(data) == record['sha256'], 'hash mismatch: ' + name)
        verified[name] = data
    need(verified.get('verify.py') == Path(__file__).read_bytes(),
         'running verifier differs from verified verifier source')
    status = json.loads(verified['STATUS.json'])
    need(status['result'] == 'UNRESOLVED_WITH_SCOPED_PARTIAL_RESULTS', 'status mismatch')
    need(status['target_answers'] == {'sphere': 'unresolved', 'real_projective_plane': 'unresolved'},
         'target answer mismatch')
    need(status['approaches_used'] == 5, 'approach count mismatch')
    approaches = json.loads(verified['APPROACHES.json'])
    need([a['number'] for a in approaches] == [1, 2, 3, 4, 5], 'approach inventory mismatch')
    provenance = json.loads(verified['DATA_PROVENANCE.json'])
    need(provenance['statement_fingerprint']['sha256'] ==
         'cbd7ff4eb23c680a12ffafa408269175e5055b5f76c99f7cb5f7e0c9ca5c4774', 'statement binding mismatch')
    need(provenance['review_fingerprint']['sha256'] ==
         '789e495c517ffce08c19dc75da7ce5a50e96969671b3b52b105dea02c6d4b878', 'review binding mismatch')
    need(provenance['statement_fingerprint']['matches_catalog'] is True
         and provenance['review_fingerprint']['matches_catalog'] is True, 'record match mismatch')
    need(provenance['review_fingerprint']['report_entry_present'] is False, 'missing-report status mismatch')
    # Execute these exact verified bytes, not an import and not a disk path
    # that might select cached bytecode. -I removes cwd/PYTHONPATH influence;
    # -B forbids cache creation. -O is propagated for the optimized replay.
    source = verified['checks.py']
    command = [sys.executable, '-I', '-B']
    if sys.flags.optimize:
        command.append('-O')
    command += ['-c', "exec(compile(bytes.fromhex(" + repr(source.hex()) +
                "), '<hash-verified-checks.py>', 'exec'), {'__name__':'__main__'})"]
    with tempfile.TemporaryDirectory(prefix='surface-gpp-replay-') as td:
        replay = subprocess.run(command, cwd=td, text=True, capture_output=True, timeout=60)
    need(replay.returncode == 0, 'verified checker failed: ' + replay.stderr)
    result = json.loads(replay.stdout)
    expected = json.loads(verified['EXPECTED_RESULTS.json'])
    need(result == expected, 'diagnostic replay differs from expected results')
    print(json.dumps({'problem_id': 30006162, 'status': 'PASS',
        'manifest_sha256': args.manifest_sha256,
        'regular_files_checked': len(observed),
        'verified_source_execution': True, 'exact_inventory': True,
        'diagnostics': result,
        'scope': 'Integrity and finite supporting controls only; mathematical target remains unresolved.'}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print('REJECT: ' + str(exc), file=sys.stderr)
        sys.exit(1)
