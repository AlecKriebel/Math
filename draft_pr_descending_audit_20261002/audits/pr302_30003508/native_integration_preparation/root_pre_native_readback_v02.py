"""ROOT full local preparation/publication authentication and read-only native check."""
from pathlib import Path
from datetime import datetime,timezone
import ast,gzip,hashlib,json,os,sqlite3,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';N=Path(__file__).parent;A=N.parent;D=A/'publication_preparation';F=A/'preprint_package_v02'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 p=Path(p);require(p.is_file() and not p.is_symlink(),'literal artifact');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def main():
 require(not sys.flags.optimize,'optimization');source=N/'integrate_pr302.py';plan=load(N/'CONTENT_PLAN.json');sourcepin=pin(source);planpin=pin(N/'CONTENT_PLAN.json')
 require(sourcepin['sha256']=='2dd3f08d52e68aed4b7a66ceea7092681e0f4e05fc5d9c7eb0c1df2757166003' and planpin['sha256']=='baea4aabf70a814f184826433ab0d62b7fc5dc8177cebaa9d80ed5d43fa6f97c' and sourcepin['mode']==planpin['mode']==0o444,'exact frozen concrete source/plan')
 roles=[source,A/'snapshot_manifest.json',A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json',A/'ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json',A/'ROOT_BOUNDED_PRIORITY_GATE_ACCEPTANCE.json',A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json',A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json',F/'SECOND_CANDIDATE_MANIFEST.json',F/'record_metadata.json',F/'spectral_tensor_consistency.pdf',F/'spectral_tensor_verification.zip',D/'REVISED_OPERATOR_MANIFEST.json',*[D/n for n in ['publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py']],N/'SOURCE_IDENTITY_PREPARATION_READBACK.json',N/'KNOWN_HELD_BASELINE.json',*[N/'payloads'/n for n in ['acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md','QUEUE_AFTER.md','PR_BODY.md']],P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py']
 require(len(plan['bound_inputs'])==len(roles)==24 and {x['path'] for x in plan['bound_inputs']}=={str(p) for p in roles},'all24exact nonvacuous input roles')
 for x in plan['bound_inputs']:require(pin(x['path'])==x,'every complete approved input before executable project code')
 # Only manually read, exact source-pinned definitions are now evaluated.
 tree=ast.parse(source.read_bytes());definitions=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['sourcepair','tracker_evidence']];require(len(definitions)==2,'two pure definitions only');env=dict(Path=Path,R=R,A=A,N=N,F=F,D=D,load=load,pin=pin,require=require,sha=sha,json=json,sqlite3=sqlite3)
 exec(compile(ast.fix_missing_locations(ast.Module(body=definitions,type_ignores=[])),str(source)+'::two_verified_readonly_functions','exec'),env);identity=env['sourcepair']()
 sys.path.insert(0,str(D));from publication_guard import clearance,authenticate_execution
 from run_zenodo_step import inspected_publication
 from verify_public_record import verify_public_evidence
 clearance();published=inspected_publication();public=verify_public_evidence(published);tracker=env['tracker_evidence'](load(A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json'),published,authenticate_execution)
 original=load(A/'snapshot_manifest.json');prefix='unsolved_math_prioritization/attempts/30003508';oldfiles=[x for x in original['files'] if x['path'].startswith(prefix+'/')];require(len(oldfiles)==28 and original['head']==plan['original_head']=='eb6e0e999521d84a65f9857d338cad76b84d30db' and original['original_submitted_status']=='claimed_solved' and original['original_author_turn_count']=='2/5','submitted claimed_solved scope/head/budget')
 for x in oldfiles:
  b=(A/'snapshot'/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob_sha'],'all28full originals')
 expected={x['path'] for x in original['files']}|{prefix+'/'+n for n in ['acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md']}|{'unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'};require(len(expected)==34 and set(plan['allowed_paths'])==expected,'exact34native domain')
 before=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();after=(N/'payloads/QUEUE_AFTER.md').read_bytes();row=lambda b:next(x for x in b.splitlines(keepends=True) if b'| 30003508 /' in x);br=row(before);ar=row(after);bc=br.split(b'|');ac=ar.split(b'|');require([i for i in range(14) if bc[i]!=ac[i]]==[8,9,11,12] and before.replace(br,b'',1)==after.replace(ar,b'',1),'four cells and foreign literal QUEUE bytes')
 rows=load(N/'KNOWN_HELD_BASELINE.json')['files'];require(len(rows)==len({x['path'] for x in rows})==41253,'all41253held inventory rows');held=[x for x in rows if str(Path(x['path']).relative_to(R)) not in expected and x['path']!=str(P/'SHARED_GIT_WINDOW_STATUS.json')]
 for x in held:require(pin(x['path'])==x,'all current nonowned held full bodies/modes')
 cap=N/'root_pre_native_readback_actual_v02';cap.mkdir(exist_ok=False)
 def run(label,argv):
  q=cap/label;q.mkdir();request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),source=pin(__file__),automatic_retry=False);(q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'source.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0));proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);started=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(started,indent=2)+'\n');out,err=proc.communicate(timeout=55);streams={}
  for n,b in [('stdout',out),('stderr',err)]:
   z=q/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(z),logical_bytes=len(b),logical_sha256=sha(b))
  (q/'execution.json').write_text(json.dumps(dict(**started,end_UTC=utc(),exit_code=proc.returncode,parent_reaped=True,streams=streams),indent=2)+'\n');require(proc.returncode==0 and not err,'fresh read-only native capture');return out
 require(run('branch',['/usr/bin/git','--no-optional-locks','branch','--show-current'])==b'main\n' and run('head',['/usr/bin/git','--no-optional-locks','rev-parse','HEAD']).decode().strip()==plan['starting_main'],'fresh main')
 require(run('remote',['/usr/bin/git','--no-optional-locks','ls-remote',plan['endpoint'],'refs/heads/main']).split()[0].decode()==plan['starting_main'],'fresh literal remote')
 require(not run('staged',['/usr/bin/git','--no-optional-locks','diff','--cached','--raw','-z']) and not (R/'.git/MERGE_HEAD').exists() and not (R/'.git/index.lock').exists(),'fresh empty index/no merge')
 pr=json.loads(run('PR',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/302']));require(pr['head']['sha']==plan['original_head'] and pr['state']=='open' and pr['draft'] and pr['base']['ref']=='main','fresh genuine original PR identity')
 files=json.loads(run('files',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/302/files?per_page=100']));require(len(files)==29 and {(x['filename'],x['sha']) for x in files}=={(x['path'],x['git_blob_sha']) for x in original['files']},'fresh original API29full domain')
 result=dict(status='PASS_ROOT_FROZEN_NATIVE_PREPARATION_FULL_INPUT_PUBLICATION_TRACKER_AND_FRESH_READBACK',UTC=utc(),actual_ROOT_recorder_PID=os.getpid(),ROOT_source=pin(__file__),source=sourcepin,plan=planpin,full24bound_inputs=plan['bound_inputs'],source_pair=identity,all13complete_actual_service_captures_reauthenticated=True,public_record_and_two_full_files=pin(A/'publication_actual/PUBLIC_RECORD_VERIFICATION.json'),tracker_completion=pin(A/'publication_actual/TRACKER_COMPLETE.json'),original28full_snapshot_bytes_Git_blobs_verified=True,exact34owned_paths=sorted(expected),target_QUEUE_only_four_cells_and_foreign_literal_bytes_verified=True,known_nonowned_held_count=len(held),all_known_nonowned_held_complete_bodies_modes_verified=True,fresh_main_equals_explicit_remote=True,fresh_PR_open_draft_original_head_and29APIblobs=True,no_native_or_service_write=True,execution_authority_granted=False,estimates_percent=dict(PR302_workflow=85,native_preparation_ROOT_check=100))
 p=N/'ROOT_PRE_NATIVE_READBACK_v02.json'
 with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 p.chmod(0o444);print(json.dumps(dict(status=result['status'],actual_ROOT_recorder_PID=os.getpid(),known_nonowned_held_count=len(held),readback=pin(p)),indent=2))
if __name__=='__main__':main()
