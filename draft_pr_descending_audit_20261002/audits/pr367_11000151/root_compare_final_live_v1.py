"""Independently close the exact live gate and compare every full math output.
The root's earlier independently written mathematical checks remain immutable.
This program also replays the whole reviewed ZIP after the agent finishes.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64, gzip, hashlib, json, os, subprocess, tempfile, zipfile
A=Path(__file__).resolve().parent
F=A/'clean_final_adversary/final_live';V=A/'preprint/verification'
R=A/'root_exact_live_streams';R.mkdir(exist_ok=True)
PY=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python')
QUEUE='unsolved_math_prioritization/QUEUE.md';PREFIX='problems/11000151_artin_a5_quotient'
CHECKS=[];CAPTURES=[]
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def check(c,label):
 CHECKS.append({'check':label,'pass':bool(c)})
 assert c,label
def run(label,args,cwd=None):
 begin=utc();r=subprocess.run(list(map(str,args)),cwd=cwd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 row={'label':label,'args':list(map(str,args)),'started_utc':begin,'finished_utc':utc(),'exit_code':r.returncode}
 for channel in ('stdout','stderr'):
  b=getattr(r,channel);p=R/(label+'.'+channel+'.gz');stored=gzip.compress(b,mtime=0);p.write_bytes(stored)
  row[channel]={'path':str(p.relative_to(A)),'raw_bytes':len(b),'raw_sha256':sha(b),'stored_bytes':len(stored),'stored_sha256':sha(stored)}
 CAPTURES.append(row)
 check(r.returncode==0 and r.stderr==b'',label+' successful complete execution')
 return r.stdout,row
def git(label,*args):return run(label,['git',*args])[0]
def api(label,path):return json.loads(run(label,['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+path])[0])
def bound(p,row,label):
 b=p.read_bytes();check(len(b)==row['bytes'] and sha(b)==row['sha256'],label+' entire bound file');return b
def manifest(p):
 m=load(p);names=[]
 for row in m['files']:
  target=p.parent/row['path'];check(target.resolve().is_relative_to(p.parent.resolve()),'confined '+row['path'])
  bound(target,row,str(p.relative_to(A))+':'+row['path']);names.append(row['path'])
 check(len(names)==len(set(names)),str(p.relative_to(A))+' unique scope');return m
pins=load(A/'LIVE_ACCEPTANCE_PINS.json');head=pins['head'];base=pins['base']
body=Path(pins['body_file']).read_bytes()
check(len(body)==pins['body_bytes'] and sha(body)==pins['body_sha256'],'literal accepted body')
clearance=Path(pins['clearance_file']);check(sha(clearance.read_bytes())==pins['clearance_sha256'] and load(clearance)==pins['clearance_complete_object'],'entire literal clearance')
check(load(clearance)['second_review_mandatory_findings']==0,'second fresh review clear')
for row in load(clearance)['sealed_submission_files']:bound(A/'preprint'/row['path'],row,'submission '+row['path'])
baseline=load(F/'PREPARATION_BASELINE.json')
for row in baseline['immutable_prior_files']:bound(A/row['path'],row,'prior '+row['path'])
for name in baseline['immutable_prior_manifests']:manifest(A/name)
check(sha(Path(pins['review02_manifest_file']).read_bytes())==pins['review02_manifest_sha256'],'second review literal manifest')
manifest(Path(pins['review02_manifest_file']))
live=load(F/'receipts/FINAL_LIVE_RECEIPT.json')
check(live['status']=='QUALIFIED_EXACT_LIVE_ACCEPTANCE_PASS' and live['head']==head and live['base']==base,'complete gate literal head/base')
allchecks=load(F/'receipts/CHECKS.json');check(len(allchecks)==live['checks'] and all(r['pass'] is True for r in allchecks),'every agent final check')
manifest(F/'PUBLIC_MANIFEST.json')
for row in load(F/'FINAL_SEAL.json')['sealed_artifacts']:bound(F/row['path'],row,'final seal '+row['path'])
check(git('branch','branch','--show-current')==b'main\n','main branch')
check(git('local_head','rev-parse','HEAD').decode().strip()==base,'literal local main')
def validate_pr(pr,main,merge):
 check(pr['state']=='open' and not pr['draft'] and not pr['merged'],'open ready PR')
 check(pr['head']['sha']==head and pr['base']['sha']==base==main['object']['sha'],'actual head/base/current main')
 check(pr['body'].encode()==body,'entire actual accepted body')
 check(pr['mergeable'] is True and pr['mergeable_state']=='clean','actual clean merge')
 check(pr['base']['ref']=='main' and pr['base']['repo']['full_name']==pr['head']['repo']['full_name']=='AlecKriebel/Math','actual repositories')
 check([r['sha'] for r in merge['parents']]==[base,head] and merge['sha']==pr['merge_commit_sha'],'actual test-merge parent pair')
 check(merge['tree']['sha']==live['testmerge_tree'],'actual test-merge tree')
pr=api('start_pr','pulls/367');main=api('start_main','git/ref/heads/main');merge=api('start_merge','git/commits/'+pr['merge_commit_sha']);validate_pr(pr,main,merge)
original=load(A/'snapshot_manifest.json');expected={r['path'] for r in original['files']}
check(set(git('delta','diff','--name-only',base,head).decode().splitlines())==expected,'entire44 path scope')
rows=api('files','pulls/367/files?per_page=100&page=1');check(api('files_end','pulls/367/files?per_page=100&page=2')==[],'complete API pagination')
check({r['filename'] for r in rows}==expected and len(rows)==44,'entire API44 scope');by={r['filename']:r for r in rows};raw={}
for i,row in enumerate(original['files']):
 p=row['path'];b=git('blob'+str(i),'show',head+':'+p);raw[p]=b
 mode,kind,oid,_=git('mode'+str(i),'ls-tree',head,'--',p).decode().split(None,3)
 check(mode=='100644' and kind=='blob' and by[p]['sha']==oid,'actual mode/blob '+p)
 api_blob=api('api_blob'+str(i),'git/blobs/'+oid)
 check(base64.b64decode(api_blob['content'])==b and api_blob['size']==len(b),'entire API/Git byte equality '+p)
 if p!=QUEUE:check(b==(A/'snapshot'/p).read_bytes() and len(b)==row['bytes'] and sha(b)==row['sha256'] and by[p]['status']=='added','entire original math bytes '+p)
 else:check(by[p]['status']=='modified','queue mode/status')
before=git('base_queue','show',base+':'+QUEUE);after=raw[QUEUE]
lines=before.splitlines(keepends=True);newlines=after.splitlines(keepends=True)
check(len(lines)==len(newlines) and [i+1 for i,(x,y) in enumerate(zip(lines,newlines)) if x!=y]==[400],'exact queue physical scope')
cells=lines[399].split(b'|');check(b'11000151 / AMR-109-0151' in cells[2] and cells[8:10]==[b' queued ',b' 0/5 '],'original own queue cells')
cells[8:10]=[b' claimed_solved ',b' 4/5 '];changed=list(lines);changed[399]=b'|'.join(cells);check(after==b''.join(changed),'all queue bytes only own cells8/9')
orig=load(A/'root_original_reproduction_receipt.json')
for row in orig['nested_bindings']:
 p=str(Path(PREFIX)/Path(row['manifest']).parent/row['path']);b=raw[p]
 check(len(b)==row['bytes'] and sha(b)==row['sha256'],'full manifest-parent binding '+p)
check(len(orig['nested_bindings'])==106,'all106 nested bindings')
for i,old in enumerate(orig['all4_actual_author_checkpoint_API_records']):check(api('author'+str(i),'git/commits/'+old['sha'])==old,'entire author commit object '+old['sha'])
with zipfile.ZipFile(A/'preprint/wajnryb-artin-a5-verification.zip') as z:
 names=z.namelist();check(len(names)==len(set(names))==60,'exact60 ZIP members')
 members={name:z.read(name) for name in names}
 for name,b in members.items():check(b==(A/'preprint'/name).read_bytes(),'entire ZIP/local member '+name)
manifest(V/'MANIFEST.json')
records=gzip.decompress((V/'certificates/30_action_records.txt.gz').read_bytes())
plain=b'{"status":"PASS","reachable_states":234368,"outgoing_edges":711342,"coaccessible_states":90921,"coaccessible_edges":261810}\n'
check(len(records.splitlines())==90921,'entire90921 state count')
pub=b'PASS: all frozen public bytes, four Python receipts, C++ full stream, and independent review controls\n'
pkg=b'PASS: complete package, all810 actions, all90921 records, author and both independent backward full replays\n'
def math_output(label,out,begin,end):
 label=label.removeprefix('with_sources_')
 if label.startswith('original_turn'):
  n=label[len('original_turn'):];expected=(V/f'reference/TURN_{n}_CHECKS.json').read_bytes()
 elif label=='cpp_wrapper':expected=(V/'reference/TURN_4_CPP_CHECKS.json').read_bytes()
 elif label=='review_control':expected=(V/'reference/review/INDEPENDENT_CHECKS.json').read_bytes()
 elif label=='author_replay':expected=(V/'reference/review/AUTHOR_REPLAY.json').read_bytes()
 elif label=='original_publication':expected=pub
 elif label=='compile_cpp':expected=b''
 elif label=='cpp_plain':expected=plain
 elif label=='cpp_full':expected=records+plain
 elif label=='full_closed_package':expected=pkg
 elif label=='packaged_independent20_30':
  o=json.loads(out);reference=load(V/'independent_expected.json');stamp=o['utc']
  check(datetime.fromisoformat(begin)<=datetime.fromisoformat(stamp)<=datetime.fromisoformat(end),'independent20/30 current UTC in actual command')
  check(out.count(stamp.encode())==1,'independent20/30 only one UTC');out=out.replace(stamp.encode(),reference['utc'].encode(),1);expected=(V/'independent_expected.json').read_bytes()
 elif label=='packaged_independent_ranks':
  text=out.decode();dec=json.JSONDecoder();values=[]
  while text.strip():o,idx=dec.raw_decode(text.lstrip());values.append(o);text=text.lstrip()[idx:]
  reference=load(V/'independent_ranks_expected.json');check(len(values)==7 and values[:6]==reference['ranks'],'all six exact independent rank objects')
  stamp=values[-1]['utc'];check(datetime.fromisoformat(begin)<=datetime.fromisoformat(stamp)<=datetime.fromisoformat(end),'independent ranks current UTC in actual command')
  check(out.count(stamp.encode())==1,'independent ranks only one UTC');out=out.replace(stamp.encode(),reference['utc'].encode(),1)
  expected=b''.join((json.dumps(r)+'\n').encode() for r in reference['ranks'])+(V/'independent_ranks_expected.json').read_bytes()
 else:raise AssertionError('Unclassified full mathematical output '+label)
 check(out==expected,'complete byte-exact mathematical stdout '+label)
def child_outputs(path):
 rows=[json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()];check(len(rows)==11,'all11 complete package children '+str(path.name))
 for row in rows:
  check(row['returncode']==0 and base64.b64decode(row['stderr_b64'],validate=True)==b'','child success/full empty stderr')
  args=row['args'];name=Path(args[-1]).name
  if args[0]=='g++':label='compile_cpp'
  elif args[-1]=='--stream':label='cpp_full'
  elif name.startswith('check_turn_'):label='original_turn'+name[len('check_turn_'):-3]
  else:label={'verify_turn_4_cpp.py':'cpp_wrapper','independent_check.py':'review_control','verify_publication.py':'original_publication','independent_20_30.py':'packaged_independent20_30','independent_ranks1_6.py':'packaged_independent_ranks'}[name]
  math_output(label,base64.b64decode(row['stdout_b64'],validate=True),row['started_utc'],row['finished_utc'])
 return rows
captures=load(F/'receipts/EXECUTIONS.json');source_rows=load(F/'receipts/FRESH_SOURCES_POSTGATES.json')
math_labels=[]
for capture in captures:
 label=capture['label'];out=None
 for channel in ('stdout','stderr'):
  row=capture[channel];stored=(F/row['path']).read_bytes();b=gzip.decompress(stored)
  check(len(stored)==row['stored_bytes'] and sha(stored)==row['stored_sha256'] and len(b)==row['bytes'] and sha(b)==row['sha256'],'whole actual retained '+label+' '+channel)
  (R/('agent_'+label+'.'+channel+'.gz')).write_bytes(stored)
  if channel=='stderr':check(b==b'','complete empty agent stderr '+label)
  else:out=b
 check(capture['exit_code']==0,'successful retained agent command '+label)
 if label.startswith('git_'):
  args=capture['command'];check(args[0]=='git' and args[1] in {'show','ls-tree','rev-parse','branch','diff','merge-base','rev-list'},'read-only Git capture command')
  current,_=run('replay_'+label,args);check(current==out,'entire current Git stdout '+label)
 elif label.startswith('api_'):
  args=capture['command'];check(args[:4]==['gh','api','--method','GET'],'read-only actual API command')
  current,_=run('replay_'+label,args);check(json.loads(current)==json.loads(out),'entire current actual API object '+label)
 elif label.startswith('fresh_source_'):
  matching=[r for r in source_rows if 'url' in r and r['url']==capture['command'][-1]];check(len(matching)==1,'fresh full source identity '+label)
  check(len(out)==matching[0]['bytes'] and sha(out)==matching[0]['sha256'],'entire fresh primary source '+label)
 elif label in ('start_original_closed_audit','end_original_closed_audit'):
  check(out==b'PASS: complete self-excluded public audit, earlier/final seals and44 raw execution-output streams\n','entire original audit verifier '+label)
 else:math_output(label,out,capture['started_utc'],capture['finished_utc']);math_labels.append(label)
for rank in range(1,7):
 expected=records if rank==6 else gzip.decompress((V/f'certificates/rank{rank}_action_records.txt.gz').read_bytes())
 check(gzip.decompress((F/f'fullstreams/rank{rank}_records.txt.gz').read_bytes())==expected,'every full rank'+str(rank)+' record byte')
check(gzip.decompress((F/'fullstreams/independent20_30_records.txt.gz').read_bytes())==records,'every independent20/30 state record')
check(gzip.decompress((F/'fullstreams/all810_actions.jsonl.gz').read_bytes())==gzip.decompress((V/'certificates/20_full_actions.jsonl.gz').read_bytes()),'every810 labeled F4 action')
agent_children=child_outputs(F/'fullstreams/package_child_outputs.jsonl.gz')
for label in ('body','head','base','draft','queue','target_bytes','package_binding','merge_tree'):
 b=(F/f'fullstreams/negative_{label}.txt').read_bytes();check(b.startswith(b'Traceback (most recent call last):\n') and b'AssertionError' in b,'entire retained expected negative failure '+label)
# New serial complete package replay; every full child output is retained.
wrapper=R/'retain_children.py'
wrapper.write_bytes((F/'retain_package_children.py').read_bytes())
with tempfile.TemporaryDirectory(prefix='root367_exact_',dir=A/'preprint/private_qa') as tmp:
 work=Path(tmp)
 for name,b in members.items():p=work/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 fresh,row=run('fresh_package',[PY,'-B',wrapper,work/'verification/verify_package.py',R/'root_package_children.jsonl.gz'],work)
 check(fresh==pkg,'entire fresh root package stdout');root_children=child_outputs(R/'root_package_children.jsonl.gz')
end=api('end_pr','pulls/367');endmain=api('end_main','git/ref/heads/main');endmerge=api('end_merge','git/commits/'+end['merge_commit_sha']);validate_pr(end,endmain,endmerge)
check(pr==end and main==endmain and merge==endmerge,'entire root start/end actual metadata unchanged')
for row in load(clearance)['sealed_submission_files']:bound(A/'preprint'/row['path'],row,'end submission '+row['path'])
result={'status':'PASS_COMPLETE_ROOT_EXACT_LIVE_AND_ALL_OUTPUTS','utc':utc(),'head':head,'base':base,'body_sha256':sha(body),'all44_actual_paths_verified':44,'all43_original_math_files_unchanged':43,'all106_manifest_parent_bindings_verified':106,'queue_line':400,'only_changed_queue_cells':[8,9],'all_other_queue_bytes_preserved':True,'agent_complete_capture_count':len(captures),'all_agent_full_outputs_compared':True,'fresh_root_complete_package_replay':True,'fresh_root_and_agent_all11_child_math_outputs_compared':True,'all6_complete_rank_records_and810_actions_compared':True,'agent_live_manifest_sha256':sha((F/'PUBLIC_MANIFEST.json').read_bytes()),'all_checks':CHECKS,'check_count':len(CHECKS),'complete_root_captures':CAPTURES,'workflow_completion_percent':93,'actual_merge_pending':True}
(A/'root_exact_live_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'all_checks','complete_root_captures'}},indent=2))
