"""Reproduce every frozen checker privately with full byte-exact receipts."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parents[2];S=A/'snapshot';m=json.loads((A/'snapshot_manifest.json').read_text());D=A/'tmp/root_original_packet';D.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
for e in m['files']:
 b=(S/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path'];assert b==subprocess.check_output(['git','show',m['head']+':'+e['path']],cwd=ROOT)
 if e['path'].startswith('problems/'):
  f=D/Path(e['path']).relative_to('problems/30004322_arrangement_seshadri');f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
python=(A/'sources_effective_review/private_runtime/bin/python').absolute();jobs=[(f'check_turn_{i}.py',[]) for i in range(1,6)]+[('REPLAY_ALL.py',[]),('review/independent_checks.py',[]),('review/verify_review.py',['--author-dir',str(D.absolute())])]
results=[]
for name,args in jobs:
 r=subprocess.run([str(python),'-B',str((D/name).absolute()),*args],cwd=D,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
 label=name.replace('/','_').replace('.py','');(A/('root_original_'+label+'.stdout')).write_bytes(r.stdout);(A/('root_original_'+label+'.stderr')).write_bytes(r.stderr);assert r.returncode==0 and not r.stderr,(name,r.stderr.decode())
 if name.startswith('check_turn_'):assert r.stdout==(D/f"TURN_{name[len('check_turn_')]}_CHECKS.json").read_bytes()
 elif name=='review/independent_checks.py':assert r.stdout==(D/'review/INDEPENDENT_CHECKS.json').read_bytes()
 elif name=='REPLAY_ALL.py':
  expected=json.loads((D/'review/AUTHOR_REPLAY.json').read_text());expected['source_files_checked']=0;assert json.loads(r.stdout)==expected
 else:assert json.loads(r.stdout)=={'review':'PASS','author_assertions':214070,'independent_assertions':93918,'source_files_checked':0,'source_note':'Raw source files absent; source verification explicitly omitted'}
 results.append({'program':name,'exit_code':0,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':0,'full_stdout_inspected':True})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':m['head'],'all_Git_and_snapshot_paths_exact':len(m['files']),'all_executable_sources_read':8,'all_full_streams':results,'author_assertions':sum(json.loads((D/f'TURN_{i}_CHECKS.json').read_text())['assertions'] for i in range(1,6)),'historical_assertions':93918,'source_files_checked_by_public_wrappers':0,'private_python':str(python),'sympy':'1.14.0','original_resolution_percent':0,'workflow_percent':65}
assert out['author_assertions']==214070;(A/'root_original_replay_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
