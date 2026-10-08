#!/usr/bin/env python3
"""Synthetic publication-gate controls; all edits affect temporary copies only."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    cases = []
    def mutate_file(root, name):
        p = root / name
        p.write_bytes(p.read_bytes() + b'\nsynthetic mutation\n')
    def extra_directory(root):
        (root / 'extra').mkdir()
    def nested_file(root):
        (root / 'extra').mkdir()
        (root / 'extra/control.txt').write_text('synthetic')
    def linked(root):
        p = root / 'original/RESULTS.md'
        p.unlink()
        p.symlink_to(ROOT / 'original/RESULTS.md')
    def linked_directory(root):
        shutil.rmtree(root / 'original')
        (root / 'original').symlink_to(ROOT / 'original', target_is_directory=True)
    def repin_author(root):
        mutate_file(root, 'original/RESULTS.md')
        path = root / 'original/MANIFEST.json'
        m = json.loads(path.read_bytes())
        b = (root / 'original/RESULTS.md').read_bytes()
        next(e for e in m['files'] if e['path'] == 'RESULTS.md').update({'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
        path.write_text(json.dumps(m))
    def repin_outer(root):
        mutate_file(root, 'original/RESULTS.md')
        path = root / 'PUBLIC_MANIFEST.json'
        m = json.loads(path.read_bytes())
        b = (root / 'original/RESULTS.md').read_bytes()
        m['files']['original/RESULTS.md'] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
        path.write_text(json.dumps(m))
    tests = [(name, lambda root, n=name: mutate_file(root, n)) for name in [
        'original/RESULTS.md', 'original/MANIFEST.json', 'accepted/audit/ACCEPTANCE.json',
        'accepted/audit/MANIFEST.json', 'accepted/packet/SOURCE_METADATA.json', 'accepted/audit/CORRECTION.patch', 'PUBLIC_MANIFEST.json']]
    tests += [('extra_file', lambda r: (r / 'extra.txt').write_text('synthetic')),
              ('extra_empty_directory', extra_directory), ('extra_nested_file', nested_file),
              ('same_byte_symlink', linked), ('directory_symlink', linked_directory),
              ('repinned_author_manifest', repin_author), ('repinned_public_manifest', repin_outer)]
    for name, change in tests:
        with tempfile.TemporaryDirectory(prefix='maximal-average-publication-mutation-') as td:
            packet = Path(td) / 'packet'
            shutil.copytree(ROOT, packet)
            change(packet)
            for optimized in (False, True):
                cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimized else [])
                result = subprocess.run(cmd + [str(packet / 'verify_publication.py'), '--manifest-sha256', args.manifest_sha256], cwd=td, capture_output=True, timeout=120)
                if result.returncode == 0 or b'RuntimeError' not in result.stderr:
                    raise RuntimeError('Mutation not rejected as expected: ' + name)
                cases.append({'case': name, 'optimized': optimized, 'rejected': True})
    print(json.dumps({'result': 'PASS', 'mutation_rejections': len(cases), 'original_bytes_changed': False, 'cases': cases}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
