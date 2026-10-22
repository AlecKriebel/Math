#!/usr/bin/env python3
"""Corruption controls on disposable copies of a sealed review tree."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

AUDIT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    assembly = json.loads((AUDIT / ('LOCAL_PR_ASSEMBLY_' + args.label.upper() + '.json')).read_text())
    source = Path(assembly['tree'])
    trusted = assembly['outer_manifest_sha256']
    need(digest((source / 'PUBLICATION_MANIFEST.json').read_bytes()) == trusted, 'Sealed tree changed')
    pdf = 'publication_20261014/preprint/output/pdf/note.pdf'
    archive = 'HIGHER_KOSZUL_30003060_CORRECTED_SAFE.zip'
    cases = [
        ('appended README', 'append', 'README.md', 'byte count'),
        ('same-size PDF mutation', 'flip', pdf, 'digest'),
        ('missing member', 'missing', 'README.md', 'closed inventory'),
        ('extra member', 'extra', '', 'closed inventory'),
        ('extra empty directory', 'emptydir', '', 'closed inventory'),
        ('file symlink', 'symlinkfile', 'README.md', 'nonregular member'),
        ('directory symlink', 'symlinkdir', '', 'nonregular member'),
        ('named pipe', 'fifo', '', 'nonregular member'),
        ('untrusted changed outer index', 'index', '', 'external index pin'),
        ('duplicate JSON key fixture', 'duplicatejson', '', 'duplicate JSON key'),
        ('unsafe manifest path fixture', 'unsafe', '', 'safe paths'),
        ('duplicate inventory fixture', 'duplicate', '', 'unique inventory'),
        ('wrong schema fixture', 'schema', '', 'package identity'),
        ('coherent unequal metadata fixture', 'metadata', 'PUBLICATION_METADATA.json', 'exact current metadata equality'),
        ('coherent unequal PDF fixture', 'coherentpdf', pdf, 'PDF identity'),
        ('coherent legacy archive fixture', 'coherentarchive', archive, 'legacy current bytes differ'),
    ]
    records = []
    for optimized in [False, True]:
        flags = ['-I', '-S', '-B', *(['-O'] if optimized else [])]
        for label, kind, name, diagnostic in [('baseline', 'baseline', '', ''), *cases]:
            with tempfile.TemporaryDirectory(prefix='pr826 integrity fixture with spaces ') as td:
                root = Path(td).resolve() / 'package'
                shutil.copytree(source, root)
                manifest_path = root / 'PUBLICATION_MANIFEST.json'
                manifest = json.loads(manifest_path.read_text())
                pin = trusted
                derived_fixture = kind in {'duplicatejson', 'unsafe', 'duplicate', 'schema',
                                           'metadata', 'coherentpdf', 'coherentarchive'}
                if kind == 'append':
                    with (root / name).open('ab') as f:
                        f.write(b'changed\n')
                elif kind in {'flip', 'coherentpdf', 'coherentarchive'}:
                    path = root / name
                    raw = bytearray(path.read_bytes())
                    raw[len(raw) // 2] ^= 1
                    path.write_bytes(raw)
                elif kind == 'missing':
                    (root / name).unlink()
                elif kind == 'extra':
                    (root / 'unexpected.txt').write_text('extra')
                elif kind == 'emptydir':
                    (root / 'unexpected-empty-directory').mkdir()
                elif kind == 'symlinkfile':
                    (root / name).unlink()
                    (root / name).symlink_to(root / 'author/PROOF.md')
                elif kind == 'symlinkdir':
                    (root / 'unexpected-link').symlink_to(root / 'author', target_is_directory=True)
                elif kind == 'fifo':
                    os.mkfifo(root / 'unexpected-fifo')
                elif kind == 'index':
                    manifest_path.write_bytes(manifest_path.read_bytes() + b' ')
                elif kind == 'unsafe':
                    manifest['files'][0]['path'] = '../escape'
                elif kind == 'duplicate':
                    manifest['files'].append(manifest['files'][0])
                elif kind == 'schema':
                    manifest['schema'] = 'wrong-problem-schema'
                elif kind == 'metadata':
                    path = root / name
                    data = json.loads(path.read_text())
                    data['zenodo_metadata']['title'] = 'Wrong title'
                    path.write_text(json.dumps(data))
                if kind in {'metadata', 'coherentpdf', 'coherentarchive'}:
                    path = root / name
                    row = next(r for r in manifest['files'] if r['path'] == name)
                    raw = path.read_bytes()
                    row.update(bytes=len(raw), sha256=digest(raw))
                if derived_fixture:
                    raw = json.dumps(manifest, sort_keys=True, indent=2).encode()
                    if kind == 'duplicatejson':
                        raw = raw.replace(b'{', b'{"problem_id":30003060,', 1)
                    manifest_path.write_bytes(raw)
                    pin = digest(raw)
                result = subprocess.run([os.sys.executable, *flags, str(root / 'verify_publication.py'), pin],
                                        cwd='/', capture_output=True, text=True, timeout=120)
                if kind == 'baseline':
                    need(result.returncode == 0 and json.loads(result.stdout)['regular_files'] == 217,
                         'Baseline failure: ' + result.stderr)
                else:
                    need(result.returncode != 0 and diagnostic in result.stderr,
                         label + ' did not reject for the expected reason: ' + result.stderr)
                records.append({'case': label, 'optimized': optimized, 'returncode': result.returncode,
                                'expected_outcome': 'accept' if kind == 'baseline' else 'reject',
                                'diagnostic_confirmed': True,
                                'trust': 'Explicit derived fixture pin for structural/semantic validation' if derived_fixture
                                         else 'Unchanged independently sealed external pin',
                                'passed': True})
    need(digest((source / 'PUBLICATION_MANIFEST.json').read_bytes()) == trusted, 'Original changed')
    output = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PASS', 'label': args.label, 'outer_manifest_sha256': trusted,
              'cases': records, 'total': len(records), 'accepted_baselines': 2,
              'expected_rejections': 32, 'sealed_original_unchanged': True,
              'boundary': 'Derived fixture pins test semantic/path validation; they do not authorize substitution under the original release pin. Arithmetic controls and unlimited proof are separate.'}
    (AUDIT / ('PACKAGE_INTEGRITY_CONTROLS_' + args.label.upper() + '.json')).write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'cases'}))


if __name__ == '__main__':
    main()
