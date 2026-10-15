"""Reproduce complete frozen streams, actual Git objects and all checkpoint bindings."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent; S=A/'snapshot'
M=json.loads((A/'snapshot_manifest.json').read_text()); T=M['target_prefix']; P=S/T
H=M['head'];B=M['base'];WIP='e27668a5dd99e38705ec6a97d15710b7eb1b0f41'
W=A/'tmp/root_original_packet'; assert not W.exists(); W.mkdir(parents=True)
OUT=A/'root_original_streams';OUT.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a])
assert git('show','-s','--format=%P',H).decode().strip().split()==[WIP,B]
assert set(git('diff','--name-only',B,H).decode().splitlines())=={e['path'] for e in M['files']}
for e in M['files']:
 b=(S/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']
 assert git('show',H+':'+e['path'])==b
assert len(M['files'])==46 and len([e for e in M['files'] if e['path'].startswith(T+'/')])==45
shutil.copytree(P,W/'current')
nested=[]
for f in sorted(P.rglob('*MANIFEST.json')):
 obj=json.loads(f.read_text())
 for e in obj.get('files',[]):
  b=(f.parent/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 nested.append({'path':str(f.relative_to(P)),'entries':len(obj.get('files',[])),'sha256':sha(f.read_bytes())})
fm=json.loads((P/'FINAL_AUTHOR_MANIFEST.json').read_text())
author=[e['path'] for e in fm['files']]+['FINAL_AUTHOR_MANIFEST.json'];assert len(author)==36
assert set(author)==set(json.loads((P/'FINAL_PUBLIC_SCOPE.json').read_text())['files'])
for name in author:
 b=(P/name).read_bytes();assert git('show',WIP+':'+T+'/'+name)==b
 q=W/'author'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
chain=['4b3af41c5eb68f29409ca55f5784ed6291552f38','f6844b255c7699ee0448839dd2355415e8b56877','57da028a10b5a910bd3c2ff5c426b487bbcde9a5','ffaf72634b53e1ffda5160adb2b2e57b69b109a3',WIP]
hist=[];total=0
for i,c in enumerate(chain,1):
 name=f'TURN_{i}_MANIFEST.json';obj=json.loads((P/name).read_text());assert obj['turn']==i
 assert git('show',c+':'+T+'/'+name)==(P/name).read_bytes()
 for e in obj['files']:assert git('show',c+':'+T+'/'+e['path'])==(P/e['path']).read_bytes()
 if i>1:
  assert obj['previous_manifest_sha256']==sha((P/f'TURN_{i-1}_MANIFEST.json').read_bytes())
  assert subprocess.run(['git','merge-base','--is-ancestor',chain[i-2],c]).returncode==0
 state=json.loads((P/f'TURN_{i}_STATE.json').read_text());checks=json.loads((P/f'TURN_{i}_CHECKS.json').read_text());total+=checks['assertions']
 assert state['author_turns_completed']==i and state['original_disposition'] in ['unresolved','unsolved']
 hist.append({'turn':i,'commit':c,'manifest_entries':len(obj['files']),'cumulative_author_assertions':total,'stored_state':state})
assert total==93505
fresh=json.loads((A/'root_primary_source_receipt.json').read_text())['files'];sources=[]
for e in fresh:
 b=(A/'raw_sources'/e['file']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'] and e['pinned_exact']
 sources.append({'file':e['file'],'bytes':len(b),'sha256':sha(b)})
queue='unsolved_math_prioritization/QUEUE.md';before=git('show',B+':'+queue);after=(S/queue).read_bytes()
a=before.splitlines(keepends=True);b=after.splitlines(keepends=True);assert len(a)==len(b)
diff=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];assert len(diff)==1;i=diff[0]
x=a[i].split(b'|');y=b[i].split(b'|');assert x[2].strip().startswith(b'30005116 /')
assert [j for j,(v,w) in enumerate(zip(x,y)) if v!=w]==[8,9]
assert [x[j].strip() for j in [8,9]]==[b'queued',b'0/5'] and [y[j].strip() for j in [8,9]]==[b'unsolved',b'5/5']
jobs=[(f'turn{j}',[sys.executable,'-B',str(W/'current'/f'verify_turn{j}.py')],P/f'TURN_{j}_CHECKS.json') for j in range(1,6)]
jobs += [('frozen_author_replay',[sys.executable,'-B',str(W/'current/independent_review/replay_author.py'),str(W/'author')],P/'independent_review/AUTHOR_REPLAY.json'),('historical_independent',[sys.executable,'-B',str(W/'current/independent_review/independent_check.py')],P/'independent_review/INDEPENDENT_CHECKS.json'),('publication',[sys.executable,'-B',str(W/'current/verify_publication.py')],None)]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(job):
 label,cmd,expected=job;r=subprocess.run(cmd,cwd=W/'current',env=env,capture_output=True)
 (OUT/(label+'.stdout')).write_bytes(r.stdout);(OUT/(label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(label,r.returncode,r.stderr.decode())
 if expected:assert r.stdout==expected.read_bytes(),label
 else:assert r.stdout==b'PASS: immutable publication hashes, exact author replay and independent SymPy-backed replay\n'
 print(label+': PASS',flush=True)
 return {'label':label,'exit':0,'stderr_empty':True,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'entire_stdout_byte_exact':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:programs=list(pool.map(run,jobs))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ORIGINAL_HEAD','workflow_percent':60,'original_resolution_percent':0,'frozen_head':H,'original_base':B,'WIP':WIP,'all_actual_git_paths':46,'target_paths':45,'immutable_author_paths':36,'immutable_old_review_paths':6,'nested_manifest_binding_occurrences':sum(e['entries'] for e in nested),'nested_manifests':nested,'all_five_history_checkpoints':hist,'fresh_pinned_primary_PDFs':sources,'historical_other_source_formats_not_byte_reproduced':True,'original_queue_physical_line':i+1,'original_queue_only_cells':[8,9],'all_other_queue_bytes_exact':True,'programs':programs,'author_assertions':total,'historical_independent_assertions':1080,'claimed_solved':False,'novelty_certified':False,'fresh_actual_head_acceptance_gate_pending':True}
(A/'root_original_replay_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'paths':46,'target':45,'author_checks':total,'historical_checks':1080,'runs':len(programs)}))
