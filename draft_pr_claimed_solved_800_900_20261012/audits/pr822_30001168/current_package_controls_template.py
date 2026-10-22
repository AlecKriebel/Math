#!/usr/bin/env python3
"""Challenge the current outer wrapper; frozen historical controls are separate."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trusted_outer_manifest_sha256')
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    manifest = root / 'PUBLICATION_MANIFEST.json'
    require(hashlib.sha256(manifest.read_bytes()).hexdigest() == args.trusted_outer_manifest_sha256,
            'trusted baseline manifest pin')
    records = []
    with tempfile.TemporaryDirectory(prefix='current yamabe repository controls ') as td:
        td = Path(td)
        def run(label, mutation=None, expected=False, pin=None):
            for optimized in (False, True):
                copy = td / ('case ' + str(len(records)))
                shutil.copytree(root, copy)
                if mutation:
                    mutation(copy)
                command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [
                    str(copy / 'verify_publication.py'), pin or args.trusted_outer_manifest_sha256]
                process = subprocess.run(command, cwd='/', capture_output=True, text=True, timeout=90)
                require((process.returncode == 0) == expected, 'wrong acceptance: ' + label + process.stderr)
                records.append({'case': label, 'optimized': optimized,
                                'accepted': process.returncode == 0, 'expected': expected})
                shutil.rmtree(copy)
        run('relocated exact current package', expected=True)
        run('wrong trusted outer pin', pin='0' * 64)
        run('missing original proof', lambda p: (p / 'author/PROOF.md').unlink())
        run('extra file', lambda p: (p / 'extra').write_text('x'))
        run('empty unexpected directory', lambda p: (p / 'extra').mkdir())
        run('bytecode directory', lambda p: (p / '__pycache__').mkdir())
        def symlink(p):
            path = p / 'author/PROOF.md'
            path.unlink()
            path.symlink_to(root / 'author/PROOF.md')
        run('symlink', symlink)
        def fifo(p):
            path = p / 'author/PROOF.md'
            path.unlink()
            os.mkfifo(path)
        run('FIFO', fifo)
        def corrupt(p):
            path = p / 'author/PROOF.md'
            raw = path.read_bytes()
            path.write_bytes(b'!' + raw[1:])
        run('same-size proof corruption', corrupt)
        def archive(p):
            path = p / 'publication_20261013/preprint/verification.zip'
            raw = path.read_bytes()
            path.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
        run('same-size current archive corruption', archive)
        def rehash(p):
            corrupt(p)
            path = p / 'PUBLICATION_MANIFEST.json'
            data = json.loads(path.read_bytes())
            for row in data['files']:
                raw = (p / row['path']).read_bytes()
                row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
            path.write_text(json.dumps(data, indent=2) + '\n')
        run('proof corruption with rewritten manifest and original pin', rehash)
    print(json.dumps({
        'status': 'PASS', 'tested_version': 'current_outer_repository_package',
        'total': len(records), 'accepted_baselines': 2, 'expected_rejections': len(records) - 2,
        'controls': records, 'mutation_scope': 'disposable copies only',
        'analytic_proof_or_priority_certified': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
