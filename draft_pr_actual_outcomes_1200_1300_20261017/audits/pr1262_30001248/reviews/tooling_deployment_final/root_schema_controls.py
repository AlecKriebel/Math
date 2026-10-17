#!/usr/bin/env python3
"""Explicit selected-schema controls; no service or Git mutation."""
from pathlib import Path
import copy
import hashlib
import json
import runpy
import shutil
import tempfile

AUDIT = Path(__file__).resolve().parents[1]
FAMILY = 'reviews/fourier_adversary'
MANIFEST = 'AUTHORED_MANIFEST.json'
ANCHOR = '3db46ded563c2d6cae8556b946fde5d18bb53ff7f0805ea876a5c1ae9d92f212'


def need(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    v = runpy.run_path(str(AUDIT / 'publication/verification/verify.py'))
    source = AUDIT / FAMILY
    original = source / MANIFEST
    need(sha(original) == ANCHOR, 'outside anchor')
    data = json.loads(original.read_text())
    registry = {'path': FAMILY + '/' + MANIFEST, 'base': FAMILY,
                'entries_key': 'entries', 'path_key': 'relative_path',
                'size_key': 'bytes', 'sha256': ANCHOR}
    v['authenticate_nested_manifests'](AUDIT, [registry], require_complete=False)
    rejected = []
    with tempfile.TemporaryDirectory(prefix='fourier-selected-schema-') as tmp:
        root = Path(tmp)
        family = root / FAMILY
        family.mkdir(parents=True)
        for entry in data['entries']:
            shutil.copyfile(source / entry['relative_path'], family / entry['relative_path'])
        dest = family / MANIFEST

        def invoke(obj=None, reg=None):
            dest.write_text(json.dumps(data if obj is None else obj, indent=2) + '\n')
            selected = dict(registry if reg is None else reg)
            selected['sha256'] = sha(dest)
            return v['authenticate_nested_manifests'](root, [selected], require_complete=False)

        invoke()
        harmless = copy.deepcopy(data)
        for entry in harmless['entries']:
            entry['path'] = '/outside/historical/receipt/never-opened'
        invoke(harmless)

        def reject(call, name):
            try:
                call()
            except (ValueError, RuntimeError, FileNotFoundError):
                rejected.append(name)
                return
            raise RuntimeError('unexpected acceptance: ' + name)

        for name, raw in [('escape', '../outside'), ('absolute', '/outside'),
                          ('noncanonical', 'a/../REPORT.md')]:
            bad = copy.deepcopy(data)
            bad['entries'][0]['relative_path'] = raw
            reject(lambda bad=bad: invoke(bad), name)
        bad = copy.deepcopy(data)
        bad['entries'].append(copy.deepcopy(bad['entries'][0]))
        reject(lambda: invoke(bad), 'duplicate_selected_member')
        wrong = dict(registry, entries_key='guessed')
        reject(lambda: invoke(reg=wrong), 'guessed_schema')
        wrong = dict(registry, path_key='path')
        reject(lambda: invoke(reg=wrong), 'absolute_receipt_selected_as_member')
        target = family / data['entries'][0]['relative_path']
        saved = target.read_bytes()
        target.write_bytes(saved + b'corrupt')
        reject(invoke, 'selected_member_bytes_changed')
        target.write_bytes(saved)
        dest.write_bytes(original.read_bytes())
        wrong = dict(registry, sha256='0' * 64)
        reject(lambda: v['authenticate_nested_manifests'](root, [wrong], require_complete=False),
               'outside_manifest_anchor_changed')
    need(sha(original) == ANCHOR, 'original changed')
    print(json.dumps({'status': 'PASS', 'exact_schema': ['entries', 'relative_path', 'bytes'],
                      'members': len(data['entries']), 'relocated_without_original_host_reads': True,
                      'unused_absolute_receipt_fields_ignored': True,
                      'negative_controls': rejected, 'original_manifest_unchanged': True}, sort_keys=True))


if __name__ == '__main__':
    main()
