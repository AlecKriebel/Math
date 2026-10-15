#!/usr/bin/env python3
"""Deterministic authored archive; primary downloads and private state excluded."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def collect_audit(pre, audit):
    payload = {}
    def add(name, path, expected=None):
        if name in payload or not stat.S_ISREG(path.lstat().st_mode):
            raise RuntimeError('duplicate or nonregular input: ' + name)
        raw = path.read_bytes()
        if expected and (len(raw) != expected['bytes'] or digest(raw) != expected['sha256']):
            raise RuntimeError('frozen source changed: ' + name)
        payload[name] = raw
    for name in ['README.md','note.tex','metadata.json','CURRENT_PRIORITY.md','verify_package.py','build_verification.py']:
        add(name, pre / name)
    add('note.pdf', pre / 'output/pdf/note.pdf')
    source = json.loads((audit / 'SOURCE_MANIFEST.json').read_bytes())
    if source['frozen_head'] != '286cc67c0727b4decfd4f261a0591cd8823ebce9' or len(source['files']) != 65:
        raise RuntimeError('wrong original identity')
    for row in source['files']:
        add('source/' + row['path'], audit / 'source' / row['path'], row)
    for family in ['algebra_audit_01','source_scope_audit_01']:
        folder = audit / family
        for path in sorted(folder.rglob('*')):
            relative = path.relative_to(folder)
            if ('private_sources' not in relative.parts and path.is_file()
                    and not path.name.startswith('.') and path.suffix in {'.md','.json','.jsonl','.py'}):
                add(family + '/' + relative.as_posix(), path)
    priority = json.loads((audit / 'priority_audit_01/PUBLIC_MANIFEST.json').read_bytes())
    for row in priority['files']:
        name = row['relative_public_path']
        add('priority_audit_01/' + name, audit / 'priority_audit_01' / name, row)
    add('priority_audit_01/PUBLIC_MANIFEST.json', audit / 'priority_audit_01/PUBLIC_MANIFEST.json')
    for name in ['SOURCE_MANIFEST.json','EXACT_CLAIM_AND_VALIDATION.md','ROOT_CORPUS_VERIFICATION.json',
                 'ROOT_AUTHOR_PROVENANCE_REPLAY.json','ROOT_PRIMARY_SOURCE_RETRIEVAL.json','ROOT_REPLAY.py',
                 'ROOT_REPLAY_RESULTS.json','ROOT_REPLAY_PATH_DIAGNOSTIC.json','ROOT_REPLAY_FAILURE_False.json',
                 'ROOT_MATHEMATICAL_AUDIT.md','ROOT_FRESH_ALGEBRA_REPLAY.json','ROOT_CLASSICAL_OPERATOR_REPLAY.json',
                 'MATHEMATICAL_ACCEPTANCE.json','PRIORITY_DISPOSITION.json']:
        add('root_evidence/' + name, audit / name)
    index = {'schema':'higher-koszul-characteristic-preprint-v1','problem_id':30003060,
             'original_head':source['frozen_head'],'unlimited_proof_certified_by_program':False,
             'priority_certified_by_program':False,
             'files':[{'path':name,'bytes':len(raw),'sha256':digest(raw)} for name,raw in sorted(payload.items())]}
    payload['package_index.json'] = (json.dumps(index,indent=2,sort_keys=True)+'\n').encode()
    return payload


def write_archive(payload, output):
    index_raw = payload['package_index.json']
    output.mkdir(parents=True, exist_ok=True)
    (output / 'package_index.json').write_bytes(index_raw)
    with zipfile.ZipFile(output / 'verification.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, raw)
    receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'members': len(payload), 'index_sha256': digest(index_raw),
               'zip_sha256': digest((output / 'verification.zip').read_bytes()),
               'zip_bytes': (output / 'verification.zip').stat().st_size,
               'pdf_sha256': digest(payload['note.pdf']), 'original_source_files_preserved': 65,
               'downloaded_primary_content_distributed': False}
    (output / 'BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-package', type=Path)
    parser.add_argument('--trusted-index-sha256')
    parser.add_argument('--output-root', type=Path)
    args = parser.parse_args()
    if args.from_package:
        if not args.trusted_index_sha256 or not args.output_root:
            raise RuntimeError('--from-package requires external --trusted-index-sha256 and fresh --output-root')
        root = args.from_package.resolve(strict=True)
        output = args.output_root.resolve()
        if root == output or root in output.parents:
            raise RuntimeError('rebuild output must be outside the intact input package')
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise RuntimeError('rebuild output must be a fresh or empty directory')
        index_raw = (root / 'package_index.json').read_bytes()
        if digest(index_raw) != args.trusted_index_sha256:
            raise RuntimeError('external input index pin mismatch')
        index = json.loads(index_raw)
        checkers = [r for r in index['files'] if r['path'] == 'verify_package.py']
        checker = root / 'verify_package.py'
        if (len(checkers) != 1 or not stat.S_ISREG(checker.lstat().st_mode) or
                len(checker.read_bytes()) != checkers[0]['bytes'] or
                digest(checker.read_bytes()) != checkers[0]['sha256']):
            raise RuntimeError('trusted input verifier binding failed')
        flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
        run = subprocess.run([sys.executable, *flags, str(root / 'verify_package.py'),
                              args.trusted_index_sha256],
                             cwd='/', capture_output=True, text=True, timeout=90)
        if run.returncode != 0:
            raise RuntimeError('input package binding failed: ' + run.stderr)
        payload = {row['path']: (root / row['path']).read_bytes() for row in index['files']}
        payload['package_index.json'] = index_raw
    else:
        if args.trusted_index_sha256:
            raise RuntimeError('trusted index is only used with --from-package')
        if not (AUDIT / 'SOURCE_MANIFEST.json').is_file():
            raise RuntimeError('For the assembled PR folder use --from-package ../verification_package '
                               '--trusted-index-sha256 PIN --output-root FRESH_DIRECTORY. '
                               'The default assembly mode requires the canonical shard audit folder.')
        payload = collect_audit(HERE, AUDIT)
        output = args.output_root.absolute() if args.output_root else HERE
    write_archive(payload, output)


if __name__ == '__main__':
    main()
