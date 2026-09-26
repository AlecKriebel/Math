#!/usr/bin/env python3
"""Review-only targeted negative checks of the new source-fidelity safeguards."""
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

root=Path(__file__).resolve().parents[1]
path=root/'supplement'/'verify_exact.py'
source=path.read_text()
print('source_sha256',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
variants=[
 ('merge_printed_with_common',
  '        scalar_mul(sqrt2 / 2, ghr_block_b),',
  '        scalar_mul(ghr_prefactor, ghr_block_b),',
  'literal mixed-prefactor preprint trace is not 1+i sqrt(3)'),
 ('change_pauli_encoding',
  '            ("ZZZ", CQ23(0, -1)),',
  '            ("ZZZ", CQ23(0, 1)),',
  'independent Pauli encoding of common-prefactor block operator'),
]
for name,old,new,expected in variants:
    if source.count(old)!=1:raise RuntimeError('nonunique mutation anchor '+name)
    with tempfile.TemporaryDirectory(prefix='algebra_closure_',dir=root/'tmp') as work:
        altered=Path(work)/'verify_exact.py';altered.write_text(source.replace(old,new))
        result=subprocess.run([sys.executable,str(altered)],text=True,capture_output=True,cwd=path.parent)
    if result.returncode==0 or 'AssertionError:' not in result.stderr or expected not in result.stderr:
        raise RuntimeError(name+' missed expected scientific safeguard\n'+result.stdout+'\n'+result.stderr)
    print('PASS',name,'->',result.stderr.strip().splitlines()[-1],flush=True)
print('FINISHED',datetime.now(timezone.utc).isoformat(),flush=True)
