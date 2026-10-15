#!/usr/bin/env python3
"""Read actual new main and prove only one unrelated campaign row changed."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
A=Path(__file__).resolve().parents[1];C=A.parents[2]
P=A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json'
OLD='f9f840d21305bdc353d151abe8dd5c51b6a27dd6';NEW='e0a94b93520610553c001f265f210f959b591c2c'
O=A/'current_main_carryforward_input_20261006';O.mkdir(exist_ok=False)
def need(x,m):
 if not x:raise RuntimeError(m)
def now():return datetime.now(timezone.utc).isoformat()
def can(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(f):return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
packet=json.loads(P.read_bytes());runtime=packet['runtime'];git=runtime['binaries']['git']['resolved_absolute_path']
need(hp(Path(git).read_bytes())=={k:runtime['binaries']['git'][k] for k in ('bytes','sha256')},'Current physical Git')
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null','GIT_NO_REPLACE_OBJECTS':'1','GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'}
journal=[]
def run(args):
 argv=[git,'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper=',*args];start=now();p=subprocess.Popen(argv,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 try:out,err=p.communicate(timeout=30)
 except BaseException:
  p.kill();out,err=p.communicate();raise
 end=now();index=len(journal);stored=out if len(out)<=1024*1024 else out[:4096];f=O/(str(index)+'.stdout.bin');f.write_bytes(stored);e=O/(str(index)+'.stderr.bin');e.write_bytes(err)
 row={'PID':p.pid,'argv':argv,'cwd':str(C),'environment_sha256':hp(can(env))['sha256'],'UTC_start':start,'UTC_end':end,'exit_code':p.returncode,'reaped':True,'stdout':{'observed_bytes':len(out),'observed_sha256':hp(out)['sha256'],'retained_pin':pin(f),'full_raw_body':len(stored)==len(out)},'stderr':{'observed_bytes':len(err),'observed_sha256':hp(err)['sha256'],'retained_pin':pin(e),'full_raw_body':True}}
 if args[0]=='show':row['stdout']['full_body_custody']='immutable_Git_commit_path:'+args[-1]
 journal.append(row);(O/'PROCESS_JOURNAL.json').write_bytes(can({'actual_root_PID':os.getpid(),'processes':journal}));need(p.returncode==0 and not err,'Actual clean Git read');need(len(out)<=32*1024*1024,'Bounded native full body');return out,f
need(run(['rev-parse','HEAD'])[0].decode().strip()==NEW,'Own main was safely fast-forwarded')
need(run(['symbolic-ref','--short','HEAD'])[0].strip()==b'main','Stay on main')
need(run(['ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main'])[0].decode().split()==[NEW,'refs/heads/main'],'Current remote verified')
need(not run(['diff','--cached','--name-only','-z'])[0],'Own index has no staged changes')
need(run(['show','-s','--format=%P',NEW])[0].decode().split()==[OLD,'b31a0703ba3cd1ccd8298cdff8b507eb82a0b6fb'],'Exact foreign merge parents')
delta,deltafile=run(['diff','--name-status','--no-renames','-z',OLD,NEW]);parts=delta.split(b'\0');need(parts[-1]==b'' and len(parts[:-1])%2==0,'Complete actual raw Git delta')
changes=[{'status':parts[i].decode(),'path':parts[i+1].decode()} for i in range(0,len(parts)-1,2)]
need(len(changes)==64 and changes[0]=={'status':'M','path':'unsolved_math_prioritization/QUEUE.md'} and all(x['status']=='A' and x['path'].startswith('unsolved_math_prioritization/attempts/30005460/') for x in changes[1:]),'Exact unrelated-row/foreign-attempt delta only')
baseline={};current_queue=None;current_queue_file=None
for name,oldspec in packet['native_baseline'].items():
 body,f=run(['show',NEW+':'+oldspec['path']]);baseline[name]={'path':oldspec['path'],**hp(body)}
 if name=='QUEUE.md':current_queue=body;current_queue_file=f
 else:need(hp(body)=={k:oldspec[k] for k in ('bytes','sha256')},'Eleven other native bodies identical')
old_queue,old_queue_file=run(['show',OLD+':unsolved_math_prioritization/QUEUE.md']);need(hp(old_queue)=={k:packet['native_baseline']['QUEUE.md'][k] for k in ('bytes','sha256')},'Exact original assessed campaign')
before=old_queue.splitlines(keepends=True);after=current_queue.splitlines(keepends=True);need(len(before)==len(after),'No campaign line/order change')
indices=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y];need(indices==[307] and b'30005460 /' in before[307] and b'30005460 /' in after[307],'Exactly one unrelated physical row308')
targets=[i for i,x in enumerate(before) if b'5100032 /' in x];need(len(targets)==1 and before[targets[0]]==after[targets[0]],'PR110 campaign row unchanged')
rb=O/'changed_physical_row_before.bin';ra=O/'changed_physical_row_after.bin';rb.write_bytes(before[307]);ra.write_bytes(after[307])
for spec in packet['input_files']:need(hp((A/spec['path']).read_bytes())=={k:spec[k] for k in ('bytes','sha256')},'All182 original science/service/source inputs unchanged')
need(not (C/'unsolved_math_prioritization/attempts/5100032').exists(),'Native target still absent')
need((C/'unsolved_math_prioritization/QUEUE.md').read_bytes()==current_queue,'Current physical campaign equals actual Git body')
out={'schema':'pr110-current-main-carryforward-inputs/v1','UTC':now(),'actual_root_PID':os.getpid(),'actual_receipt':True,'template_only':False,'fixture':False,'simulated':False,'original_assessed_main_parent':OLD,'main_parent':NEW,'remote_main':NEW,'branch':'main','original_packet_sha256':hp(P.read_bytes())['sha256'],'native_baseline':baseline,'Git_delta_pin':pin(deltafile),'changed_paths':changes,'unrelated_QUEUE_id':'30005460','original_QUEUE_pin':pin(old_queue_file),'current_QUEUE_pin':pin(current_queue_file),'changed_physical_row_number':308,'changed_physical_row_before_pin':pin(rb),'changed_physical_row_after_pin':pin(ra),'all12_current_native_fullbodies_authenticated':True,'eleven_non_QUEUE_native_files_identical':True,'exactly_one_unrelated_QUEUE_row_changed':True,'target_QUEUE_row_unchanged':True,'original_target_source_prior_original17_unchanged':True,'science_priority_publication_tracker_unchanged':True,'main_and_remote_current_verified':True,'original_worker_not_reassessed':True,'Git_state_mutations_in_this_authentication':0,'checked_artifacts':[pin(O/'PROCESS_JOURNAL.json')]+[pin(O/(str(i)+'.'+stream+'.bin')) for i in range(len(journal)) for stream in ('stdout','stderr')]+[pin(rb),pin(ra)],'writer_window':'Other authorized audit chat confirmed it holds main pushes/merges until explicit PR110 writer release.'}
(O/'CURRENT_INTEGRATION_INPUTS.json').write_bytes(can(out));print(json.dumps({'current_main':NEW,'all12_native_bodies_authenticated':True,'only_one_unrelated_QUEUE_row_changed':True,'all182_original_inputs_unchanged':True,'integration_inputs_pin':pin(O/'CURRENT_INTEGRATION_INPUTS.json')}))
