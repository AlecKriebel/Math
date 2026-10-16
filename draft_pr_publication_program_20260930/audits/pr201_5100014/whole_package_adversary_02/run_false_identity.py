from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,json,os
D=Path(__file__).resolve().parent;rows=[]
for opt in (False,True):
    label='false_identity_'+('optimized' if opt else 'normal')
    cmd=[sys.executable,'-B']+(['-O'] if opt else [])+[str(D/'independent_exact.py'),'--false-identity']
    start=datetime.now(timezone.utc).isoformat();r=subprocess.run(cmd,capture_output=True,text=True,env=os.environ.copy())
    (D/(label+'.stdout')).write_text(r.stdout);(D/(label+'.stderr')).write_text(r.stderr)
    good=r.returncode!=0 and 'deliberately false 41' in r.stderr
    rows.append({'start_UTC':start,'end_UTC':datetime.now(timezone.utc).isoformat(),'command':cmd,'returncode':r.returncode,'false_identity_rejected':good})
    if not good:raise RuntimeError('False product identity was not rejected')
print(json.dumps({'status':'PASS','false_claim':'Hexagon product 41*(1+|M|²/9) rather than 40*(1+|M|²/9)','records':rows},indent=2))
