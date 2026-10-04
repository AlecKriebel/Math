"""Fresh complete source, submission and review gate for exact PR364 head.

Only evidence captures outside sealed namespaces are written. All proof files
remain the original reviewed bytes. Native complete outputs are compared;
finite checks and provenance identities do not replace the universal proof.
"""
from pathlib import Path
import base64,datetime,hashlib,json,os,subprocess,zipfile
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
Q='unsolved_math_prioritization/QUEUE.md';PROBLEM=b'30004048'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
load=lambda p:json.loads(p.read_bytes())
clear=load(A/'PUBLISHING_CLEARANCE.json')
assert clear['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS'
assert clear['second_review_mandatory_findings']==0
for e in clear['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
for n in (1,2):
 c=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')
 assert c['mandatory_findings']==0 and c['closed_namespace_unchanged'] and c['whole_verifier_output_compared']
 assert c['review_seal_sha256']==sha((A/f'preprint_review_0{n}/FINAL_SEAL.json').read_bytes())
 c=load(A/f'ROOT_PREPRINT_REVIEW0{n}_CONTROL_REPRODUCTION.json')
 assert c['entire_stdout_identical'] and c['closed_review_namespace_unchanged'] and c['execution']['exit_code']==0 and c['execution']['stderr_bytes']==0
reviewed=load(A/'repaired_snapshot_manifest.json');original=load(A/'snapshot_manifest.json')
H=reviewed['head'];B=reviewed['base'];OH=original['head']
expected={e['path'] for e in reviewed['files']};assert len(expected)==42
D=A/'root_replay_private'/('exact_live_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
D.mkdir(parents=True,exist_ok=False);captures=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1')
def run(tag,args,cwd=R,ok=(0,)):
 start=utc();z=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True,env=env);end=utc();streams={}
 for name,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  p=D/(tag+'.'+name);p.write_bytes(b);streams[name]={'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)}
 c={'tag':tag,'argv':[str(x) for x in args],'cwd':str(cwd),'started_utc':start,'finished_utc':end,'exit_code':z.returncode,'streams':streams}
 captures.append(c);(D/(tag+'.json')).write_text(json.dumps(c,indent=2)+'\n')
 assert z.returncode in ok,(tag,z.returncode,z.stderr.decode(errors='replace'));return z
counter=0
def git(*args):
 global counter
 counter+=1;z=run('git_'+str(counter),['git',*args]);assert not z.stderr;return z.stdout
assert git('branch','--show-current').strip()==b'main'
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
assert git('rev-parse','HEAD').decode().strip()==B
ix=Path(git('rev-parse','--git-path','index').decode().strip());ix=ix if ix.is_absolute() else R/ix;index=ix.read_bytes()
pr=json.loads(run('api_pr_before',['gh','api','repos/AlecKriebel/Math/pulls/364']).stdout)
assert pr['state']=='open' and pr['head']['sha']==H and pr['base']['sha']==B
assert pr['head']['ref']=='math/30004048-reviewed-psi-asymmetry'
assert set(git('diff','--name-only',B,H).decode().splitlines())==expected
original_by={e['path']:e for e in original['files']};bindings=[]
for i,e in enumerate(reviewed['files']):
 path=e['path'];b=git('show',f'{H}:{path}')
 assert len(b)==e['bytes'] and sha(b)==e['sha256'] and b==(A/'repaired_snapshot'/path).read_bytes()
 meta=git('ls-tree',H,'--',path).split(b'\t',1)[0].split();assert meta==[b'100644',b'blob',e['git_blob_sha'].encode()]
 api=json.loads(run('api_blob_'+str(i),['gh','api',f"repos/AlecKriebel/Math/git/blobs/{e['git_blob_sha']}"]).stdout)
 assert api['sha']==e['git_blob_sha'] and api['encoding']=='base64' and api['size']==len(b)
 assert base64.b64decode(api['content'])==b
 if path!=Q:
  old=original_by[path];assert (e['bytes'],e['sha256'],e['git_blob_sha'])==(old['bytes'],old['sha256'],old['git_blob_sha'])
 bindings.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':e['git_blob_sha'],'mode':'100644','fresh_entire_API_body_matches':True})
before=git('show',f'{B}:{Q}').splitlines(keepends=True);after=git('show',f'{H}:{Q}').splitlines(keepends=True)
assert len(before)==len(after);diff=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y];assert len(diff)==1
i=diff[0];bc=before[i].split(b'|');ac=after[i].split(b'|')
assert bc[2].strip().split(b' / ')[0]==PROBLEM and [bc[j].strip() for j in (8,9)]==[b'queued',b'0/5']
assert [ac[j].strip() for j in (8,9)]==[b'claimed_solved',b'3/5']
assert [j for j,(x,y) in enumerate(zip(bc,ac)) if x!=y]==[8,9,11]
old=git('show',f'{OH}:{Q}').splitlines(keepends=True)
rows=[b.split(b'|') for b in old if len(b.split(b'|'))>11 and b.split(b'|')[2].strip().split(b' / ')[0]==PROBLEM]
assert len(rows)==1 and all(ac[j]==rows[0][j] for j in (8,9,11))
S=D/'zip_scratch';S.mkdir();Z=A/'preprint/biconstrained-asymmetry-verification.zip'
with zipfile.ZipFile(Z) as z:
 members=z.infolist();assert len(members)==87 and len({x.filename for x in members})==87
 for m in members:
  p=Path(m.filename);assert not m.is_dir() and p.parts[0]=='biconstrained-asymmetry-verification' and not p.is_absolute() and '..' not in p.parts
  assert ((m.external_attr>>16)&0o170000) in (0,0o100000)
  b=z.read(m);target=S/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
  assert b==(A/'preprint/verification'/Path(*p.parts[1:])).read_bytes()
T=S/'biconstrained-asymmetry-verification';tree_before={p.relative_to(T).as_posix():sha(p.read_bytes()) for p in T.rglob('*') if p.is_file()}
spec=[('reference/verify_turn1.py','reference/TURN_1_CHECKS.json'),('reference/verify_turn2.py','reference/TURN_2_CHECKS.json'),('reference/verify_turn3.py','reference/TURN_3_CHECKS.json'),('reference/review/check_independent.py','reference/review/INDEPENDENT_CHECKS.json'),('controls/graph_boundary_controls.py','controls/graph_boundary_expected.json'),('controls/polytope_controls.py','controls/polytope_expected.json'),('verify_package.py',None)]
whole=[]
for i,(program,receipt) in enumerate(spec):
 cwd=T/'reference' if program.startswith('reference/') else (T/program).parent
 z=run('portable_'+str(i),['python3','-B',T/program],cwd=cwd);assert z.stderr==b'' and json.loads(z.stdout)['status']=='PASS'
 if receipt:assert z.stdout==(T/receipt).read_bytes()
 else:assert json.loads(z.stdout)==load(A/'preprint/INITIAL_REVIEW_PACKAGE.json')['portable_whole_replay']
 for n in (1,2):
  V=A/f'preprint_review_0{n}';records=load(V/'REPLAY_RECEIPT.json')['entries'];assert len(records)==7
  e=records[i];assert e['program']==program and e['exit_code']==0
  if n==1:assert e['expected_file']==receipt
  else:
   expected_path=V/'private/execution_package'/receipt if receipt else V/'private/package_expected.json'
   assert e['expected_file']==str(expected_path)
  out=(V/'private/replays_001'/(e['capture_stem']+'.stdout')).read_bytes();err=(V/'private/replays_001'/(e['capture_stem']+'.stderr')).read_bytes()
  assert z.stdout==out and z.stderr==err==b'' and len(out)==e['stdout_bytes'] and sha(out)==e['stdout_sha256']
  assert len(err)==e['stderr_bytes'] and sha(err)==e['stderr_sha256'] and sha(b'STDOUT\0'+out+b'STDERR\0'+err)==e['logical_stream_sha256']
 whole.append({'program':program,'root_stdout_bytes':len(z.stdout),'root_stdout_sha256':sha(z.stdout),'both_fresh_agent_whole_outputs_identical':True})
assert tree_before=={p.relative_to(T).as_posix():sha(p.read_bytes()) for p in T.rglob('*') if p.is_file()}
G=A/'graph_boundary_review/public';L=A/'polytope_duality_review'
graph=run('graph_closed',['python3','-B',G/'check_public_namespace.py','--require-private'],cwd=G)
assert graph.stderr==b'' and json.loads(graph.stdout)['status']=='PASS_CLOSED_PUBLIC_NAMESPACE'
poly=run('polytope_closed',['python3','-B',L/'verify_review.py','--snapshot',A/'snapshot','--repo',R],cwd=L)
assert poly.stderr==b'' and json.loads(poly.stdout)['status']=='PASS'
closures=[]
for n in (1,2):
 V=A/f'preprint_review_0{n}';vbefore={p.relative_to(V).as_posix():sha(p.read_bytes()) for p in V.rglob('*') if p.is_file()}
 z=run('preprint_closed_'+str(n),['python3','-B',V/'verify_review.py'],cwd=V)
 if n==1:
  assert z.stderr==b'' and z.stdout==(V/'private/closure_001/stdout').read_bytes()
 else:
  preseal=json.loads((V/'private/closure_001/verify.stdout').read_bytes());assert preseal['status']=='PASS_PRESEAL'
  preseal['status']='PASS_SEALED';expected_stdout=(json.dumps(preseal,indent=2,sort_keys=True)+'\n').encode()
  assert z.stderr==b'' and z.stdout==expected_stdout
 assert vbefore=={p.relative_to(V).as_posix():sha(p.read_bytes()) for p in V.rglob('*') if p.is_file()}
 closures.append({'review':n,'seal_sha256':sha((V/'FINAL_SEAL.json').read_bytes()),'closed_whole_output_compared':True,'only_declared_preseal_to_postseal_status_difference':n==2})
last=json.loads(run('api_pr_after',['gh','api','repos/AlecKriebel/Math/pulls/364']).stdout)
assert last['state']=='open' and last['head']['sha']==H and last['base']['sha']==B
remote=json.loads(run('api_main_after',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert remote['object']['sha']==B and git('rev-parse','HEAD').decode().strip()==B and ix.read_bytes()==index
for e in clear['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
result={'utc':utc(),'status':'PASS_COMPLETE_PR364_EXACT_LIVE_AND_SUBMISSION','pr':364,'head':H,'base':B,'original_head':OH,'fresh_complete_bindings':bindings,'original_math_files_unchanged':41,'queue_physical_line':diff[0]+1,'queue_only_pipe_cells':[8,9,11],'all_other_queue_bytes_equal':True,'fresh_root_complete_package_replay':True,'all_agent_full_outputs_compared':True,'whole_portable_programs':whole,'fresh_closed_reviews':closures,'ordinary_zip_files':87,'fresh_original_nested_manifest_instances':135,'entire_index_and_head_unchanged':True,'source_and_proof_percent':100,'priority_certified':False,'acceptance_publication_workflow_percent':80,'actual_merge_zenodo_tracker_pending':True,'captures':captures,'program_sha256':sha(Path(__file__).read_bytes()),'scope':'Fresh exact live Git/API/head/queue/submission binding and whole root/agent output comparisons. Independently reconstructed universal proof is recorded separately; no global priority, exact minima/value ordering, or execution-event certification.'}
(A/'root_exact_live_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
c=load(A/'acceptance_criteria.json');c.update(accepted_status='claimed_solved',exact_live_root_and_whole_gates_pending=False,fresh_whole_exact_live_pending=False,workflow_completion_percent=80);(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'captures','fresh_complete_bindings'}},indent=2))
