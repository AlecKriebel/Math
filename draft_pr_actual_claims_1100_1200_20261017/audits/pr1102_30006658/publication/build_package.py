#!/usr/bin/env python3
"""Build explicit, deterministic source/verification and Zenodo-kit archives."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def archive(path, members):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, raw)


def main():
    expected = json.loads((HERE / 'verification/expected_results.json').read_text())
    run = subprocess.run([sys.executable, str(HERE / 'verification/check_bosonization.py')],
                         check=True, capture_output=True, text=True)
    if json.loads(run.stdout) != expected:
        raise SystemExit('Verifier differs from the recorded results')
    optimized = subprocess.run([sys.executable, '-O', str(HERE / 'verification/check_bosonization.py')],
                               capture_output=True, text=True)
    if optimized.returncode == 0:
        raise SystemExit('Verifier must reject disabled assertions')
    if not (HERE / 'output/pdf/cellularization-vanishing.pdf').read_bytes().startswith(b'%PDF-'):
        raise SystemExit('Final PDF absent')

    members = {}
    for name in ['main.tex', 'README.md', 'LICENSE.txt', 'output/pdf/cellularization-vanishing.pdf',
                 'verification/check_bosonization.py', 'verification/expected_results.json']:
        members[name] = (HERE / name).read_bytes()
    audits = {
        'audits/hopf_01/REVIEW.md': AUDIT / 'reviews/hopf_01/REVIEW.md',
        'audits/hopf_01/INDEPENDENT_DERIVATION.md': AUDIT / 'reviews/hopf_01/INDEPENDENT_DERIVATION.md',
        'audits/hopf_01/check_bosonization.py': AUDIT / 'reviews/hopf_01/check_bosonization.py',
        'audits/hopf_01/bosonization_results.json': AUDIT / 'reviews/hopf_01/bosonization_results.json',
        'audits/topology_01/REVIEW.md': AUDIT / 'reviews/topology_01/REVIEW.md',
        'audits/topology_01/INDEPENDENT_DERIVATION.md': AUDIT / 'reviews/topology_01/INDEPENDENT_DERIVATION.md',
        'audits/topology_01/sources/RECEIPTS.json': AUDIT / 'reviews/topology_01/sources/RECEIPTS.json',
        'audits/source_retrieval.json': AUDIT / 'sources/SOURCE_RETRIEVAL.json',
        'audits/priority_01/PRIORITY_AUDIT.md': AUDIT / 'reviews/priority_01/PRIORITY_AUDIT.md',
    }
    for name, path in audits.items():
        members[name] = path.read_bytes()
    # Include only explicitly public priority evidence, never downloaded sources.
    for name in ['SOURCE_LEDGER.json', 'QUERY_LEDGER.json', 'RETRIEVALS.json', 'COMPARISON_MATRIX.md']:
        path = AUDIT / 'reviews/priority_01' / name
        if path.exists():
            members['audits/priority_01/' + name] = path.read_bytes()
    members['PROVENANCE.json'] = (json.dumps({
        'problem_id': 30006658,
        'problem_alias': 'OWR-14299915-021',
        'source_pr': 'https://github.com/AlecKriebel/Math/pull/1102',
        'source_head_sha': '860cd93b8fb3ce5e9c7dc9109fc1e7cc83c9347a',
        'source_report_sha256': 'c985406f6b9b456a220baecc70f836dd98bb0ba950a153b08e35e5677ff8b23b',
        'analytic_proof': 'main.tex',
        'computation_role': 'Bounded convention checks only; not a proof of the infinite theorem.',
        'review_status': 'AI-assisted, unrefereed; no external human peer review claimed.',
    }, indent=2) + '\n').encode()
    source_manifest = {
        name: {'bytes': len(raw), 'sha256': sha(raw)} for name, raw in sorted(members.items())
    }
    members['SOURCE_MANIFEST.json'] = (json.dumps(source_manifest, indent=2) + '\n').encode()
    out = HERE / 'output'
    out.mkdir(exist_ok=True)
    source_zip = out / 'cellularization-vanishing-source-and-verification.zip'
    archive(source_zip, members)
    metadata = json.loads((HERE / 'zenodo-metadata.json').read_text())
    manifest = json.loads((HERE / 'zenodo-deposit.json').read_text())
    if manifest['metadata'] != metadata:
        raise SystemExit('Upload metadata and deposit manifest differ')
    upload_manifest = dict(manifest)
    upload_manifest['files'] = [
        {'path': 'cellularization-vanishing.pdf'},
        {'path': source_zip.name},
    ]
    kit = {
        'cellularization-vanishing.pdf': (out / 'pdf/cellularization-vanishing.pdf').read_bytes(),
        source_zip.name: source_zip.read_bytes(),
        'zenodo-metadata.json': (HERE / 'zenodo-metadata.json').read_bytes(),
        'zenodo-deposit.json': (json.dumps(upload_manifest, indent=2) + '\n').encode(),
        'README.md': (HERE / 'README.md').read_bytes(),
    }
    archive(out / 'zenodo-upload-kit.zip', kit)
    result = {
        'source_members': source_manifest,
        'files': {str(path.relative_to(HERE)): {'bytes': path.stat().st_size,
                                               'sha256': sha(path.read_bytes())}
                  for path in [out / 'pdf/cellularization-vanishing.pdf', source_zip,
                               out / 'zenodo-upload-kit.zip', HERE / 'main.tex',
                               HERE / 'zenodo-deposit.json']},
        'verifier': 'PASS',
        'optimized_python': 'rejected as required',
    }
    (HERE / 'PACKAGE_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['files', 'verifier', 'optimized_python']}, indent=2))


if __name__ == '__main__':
    main()
