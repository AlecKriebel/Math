"""Independent read-only complete-body inspector. Execute only this new own source.

Foreign primary/access/OCR/cache/SQL inputs stay in place: only bindings leave.
Full Git output retention is limited to first-party procedural native4 evidence
and original scientific Git bodies; it never retains full raw caches or SQL.
"""
from pathlib import Path,PurePosixPath
import json,hashlib,datetime,os,stat,subprocess,sqlite3,collections
from fractions import Fraction as F
from itertools import product

OWN=Path(__file__).resolve().parent;A=OWN.parent;R=A.parents[2];C=A/'reviewed_candidate'
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(o):return (json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def write(n,o):(OWN/n).write_bytes(dump(o))
def unique(items):
 d={}
 for k,v in items:
  assert k not in d,('duplicate_key',k)
  d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(x,y):
 if type(x)is not type(y):return False
 if type(x)is dict:return x.keys()==y.keys()and all(equal(x[k],y[k])for k in x)
 if type(x)is list:return len(x)==len(y)and all(equal(a,b)for a,b in zip(x,y))
 return x==y
def safe(p):
 assert not p.is_symlink()and all(not q.is_symlink()for q in p.parents)
 assert stat.S_ISREG(p.stat().st_mode)
 return p.read_bytes()
def ref(p):
 b=safe(p);return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def rel(n):
 p=PurePosixPath(n)
 assert type(n)is str and n and '\x00'not in n and '\\'not in n and not p.is_absolute()and p.as_posix()==n and not set(p.parts)&{'.','..','.git','__pycache__'}
 return n
def topo(root):
 assert root.is_dir()and not root.is_symlink()and all(not q.is_symlink()for q in root.parents)
 files=set();dirs=set()
 for p in root.rglob('*'):
  assert not p.is_symlink();n=rel(p.relative_to(root).as_posix())
  if p.is_file():files.add(n)
  else:assert p.is_dir();dirs.add(n)
 return files,dirs
def closure(root,name,rows=None,selfs=None,empty_ok=False):
 m=parse(safe(root/name));items=rows if rows is not None else m['files'];names={rel(z['path'])for z in items}
 assert len(names)==len(items)
 exclusions=set(selfs or m.get('self_excluded',[name]));files,dirs=topo(root)
 assert files==names|exclusions,('closure_topology',str(root),files^(names|exclusions))
 expected={p.as_posix()for n in files for p in PurePosixPath(n).parents if p.as_posix()!='.'}
 if not empty_ok:assert dirs==expected,('empty_directory',str(root),dirs^expected)
 observations=[]
 for z in items:
  p=root/z['path'];b=safe(p)
  assert type(z['bytes'])is int and len(b)==z['bytes']and sha(b)==z['sha256']
  assert stat.S_IMODE(p.stat().st_mode)==0o444,('full_mode',str(p))
  observations.append({'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':'0444'})
 for n in exclusions:assert stat.S_IMODE((root/n).stat().st_mode)==0o444
 return m,observations,dirs
GIT=[]
def git(label,*args):
 d=OWN/'actual_git'/'v2'/label;d.mkdir(parents=True,exist_ok=False)
 source=safe(Path(__file__));operator=safe(OWN/'capture_own.py')
 (d/'prelaunch_source.py').write_bytes(source);(d/'prelaunch_operator.py').write_bytes(operator)
 argv=['git',*args];start=utc()
 pre={'argv':argv,'cwd':str(R),'prepared_utc':start,'operator_pid':os.getpid(),'source_sha256':sha(source),'operator_sha256':sha(operator),'read_only':True}
 (d/'PRELAUNCH.json').write_bytes(dump(pre))
 child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
 (d/'LAUNCHED.json').write_bytes(dump({'argv':argv,'child_pid':child.pid,'parent_pid':os.getpid(),'start_utc':start}))
 out,err=child.communicate();end=utc()
 (d/'stdout.bin').write_bytes(out);(d/'stderr.bin').write_bytes(err)
 cap={**pre,'child_pid':child.pid,'start_utc':start,'end_utc':end,'exit_code':child.returncode,'stdout':ref(d/'stdout.bin'),'stderr':ref(d/'stderr.bin'),'source_unchanged':safe(Path(__file__))==source,'operator_unchanged':safe(OWN/'capture_own.py')==operator}
 (d/'CAPTURE.json').write_bytes(dump(cap));GIT.append({'label':label,'capture':ref(d/'CAPTURE.json'),**cap})
 assert child.returncode==0 and err==b''
 return out
def stream(cap,parent,channel):
 z=cap[channel];p=Path(z['path']);p=p if p.is_absolute() else (R/p if p.parts[0]=='draft_pr_publication_program_20260930' else parent/p)
 b=safe(p);assert type(z['bytes'])is int and len(b)==z['bytes']and sha(b)==z['sha256'];return b
def check_clock(start,end):
 a=datetime.datetime.fromisoformat(start.replace('Z','+00:00'));b=datetime.datetime.fromisoformat(end.replace('Z','+00:00'))
 assert a.utcoffset()==b.utcoffset()==datetime.timedelta(0)and a<=b
 return a,b
def typednodes(x,path='$'):
 yield {'path':path,'type':type(x).__name__,'value_sha256':sha(dump(x))}
 if type(x)is dict:
  for k,v in x.items():yield from typednodes(v,path+'/'+k)
 elif type(x)is list:
  for i,v in enumerate(x):yield from typednodes(v,path+'/'+str(i))

assert __debug__
m,packet,dirs=closure(C,'MANIFEST.json');assert len(packet)==497
deps=parse(safe(C/'CURRENT_DEPENDENCIES.json'));assert len(deps['files'])==416 and (R/deps['anchor_repository_relative']).resolve()==A
depobs=[]
for z in deps['files']:
 rel(z['path']);b=safe(A/z['path']);assert len(b)==z['bytes']and sha(b)==z['sha256']
 if z['path'].endswith('.json'):parse(b)
 if z['path'].endswith('.jsonl'):
  for line in b.splitlines():assert line.strip();parse(line)
 depobs.append({'path':str(A/z['path']),'bytes':len(b),'sha256':sha(b),'roles':z['roles']})
write('COMPLETE_PACKET_AND_DEPENDENCY_BINDINGS.json',{'packet_manifest':ref(C/'MANIFEST.json'),'packet_members':packet,'packet_directories':sorted(dirs),'dependency_manifest':ref(C/'CURRENT_DEPENDENCIES.json'),'complete_dependencies':depobs})
snap=parse(safe(A/'snapshot_manifest.json'));assert len(snap['files'])==18
head=snap['head'];assert head=='d9b4acf5d070d1f04ffac86a4f08916a5629ff16'
assert git('actual_merge_base','merge-base',head,snap['github_base']).decode().strip()==snap['merge_base']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737'
assert snap['github_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
originalobs=[]
for i,z in enumerate(snap['files']):
 n=z['relative_path'];b=safe(A/'source_snapshot'/n)
 assert len(b)==z['bytes']and sha(b)==z['sha256']and safe(C/'original_archive'/n)==b
 actual=git('original_body_%02d'%i,'show',head+':'+z['path']);tree=git('original_tree_%02d'%i,'ls-tree',head,'--',z['path'])
 assert actual==b and tree==('100644 blob '+z['git_object']+'\t'+z['path']+'\n').encode()
 originalobs.append({'name':n,**ref(A/'source_snapshot'/n),'git_blob':z['git_object'],'git_mode':'100644'})
immutable=['PARTIAL.md','SOURCES.md','binary_verification.json','source_manifest.json','source_record.json','turns.jsonl','verify_binary_process.py','review/verify_binary_process.py','review/submitted_results.json','review/PARTIAL.md','review/independent_checks.py','review/independent_results.json']
for n in immutable:assert safe(C/n)==safe(A/'source_snapshot'/n)
actualdiff=git('original_diff','diff','--no-ext-diff','--no-textconv','--binary',snap['merge_base'],head,'--')
assert actualdiff==safe(A/'original_diff.patch')==safe(C/'original_diff.patch')and len(actualdiff)==183402
changes=git('original_changed_paths','diff','--name-only',snap['merge_base'],head).decode().splitlines();assert len(changes)==19
write('ORIGINAL18_AND_IMMUTABLE12.json',{'original':originalobs,'immutable12':immutable,'whole19_diff':ref(A/'original_diff.patch'),'all_changed_paths':changes})

# Full original result objects and every historical diagnostic label, no old code execution.
author=parse(safe(C/'binary_verification.json'));ind=parse(safe(C/'review/independent_results.json'))
assert type(author['exact_assertions'])is int and author['exact_assertions']==885
for z in author['window_receipts']:
 n,r=z['n'],z['r'];assert type(n)is type(r)is int and F(z['tv'])==F(r,n+r+1)and F(z['no_flip'])==F(n+1,n+r+1)
expected=[]
for n in range(1,10):
 expected += ['mass_%d'%n,'fair_last_%d'%n]
 for mh in range(n):
  expected += ['conditional_%d_%d_%d'%(n,mh,j)for j in range(2**(mh+1))]
  expected += ['max_finite_history_correlation_%d_%d'%(n,mh)]
for n in range(4,10):
 for mask in range(16):expected += ['anticipative_%s_%d_%d'%(s,n,mask)for s in ['B_fair','tower','mismatch']]
for n in range(6):
 for r in range(5):expected += ['window_TV_%d_%d'%(n,r),'no_flip_window_%d_%d'%(n,r)]
for idx in range(64):
 for b in [-1,1]:expected += ['metric_pointwise_%d_%d'%(idx,b)]
for n in range(40):
 for s in range(9):expected += ['offset_bound_%d_%d'%(n,s)]
expected += ['offset_union_sum_%d'%n for n in range(40)]+['double_time_gap_%d'%n for n in range(1,80)]
assert len(expected)==3044 and set(expected)==set(ind['checks'])and len(set(expected))==3044
assert type(ind['passed'])is int and ind['passed']==3044 and type(ind['failed'])is int and ind['failed']==0
labelobs=[{'label':n,'saved_type':type(ind['checks'][n]).__name__,'saved_value':ind['checks'][n],'independently_reconstructed_parameter_schema':True}for n in expected]
assert all(z['saved_type']=='str'and z['saved_value']=='PASS'for z in labelobs)
write('ALL3044_HISTORICAL_LABEL_INSPECTION.json',{'schema':'pr45-complete-historical-label-inspection/v1','ordered_labels':labelobs,'execution_attribution':'historical results plus ROOT current unchanged reproductions, not execution by this family','universal_proof_from_counts':False})
write('COMPLETE_ORIGINAL_RESULT_TYPED_NODES.json',{'author_nodes':list(typednodes(author)),'independent_nodes':list(typednodes(ind))})
root=A/'root_original_actual_reproduction';rm,rootobs,_=closure(root,'MANIFEST.json');assert len(rootobs)==41
result=parse(safe(root/'ROOT_REPRODUCTION_RESULT.json'));summary=parse(safe(root/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json'))
assert equal(result['author_result'],author)and equal(result['historical_submitted_result'],author)and equal(result['independent_result'],ind)
assert equal(summary['entire_author_result'],author)and equal(summary['entire_independent_result'],ind)
for name,count,pid,src in [('current_author',885,88784,'verify_binary_process.py'),('historical_submitted',885,88785,'review/verify_binary_process.py'),('historical_independent',3044,88786,'review/independent_checks.py')]:
 d=root/name;cap=parse(safe(d/'CAPTURE.json'))
 assert cap['pid']==pid and cap['exit_code']==0 and cap['actual_execution']is True and cap['completed']is True and cap['source_unchanged']is True
 assert safe(d/'PRELAUNCH_SOURCE.py')==safe(A/'source_snapshot'/src)
 for k in ['stdout','stderr']:stream(cap,d,k)
 assert safe(d/'stderr.bin')==b'' and safe(d/'ACTUAL_RESULT.json')==safe(d/'ORIGINAL_SAVED_RESULT.json')
 if name=='historical_independent':
  assert safe(d/'PARTIAL.md')==safe(C/'PARTIAL.md')and safe(d/'independent_results.json')==safe(d/'ACTUAL_RESULT.json')
  assert equal(parse(safe(d/'stdout.bin')),{k:v for k,v in ind.items()if k!='checks'})
 else:assert safe(d/'stdout.bin')==safe(d/'ACTUAL_RESULT.json')
 check_clock(cap['started_utc'],cap['finished_utc'])
outerobs=[]
for name,pid,exitcode in [('root_helper_reproduction_actual_capture',88783,0),('root_full_raw_SQL_actual_capture',88914,1),('root_full_raw_SQL_v2_actual_capture',89614,0),('root_reproduction_closure_actual_capture',96803,1),('root_reproduction_closure_v2_actual_capture',97408,0),('root_current_freeze_inspection_actual_capture',2177,0)]:
 d=A/name;cap=parse(safe(d/'CAPTURE.json'));assert cap['pid']==pid and cap['exit_code']==exitcode
 for k in ['stdout','stderr']:stream(cap,d,k)
 check_clock(cap['started_utc'],cap['finished_utc']);outerobs.append({'capture':ref(d/'CAPTURE.json'),'entire_capture':cap})
assert safe(root/'ROOT_CURRENT_REPRODUCTION_SUMMARY_FIRST_FAILED_CLOSURE.json')==safe(root/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json')
write('ROOT_ACTUAL_REPRODUCTION_INSPECTION.json',{'root_manifest':ref(root/'MANIFEST.json'),'members':rootobs,'captures':outerobs,'all_complete_objects_typed_equal':True,'all41_plus_self_actual':True,'failed_history_preserved':True})

# Complete raw importer reconstruction in place; record only hashes per entire row.
cache=R/'unsolved_math_prioritization/cache';rb=safe(cache/'problems.json');pb=safe(cache/'research_results.json')
raw=parse(rb);prior=parse(pb);assert len(rb)+len(pb)==149266659
byid={str(v['id']):v for v in raw};codes=collections.Counter(v['problem_number']for v in raw)
assert len(byid)==len(raw)==15458 and len(prior)==6701
conn=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True);conn.execute('PRAGMA query_only=ON')
assert conn.execute('PRAGMA query_only').fetchone()==(1,)
sqlobs=[]
for key,payload,report in conn.execute('SELECT key,payload,report FROM records ORDER BY key'):
 expectedpayload=dict(byid[key]);code=expectedpayload['problem_number']
 ambiguous=codes[code]>1 and code in prior
 if ambiguous:expectedpayload['_ambiguous_report']=True
 expectedprior={}if ambiguous else prior.get(code,{})
 observedpayload=parse(payload);observedprior=parse(report)
 assert equal(observedpayload,expectedpayload)and equal(observedprior,expectedprior),key
 sqlobs.append({'key':key,'entire_payload_sha256':sha(payload.encode()),'entire_report_sha256':sha(report.encode()),'recursive_type_sensitive_payload_equal':True,'recursive_type_sensitive_report_equal':True,'raw_prior_present':code in prior,'ambiguous_code_fallback':ambiguous})
conn.close();assert len(sqlobs)==15458
source=parse(safe(C/'source_record.json'));selected=byid['9900007'];code=selected['problem_number']
assert code=='AMR-098-0007'and code in prior and type(prior[code])is dict and prior[code]
assert set(source)=={'dataset_revision','problem','upstream_report'}and equal(source['problem'],selected)and equal(source['upstream_report'],prior[code])
write('COMPLETE_RAW_SQL_INSPECTION_BINDINGS.json',{'schema':'pr45-own-in-place-full-raw-sql-inspection/v1','input_bindings':[ref(cache/n)for n in ['problems.json','research_results.json','catalog.sqlite']],'complete_row_bindings':sqlobs,'selected_prior_present_nonempty_dict':True,'selected_wrapper_typed_equal':True,'absent_fallback_for_pr45':False,'foreign_bodies_copied':False})
del rb,pb,raw,prior,byid

# Exact source/family closures including source adversary outside reviewed packet.
pins=parse(safe(A/'current_preparation_family/STATIC_INPUT_BINDINGS.json'));familyobs=[]
for family,info in pins['families'].items():
 rootf=A/family;copied=info['copied_members'];foreign=info['foreign_members'];mf=info['manifest']['path']
 mfo=closure(rootf,mf,rows=copied+foreign,selfs=[mf],empty_ok=True)
 actualdirs={p.relative_to(rootf).as_posix()for p in rootf.rglob('*')if p.is_dir()}
 assert actualdirs==set(info['directories'])
 for n,mode in info['directory_modes'].items():assert stat.S_IMODE((rootf/n).stat().st_mode)==mode
 familyobs.append({'family':family,'manifest':ref(rootf/mf),'copied_members':copied,'foreign_members_individually_excluded':foreign,'directories':sorted(actualdirs)})
sm,sourceobs,_=closure(A/'current_preparation_family','PREPARATION_MANIFEST.json');assert len(sourceobs)==47
am,adverobs,adverdirs=closure(A/'current_source_adversary_family','OWN_CLOSURE.json',empty_ok=True);assert len(adverobs)==70 and set(am['directories'])==adverdirs
ss=parse(safe(A/'ROOT_SOURCE_SAFETY_INSPECTION.json'))
assert equal(ss['entire_source_verdict'],parse(safe(A/'current_source_adversary_family/VERDICT.json')))
assert ss['source_adversary_report']['sha256']==sha(safe(A/'current_source_adversary_family/REPORT.md'))
assert ss['source_adversary_verdict']['sha256']==sha(safe(A/'current_source_adversary_family/VERDICT.json'))
assert ss['source_closures'][1]['sha256']==sha(safe(A/'current_source_adversary_family/OWN_CLOSURE.json'))
foreign64=pins['families']['literal_priority_family']['foreign_members'];assert len(foreign64)==64
primaryhash={z['sha256']:z['path']for z in foreign64 if z['path'].startswith('foreign_primary/')and z['bytes']}
assert not set(primaryhash)&{z['sha256']for z in packet}
write('SOURCE_AND_FAMILY_CLOSURES_INSPECTION.json',{'families':familyobs,'SOURCE47_plus_self':sourceobs,'new_source_adversary70_plus_self':adverobs,'outside_packet_source_safety_record':ref(A/'ROOT_SOURCE_SAFETY_INSPECTION.json'),'all64_foreign_paths_individually_bound_and_not_copied':True,'nonempty_primary_payload_hash_collisions':[],'empty_streams_and_shared_authored_code_not_treated_as_foreign_payload_copy':True})

# Genuine final outer versus honest inner prefix.
execution=parse(safe(C/'CURRENT_EXECUTION_REFERENCE.json'));od=A/execution['audit_relative_outer_capture'];id_=A/execution['audit_relative_inner_attempt']
cap=parse(safe(od/'CAPTURE.json'));pre=parse(safe(od/'OPERATION_PRELAUNCH.json'));inv=parse(safe(id_/'INVOCATION.json'))
assert topo(od)[0]=={'CAPTURE.json','OPERATION_PRELAUNCH.json','PRELAUNCH_BUILDER_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}
assert sha(safe(od/'CAPTURE.json'))=='bcfa9fc8791326fb79771c74e48d3e1dc51abe38c48c4e624d6800128b9f201b'
assert cap['operator_pid']==pre['operator_pid']==inv['parent_pid']==99703 and cap['pid']==inv['pid']==99704
assert cap['argv']==pre['argv']and cap['argv'][2:]==inv['argv']and cap['cwd']==pre['cwd']==inv['cwd']==str(R)
assert cap['builder_sha256']==sha(safe(od/'PRELAUNCH_BUILDER_SOURCE.py'))==sha(safe(A/'current_preparation_family/prepare_current_packet.py'))
assert cap['operator_sha256']==sha(safe(od/'PRELAUNCH_OPERATOR.py'))==sha(safe(A/'current_preparation_family/capture_root_builder_operation.py'))
assert sha(safe(od/'OPERATION_PRELAUNCH.json'))==execution['outer_prelaunch_sha256']
for k in ['stdout','stderr']:stream(cap,od,k)
assert cap['exit_code']==0 and cap['actual_execution']is cap['completed']is True and cap['current_whole_verdict']is None
start,end=check_clock(cap['started_utc'],cap['finished_utc']);commands=parse(safe(id_/'GIT_COMMANDS.json'));prefix=parse(safe(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json'))
assert len(commands)==47 and len(prefix)==45 and equal(commands[:45],prefix)
for cmd in commands:
 assert cmd['exit_code']==0 and cmd['actual_execution']is cmd['completed']is True and type(cmd['pid'])is int and cmd['pid']>0 and cmd['argv'][0]=='git'
 cs,ce=check_clock(cmd['started_utc'],cmd['finished_utc']);assert start<=cs<=ce<=end
 for k in ['stdout','stderr']:stream(cmd,id_,k)
 assert cmd['stderr']['bytes']==0
write('COMPLETE_FINAL_OUTER_AND_INNER_INSPECTION.json',{'outer_six_members':[ref(p)for p in sorted(od.iterdir())],'entire_outer':cap,'entire_final_inner_commands':commands,'honest_prefix_count':45,'final_count':47,'all47_full_streams_read_and_bound':True,'prepublication_prefix_is_not_final_capture':True})

# Dated native four queried at frozen Git HEAD; stable nine read live separately.
fresh=parse(safe(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'));frozen=fresh['current_head'];assert frozen==deps['current_main_head']=='264c26d539d616b0da6f8df76478a213d20939e4'
four={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
assert len(fresh['files'])==13 and {z['path']for z in fresh['files']}=={z['path']for z in deps['current_native13']}
native=[]
for z in fresh['files']:
 n=z['path'];live=safe(R/n);observed={'path':n,'frozen_binding':z,'live_binding':ref(R/n)}
 if n in four:
  label=Path(n).name.replace('.','_');body=git('frozen_native4_'+label+'_body','show',frozen+':'+n);tree=git('frozen_native4_'+label+'_tree','ls-tree',frozen,'--',n)
  assert len(body)==z['bytes']and sha(body)==z['sha256']
  assert tree.decode().startswith('100644 blob ')and tree.decode().endswith('\t'+n+'\n')
  observed.update(actual_frozen_git_body_equal=True,git_mode='100644',git_tree_stdout_sha256=sha(tree),live_equal_frozen=live==body)
 else:
  assert len(live)==z['bytes']and sha(live)==z['sha256'];observed.update(stable_live_equals_frozen_binding=True)
 native.append(observed)
branch=git('live_branch','branch','--show-current').decode().strip();livehead=git('live_head','rev-parse','HEAD').decode().strip();assert branch=='main'
write('DATED_NATIVE4_AND_STABLE_LIVE9.json',{'frozen_main_head':frozen,'live_head_at_inspection':livehead,'branch':branch,'native13':native,'dated_native_four_enumerated_even_if_foreign_inventory_excludes_them':sorted(four),'full_git_streams_retained_first_party_procedural_exception':True,'acceptance_on_future_main_approved':False,'must_restore_local0444_after_git_checkout':True,'git_full_permissions_preserved':False,'git_empty_directories_preserved':False})

patch=parse(safe(C/'CURRENT_QUEUE_PATCH.json'));before=safe(C/'queue_proposal/QUEUE_PREIMAGE.md');after=safe(C/'queue_proposal/QUEUE_PROSPECTIVE.md')
old=patch['row_before'].encode();new=patch['row_prospective'].encode()
assert before.count(old)==1 and after.count(new)==1 and before.replace(old,new,1)==after and after.replace(new,old,1)==before
assert sha(before)==patch['whole_preimage_sha256']and sha(after)==patch['whole_prospective_sha256']
assert [i for i,(x,y)in enumerate(zip(old.split(b'|'),new.split(b'|')))if x!=y]==[8,9,11]
assert patch['allowed_named_changes']==['Status','Turns','Findings']
for name in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:
 o=parse(safe(C/name));assert o['status']=='unsolved'and o['full_problem_solved']is o['novelty_claimed']is False and o['original_substantive_attempts']==1 and o['new_substantive_attempts']==o['audit_turns']==0
 assert all(o[k]is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict'])
write('QUEUE_INVERSE_AND_PRESENTATION_INSPECTION.json',{'inverse_whole_queue_identity':True,'only_changed_named_fields':['Status','Turns','Findings'],'all_other_fields_rows_Chat_DOI_preserved':True,'native_queue_written':False,'current_status_unsolved_and_runtime_null':True})
write('OWN_ACTUAL_READ_ONLY_GIT_CAPTURES.json',{'complete_actual_captures':GIT,'full_stdout_stderr_retained':True,'foreign_primary_or_raw_cache_Git_retrieval':False})
print(json.dumps({'schema':'pr45-own-whole-current-inspection/v1','status':'PASS_COMPLETE_INDEPENDENT_READ_ONLY_INSPECTION','pid':os.getpid(),'utc':utc(),'packet497_plus_self':True,'dependencies416_full_bytes':True,'original18_and_immutable12':True,'all3044_typed_labels':True,'ROOT41_plus_self':True,'SOURCE47_plus_self':True,'newsource70_plus_self':True,'full_raw149266659_SQL15458_in_place':True,'prior_present_nonempty_dict':True,'complete_outer99703_inner99704':True,'final47_prefix45':True,'frozen_native4_full_actual_Git_captures':True,'live_stable9':True,'new_whole_acceptance_approved':False,'full_problem_solved':False},indent=2))
