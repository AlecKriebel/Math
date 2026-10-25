#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,datetime
P=Path(__file__).resolve().parents[1];B=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
c=json.loads((P/'evidence/custody.json').read_text())
primary_scopes={
'owr2017-50-published.pdf':{'read':'Harvey contribution printed3020–3021, entire contribution and surrounding Question3/derived definition','interface':'Ordinary derived pure-braid containment into the standard solvable filtration','role':'Question identity/attribution'},
'gambaudo-ghys-published.pdf':{'read':'Printed542–545,567–569,574–575: definitions, TheoremA, Remarks1–3, specifically n=3 Lemma4.1, homogenization','interface':'Pointwise ordinary link signature, exact Meyer cocycle, split-strand invariance and homogeneous error bound6 on B3','role':'Load-bearing'},
'otto-published.pdf':{'read':'Printed2631–2632 Section2 and complete Definition2.3','interface':'Compact smooth integral1-solution, free H1, complete framed hyperbolic basis, both surface families in ordinary commutator subgroup, closure convention and descending filtration','role':'Load-bearing definition'},
 'toffoli-published.pdf':{'read':'Internal1–2,9,20–22,27–31 including Theorem2.6(ii), domain/compatible framing, Theorem4.24 and its proof, Remark4.25','interface':'Bounding rho/signature identity and pointwise one-colour surgery formula on U(1) minus1, with all corrections zero for algebraically split zero framing','role':'Load-bearing'},
'calegari-scl-author.pdf':{'read':'Printed27 amenability and33 Proposition2.65 with proof','interface':'Solvable discrete groups amenable; homogeneous real quasimorphisms on amenable groups homomorphisms','role':'Load-bearing'},
'kkmmm-published.pdf':{'read':'Printed1206–1207 Lemmas7.10 and7.12 and proofs','interface':'Equality of quasimorphism defects on normal subgroup with solvable quotient','role':'Credited stronger known result; not necessary for the manuscript proof via amenability'},
'erle-published.pdf':{'read':'Printed161–165 plus visual163–164','interface':'Standard3-braid checkerboard incidence signs, small-region cases and signature correction; actual crossing construction resolves displayed off-diagonal index issue','role':'Explicit finite witness support; universal proof independent of this computation'}
}
ledger=[]
for row in c['primary_sources']:
 ledger.append({**row,**primary_scopes[row['name']],'pdf_path':str(B/'reviews/scope/cache/primary-sources'/row['name']),'complete_work_read':False})
(P/'evidence/primary-interface-ledger.json').write_text(json.dumps({'utc':now,'primary_text_custody':'primary-text-custody.json','sources':ledger,'inaccessible_load_bearing_interfaces':[],'limits':'Exact theorem interfaces reviewed; no claim to reprove underlying APS analytic index theorem or to read entire book/article bodies.'},indent=2)+'\n')
# Check sources and the pre-helper seal once more; no replay rerun is needed.
for f in c['public_assets']:assert sha(B/'sources'/f['name'])==f['sha256']
for m in c['members']:assert sha(B/'sources/published-source/deep-derived-pure-braids-source-verification-v1.0'/m['member'])==m['sha256']
seal=json.loads((P/'evidence/pre-helper-seal.json').read_text())
for f in seal['files']:assert sha(P/f['path'])==f['sha256']
v={'schema_version':1,'record_id':'23393596','role':'independent_adversarial','status':'PASS','verdict':'PASS','completion_percent':100,'completed_utc':now,
'source_binding':{'receipt_path':str(B/'sources/receipt.json'),'receipt_sha256':c['receipt_sha256'],'record_path':str(B/'sources/record.json'),'record_sha256':c['record_sha256'],'public_assets':c['public_assets'],'metadata':c['metadata'],'main_pdf_pages':4,'archive_regular_members':213,'embedded_reader_equals_main_pdf':True,'members_verified_unchanged_at_completion':True},
'exact_claim':'For every integer m>=3 and every finite integer k>=1, P_m^(k) is not contained in F_1^m for the ordinary derived series and integral smooth1-solvability via standard closure; hence P_m^(n+2) is not contained in F_n^m for every integer n>=1.',
'strongest_verified_claim':'Entire stated theorem and its corollary at the exact domain above, plus the explicit104-crossing P_3^(3) witness with signature-2, Goeritz inertia(23,25,0) and determinant-7154819319988224.',
'exact_remaining_gap':None,'substantive_defects':[],
'independence':{'pre_helper_seal_sha256':sha(P/'evidence/pre-helper-seal.json'),'pre_helper_seal_utc':seal['utc'],'fresh_controls_before_helper_read_or_execution':True,'sibling_or_dedicated_historical_assessment_bodies_read':False,'incidental_exposure':'Historical status/priority/attempt-count strings in current manuscript and necessary mathematical PROOF supports, later descriptive strings in finite helpers. Not adopted as correctness evidence. Opaque archive bytes hashed only.','strict_source_blindness_claimed':False},
'evidence':{'independent_exact_controls':'evidence/independent-controls.json','code':'evidence/independent_controls.py','independent_signature':-2,'goeritz_inertia':[23,25,0],'goeritz_determinant':'-7154819319988224','package_replay':'evidence/package-replay.stdout.json','package_replay_receipt':'evidence/package-replay-receipt.json','negative_controls':'evidence/post-helper-controls.json','primary_interfaces':'evidence/primary-interface-ledger.json','custody':'evidence/custody.json'},
'limitations':['AI-assisted mathematical review only; not independent human peer review or formal certification.','Arbitrary-depth witnesses may depend on finite k and are existential; explicit recorded word addresses k=3 only.','No claim for m=1,2, one braid in every derived term, a rational/topological variant, or arbitrary-complex-character version of the mod2 rank argument.','No novel status assigned to quasimorphism/amenability/defect-restriction/signature inputs.','No first-priority, continued-openness or journal-suitability certification.','Historical transport/recovery suites and priority searches were not re-executed.'],
'nonblocking_notes':['Erle displayed off-diagonal indexing issue was inspected; crossing geometry and separate Meyer calculation support current construction. The wrong index is invariant-insensitive on the main witness, explicitly documented.','Two local reviewer-control expectations failed, were transparently preserved and narrowed/corrected; neither is a manuscript defect.'],
'follow_up':None,'promotion_authorized':False,'external_or_publication_mutations':False,'report_sha256':sha(P/'REVIEW.md')}
(P/'verdict.json').write_text(json.dumps(v,indent=2)+'\n')
with (P/'LOG.md').open('a') as f:f.write('\n## '+now+' — 100%\nIndependent adversarial review complete: PASS at the exact smooth integral, ordinary-derived, finite-depth scope. Full claim/proof audit, primary-interface ledger, both fresh exact signature mechanisms, published replay, negative controls, unchanged-byte custody and limitations are documented. Original sources and pre-helper seal still match; no mathematical repair or public mutation was performed. Final evidence manifest seals the durable report/verdict/log and artifacts.\n')
files=[]
for f in sorted(P.rglob('*')):
 if not f.is_file() or 'replay-work' in f.parts or f.name=='evidence-manifest.json' or '__pycache__' in f.parts:continue
 files.append({'path':f.relative_to(P).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
manifest={'schema_version':1,'completed_utc':now,'record_id':'23393596','role':'adversarial','completion_percent':100,'artifact_count':len(files),'files':files,'scratch_excluded':'replay-work/; all substantive checks, results, source bindings and replay commands are preserved outside scratch.'}
(P/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'verdict':'PASS','completed_utc':now,'artifact_count':len(files),'report_sha256':sha(P/'REVIEW.md'),'verdict_sha256':sha(P/'verdict.json'),'manifest_sha256':sha(P/'evidence-manifest.json')},indent=2))
