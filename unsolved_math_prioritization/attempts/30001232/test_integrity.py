#!/usr/bin/env python3
"""Negative controls run only in disposable copies; frozen files stay unchanged."""
from pathlib import Path
import importlib.util,json,os,shutil,subprocess,sys,tempfile
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('release_integrity',ROOT/'verify_release.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
v.verify_integrity(ROOT)
mutations={
 'changed_file':lambda r:(r/'author/README.md').write_bytes((r/'author/README.md').read_bytes()+b'!'),
 'missing_file':lambda r:(r/'author/README.md').unlink(),
 'extra_file':lambda r:(r/'UNLISTED.md').write_text('must fail'),
 'extra_directory':lambda r:(r/'unlisted_empty_directory').mkdir(),
 'symlink':lambda r:(r/'extra_link').symlink_to(r/'author/README.md'),
}
def change_manifest(r,kind):
 p=r/'RELEASE_MANIFEST.json';d=json.loads(p.read_text())
 if kind=='duplicate':d['files'].append(dict(d['files'][0]))
 else:d['files'][0]['path']='../outside.md'
 p.write_text(json.dumps(d))
mutations['duplicate_manifest']=lambda r:change_manifest(r,'duplicate')
mutations['traversal_manifest']=lambda r:change_manifest(r,'traversal')
results=[]
for name,mutate in mutations.items():
 with tempfile.TemporaryDirectory() as t:
  copy=Path(t)/'packet';shutil.copytree(ROOT,copy);mutate(copy)
  try:v.verify_integrity(copy)
  except (RuntimeError,ValueError,KeyError) as e:results.append({'mutation':name,'rejected':True})
  else:raise RuntimeError('Mutation was not detected: '+name)
proc=subprocess.run([sys.executable,'-O',str(ROOT/'verify_release.py')],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
if proc.returncode==0 or b'Optimized Python' not in proc.stderr:raise RuntimeError('Optimized execution was not rejected.')
results.append({'mutation':'optimized_python','rejected':True})
v.verify_integrity(ROOT)
print(json.dumps({'status':'PASS','negative_controls':results,'frozen_inputs_unchanged':True},indent=2,sort_keys=True))
