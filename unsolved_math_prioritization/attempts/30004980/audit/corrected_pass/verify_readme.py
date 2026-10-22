#!/usr/bin/env python3
"""Run all four documented commands in a temporary copy; compare output bytes.
Usage: python verify_readme.py /path/to/author
Python 3.10+, no third-party dependencies or network access needed.
"""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,time
source=pathlib.Path(sys.argv[1]).resolve()
initial={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source.rglob('*') if p.is_file()}
manifest=json.loads((source/'MANIFEST.json').read_text())
for f in manifest['files']:
 b=(source/f['path']).read_bytes()
 if len(b)!=f['bytes'] or hashlib.sha256(b).hexdigest()!=f['sha256']:raise RuntimeError('Manifest mismatch: '+f['path'])
results=[]
with tempfile.TemporaryDirectory(prefix='twinwidth_audit_') as d:
 target=pathlib.Path(d)/'package';shutil.copytree(source,target)
 for script in ['twinwidth.py','verify_small.py','conference_controls.py','verify_obstruction.py']:
  start=time.monotonic();run=subprocess.run([sys.executable,script],cwd=target/'checks',env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE':'0'},text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  print('=== '+script+' ===\n'+run.stdout)
  if run.returncode:raise RuntimeError(script+' failed')
  results.append({'script':script,'exit':run.returncode,'seconds':time.monotonic()-start})
 for name in ['pair_search_results.json','verification_results.json','conference_results.json','cyclic_pair_obstruction.json']:
  if (source/'checks'/name).read_bytes()!=(target/'checks'/name).read_bytes():raise RuntimeError('Regenerated output differs: '+name)
final={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source.rglob('*') if p.is_file()}
if initial!=final:raise RuntimeError('Source bytes changed')
print(json.dumps({'all_commands_passed':True,'all_four_json_outputs_identical':True,'source_unchanged':True,'results':results},indent=2))
