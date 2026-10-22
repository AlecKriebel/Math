#!/usr/bin/env python3
"""Build an explicitly allowlisted deterministic source/verification archive."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import zipfile

P = Path(__file__).resolve().parent
A = P.parent
PREFIX = 'unsolved_math_prioritization/attempts/30006191/bounded_region_v2/'
PIN = '828280cc131c38e1f651b48b655dff177f880ba3505bba54e049510d81827795'
FAMILIES = ['localization_family', 'operator_algebra_family', 'computation_family',
            'source_model_family', 'priority_family', 'priority_mapping_family']


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def fingerprint(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def family_records(manifest):
    if 'intentional_public_files' in manifest:
        records = manifest['intentional_public_files']
    elif type(manifest.get('files')) is list:
        records = {r['path']: {'bytes': r['bytes'], 'sha256': r['sha256']}
                   for r in manifest['files']}
        require(len(records) == len(manifest['files']), 'Duplicate family path')
    elif type(manifest.get('files')) is dict:
        records = manifest['files']
    elif type(manifest.get('artifact_fingerprints')) is list:
        records = {r['path']: {'bytes': r['bytes'], 'sha256': r['sha256']}
                   for r in manifest['artifact_fingerprints']}
        require(len(records) == len(manifest['artifact_fingerprints']), 'Duplicate family path')
    else:
        raise RuntimeError('Missing explicit public family manifest')
    if 'explicit_public_allowlist' in manifest:
        require(set(manifest['explicit_public_allowlist']) == set(records),
                'Family map disagrees with explicit public allowlist')
    if 'public_allowlist' in manifest:
        require(set(manifest['public_allowlist']) == set(records) | {'MANIFEST.json'},
                'Family map disagrees with self-excluded public allowlist')
    return records


def main():
    bundle = P/'tmp/bundle'
    require(not bundle.is_symlink(), 'Symlinked disposable bundle')
    if bundle.exists():
        shutil.rmtree(bundle)
    bundle.mkdir(parents=True)
    mapping = {}
    def add(source, name, expected=None):
        q = PurePosixPath(name)
        require(not q.is_absolute() and q.as_posix() == name and
                all(x not in ('', '.', '..') for x in q.parts), 'Unsafe output path')
        require(not any(x in ('private_sources', 'raw_sources', 'tmp', '__pycache__')
                        for x in q.parts), 'Private or temporary payload forbidden')
        require(name not in mapping, 'Duplicate output path')
        require(stat.S_ISREG(source.lstat().st_mode), 'Nonregular input: '+str(source))
        record = fingerprint(source)
        require(expected is None or expected == record, 'Sealed artifact changed: '+str(source))
        dest = bundle/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        mapping[name] = record

    snapshot = json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
    require(snapshot['head'] == 'a35667b1bb0bafed69916709997a4684223ecc93', 'Wrong original head')
    require(len(snapshot['files']) == 26, 'Wrong original file count')
    for name, sha in snapshot['files'].items():
        require(name.startswith(PREFIX), 'Wrong original target')
        source = A/'original'/name
        require(fingerprint(source)['sha256'] == sha, 'Original packet changed')
        add(source, 'original_packet/'+name[len(PREFIX):])
    require(fingerprint(bundle/'original_packet/PACKAGE_MANIFEST.json')['sha256'] == PIN,
            'Original external manifest mismatch')
    for family in FAMILIES:
        folder = A/'reviews'/family
        manifest = json.loads((folder/'MANIFEST.json').read_text())
        records = family_records(manifest)
        require(type(records) is dict and records, 'Missing explicit public family map')
        for name, record in records.items():
            add(folder/name, 'reviews/'+family+'/'+name, record)
        add(folder/'MANIFEST.json', 'reviews/'+family+'/MANIFEST.json')
    for name in ['note.tex', 'README.md', 'requirements.txt', 'verify_package.py', 'run_checked.py',
                 'copy_guard_challenge.py']:
        add(P/name, name)
    add(P/'output/pdf/note.pdf', 'note.pdf')
    for name in ['ORIGINAL_SNAPSHOT.json', 'PR_DESCRIPTION_ANCHOR.json',
                 'TARGET_IDENTITY_PREFLIGHT.json', 'ROOT_ANALYTIC_CHECKPOINT.md',
                 'PRIORITY_FRAMING.md', 'ROOT_PRIORITY_MAPPING_CHECK.md', 'BIBLIOGRAPHIC_IDENTITIES.json',
                 'MATH_AUDIT_SYNTHESIS.json', 'PUBLICATION_REVIEW_CORRECTIONS.md']:
        add(A/name, name)
    for name in ['REVIEW01_REPAIR_RECEIPT.json', 'PR_DESCRIPTION_CORRECTED.md']:
        add(A/name, name)
    manifest = {'schema_version': 1, 'pr': 908, 'problem_id': '30006191',
                'original_pr_head': snapshot['head'], 'original_packet_manifest_sha256': PIN,
                'scope': 'Authored note PDF/source, unchanged historical packet, independent public reviews and source metadata; raw third-party sources excluded.',
                'files': dict(sorted(mapping.items()))}
    manifest_path = bundle/'PACKAGE_MANIFEST.json'
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
    archive = P/'bounded-region-fermions-source-verification-v1.0.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted([*mapping, 'PACKAGE_MANIFEST.json']):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, (bundle/name).read_bytes())
    receipt = {'manifest_sha256': fingerprint(manifest_path)['sha256'],
               'archive_sha256': fingerprint(archive)['sha256'], 'archive_bytes': archive.stat().st_size,
               'payload_files': len(mapping), 'zip_members': len(mapping)+1,
               'original_files_unchanged': 26, 'authored_pdf_inside_archive_matches_separate_pdf': True,
               'raw_third_party_sources_distributed': False}
    (P/'BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
