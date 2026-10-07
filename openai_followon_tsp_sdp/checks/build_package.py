#!/usr/bin/env python3
"""Deterministically assemble exactly the intended authored publication payload."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'publication/zenodo-upload-kit';KIT.mkdir(parents=True,exist_ok=True)
SOURCE=['main.tex','CITATIONS.bib','LICENSES.md','LICENSE_CODE.txt','publication/README.md']
VERIFICATION=['README.md','LICENSES.md','LICENSE_CODE.txt','DEPENDENCY_LEDGER.md','THEOREM_LEDGER.md','APPROACH_TABLE.md','RESEARCH_LOG.md','CITATIONS.bib',
'proofs/tsp_reduction.md','proofs/upper_bound.md',
'agent_notes/upstream_adversary.md','agent_notes/source_bridge.md','agent_notes/tsp_reduction.md','agent_notes/independent_geometry.md','agent_notes/priority_audit.md','agent_notes/upstream_adversary_checks.py','agent_notes/upstream_adversary_checks.json',
'checks/tsp_reduction_check.py','checks/tsp_reduction_results.json','checks/independent_geometry_checks.py','checks/independent_geometry_checks.json','checks/source_bridge_audit.py','checks/source_bridge_receipt.json','checks/source_bridge_finite_results.json','checks/fetch_pinned_sections.py','checks/reproduce.py',
'receipts/upstream_source_hashes.json','receipts/pdf_visual_verification.json','sources/priority_evidence_manifest.json','publication/README.md']
def make(name,files):
    with zipfile.ZipFile(KIT/name,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in sorted(files):
            info=zipfile.ZipInfo(rel,date_time=(2026,10,6,22,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,(ROOT/rel).read_bytes())
    return {rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in files}
source=make('tsp-source.zip',SOURCE);verification=make('tsp-verification.zip',VERIFICATION)
shutil.copyfile(ROOT/'publication/paper.pdf',KIT/'paper.pdf')
metadata={
 'title':'Exact semidefinite complexity of the symmetric traveling-salesman polytope',
 'upload_type':'publication','publication_type':'preprint','publication_date':'2026-10-06',
 'description':'The exponential real PSD-rank theorem for shifted perfect-matching matrices in the OpenAI Math Release implies that the symmetric traveling-salesman polytope on N cities has exact real semidefinite extension complexity 2^Theta(N), measured by the order of one real PSD matrix (or total block order). This concise consequence note gives explicit data for Yannakakis\'s established 3n-city face projection, a 2n-city contraction variant, all-city-count padding, an exact affine-slack calculation, and the subset-state flow upper bound 2(N-1)+(N-1)(N-2)2^(N-3). The lower-bound breakthrough is attributed to OpenAI; no new lower-bound method or firstness claim is made. Independent mathematical audits examined the central matching proof and found no material defect. The supplied Lean statements cover only superpolynomial matching bounds; neither the exponential input nor this follow-on theorem is claimed to be formally verified. The deposit includes a separately downloadable PDF, standalone source, and reproducible finite checks with audit and dependency records. AI tools were used extensively in research, drafting and verification. This preprint has not undergone conventional human peer review or refereeing; automated reviews are not human peer review. Exact real lifts only; no approximate-relaxation, hierarchy-specific or P-versus-NP assertion.',
 'creators':[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}],
 'access_right':'open','license':'cc-by-4.0',
 'keywords':['semidefinite extension complexity','traveling-salesman polytope','positive semidefinite rank','perfect matching','polyhedral reductions'],
 'related_identifiers':[
  {'identifier':'https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Exponential-PSD-rank-of-positively-shifted-matching-matrices-October-5-2026/shifted-matching-psd.pdf','relation':'references','scheme':'url'},
  {'identifier':'10.1016/0022-0000(91)90024-Y','relation':'references','scheme':'doi'},
  {'identifier':'10.4230/LIPIcs.CCC.2016.17','relation':'references','scheme':'doi'}]
}
manifest={'metadata':metadata,'files':[{'path':'publication/zenodo-upload-kit/'+name,'name':name} for name in ['paper.pdf','tsp-source.zip','tsp-verification.zip']]}
(ROOT/'zenodo-deposit.json').write_text(json.dumps(manifest,indent=2)+'\n')
checks={name:{'bytes':(KIT/name).stat().st_size,'sha256':hashlib.sha256((KIT/name).read_bytes()).hexdigest(),'md5':hashlib.md5((KIT/name).read_bytes()).hexdigest()} for name in ['paper.pdf','tsp-source.zip','tsp-verification.zip']}
frozen={'version':'candidate-v1','manifest_sha256':hashlib.sha256((ROOT/'zenodo-deposit.json').read_bytes()).hexdigest(),'payload':checks,'source_members_sha256':source,'verification_members_sha256':verification,'note':'Complete-package reviews are retained outside this frozen payload, with exact reviewed hashes; archive hashes have no recursive dependency on their reviews.'}
(ROOT/'receipts/frozen_candidate_v1.json').write_text(json.dumps(frozen,indent=2)+'\n')
print(json.dumps(checks,indent=2))
