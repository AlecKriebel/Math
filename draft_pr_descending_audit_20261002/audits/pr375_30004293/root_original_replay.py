"""Original Git/history/source bindings and full private executable reproduction."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;S=A/'snapshot';T='unsolved_math_prioritization/attempts/30004293'
P=S/T;W=A/'tmp/root_original_packet';assert not W.exists();W.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a])
m=json.loads((A/'snapshot_manifest.json').read_text());H=m['head'];B=m['base'];WIP='cd4f8dc65cd68c002e2cf85c9df60ce962f33c0d'
assert git('show','-s','--format=%P',H).decode().strip().split()==[B,WIP]
assert set(git('diff','--name-only',B,H).decode().splitlines())=={e['path'] for e in m['files']}
for e in m['files']:
 b=(S/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']
 assert git('show',H+':'+e['path'])==b
assert len(m['files'])==54 and len(list(P.rglob('*')))>53
shutil.copytree(P,W/'current')
nested=[]
for f in sorted(P.rglob('*MANIFEST.json')):
 obj=json.loads(f.read_text())
 for e in obj.get('files',[]):
  b=(f.parent/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 nested.append({'path':str(f.relative_to(P)),'entries':len(obj.get('files',[])),'sha256':sha(f.read_bytes())})
fm=json.loads((P/'FINAL_AUTHOR_MANIFEST.json').read_text());author=[e['path'] for e in fm['files']]+['FINAL_AUTHOR_MANIFEST.json'];assert len(author)==42
for name in author:
 b=(P/name).read_bytes();assert git('show',WIP+':'+T+'/'+name)==b
 q=W/'author'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
raw=json.loads((P/'review/REMOTE_BINDING.json').read_text());assert raw['head']==WIP and len(raw['files'])==42
for e in raw['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['size'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha']
 assert git('rev-parse',WIP+':'+T+'/'+e['path']).decode().strip()==e['sha']
chain=['624b3d15f77ea192eb69f8a0b6d79c484c1237b8','3c8244f53f230138df4393c79c0f6fe86799f137','62b7d113b4bfbf7faf1d0333c8a8a99b3b7d304c','a5377aba029e573d577653330e63619de625fd39',WIP]
hist=[];previous=set();total=0
for turn,c in enumerate(chain,1):
 name=f'TURN_{turn}_MANIFEST.json';obj=json.loads((P/name).read_text());assert obj['author_turns']==turn
 assert git('show',c+':'+T+'/'+name)==(P/name).read_bytes()
 for e in obj['files']:assert git('show',c+':'+T+'/'+e['path'])==(P/e['path']).read_bytes()
 names={e['path'] for e in obj['files']};assert previous<=names;previous=names
 if turn>1:assert subprocess.run(['git','merge-base','--is-ancestor',chain[turn-2],c]).returncode==0
 state=json.loads((P/f'CURRENT_STATE_T{turn}.json').read_text());total+=json.loads((P/f'TURN_{turn}_CHECKS.json').read_text())['exact_assertions']
 assert state['author_turns']==turn and (state.get('total_exact_assertions',state.get('exact_assertions'))==total)
 assert state['complete_quantitative_resolution'] is False
 hist.append({'turn':turn,'commit':c,'manifest_entries':len(obj['files']),'cumulative_author_assertions':total})
sources=[]
for e in json.loads((P/'SOURCE_MANIFEST.json').read_text())['sources']:
 b=(A/'raw_sources'/e['file']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 q=W/'source'/e['file'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);sources.append(e)
queue='unsolved_math_prioritization/QUEUE.md';before=git('show',B+':'+queue);after=(S/queue).read_bytes();a=before.splitlines(keepends=True);b=after.splitlines(keepends=True);assert len(a)==len(b)
diff=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];assert len(diff)==1;i=diff[0];x=a[i].split(b'|');y=b[i].split(b'|');assert x[2].strip().startswith(b'30004293 /') and [j for j,(v,w) in enumerate(zip(x,y)) if v!=w]==[8,9]
assert [x[j].strip() for j in [8,9]]==[b'queued',b'0/5'] and [y[j].strip() for j in [8,9]]==[b'unsolved',b'5/5']
programs=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
jobs=[(f'turn{i}',W/'current'/f'verify_turn{i}.py',P/f'TURN_{i}_CHECKS.json') for i in range(1,6)]
jobs += [('author_frozen_source_bound',W/'author/replay_author.py',P/'AUTHOR_REPLAY.json'),('historical_independent',W/'current/review/independent_checks.py',P/'review/INDEPENDENT_CHECKS.json'),('publication',W/'current/verify_publication.py',None)]
for label,program,expected in jobs:
 r=subprocess.run([sys.executable,'-B',str(program)],cwd=program.parent,env=env,capture_output=True)
 (A/f'root_{label}.stdout').write_bytes(r.stdout);(A/f'root_{label}.stderr').write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(label,r.returncode,r.stderr.decode())
 if expected:assert r.stdout==expected.read_bytes(),label
 if label=='publication':
  objects=[json.loads(line) for line in r.stdout.splitlines()]
  assert objects==[{'author_receipts_byte_exact':True,'frozen_author_files':42,'independent_assertions':8390,'raw_blobs':42,'source_pdfs_checked_by_this_portable_wrapper':False},{'frozen_author_files':42,'frozen_review_files':8,'publication_hashes_verified':52,'source_pdfs_reverified':False}]
 programs.append({'label':label,'program':str(program.relative_to(W)),'exit':0,'stderr_empty':True,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'full_frozen_stream_byte_exact':expected is not None,'full_wrapper_json_exact':label=='publication'})
 print(label+': PASS',flush=True)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ORIGINAL_HEAD','workflow_percent':60,'original_resolution_percent':0,'frozen_head':H,'base':B,'author_WIP':WIP,'all54_actual_Git_bindings':True,'target_files':53,'author_WIP_immutable_files':42,'historical_review_files':8,'nested_manifests':nested,'nested_binding_occurrences':sum(x['entries'] for x in nested),'all_five_history_checkpoints':hist,'fresh_primary_PDFs_bound':sources,'original_queue_physical_line':i+1,'original_queue_only_cells':[8,9],'every_other_original_queue_byte_preserved':True,'programs':programs,'author_assertions':total,'historical_independent_assertions':8390,'source_bound_author_replay':'Original42-file author copy;all5sources;120historical binding occurrences;byteexactAUTHOR_REPLAY','portable_wrapper_PDF_count':0,'claimed_solved':False,'novelty_certified':False,'fresh_final_actual_head_gate_pending':True}
(A/'root_original_replay_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'paths':54,'target':53,'author_checks':total,'historical_checks':8390,'runs':len(programs)}))
