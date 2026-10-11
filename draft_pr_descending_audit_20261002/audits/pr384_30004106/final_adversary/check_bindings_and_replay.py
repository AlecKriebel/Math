from pathlib import Path
import hashlib,json,subprocess,shutil,os,datetime,sys
b=Path(__file__).resolve().parent.parent;o=Path(__file__).resolve().parent;root=Path('/Users/alec/Documents/Math');snap=b/'snapshot';head='682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6';base='efd29c05204703acca9a0860812f54b94fae54b1';manifest=json.loads((b/'snapshot_manifest.json').read_text());env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
def sha(x):return hashlib.sha256(x).hexdigest()
status=git('status','--porcelain=v1').decode();main=git('rev-parse','main').decode().strip();branch=git('branch','--show-current').decode().strip();before={'branch':branch,'main':main,'head':git('rev-parse','HEAD').decode().strip(),'status':status,'index_sha256':sha((root/'.git/index').read_bytes())}
checks=[]
for f in manifest['files']:
 raw=(snap/f['path']).read_bytes();blob=git('show',head+':'+f['path'])
 assert len(raw)==f['bytes'] and sha(raw)==f['sha256'] and raw==blob,f['path']
 checks.append({'path':f['path'],'bytes':len(raw),'sha256':sha(raw),'git_blob_sha1':git('rev-parse',head+':'+f['path']).decode().strip(),'match':True})
changed=git('diff','--name-only',base,head).decode().splitlines();assert set(changed)=={f['path'] for f in manifest['files']}
(o/'INPUT_BINDINGS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':head,'base':base,'Git_blob_bindings':checks,'changed_file_set_exact':True,'state_before':before},indent=2)+'\n')
# Fresh private tree. All executable sources had been read before this replay.
private=o/'private_replay';private.mkdir(exist_ok=True)
p=snap/'unsolved_math_prioritization/attempts/30004106'
shutil.copytree(p,private/'30004106',dirs_exist_ok=True);pp=private/'30004106'
records=[]
for n in range(1,6):
 script=pp/f'verify_turn{n}.py';run=subprocess.run([sys.executable,'-B',str(script)],cwd=pp,env=env,capture_output=True)
 (o/f'turn{n}.stdout').write_bytes(run.stdout);(o/f'turn{n}.stderr').write_bytes(run.stderr)
 expected=(p/f'TURN_{n}_CHECKS.json').read_bytes();assert run.returncode==0 and run.stdout==expected and not run.stderr
 records.append({'script':script.name,'exit':run.returncode,'stdout_bytes':len(run.stdout),'stdout_sha256':sha(run.stdout),'full_stdout_equal_frozen':True,'assertions':json.loads(run.stdout)['exact_assertions']})
for name,receipt in [('replay_author.py','AUTHOR_REPLAY.json'),('review/independent_check.py','review/INDEPENDENT_CHECKS.json')]:
 run=subprocess.run([sys.executable,'-B',str(pp/name)],cwd=(pp/name).parent,env=env,capture_output=True)
 (o/(Path(name).stem+'.stdout')).write_bytes(run.stdout);(o/(Path(name).stem+'.stderr')).write_bytes(run.stderr)
 assert run.returncode==0 and run.stdout==(p/receipt).read_bytes() and not run.stderr
 records.append({'script':name,'exit':run.returncode,'stdout_bytes':len(run.stdout),'stdout_sha256':sha(run.stdout),'full_stdout_equal_frozen':True})
run=subprocess.run([sys.executable,'-B',str(pp/'verify_publication.py')],cwd=pp,env=env,capture_output=True)
(o/'verify_publication.stdout').write_bytes(run.stdout);(o/'verify_publication.stderr').write_bytes(run.stderr)
assert run.returncode==0 and not run.stderr
records.append({'script':'verify_publication.py','exit':run.returncode,'stdout_bytes':len(run.stdout),'stdout_sha256':sha(run.stdout),'full_stdout_equal_root_public_replay':run.stdout==(b/'root_public_replay.stdout').read_bytes(),'result':json.loads(run.stdout)})
# Independently inspect the nested manifests, not merely rely on wrapper passing.
nested=[]
for parent,names in [(p,['SOURCE_GATE_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json','PUBLICATION_MANIFEST.json']),(p/'review',['REVIEW_MANIFEST.json'])]:
 for name in names:
  m=json.loads((parent/name).read_text())
  for entry in m['files']:
   raw=(parent/entry['path']).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
   nested.append({'manifest':name,'path':entry['path'],'sha256':sha(raw),'match':True})
(o/'REPLAY_AND_NESTED_BINDINGS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'private_replay':str(pp),'replays':records,'total_author_assertions':sum(x.get('assertions',0) for x in records),'nested_bindings':nested,'nested_entries':len(nested)},indent=2)+'\n')
# Queue comparison: three versions read, only target line extracted; no queue write.
qpath='unsolved_math_prioritization/QUEUE.md'
queues={ref:git('show',ref+':'+qpath).decode() for ref in [base,head,main]}
def line(q):
 hits=[x for x in q.splitlines() if '30004106' in x];assert len(hits)==1,hits;return hits[0]
rows={ref:line(q) for ref,q in queues.items()}
# Preserve all unrelated current-main text: replace ONLY exact base target row.
current=queues[main];proposed=current.replace(rows[base],rows[head]) if rows[base] in current else None
qdelta=git('diff','--unified=0',base,head,'--',qpath).decode();(o/'queue_head_vs_base.diff').write_text(qdelta)
(o/'QUEUE_THREE_WAY.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main':main,'rows':rows,'target_base_row_present_on_current_main':rows[base] in current,'safe_single_row_projection_available':proposed is not None,'unrelated_current_main_bytes_preserved_by_projection':proposed.replace(rows[head],rows[base])==current if proposed is not None else None,'queue_written':False,'note':'Root must dispose PR385 before proceeding with PR384; no merge-ready state issued'},indent=2)+'\n')
# Ensure our operations left Git index/branch and current queue untouched.
after={'branch':git('branch','--show-current').decode().strip(),'main':git('rev-parse','main').decode().strip(),'head':git('rev-parse','HEAD').decode().strip(),'index_sha256':sha((root/'.git/index').read_bytes())}
assert {k:v for k,v in before.items() if k!='status'}==after
(o/'STATE_PRESERVATION.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before':before,'after':after,'Git_index_branch_main_HEAD_unchanged':True,'working_queue_sha256':sha((root/qpath).read_bytes()),'services_mutated':False},indent=2)+'\n')
print(json.dumps({'Git_blobs':len(checks),'nested_manifest_entries':len(nested),'author_assertions':sum(x.get('assertions',0) for x in records),'old_review_assertions':json.loads((o/'independent_check.stdout').read_bytes())['assertions'],'queue_target_base_still_on_main':rows[base] in current,'publication_result':json.loads(run.stdout)},indent=2))
