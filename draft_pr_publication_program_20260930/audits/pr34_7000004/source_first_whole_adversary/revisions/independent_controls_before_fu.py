"""Own all-parameter algebra, full corpus/SQLite/Git checks, executable falsifiers."""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,re,shutil,sqlite3,subprocess,unicodedata
import sympy as s
from packet_guard import guard
H=Path(__file__).resolve().parent;R=H.parents[3];P=H.parent;C=P/'reviewed_candidate_v2'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes());checks={}
def ck(n,b):assert bool(b),n;checks[n]=True
t,e=s.symbols('t e',real=True);g=s.Matrix([s.cos(t),s.sin(t),s.cos(2*t)/4]);w=g.diff(t).cross(g.diff(t,2))
W=s.Matrix([-s.cos(t)**3,s.sin(t)**3,1]);zero=lambda q:all(s.trigsimp(s.expand_trig(a))==0 for a in q)
ck('trigonometric_cross_independent',zero(w-W));ck('binormal_velocity',s.trigsimp(W.dot(g.diff(t)))==0);ck('binormal_acceleration',s.trigsimp(W.dot(g.diff(t,2)))==0)
ck('all_t_speed',s.trigsimp(g.diff(t).dot(g.diff(t))-1-s.sin(t)**2*s.cos(t)**2)==0)
ck('all_t_torsion_numerator',s.trigsimp(W.dot(g.diff(t,3))-3*s.sin(t)*s.cos(t))==0)
ck('all_t_norm_lower_identity',s.trigsimp(W.dot(W)-s.Rational(5,4)-s.Rational(3,4)*s.cos(2*t)**2)==0)
for v in [0,s.pi/2,s.pi,3*s.pi/2]:ck('exact_stationary_'+str(v),W.diff(t).subs(t,v)==s.zeros(3,1))
x,y,r=s.symbols('x y r',real=True);q=s.Matrix([x-e*x**3/r,y+e*y**3/r,(x*x-y*y)/4+e/r]);hz=q[2]-(q[0]**2-q[1]**2)/4
ck('independent_full_shear_expansion',s.expand(hz-e/r-e*(x**4+y**4)/(2*r)+e*e*(x**6-y**6)/(4*r*r))==0)
ck('entire_strict_embedding_interval',1-3*e==3*(s.Rational(1,3)-e))
ck('entire_height_interval_positive',1-s.Rational(1,3)/4==s.Rational(11,12)>0)
a=s.symbols('a',positive=True);prior=s.Matrix([a*s.cos(t),a*s.sin(t),a**4*(s.cos(t)**4-s.sin(t)**4)])
ck('all_a_prior_cross',zero(prior.diff(t).cross(prior.diff(t,2))-a*a*s.Matrix([-4*a**3*s.cos(t)**3,4*a**3*s.sin(t)**3,1])))
ck('exact_scale_specialization',zero(prior.subs(a,4**(-s.Rational(1,3)))*4**s.Rational(1,3)-g))
ck('graph_curvature_numerator',s.hessian(x**4-y**4,(x,y)).det()==-144*x*x*y*y)
# Read and parse the entire pinned 149 MB corpus; every SQLite JSON payload/report.
m=load(R/'unsolved_math_prioritization/manifest.json');cache=R/'unsolved_math_prioritization/cache';corpus=[]
for name,z in m['files'].items():
 b=(cache/name).read_bytes();ck(name+'_bytes_and_sha',len(b)==z['bytes'] and sha(b)==z['sha256']);corpus.append({'name':name,'bytes':len(b),'sha256':sha(b),'fully_json_parsed':True})
problems=load(cache/'problems.json');reports=load(cache/'research_results.json')
ck('15458_unique_numeric_records',len(problems)==15458==len({p['id'] for p in problems}))
p=next(z for z in problems if z['id']==7000004);rep=reports[p['problem_number']]
ck('complete_selected_raw_identity',p==load(C/'source_record.json') and rep==load(C/'prior_report.json'))
norm=lambda z:re.sub(r'\s+',' ',unicodedata.normalize('NFKC',z)).strip()
dups=[z['id'] for z in problems if norm(z.get('statement',''))==norm(p['statement'])];ck('complete_exact_statement_scan',dups==[7000004])
binorm=[{'id':z['id'],'statement':z.get('statement')} for z in problems if 'binormal' in z.get('statement','').lower()]
db=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro',uri=True);ck('sqlite_revision',db.execute('select revision from metadata').fetchone()==(m['revision'],))
parsed=0
for key,payload,report in db.execute('select key,payload,report from records'):
 pp=json.loads(payload);rr=json.loads(report);parsed+=1
 if key=='7000004':ck('actual_selected_sqlite_join',pp==p and rr==rep)
db.close();ck('all_sqlite_json_fully_parsed',parsed==15458)
qp=R/'unsolved_math_prioritization/queue.py';spec=importlib.util.spec_from_file_location('own_pure_score',qp);queue=importlib.util.module_from_spec(spec);spec.loader.exec_module(queue)
score=queue.score(p,rep,load(R/'unsolved_math_prioritization/policy.json'));ck('actual_pure_importer_hash',score['review_hash']==sha(json.dumps([p,rep],sort_keys=True).encode())==load(C/'readiness.json')['review_hash'])
ck('actual_pure_statement_hash',score['statement_hash']==sha(p['statement'].encode()))
sm=load(P/'snapshot_manifest.json');head=sm['head'];base=sm['base'];git=lambda args:subprocess.check_output(['git']+args,cwd=R)
ck('actual_git_merge_base',git(['merge-base',base,head]).decode().strip()==base)
ck('actual17path_diff',git(['diff','--name-only',base,head]).decode().splitlines()==sm['changed_paths'])
for z in sm['files']:ck('actual_original_git_'+z['path'],git(['show',head+':unsolved_math_prioritization/attempts/7000004/'+z['path']])==(C/'original_archive'/z['path']).read_bytes())
ck('all_original16_git_bytes',len(sm['files'])==16)
ck('original_and_new_turns_byte_unchanged', (C/'turns.jsonl').read_bytes()==(P/'reviewed_candidate/turns.jsonl').read_bytes())
related=load(R/'unsolved_math_prioritization/review_v2/related_target_groups.json');ck('related_target_not_present',all('7000004' not in z.get('ids',[]) for z in related['groups']))
ck('own_complete_packet_guard',bool(guard(C,R/'unsolved_math_prioritization/QUEUE.md')))
# Real source-code mutations; every mutated implementation is executed.
source=(C/'verify.py').read_text();mutations={
 'wrong_binormal_y':('C=S.Matrix([-x**3,y**3,1]);','C=S.Matrix([-x**3,-y**3,1]);'),
 'wrong_amplitude':('gamma=S.Matrix([x,y,(x*x-y*y)/4])','gamma=S.Matrix([x,y,(x*x-y*y)/2])'),
 'missing_norm_constant':('R2=1+x**6+y**6;q=','R2=x**6+y**6;q='),
 'wrong_torsion':('C.dot(gppp)-3*x*y','C.dot(gppp)-2*x*y'),
 'wrong_shear_height':('expected=e/r+e*(x**4+y**4)/(2*r)','expected=e/r-e*(x**4+y**4)/(2*r)'),
 'no_offset_normalization':('P=gamma+e*C/r','P=gamma+e*C'),
 'signed_tau_instead_of_abs':('S.simplify(kg-k/abs(tors))==0','S.simplify(kg-k/tors)==0')}
actual=[]
for name,(old,new) in mutations.items():
 assert source.count(old)==1;d=H/'actual_mutations'/name;d.mkdir(parents=True,exist_ok=True);f=d/'verify.py';f.write_text(source.replace(old,new));run=subprocess.run(['/usr/bin/python3',str(f)],capture_output=True,timeout=120)
 (d/'stdout.txt').write_bytes(run.stdout);(d/'stderr.txt').write_bytes(run.stderr);ck('actual_math_mutant_'+name,run.returncode!=0 and b'AssertionError:' in run.stderr)
 actual.append({'name':name,'sha256':sha(f.read_bytes()),'exit':run.returncode,'assertion':run.stderr.decode().split('AssertionError:',1)[1].strip()})
# Actual packet mutation files and subprocess validation; source and status are independently guarded.
packet=[]
def packetmut(name,rel,change,queuechange=None):
 d=H/'tmp/packet_mutants'/name;shutil.copytree(C,d,dirs_exist_ok=True)
 if rel:
  a=load(d/rel);change(a);(d/rel).write_text(json.dumps(a,indent=2)+'\n')
 q=d/'queue.md';q.write_bytes((R/'unsolved_math_prioritization/QUEUE.md').read_bytes())
 if queuechange:queuechange(q,d)
 run=subprocess.run(['/usr/bin/python3',str(H/'packet_guard.py'),str(d),str(q)],capture_output=True,timeout=120)
 out=H/'actual_packet_mutants'/name;out.mkdir(parents=True,exist_ok=True);(out/'stdout.txt').write_bytes(run.stdout);(out/'stderr.txt').write_bytes(run.stderr)
 if rel:shutil.copyfile(d/rel,out/Path(rel).name)
 ck('actual_packet_mutant_'+name,run.returncode!=0 and b'AssertionError:' in run.stderr)
 packet.append({'name':name,'exit':run.returncode,'assertion':run.stderr.decode().split('AssertionError:',1)[1].strip(),'mutated_input_sha256':sha((d/rel).read_bytes()) if rel else sha(q.read_bytes())})
packetmut('raw_source_changed','source_record.json',lambda a:a.update(status='fabricated'))
packetmut('raw_report_changed','prior_report.json',lambda a:a.update(fabricated=True))
packetmut('reviewdoc_substituted_for_sourcepair','readiness.json',lambda a:a.update(review_hash=load(C/'original_archive/review/verdict.json')['review_sha256']))
packetmut('statement_hash_changed','readiness.json',lambda a:a.update(statement_hash='0'*64))
packetmut('stale_artifact_binding','readiness.json',lambda a:a.update(reviewed_artifact_sha256=sha((C/'original_archive/OBSTRUCTION.md').read_bytes())))
packetmut('attempt_reset','readiness.json',lambda a:a['budget'].update(used_substantive_attempts=1))
packetmut('audit_hides_new_route','readiness.json',lambda a:a['budget'].update(new_substantive_attempts=0,verification_attempts=1))
packetmut('inherited_expired_deadline','readiness.json',lambda a:a['budget'].update(time_cap_utc='2026-09-30T06:43:00Z'))
packetmut('unexposed_model_fabricated','readiness.json',lambda a:a['budget'].update(model='gpt-6-astra'))
packetmut('historical_timestamp_presented_current','readiness.json',lambda a:a.update(literature_checked_at='2026-09-30T04:52:00Z'))
packetmut('novelty_promotion','readiness.json',lambda a:a.update(positive_novelty_claim=True))
packetmut('new_paper_for_prior','readiness.json',lambda a:a.update(paper_or_new_doi_or_tracker=True))
packetmut('narrower_target_claim','current_status.json',lambda a:a.update(narrower_negative_curvature_target_resolved=True))
packetmut('downgrade_credited_result','current_status.json',lambda a:a.update(queue_status_proposed='unsolved'))
packetmut('historical_model_overwritten','readiness.json',lambda a:a['historical_original_attempt_metadata']['budget'].update(model='unexposed'))
for name,idx in [('findings_into_chat',10),('findings_into_doi',12)]:
 def change(a,idx=idx):
  z=a['row_prospective'].split('|');z[idx],z[11]=z[11],z[idx];a['row_prospective']='|'.join(z)
 packetmut(name,'CURRENT_QUEUE_PATCH.json',change)
packetmut('queue_budget_reset','CURRENT_QUEUE_PATCH.json',lambda a:a.update(row_prospective=a['row_prospective'].replace('2/5','1/5')))
def duplicate(q,d):
 q.write_bytes(q.read_bytes()+load(d/'CURRENT_QUEUE_PATCH.json')['row_before'].encode());a=load(d/'CURRENT_QUEUE_PATCH.json');a['whole_queue_preimage_sha256']=sha(q.read_bytes());(d/'CURRENT_QUEUE_PATCH.json').write_text(json.dumps(a))
packetmut('duplicate_queue_target',None,None,duplicate)
def legacy(q,d):
 q.write_bytes(q.read_bytes().replace(b'| Chat | Findings | DOI |',b'| Findings | DOI |'));a=load(d/'CURRENT_QUEUE_PATCH.json');a['whole_queue_preimage_sha256']=sha(q.read_bytes());(d/'CURRENT_QUEUE_PATCH.json').write_text(json.dumps(a))
packetmut('legacy_column_schema',None,None,legacy)
# Coverage negative controls: actual old programs still accept false adjacent global prose.
negative=[]
for label,rel,want in [('author','verify.py','verification.json'),('independent','review/independent_checks.py','review/independent_results.json')]:
 d=H/'tmp/negative_prose'/label;d.mkdir(parents=True,exist_ok=True);f=d/Path(rel).name;shutil.copyfile(C/'original_archive'/rel,f)
 (d/'OBSTRUCTION.md').write_text('FALSE CONTROL: every injective spherical binormal is regular, the global nonzero linking theorem is solved and novel.\n')
 run=subprocess.run(['/usr/bin/python3',str(f)],capture_output=True,timeout=120);ck('negative_prose_'+label,run.returncode==0 and not run.stderr and run.stdout==(C/'original_archive'/want).read_bytes())
 negative.append({'program':label,'unchanged_implementation_sha256':sha(f.read_bytes()),'false_prose_accepted':True,'output_byte_exact':True,'meaning':'Expected coverage hole: local-only diagnostics do not certify theorem prose, priority or current status.'})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks_passed':len(checks),'checks':checks,'corpus':corpus,'all_sqlite_payload_report_json_parsed':parsed,'full_normalized_exact_statement_duplicates':dups,'binormal_records':binorm,'pure_actual_importer_sha256':sha(qp.read_bytes()),'actual_math_mutants':actual,'actual_packet_mutants':packet,'negative_prose_controls':negative,'new_substantive_attempts_added':0,'scope':'All-parameter analytic proof sealed before history; computations supplement it. Full corpus parsed and selected join independently verified; no global source literature certification.'}
(H/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'math_mutants':len(actual),'packet_mutants':len(packet),'negative_prose_controls':len(negative)}))
