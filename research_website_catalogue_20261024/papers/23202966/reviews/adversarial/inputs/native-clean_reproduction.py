#!/usr/bin/env python3
"""Test publication sources/code in a project-local clean temporary directory."""
from pathlib import Path
import hashlib,json,platform,shutil,subprocess,tempfile,time
root=Path(__file__).resolve().parents[1]
scripts=['code/binary_compiler.py','reviews/reduction_adversary_check.py',
         'agent_notes/determinization_algebra_check.py','agent_notes/upstream_algebra_check.py']
receipt={'python':platform.python_version(),'runs':[]}
(root/'tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir=root/'tmp',prefix='clean-reproduction-') as temp:
    clean=Path(temp)
    for name in scripts+['main.tex']:
        destination=clean/name;destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(root/name,destination)
    for script in scripts:
        started=time.monotonic()
        p=subprocess.run(['python3',script],cwd=clean,capture_output=True,text=True,check=True)
        result=json.loads(p.stdout)
        receipt['runs'].append({'script':script,'sha256':hashlib.sha256((clean/script).read_bytes()).hexdigest(),
                                'seconds':round(time.monotonic()-started,3),'result':result})
    p=subprocess.run(['tectonic','main.tex'],cwd=clean,capture_output=True,text=True,check=True)
    receipt['pdf_build']={'status':'passed','compiler':subprocess.check_output(['tectonic','--version'],text=True).strip(),
                          'pdf_bytes':(clean/'main.pdf').stat().st_size,
                          'tex_sha256':hashlib.sha256((clean/'main.tex').read_bytes()).hexdigest(),
                          'stdout':p.stdout,'stderr':p.stderr}
receipt['status']='passed'
(root/'receipts/clean_reproduction.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'passed','scripts':len(scripts),'pdf_build':'passed'},indent=2))
