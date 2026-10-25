#!/usr/bin/env python3
"""Finalize only the independent analytic review and its custody record."""
from pathlib import Path
import datetime,hashlib,json,zipfile
O=Path(__file__).resolve().parent
P=O.parents[1]
S=P/'sources'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return {'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,value):
 with p.open('x') as f:f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert sha(S/'common_basin_boundaries.pdf')=='5c44dd3cc2cbdea38eb0da0c03bd42dd409ae78334ce47f3956f827caa0032cb'
assert sha(S/'basin-boundaries-verification.zip')=='1251fcb97b28cc15e72a65195757dd20029f5695f06e3d4de97d64077bd21005'
assert sha(S/'published-source/basin-boundaries-verification/paper/common_basin_boundaries.tex')=='665ef241d04e22680416afcdbc734e7a1f74bd55fb8d8ea0ea65995c3792c982'
assert sha(O/'independent-initial-seal.json')=='702d6f420d16b1b07ee77488f12aa5108052b12f38de796dd16b31cb99ea6900'
before=load(O/'source-baseline.json')['files'];custody=[]
for row in before:
 current=bind(P/row['path']);assert current==row,row['path'];custody.append({'before':row,'after':current,'unchanged':True})
with zipfile.ZipFile(S/'basin-boundaries-verification.zip') as archive:
 members=[]
 for item in archive.infolist():
  if item.is_dir():continue
  target=S/'published-source'/item.filename
  assert target.read_bytes()==archive.read(item),item.filename
  members.append({'member':item.filename,'bytes':item.file_size,'sha256':sha(target)})

full_text_names={
 'candidate/FINAL_RESULT.md','candidate/TURN_1.md','candidate/TURN_3.md',
 'candidate/SOURCE_SCOPE.md','candidate/SOURCE_ADDITION_T3.md',
 'controls/algebra/SYMBOLIC_IDENTITIES.json','controls/algebra/UNIFORM_CERTIFICATE.json'
}
full_static={
 'candidate/check_turn_1.py','candidate/check_turn_2.py','candidate/check_turn_3.py',
 'candidate/review/check_independent.py','candidate/verify_packet.py',
 'controls/algebra/check_symbolic_equations.py','controls/algebra/check_uniform_algebra.py',
 'controls/backward/check_backward_feedback.py','controls/backward/verify_controls.py',
 'controls/topology/check_topology.py','verify_supplement.py','audits/priority/check_priority_claims.py'
}
source_reads=[]
prefix='sources/published-source/basin-boundaries-verification/'
for row in before:
 name=row['path'];local=name[len(prefix):] if name.startswith(prefix) else None
 if name=='sources/common_basin_boundaries.pdf':extent='Complete actual six-page PDF, every page text and every rendered page read.'
 elif name=='sources/common_basin_boundaries.full-text.txt':extent='Complete six-page extraction read and cross-read with actual PDF images and complete TeX.'
 elif local=='paper/common_basin_boundaries.tex':extent='Complete actual TeX read before initial independent seal.'
 elif local in full_text_names:extent='Complete body read after independent initial seal; historical author/support conclusions treated as submitted evidence only.'
 elif local in full_static:extent='Complete static program read after independent initial seal; no execution, import, compile or replay.'
 elif local and local.endswith('.json'):extent='Complete JSON parsed and structure inventoried; not every historical opinion value substantively read or adopted.'
 elif local and (local.endswith('SOURCE_FIRST.md') or local.endswith('SOURCE_FIRST_BASELINE.md')):extent='Only targeted source-hypothesis search hits read after initial seal; complete historical opinion body not read or adopted.'
 else:extent='Inventoried and byte-authenticated; no substantive full reading claimed.'
 source_reads.append({**row,'read_extent':extent})

primary=[]
specs={
 'bkz-v1':{'read_physical_pages':list(range(3,9))+list(range(10,15))+list(range(23,32))+[34,35],
  'visually_read_pages':[8,27,30],
  'edition':'arXiv0812.4040v1; submitted21December2008; 36 physical pages',
  'interfaces':'Exact map/space; generic assumptions I and II; Theorem2 and asserted tanhExample1; finite-dimensional inverse mechanism; invariant mixture family; entire Proposition3 global proof and Proposition4 core-boundary proof, including Lemmas12–13; A.2 numerical S-shape verification. Deep earlier order/IFS lemmas outside these pages remain source dependencies.',
  'proof_status':'Theorem2conditional onI/II; all-parameter II verification in inspected body is numerical, not a rigorous continuous certificate.'},
 'bkz-author':{'read_physical_pages':[1,4,6,7,8,13,14,23,27,30,34,35],
  'visually_read_pages':[],
  'edition':'Author-hosted manuscript dated19December2008, 36 physical pages; not authenticated as final CMP proof',
  'interfaces':'Corresponding model, assumptions, theorem/example, invariant family, proposition statements/core-seed proof and complete relevant A.2 numerical verification.',
  'proof_status':'Same source-interface gap; no journal-edition proof equivalence inferred from author hosting.'},
 'owr-ems':{'read_physical_pages':[15,16,17],
  'visually_read_pages':[16,17],
  'edition':'Published EMS OWR49/2009 body, printed2713–2715 for complete Keller contribution; wholevolume32physicalpages',
  'interfaces':'Complete contribution; exact full-D A≤0.4 and6<B≤16 unconditional Theorem2, open basins/global convergence and exact boundary conjecture.',
  'proof_status':'Actual unconditional published statement/announcement of BKZ result; no independent proof of parameter condition. Statement and proof coverage kept separate.'}
}
for row in load(O/'primary-acquisition.json')['sources']:
 assert not row.get('error')
 assert sha(O/row['raw_path'])==row['sha256']
 assert sha(O/row['text_path'])==row['text_sha256']
 primary.append({**row,**specs[row['name']]})
journal=[]
for row in load(O/'journal-acquisition.json')['sources']:
 if row.get('raw_path'):assert sha(O/row['raw_path'])==row['sha256']
 journal.append({**row,'read_extent':'Publisher metadata, abstract and subscription-access notice inspected; no full article proof obtained. Ordinary PDF route redirects to preview, not a PDF.','final_journal_proof_read':False})
save(O/'read-ledger.json',{
 'record_id':'23129302','utc':now,'source_files':source_reads,
 'primary_bodies':primary,'journal_access_attempts':journal,
 'all_support_JSON_structures':'support-json-inventory.json',
 'initial_independence_seal_sha256':sha(O/'independent-initial-seal.json'),
 'current_sibling_or_root_reports_read':False,
 'source_programs_executed':False,
 'owned_independent_controls':['check_exact.py','check_probability.py'],
 'boundary_of_reading':'Whole downloaded primary PDFs do not imply whole-body reading; exact pages above are the actual extent. No global priority/current-status certification.'
})
save(O/'custody-before-after.json',{
 'record_id':'23129302','utc':now,'all_initial_source_files_unchanged':True,
 'files':custody,'all_regular_archive_member_bytes_match_extracted':True,
 'archive_regular_members':members,'own_write_directory':'reviews/analytic/',
 'initial_independence_seal_unchanged':True,
 'source_or_other_review_mutations':False
})
exact=load(O/'exact-results.json');prob=load(O/'probability-results.json')
assert len(exact['checks'])==32 and all(x['verified'] for x in exact['checks'])
for script in ['check_exact','check_probability']:
 result=load(O/(script+'-run.json'));assert result['returncode']==0 and not result['timed_out']
save(O/'verdict.json',{
 'record_id':'23129302','utc':now,'task_status':'COMPLETE',
 'completion_estimate_percent_of_assigned_analytic_review':100,
 'mathematical_verdict':'CONDITIONAL_ANALYTIC_CORE_VERIFIED_SOURCE_PREREQUISITE_OPEN',
 'full_original_theorem_independently_cleared':False,
 'new_analytic_construction_verified':True,
 'original_claim_weakened_or_replaced':False,
 'original_target':'W=closure_D union_{n>=0}F^{-n}({1})=boundary_D B+=boundary_D B- on all probability densities;0<A<=2/5,6<B<=16.',
 'strongest_unconditional_result_verified':'F continuous open onto; uniform probability-space inverse contraction21/25; every u inW is an L1 limit of densities vn withF^n vn=1, including arbitrary integrable/unbounded/vanishing densities.',
 'strongest_conditional_result_verified':'The entire original closure/common-boundary theorem follows if the imported full-range global trichotomy, basin openness and boundaryseed are rigorously established.',
 'central_new_proof_defect_found':False,
 'load_bearing_open_gap':{
  'id':'BKZ_ASSUMPTION_II_PARAMETER_CERTIFICATE',
  'location':'BKZTheorem2 pp7–8 conditionalI/II; AppendixA.2 pp34–35 numerical verification; currentpaper§1 importedfacts and§5completion.',
  'detail':'Accessible BKZv1/author proof supplies no rigorous all-parameter verification of H(r)=G(phi(u_r)) S-shape or sufficient weaker dichotomy; current exact certificates concern inverse contraction andI. OWR prints exact unconditional theorem but gives no independent proof of this parameter verification. Final journal proof not obtained or compared.',
  'counterexample_claimed':False,
  'absence_of_any_rigorous_proof_claimed':False,
  'needed_evidence':'Inspected rigorous final-source proof or exact continuous certificate ofII/sufficient weaker classification, covering the entire rectangle; finite checked parameter values do not suffice.',
  'repair_attempted':False
 },
 'published_unconditional_OWR_theorem_statement_read':True,
 'unconditional_OWR_statement_treated_as_independent_proof':False,
 'final_CMP_journal_proof_read':False,
 'source_programs_executed':False,
 'independent_exact_controls':32,
 'independent_numerical_probability_cases':prob['numerical_probability_cases'],
 'finite_controls_claimed_to_prove_universal_statement':False,
 'external_priority_status':'UNKNOWN; no independent broad novelty adjudication assigned',
 'publication_clearance':False,'page_promotion_permission':False,
 'public_page_rendered':False,'live_action':False,'browser_UI_used':False,
 'native_Sheet_mutated':False,'native_AA':None,
 'follow_up':None,'external_contact_or_outreach':False,
 'other_current_review_lanes_read':False,
 'prior_Langlands_scope_package_modified':False
})
save(O/'validation.json',{
 'record_id':'23129302','utc':now,
 'all_initial_source_bindings_unchanged':True,'initial_source_files_rehashed':len(custody),
 'regular_archive_member_bytes_verified':len(members),
 'initial_independence_seal_unchanged':True,
 'primary_raw_and_extract_hashes_match_receipts':True,
 'owned_control_runs_complete_under_timeout':True,
 'full_original_mathematical_clearance':False,
 'source_helpers_executed':False,
 'note':'This validation authenticates custody and recorded control completion; it does not close the source Assumption-II gap.'
})
with (O/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n'+now+' — Final classification: new analytic construction verified, full original theorem not independently cleared because BKZAssumptionII/all-parameter source proof coverage is open. OWR exact unconditional statement is distinguished from its proof coverage; ordinary journal route remains subscription preview. No extended repair. All initial source files and extracted member bytes rehashed unchanged. Completion: **100% of this assigned analytic review task**; no publication or overall programme clearance.\n')
excluded={'SEAL.json','SEAL.sha256','SHA256SUMS'}
files=sorted(f for f in O.rglob('*') if f.is_file() and f.name not in excluded)
seal={'record_id':'23129302','utc':now,'seal_kind':'INDEPENDENT_ANALYTIC_REVIEW_HANDOFF',
 'verdict':'CONDITIONAL_ANALYTIC_CORE_VERIFIED_SOURCE_PREREQUISITE_OPEN',
 'full_original_mathematical_clearance':False,'publication_clearance':False,
 'source_authorities':[bind(P/row['path']) for row in before],
 'review_files':[bind(f) for f in files],
 'initial_independence_seal_sha256':sha(O/'independent-initial-seal.json'),
 'excludes_self_and_sha_manifests':True}
save(O/'SEAL.json',seal)
(O/'SEAL.sha256').write_text(sha(O/'SEAL.json')+'  SEAL.json\n')
with (O/'SHA256SUMS').open('x') as f:
 for row in seal['source_authorities']+seal['review_files']:f.write(row['sha256']+'  '+row['path']+'\n')
 f.write(sha(O/'SEAL.json')+'  reviews/analytic/SEAL.json\n')
print(json.dumps({'record_id':'23129302','task_status':'COMPLETE','verdict':seal['verdict'],'seal_sha256':sha(O/'SEAL.json'),'source_bindings':len(before),'review_files':len(files)}))
