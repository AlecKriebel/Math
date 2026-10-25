from pathlib import Path
import json,hashlib,zipfile,datetime
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1];SRC=BASE/'sources';ROOT=SRC/'published-source/simple-brace-counterexample-source-and-verification'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,o):(HERE/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
primary_dir=BASE/'reviews/scope/cache/primary-sources'
observed=json.loads((primary_dir/'receipt.json').read_text())
scopes={
'owr-2019-51.pdf':{'read':'Cedó contribution printed3226–3228 in full, definitions/construction context and exact Problem9.','use':'Question exactly requires finite nontrivial simple left brace, metabelian multiplication and abelian Sylow subgroups; asks asymmetric product of two trivial left braces.'},
'asymmetric-1705.08493v1.pdf':{'read':'Relevant section2 star/trivial/ideal conventions; section3 full generalized cocycle definition, Theorem3.1, lambda formula, biadditive specialization and Lemma3.2.','use':'Primary full left-brace asymmetric-product interface and ideal-star closure. No later classification or all-paper proof audit claimed.'},
'abelian-2001.08905v1.pdf':{'read':'Section2 definitions, ideal/quotient discussion, Lemma2.1, Theorem2.2, subtraction/lambda formulas, bilinear specialization and Lemma2.3 with even-order boundary.','use':'Independent primary confirmation of the generalized product definition and non-split additive boundary; no later construction theorem imported.'},
'matched-1511.08477v3.pdf':{'read':'Definitions2.1,2.4,2.5, lambda Lemmas2.3/2.6; section4 setup, matched-pair Definition4.1 and Theorem4.2 statement/converse and initial proof interface.','use':'Definitions and matched-product context. The present direct construction proof does not require the full matched-product theorem or its simplicity classifications.'}}
entries=[]
for r in observed['sources']:
 if r.get('filename') not in scopes:continue
 p=primary_dir/r['filename'];assert sha(p)==r['sha256']
 entries.append({**{k:r[k] for k in ['filename','url','sha256','bytes']},'local_path':str(p),**scopes[r['filename']]})
assert len(entries)==4
save('primary-interfaces.json',{'created_utc':now,'shared_receipt_sha256_as_observed':sha(primary_dir/'receipt.json'),'sources':entries,'body_access':'All four relevant primary bodies available. Original CCS journal body not independently audited; its full left-brace formulation checked in two author primary papers.','not_certified':['Full original CCS journal proof.','Entire later construction/classification literature and cited2026 papers.','All final journal editions.','Historical first priority or minimum order.'],'web_metadata_crosschecks':['https://arxiv.org/abs/1705.08493v1','https://arxiv.org/abs/2001.08905v1'],'web_doi_tool_note':'The web tool could not resolve DOI10.4171/OWR/2019/51, but the complete EMS-hosted original report was available, hash-bound and read.'})
receipt=json.loads((SRC/'receipt.json').read_text());assert sha(SRC/'record.json')==receipt['record_sha256']
assets=[]
for a in receipt['files']:
 p=SRC/a['name'];data=p.read_bytes();assert len(data)==a['bytes'] and hashlib.md5(data).hexdigest()==a['md5'] and sha(p)==a['sha256']
 assets.append({**a,'fresh_receipt_match':True})
extract=json.loads((SRC/'extraction-integrity.json').read_text());expected={x['member']:x for x in extract['members']}
checks=[]
with zipfile.ZipFile(SRC/'simple-brace-counterexample-source-and-verification.zip') as z:
 regular=[i for i in z.infolist() if not i.is_dir()];assert len(regular)==79
 for info in regular:
  data=z.read(info);a=expected[info.filename];p=SRC/a['path'];h=hashlib.sha256(data).hexdigest()
  assert h==a['sha256'] and p.read_bytes()==data and len(data)==a['bytes']
  checks.append({'member':info.filename,'source_relative_path':a['path'],'bytes':len(data),'sha256':h,'unchanged':True})
assert (ROOT/'output/pdf/simple-brace-counterexample.pdf').read_bytes()==(SRC/'simple-brace-counterexample.pdf').read_bytes()
replay=json.loads((HERE/'replay.json').read_text());assert replay['status']=='PASS' and replay['sources_unchanged']
controls=json.loads((HERE/'fresh-controls.json').read_text());assert controls['status']=='PASS'
art=[]
for p in sorted(HERE.iterdir()):
 if p.is_file() and p.name not in ['evidence-bindings.json','verdict.json','RESEARCH_LOG.md']:
  art.append({'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
save('evidence-bindings.json',{'created_utc':now,'record_id':'23441906','record_sha256':sha(SRC/'record.json'),'receipt_sha256':sha(SRC/'receipt.json'),'extraction_receipt_sha256':sha(SRC/'extraction-integrity.json'),'reader_map_sha256':sha(SRC/'reader-pdf-map.json'),'public_assets':assets,'all79_regular_members_verified_unchanged':True,'embedded_main_pdf_identical':True,'members':checks,'artifacts':art,'binding_order':'Fixed review/control artifacts are bound here; verdict binds this file; final research log records verdict hash.'})
verdict={
'record_id':'23441906','title':'A simple brace outside asymmetric products of two trivial braces','version':'1.0.0','date':'2026-10-17','role':'independent analytic','completed_utc':now,'completion_percent':100,'verdict':'PASS_EXACT_STATED_THEOREM',
'pdf_sha256':sha(SRC/'simple-brace-counterexample.pdf'),'zip_sha256':sha(SRC/'simple-brace-counterexample-source-and-verification.zip'),'main_tex_sha256':sha(ROOT/'main.tex'),'original_proof_sha256':sha(ROOT/'audit/inputs/PROOF.md'),'report_sha256':sha(HERE/'REVIEW.md'),'evidence_bindings_sha256':sha(HERE/'evidence-bindings.json'),'primary_interfaces_sha256':sha(HERE/'primary-interfaces.json'),
'strongest_verified_result':'The explicit order20000 finite nontrivial simple left brace has additive group C5^4 × C2^5 and multiplicative group (C5^3 semidirect C2) × (C2^4 semidirect C5), is metabelian with all multiplicative Sylow subgroups abelian, and is not brace-isomorphic to any admissible asymmetric product of two trivial left braces. It answers the exact OWR51/2019 Problem9 negatively.',
'exact_checked_claims':[
'Full generalized normalized symmetric-cocycle asymmetric-product definition agrees with two primary left-brace formulations; brace admissibility forces biadditivity for two trivial factors.',
'The set Tp × Sp is both the unique additive p-primary subgroup and a multiplicative Sylow subgroup, without assuming split addition, including p=2.',
'Abelian multiplicative Sylow groups force their same-primary action to be trivial and hence every left-associated primary triple star to vanish in every such presentation.',
'Explicit truncated log/exp over F5, binary quadratic polarization and fixed-point-free rotation establish the bijective transport to the stated direct product of semidirect groups.',
'All lambda maps are additive automorphisms; group identity, associativity and inverses follow universally from the coordinate transport.',
'Derived group C5^2 × C2^4 has order400; chosen Sylows have orders625 and32 and are abelian; conjugacy covers every Sylow.',
'Ideal normality plus lambda invariance justify both propagation rules; every nonzero ideal reaches all nine additive generators.',
'On P5 the star operation is ring multiplication; (x*x)*x=x^3 is nonzero and is an isomorphism-invariant obstruction.',
'Original support’s redundant fixed-set order10, center order5, abelianization order50 and derived-star witnesses agree with the explicit construction and their exact two-trivial-factor scope.'
],
'fresh_evidence':{'script':'fresh_controls.py','results':'fresh-controls.json','direction_receipts':'fresh-ideal-directions.json','before_packaged_helpers':True,'ring_pairs':390625,'full_element_inverse_and_bijection_checks':20000,'supplemental_generator_transport_pairs':180000,'prime_projective_ideal_directions':187,'all_direction_final_ranks':[4,5],'boundaries':['C4 non-split addition with zero triples.','D8 multiplicative Sylow example with a nonzero triple, showing the abelian-Sylow assumption is necessary.','C3 carry cocycle fails brace admissibility.','Removing sign strands scalar binary line; removing rotation strands ring part.'],'implementation_corrections':['Replaced Python3.10-only bit_count for Python3.9 fresh runtime.','Corrected own no-sign mutant expectation from full binary part to scalar line; both are proper, and original theorem unaffected.']},
'reproduction':{'status':'PASS','runs':8,'programs':4,'modes':['ordinary','optimized'],'python':'3.12.14','source_files':79,'source_bytes_unchanged':True,'seed_derivation_certificate_sha256':'50457c40dc45d0a3fd6c685830ad024e89c2a21c47552eda9718e403c1ad28c7','sample_trace_certificate_sha256':'a076a48e252be8b03ddf76d03e7edb7cdde335f6c04c956e174db38e5dac5345','certificate_comparison':'Published runner regenerated and compared both certificate bytes in ordinary and optimized modes.'},
'independence':{'sibling_reports_read':False,'dedicated_archived_review_bodies_read':False,'incidental_exposure':'Necessary manuscript/original PROOF.md prior-audit and acceptance assertions, historical filenames, and code references to archived reports. None treated as evidence. Numeric expected computational results read by the isolated verifier are distinguished from reviewer assessments.'},
'defects':[],'exact_remaining_gap':'No substantive proof gap found within the exact theorem. Bibliographic novelty and first priority are not certified; not all cited background literature/final editions were independently audited.','limits':['No minimum-order or universal classification result.','Only asymmetric products of two trivial factors are excluded; general matched products and nontrivial-factor constructions are not.','No enumeration of all20000^3 operation triples or all candidate presentations.','No human peer review or formal proof-assistant certification.'],
'publication_authorized':False,'human_peer_review':False,'formal_proof_certificate':False,'priority_certificate':False,'no_repairs':True,'sources_unchanged':True}
save('verdict.json',verdict)
with (HERE/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n## '+now+' — 100%\nFinal analytic PASS for the exact theorem. Full five-page manuscript, all necessary mathematical support and four programs read; all five PDF pages visually inspected. Original problem and generalized product interfaces checked in primary bodies. Fresh controls and eight isolated published runs pass, with all79 source members unchanged and embedded main PDF identical. No substantive defect, source repair or publication mutation. Exact literature and computational limits retained.\n\n')
 for name in ['REVIEW.md','verdict.json','evidence-bindings.json']:
  f.write(name+' SHA256: `'+sha(HERE/name)+'`\n\n')
for a in art:assert sha(HERE/a['name'])==a['sha256']
print(json.dumps({'completed_utc':now,'verdict':verdict['verdict'],'report_sha256':sha(HERE/'REVIEW.md'),'verdict_sha256':sha(HERE/'verdict.json'),'evidence_sha256':sha(HERE/'evidence-bindings.json'),'source_files_unchanged':79},indent=2))
