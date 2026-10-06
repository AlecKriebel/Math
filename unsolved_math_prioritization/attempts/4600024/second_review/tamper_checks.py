#!/usr/bin/env python3
"""Replayable inventory controls; temporary altered copies never execute altered payloads."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def run():
    mutations = [
        ('clean', lambda p: None, True),
        ('changed_review', lambda p: (p/'REVIEW.md').write_bytes(b'changed'), False),
        ('changed_results', lambda p: (p/'RESULTS.json').write_bytes(b'{}'), False),
        ('changed_source', lambda p: (p/'checks.py').write_bytes(b'raise RuntimeError()'), False),
        ('missing', lambda p: (p/'README.md').unlink(), False),
        ('extra_file', lambda p: (p/'extra.txt').write_bytes(b''), False),
        ('malformed_manifest', lambda p: (p/'MANIFEST.json').write_bytes(b'[]'), False),
        ('extra_directory', lambda p: (p/'extra').mkdir(), False),
        ('empty_bytecode_directory', lambda p: (p/'__pycache__').mkdir(), False),
        ('raw_bytecode', lambda p: (p/'checks.pyc').write_bytes(b'junk'), False),
        ('symlink', lambda p: ((p/'README.md').unlink(), (p/'README.md').symlink_to('REVIEW.md')), False),
        ('fifo', lambda p: os.mkfifo(p/'pipe'), False),
    ]
    records = []
    for optimized in (False, True):
        for name, mutate, expected in mutations:
            with tempfile.TemporaryDirectory(prefix='block-code-inventory-') as temp:
                dest = Path(temp)/'packet'
                shutil.copytree(ROOT, dest)
                mutate(dest)
                command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else [])
                command += [str(dest/'verify_review.py'), '--inventory-only']
                result = subprocess.run(command, cwd='/tmp', capture_output=True)
                if (result.returncode == 0) != expected:
                    raise RuntimeError('unexpected inventory outcome: '+name)
                records.append({'case': name, 'optimized': optimized, 'expected_acceptance': expected})
    print(json.dumps({'controls': len(records), 'cases': records, 'status': 'PASS'}, sort_keys=True, indent=2))

if __name__ == '__main__':
    run()
