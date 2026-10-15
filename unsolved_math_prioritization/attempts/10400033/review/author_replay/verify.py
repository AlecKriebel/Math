#!/usr/bin/env python3
"""Run both exact verification methods and report their distinct coverage."""
from pathlib import Path
import subprocess,json,sys
here=Path(__file__).resolve().parent
results={}
for name in ['verify_jones.py','verify_tournaments.py']:
    run=subprocess.run([sys.executable,str(here/name)],cwd=here,capture_output=True,text=True,check=True)
    results[name]=json.loads(run.stdout)
    assert results[name]['status']=='PASS'
print(json.dumps({'status':'PASS','exact_assertions':sum(r['exact_assertions'] for r in results.values()),'methods':results,'limitation':'Finite exact checks support the written all-diagram proof; they do not replace it.'},indent=2,sort_keys=True))
