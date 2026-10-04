"""Independently verify every family artifact and replay every complete capture."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'snapshot/unsolved_math_prioritization/attempts/2303016';PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
S=A/'root_family_streams';S.mkdir(exist_ok=True);checks=[];sha=lambda b:hashlib.sha256(b).hexdigest();replays=[];families=[]
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def bind(root,e):
 q=PurePosixPath(e['path']);ck(not q.is_absolute() and '..' not in q.parts and q.as_posix()==e['path'],'safe path '+e['path']);p=root/q;ck(p.is_file() and not p.is_symlink(),'regular '+e['path']);b=p.read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'whole binding '+str(p));return b
def capture(label,args,cwd,expected=None):
 r=subprocess.run(args,cwd=cwd,capture_output=True)
 for stream,b in [('stdout',r.stdout),('stderr',r.stderr)]:(S/(label+'.'+stream)).write_bytes(b)
 ck(r.returncode==0 and not r.stderr,'complete replay exit '+label)
 if expected is not None:ck(r.stdout==expected,'every output byte '+label)
 replays.append({'label':label,'args':[str(a) for a in args],'cwd':str(cwd),'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)})
 return r.stdout
for family,mfn,count,pin,ignore in [('priority_method_review','REVIEW_MANIFEST.json',8,'c37d071fcafdb11d26332a185676a381b2af8746e9855669075c98ec1e0d646d',{'private_replays','private_sources','replays','__pycache__'}),('variational_capacity_review','IMMUTABLE_MANIFEST.json',26,'aa86e6f71ddeb7ea73ac13729035cbe0bb846a5aac7d12a9b6200e4ed97d2358',{'private'})]:
 F=A/family;raw=(F/mfn).read_bytes();ck(sha(raw)==pin,'literal sealed manifest '+family);m=json.loads(raw);names={e['path'] for e in m['files']};ck(len(names)==len(m['files'])==count,'closed manifest count '+family)
 actual={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file() and not set(p.relative_to(F).parts)&ignore and p.name not in {mfn,'FINAL_SEAL.json'}};ck(actual==names,'exact public enumeration '+family)
 for e in m['files']:bind(F,e)
 families.append({'family':family,'manifest':mfn,'sha256':pin,'bound_public_files':count})
 if family=='priority_method_review':
  for e in m['candidate_files']:bind(D,e)
  for e in m['replay_records']:bind(F,e)
  bs=json.loads((F/'BASELINE_SEAL.json').read_bytes())
  for e in bs['files']:ck(sha((F/e['path']).read_bytes())==e['sha256'],'pre-candidate baseline '+e['path'])
  for e in bs['primary_pdfs']:ck(sha((F/e['private_path']).read_bytes())==e['sha256'],'method whole primary '+e['private_path'])
  for label,expected in [('author',D/'TURN_1_CHECKS.json'),('historical',D/'final_review/CHECKS.json')]:
   b=(F/'private_replays'/(label+'.stdout')).read_bytes();ck(b==expected.read_bytes(),'historical full output '+label);ck((F/'private_replays'/(label+'.stderr')).read_bytes()==b'' and (F/'private_replays'/(label+'.exit')).read_text().strip()=='0','historical exits '+label)
  capture('method_integrity',[str(PY),str(F/'check_integrity.py')],F,(F/'CHECKS.json').read_bytes())
 else:
  final=json.loads((F/'FINAL_SEAL.json').read_bytes());ck(final['manifest_sha256']==pin and final['mandatory_repairs']==0 and final['family_completion_percent']==100,'final variational seal')
  expected=json.dumps(final['complete_final_verifier_output'],indent=2,sort_keys=True).encode()+b'\n';capture('variational_closed_verifier',[str(PY),str(F/'verify_audit.py')],F,expected)
  r=json.loads((F/'REPRODUCTION.json').read_bytes());ck(r['assertions']==340 and r['complete_manifest_binding_instances']==48 and len(r['commands'])==28,'entire driver scope')
  for i,row in enumerate(r['commands']):
   out=bind(F,row['stdout']);err=bind(F,row['stderr']);ck(row['returncode']==0 and not err,'historical full capture '+row['label']);capture('variational_capture_'+str(i),row['argv'],row['cwd'],out)
  for e in r['all_bindings']:bind(Path(e['manifest']).parent,e)
  ck(r['independent_full_output']['assertions']==823 and len(r['independent_full_output']['negative_controls_rejected'])==7,'823 new and7 negative controls')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ALL_FAMILY_EVIDENCE_AND_EVERY_COMPLETE_CAPTURE','check_count':len(checks),'checks':checks,'families':families,'replays':replays,'all_family_public_bindings':34,'new_math_controls':823,'negative_errors_rejected':7,'full_driver_commands_independently_reexecuted':28,'scope':'Root full analytical/code reading, literal closed manifests, every raw stream and every executable historical capture; immutable family artifacts remain unchanged','program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_family_verification_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','check_count','all_family_public_bindings','new_math_controls','full_driver_commands_independently_reexecuted']},indent=2))
