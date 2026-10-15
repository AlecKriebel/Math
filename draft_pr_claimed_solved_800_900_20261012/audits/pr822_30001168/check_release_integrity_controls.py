#!/usr/bin/env python3
"""Integrity challenges in disposable copies, retaining only one case at a time."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent


def main():
    pre = HERE / 'preprint'
    receipt = json.loads((pre / 'BUILD_RECEIPT.json').read_bytes())
    records = []
    with tempfile.TemporaryDirectory(prefix='yamabe release integrity challenges ') as temporary:
        temporary = Path(temporary)
        baseline = temporary / 'frozen release with spaces'
        baseline.mkdir()
        with zipfile.ZipFile(pre / 'verification.zip') as archive:
            archive.extractall(baseline)
        def run(label, mutation=None, expected=False, pin=None):
            for optimized in (False, True):
                root = temporary / ('case ' + str(len(records)))
                shutil.copytree(baseline, root)
                if mutation:
                    mutation(root)
                trusted = pin or receipt['index_sha256']
                if trusted == 'REPIN':
                    trusted = hashlib.sha256((root / 'package_index.json').read_bytes()).hexdigest()
                process = subprocess.run([sys.executable, '-I', '-B'] + (['-O'] if optimized else []) +
                                         [str(root / 'verify_package.py'), trusted],
                                         cwd='/', capture_output=True, text=True, timeout=60)
                if (process.returncode == 0) != expected:
                    raise RuntimeError(label + ': ' + process.stderr)
                records.append({'case': label, 'optimized': optimized,
                                'accepted': process.returncode == 0, 'expected': expected})
                shutil.rmtree(root)
        run('exact relocated release', expected=True)
        run('wrong external pin', pin='0' * 64)
        run('missing original proof', lambda r: (r / 'source/author/PROOF.md').unlink())
        run('undeclared extra file', lambda r: (r / 'extra.txt').write_text('x'))
        run('undeclared empty directory', lambda r: (r / 'extra').mkdir())
        run('bytecode directory', lambda r: (r / '__pycache__').mkdir())
        def corrupt(root):
            path = root / 'note.tex'
            raw = path.read_bytes()
            path.write_bytes(b'!' + raw[1:])
        run('same-size note source corruption', corrupt)
        def link(root):
            path = root / 'note.pdf'
            path.unlink()
            path.symlink_to(baseline / 'note.pdf')
        run('symlink', link)
        def fifo(root):
            path = root / 'note.pdf'
            path.unlink()
            os.mkfifo(path)
        run('FIFO', fifo)
        def unsafe(root):
            path = root / 'package_index.json'
            data = json.loads(path.read_bytes())
            data['files'][0]['path'] = '../escape'
            path.write_text(json.dumps(data))
        run('unsafe manifest path with fresh pin', unsafe, pin='REPIN')
        def duplicate(root):
            path = root / 'package_index.json'
            path.write_text(path.read_text().replace('"schema":', '"schema":"duplicate","schema":', 1))
        run('duplicate JSON key with fresh pin', duplicate, pin='REPIN')
        def rehash(root):
            corrupt(root)
            path = root / 'package_index.json'
            data = json.loads(path.read_bytes())
            for row in data['files']:
                raw = (root / row['path']).read_bytes()
                row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
            path.write_text(json.dumps(data))
        run('corruption with rewritten index and original external pin', rehash)
    out = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'status': 'PASS', 'total': len(records), 'accepted_baselines': 2,
           'expected_rejections': len(records) - 2, 'cases': records,
           'mutation_scope': 'disposable copies only', 'analytic_proof_or_priority_certified': False,
           'initial_interruption': 'environmental ENOSPC before cases; final low-storage run completed'}
    (HERE / 'ROOT_RELEASE_INTEGRITY_CONTROLS.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'controls': len(records), 'expected_rejections': len(records) - 2}))


if __name__ == '__main__':
    main()
