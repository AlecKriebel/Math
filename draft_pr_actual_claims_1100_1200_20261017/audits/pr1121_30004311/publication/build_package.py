#!/usr/bin/env python3
"""Deterministic source/verification archive and portable Zenodo upload kit.

The operative PDF is a frozen input, never silently replaced or recompiled.
Works in the repository and after extracting the source archive. Stdlib only.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE / 'audit' if (HERE / 'audit').is_dir() else HERE.parent
VER = HERE / 'verification'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def archive(path, members):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as zipped:
        for name, raw in sorted(members.items()):
            item = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o644 << 16
            zipped.writestr(item, raw)


def main():
    controls = [
        ('reviews/construction_01/check_construction.py', 'reviews/construction_01/RESULT.normal.json', None, False),
        ('reviews/obstruction_01/check_boundaries.py', 'reviews/obstruction_01/RESULTS.json', None, False),
        ('reviews/finite_01/check.py', 'reviews/finite_01/results.json', 'results.json', True),
        ('root_reproduction/symbolic_ingredients.py', 'root_reproduction/SYMBOLIC_RESULTS.json', None, False),
    ]
    plan = []
    for file, expected, result_file, finite in controls:
        certificates = {}
        if finite:
            for name in ['ideal_seed_derivations.jsonl', 'sample_ideal_traces.json']:
                raw = (AUDIT / 'reviews/finite_01' / name).read_bytes()
                certificates[name] = {'bytes': len(raw), 'sha256': digest(raw)}
        plan.append({'file': file, 'sha256': digest((AUDIT / file).read_bytes()),
                     'expected': expected, 'expected_sha256': digest((AUDIT / expected).read_bytes()),
                     'result_file': result_file, 'finite': finite, 'certificates': certificates,
                     'historical_symbolic_receipt': file == 'root_reproduction/symbolic_ingredients.py'})
    (VER / 'CONTROL_PLAN.json').write_bytes(encoded(plan))
    checked = subprocess.run([sys.executable, '-B', str(VER / 'verify_all.py')], capture_output=True, text=True)
    if checked.returncode:
        raise RuntimeError(checked.stderr[-5000:])
    (VER / 'REPLAY_RECEIPT.json').write_bytes(encoded(json.loads(checked.stdout)))

    members = {}
    def add(name, file):
        if name in members:
            raise RuntimeError('Duplicate archive member: ' + name)
        members[name] = file.read_bytes()

    for name in ['main.tex', 'README.md', 'LICENSE.txt', 'zenodo-metadata.json', 'zenodo-deposit.json',
                 'build_package.py', 'output/pdf/simple-brace-counterexample.pdf',
                 'verification/verify_all.py', 'verification/CONTROL_PLAN.json', 'verification/REPLAY_RECEIPT.json']:
        add(name, HERE / name)
    for name in ['PROOF.md', 'SOURCE_METADATA.json', 'SOURCE_REVIEW.md', 'MATHEMATICAL_AUDIT.md',
                 'ACCEPTANCE.json', 'STATUS.json', 'MANIFEST.json', 'README.md']:
        add('audit/inputs/' + name, AUDIT / 'inputs' / name)
    for name in ['ROOT_MATHEMATICAL_CHECK.md', 'ROOT_PRIORITY_DECISION.md', 'ROOT_PRIORITY_SOURCE_NOTES.md',
                 'ROOT_PRIORITY_QUERY_LEDGER.json', 'ROOT_PDF_QA.json', 'RETRIEVAL_RECEIPT.json', 'PR_BODY.md']:
        add('audit/' + name, AUDIT / name)
    for name in ['ROOT_FETCH_RECEIPTS.json', 'ROOT_PRIORITY_FETCH_RECEIPTS.json', 'ROOT_SOURCE_INSPECTION.json']:
        add('audit/sources/' + name, AUDIT / 'sources' / name)
    for name in ['CONSTRUCTION_REPLAY.json', 'OBSTRUCTION_REPLAY.json', 'FINITE_REPLAY.json',
                 'PRIORITY_FINGERPRINT_CHECK.json', 'SYMBOLIC_RESULTS.json', 'symbolic_ingredients.py']:
        add('audit/root_reproduction/' + name, AUDIT / 'root_reproduction' / name)

    def review_entry(family, name, sha256, size=None):
        if not name or '/' in name or name.endswith(('.pdf', '.html', '.xml')):
            raise RuntimeError('Unsafe or non-authored review entry: ' + name)
        file = AUDIT / 'reviews' / family / name
        raw = file.read_bytes()
        if digest(raw) != sha256 or (size is not None and len(raw) != size):
            raise RuntimeError('Review artifact changed: ' + family + '/' + name)
        add('audit/reviews/' + family + '/' + name, file)

    for family, receipt_name, key in [
        ('construction_01', 'ARTIFACT_RECEIPT.json', 'authored_artifacts'),
        ('priority_01', 'ARTIFACT_RECEIPT.json', 'public_artifacts'),
        ('priority_bridge_01', 'HASH_RECEIPT.json', 'files'),
    ]:
        file = AUDIT / 'reviews' / family / receipt_name
        receipt = json.loads(file.read_text())
        add('audit/reviews/' + family + '/' + receipt_name, file)
        entries = receipt[key]
        rows = [{'path': name, **pin} for name, pin in entries.items()] if isinstance(entries, dict) else entries
        for row in rows:
            review_entry(family, row['path'], row['sha256'], row['bytes'])
        if family == 'priority_01':
            review_entry(family, 'SHA256SUMS', receipt['sha256sums_sha256'])
    for family in ['obstruction_01', 'finite_01']:
        file = AUDIT / 'reviews' / family / 'SHA256SUMS'
        add('audit/reviews/' + family + '/SHA256SUMS', file)
        for line in file.read_text().splitlines():
            sha256, name = line.split('  ', 1)
            review_entry(family, name, sha256)

    pdf = HERE / 'output/pdf/simple-brace-counterexample.pdf'
    if not pdf.read_bytes().startswith(b'%PDF-'):
        raise RuntimeError('Missing compiled PDF')
    qa = json.loads((AUDIT / 'ROOT_PDF_QA.json').read_text())
    for key, file in [('source', HERE / 'main.tex'), ('pdf', pdf)]:
        if digest(file.read_bytes()) != qa[key]['sha256']:
            raise RuntimeError('PDF visual QA input changed: ' + key)
    metadata = json.loads((HERE / 'zenodo-metadata.json').read_text())
    deposit = json.loads((HERE / 'zenodo-deposit.json').read_text())
    if metadata != deposit['metadata']:
        raise RuntimeError('Deposit metadata mismatch')
    members['PROVENANCE.json'] = encoded({
        'problem_id': 30004311, 'alias': 'OWR-17294-011',
        'source_pr': 'https://github.com/AlecKriebel/Math/pull/1121',
        'source_head_sha': 'f86b108ac1bc024302648eee9f47f74e26c810ec',
        'source_proof_sha256': '68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75',
        'operative_paper': 'main.tex', 'original_full_proof': 'audit/inputs/PROOF.md',
        'historical_scope': 'All eight original inputs remain unchanged; present audits and note supersede historical priority summaries.',
        'priority': 'No identified prior full answer in a bounded audit; exhaustive priority and historical novelty uncertified. Rump 2020/2022 full bodies and several final journal comparisons unavailable.',
        'computation_role': 'Finite falsification controls and exact per-seed certificates supplement universal written proofs.',
        'review_status': 'Extensive AI assistance; unrefereed; no external human peer review or formal proof-assistant certification.',
        'source_bodies': 'Third-party full articles, extracts, images and private caches excluded.',
    })
    manifest = {name: {'bytes': len(raw), 'sha256': digest(raw)} for name, raw in sorted(members.items())}
    members['SOURCE_MANIFEST.json'] = encoded(manifest)
    out = HERE / 'output'
    source = out / 'simple-brace-counterexample-source-and-verification.zip'
    archive(source, members)
    portable = dict(deposit)
    portable['files'] = [{'path': pdf.name}, {'path': source.name}]
    archive(out / 'zenodo-upload-kit.zip', {
        pdf.name: pdf.read_bytes(), source.name: source.read_bytes(),
        'zenodo-metadata.json': (HERE / 'zenodo-metadata.json').read_bytes(),
        'zenodo-deposit.json': encoded(portable), 'README.md': members['README.md'],
    })
    files = [pdf, source, out / 'zenodo-upload-kit.zip', HERE / 'main.tex',
             HERE / 'zenodo-metadata.json', HERE / 'zenodo-deposit.json']
    receipt = {'files': {str(file.relative_to(HERE)): {'bytes': file.stat().st_size,
               'sha256': digest(file.read_bytes())} for file in files}, 'source_members': manifest,
               'source_members_including_manifest': len(members), 'kit_members': 5,
               'verifiers': 'Four unchanged controls PASS in ordinary and optimized Python',
               'operative_paper_pages': 5}
    (HERE / 'PACKAGE_RECEIPT.json').write_bytes(encoded(receipt))
    print(json.dumps({key: value for key, value in receipt.items() if key != 'source_members'}, indent=2))


if __name__ == '__main__':
    main()
