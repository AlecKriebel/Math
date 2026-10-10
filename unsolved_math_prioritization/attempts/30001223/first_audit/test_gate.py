#!/usr/bin/env python3
"""Run mutation controls on temporary copies, preserving this archive."""
import json,hashlib,shutil,subprocess,sys,tempfile,os
from pathlib import Path
root=Path(__file__).absolute().parent

def pin(r):
 files={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in r.iterdir() if p.name!='manifest.json'}
 (r/'manifest.json').write_text(json.dumps({'schema':'young-tops-independent-audit-v1','files':files},sort_keys=True,indent=2)+'\n')

results=[]
with tempfile.TemporaryDirectory(prefix='audit-acceptance-') as td:
 for optimized in (False,True):
  for case in ['baseline','relocation','source','result','proof','cache','extra','missing','directory','symlink','fifo','manifest_schema','manifest_extra','repinned_false_result']:
   dst=Path(td)/str(optimized)/case/'relocated path';shutil.copytree(root,dst)
   if case in ('source','result','proof'):
    n={'source':'independent_check.py','result':'independent_results.json','proof':'mathematical_audit.md'}[case]
    p=dst/n;p.write_bytes(p.read_bytes()+b' ')
   elif case=='cache':(dst/'__pycache__').mkdir()
   elif case=='extra':(dst/'extra').write_bytes(b'')
   elif case=='missing':(dst/'independent_results.json').unlink()
   elif case in ('directory','symlink','fifo'):
    p=dst/'independent_results.json';p.unlink()
    if case=='directory':p.mkdir()
    elif case=='symlink':p.symlink_to('README.md')
    else:os.mkfifo(p)
   elif case in ('manifest_schema','manifest_extra'):
    p=dst/'manifest.json';m=json.loads(p.read_text())
    if case=='manifest_schema':m['schema']='bad'
    else:m['files']['extra']={'bytes':0,'sha256':'0'*64}
    p.write_text(json.dumps(m))
   elif case=='repinned_false_result':
    p=dst/'independent_results.json';m=json.loads(p.read_text());m['endomorphism_dimension']=2;p.write_text(json.dumps(m));pin(dst)
   flags=['-B']+(['-O'] if optimized else [])
   r=subprocess.run([sys.executable,*flags,str(dst/'audit_gate.py')],cwd=td,capture_output=True,text=True,timeout=30)
   good=(r.returncode==0) if case in ('baseline','relocation') else (r.returncode!=0 and 'REJECT:' in r.stderr)
   if not good:raise RuntimeError(case+': '+r.stdout+r.stderr)
   row={'test':case,'optimized':optimized,'passed':True,'returncode':r.returncode}
   if r.returncode:row['rejection']=r.stderr.strip()
   results.append(row)
print(json.dumps({'status':'PASS','checks':results,'checker_development_note':'During independent checker development, an incorrect provisional expected rank of 9 was replaced by the computed rank 12. This was an auditor test expectation error, not a defect in the author proof. The final source was fixed before the acceptance replay.'},sort_keys=True,indent=2))
