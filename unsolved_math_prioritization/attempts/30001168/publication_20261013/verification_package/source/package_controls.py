#!/usr/bin/env python3
"""Test the trusted outer gate using temporary copies in both Python modes."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, description):
    if not ok:
        raise ValueError(description)


def main():
    root = Path(__file__).absolute().parent
    gate = root/'verify_publication.py'
    records = []
    with tempfile.TemporaryDirectory(prefix='yamabe publication controls ') as td:
        td = Path(td)
        def run(label, mutate=None, expected=False, diagnostic=''):
            for optimize in (False, True):
                target = td/('case ' + str(len(records)))
                shutil.copytree(root, target)
                if mutate:
                    mutate(target)
                command = [sys.executable, '-I', '-B'] + (['-O'] if optimize else []) + [str(gate), '--root', str(target), '--integrity-only']
                process = subprocess.run(command, cwd=td, capture_output=True, text=True, timeout=30)
                require((process.returncode == 0) == expected, 'wrong acceptance: ' + label)
                if diagnostic:
                    require(diagnostic in process.stderr, 'wrong failure: ' + label)
                records.append({'case': label, 'optimized': optimize, 'accepted': process.returncode == 0, 'expected': expected})
        run('relocated exact package', expected=True)
        run('missing proof', lambda p:(p/'author/PROOF.md').unlink(), diagnostic='inventory mismatch')
        run('extra file', lambda p:(p/'extra').write_text('x'), diagnostic='inventory mismatch')
        run('empty unexpected directory', lambda p:(p/'extra').mkdir(), diagnostic='unexpected directory')
        run('bytecode directory', lambda p:(p/'__pycache__').mkdir(), diagnostic='unexpected directory')
        def symlink(p):
            (p/'author/PROOF.md').unlink()
            (p/'author/PROOF.md').symlink_to(root/'author/PROOF.md')
        run('symlink', symlink, diagnostic='symlink')
        def fifo(p):
            (p/'author/PROOF.md').unlink()
            os.mkfifo(p/'author/PROOF.md')
        run('FIFO', fifo, diagnostic='nonregular file')
        def corrupt(p):
            path = p/'author/PROOF.md'
            raw = path.read_bytes()
            path.write_bytes(b'!'+raw[1:])
        run('same-size proof corruption', corrupt, diagnostic='hash mismatch')
        def archive(p):
            path = next((p/'archives').glob('*AUTHOR*'))
            raw = path.read_bytes()
            path.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
        run('same-size archive corruption', archive, diagnostic='hash mismatch')
        def rehash(p):
            corrupt(p)
            path = p/'PUBLICATION_MANIFEST.json'
            doc = json.loads(path.read_bytes())
            for row in doc['files']:
                data = (p/row['path']).read_bytes()
                row['bytes'] = len(data)
                row['sha256'] = hashlib.sha256(data).hexdigest()
            path.write_text(json.dumps(doc, indent=2, sort_keys=True)+'\n')
        run('proof corruption with rehashed manifest', rehash, diagnostic='pinned manifest mismatch')
    require(len(records) == 20, 'control count')
    return {'problem_id': 30001168, 'total': 20, 'accepted_baselines': 2, 'expected_rejections': 18, 'controls': records}


if __name__ == '__main__':
    require(len(sys.argv) == 1, 'No command-line arguments supported')
    print(json.dumps(main(), indent=2, sort_keys=True))
