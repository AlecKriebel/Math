#!/usr/bin/env python3
"""Mutation tests of copied wrapper; originals are read-only and rehashed."""
from pathlib import Path
import runpy,sys,tempfile,shutil,json,hashlib,subprocess,os,datetime
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
(R/'tmp').mkdir(exist_ok=True)
os.environ['TMPDIR']=str(R/'tmp')
tempfile.tempdir=str(R/'tmp')
P=R/'extracted/dfc_stability_verification'
ns=runpy.run_path(str(P/'reproduce.py'),run_name='audit_import')
results=[]
def rejected(label,call):
 try:call()
 except Exception as e:results.append({'case':label,'rejected':True,'exception':str(e)[:200]});return
 raise RuntimeError('FALSE GREEN '+label)
def rehash(root,rel):
 m=json.loads((root/'MANIFEST.json').read_text());b=(root/rel).read_bytes()
 for x in m['files']:
  if x['path']==rel:x.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 (root/'MANIFEST.json').write_text(json.dumps(m))

def run_main(root,*extra,env=None):
 p=subprocess.run([sys.executable,*extra,str(root/'reproduce.py'),'--integrity-only'],capture_output=True,text=True,env=env)
 if p.returncode==0:raise RuntimeError('incorrect success return code')
 return p

for case in ['missing','tampered','unlisted','symlink','duplicate_manifest']:
 with tempfile.TemporaryDirectory(dir=R,prefix='mutation-') as d:
  q=Path(d)/'package';shutil.copytree(P,q)
  if case=='missing':(q/'main.tex').unlink()
  elif case=='tampered':(q/'main.tex').write_bytes((q/'main.tex').read_bytes()+b'\n')
  elif case=='unlisted':(q/'extra.txt').write_text('unlisted')
  elif case=='symlink':(q/'extra-link').symlink_to(q/'main.tex')
  else:
   m=json.loads((q/'MANIFEST.json').read_text());m['files'].append(m['files'][0]);(q/'MANIFEST.json').write_text(json.dumps(m))
  rejected(case,lambda:ns['verify'](q))
# Call both negative conditions independently, without launching all research controls.
with tempfile.TemporaryDirectory(dir=R,prefix='execute-tests-') as d:
 q=Path(d)
 for name,source in {
  'zero_with_marker.py':"import sys;print('EXPECTED_REJECTION: Common Chunk is not DFC',file=sys.stderr)\n",
  'nonzero_without_marker.py':"raise RuntimeError('other error')\n",
  'nonzero_with_marker.py':"raise RuntimeError('EXPECTED_REJECTION: Common Chunk is not DFC')\n",
  'nonjson_success.py':"print('not JSON')\n",
  'positive_failure.py':"raise RuntimeError('positive failed')\n"}.items():(q/name).write_text(source)
 rejected('negative exits zero despite marker',lambda:ns['execute'](q,'zero_with_marker.py',failure_marker='EXPECTED_REJECTION: Common Chunk is not DFC'))
 rejected('negative exits nonzero without marker',lambda:ns['execute'](q,'nonzero_without_marker.py',failure_marker='EXPECTED_REJECTION: Common Chunk is not DFC'))
 assert ns['execute'](q,'nonzero_with_marker.py',failure_marker='EXPECTED_REJECTION: Common Chunk is not DFC')['expected_rejection']
 results.append({'case':'negative nonzero with exact marker','correctly_accepted':True})
 rejected('positive program fails',lambda:ns['execute'](q,'positive_failure.py'))
 rejected('positive stdout is not JSON',lambda:ns['execute'](q,'nonjson_success.py'))
# Guard remains active even when integrity-only requested.
p=run_main(P,'-O');assert 'Run without -O' in p.stderr
results.append({'case':'Python -O','rejected':True})
env=dict(os.environ);env['PYTHONOPTIMIZE']='1';p=run_main(P,env=env);assert 'Run without -O' in p.stderr
results.append({'case':'PYTHONOPTIMIZE=1','rejected':True})
assert ns['simulation_equal']({'v':1.0,'n':5},{'v':1.0+1e-12,'n':5})
assert not ns['simulation_equal']({'v':1.01,'n':5},{'v':1.0,'n':5})
assert not ns['simulation_equal']({'v':float('nan'),'n':5},{'v':1.0,'n':5})
assert not ns['simulation_equal']({'v':1.0,'n':6},{'v':1.0,'n':5})
results.append({'case':'only stated float tolerance; bad float, NaN and integer change','rejected':True})
# A coherent manifest with a deliberately false expected output must not green.
with tempfile.TemporaryDirectory(dir=R,prefix='full-wrapper-mutation-') as d:
 q=Path(d)/'package';shutil.copytree(P,q)
 rel='original/checks/turn1_output.json'
 j=json.loads((q/rel).read_text());j['assertions']+=1;(q/rel).write_text(json.dumps(j));rehash(q,rel)
 # Nested original chain also detects it; either rejection suffices to prevent green.
 p=subprocess.run([sys.executable,str(q/'reproduce.py')],capture_output=True,text=True)
 assert p.returncode!=0 and 'PASS_COMPLETE_REPRODUCTION' not in p.stdout
 results.append({'case':'changed frozen output, outer manifest recomputed','rejected':True,'stderr_tail':p.stderr[-500:]})
print(json.dumps({'status':'PASS_WRAPPER_ADVERSARIAL_MUTATIONS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':results,'frozen_payloads_still_valid':ns['verify'](P)},indent=2))
