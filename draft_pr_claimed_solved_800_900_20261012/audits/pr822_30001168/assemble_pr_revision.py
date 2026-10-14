#!/usr/bin/env python3
"""Local reviewable assembly only; no Git branch or external-service mutation."""
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
PREFIX = 'unsolved_math_prioritization/attempts/30001168/'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='r1')
    args = parser.parse_args()
    if not args.label.isalnum():
        raise RuntimeError('label must be alphanumeric')
    pre = AUDIT / 'preprint'
    sealed = json.loads((AUDIT / 'PACKAGE_SEAL_R1.json').read_bytes())
    for row in sealed['core_files']:
        raw = (pre / row['path']).read_bytes()
        if len(raw) != row['bytes'] or sha(raw) != row['sha256']:
            raise RuntimeError('sealed core changed')
    tree = PROGRAM / 'work' / ('pr822_revision_' + args.label)
    if tree.exists():
        raise RuntimeError('retain existing assembly; choose a new label')
    tree.parent.mkdir(exist_ok=True)
    shutil.copytree(AUDIT / 'source', tree)
    publication = tree / 'publication_20261013'
    extracted = publication / 'verification_package'
    extracted.mkdir(parents=True)
    with zipfile.ZipFile(pre / 'verification.zip') as archive:
        for info in archive.infolist():
            name = Path(info.filename)
            if name.is_absolute() or '..' in name.parts or info.is_dir() or not stat.S_ISREG(info.external_attr >> 16):
                raise RuntimeError('unsafe archive')
        archive.extractall(extracted)
    for row in sealed['core_files']:
        target = publication / 'preprint' / row['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pre / row['path'], target)
    build = json.loads((pre / 'BUILD_RECEIPT.json').read_bytes())
    kit = json.loads((pre / 'zenodo-deposit.json').read_bytes())
    metadata = {
        'format': 'weighted-yamabe-30001168-preprint-v2', 'problem_id': 30001168,
        'original_head': sealed['frozen_original_head'], 'original_turns': '1/5',
        'scope': 'finite smooth normalized S3 counterexample to universal n>=3 comparison',
        'AI_assisted': True, 'human_peer_review': False, 'formal_verification': False,
        'new_geometric_or_spectral_mechanism_claimed': False,
        'historical_firstness_certified': False, 'worldwide_openness_certified': False,
        'verification_members': build['members'], 'package_index_sha256': build['index_sha256'],
        'zenodo_metadata': kit['metadata'],
        'original_immutable_freeze': 'publication_20261013/verification_package/source/',
        'current_preprint': 'publication_20261013/preprint/output/pdf/note.pdf'}
    (tree / 'PUBLICATION_METADATA.json').write_text(json.dumps(metadata, indent=2) + '\n')
    (tree / 'verify_publication.py').write_bytes((AUDIT / 'outer_verify_template.py').read_bytes())
    (tree / 'README.md').write_text("""# Finite weighted Yamabe heat trace counterexample

Problem 30001168 / OWR-3389-021: claimed_solved, original 1/5 proof effort. The complete negative answer refutes Morpurgo's assertion over all n >= 3 using a smooth positive normalized weight on S^3, length 10000 and specified positive time. The weighted trace exceeds 13/20 and the round maximum is below 321/500. Both maxima are attained. Dimensions n >= 4 and adjacent problem 30001169 remain unaddressed.

The qualitative argument is an assembled classical corollary of credited cylindrical conformal geometry, a chosen fixed rescaled cap, standard Dirichlet min--max and an elementary round bound. Ammann--Jammes and the earlier constructions cited there are credited. The current note records an explicit finite quantitative application to the exact historical comparison. No new geometric or spectral mechanism, historical firstness or worldwide current-openness certificate is claimed.

The [four-page note](publication_20261013/preprint/output/pdf/note.pdf), [editable source](publication_20261013/preprint/note.tex), [verification archive](publication_20261013/preprint/verification.zip) and [reproduction instructions](publication_20261013/preprint/README.md) form the current preprint package. All 42 original files are frozen inside publication_20261013/verification_package/source/. Original author, audit, second-review and three ZIP payloads also remain unchanged at their original locations. Historical pending-review/no-publication labels are retained as dated history; current status is described here and in PUBLICATION_METADATA.json.

Run python3 -I -B verify_publication.py TRUSTED_OUTER_MANIFEST_SHA256 --full in an intact copy of this folder, then repeat with -O. Obtain the trusted digest from the reviewed assembly receipt on main. The wrapper binds the closed outer inventory, metadata/source/PDF identity, all ZIP and extracted members, preserved original payloads and portable arithmetic/semantic checks. These programs do not prove analytic lemmas or certify priority. Fresh final package review receipts are retained in the dedicated shard audit folder on main.

OpenAI tools were used extensively in development, solving, drafting, coding and adversarial verification. This is unrefereed work without completed external human peer review or formal proof-assistant certification. Authored publication materials use CC BY 4.0; downloaded primary works and private state are excluded.
""")
    with (tree / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n## ' + datetime.datetime.now(datetime.timezone.utc).isoformat() +
                  ' — finite quantitative preprint preparation (50%)\n\n'
                  'Independent geometry and trace reviews accepted the full negative answer; bounded priority audit established the qualitative route as an assembled classical corollary. Four-page note credits this relationship and leaves exact historical priority unclaimed. A new exact certificate strengthens the round bound to <321/500. Original42 files and three archives are preserved. Fresh final package reviews remain required before merge/publication. Original1/5 effort unchanged; no additional central proof search.\n')
    files = [p for p in sorted(tree.rglob('*')) if p.is_file()]
    rows = [{'path': p.relative_to(tree).as_posix(), 'bytes': p.stat().st_size,
             'sha256': sha(p.read_bytes())}
            for p in files if p != tree / 'PUBLICATION_MANIFEST.json']
    (tree / 'PUBLICATION_MANIFEST.json').write_text(json.dumps({
        'format': 'weighted-yamabe-30001168-preprint-v2', 'files': rows}, indent=2) + '\n')
    mapping = {
        'pr': 822, 'problem_id': 30001168, 'expected_head': sealed['frozen_original_head'],
        'original_turns': '1/5', 'final_review_status': 'AWAITING_FRESH_PACKAGE_REVIEWS',
        'findings': 'Full finite S3 counterexample to universal n>=3 weighted Yamabe heat trace comparison; explicit quantitative classical application with attribution; AI-assisted unrefereed four-page note and verification package; final package review pending.',
        'commit_message': 'Prepare finite weighted Yamabe heat trace counterexample and reviewed preprint package',
        'receipt_path': str(AUDIT / 'PREPARED_PR_REVISION_RECEIPT_R1.json'),
        'files': [{'local_path': str(p), 'repo_path': PREFIX + p.relative_to(tree).as_posix(),
                   'sha256': sha(p.read_bytes())}
                  for p in sorted(tree.rglob('*')) if p.is_file()]}
    (AUDIT / 'PREPARED_PR_MAPPING_R1.json').write_text(json.dumps(mapping, indent=2) + '\n')
    receipt = {
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'tree': str(tree), 'files': len(mapping['files']),
        'outer_manifest_sha256': sha((tree / 'PUBLICATION_MANIFEST.json').read_bytes()),
        'core_seal': 'PACKAGE_SEAL_R1.json', 'Git_or_service_mutations': False}
    (AUDIT / 'LOCAL_PR_ASSEMBLY_R1.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
