"""ROOT complete second-review closure and new-control reproduction.

Capture outside the immutable reviewer namespace. Compare the whole verifier
output with its one declared preseal/postseal status change; all scientific
portable outputs and new controls must be byte-identical.
"""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;B=A/'preprint_review_02'
D=A/'root_replay_private/preprint02_reproduction_001';D.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
load=lambda p:json.loads(p.read_bytes())
assert sha((B/'MANIFEST.json').read_bytes())=='736061529e6a7bdbe8f294c2df6f1585361a90b7507e4f3b04529ab1616c9295'
assert sha((B/'FINAL_SEAL.json').read_bytes())=='aa01174f3c442ff665e9b4511f0a0545b0431b3f2403a1498b64d9cbeb90c2e5'
before={p.relative_to(B).as_posix():sha(p.read_bytes()) for p in B.rglob('*') if p.is_file()}
captures=[]
def run(name,program):
 args=['python3','-B',str(B/program)];start=utc();z=subprocess.run(args,cwd=B,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));end=utc()
 (D/(name+'.stdout')).write_bytes(z.stdout);(D/(name+'.stderr')).write_bytes(z.stderr)
 e={'argv':args,'cwd':str(B),'started_utc':start,'finished_utc':end,'exit_code':z.returncode,'program_sha256':sha((B/program).read_bytes()),'stdout_bytes':len(z.stdout),'stdout_sha256':sha(z.stdout),'stderr_bytes':len(z.stderr),'stderr_sha256':sha(z.stderr),'logical_stream_sha256':sha(b'STDOUT\0'+z.stdout+b'STDERR\0'+z.stderr)}
 (D/(name+'.json')).write_text(json.dumps(e,indent=2)+'\n');captures.append(e)
 assert z.returncode==0 and z.stderr==b'';return z
v=run('closed_verifier','verify_review.py')
preseal=load(B/'private/closure_001/verify.stdout');assert preseal['status']=='PASS_PRESEAL'
preseal['status']='PASS_SEALED';expected=(json.dumps(preseal,indent=2,sort_keys=True)+'\n').encode()
assert v.stdout==expected and json.loads(v.stdout)['mandatory_submission_defects']==0
R=A/'preprint/verification';reads=load(B/'ALL_FILE_READ_RECEIPT.json');instances=[]
for e in reads['manifest_bindings']:
 mf=R/e['manifest'];j=load(mf);items=j.get('files',j.get('public_files'));items=items if isinstance(items,dict) else {x['path']:x for x in items}
 declared=items[e['path']];b=(mf.parent/e['path']).read_bytes()
 assert len(b)==e['bytes']==declared['bytes'] and sha(b)==e['sha256']==declared['sha256']
 instances.append((e['manifest'],e['path']))
assert len(instances)==len(set(instances))==253
z=run('new_controls','independent_controls.py');assert z.stdout==(B/'CONTROLS.json').read_bytes()
assert json.loads(z.stdout)['status']=='PASS' and json.loads(z.stdout)['assertions']==919
assert before=={p.relative_to(B).as_posix():sha(p.read_bytes()) for p in B.rglob('*') if p.is_file()}
seal=load(B/'FINAL_SEAL.json');assert seal['mandatory_submission_defects']==0 and seal['workflow_completion_percent']==100
root={'utc':utc(),'status':'PASS_ROOT_COMPLETE_REVIEW02_READ_AND_CLOSURE','review_manifest_sha256':sha((B/'MANIFEST.json').read_bytes()),'review_seal_sha256':sha((B/'FINAL_SEAL.json').read_bytes()),'mandatory_findings':0,'root_full_substantive_reads':['ANALYTIC_ASSESSMENT.md','FINAL_REPORT.md','PRIORITY_NOTE.md','README.md','independent_controls.py','verify_review.py','private/close_review.py'],'root_direct_declared_distributed_manifest_instances_checked':253,'closed_namespace_files':len(before),'closed_namespace_unchanged':True,'whole_verifier_output_compared':True,'whole_verifier_stdout_identical':False,'only_declared_postseal_mode_difference':True,'typed_mode_difference':{'field':'status','before':'PASS_PRESEAL','after':'PASS_SEALED','all_other_complete_output_bytes_equal':True},'execution':captures[0],'all_submission_files_unchanged':True,'math_percent':100,'preprint_workflow_percent':100,'scope':'Universal proof and priority/provenance limits fully read; direct253 member declaration checks and full closure/new-control outputs reproduced. No true minima/value ordering/global novelty or external human-review certificate.'}
(A/'ROOT_PREPRINT_REVIEW02_VERIFICATION.json').write_text(json.dumps(root,indent=2)+'\n')
control={'utc':utc(),'status':'PASS_ROOT_FULL_REVIEW02_NEW_CONTROL_REPRODUCTION','entire_stdout_identical':True,'closed_review_namespace_unchanged':True,'execution':captures[1],'control_result':json.loads(z.stdout),'program_sha256':sha(Path(__file__).read_bytes()),'scope':'New exact affine feasibility, row dual/average, row splitting, irregular ordinary-graph and invalid-hypothesis finite controls. Universal proof is independent and no invariant minima or priority is calculated.'}
(A/'ROOT_PREPRINT_REVIEW02_CONTROL_REPRODUCTION.json').write_text(json.dumps(control,indent=2)+'\n')
print(json.dumps({'review':root,'new_control':control},indent=2))
