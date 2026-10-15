#!/usr/bin/env python3
"""Allowlisted authored evidence; no raw sources or mutable operation receipts."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

P = Path(__file__).resolve().parent
A = P.parent
WORK = P / 'tmp/packet'
FAMILIES = {
    'operator_01': ['exact_operator_check.py', 'VERDICT.json', 'EXACT_RESULTS.json',
                    'RESEARCH_LOG.md', 'ORIGINAL_REPLAY.json', 'FINDINGS.md',
                    'REVIEW_MANIFEST.json', 'SOURCE_METADATA.json'],
    'scope_01': ['VERDICT.json', 'RESEARCH_LOG.md', 'DEDUCTIONS.md', 'CHECK_RESULTS.json',
                 'FINDINGS.md', 'SOURCE_HASHES.json', 'check_scope.py'],
    'priority_01': ['CURRENT_PUBLIC_VISIBILITY.json', 'PRIOR_IMPLICATION_CHECK.json',
                    'DOWNLOAD_MANIFEST_ADDITIONAL.json', 'DOWNLOAD_MANIFEST.json',
                    'SEARCH_LEDGER.md', 'CHRONOLOGY.md', 'SOURCE_LEDGER.md',
                    'SOURCE_LEDGER.json', 'VERDICT.json', 'EULERSOLVE_ENDPOINT_CHECK.json',
                    'RESEARCH_LOG.md', 'METHOD_COMPARISON.md', 'verify_prior_implication.py',
                    'FINDINGS.md', 'SEARCH_LEDGER.json', 'PRIOR_IMPLICATION.md',
                    'REVIEW_MANIFEST.json', 'EULERSOLVE_CATALOGUE_CHECK.json'],
    'classical_implication_01': ['exact_compression_check.py', 'SOURCE_LEDGER.json',
                                'VERDICT.json', 'RESEARCH_LOG.md',
                                'EXACT_COMPRESSION_RESULTS.json', 'FINDINGS.md', 'DERIVATION.md'],
}


def copy(source, name):
    target = WORK / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def main():
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    for name in ['gns_generation_counterexample.pdf', 'gns_generation_counterexample.tex',
                 'verify_package.py', 'requirements.txt', 'CURRENT_PRIORITY_AND_STATUS.md']:
        copy(P / name, name)
    copy(P / 'PACKAGE_README.md', 'README.md')
    candidate = A / 'native/unsolved_math_prioritization/attempts/30001184'
    doc = json.loads((candidate / 'PUBLICATION_MANIFEST.json').read_text())
    for name in [entry['path'] for entry in doc['files']] + ['PUBLICATION_MANIFEST.json']:
        copy(candidate / name, 'candidate/' + name)
    for family, names in FAMILIES.items():
        for name in names:
            copy(A / 'reviews' / family / name, 'reviews/' + family + '/' + name)
    for name in ['PR_PUBLIC_CHRONOLOGY.json', 'PROOF_COMMIT_CHRONOLOGY.txt',
                 'ROOT_PRIMARY_SOURCE_CHECK.json', 'ROOT_ORIGINAL_REPLAY.json',
                 'ROOT_INTEGRITY_CONTROLS.txt', 'ROOT_OPERATOR_REPLAY.json',
                 'ROOT_SCOPE_REPLAY.json', 'ROOT_PRIORITY_REPLAY.json',
                 'ROOT_CLASSICAL_REPLAY.json', 'ROOT_REPRODUCTION_ENVIRONMENT.json',
                 'MATH_GATE_ACCEPTANCE.json', 'PRIORITY_GATE_ACCEPTANCE.json']:
        copy(A / name, 'chronology_and_reproduction/' + name)
    entries = []
    for path in sorted(WORK.rglob('*')):
        if path.is_file():
            data = path.read_bytes()
            entries.append({'path': path.relative_to(WORK).as_posix(), 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest()})
    manifest = {'schema': 1, 'file_count': len(entries), 'files': entries,
                'raw_third_party_fulltexts_included': False}
    (WORK / 'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    output = P / 'gns_verification.zip'
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(WORK.rglob('*')):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(WORK).as_posix(),
                                       date_time=(2026, 10, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())
    receipt = {'files': len(entries) + 1, 'zip_bytes': output.stat().st_size,
               'zip_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
               'pdf_sha256': hashlib.sha256((P / 'gns_generation_counterexample.pdf').read_bytes()).hexdigest()}
    (P / 'PACKAGE_BUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
