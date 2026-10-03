#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parent
specs=[('verify_affine_modules.py','affine_module_results.json'),('verify_nonsplit_candidate.py','nonsplit_candidate_results.json')]
results=[]
for script,result in specs:
 before=json.loads((root/result).read_text())
 proc=subprocess.run([sys.executable,str(root/script)],capture_output=True,text=True,check=True)
 after=json.loads((root/result).read_text())
 assert before==after, f'Replay differs from frozen expected output: {result}'
 results.append({'script':script,'status':'PASS','expected_output_match':True})
print(json.dumps({'status':'PASS','checks':results,'scope':'Finite checks only; universal target remains unresolved.'},indent=2))
