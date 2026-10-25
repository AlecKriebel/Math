#!/usr/bin/env python3
"""Finalize this bounded analytic review, with no source or sibling mutations."""
from pathlib import Path
import datetime,hashlib,json,zipfile
O=Path(__file__).resolve().parent;P=O.parents[1];S=P/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def binding(p):return {'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,value):
 with p.open('x') as f:f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert sha(S/'paper.pdf')=='62982a0e0508edabbfea63f4b5dc69ffe928d7c657103ee3d31296a6393e5d8c'
assert sha(S/'source-and-verification.zip')=='738ccb98e973b71f642f83a8abdb05559ad58073b7a2dde79e785f869e6a567c'
assert sha(S/'published-source/owr_4136_011_equality/manuscript/paper.tex')=='ce8a48dc12ac9d80144a7de7391f2583c6d567c5d4d1067c3be122bf10283b29'
assert sha(S/'SOURCE_READY_SEAL.json')=='3c221c98107e97be91df574faef65935f19001dae45418a2edfdd5bfc5059c70'
assert sha(O/'independent-initial-seal.json')=='81d0a1e23d3b2c4cfa221ce7bb073047e3d5769f30a72ec545dbccfe3eb92b1a'
initial=load(O/'source-baseline.json')['files'];custody=[]
for row in initial:
 current=binding(P/row['path']);assert current==row,row['path'];custody.append({'before':row,'after':current,'unchanged':True})
members=[]
with zipfile.ZipFile(S/'source-and-verification.zip') as archive:
 for item in archive.infolist():
  if item.is_dir():continue
  target=S/'published-source'/item.filename
  assert target.read_bytes()==archive.read(item),item.filename
  members.append({'member':item.filename,'bytes':item.file_size,'sha256':sha(target)})
assert len(members)==29
assert (S/'published-source/owr_4136_011_equality/output/pdf/paper.pdf').read_bytes()==(S/'paper.pdf').read_bytes()
prefix='sources/published-source/owr_4136_011_equality/'
reads=[]
for row in initial:
 name=row['path'];local=name[len(prefix):] if name.startswith(prefix) else None
 if name=='sources/paper.pdf':extent='Entire actual four-page PDF text and all four rendered pages read before independent initial seal.'
 elif local=='manuscript/paper.tex':extent='Entire actual TeX read before independent initial seal.'
 elif local=='output/pdf/paper.pdf':extent='Byte-identical embedded duplicate of fully read selected PDF; no second independent reader claimed.'
 elif name in ['sources/SOURCE_READY.json','sources/SOURCE_READY_SEAL.json']:extent='Complete source identity/receipt JSON read; all selected initial source bindings rehashed.'
 elif local=='audit/independent-proof.md':extent='Complete finite-approximation proof and boundary discussion read after initial seal; historical favorable opinion treated as submitted evidence, never adopted as a fresh verdict.'
 elif local=='verification/verify.py':extent='Entire program read statically after initial seal; never executed, imported or compiled.'
 else:extent='Inventoried and authenticated only; no complete substantive reading or adoption of historical opinion claimed.'
 reads.append({**row,'read_extent':extent})
primary=[]
specs={
 'fps-published':{'edition':'Published Canadian Mathematical Bulletin55(3),2012,498–508;11physicalpages; printed firstpage electronicdate8July2011.',
 'read_physical_pages':[1,2,3,5,6,7],'visually_read_pages':[2,5,6,7],
 'interfaces':'Exact Theorem1.1, posttheorem general-body equality conjecture, origin/affine caveat, Lemma3.1 and3.2 with full proofs and n>=1 moment formula, simplex remark with explicit >=r, entire relevant Theorem1.1 polytope and general approximation proof.',
 'reading_limits':'Not all11pages or unrelated John/Löwner-position results read. No current worldwide priority inference from historical conjecture.'},
 'owr-ems':{'edition':'Published EMS OWR53/2009 volume;76physicalpages; entire Fradelizi contribution printed2907–2909.',
 'read_physical_pages':[57,58,59],'visually_read_pages':[58],
 'interfaces':'Complete relevant contribution, exact centroid-corrected theorem and general-body equality conjecture, historical stronger-than wording and sphere equality convention.',
 'reading_limits':'Other contributions in the76page volume not read. No current open-status/priority conclusion.'},
 'fps-author':{'read_extent':'Ordinary acquisition failed TLS certificate verification; no body obtained or read. Published journal body was successfully obtained instead.','access_bypass':False}
}
for row in load(O/'primary-acquisition.json')['sources']:
 if row.get('raw_path'):
  assert sha(O/row['raw_path'])==row['sha256']
  assert sha(O/row['text_path'])==row['text_sha256']
 primary.append({**row,**specs[row['name']]})
save(O/'read-ledger.json',{'record_id':'22983138','utc':now,'source_files':reads,'primary_bodies':primary,
 'initial_independence_seal_sha256':sha(O/'independent-initial-seal.json'),
 'primary_body_and_extract_private_directory':'reviews/analytic/primary-cache/;entire directory ignored before acquisition',
 'current_sibling_or_root_mathematical_reports_read':False,
 'source_programs_run_imported_or_compiled':False,
 'own_independent_controls':'reviews/analytic/check_exact.py; repeated polynomial integration, exact cross-section and shell controls',
 'geometric_imports':'Finite-dimensional extreme-point representation and convex boundary nullity checked by elementary reasoning in REPORT.md, not extended to infinite dimensions.',
 'whole_download_not_whole_read':True})
save(O/'custody-before-after.json',{'record_id':'22983138','utc':now,'all_initial_authorities_unchanged':True,
 'source_files':custody,'archive_regular_members':members,'all_archive_member_bytes_match_extraction':True,
 'embedded_pdf_identical':True,'initial_independence_seal_unchanged':True,
 'source_sibling_prior_package_mutations':False,'own_write_scope':'reviews/analytic/'})
run=load(O/'exact-run.json');exact=load(O/'exact-results.json')
assert not run['timed_out'] and run['returncode']==0 and not run['stderr']
assert len(exact['checks'])==121 and all(row['verified'] for row in exact['checks'])
save(O/'verdict.json',{'record_id':'22983138','sheet_row':87,'utc':now,
 'task_status':'COMPLETE','completion_estimate_percent_of_assigned_analytic_review':100,
 'mathematical_verdict':'PASS_FULL_ORIGINAL_ANALYTIC_EQUALITY_THEOREM',
 'full_original_theorem_verified_in_this_lane':True,'original_claim_weakened':False,
 'exact_target':'Alln>=1,r>0, compact full-dimensional convexK with||v||>=r for every extreme point: C2(K)>=[r²+(n+1)||gK||²]/(n+2), equality iff a nondegenerate simplex with every vertex onradiusr sphere.',
 'verified_mechanisms':['Countable retained extreme-vertex shell partition with full-volume coverage.','Exact absolutely convergent nonnegative deficit.','Same-centroid shared-interior equality rigidity.','Retained finite positive witness survives approximation.','Exactn1/non-strict/strictnorm/zero-volume exclusions and no centering/origin/regularity assumptions.'],
 'central_defect_found':False,'unresolved_mathematical_gap':None,
 'primary_published_proof_body_read':True,'prior_credit':'FPSinequality,simplex moment formula,vertex triangulation andpolytope common-centroid rigidity are established prior results; classical finite-dimensional convexgeometry is credited.',
 'priority_status':'UNKNOWN inthis analytic lane;historical conjecture authenticated, no worldwide firstness/current-open inference.',
 'independent_exact_controls':121,'finite_controls_claimed_to_prove_universal_theorem':False,
 'source_programs_run_imported_or_compiled':False,'current_sibling_or_root_reports_read':False,
 'publication_clearance':False,'page_promotion_permission':False,
 'public_page_rendered':False,'live_action':False,'browser_UI_used':False,
 'native_Sheet_mutated':False,'native_AA':None,
 'follow_up':None,'external_contact_or_outreach':False,
 'prior_Basin_and_Langlands_seals_modified':False})
save(O/'validation.json',{'record_id':'22983138','utc':now,'source_bindings_rehashed':len(initial),
 'all_initial_sources_unchanged':True,'archive_regular_members_verified':len(members),
 'selected_hashes_equal_assignment':True,'primary_body_text_hashes_equal_receipts':True,
 'initial_independence_seal_unchanged':True,'independent_exact_controls_passed':121,
 'bounded_run_completed':True,'submitted_programs_executed':False,
 'mathematical_verdict_scope':'This lane full-original theorem only;root separate complete-package/promotion gates remain.'})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Complete analytic report, exact read ledger, original-source/member before-after custody and custom verdict finalized. Completion: **100% of assigned analytic review**. Full original mathematical theorem verified; all121 owned exact controls passed; no remaining analytic gap found. Priority not adjudicated; publication/native/root gates remain separate. Original sources and previous task handoffs unchanged; no submitted code execution, current sibling report reading, repair campaign, external communication or shared/public/native/Git mutation.\n')
exclude={'SEAL.json','SEAL.sha256','SHA256SUMS'}
files=sorted(f for f in O.rglob('*') if f.is_file() and f.name not in exclude)
seal={'record_id':'22983138','utc':now,'seal_kind':'INDEPENDENT_ANALYTIC_FULL_ORIGINAL_THEOREM_HANDOFF',
 'mathematical_verdict':'PASS_FULL_ORIGINAL_ANALYTIC_EQUALITY_THEOREM','publication_clearance':False,
 'source_authorities':[binding(P/row['path']) for row in initial],
 'review_files':[binding(f) for f in files],
 'initial_independence_seal_sha256':sha(O/'independent-initial-seal.json'),
 'third_party_raw_bodies_and_excerpts_private_entire_ignored_cache':True,
 'excludes_self_and_sha_manifests':True}
save(O/'SEAL.json',seal)
(O/'SEAL.sha256').write_text(sha(O/'SEAL.json')+'  SEAL.json\n')
with (O/'SHA256SUMS').open('x') as f:
 for row in seal['source_authorities']+seal['review_files']:f.write(row['sha256']+'  '+row['path']+'\n')
 f.write(sha(O/'SEAL.json')+'  reviews/analytic/SEAL.json\n')
print(json.dumps({'record_id':'22983138','status':'COMPLETE','mathematical_verdict':seal['mathematical_verdict'],'seal_sha256':sha(O/'SEAL.json'),'source_bindings':len(initial),'review_bindings':len(files)}))
