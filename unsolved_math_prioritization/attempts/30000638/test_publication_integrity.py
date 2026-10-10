#!/usr/bin/env python3
"""Negative controls for the publication boundary; never alters the original."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import shutil
import subprocess
import tempfile

def need(value, label):
    if not value:
        raise RuntimeError(label)

def main():
    root = Path(__file__).resolve().parent
    probes = ['baseline', 'changed', 'missing', 'extra', 'empty_directory',
              'empty_cache', 'cache_file', 'symlink', 'archive_changed', 'duplicate_manifest_key']
    results = []
    with tempfile.TemporaryDirectory(prefix='publication negative controls ') as temp:
        base = Path(temp)
        for flags in ([], ['-O']):
            for label in probes:
                target = base / (('optimized_' if flags else 'normal_') + label)
                shutil.copytree(root, target)
                if label == 'changed':
                    (target / 'corrected/PROOF.md').write_text('changed proof')
                elif label == 'missing':
                    (target / 'corrected/results.json').unlink()
                elif label == 'extra':
                    (target / 'unlisted.txt').write_text('extra')
                elif label == 'empty_directory':
                    (target / 'empty').mkdir()
                elif label == 'empty_cache':
                    (target / 'corrected/__pycache__').mkdir()
                elif label == 'cache_file':
                    (target / 'audit/__pycache__').mkdir()
                    (target / 'audit/__pycache__/independent_geometry.pyc').write_bytes(b'not bytecode')
                elif label == 'symlink':
                    (target / 'link').symlink_to(target / 'README.md')
                elif label == 'archive_changed':
                    p = next((target / 'frozen_archives').iterdir())
                    p.write_bytes(p.read_bytes() + b'changed')
                elif label == 'duplicate_manifest_key':
                    p = target / 'PUBLICATION_MANIFEST.json'
                    p.write_text(p.read_text().replace('"schema": 1', '"schema": 1, "schema": 1'))
                run = subprocess.run([sys.executable, *flags, str(target / 'verify_publication.py')],
                                     cwd=base, capture_output=True, timeout=30)
                need((run.returncode == 0) == (label == 'baseline'), 'unexpected control: ' + label)
                results.append(('optimized:' if flags else 'normal:') + label)
    print(json.dumps({'status': 'PASS', 'checks': len(results), 'passed': results}, sort_keys=True))

if __name__ == '__main__':
    main()
