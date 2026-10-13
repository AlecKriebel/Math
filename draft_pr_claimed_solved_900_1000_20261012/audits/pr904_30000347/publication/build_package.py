#!/usr/bin/env python3
"""Build a deterministic source archive using only the public file allowlist."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FROZEN = AUDIT/'original/unsolved_math_prioritization/attempts/30000347'
DEST = HERE/'tmp/bundle'
REVIEW_FILES = {
    'proof_family': ['AUDIT.md', 'RESEARCH_LOG.md', 'independent_checks.py', 'independent_results.json'],
    'computation_family': ['AUDIT.md', 'audit_result.json', 'independent_structural_checks.py',
                          'independent_structural_results.json', 'independent_structural_results_optimized.json',
                          'optimization_and_integrity_controls.py', 'optimization_and_integrity_results.json',
                          'replay_normal.json', 'replay_optimized.json', 'submitted_mutation_results.json'],
    'source_model_family': ['SOURCE_MODEL_REPORT.md', 'SOURCE_MODEL_MANIFEST.json'],
    'priority_family': ['PRIORITY_AUDIT.md', 'SOURCE_MANIFEST.json', 'QUERY_LOG.md',
                        'CITING_KRAUSE.json', 'CITING_BIENSTOCK.json'],
}

def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    shutil.copytree(FROZEN, DEST/'original_packet')
    for name in ['note.tex', 'README.md', 'verify_package.py']:
        shutil.copy2(HERE/name, DEST/name)
    for family, files in REVIEW_FILES.items():
        p = DEST/'reviews'/family
        p.mkdir(parents=True)
        for name in files:
            shutil.copy2(AUDIT/'reviews'/family/name, p/name)
    pdf = HERE/'output/pdf/note.pdf'
    files = {}
    for p in sorted(DEST.rglob('*')):
        if not p.is_file():
            continue
        if p.is_symlink():
            raise ValueError('Symlink in package')
        files[p.relative_to(DEST).as_posix()] = {'bytes': p.stat().st_size,
                                               'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    manifest = {'problem_id': 30000347, 'pr_number': 904,
                'original_pr_head': 'd67d11bcb7d1e730daf9be7555c75950d3484b5d',
                'version': '1.0', 'files': files,
                'separate_pdf': {'name': 'three-terminal-shortest-path-blocking-v1.0.pdf',
                                 'bytes': pdf.stat().st_size,
                                 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest()},
                'claim_scope': 'Undirected triangle BSP NP-completeness; unit costs and original distances 3; finite and exact 3-to-4 variants',
                'review_status': 'Unrefereed; extensive AI assistance; no independent human peer review',
                'priority': 'Historical first priority not asserted; see bounded priority audit',
                'trust_boundary': 'Hash consistency against trusted verifier/manifest; not proof-assistant certification'}
    (DEST/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
    archive = HERE/'three-terminal-bsp-source-verification-v1.0.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(DEST.rglob('*')):
            if p.is_file():
                info = zipfile.ZipInfo(p.relative_to(DEST).as_posix(), date_time=(2026,10,12,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, p.read_bytes())
    receipt = {'files': len(files)+1, 'archive_bytes': archive.stat().st_size,
               'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
               'pdf_sha256': manifest['separate_pdf']['sha256'],
               'manifest_sha256': hashlib.sha256((DEST/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest()}
    (HERE/'PACKAGE_BUILD.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
