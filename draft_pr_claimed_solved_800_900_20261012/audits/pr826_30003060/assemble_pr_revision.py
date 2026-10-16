#!/usr/bin/env python3
"""Build an isolated exact review tree without touching the shared checkout."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import stat
import zipfile

AUDIT = Path(__file__).resolve().parent
PROGRAM = AUDIT.parents[1]
REPO = PROGRAM.parent


def meta(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    if not args.label.isalnum():
        raise RuntimeError('Alphanumeric label required')
    work = PROGRAM / 'work' / ('pr826_revision_' + args.label)
    if work.exists():
        raise RuntimeError('Review snapshot already exists; never replace it')
    shutil.copytree(AUDIT / 'source', work)
    pre = AUDIT / 'preprint'
    dest = work / 'publication_20261014/preprint'
    dest.mkdir(parents=True)
    core = ['note.tex', 'output/pdf/note.pdf', 'README.md', 'metadata.json',
            'CURRENT_PRIORITY.md', 'verify_package.py', 'build_verification.py',
            'package_index.json', 'verification.zip', 'zenodo-deposit.json']
    for name in core:
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pre / name, target)
    portable = work / 'publication_20261014/verification_package'
    portable.mkdir()
    with zipfile.ZipFile(pre / 'verification.zip') as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or len(names) != 140:
            raise RuntimeError('Unexpected archive inventory')
        for entry in archive.infolist():
            name = Path(entry.filename)
            if name.is_absolute() or '..' in name.parts or not stat.S_ISREG(entry.external_attr >> 16):
                raise RuntimeError('Unsafe archive entry')
            target = portable / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(entry))
    shutil.copyfile(AUDIT / 'outer_verify_template.py', work / 'verify_publication.py')
    (work / 'PACKAGE_MANIFEST.json').write_text(json.dumps({
        'schema': 'higher-koszul-current-manifest-locator-v1',
        'current_manifest': 'PUBLICATION_MANIFEST.json',
        'complete_original_manifest': 'publication_20261014/verification_package/source/PACKAGE_MANIFEST.json',
        'note': 'Original complete 65-file tree is frozen inside the portable package; current wrappers use the current manifest.'
    }, indent=2) + '\n')
    (work / 'PUBLICATION_METADATA.json').write_text(json.dumps({
        'schema': 'higher-koszul-current-publication-metadata-v1',
        'problem_id': 30003060, 'pr': 826, 'status': 'PREPRINT_PACKAGE_UNDER_INDEPENDENT_REVIEW',
        'original_head': '286cc67c0727b4decfd4f261a0591cd8823ebce9',
        'original_gate': 'claimed_solved', 'original_effort': '1/5',
        'zenodo_metadata': json.loads((pre / 'metadata.json').read_text()),
        'production_publication_performed': False,
        'scope': 'Literal unrestricted iff refuted; characteristic-zero/general converse not resolved; credited classical elementary application; no firstness/current-openness/human/formal certification.'
    }, indent=2) + '\n')
    (work / 'README.md').write_text('''# Higher Koszul homology: a positive-characteristic obstruction

For problem 30003060 / OWR-14218-004, the literal unrestricted-field equivalence is false: the Koszul free algebra k<x,y> has nonzero coefficient-A fundamental-cocycle higher homology in every positive characteristic. The characteristic-zero converse and general vanishing-to-Koszulness implication remain unresolved here. Historical uniquely intended scope is undetermined.

The three-page [research note](publication_20261014/preprint/output/pdf/note.pdf), [editable source](publication_20261014/preprint/note.tex), [verification ZIP](publication_20261014/preprint/verification.zip) and [guide](publication_20261014/preprint/README.md) form the current preprint package. The complete calculation is an elementary assembled classical consequence of Loday–Quillen, Goodwillie and the BLS definition; no new substantial mechanism or historical firstness is claimed. The [bounded priority disposition](publication_20261014/preprint/CURRENT_PRIORITY.md) records current literature and exact access/version limits.

OpenAI tools were used extensively in solving, development, drafting, coding and adversarial verification. This is unrefereed, without completed external human peer review or formal proof-assistant certification. Computation supplements the unlimited algebraic proof; it does not certify it or priority.

All 65 original files, four evidence archives and original reviews are preserved byte for byte under [the frozen source](publication_20261014/verification_package/source/README.md). The readable author/independent_audit/second_review files and external evidence archives at this level retain their original bytes. Four top wrappers have been superseded; PACKAGE_MANIFEST.json points to the full historical manifest and the current PUBLICATION_MANIFEST.json. Historical metadata and pending-publication statements are dated records, not current claims.

Before running downloaded code, independently obtain trusted SHA-256 pins from the repository's final acceptance receipt at draft_pr_claimed_solved_800_900_20261012/audits/pr826_30003060/FINAL_PREPRINT_ACCEPTANCE.json and check the entrypoint bytes. From this directory, substitute the externally trusted outer-manifest digest for PIN:

    python3 -I -S -B verify_publication.py PIN --full
    python3 -I -S -B -O verify_publication.py PIN --full

The current verifier binds the entire closed tree, exact metadata/PDF/ZIP identity and all frozen original evidence before calling the portable checks. The guide documents canonical temporary paths, historical optimized rejections and the genuinely optimized current diagnostics. The original complete corpus/PDF provenance checks require separate input files; raw publications and corpus contents are excluded.
''')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (work / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n## ' + now + ' — Preprint preparation checkpoint (45%)\n\n')
        log.write('The literal unrestricted negative answer passes independent algebra and primary-source audits. Deep bounded priority identifies a fully assembled classical consequence and leaves firstness/current openness uncertified. Three-page note, complete original snapshot and fresh explicit-guard diagnostics prepared for independent package review. Characteristic-zero/general converse remains unresolved. Original effort stays 1/5; no additional central proof search. No merge or production publication yet.\n')
    files = sorted(p for p in work.rglob('*') if p.is_file())
    manifest = {'schema': 'higher-koszul-current-publication-v1', 'problem_id': 30003060,
                'files': [{'path': p.relative_to(work).as_posix(), **meta(p)} for p in files]}
    (work / 'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    files = sorted(p for p in work.rglob('*') if p.is_file())
    mapping = {'pr': 826, 'problem_id': 30003060,
               'expected_head': '286cc67c0727b4decfd4f261a0591cd8823ebce9',
               'original_turns': '1/5',
               'final_review_status': 'AWAITING_INDEPENDENT_PACKAGE_REVIEW',
               'findings': 'Literal unrestricted-field equivalence refuted by a Koszul free-algebra example in every positive characteristic. Credited elementary classical application; characteristic-zero/general converse unaddressed; no firstness/human/formal certification. Three-page unrefereed AI-assisted note and exact verification package.',
               'commit_message': 'Prepare independently audited positive-characteristic higher Koszul note (30003060)',
               'receipt_path': str(AUDIT / ('PREPARED_PR_REVISION_RECEIPT_' + args.label.upper() + '.json')),
               'files': [{'local_path': str(p), 'repo_path': 'unsolved_math_prioritization/attempts/30003060/' + p.relative_to(work).as_posix(), 'sha256': meta(p)['sha256']} for p in files]}
    (AUDIT / ('PREPARED_PR_MAPPING_' + args.label.upper() + '.json')).write_text(json.dumps(mapping, indent=2) + '\n')
    receipt = {'timestamp_utc': now, 'label': args.label, 'tree': str(work),
               'files': len(files), 'outer_manifest_sha256': meta(work / 'PUBLICATION_MANIFEST.json')['sha256'],
               'original_files_preserved_in_portable_package': 65,
               'core_files': [{'path': n, **meta(pre / n)} for n in core],
               'regular_files': [{'path': p.relative_to(work).as_posix(), **meta(p)} for p in files],
               'git_or_external_service_mutation': False}
    (AUDIT / ('LOCAL_PR_ASSEMBLY_' + args.label.upper() + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k not in {'core_files', 'regular_files'}}))


if __name__ == '__main__':
    main()
