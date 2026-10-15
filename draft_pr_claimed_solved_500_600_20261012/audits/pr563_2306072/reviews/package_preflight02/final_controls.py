#!/usr/bin/env python3
"""Supplemental fresh review controls, confined to expendable cache copies."""
from pathlib import Path
import shutil,subprocess,hashlib,json,sys,os
HERE=Path(__file__).resolve().parent
BASE=HERE/'.cache/extract2/support_slit_verification'
CACHE=HERE/'.cache/final-controls'
if CACHE.exists():shutil.rmtree(CACHE)
CACHE.mkdir()
records=[]
p=CACHE/'opt';shutil.copytree(BASE,p)
x=subprocess.run([sys.executable,'-O',str(p/'run_all.py')],capture_output=True,text=True)
assert x.returncode and 'Run without Python optimization' in x.stderr
records.append({'name':'command_line_optimization','pass':True,'stderr':x.stderr})
p=CACHE/'late-mutation';shutil.copytree(BASE,p);driver=CACHE/'driver.py'
driver.write_text("import sys, pathlib\nsys.path.insert(0,sys.argv[1])\nimport run_all\nreal=run_all.subprocess.run\ncount=0\ndef instrument(*a,**kw):\n global count\n script=pathlib.Path(a[0][1])\n assert '.verify-' in str(script)\n assert pathlib.Path(kw['cwd'])==script.parent\n x=real(*a,**kw);count+=1\n if count==14:(run_all.ROOT/'README.md').write_text('late mutation')\n return x\nrun_all.subprocess.run=instrument\nrun_all.main()\n")
x=subprocess.run([sys.executable,str(driver),str(p)],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
assert x.returncode and 'Frozen payload changed during replay' in x.stderr
records.append({'name':'scratch_local_jobs_and_late_parent_mutation','pass':True,'stderr':x.stderr,'stdout':x.stdout})
p=CACHE/'FS_optional';shutil.copytree(BASE/'reviews/priority05_friedland1977',p)
x=subprocess.run([sys.executable,str(p/'verify_manifest.py')],capture_output=True,text=True)
assert x.returncode==0
records.append({'name':'FS_optional_with_present_original','pass':True,'stdout':x.stdout})
q=p/'SOURCE.json';s=json.loads(q.read_text());s['pdf']['path']=str(CACHE/'absent-original.pdf');q.write_text(json.dumps(s,indent=2)+'\n')
m=json.loads((p/'MANIFEST.json').read_text());d=q.read_bytes();m['files']['SOURCE.json']={'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()};(p/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
x=subprocess.run([sys.executable,str(p/'verify_manifest.py')],capture_output=True,text=True)
assert x.returncode and 'FileNotFoundError' in x.stderr
records.append({'name':'FS_optional_without_original_is_not_offline','pass':True,'stderr':x.stderr})
(HERE/'ADDITIONAL_CONTROLS.json').write_text(json.dumps({'status':'PASS','count':len(records),'records':records},indent=2)+'\n')
print(json.dumps({'status':'PASS','count':len(records)}))
