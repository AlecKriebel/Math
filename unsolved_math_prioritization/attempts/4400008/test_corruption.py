#!/usr/bin/env python3
"""Actual disposable packet mutations, never edits the retained publication."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
KINDS = ('content', 'missing', 'extra', 'symlink', 'duplicate-path',
         'unsafe-path', 'duplicate-key', 'author-manifest-reseal',
         'audit-manifest-reseal', 'author-content-reseal')


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')


def reseal(root, filename):
    path = root / filename
    obj = json.loads(path.read_text())
    for row in obj['files']:
        data = (root / row['path']).read_bytes()
        row['bytes'] = len(data)
        row['sha256'] = hashlib.sha256(data).hexdigest()
    save(path, obj)


def mutate(root, kind):
    manifest = root / 'PUBLICATION_MANIFEST.json'
    obj = json.loads(manifest.read_text())
    if kind == 'content':
        with (root / 'author/proofs.md').open('ab') as f:
            f.write(b'\ncorrupted\n')
    elif kind == 'missing':
        (root / 'author/proofs.md').unlink()
    elif kind == 'extra':
        (root / 'unexpected.txt').write_text('unexpected\n')
    elif kind == 'symlink':
        p = root / 'author/proofs.md'
        p.unlink()
        p.symlink_to('README.md')
    elif kind == 'duplicate-path':
        obj['files'].append(obj['files'][0].copy())
        save(manifest, obj)
    elif kind == 'unsafe-path':
        obj['files'][0]['path'] = '../outside.txt'
        save(manifest, obj)
    elif kind == 'duplicate-key':
        raw = manifest.read_text()
        manifest.write_text('{"files": [], ' + raw[1:])
    elif kind in ('author-manifest-reseal', 'audit-manifest-reseal'):
        folder = 'author' if kind.startswith('author') else 'independent_audit'
        p = root / folder / 'manifest.json'
        changed = json.loads(p.read_text())
        changed['tampered'] = True
        save(p, changed)
        reseal(root, 'PUBLICATION_MANIFEST.json')
    elif kind == 'author-content-reseal':
        with (root / 'author/proofs.md').open('ab') as f:
            f.write(b'\ncorrupted and resealed\n')
        reseal(root / 'author', 'manifest.json')
        reseal(root, 'PUBLICATION_MANIFEST.json')
    else:
        raise ValueError(kind)


def main():
    rows = []
    for optimized in (False, True):
        flags = ['-O'] if optimized else []
        # Positive control ensures rejection is not caused by a broken runner.
        positive = subprocess.run([sys.executable, '-I', '-B', *flags,
                                   str(ROOT / 'verify_publication.py'), '--integrity-only'],
                                  capture_output=True, check=True)
        if json.loads(positive.stdout)['result'] != 'PASS':
            raise ValueError('positive control failed')
        for kind in KINDS:
            with tempfile.TemporaryDirectory(prefix='boyle-corruption-') as temp:
                root = Path(temp) / 'packet'
                shutil.copytree(ROOT, root)
                mutate(root, kind)
                run = subprocess.run([sys.executable, '-I', '-B', *flags,
                                      str(root / 'verify_publication.py'), '--integrity-only'],
                                     capture_output=True, text=True)
                if run.returncode == 0 or 'ValueError:' not in run.stderr:
                    raise ValueError('mutant not properly rejected: ' + kind)
                rows.append({'kind': kind, 'optimized_wrapper': optimized, 'rejected': True,
                             'diagnostic': run.stderr.splitlines()[-1]})
    print(json.dumps({'target_id': '4400008', 'result': 'PASS',
                      'actual_mutants_rejected': len(rows), 'positive_controls': 2,
                      'mutants': rows, 'theorem_proof': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
