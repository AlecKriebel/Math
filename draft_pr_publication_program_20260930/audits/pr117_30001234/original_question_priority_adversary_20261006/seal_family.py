#!/usr/bin/env python3
"""Seal public-safe completed priority artifacts; excludes source bodies/renders."""
import datetime, hashlib, json, os, pathlib
D=pathlib.Path(__file__).resolve().parent
def ck(b,m):
    if not b: raise ValueError(m)
def pin(p):
    b=p.read_bytes(); return {'relative_path':str(p.relative_to(D)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
controls=json.loads((D/'CHECK_PROCESS_RECEIPT.json').read_text())
ck(controls['status']=='PASS' and controls['optimized_equivalence'] and controls['false_guard_controls']==2,'Completed actual controls')
ck(controls['private_guards']==180 and controls['portable_guards']==43 and controls['private_members_verified']==62,'Exact actual guard/source counts')
result={
 'schema':'pr117-original-question-priority-family-result/v1',
 'utc':now,'actual_sealer_pid':os.getpid(),'PR':117,'problem_id':30001234,
 'original_immutable_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8',
 'candidate_sha256':'1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf',
 'source_prior_review_hash':'6ff8253c57c5544f0b33ac8a6303be8ec7f42ac0f5ce6b4976a8149ae1b28152',
 'status':'EXACT_PRIOR_COUNTEREXAMPLE_CONFIRMED',
 'supported_classification':'already_solved',
 'math_valid':True,'novel_original_resolution':False,'preprint_promotion':False,
 'priority_is_unresolved_due_to_full_text_access':False,
 'decisive_prior':{'author':'Shunsuke Takagi','title':'Adjoint ideals and a correspondence between log canonicity and F-purity',
   'earliest_verified_disclosure_utc':'2011-04-30T10:42:16Z','earliest_version':'arXiv:1105.0072v1',
   'earliest_version_operative_pages':'Remark4.3pp18-19; Example4.4p19',
   'journal':'Algebra & Number Theory7(4)(2013),917-942','journal_doi':'10.2140/ant.2013.7.917',
   'journal_operative_pages':'Triangle-labelled augmented matrixp937; Remark4.3p939; Example4.4p940',
   'mechanism':'Explicit identical earlier counterexample; exact coordinate permutation establishes literal target equivalence',
   'source_to_candidate_order':[0,3,1,4,5,2],
   'earliest_version_pin':pin(D/'private_sources/takagi_1105.0072v1.pdf'),
   'published_body_pin':pin(D/'private_sources/takagi_adjoint2013.pdf')},
 'meaningful_new_core_theorem_present':False,
 'added_value':'Elementary full-face exposition, ideal-hypothesis checks and reproducible independent verification of the known counterexample',
 'required_corrections':['Credit the exact Takagi2011/2013 Example4.4','Correct the dated open-status assessment via an authorized native correction preserving immutable cache history','Do not describe the existing theorem as a novel open-problem resolution or create a preprint/DOI/tracker row for it'],
 'mandatory_math_corrections':[],
 'attempt_ledger_preserved':'1/5','new_central_proof_turns':0,
 'other_new_priority_reports_read':False,'outside_contact':False,
 'git_index_ref_native_service_global_mutations':False,
 'priority_family_completion_percent':100,'program_complete':False,
 'report_pin':pin(D/'REPORT.md'),'source_manifest_pin':pin(D/'SOURCE_MANIFEST.json'),
 'actual_control_receipt_pin':pin(D/'CHECK_PROCESS_RECEIPT.json'),
 'parent_disposition_still_required':True
}
(D/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
members=[]
for p in sorted(D.iterdir()):
    if not p.is_file() or p.name=='OUTPUT_MANIFEST.json': continue
    ck(p.name not in ['private_sources','private_renders'],'Private body exclusion')
    members.append(pin(p))
manifest={'schema':'pr117-original-question-public-output-manifest/v1','utc':now,'actual_sealer_pid':os.getpid(),'members':members,'public_safe':True,'excluded_private_directories':['private_sources/','private_renders/'],'new_central_proof_turns':0,'original_candidate_unchanged':True}
(D/'OUTPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'pid':os.getpid(),'status':result['status'],'public_members':len(members),'report_pin':pin(D/'REPORT.md'),'result_pin':pin(D/'RESULT.json'),'manifest_pin':pin(D/'OUTPUT_MANIFEST.json'),'checker_pin':pin(D/'priority_scope_checks.py')},sort_keys=True))
