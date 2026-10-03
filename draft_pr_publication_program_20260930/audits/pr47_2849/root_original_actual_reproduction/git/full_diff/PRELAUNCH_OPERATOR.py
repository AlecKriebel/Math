"""ROOT reproduction of literal original diagnostics; no global Floer claim."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_original_actual_reproduction'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 return p.read_bytes()
def parse(b):
 def pairs(items):
  o={}
  for k,v in items:
   assert k not in o;o[k]=v
  return o
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(x,y):
 if type(x)is not type(y):return False
 if type(x)is dict:return x.keys()==y.keys()and all(equal(x[k],y[k])for k in x)
 if type(x)is list:return len(x)==len(y)and all(equal(a,b)for a,b in zip(x,y))
 return x==y
def ref(p):
 b=read(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def dump(o):return (json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def capture(folder,argv,source=None):
 folder.mkdir(parents=True,exist_ok=False)
 pre={'schema':'pr47-root-literal-operation-capture/v1','argv':argv,'cwd':str(R),'started_utc':utc(),'actual_operator_pid':os.getpid(),'stdin_supplied':False,'source':ref(source)if source else None}
 if source:(folder/'PRELAUNCH_SOURCE.py').write_bytes(read(source))
 (folder/'PRELAUNCH_OPERATOR.py').write_bytes(read(Path(__file__).resolve()))
 (folder/'PRELAUNCH.json').write_bytes(dump(pre))
 child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
 out,err=child.communicate()
 (folder/'stdout.bin').write_bytes(out);(folder/'stderr.bin').write_bytes(err)
 cap={**pre,'actual_execution':True,'pid':child.pid,'completed':True,'exit_code':child.returncode,'finished_utc':utc(),'stdout':ref(folder/'stdout.bin'),'stderr':ref(folder/'stderr.bin'),'source_unchanged':read(source)==read(folder/'PRELAUNCH_SOURCE.py')if source else None}
 (folder/'CAPTURE.json').write_bytes(dump(cap))
 assert child.returncode==0 and err==b''
 return out,cap
assert __debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','')in ('','0')
source=read(Path(__file__).resolve());(A/'ROOT_REPRODUCTION_PRELAUNCH_SOURCE.py').write_bytes(source)
D.mkdir(exist_ok=False)
closures=[]
for folder,name,pin,count in [(A,'ORIGINAL_PREPARATION_MANIFEST.json','d27e4f27be1743926b89a79dbb616773127c81f01b093c4be7caa6f941cc72b6',301),(A/'cover_algebra_family','SELF_MANIFEST.json','3ef0383c70a0ed8c08bd7f4a403b1e82057a9d7038a45bac45cbd3fe271814fe',143),(A/'gauge_geometry_family','SELF_MANIFEST.json','0133b0499de07f9eda83e1572d8f87ccece779065520ba439b200e5be478f79d',71)]:
 raw=read(folder/name);assert sha(raw)==pin;m=parse(raw);assert len(m['files'])==count
 names={r['path']for r in m['files']}|{name};assert len(names)==count+1
 if folder==A:
  physical=set(m['authorship_root_files'])|{name}
  for n in m['authorship_directory_roots']:physical|={p.relative_to(A).as_posix()for p in(A/n).rglob('*')if p.is_file()}
 else:physical={p.relative_to(folder).as_posix()for p in folder.rglob('*')if p.is_file()}
 assert physical==names
 for row in m['files']:
  p=folder/row['path'];b=read(p);assert len(b)==row['bytes']and sha(b)==row['sha256']and stat.S_IMODE(p.stat().st_mode)==0o444
 assert stat.S_IMODE((folder/name).stat().st_mode)==0o444
 closures.append({'manifest':ref(folder/name),'complete_payload_files':count,'all_payload_bytes_and_full_modes_checked':True})
snapshot=parse(read(A/'snapshot_manifest.json'));assert len(snapshot['files'])==snapshot['original_files']==16
caps=[]
for i,row in enumerate(snapshot['files']):
 raw=read(A/'source_snapshot'/row['relative_path']);assert len(raw)==row['bytes']and sha(raw)==row['sha256']
 out,cap=capture(D/'git'/('body_'+str(i)),['git','show',snapshot['head']+':'+row['path']]);caps.append(cap);assert out==raw
 out,cap=capture(D/'git'/('tree_'+str(i)),['git','ls-tree',snapshot['head'],'--',row['path']]);caps.append(cap)
 assert out.decode().strip()=='100644 blob '+row['git_object']+'\t'+row['path']
out,cap=capture(D/'git'/'full_diff',['git','diff','--no-ext-diff','--no-textconv','--binary',snapshot['merge_base'],snapshot['head'],'--']);caps.append(cap)
assert out==read(A/'original_diff.patch')and len(out)==59460 and sha(out)=='17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27'
turns=parse(read(A/'source_snapshot/turns.json'));assert type(turns)is dict and type(turns['count'])is int and turns['count']==1 and len(turns['attempts'])==1
assert read(A/'source_snapshot/prior_report.json')==b'null\n'
helper_caps=[];results={}
for label,helper,receipt,count in [('author','verify.py','verification.json',114),('submitted_copy','review/submitted_verify.py','verification.json',114),('historical_independent','review/independent_checks.py','independent_results.json',100)]:
 folder=D/label;folder.mkdir();original=A/'source_snapshot'/helper;copied=folder/original.name;copied.write_bytes(read(original))
 out,cap=capture(folder/'actual_capture',['/usr/bin/python3','-B',str(copied)],original);helper_caps.append(cap)
 actual=read(folder/receipt);expected=read(A/'source_snapshot'/('verification.json'if label!='historical_independent'else'review/independent_results.json'))
 assert actual==expected and equal(parse(actual),parse(expected))and read(copied)==read(original)
 obj=parse(actual)
 if label!='historical_independent':assert obj['passed']is True and type(obj['assertions'])is int and obj['assertions']==count and len(obj['checks'])==count
 else:assert type(obj['passed'])is int and obj['passed']==100 and type(obj['failed'])is int and obj['failed']==0 and len(obj['checks'])==100
 assert equal(parse(out),{k:v for k,v in obj.items()if k!='checks'})
 results[label]=obj
assert read(A/'source_snapshot/verify.py')==read(A/'source_snapshot/review/submitted_verify.py')
summary={'schema':'pr47-root-original-complete-reproduction/v1','created_utc':utc(),'actual_operator_pid':os.getpid(),'status':'PASS_ROOT_UNCHANGED_ORIGINAL_REPRODUCTION','closures':closures,'complete_actual_helper_captures':helper_caps,'complete_actual_Git_captures':caps,'entire_author_result':results['author'],'entire_identical_submitted_copy_result':results['submitted_copy'],'entire_historical_independent_result':results['historical_independent'],'complete_original_turns':turns,'original_substantive_attempts':1,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'duplicate114_counted_independent':False,'original_prior_literal':None,'upstream_prior_presence_not_inferred_from_literal':True,'full_Floer_problem_solved':False,'mandatory_correction_to_universal_vanishing_route_pending':True,'future_acceptance_approved':False}
(D/'ROOT_REPRODUCTION_RESULT.json').write_bytes(dump(summary))
assert read(Path(__file__).resolve())==source
print(json.dumps({'status':summary['status'],'actual_operator_pid':os.getpid(),'author':114,'identical_submitted_copy':114,'historical_independent':100,'full_original16_and17_path_diff_Git_proven':True,'entire_receipts_byte_and_recursive_types_equal':True,'future_acceptance_approved':False}))
