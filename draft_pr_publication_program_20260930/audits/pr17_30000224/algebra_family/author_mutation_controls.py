#!/usr/bin/env python3
"""Run deliberately incorrect isolated copies; do not touch frozen source."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source_snapshot'/'verify.py'
original=SOURCE.read_bytes()
text=original.decode()
mutations=[
 ('missing_monomial_changed','u = mono((2, 2))','u = mono((1, 3))'),
 ('conormal_coefficient_changed','v1 = [mono((0, 3), 2),','v1 = [mono((0, 3), 3),'),
 ('socle_sign_changed','c = [scale(-1, times(x, z)), times(x, y), {}, {}]',
                       'c = [scale(1, times(x, z)), times(x, y), {}, {}]'),
 ('Segre_factor_sign_changed','minus(times(b, power(cc, 3)), times(a, power(dd, 3)))',
                            'plus(times(b, power(cc, 3)), times(a, power(dd, 3)))'),
 ('nonboundary_rank_changed','assert_equal(rank(cols+[flatten(c)]), 7)',
                            'assert_equal(rank(cols+[flatten(c)]), 6)'),
]
records=[]
for name,old,new in mutations:
    assert text.count(old)==1
    folder=HERE/'tmp'/'author_mutations'/name
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/'verify.py'
    path.write_text(text.replace(old,new))
    run=subprocess.run([sys.executable,'-B',str(path)],cwd=folder,capture_output=True,text=True)
    record={'name':name,'mutated_script_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'exit_code':run.returncode,'failure_detected':run.returncode!=0,
            'receipt_written':(folder/'verification.json').exists(),
            'stdout':run.stdout,'stderr':run.stderr}
    assert record['failure_detected'] and not record['receipt_written']
    records.append(record)
assert SOURCE.read_bytes()==original
out={'checked_at_utc':datetime.now(timezone.utc).isoformat(),
     'status':'passed: all five deliberately wrong copies rejected',
     'frozen_verify_sha256':hashlib.sha256(original).hexdigest(),
     'frozen_source_unchanged':True,'records':records}
(HERE/'evidence'/'author_mutation_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
