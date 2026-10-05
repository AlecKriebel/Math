#!/usr/bin/env python3
"""Precisely authorize, then externally capture one reviewed family closure.

Only the explicitly reviewed additions in each family's closure plan are
permitted. All original namespace files, common source files, and modes must
remain equal to the root's complete independently captured preclosure state.
"""
import argparse, datetime, hashlib, json, pathlib, stat, subprocess, sys
A=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('/Users/alec/Documents/Math')
ENV={'PATH':'/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin','LANG':'C','LC_ALL':'C','TZ':'UTC','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
def inv(base):
    result={}
    for p in sorted(base.rglob('*')):
        if p.is_symlink(): raise RuntimeError('Unexpected symlink')
        if p.is_file(): result[p.relative_to(base).as_posix()]=pin(p)
    return result
def save(p,x):
    with p.open('x') as f: f.write(json.dumps(x,indent=2)+'\n')
def require(x,s):
    if not x: raise RuntimeError(s)
ap=argparse.ArgumentParser()
ap.add_argument('family',choices=['honda_lifting','intrinsic_invariants'])
ap.add_argument('--prepare-authorization',action='store_true')
ap.add_argument('--close',action='store_true')
args=ap.parse_args()
require(args.prepare_authorization != args.close,'Choose exactly one operation')
N=A/args.family
CAP=A/'root_family_capture_private'/args.family/'preclosure001'
pre=json.loads((CAP/'whole_before.json').read_text())
root_receipt=json.loads((CAP/'ROOT_RECEIPT.json').read_text())
require(root_receipt['status']=='PASS_ROOT_EXTERNAL_READONLY_COMPLETE_FAMILY_REPRODUCTION','Root preclosure not passed')
require(inv(N)==pre['namespace'],'Reviewed complete namespace changed before closure')
require(inv(A/'snapshot')==pre['common']['snapshot'] and inv(A/'root_sources_private')==pre['common']['primary_sources'],'Common input changed before closure')
authorization_path=A/('ROOT_'+args.family.upper()+'_CLOSURE_AUTHORIZATION.json')
if args.family=='honda_lifting':
    manifest_name='AUDIT_MANIFEST.json'; plan_name='CLOSURE_PLAN.md'; seal_name='SEAL.json'
    additions=['SEAL.json','closure/metadata.json','closure/script_stderr.txt','closure/script_stdout.txt','closure/verifier_stderr.txt','closure/verifier_stdout.txt']
    require(pin(N/'seal_once.py')['sha256']=='62b372f08e6e6e05c98b1e5001e7cc9026585696691d4afdb37a85c9b38cf716','Reviewed Honda sealer changed')
else:
    manifest_name='audit_manifest.json'; plan_name='closure_plan.md'; seal_name='seal.json'; additions=['seal.json']
require(not (N/seal_name).exists(),'Already sealed; no retry')
token='ROOT_PR344_'+args.family.upper()+'_ONCE_AFTER_FULL_REVIEW_20261004'
if args.prepare_authorization:
    auth={'utc':now(),'authorized':True,'one_time_only':True,'family':args.family,'authorization_text':token,'candidate_head':'86a758b1cc9c94322ce6afc3d17150fa2c90327a','manifest':pin(N/manifest_name),'closure_plan':pin(N/plan_name),'root_full_preclosure_receipt':pin(CAP/'ROOT_RECEIPT.json'),'root_whole_preclosure':pin(CAP/'whole_before.json'),'root_closure_program':pin(pathlib.Path(__file__)),'allowed_final_additions':additions,'pre_existing_file_changes_allowed':False,'writes_after_seal_allowed':False,'review_adjudication':'Complete source-first gates, first candidate assessment, mathematical report, proof, all program code, complete manifest, native receipts/full mathematical streams and retained failed-version differences reviewed. Actual independent root native controls/private verification passed with whole before/after body and mode equality. No mathematical gap remains in this family; priority and preprint acceptance remain separate pending gates.','limitations':'Public algebra controls are finite corroboration; primary finite-Honda/Dieudonne theorems are cited inputs. Private source and original host provenance are not public-package prerequisites.'}
    save(authorization_path,auth)
    print(json.dumps({'authorization':str(authorization_path),'sha256':pin(authorization_path)['sha256'],'token':token},indent=2))
    sys.exit(0)
auth=json.loads(authorization_path.read_text())
require(auth['authorized'] and auth['authorization_text']==token and auth['root_closure_program']==pin(pathlib.Path(__file__)),'Wrong authorization or closure program')
require(auth['manifest']==pin(N/manifest_name) and auth['closure_plan']==pin(N/plan_name),'Approval input changed')
OUT=A/'root_family_capture_private'/args.family/'closure001'
require(not OUT.exists(),'Closure capture already exists; no retry')
OUT.mkdir()
save(OUT/'PREEXECUTION.json',{'utc':now(),'authorization':pin(authorization_path),'whole_namespace_before':pre['namespace'],'environment_exact':ENV,'closure_program':pin(pathlib.Path(__file__)),'parent_interpreter':sys.executable,'parent_version':sys.version})
if args.family=='honda_lifting':
    argv=['/opt/homebrew/bin/python3','-B',str(N/'seal_once.py'),'--workspace',str(ROOT),'--authorization',token]
    start=now()
    process=subprocess.run(argv,cwd=N,env=ENV,capture_output=True)
    (OUT/'native.stdout').write_bytes(process.stdout)
    (OUT/'native.stderr').write_bytes(process.stderr)
    save(OUT/'NATIVE_EXECUTION.json',{'started_utc':start,'completed_utc':now(),'argv':argv,'cwd':str(N),'environment_exact':ENV,'exit_status':process.returncode,'stdout':pin(OUT/'native.stdout'),'stderr':pin(OUT/'native.stderr'),'stdout_text':process.stdout.decode(),'stderr_text':process.stderr.decode(),'authorization':pin(authorization_path)})
    require(process.returncode==0 and process.stderr==b'','Honda native closure failed; inspect capture and do not retry')
    require(process.stdout==(N/'closure/script_stdout.txt').read_bytes() and process.stderr==(N/'closure/script_stderr.txt').read_bytes(),'Actual outer closure streams differ from stored internal streams')
    seal=json.loads((N/seal_name).read_text())
    metadata=json.loads((N/'closure/metadata.json').read_text())
    require(metadata['authorization']==token and metadata['exit_code']==0 and metadata['unchanged_inputs'] and metadata['input_before']==metadata['input_after'],'Honda verifier actual child result invalid')
    require(seal['authorization']==token and seal['manifest_sha256']==pin(N/manifest_name)['sha256'],'Honda seal binding invalid')
else:
    seal={'status':'sealed','sealed_utc':now(),'parent_approval':auth,'parent_approval_path':str(authorization_path),'parent_approval_sha256':pin(authorization_path)['sha256'],'manifest_sha256':pin(N/manifest_name)['sha256'],'candidate_head':auth['candidate_head'],'source_gate_sha256':pin(N/'exposure_gate.md')['sha256'],'first_assessment_sha256':pin(N/'first_candidate_assessment.md')['sha256'],'family_completion_estimate_percent':100,'writes_after_seal':'forbidden','closure_kind':'Parent-authorized final metadata addition after genuine externally captured mathematical/private verification; this metadata does not claim to be a native process-exit receipt.'}
    save(N/seal_name,seal)
after=inv(N)
require(set(after)-set(pre['namespace'])==set(additions),'Unexpected closing additions')
require(all(after[k]==v for k,v in pre['namespace'].items()),'Original reviewed file body/mode changed at closure')
require(inv(A/'snapshot')==pre['common']['snapshot'] and inv(A/'root_sources_private')==pre['common']['primary_sources'],'Common input changed at closure')
receipt={'utc':now(),'status':'PASS_EXACT_ONE_TIME_REVIEWED_FAMILY_CLOSURE','family':args.family,'namespace_file_count':len(after),'prior_file_count':len(pre['namespace']),'permitted_additions':{k:after[k] for k in additions},'all_pre_existing_bodies_modes_unchanged':True,'common_sources_snapshot_unchanged':True,'authorization':pin(authorization_path),'whole_namespace_after':after,'family_completion_estimate_percent':100,'priority_complete':False,'preprint_approved':False}
save(OUT/'ROOT_CLOSURE_RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='whole_namespace_after'},indent=2))
