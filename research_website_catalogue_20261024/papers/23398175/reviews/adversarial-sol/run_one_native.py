"""One direct ordinary native run after full input/code/expected/safety reading."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,stat,os,time,sys
O=Path(__file__).resolve().parent
S=O.parents[1]/'sources'
R=S/'published-source/container-001/tree/k605a_outer_focal_pedal_product/pr_update/5100033'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def snapshot():
 paths=sorted(S.rglob('*'))
 if any(p.is_symlink() or not(p.is_file() or p.is_dir()) for p in paths):raise ValueError('Unexpected source special file')
 return {'files':[{'path':p.relative_to(S).as_posix(),**pin(p)} for p in paths if p.is_file()],'directories':[{'path':p.relative_to(S).as_posix(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')} for p in paths if p.is_dir()]}
def typed(v):
 if isinstance(v,dict):return ['object',[[k,typed(x)] for k,x in v.items()]]
 if isinstance(v,list):return ['array',[typed(x) for x in v]]
 return [type(v).__name__,v]
for name in ['NATIVE_SOURCE_GUARD.json','native.stdout.json','native.stderr','NATIVE_EXECUTION.json']:
 if (O/name).exists():raise SystemExit('Refuse to overwrite native run artifacts')
before=snapshot();(O/'NATIVE_SOURCE_GUARD.json').write_text(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'source_root':str(S),'before':before},indent=2)+'\n')
expected=json.loads((R/'verification.json').read_bytes())['original_result']
old_hash=expected['proof_sha256'];new_hash=pin(R/'PROOF.md')['SHA256'];expected['proof_sha256']=new_hash
start=datetime.now(timezone.utc).isoformat();tick=time.monotonic();env=dict(os.environ);env['PYTHONOPTIMIZE']='0'
with (O/'native.stdout.json').open('wb') as out,(O/'native.stderr').open('wb') as err:
 done=subprocess.run(['/opt/homebrew/bin/python3.11','-B',str(R/'verify.py')],cwd=str(O),env=env,stdout=out,stderr=err)
end=datetime.now(timezone.utc).isoformat();after=snapshot();same=before==after
parse_error=None;match=False
try:
 actual=json.loads((O/'native.stdout.json').read_bytes());match=typed(actual)==typed(expected)
except Exception as e:parse_error=str(e)
receipt={'UTC_start':start,'UTC_end':end,'seconds':time.monotonic()-tick,'command':['/opt/homebrew/bin/python3.11','-B',str(R/'verify.py')],'cwd':str(O),'invocations':1,'exit_code':done.returncode,'native_script':pin(R/'verify.py'),'PROOF':pin(R/'PROOF.md'),'historical_expected_record':pin(R/'verification.json'),'stdout':pin(O/'native.stdout.json'),'stderr':pin(O/'native.stderr'),'source_files':len(before['files']),'source_child_directories':len(before['directories']),'full_finite_source_unchanged':same,'scientific_expected_comparison_exact':match,'expected_PROOF_binding_only':{'historical_original_hash':old_hash,'actual_current_adjacent_hash':new_hash,'justification':'Explicit current_note in actual historical wrapper; no scientific fields discarded'},'parse_error':parse_error,'optimization':0,'optimized_duplicate_runs':0,'harness_or_oldhelper_runs':0,'new_native_proof_or_interval_claim':False}
(O/'NATIVE_EXECUTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
raise SystemExit(0 if done.returncode==0 and same and match and (O/'native.stderr').stat().st_size==0 else 1)
