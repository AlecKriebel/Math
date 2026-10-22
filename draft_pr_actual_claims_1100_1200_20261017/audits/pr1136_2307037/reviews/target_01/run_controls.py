#!/usr/bin/env python3
"""Run baseline plus three deliberate mathematical errors under normal and -O."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
rows=[]
baseline=[]
for optimized in [False,True]:
    mode = 'optimized' if optimized else 'normal'
    for mutant in ['none','missing_pi','spurious_R2','radius_lambda']:
        command = [sys.executable] + (['-O'] if optimized else []) + [str(HERE/'independent_controls.py')]
        if mutant != 'none':
            command += ['--mutant',mutant]
        proc = subprocess.run(command,text=True,capture_output=True)
        expected = 0 if mutant == 'none' else 1
        if proc.returncode != expected or proc.stderr:
            raise RuntimeError('Unexpected control execution: '+repr((mode,mutant,proc.returncode,proc.stderr)))
        result = json.loads(proc.stdout)
        if result['status'] != ('PASS' if mutant == 'none' else 'FAIL'):
            raise RuntimeError('Unexpected control status')
        if mutant == 'none':
            output = HERE/('controls.'+mode+'.json')
            output.write_text(proc.stdout)
            baseline.append(proc.stdout)
        rows.append({'mode':mode,'mutant':mutant,'returncode':proc.returncode,
                     'expected_returncode':expected,'reason':result.get('reason'),'status':result['status']})
if baseline[0] != baseline[1]:
    raise RuntimeError('Normal and -O baseline outputs differ')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary={'status':'PASS','baseline_normal_optimized_byte_equal':True,
         'runner_sha256':sha(Path(__file__)),'control_code_sha256':sha(HERE/'independent_controls.py'),
         'input_sha256':sha(HERE/'control_inputs.json'),'runs':rows}
(HERE/'guard_results.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps(summary,indent=2,sort_keys=True))
