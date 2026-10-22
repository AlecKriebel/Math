#!/usr/bin/env python3
"""Portable offline verifier for this bound audit. Requires only Python 3."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

EXPECTED_MANIFEST = '91313d8e77bbd9b47d478beee9aef2b6507a80063920d3853265013848d6e31d'
EXPECTED_ZIP = 'b8fb3c3b97601c74f91e8dba2e0b1f35b6fdc024a5a0c07009a30c8add557718'
EXPECTED_ZIP_BYTES = 20003


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path, help='optional local folder containing the six source PDFs')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    require(__debug__, 'Do not run the audit verifier with Python optimization enabled.')
    manifest = json.loads((root/'AUDIT_MANIFEST.json').read_text())
    rows = manifest['files']
    listed = {r['path'] for r in rows}
    require(len(listed) == len(rows), 'duplicate audit-manifest paths')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual == listed | {'AUDIT_MANIFEST.json'}, 'audit file-set mismatch')
    for row in rows:
        require(not PurePosixPath(row['path']).is_absolute() and '..' not in PurePosixPath(row['path']).parts, 'unsafe manifest path')
        data = (root/row['path']).read_bytes()
        require(len(data) == row['bytes'], row['path']+' bytes')
        require(sha(data) == row['sha256'], row['path']+' SHA-256')

    frozen = (root/'AUDITED_INPUTS.json').read_bytes()
    require(sha(frozen) == EXPECTED_MANIFEST, 'frozen manifest hash')
    author = json.loads(frozen)
    zpath = root/'inputs/author.zip'
    zd = zpath.read_bytes()
    require(len(zd) == EXPECTED_ZIP_BYTES and sha(zd) == EXPECTED_ZIP, 'author archive bytes/hash')
    expected_names = {'packet/'+r['path'] for r in author['files']} | {'FREEZE_MANIFEST.json','SHA256SUMS'}
    require(len(author['files']) == 8, 'author packet file count')
    with tempfile.TemporaryDirectory(prefix='connected-limit-audit-') as td:
        temp = Path(td)
        with zipfile.ZipFile(zpath) as archive:
            require(set(archive.namelist()) == expected_names, 'archive exact members')
            require(len(archive.namelist()) == len(expected_names), 'archive duplicate members')
            require(archive.read('FREEZE_MANIFEST.json') == frozen, 'embedded freeze manifest')
            for row in author['files']:
                data = archive.read('packet/'+row['path'])
                require(len(data) == row['bytes'], row['path']+' frozen bytes')
                require(sha(data) == row['sha256'], row['path']+' frozen SHA-256')
            expected_sums = ''.join(r['sha256']+'  packet/'+r['path']+'\n' for r in author['files'])
            expected_sums += EXPECTED_MANIFEST+'  FREEZE_MANIFEST.json\n'
            require(archive.read('SHA256SUMS').decode() == expected_sums, 'embedded SHA256SUMS')
            # Exact, validated member names contain no absolute or parent paths.
            for name in expected_names:
                destination = temp/name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(archive.read(name))
        proc = subprocess.run([sys.executable,'-I',str(temp/'packet/verify.py')], check=True, capture_output=True, text=True)
        replay = json.loads(proc.stdout)
        require(replay == json.loads((root/'AUTHOR_CHECK_RERUN.json').read_text()), 'author replay JSON')
        require(replay['all_passed'] and replay['assertions'] == 5859, 'author assertion count')

    proc = subprocess.run([sys.executable,'-I',str(root/'independent_checks.py')], check=True, capture_output=True, text=True)
    independent = json.loads(proc.stdout)
    require(independent == json.loads((root/'INDEPENDENT_CHECKS.json').read_text()), 'independent replay JSON')
    require(independent['all_passed'] and independent['assertions'] == 13323, 'independent assertion count')

    source_meta = json.loads((root/'AUDIT_SOURCE_METADATA.json').read_text())
    source_rows = source_meta['sources']
    require(len(source_rows) == 6 and all(r['matches_author_bytes_and_hash'] for r in source_rows), 'recorded fresh-source matches')
    pdf_checks = 0
    if args.source_dir:
        for row in source_rows:
            data = (args.source_dir/row['filename']).read_bytes()
            require(data.startswith(b'%PDF-'), row['id']+' PDF signature')
            require(len(data) == row['bytes'], row['id']+' PDF bytes')
            require(sha(data) == row['sha256'], row['id']+' PDF SHA-256')
            pdf_checks += 1
    verdict = json.loads((root/'AUDIT_RESULT.json').read_text())
    require(verdict['target_status'] == 'unsolved' and not verdict['full_target_candidate'], 'verdict scope')
    require(verdict['author_manifest_sha256'] == EXPECTED_MANIFEST and verdict['author_zip_sha256'] == EXPECTED_ZIP, 'verdict binding')
    print(json.dumps({
        'status':'PASS',
        'audit_manifest_sha256':sha((root/'AUDIT_MANIFEST.json').read_bytes()),
        'audit_manifest_files':len(rows),
        'frozen_author_files':8,
        'author_assertions':replay['assertions'],
        'independent_assertions':independent['assertions'],
        'recorded_fresh_source_pdf_matches':6,
        'local_source_pdf_hashes_rechecked':pdf_checks,
        'target_status':'unsolved',
        'full_target_candidate':False,
        'scope':'Byte identity and exact finite controls; mathematical audit conclusions are documented in AUDIT.md.'
    },indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
