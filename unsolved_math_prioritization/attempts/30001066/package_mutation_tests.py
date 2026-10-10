#!/usr/bin/env python3
"""Synthetic fail-closed tests of the publication gate; all mutations are temporary."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    outcomes = []
    modes = [('normal', []), ('optimized', ['-O']), ('bytecode_disabled', ['-B']), ('optimized_bytecode_disabled', ['-B', '-O'])]
    mutations = [
        ('missing_strict_gate', 'audit/strict_inventory.py', 'delete'),
        ('changed_patch', 'audit/verify_package_strict.patch', 'append'),
        ('changed_proof', 'author/proof.md', 'append'),
        ('changed_publication_manifest', 'PUBLICATION_MANIFEST.json', 'append'),
        ('extra_root', 'unlisted.txt', 'extra'),
        ('unlisted_audit_bytecode', 'audit/__pycache__/strict_inventory.cpython-312.pyc', 'extra'),
        ('unlisted_author_payload', 'author/__pycache__/unexpected.pdf', 'extra'),
        ('symlink', 'author/README.md', 'symlink'),
        ('corrupt_archive', None, 'archive'),
    ]
    with tempfile.TemporaryDirectory(prefix='isolated-publication-mutations-') as td:
        td = Path(td)
        for mode, flags in modes:
            clean = td / ('clean ' + mode)
            shutil.copytree(ROOT, clean)
            env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
            def check(directory, succeeds):
                p = subprocess.run([sys.executable, *flags, str(directory / 'verify_publication.py'), '--integrity-only'], cwd=td, env=env, capture_output=True, text=True)
                require((p.returncode == 0) == succeeds, 'unexpected result: ' + p.stdout + p.stderr)
            check(clean, True)
            for label, name, action in mutations:
                candidate = td / (mode + ' ' + label)
                shutil.copytree(ROOT, candidate)
                if action == 'archive':
                    path = next((candidate / 'archives').glob('*AUTHOR*.zip'))
                    path.write_bytes(path.read_bytes() + b'SYNTHETIC')
                else:
                    path = candidate / name
                    if action == 'delete':
                        path.unlink()
                    elif action == 'append':
                        path.write_bytes(path.read_bytes() + b'\nSYNTHETIC\n')
                    elif action == 'extra':
                        path.parent.mkdir(exist_ok=True)
                        path.write_bytes(b'SYNTHETIC UNLISTED PAYLOAD')
                    elif action == 'symlink':
                        path.unlink()
                        path.symlink_to(clean / 'author/README.md')
                check(candidate, False)
                outcomes.append({'mode': mode, 'mutation': label, 'rejected': True})
            check(clean, True)
    print(json.dumps({'status': 'PASS', 'clean_checks': 8, 'mutations_rejected': outcomes}, sort_keys=True))


if __name__ == '__main__':
    main()
