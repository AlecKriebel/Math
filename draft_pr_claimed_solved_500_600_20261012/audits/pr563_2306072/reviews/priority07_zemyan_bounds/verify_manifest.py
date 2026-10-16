#!/usr/bin/env python3
"""Verify authored-file seal and read-only source custody without mutation."""
from pathlib import Path
import hashlib,json,subprocess,sys
here=Path(__file__).resolve().parent
root=here
while not (root/'.git').exists():root=root.parent
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
manifest=json.loads((here/'MANIFEST.json').read_text())
for row in manifest['files']:
    p=here/row['path']
    if not p.exists() or digest(p)!=row['sha256'] or p.stat().st_size!=row['size']:
        errors.append('authored digest/size mismatch: '+row['path'])
    ignored=subprocess.run(['git','check-ignore','-q',str(p)],cwd=root).returncode==0
    if ignored:errors.append('authored file ignored: '+row['path'])
identity=json.loads((here/'SOURCE_IDENTITY.json').read_text())
for row in identity['primary_sources']+identity['comparison_inputs']:
    p=Path(row['path'])
    if not p.exists() or digest(p)!=row['sha256']:errors.append('input drift: '+row['path'])
for p in [here/'raw/zemyan2005.txt',here/'raw/zemyan2007.txt',here/'raw/zemyan2005_9.png',here/'raw/zemyan2007_4.png']:
    if p.exists() and subprocess.run(['git','check-ignore','-q',str(p)],cwd=root).returncode!=0:errors.append('raw not ignored: '+str(p))
if subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()!='main':errors.append('branch is not main')
if (here/'SEAL.json').exists():
    seal=json.loads((here/'SEAL.json').read_text())
    for filename,sha in seal['binds'].items():
        if not (here/filename).exists() or digest(here/filename)!=sha:errors.append('terminal seal mismatch: '+filename)
result={'all_passed':not errors,'authored_files_checked':len(manifest['files']),'input_files_checked':len(identity['primary_sources'])+len(identity['comparison_inputs']),'raw_ignored':True if not any('raw' in s for s in errors) else False,'main_branch':not any('branch' in s for s in errors),'errors':errors}
print(json.dumps(result,indent=2))
sys.exit(bool(errors))
