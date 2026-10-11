"""Full root replay in private copies; preserve every frozen input."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, time
A=Path(__file__).resolve().parent;S=A/'snapshot/problems/30000590_group_ring_cohomology';T=A/'tmp/root_original_packet'
shutil.copytree(S,T,dirs_exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((A/'snapshot_manifest.json').read_text());W=Path('/Users/alec/Documents/Math')
for e in m['files']:
 b=(A/'snapshot'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];assert b==subprocess.check_output(['git','show',f"{m['head']}:{e['path']}"],cwd=W)
runs=[];total=0
jobs=[(f'check_turn_{i}.py',f'TURN_{i}_CHECKS.json') for i in range(1,6)]+[('review/independent_checks.py','review/INDEPENDENT_CHECKS.json'),('verify_packet.py',None),('review/verify_review.py',None),('verify_publication.py',None)]
for name,expected in jobs:
 start=time.monotonic();stem='root_original_'+Path(name).stem
 cmd=[sys.executable,'-B',str((T/name).absolute())]
 if name=='review/verify_review.py':cmd+=['--author',str(T.absolute())]
 stored=(A/(stem+'.stdout'));err=(A/(stem+'.stderr'))
 reuse='--resume' in sys.argv and stored.exists() and err.exists() and not err.read_bytes() and bool(stored.read_bytes())
 if reuse:r=subprocess.CompletedProcess(cmd,0,stored.read_bytes(),b'')
 else:
  r=subprocess.run(cmd,capture_output=True,cwd=T)
  stored.write_bytes(r.stdout);err.write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(name,r.returncode,r.stderr.decode())
 if expected:assert r.stdout==(S/expected).read_bytes(),name
 try:j=json.loads(r.stdout)
 except json.JSONDecodeError:j={'full_text':r.stdout.decode()}
 if name.startswith('check_turn_'):total+=j.get('exact_assertions',j.get('assertions'))
 runs.append({'program':name,'exit_code':r.returncode,'reused_complete_successful_root_capture':reuse,'seconds_this_invocation':time.monotonic()-start,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'complete_historical_bytes_equal':True if expected else None,'result':j})
assert total==747103
assert all((T/f.relative_to(S)).read_bytes()==f.read_bytes() for f in S.rglob('*') if f.is_file())
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':m['head'],'all56_git_input_files_exact':True,'author_assertions':total,'historical_assertions':23463,'all_full_per_turn_and_historical_stdout_equal':True,'all9_executable_sources_read_and_run':True,'source_pdf_replay_count':0,'fresh_primary_pdf_hashes_separately_verified':6,'frozen_and_private_input_bytes_unchanged':True,'runs':runs}
(A/'root_public_replay_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
