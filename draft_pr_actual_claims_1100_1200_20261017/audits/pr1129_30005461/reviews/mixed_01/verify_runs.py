#!/usr/bin/env python3
"""Compare normal/optimized check reports and demonstrate guards survive -O."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

here=Path(__file__).resolve().parent
paths=[here/'CHECKS_NORMAL.json',here/'CHECKS_OPTIMIZED.json']
if paths[0].read_bytes()!=paths[1].read_bytes():
    raise RuntimeError('normal and optimized results differ')
reports=[json.loads(p.read_text()) for p in paths]
for x in reports:
    if x['status']!='PASS' or x['negative_control_count']!=11:
        raise RuntimeError('unexpected verification outcome')
items=[]
for flag in [[],['-O']]:
    proc=subprocess.run([sys.executable]+flag+['-c',
      'import verify_mixed as m; m.require(False, "deliberate_guard", "must fail under optimization")'],
      cwd=here, capture_output=True,text=True)
    label='optimized' if flag else 'normal'
    (here/'tmp'/('deliberate_guard_'+label+'.stderr.txt')).write_text(proc.stderr)
    if proc.returncode==0 or 'RuntimeError: deliberate_guard' not in proc.stderr:
        raise RuntimeError('deliberate failing guard was not rejected: '+label)
    items.append({'mode':label,'expected_nonzero_returncode':proc.returncode,
                  'explicit_guard_rejected':True})
out={'status':'PASS','normal_optimized_results_byte_identical':True,
     'result_sha256':sha256(paths[0].read_bytes()).hexdigest(),
     'total_checks_per_mode':reports[0]['total_checks'],
     'adverse_controls_per_mode':11,'deliberate_guard_runs':items,
     'python_executable':sys.executable,'python_version':sys.version}
(here/'RUN_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
