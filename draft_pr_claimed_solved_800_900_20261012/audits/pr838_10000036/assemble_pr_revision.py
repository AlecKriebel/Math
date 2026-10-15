#!/usr/bin/env python3
"""Assemble a fresh isolated review tree; never touch the shared checkout."""
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


def meta(path):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise RuntimeError('nonregular input')
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    if not args.label.isalnum():
        raise RuntimeError('Alphanumeric label required')
    work = PROGRAM / 'work' / ('pr838_revision_' + args.label)
    if work.exists():
        raise RuntimeError('Review snapshot already exists; never replace it')
    shutil.copytree(AUDIT / 'source', work)
    pre = AUDIT / 'preprint'
    dest = work / 'publication_20261015/preprint'
    dest.mkdir(parents=True)
    core = ['note.tex', 'output/pdf/note.pdf', 'README.md', 'metadata.json', 'CURRENT_PRIORITY.md',
            'verify_package.py', 'build_verification.py', 'package_index.json', 'verification.zip',
            'zenodo-deposit.json']
    for name in core:
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pre / name, target)
    portable = work / 'publication_20261015/verification_package'
    portable.mkdir()
    with zipfile.ZipFile(pre / 'verification.zip') as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or len(names) != 108:
            raise RuntimeError('Unexpected archive inventory')
        for entry in archive.infolist():
            name = Path(entry.filename)
            if (name.is_absolute() or '..' in name.parts or '\\' in entry.filename
                    or not stat.S_ISREG(entry.external_attr >> 16)
                    or (entry.external_attr >> 16) & 0o111 or entry.flag_bits & 1):
                raise RuntimeError('Unsafe archive entry')
            target = portable / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(entry))
    shutil.copyfile(AUDIT / 'outer_verify_template.py', work / 'verify_publication.py')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (work / 'CURRENT_PUBLICATION.json').write_text(json.dumps({
        'schema': 'finite-energy-current-publication-metadata-v1', 'prepared_at_utc': now,
        'problem_id': 10000036, 'pr': 838,
        'phase_at_preparation': 'PREPARED_FOR_INDEPENDENT_PACKAGE_REVIEW',
        'original_head': 'ed2de7249953ba0c1afad253adca9b820d7297c5',
        'original_gate': 'claimed_solved', 'original_effort': '3/5',
        'current_manifest': 'PUBLICATION_MANIFEST.json',
        'final_external_acceptance': 'draft_pr_claimed_solved_800_900_20261012/audits/pr838_10000036/FINAL_PREPRINT_ACCEPTANCE.json',
        'zenodo_metadata': json.loads((pre / 'metadata.json').read_text()),
        'production_publication_performed_at_preparation': False,
        'scope': 'Every d>=2, ordinary finite-energy fully invariant mixing bond law, unique infinite component, quenched bond/site pc1; strong HM planar antecedent credit; no firstness/current-openness/novelty/human/formal certification.'
    }, indent=2) + '\n')
    (work / 'README.md').write_text('''# Finite-energy lattice percolation with internal critical probability one

For problem10000036 / AMR-099-0036, the five-page [research note](publication_20261015/preprint/output/pdf/note.pdf) gives an affirmative construction for the historical ordinary finite-energy bond question in every d>=2. The law has full lattice-automorphism invariance, translation mixing, a unique infinite component, and quenched internal bond/site critical probabilities one. It uses established one-ended spanning-tree inputs and a maximum finite-past rule suppressing every bypass of late tree cuts.

The construction develops Haggstrom-Mester's published summable tree-flip mechanism. The note also supplies the planar bounded-cutset deduction for their exact fixed-phase midpoint projection. This is a source-consequence deduction, not a located previously printed solution. No wholly new planar mechanism, verified first priority, certified novelty, or worldwide current-open status is claimed. The [priority statement](publication_20261015/preprint/CURRENT_PRIORITY.md) records exact credit, chronology and source/version limits. No uniform energy bound or failure of all uniform marginal bounds is asserted.

[Editable source](publication_20261015/preprint/note.tex), [verification ZIP](publication_20261015/preprint/verification.zip), [portable guide](publication_20261015/preprint/README.md), and [current dated metadata](CURRENT_PUBLICATION.json) accompany the note. OpenAI tools were used extensively in solving, proof development, drafting, coding and adversarial verification. This is unrefereed, without completed external human peer review or formal proof-assistant verification. Automated checks authenticate bytes and archive relationships, not the infinite mathematical proof or priority.

All27 original files and all 3 original evidence archives remain byte-identical in [the complete frozen source](publication_20261015/verification_package/source/README.md). At this level24 original files retain their bytes; README.md, RESEARCH_LOG.md and PUBLICATION_MANIFEST.json are current wrappers. The original complete wrappers are preserved inside the portable package. Original PUBLICATION_ACCEPTANCE.json, PUBLICATION_METADATA.json and PUBLICATION_TEST_RESULTS.json remain dated historical records; CURRENT_PUBLICATION.json and the external final acceptance govern the current package.

Before running downloaded code, independently obtain the SHA-256 pins from the repository's final external acceptance receipt at draft_pr_claimed_solved_800_900_20261012/audits/pr838_10000036/FINAL_PREPRINT_ACCEPTANCE.json and verify the startup file's bytes. From this directory substitute the externally trusted outer-manifest digest for PIN:

    python3 -I -S -B verify_publication.py PIN --full
    python3 -I -S -B -O verify_publication.py PIN --full

The verifier binds the complete closed tree, metadata/PDF/ZIP copies and all frozen original evidence, then calls the portable checks. The guide documents independent startup trust and deterministic rebuilding. Raw primary publications, source extracts, renders, full input corpora and private credentials are excluded. The canonical production deposit manifest is in this shard's audit/preprint folder; no deposit or spreadsheet action is performed by these verification commands.
''')
    with (work / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n## ' + now + ' — Preprint preparation checkpoint (50%)\n\n')
        log.write('All three mathematical/source families pass; classical and recent bounded priority reviews complete, and a fresh independent adversary verifies the exact HM planar consequence. Strong precursor credit and no firstness/current-open-status claims are integrated. Five-page note and portable evidence package are prepared for fresh adversarial package reviews. Original effort remains 3/5; no additional central proof-search turn. No merge or production publication yet.\n')
    (work / 'PUBLICATION_MANIFEST.json').unlink()
    files = sorted(p for p in work.rglob('*') if p.is_file())
    manifest = {'schema': 'finite-energy-current-publication-v1', 'problem_id': 10000036,
                'files': [{'path': p.relative_to(work).as_posix(), **meta(p)} for p in files]}
    (work / 'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    files = sorted(p for p in work.rglob('*') if p.is_file())
    mapping = {'pr': 838, 'problem_id': 10000036,
               'expected_head': 'ed2de7249953ba0c1afad253adca9b820d7297c5', 'original_turns': '3/5',
               'final_review_status': 'AWAITING_INDEPENDENT_PACKAGE_REVIEW',
               'findings': 'Affirmative ordinary finite-energy bond construction for every d>=2: full automorphism invariance, mixing, unique infinite component, quenched bond/site pc1. Maximum-path finite-past bypass control; established Timar input. Strong HM planar antecedent credit and explicit bounded-cutset deduction. No verified firstness/current-openness or uniform-energy assertion. Five-page unrefereed extensively AI-assisted note and exact evidence package.',
               'commit_message': 'Prepare audited finite-energy percolation research note (10000036)',
               'receipt_path': str(AUDIT / ('PREPARED_PR_REVISION_RECEIPT_' + args.label.upper() + '.json')),
               'files': [{'local_path': str(p), 'repo_path': 'unsolved_math_prioritization/attempts/10000036/' + p.relative_to(work).as_posix(), 'sha256': meta(p)['sha256']} for p in files]}
    (AUDIT / ('PREPARED_PR_MAPPING_' + args.label.upper() + '.json')).write_text(json.dumps(mapping, indent=2) + '\n')
    receipt = {'timestamp_utc': now, 'label': args.label, 'tree': str(work), 'files': len(files),
               'outer_manifest_sha256': meta(work / 'PUBLICATION_MANIFEST.json')['sha256'],
               'original_files_preserved_in_portable_package': 27,
               'core_files': [{'path': n, **meta(pre / n)} for n in core],
               'regular_files': [{'path': p.relative_to(work).as_posix(), **meta(p)} for p in files],
               'git_or_external_service_mutation': False}
    (AUDIT / ('LOCAL_PR_ASSEMBLY_' + args.label.upper() + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in {'core_files', 'regular_files'}}))


if __name__ == '__main__':
    main()
