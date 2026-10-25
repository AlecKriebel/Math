#!/usr/bin/env python3
"""Build exact source/verification and portable Zenodo upload archives."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE / 'audit' if (HERE / 'audit').is_dir() else HERE.parent
VER = HERE / 'verification'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def archive(path, members):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as zipped:
        for name, raw in sorted(members.items()):
            item = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o644 << 16
            zipped.writestr(item, raw)


def main():
    VER.mkdir(exist_ok=True)
    converter = VER / 'guard_assertions.py'
    if not converter.exists():
        converter.write_bytes((AUDIT / 'root_reproduction/guard_assertions.py').read_bytes())
    spec = importlib.util.spec_from_file_location('explicit_guards', converter)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    control_specs = [
        ('classical_01', 'controls.py', 'controls_results.json', []),
        ('classical_01', 'parameter_controls.py', 'parameter_results.json', []),
        ('construction_01', 'exact_controls.py', 'RESULTS.json', []),
        ('oracle_01', 'oracle_checker.py', 'oracle_checker_results.json', []),
        ('cover_reduction_01', 'check_small_covers.py', 'small_cover_results.json',
         ['elapsed_seconds', 'script_sha256']),
        ('priority_bridge_01', 'verify_bridge.py', 'bridge_check_results.json', []),
    ]
    plan, provenance = [], []
    for family, name, result_name, ignored in control_specs:
        original = AUDIT / 'reviews' / family / name
        raw = original.read_bytes()
        guarded, count = module.convert(raw.decode())
        target = VER / family / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(guarded)
        expected = json.loads((AUDIT / 'reviews' / family / result_name).read_text())
        for field in ignored:
            expected.pop(field, None)
        expected_path = VER / 'expected' / (family + '_' + name + '.json')
        expected_path.parent.mkdir(exist_ok=True)
        expected_path.write_bytes(encoded(expected))
        plan.append({'file': str(target.relative_to(VER)),
                     'sha256': digest(target.read_bytes()),
                     'expected': str(expected_path.relative_to(VER)),
                     'result_file': None if family == 'oracle_01' else result_name,
                     'ignored_result_fields': ignored})
        provenance.append({'source': 'audit/reviews/' + family + '/' + name,
                           'source_sha256': digest(raw),
                           'public_copy': 'verification/' + str(target.relative_to(VER)),
                           'public_sha256': digest(target.read_bytes()),
                           'asserts_replaced_with_explicit_failures': count,
                           'other_ast_changes': False,
                           'comparison_exclusions': ignored})
    (VER / 'CONTROL_PLAN.json').write_bytes(encoded(plan))
    (VER / 'VERIFIER_PROVENANCE.json').write_bytes(encoded(provenance))
    checked = subprocess.run([sys.executable, '-B', str(VER / 'verify_all.py')],
                             capture_output=True, text=True)
    if checked.returncode:
        raise RuntimeError(checked.stderr)
    (VER / 'REPLAY_RECEIPT.json').write_bytes(encoded(json.loads(checked.stdout)))
    pdf = HERE / 'output/pdf/vdf-testing-gap.pdf'
    pdf.parent.mkdir(parents=True, exist_ok=True)
    if (pdf.parent / 'main.pdf').exists():
        pdf.write_bytes((pdf.parent / 'main.pdf').read_bytes())
    if not pdf.read_bytes().startswith(b'%PDF-'):
        raise RuntimeError('Missing compiled PDF')
    members = {}
    for name in ['main.tex', 'README.md', 'LICENSE.txt', 'zenodo-metadata.json', 'zenodo-deposit.json',
                 'build_package.py', 'output/pdf/vdf-testing-gap.pdf']:
        members[name] = (HERE / name).read_bytes()
    for file in VER.rglob('*'):
        if file.is_file() and '__pycache__' not in file.parts:
            members[str(file.relative_to(HERE))] = file.read_bytes()
    for name in ['PROOF.md', 'SOURCE_METADATA.json', 'SOURCE_REVIEW.md']:
        members['audit/inputs/' + name] = (AUDIT / 'inputs' / name).read_bytes()
    root_names = ['ROOT_MATHEMATICAL_CHECK.md', 'ROOT_PRIORITY_DECISION.md', 'ROOT_PDF_QA.json',
                  'ROOT_PRIORITY_QUERY_LEDGER.json', 'RETRIEVAL_RECEIPT.json']
    for name in root_names:
        members['audit/' + name] = (AUDIT / name).read_bytes()
    receipts = [
        ('classical_01', 'REVIEW_RECEIPT.json', 'files'),
        ('construction_01', 'ARTIFACT_HASHES.json', 'artifacts'),
        ('oracle_01', 'ARTIFACT_MANIFEST.json', 'files'),
        ('priority_01', 'REVIEW_RECEIPT.json', 'artifacts'),
        ('priority_bridge_01', 'authored_manifest.json', 'authored_files'),
    ]
    for family, receipt_name, key in receipts:
        directory = AUDIT / 'reviews' / family
        receipt = json.loads((directory / receipt_name).read_text())
        entries = receipt[key]
        rows = [{'file': name, **meta} for name, meta in entries.items()] if isinstance(entries, dict) else entries
        members['audit/reviews/' + family + '/' + receipt_name] = (directory / receipt_name).read_bytes()
        for row in rows:
            name = row.get('file', row.get('path'))
            if not name or '/' in name or name.endswith(('.pdf', '.html', '.xml')):
                raise RuntimeError('Non-authored or unsafe review entry: ' + str(name))
            raw = (directory / name).read_bytes()
            if digest(raw) != row['sha256'] or len(raw) != row['bytes']:
                raise RuntimeError('Review artifact changed: ' + family + '/' + name)
            members['audit/reviews/' + family + '/' + name] = raw
    family = 'cover_reduction_01'
    directory = AUDIT / 'reviews' / family
    for name in ['REPORT.md', 'RESEARCH_LOG.md', 'check_small_covers.py',
                 'small_cover_results.json', 'HASHES.sha256', '.gitignore']:
        members['audit/reviews/' + family + '/' + name] = (directory / name).read_bytes()
    for file in (AUDIT / 'root_reproduction').glob('*.json'):
        members['audit/root_reproduction/' + file.name] = file.read_bytes()
    for name in ['README.md', 'guard_assertions.py']:
        members['audit/root_reproduction/' + name] = (AUDIT / 'root_reproduction' / name).read_bytes()
    for file in (AUDIT / 'root_reproduction/guarded').rglob('*.py'):
        members['audit/' + str(file.relative_to(AUDIT))] = file.read_bytes()
    members['PROVENANCE.json'] = encoded({
        'problem_id': 30004127, 'alias': 'OWR-16931-012',
        'source_pr': 'https://github.com/AlecKriebel/Math/pull/1119',
        'source_head_sha': '786fff9ba06951209e8c1e3bc6114efbfa2c9d16',
        'source_proof_sha256': '1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3',
        'operative_paper': 'main.tex',
        'historical_direct_proof': 'audit/inputs/PROOF.md',
        'historical_scope': 'Pinned original proof and historical source review/metadata are unchanged. New priority findings and short cover reduction are in the note and current audit reports.',
        'computation_role': 'Finite falsification controls; universal claims rely on analytic proofs and the explicitly credited classical triangle theorem.',
        'review_status': 'Extensive AI assistance; unrefereed; no external human peer review or formal proof-assistant certification.',
        'source_bodies': 'Third-party full articles, extracts, images and private caches excluded.',
    })
    manifest = {name: {'bytes': len(raw), 'sha256': digest(raw)}
                for name, raw in sorted(members.items())}
    members['SOURCE_MANIFEST.json'] = encoded(manifest)
    out = HERE / 'output'
    source = out / 'vdf-testing-gap-source-and-verification.zip'
    archive(source, members)
    metadata = json.loads((HERE / 'zenodo-metadata.json').read_text())
    deposit = json.loads((HERE / 'zenodo-deposit.json').read_text())
    if metadata != deposit['metadata']:
        raise RuntimeError('Metadata mismatch')
    portable = dict(deposit)
    portable['files'] = [{'path': pdf.name}, {'path': source.name}]
    archive(out / 'zenodo-upload-kit.zip', {
        pdf.name: pdf.read_bytes(), source.name: source.read_bytes(),
        'zenodo-metadata.json': (HERE / 'zenodo-metadata.json').read_bytes(),
        'zenodo-deposit.json': encoded(portable), 'README.md': members['README.md'],
    })
    paths = [pdf, source, out / 'zenodo-upload-kit.zip', HERE / 'main.tex',
             HERE / 'zenodo-metadata.json', HERE / 'zenodo-deposit.json']
    receipt = {'files': {str(file.relative_to(HERE)): {
                   'bytes': file.stat().st_size, 'sha256': digest(file.read_bytes())} for file in paths},
               'source_members': manifest, 'source_members_including_manifest': len(members),
               'kit_members': 5, 'verifiers': 'Six controls PASS in ordinary and optimized Python',
               'operative_paper_pages': 5}
    (HERE / 'PACKAGE_RECEIPT.json').write_bytes(encoded(receipt))
    print(json.dumps({key: value for key, value in receipt.items() if key != 'source_members'}, indent=2))


if __name__ == '__main__':
    main()
