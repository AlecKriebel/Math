#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
version,family=sys.argv[1:3]
base=HERE/('exact_replays' if version=='original' else 'suggested_guard_repairs')
scriptname='verify.py' if family=='author' else 'independent_checks.py'
rows=[]
for mode in ['normal','optimized']:
    p=base/f'{family}_{mode}'/scriptname
    flags=['-O'] if mode=='optimized' else []
    for attack in ['known_false','corrupt_cost','cycles']:
        label=f'control_{version}_{family}_{mode}_{attack}'
        command=['python3',str(HERE/'execute_case.py'),label,str(HERE),'python3',*flags,str(HERE/'guard_adversary.py'),family,str(p),attack]
        r=subprocess.run(command,cwd=HERE,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(r.stderr)
        record=json.loads((HERE/'journals'/f'{label}.json').read_text())
        expected=0 if attack=='cycles' or (version=='original' and mode=='optimized') else 1
        if record['returncode']!=expected:raise RuntimeError(f'unexpected control outcome {label}: {record}')
        rows.append({'label':label,'version':version,'family':family,'mode':mode,'attack':attack,'returncode':record['returncode'],'expected_returncode':expected,'interpretation': 'valid enumeration control passed' if attack=='cycles' else 'unsafe optimized guard bypass confirmed' if record['returncode']==0 else 'false/corrupted control rejected'})
(HERE/f'controls_{version}_{family}.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,sort_keys=True))
