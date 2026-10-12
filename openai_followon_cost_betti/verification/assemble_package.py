#!/usr/bin/env python3
"""Build a deterministic, explicit allowlist archive of this project's original work."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'publication'

def main():
    mapping={
        'main.tex':'publication/main.tex',
        'paper.pdf':'publication/paper.pdf',
        'README.md':'publication/README.md',
        'DEPENDENCIES.md':'DEPENDENCY_LEDGER.md',
        'upstream/UPSTREAM_MANIFEST.json':'sources/UPSTREAM_MANIFEST.json',
        'verification/verify_exact.py':'verification/verify_exact.py',
        'verification/exact_certificate.json':'receipts/exact_certificate.json',
        'verification/finite_boundary_check.py':'reviews/compression_audit/finite_boundary_check.py',
        'verification/finite_boundary_results.json':'reviews/compression_audit/finite_boundary_results.json',
        'reproducibility/software_versions.json':'receipts/software_versions.json',
        'reproducibility/upstream_tex_adaptation.json':'receipts/upstream_tex_adaptation.json',
        'reproducibility/clean_reproduction.json':'receipts/clean_reproduction.json',
        'priority/AUDIT.md':'notes/priority_audit/AUDIT.md',
        'priority/PUBLICATION_ELIGIBILITY_ADDENDUM.md':'notes/priority_audit/PUBLICATION_ELIGIBILITY_ADDENDUM.md',
        'priority/DIRECT_COMPUTATION_PRIORITY.md':'notes/priority_audit/DIRECT_COMPUTATION_PRIORITY.md',
        'priority/web_source_manifest.json':'notes/priority_audit/web_source_manifest.json',
        'priority/local_source_manifest.json':'notes/priority_audit/local_source_manifest.json',
        'priority/direct_computation_source_manifest.json':'notes/priority_audit/direct_computation_source_manifest.json',
        'priority/direct_computation_web_manifest.json':'notes/priority_audit/direct_computation_web_manifest.json',
        'verification/check_fox.py':'notes/classical_bridge/direct_review/check_fox.py',
        'verification/check_fox_results.json':'notes/classical_bridge/direct_review/check_results.json',
        'verification/verify_constants.py':'reviews/upstream_lower_audit/verify_constants.py',
        'verification/constants_certificate.json':'reviews/upstream_lower_audit/constants_certificate.json',
        'proof-audits/upper/AUDIT.md':'reviews/upstream_upper_audit/AUDIT.md',
        'proof-audits/upper/SOURCE_HASHES.json':'reviews/upstream_upper_audit/SOURCE_HASHES.json',
        'proof-audits/compression/AUDIT.md':'reviews/compression_audit/AUDIT.md',
        'proof-audits/lower/AUDIT.md':'reviews/upstream_lower_audit/lower_bound_audit.md',
        'proof-audits/lower/reviewed_sources.json':'reviews/upstream_lower_audit/reviewed_sources.json',
        'proof-audits/planar/AUDIT.md':'reviews/upstream_lower_audit/planar_falsifier/AUDIT.md',
        'proof-audits/classical/REPORT.md':'notes/classical_bridge/REPORT.md',
        'proof-audits/direct/DIRECT_BETTI.md':'notes/classical_bridge/DIRECT_BETTI.md',
        'proof-audits/direct/independent_review.md':'notes/classical_bridge/direct_review/AUDIT.md',
        'proof-audits/tree/PROOF.md':'notes/classical_bridge/special_s/PROOF.md',
        'proof-audits/tree/independent_review.md':'notes/classical_bridge/special_s/tree_zero_check/graph_operator_audit.md',
    }
    contents={}
    blobs={}
    for dest,source in mapping.items():
        path=ROOT/source
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f'Expected owned regular file missing: {source}')
        blobs[dest]=path.read_bytes()
        contents[dest]={'bytes':len(blobs[dest]),'sha256':hashlib.sha256(blobs[dest]).hexdigest(),'project_source':source}
    manifest={'license':'CC BY 4.0 for original material; third-party source PDFs/TeX excluded','files':contents,'scope':'Proofs and audits are mathematical evidence; exact computations have their recorded limited scope. No human peer review or machine formalization claimed.'}
    blobs['PACKAGE_CONTENTS.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    (PUBLIC/'PACKAGE_CONTENTS.json').write_bytes(blobs['PACKAGE_CONTENTS.json'])
    target=PUBLIC/'cost-betti-source-and-verification.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(blobs.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,data)
    print(json.dumps({'archive':str(target),'entries':len(blobs),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))

if __name__=='__main__':
    main()
