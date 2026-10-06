from pathlib import Path
import json,shutil,runpy,ast,hashlib,sys,datetime
from audit_process import run
A=Path(__file__).resolve().parent;SRC=A/'fresh_extracted'
PYTHON='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
CASES=['content','missing','file_symlink','unsafe','duplicate','assertion','ancestor_symlink']
results=[]
for name in CASES:
 root=A/'payload_controls'/name;root.parent.mkdir(exist_ok=True);shutil.copytree(SRC,root)
 m=root/'PAYLOAD_MANIFEST.json';d=json.loads(m.read_text())
 if name=='content':
  p=root/'verification/verify.py';p.write_text(p.read_text()+'\n# deliberately changed payload\n')
 elif name=='missing':(root/'LICENSE.txt').unlink()
 elif name=='file_symlink':
  p=root/'LICENSE.txt';p.unlink();p.symlink_to(SRC/'LICENSE.txt')
 elif name=='unsafe':d['files'][0]['file']='../outside.txt';m.write_text(json.dumps(d))
 elif name=='duplicate':d['files'].append(d['files'][0]);m.write_text(json.dumps(d))
 elif name=='assertion':
  p=root/'verification/verify.py';p.write_text(p.read_text()+'\nassert False\n')
  for r in d['files']:
   if r['file']=='verification/verify.py':r['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();r['bytes']=p.stat().st_size
  m.write_text(json.dumps(d))
 elif name=='ancestor_symlink':
  p=root/'verification/recorded_processes';shutil.rmtree(p);p.symlink_to(SRC/'verification/recorded_processes',target_is_directory=True)
 for optimized in (False,True):
  cmd=[PYTHON,'-E','-B']+(['-O'] if optimized else [])+['-c',"import runpy; d=runpy.run_path("+repr(str(root/'verification/run_all.py'))+"); print(d['guard']())"]
  out,err,code=run('payload_'+name+('_O' if optimized else '_normal'),cmd,inputs=[root/'verification/run_all.py',m],expected=0 if name=='ancestor_symlink' else 1)
  results.append({'case':name,'optimized':optimized,'exit':code,'stdout':out.decode(),'stderr_tail':err.decode()[-500:],'expected':'accepted ancestor symlink boundary' if name=='ancestor_symlink' else 'explicit rejection'})
(A/'PAYLOAD_CONTROLS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'boundary':'The guard rejects leaf-file symlinks but accepts symlinked ancestor directories for manifest members. No candidate bytes mutated.'},indent=2)+'\n')
