"""Independent symbolic identities, actual-code falsifiers, and complete packet guards."""
from pathlib import Path
import hashlib,json,copy,subprocess,datetime
import sympy as s
H=Path(__file__).resolve().parent;P=H.parent;R=Path('/Users/alec/Documents/Math');C=P/'reviewed_candidate'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
checks={};rejects={}
def ck(n,b):
 assert bool(b),n;checks[n]=True
def reject(n,f):
 try:f()
 except (AssertionError,ValueError,KeyError):rejects[n]=True
 else:raise AssertionError('mutant accepted: '+n)
x,y,e,r,a=s.symbols('x y e r a',real=True)
ideal=s.groebner([x*x+y*y-1],x,y,domain='EX')
def z(q):
 if isinstance(q,s.MatrixBase):return all(z(v) for v in q)
 return ideal.reduce(s.expand(q))[1]==0
def D(q):
 if isinstance(q,s.MatrixBase):return q.applyfunc(D)
 return -y*s.diff(q,x)+x*s.diff(q,y)
g=s.Matrix([x,y,(x*x-y*y)/4]);w=D(g).cross(D(D(g)));W=s.Matrix([-x**3,y**3,1]);R2=1+x**6+y**6
ck('actual_cross_all_circle',z(w-W));ck('first_orthogonality',z(W.dot(D(g))));ck('second_orthogonality',z(W.dot(D(D(g)))))
ck('positive_speed_identity',z(D(g).dot(D(g))-(1+x*x*y*y)));ck('positive_curvature_cross_z',z(w[2]-1))
ck('normalization_identity',W.dot(W)==R2);ck('R2_lower_bound_identity',z(R2-(s.Rational(5,4)+3*(x*x-y*y)**2/4)))
ck('normalized_direction_ratio_x',s.cancel(-W[0]/W[2])==x**3);ck('normalized_direction_ratio_y',s.cancel(W[1]/W[2])==y**3)
u,v=s.symbols('u v',real=True)
ck('real_cube_difference',s.expand(u**3-v**3-(u-v)*(u*u+u*v+v*v))==0)
ck('real_cube_factor_squares',s.expand(u*u+u*v+v*v-((u+v/2)**2+3*v*v/4))==0)
ck('Wprime_all_circle',z(D(W)-s.Matrix([3*x*x*y,3*y*y*x,0])))
ck('torsion_numerator_all_circle',z(W.dot(D(D(D(g))))-3*x*y))
for name,point in [('0',(1,0)),('pi2',(0,1)),('pi',(-1,0)),('3pi2',(0,-1))]:
 ck('stationary_exact_'+name,D(W).subs({x:point[0],y:point[1]})==s.zeros(3,1));ck('positive_curvature_at_'+name,R2.subs({x:point[0],y:point[1]})>0)
# Polynomial critical system: Wprime=0 and x²+y²=1 forces xy=0.
critical=s.groebner([x*x+y*y-1,3*x*x*y,3*y*y*x],x,y)
ck('all_critical_points_cardinal',critical.reduce(x*y)[1]==0)
q=g+e*W/r
h=q[2]-(q[0]**2-q[1]**2)/4
ck('whole_shear_height_identity',s.expand(h-(e/r+e*(x**4+y**4)/(2*r)-e*e*(x**6-y**6)/(4*r*r)))==0)
ck('fourth_power_min_half_identity',z(x**4+y**4-(s.Rational(1,2)+(x*x-y*y)**2/2)))
ck('uniform_height_margin_at_upper_endpoint',1-s.Rational(1,3)/4==s.Rational(11,12)>0)
ck('exact_disk_derivative_matrix',W.jacobian([x,y])==s.Matrix([[-3*x*x,0],[0,3*y*y],[0,0]]))
ck('embedding_lipschitz_strict_interval',1-3*e==3*(s.Rational(1,3)-e))
prior=s.Matrix([a*x,a*y,a**4*(x**4-y**4)])
ck('prior_cross_exact_all_a',z(D(prior).cross(D(D(prior)))-a*a*s.Matrix([-4*a**3*x**3,4*a**3*y**3,1])))
ck('prior_scale_z_exact',z(prior/a-s.Matrix([x,y,a**3*(x*x-y*y)])))
ck('exact_prior_positive_root',s.Pow(4,-s.Rational(1,3))>0 and s.Pow(4,-s.Rational(1,3))**3==s.Rational(1,4))
ck('offset_scale_exact',s.cancel(e/a-e*(1/a))==0)
ck('surface_K_numerator',s.hessian(x**4-y**4,(x,y)).det()==-144*x*x*y*y)
# Independently check source, metadata and exact named queue patch.
ready=load(C/'readiness.json');status=load(C/'current_status.json');patch=load(C/'CURRENT_QUEUE_PATCH.json')
p=load(C/'source_record.json');report=load(C/'prior_report.json');oldverdict=load(C/'original_archive/review/verdict.json')
def bind(rr,pp=p,prior=report):
 assert rr['review_hash']==sha(json.dumps([pp,prior],sort_keys=True).encode())
 assert rr['statement_hash']==sha(pp['statement'].encode())
 assert rr['reviewed_artifact_sha256']==sha((C/'RESULT.md').read_bytes())
bind(ready);ck('current_sourcepair_and_artifact_roles',True)
ck('old_reviewdoc_distinct_role',sha((C/'original_archive/review/REVIEW.md').read_bytes())==oldverdict['review_sha256']!=ready['review_hash'])
turnbytes=(C/'turns.jsonl').read_bytes();oldturn=(C/'original_archive/turns.jsonl').read_bytes();turns=[json.loads(z) for z in turnbytes.splitlines()]
ck('original_turn_byte_prefix',turnbytes.startswith(oldturn));ck('cumulative_two_turns',len(turns)==2 and [z['turn'] for z in turns]==[1,2])
def outcome(rr,st):
 assert rr['queue_outcome_requested']==st['queue_status_proposed']=='already_solved'
 assert rr['budget']['maximum_substantive_attempts']==5 and rr['budget']['used_substantive_attempts']==2
 assert rr['budget']['original_substantive_attempts']==rr['budget']['new_substantive_attempts']==1
 assert rr['budget']['verification_attempts']==0
 assert st['cumulative_attempts']=='2/5' and st['new_substantive_attempts']==1
 assert rr['positive_novelty_claim'] is False and rr['paper_or_new_doi_or_tracker'] is False
 assert st['narrower_negative_curvature_target_resolved'] is False and st['earliest_historical_recognition_established'] is False
outcome(ready,status);ck('whole_disposition_and_budget',True)
head=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
base=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes()
def queuecheck(q,pa):
 assert sha(q)==pa['whole_queue_preimage_sha256']
 lines=q.decode().splitlines(keepends=True)
 h=next(z for z in lines if z.startswith('| Rank |'));assert [z.strip() for z in h.split('|')[1:-1]]==head
 matches=[z for z in lines if len(z.split('|'))==14 and z.split('|')[2].strip().split(' / ')[0]=='7000004'];assert len(matches)==1
 before=matches[0];assert before==pa['row_before']
 after=pa['row_prospective'];bc=before.split('|');ac=after.split('|');assert len(ac)==14
 assert ac[8].strip()=='already_solved' and ac[9].strip()=='2/5' and not ac[10].strip() and not ac[12].strip()
 assert 'Ni-Zhang-Zhang2026' in ac[11] and 'verified elementary consequence' in ac[11]
 assert all(bc[i]==ac[i] for i in range(14) if i not in [8,9,11])
 new=q.replace(before.encode(),after.encode());assert sha(new)==pa['whole_queue_prospective_sha256']
 assert new.replace(after.encode(),before.encode())==q
 return new
prospective=queuecheck(base,patch);ck('whole_actual12column_patch',True)
# Rejection paths use independent complete validators; no corrected current writes.
for n,field,new in [('sourcepair_replaced_by_reviewdoc','review_hash',oldverdict['review_sha256']),('statement_hash_replaced','statement_hash','0'*64),('wrong_current_artifact','reviewed_artifact_sha256',sha((C/'original_archive/OBSTRUCTION.md').read_bytes()))]:
 bad=copy.deepcopy(ready);bad[field]=new;reject(n,lambda bad=bad:bind(bad))
for n,change in [('status_downgrade',lambda q:q.update(queue_outcome_requested='unsolved')),('novelty_promotion',lambda q:q.update(positive_novelty_claim=True)),('paper_upload_for_prior',lambda q:q.update(paper_or_new_doi_or_tracker=True)),('attempt_reset',lambda q:q['budget'].update(used_substantive_attempts=1))]:
 bad=copy.deepcopy(ready);change(bad);reject(n,lambda bad=bad:outcome(bad,status))
badstatus=copy.deepcopy(status);badstatus['narrower_negative_curvature_target_resolved']=True;reject('narrower_target_promotion',lambda:outcome(ready,badstatus))
for name,i,j in [('findings_into_chat',10,11),('findings_into_doi',12,11)]:
 pa=copy.deepcopy(patch);pieces=pa['row_prospective'].split('|');pieces[i],pieces[j]=pieces[j],pieces[i];pa['row_prospective']='|'.join(pieces);reject(name,lambda pa=pa:queuecheck(base,pa))
badq=base+patch['row_before'].encode();pa=copy.deepcopy(patch);pa['whole_queue_preimage_sha256']=sha(badq);reject('duplicate_live_queue_target',lambda:queuecheck(badq,pa))
pa=copy.deepcopy(patch);pa['row_prospective']=pa['row_prospective'].replace('2/5','1/5');reject('wrong_prospective_budget',lambda:queuecheck(base,pa))
# The one real current failure: current-looking budget/date fields need explicit archival roles.
t2=datetime.datetime.fromisoformat(turns[1]['timestamp'].replace('Z','+00:00'));cap=datetime.datetime.fromisoformat(ready['budget']['time_cap_utc'].replace('Z','+00:00'))
metadata_failure={'mandatory':True,'field':'readiness.json budget.time_cap_utc/model/reasoning_effort/compute and literature_checked_at','current_turn2_timestamp':turns[1]['timestamp'],'inherited_deadline':ready['budget']['time_cap_utc'],'deadline_precedes_current_turn':cap<t2,'inherited_model':ready['budget']['model'],'current_turn_model':turns[1]['model'],'literature_checked_at':ready['literature_checked_at'],'source_new_checked_at':load(P/'ROOT_NI2026_RETRIEVAL.json')['utc'],'repair':'Explicitly archive the original attempt budget/deadline/model/compute and original literature timestamp; provide current campaign scope and actual new checking timestamp, without inventing an exposed model or replacing original bytes.'}
ck('actual_metadata_defect_exposed',metadata_failure['deadline_precedes_current_turn'] and ready['budget']['model']!=turns[1]['model'])
# Actually execute mutated current source. Preserve implementation and actual stderr.
source=(C/'verify.py').read_text();mutants={'B_y_wrong':('C=S.Matrix([-x**3,y**3,1]);','C=S.Matrix([-x**3,-y**3,1]);'),'wrong_Gamma_amplitude':('gamma=S.Matrix([x,y,(x*x-y*y)/4])','gamma=S.Matrix([x,y,(x*x-y*y)/2])'),'omit_normalization':('P=gamma+e*C/r','P=gamma+e*C'),'wrong_shear_orientation':('Z-(X*X-Y*Y)/4','Z+(X*X-Y*Y)/4'),'wrong_prior_regular_B_assumption':("check('Bprime_nonzero_away_from_cusps',M.dot(M).subs({x:S.sqrt(2)/2,y:S.sqrt(2)/2})!=0)","check('Bprime_nonzero_away_from_cusps',M.dot(M).subs({x:1,y:0})!=0)")}
actual=[]
for name,(old,new) in mutants.items():
 assert source.count(old)==1,name
 d=H/'actual_mutations'/name;d.mkdir(parents=True,exist_ok=True);code=d/'verify.py';code.write_text(source.replace(old,new))
 run=subprocess.run(['/usr/bin/python3',str(code)],capture_output=True);(d/'stdout.txt').write_bytes(run.stdout);(d/'stderr.txt').write_bytes(run.stderr)
 ck('actual_current_mutant_rejected_'+name,run.returncode!=0 and b'AssertionError:' in run.stderr)
 actual.append({'name':name,'implementation_sha256':sha(code.read_bytes()),'exit':run.returncode,'stderr_sha256':sha(run.stderr),'assertion':run.stderr.decode().split('AssertionError:',1)[1].strip()})
out={'checks_passed':len(checks),'independent_validator_mutants_rejected':len(rejects),'actual_current_code_mutants_rejected':len(actual),'checks':checks,'mutants':rejects,'actual_mutations':actual,'mandatory_administrative_failure':metadata_failure,'mathematical_failure_found':False,'scope':'All-circle polynomial identities and universal proofs; finite controls supplement them. No current packet edit. Base administrative failure remains a failure requiring new complete review.'}
(H/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['checks_passed','independent_validator_mutants_rejected','actual_current_code_mutants_rejected','mathematical_failure_found']}))
