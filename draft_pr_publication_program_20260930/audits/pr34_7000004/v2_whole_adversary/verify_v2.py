"""New complete v2 adversary: read-only frozen bindings, metadata and actual code controls."""
from pathlib import Path
import copy,datetime,hashlib,json,subprocess,sys
import sympy as S
H=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_publication_program_20260930/audits/pr34_7000004';C=P/'reviewed_candidate_v2'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
checks={};rejected={}
def ck(n,v):
 assert bool(v),n;checks[n]=True
def reject(n,f):
 try:f()
 except (AssertionError,ValueError,KeyError,TypeError):rejected[n]=True
 else:raise AssertionError('mutant accepted '+n)
def closure():
 ck('frozen_manifest_exact',sha((C/'MANIFEST.json').read_bytes())=='8afc9a17669c12559aea4287117069a20fbb39eea2af4ffe9bba81d7586a702a')
 m=load(C/'MANIFEST.json');d=load(C/'CURRENT_PROOF_DEPENDENCIES.json');records=[]
 ck('entire_candidate38_dependency235',len(m['files'])==38 and len(d['files'])==235)
 for base,entries in [(C,m['files']),(P,d['files'])]:
  for z in entries:
   p=base/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'],str(p)
   fmt='bytes read'
   if '.jsonl' in p.name:
    values=[json.loads(v) for v in b.splitlines()];fmt='all JSONL records parsed'
   elif '.json' in p.name:
    values=json.loads(b);fmt='complete JSON parsed'
   records.append({'path':str(p.relative_to(P)),'bytes':len(b),'sha256':sha(b),'read_method':fmt})
 return records
before=closure();(H/'READING_BINDING_LEDGER.json').write_text(json.dumps(before,indent=2)+'\n')
ck('branch_stays_main',subprocess.check_output(['git','branch','--show-current'],cwd=R).decode().strip()=='main')
original=load(P/'snapshot_manifest.json');head=original['head'];base=original['base']
ck('actual17path_git_diff',subprocess.check_output(['git','diff','--name-only',base,head],cwd=R).decode().splitlines()==original['changed_paths'])
ck('actual_base_mergebase',subprocess.check_output(['git','merge-base',base,head],cwd=R).decode().strip()==base)
for z in original['files']:
 b=subprocess.check_output(['git','show',head+':unsolved_math_prioritization/attempts/7000004/'+z['path']],cwd=R)
 ck('actual_original_blob_'+z['path'],b==(C/'original_archive'/z['path']).read_bytes() and len(b)==z['size'] and sha(b)==z['sha256'])
ck('actual_original16',len(original['files'])==16)
ck('actual_preserved_diff_patch',subprocess.check_output(['git','diff',base,head],cwd=R)==(P/'pr_input/diff.patch').read_bytes())
ready=load(C/'readiness.json');st=load(C/'current_status.json');ctx=load(C/'CURRENT_SOURCE_CONTEXT.json');old=load(C/'original_archive/readiness.json')
turnbytes=(C/'turns.jsonl').read_bytes();turns=[json.loads(v) for v in turnbytes.splitlines()]
ck('turn1_exact_prefix',turnbytes.startswith((C/'original_archive/turns.jsonl').read_bytes()))
ck('v1_v2_turns_byte_identical',turnbytes==(P/'reviewed_candidate/turns.jsonl').read_bytes())
ck('turn1and2_only',len(turns)==2 and [z['turn'] for z in turns]==[1,2])
p=load(C/'source_record.json');prior=load(C/'prior_report.json');verdict=load(C/'original_archive/review/verdict.json')
ck('sourcepair_actual_serialization',ready['review_hash']==sha(json.dumps([p,prior],sort_keys=True).encode()))
ck('statement_exact_hash',ready['statement_hash']==sha(p['statement'].encode()))
ck('separate_reviewdoc_role',verdict['review_sha256']==sha((C/'original_archive/review/REVIEW.md').read_bytes())!=ready['review_hash'])
ck('current_artifact_binding',ready['reviewed_artifact_sha256']==sha((C/'RESULT.md').read_bytes()))
ck('old_review_artifact_binding',old['reviewed_artifact_sha256']==verdict['final_artifact_sha256']==sha((C/'original_archive/OBSTRUCTION.md').read_bytes()))
def metadata(rr,ss=st,cc=ctx):
 b=rr['budget'];hh=rr['historical_original_attempt_metadata']
 assert b['maximum_substantive_attempts']==5 and b['used_substantive_attempts']==2
 assert b['original_substantive_attempts']==b['new_substantive_attempts']==1 and b['verification_attempts']==0
 assert b['time_cap_utc'] is None and 'no replacement deadline' in b['time_scope']
 assert b['model']==turns[1]['model'] and b['reasoning_effort']==turns[1]['reasoning_effort']
 assert b['compute']!=old['budget']['compute'] and 'nine outer' in b['compute']
 assert hh['budget']==old['budget'] and hh['literature_checked_at']==old['literature_checked_at']
 assert hh['readiness_sha256']==sha((C/'original_archive/readiness.json').read_bytes())
 assert rr['literature_checked_at']==cc['current_source_check_checkpoint_utc']
 assert datetime.datetime.fromisoformat(rr['literature_checked_at'])>datetime.datetime.fromisoformat(turns[1]['timestamp'])
 assert 'not an assertion of exhaustive worldwide' in rr['literature_check_scope']
 assert 'fresh retrieval of every' in rr['literature_check_scope']
 assert rr['literature_check_scope']==cc['current_source_check_scope']
 assert rr['queue_outcome_requested']==ss['queue_status_proposed']=='already_solved'
 assert rr['positive_novelty_claim'] is False and rr['paper_or_new_doi_or_tracker'] is False
 assert ss['cumulative_attempts']=='2/5' and ss['verification_attempts']==0
 assert ss['previous_whole_verdict']=='FIX_REQUIRED_ADMINISTRATIVE_PROVENANCE'
 assert ss['current_revision']=='reviewed_candidate_v2'
 assert ss['narrower_negative_curvature_target_resolved'] is False and ss['earliest_historical_recognition_established'] is False
 assert ss['current_gate']=='pending_DIFFERENT_NEW_complete_v2_adversary'
metadata(ready);ck('historical_metadata_repair_complete',True)
changes={
 'expired_deadline_current':lambda q:q['budget'].update(time_cap_utc=old['budget']['time_cap_utc']),
 'old_model_current':lambda q:q['budget'].update(model=old['budget']['model']),
 'old_effort_current':lambda q:q['budget'].update(reasoning_effort=old['budget']['reasoning_effort']),
 'old_compute_current':lambda q:q['budget'].update(compute=old['budget']['compute']),
 'old_literature_current':lambda q:q.update(literature_checked_at=old['literature_checked_at']),
 'deleted_history':lambda q:q.pop('historical_original_attempt_metadata'),
 'changed_history_budget':lambda q:q['historical_original_attempt_metadata']['budget'].update(used_substantive_attempts=2),
 'changed_history_date':lambda q:q['historical_original_attempt_metadata'].update(literature_checked_at=rrdate),
 'attempt_reset':lambda q:q['budget'].update(used_substantive_attempts=1),
 'audit_charged_or_extra_route':lambda q:q['budget'].update(verification_attempts=1),
 'novelty_promotion':lambda q:q.update(positive_novelty_claim=True),
 'new_paper_or_DOI':lambda q:q.update(paper_or_new_doi_or_tracker=True),
 'unqualified_exhaustive_search':lambda q:q.update(literature_check_scope='All bibliography freshly retrieved; exhaustive novelty certified.'),
}
rrdate=ready['literature_checked_at']
for n,f in changes.items():q=copy.deepcopy(ready);f(q);reject(n,lambda q=q:metadata(q))
for n,f in [('narrower_target_promotion',lambda q:q.update(narrower_negative_curvature_target_resolved=True)),('earliest_priority_promotion',lambda q:q.update(earliest_historical_recognition_established=True)),('transferred_clean_gate',lambda q:q.update(current_gate='PASS'))]:
 q=copy.deepcopy(st);f(q);reject(n,lambda q=q:metadata(ready,q))
patch=load(C/'CURRENT_QUEUE_PATCH.json');queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes()
def qcheck(pa,b=queue):
 assert sha(b)==pa['whole_queue_preimage_sha256']
 ls=b.decode().splitlines(keepends=True);rows=[z for z in ls if len(z.split('|'))==14 and z.split('|')[2].strip().split(' / ')[0]=='7000004'];assert len(rows)==1
 assert rows[0]==pa['row_before'];header=next(z for z in ls if z.startswith('| Rank |'));names=[z.strip() for z in header.split('|')[1:-1]];assert len(names)==12 and names==pa['header_names']
 oldfields=dict(zip(names,rows[0].split('|')[1:-1]));newfields=dict(zip(names,pa['row_prospective'].split('|')[1:-1]));assert len(pa['row_prospective'].split('|'))==14
 assert newfields['Status'].strip()=='already_solved' and newfields['Turns'].strip()=='2/5'
 assert newfields['Chat']==oldfields['Chat'] and newfields['DOI']==oldfields['DOI']
 assert 'verified elementary consequence' in newfields['Findings'] and 'no paper/newDOI/tracker' in newfields['Findings']
 assert set(k for k in names if oldfields[k]!=newfields[k])=={'Status','Turns','Findings'}
 new=b.replace(pa['row_before'].encode(),pa['row_prospective'].encode());assert sha(new)==pa['whole_queue_prospective_sha256']
 assert new.replace(pa['row_prospective'].encode(),pa['row_before'].encode())==b
qcheck(patch);ck('actual_whole12column_queue_patch',True)
for n,i in [('findings_in_Chat',10),('findings_in_DOI',12)]:
 q=copy.deepcopy(patch);cols=q['row_prospective'].split('|');cols[i],cols[11]=cols[11],cols[i];q['row_prospective']='|'.join(cols);reject(n,lambda q=q:qcheck(q))
q=copy.deepcopy(patch);q['row_prospective']=q['row_prospective'].replace('2/5','1/5');reject('queue_budget_reset',lambda:qcheck(q))
# New direct trig reconstruction, identities hold symbolically for real t and all positive a.
t=S.symbols('t',real=True);a=S.symbols('a',positive=True);x=S.cos(t);y=S.sin(t)
g=S.Matrix([x,y,S.cos(2*t)/4]);w=S.Matrix([-x**3,y**3,1]);gp=g.diff(t);gpp=gp.diff(t)
def zero(z):return all(S.trigsimp(q)==0 for q in z) if isinstance(z,S.MatrixBase) else S.trigsimp(z)==0
ck('fresh_trig_actual_cross',zero(gp.cross(gpp)-w));ck('fresh_trig_speed',zero(gp.dot(gp)-1-x*x*y*y))
ck('fresh_trig_torsion',zero(w.dot(g.diff(t,3))-3*x*y))
ck('actual_stationary_locus_factor',w.diff(t)==S.Matrix([3*x*x*y,3*y*y*x,0]))
for v in [0,S.pi/2,S.pi,3*S.pi/2]:ck('fresh_stationary_'+str(v),w.diff(t).subs(t,v)==S.zeros(3,1))
r,e=S.symbols('r e',positive=True);q=g+e*w/r
ck('fresh_height_all_parameter_identity',zero(q[2]-(q[0]**2-q[1]**2)/4-(e/r+e*(x**4+y**4)/(2*r)-e*e*(x**6-y**6)/(4*r*r))))
priorg=S.Matrix([a*x,a*y,a**4*(x**4-y**4)])
ck('fresh_prior_all_positive_a_cross',zero(priorg.diff(t).cross(priorg.diff(t,2))-a*a*S.Matrix([-4*a**3*x**3,4*a**3*y**3,1])))
ck('fresh_prior_exact_positive_scale',zero((priorg/a).subs(a,4**(-S.Rational(1,3)))-g))
# Actual unmodified current executable, outputs preserved and compared byte-exact.
def run(name,source):
 dest=H/'actual_executions'/name;dest.mkdir(parents=True,exist_ok=True);code=dest/'verify.py';code.write_bytes(source)
 proc=subprocess.run([sys.executable,str(code)],capture_output=True)
 (dest/'stdout.txt').write_bytes(proc.stdout);(dest/'stderr.txt').write_bytes(proc.stderr)
 receipt={'name':name,'implementation_sha256':sha(source),'returncode':proc.returncode,'stdout_sha256':sha(proc.stdout),'stderr_sha256':sha(proc.stderr)}
 (dest/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');return proc,receipt
code=(C/'verify.py').read_bytes();r,rc=run('current_v2_exact',code)
ck('actual_current_v2_226controls_byteexact',r.returncode==0 and not r.stderr and r.stdout==(C/'exact_results.json').read_bytes())
src=code.decode();mutants={
 'wrong_amplitude':('gamma=S.Matrix([x,y,(x*x-y*y)/4])','gamma=S.Matrix([x,y,(x*x-y*y)/2])'),
 'wrong_binormal_y':('C=S.Matrix([-x**3,y**3,1]);','C=S.Matrix([-x**3,-y**3,1]);'),
 'wrong_nonzero_curvature_claim':('C=S.Matrix([-x**3,y**3,1]);','C=S.Matrix([-x**3,y**3,0]);'),
 'wrong_shear':('Z-(X*X-Y*Y)/4','Z+(X*X-Y*Y)/4'),
 'nonunit_push_off':('P=gamma+e*C/r','P=gamma+e*C'),
 'wrong_torsion_sign_formula':('S.simplify(kg-k/abs(tors))==0','S.simplify(kg-k/tors)==0'),
}
actual=[]
for name,(oldtext,newtext) in mutants.items():
 assert src.count(oldtext)==1;proc,rec=run(name,src.replace(oldtext,newtext).encode())
 ck('actual_math_corruption_rejected_'+name,proc.returncode!=0 and b'AssertionError:' in proc.stderr)
 rec['assertion']=proc.stderr.decode().split('AssertionError:',1)[1].strip();actual.append(rec)
ck('all_before_after_bindings_equal',closure()==before)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_checks':len(checks),'validator_mutants_rejected':len(rejected),'actual_mathematical_code_mutants_rejected':len(actual),'checks':checks,'rejected_validator_mutants':rejected,'actual_code_mutants':actual,'current_exact_execution':rc,'frozen_bindings_verified_before_after':len(before),'original_attempts_added':0,'scope':'Frozen currentv2 only, independent universal proof essential; exact algebra and validator mutant counts supplement it.'}
(H/'V2_VERIFICATION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['independent_checks','validator_mutants_rejected','actual_mathematical_code_mutants_rejected','frozen_bindings_verified_before_after']}))
