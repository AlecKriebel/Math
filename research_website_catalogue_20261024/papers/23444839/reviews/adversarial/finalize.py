from pathlib import Path
import json,hashlib,zipfile,datetime
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
SRC=BASE/'sources'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
primary_receipt=BASE/'reviews/scope/primary-source-receipts.json'
raw=json.loads(primary_receipt.read_text())
scopes={
'nevo-owr-2005':('Nevo contribution pp959–962, especially Theorem7 and Problem8.','Exact original question and two-CM definition; not the other workshop contributions.'),
'nevo-arxiv-v2':('Matching minimal-cycle decomposition theorem, question and two-CM definition.','Cross-edition check; not a full audit of the rigidity proof.'),
'nevo-published':('Definition3.1, Theorem3.4, Problem3.7 and surrounding context.','Exact union-of-subcomplexes question; no mapped or subdivided replacement.'),
'swartz-v1':('Section4 homology-sphere definition and Theorem4.1 context.','Global and all-link homology convention, equivalent Gorenstein* terminology.'),
'lsv-v2':('Sections2–4: lattice/flag geometry, cyclic algebra center/splitting and faithful conjugation; Eq9, Cor4.6, Definition4.7, Proposition4.8 and relevant proofs.','The imported vertex-regular action and polynomial representation interfaces were checked. Later Ramanujan-spectrum results are unnecessary and not audited.'),
'lm-author-alt':('Sections3.1–3.2 and Proposition3.3 with full degree/divisibility proof.','Its irreducible modulus theorem is not applied to t^9; the paper supplies its own kernel argument. Full primary body available.'),
'ballmann-swiatkowski':('Introductory Theorem1 and spectral conventions/strict threshold.','Attribution interface only; the finite weighted-cohomology proof is independently reconstructed in REVIEW.md.'),
'januszkiewicz-swiatkowski':('Example1.8, items3–6, especially item5.','Relevant Gauss–Bonnet obstruction antecedent; not the whole 85-page article.'),
'larson-stapledon-v2':('Introduction pp1–2, nearby decomposition/two-CM context.','Background only; not a complete proof or priority review.')}
entries=[]
for r in raw:
 if r['name'] not in scopes: continue
 p=Path(r['path']); assert sha(p)==r['sha256']
 extent,limit=scopes[r['name']]
 entries.append({k:r[k] for k in ['name','url','path','bytes','sha256']})
 entries[-1].update(read_extent=extent,interface_and_limits=limit)
assert len(entries)==9
write('primary-interfaces.json',{'completed_utc':now,'receipt_path':str(primary_receipt),'receipt_sha256':sha(primary_receipt),'entries':entries,'access_note':'Initial LM www-host TLS and IAS403 attempts failed; the author alternate PDF was retrieved and the relevant full proof read. No current LM-body access gap.','limits':['No full Chari/Baclawski primary-body audit.','No exhaustive literature search or priority certificate.','No sibling report or historical verdict body used.']})
receipt=json.loads((SRC/'receipt.json').read_text())
assert sha(SRC/'record.json')==receipt['record_sha256']
asset_checks=[]
for a in receipt['files']:
 p=SRC/a['name']; b=p.read_bytes()
 assert len(b)==a['bytes'] and hashlib.md5(b).hexdigest()==a['md5'] and sha(p)==a['sha256']
 asset_checks.append({'name':a['name'],'bytes':len(b),'md5':a['md5'],'sha256':a['sha256'],'matches_fresh_receipt':True})
member_checks=[]
for archive in receipt['archives']:
 with zipfile.ZipFile(SRC/archive['name']) as z:
  regs=[x for x in z.infolist() if not x.is_dir()]
  assert len(regs)==120
  expected={x['member']:x for x in archive['members']}
  for info in regs:
   data=z.read(info); p=SRC/'published-source'/info.filename
   h=hashlib.sha256(data).hexdigest()
   assert h==expected[info.filename]['sha256'] and p.read_bytes()==data
   member_checks.append({'member':info.filename,'sha256':h,'extracted_bytes_unchanged':True})
assert len(member_checks)==120
pdf=SRC/'spherefree-doubly-cm.pdf'
assert pdf.read_bytes()==(SRC/'published-source/output/pdf/spherefree-doubly-cm.pdf').read_bytes()
artifacts=[]
for p in sorted(HERE.iterdir()):
 if p.is_file() and p.name not in ['evidence-bindings.json','verdict.json','RESEARCH_LOG.md']:
  artifacts.append({'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
write('evidence-bindings.json',{'created_utc':now,'record_id':'23444839','fresh_record_sha256':sha(SRC/'record.json'),'fresh_source_receipt_sha256':sha(SRC/'receipt.json'),'public_assets':asset_checks,'source_main_tex_sha256':sha(SRC/'published-source/main.tex'),'all_120_regular_members_match_archive_and_receipt':True,'embedded_pdf_identical':True,'archive_members':member_checks,'review_artifacts':artifacts,'noncircular_binding_note':'This file binds fixed review artifacts; verdict binds this file; completion log records verdict hash. The finalizer does not bind itself recursively through generated outputs.','sources_unchanged':True})
verdict={
 'record_id':'23444839','title':"A negative answer to Nevo's homology-sphere decomposition question",'version':'1.0.0','role':'independent adversarial','completed_utc':now,'completion_percent':100,
 'verdict':'PASS_EXACT_STATED_THEOREM','publication_authorized':False,'human_peer_review':False,'formal_proof_certificate':False,'priority_certificate':False,
 'pdf_sha256':sha(pdf),'zip_sha256':asset_checks[1]['sha256'],'main_tex_sha256':sha(SRC/'published-source/main.tex'),'report_sha256':sha(HERE/'REVIEW.md'),'evidence_bindings_sha256':sha(HERE/'evidence-bindings.json'),'primary_interfaces_sha256':sha(HERE/'primary-interfaces.json'),
 'strongest_verified_result':'A finite pure two-dimensional abstract simplicial complex K is doubly Cohen–Macaulay over every characteristic-zero field and has no two-dimensional homology-sphere subcomplex over any field, with homology sphere understood through the global and all-face-link conditions. This answers Nevo’s stated union-decomposition question negatively.',
 'exact_checked_claims':[
  'Nevo original Problem8 and published Problem3.7 concern homology-sphere subcomplex pieces replacing minimal-cycle pieces; dimension two over Q is in scope.',
  'Faithful GL9(F11[t]) representation, vertex-regular building action, positive-generator lengths covering both neighbor types, finite-index normal kernel modulo t^9, and degree/divisibility displacement bound.',
  'The images-of-faces abstract quotient has no collapsed faces and every vertex link is the PG(2,11) incidence graph.',
  'Exact incidence Gram identity, girth at least six, and normalized spectral gap after any one link-vertex deletion at least (11-sqrt(11))/12 > 1/2.',
  'Purity, nonemptiness, connectivity and all face conditions for K and every vertex deletion, together with finite weighted-cocycle H1 vanishing and characteristic-zero transfer.',
  'Local-link homology-sphere edge/vertex conditions force triangle incidences and degree at least six, contradicting Euler characteristic two over any field.'
 ],
 'hypotheses_and_limits':[
  'F11 is the geometry field, not the homology coefficient field.',
  'Two-CM is proved for characteristic-zero fields; no positive-characteristic extension is certified.',
  'Homology sphere means all face links, including the empty face; no exclusion of global-only sphere homology objects is claimed.',
  'K is a finite abstract pure two-complex, not asserted to be a manifold, PL sphere or topological sphere.',
  'The quotient is defined using images of building faces, not a subsequent clique completion.',
  'No minimum size, full quotient computational enumeration, all-subcomplex enumeration, subdivision statement, or first-priority claim.'
 ],
 'fresh_controls':{
  'sequence':'Both fresh control families completed before packaged mathematical helper reading.',
  'affine_chart_incidence':'Exact PG(2,11) incidence and Gram identities, all266 deletions, degree/connectivity and incidence-mutant rejection.',
  'threshold_countercontrol':'Independent nine-vertex periodic torus, Betti(1,2,1), all links C6 with normalized gap1/2, nonzero harmonic cochain with energies36/36/72.',
  'cyclic_algebra':'Direct GF11(t) multiplication reconstructs generator and inverse conjugation matrices with polynomial degree1 and determinant1; does not construct the full lattice quotient.',
  'initial_control_issue':'Structural comparison of finite-field fraction4/4 and dense/sparse matrices produced a false assertion; exact entrywise/cross-multiplied checks corrected the control, with no paper defect.'
 },
 'published_replay':{'isolation':'Copy of120 source files in ignored local cache; source bytes independently rechecked unchanged.','default_verifier':'Exit0;2 normal/optimized positive runs and6 required mutation failures.','optional_matrix_diagnostic':'Exit0 normal; expected exit1 under optimized mode. Local exact arithmetic and float diagnostic spectrum only.','package_self_test':'Not run; not claimed.'},
 'dependencies':'Checked primary LSV lattice/building and faithful representation interfaces plus standard linear algebra; finite cohomology and Euler-count arguments independently reconstructed. LM irreducible-modulus theorem is not substituted for the actual t^9 proof.',
 'independence':{'sibling_or_archived_verdict_bodies_read':False,'incidental_exposure':'Historical filenames and manuscript/verification prior-review or priority assertions only. Replay authenticated historical files as opaque bytes without accepting their verdicts.','prior_ai_status_used_as_evidence':False},
 'substantive_defects':[],'exact_remaining_gap':'No substantive proof gap found within the stated model. Independent review is not a formal proof or human referee certification; full foundational building theory and exhaustive priority are outside this review.',
 'no_repairs':True,'sources_unchanged':True
}
write('verdict.json',verdict)
with (HERE/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n## '+now+' — 100%\n')
 f.write('Independent adversarial review complete: PASS for the exact stated theorem. Full paper and load-bearing primary interfaces checked; independent affine-incidence/deletion, strict-threshold torus, and direct cyclic-algebra controls pass. Published verifier replay is limited to its actual finite/local scope. No substantive defect or repair. All120 source members, public assets, and embedded PDF match their fresh receipt; no source mutation. Primary editions, read extents and limitations are preserved.\n\n')
 for n in ['REVIEW.md','verdict.json','evidence-bindings.json']:
  f.write(n+' SHA256: `'+sha(HERE/n)+'`\n\n')
print(json.dumps({'completed_utc':now,'verdict':verdict['verdict'],'report_sha256':sha(HERE/'REVIEW.md'),'verdict_sha256':sha(HERE/'verdict.json'),'evidence_sha256':sha(HERE/'evidence-bindings.json'),'regular_archive_members':len(member_checks)},indent=2))
