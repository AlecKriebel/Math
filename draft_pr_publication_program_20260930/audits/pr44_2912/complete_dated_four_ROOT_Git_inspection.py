"""ROOT supplies actual direct four-file immutable-Git evidence omitted by V2 row inventory."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
assert __debug__;source=Path(__file__).read_bytes();(A/'ROOT_DATED4_PRELAUNCH_SOURCE.py').write_bytes(source)
p=A/'ROOT_WHOLE_CURRENT_REVIEW.json';old=p.read_bytes();assert sha(old)=='3f5190f884a1e02ee7d7e02df0a59caf0067abf4869a96f4f68121f0f6c7c1ef'
(A/'ROOT_WHOLE_CURRENT_REVIEW_V2_BEFORE_DIRECT_FOUR.json').write_bytes(old)
j=json.loads(old);freeze=json.loads((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes());head=freeze['current_head'];assert head=='2b9d0234b1396fa84c4b34055b5e8e14c873588b'
D=A/'root_complete_dated_four_actual_Git';D.mkdir(exist_ok=False);rows={z['path']:z for z in freeze['files']};caps=[];changes=[]
for n in sorted(['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']):
 pair=[]
 for args in [['ls-tree',head,'--',n],['show',head+':'+n]]:
  folder=D/str(len(caps));folder.mkdir();argv=['git',*args];started=stamp();pre={'argv':argv,'cwd':str(R),'started_utc':started,'operator_pid':os.getpid(),'stdin_supplied':False};(folder/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
  with (folder/'stdout.bin').open('xb') as out,(folder/'stderr.bin').open('xb') as err:
   child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'});code=child.wait()
  cap={**pre,'pid':child.pid,'finished_utc':stamp(),'exit_code':code,'actual_execution':True,'completed':True,'stdout':ref(folder/'stdout.bin'),'stderr':ref(folder/'stderr.bin')};(folder/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n');caps.append(cap)
  assert code==0 and (folder/'stderr.bin').read_bytes()==b'';pair.append((folder/'stdout.bin').read_bytes())
 tree,body=pair;assert tree.decode().startswith('100644 blob ') and tree.decode().endswith('\t'+n+'\n') and len(body)==rows[n]['bytes'] and sha(body)==rows[n]['sha256']
 actual=(R/n).read_bytes()
 if actual!=body:changes.append({'path':n,'historical_bytes':len(body),'historical_sha256':sha(body),'present_bytes':len(actual),'present_sha256':sha(actual),'qualification':'Immutable dated input only; actual present state requires separate fresh acceptance preimages.'})
assert len(caps)==8
j.update(created_utc=stamp(),complete_dated_git_captures=caps,legitimate_dated_native_changes=changes,source_and_failure_qualification='Original ROOT94701 compared deliberately false prelaunch mutable fields with final capture; preserved corrected95178 validates96+self,all964 foreign and own genuine ten immutable Git records. That foreign inventory excludes four live-native paths, so95178 direct-loop arrays were empty. This distinct actual operation independently queries all four100644 bodies from frozen2b9d023 and binds eight genuine complete ROOT Git captures; V2 record retained verbatim. Every science/current/whole byte and original own failures remain unchanged. No epoch rebinding or future acceptance is certified.',direct_four_independent_ROOT_Git_checks_completed=True,actual_direct_four_operator_pid=os.getpid(),superseded_ROOT_V2_record=ref(A/'ROOT_WHOLE_CURRENT_REVIEW_V2_BEFORE_DIRECT_FOUR.json'))
p.write_text(json.dumps(j,indent=2)+'\n');assert Path(__file__).read_bytes()==source
print(json.dumps({'status':'PASS_ROOT_COMPLETE_DIRECT_FOUR_AND_WHOLE_INSPECTION','actual_pid':os.getpid(),'actual_git_children':[z['pid'] for z in caps],'updated_ROOT_record':ref(p),'frozen_head':head,'future_execution_approved':False}))
