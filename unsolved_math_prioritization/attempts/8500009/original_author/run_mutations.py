#!/usr/bin/env python3
"""Relocation, optimized execution, certificate parity and eight negative controls."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
source = (HERE/'verify_exact.py').read_text()
mutations = [
 ('drop_diagonals', 'for j in range(i, len(values)):', 'for j in range(i+1, len(values)):'),
 ('allow_zero_element', 'if not values or any(x == 0 for x in values):', 'if not values:'),
 ('allow_duplicate_elements', 'if len(set(values)) != len(values):', 'if False:'),
 ('skip_missing_cross', 'q = values[i]*values[j]+1', 'q = 1 if (i,j)==(2,3) else values[i]*values[j]+1'),
 ('accept_negative_square', 'if q < 0:\n        return None', 'if q < 0:\n        return Q(1)'),
 ('wrong_cover_scale', 'return 2*t*(a*t*t+2*t-a)', 'return 4*t*(a*t*t+2*t-a)'),
 ('product_square_only', 'and all(root(f(a, t)) is not None for a in base))', 'and root(__import__("functools").reduce(lambda x,y:x*y, (f(a,t) for a in base), Q(1))) is not None)'),
 ('wrong_branch_count', 'degree, branch_points = 2**k, 2*k+2', 'degree, branch_points = 2**k, 2*k+1'),
]
results = {'original_sha256': hashlib.sha256(source.encode()).hexdigest(), 'runs': [], 'mutations': []}
with tempfile.TemporaryDirectory(prefix='strong_quadruple_relocated_') as raw:
    work = Path(raw)
    script = work/'verify_exact.py'
    script.write_text(source)
    env = {'PATH': os.environ.get('PATH',''), 'HOME': raw, 'LANG': 'C.UTF-8'}
    outputs=[]
    for flags in ([],['-O'],['-I'],['-I','-O']):
        p = subprocess.run([sys.executable,*flags,str(script),'--test'],cwd=work,env=env,text=True,capture_output=True)
        results['runs'].append({'flags':flags,'returncode':p.returncode,'log':(p.stdout+p.stderr).replace(str(script),'verify_exact.py')})
        if p.returncode: raise RuntimeError('genuine tests failed: '+p.stderr)
        c = subprocess.run([sys.executable,*flags,str(script)],cwd=work,env=env,capture_output=True,check=True).stdout
        outputs.append(c)
    expected = (HERE/'exact_certificate.json').read_bytes()
    if any(o != expected for o in outputs): raise RuntimeError('certificate changed or disagrees with saved file')
    results['certificate_sha256'] = hashlib.sha256(expected).hexdigest()
    for name, old, new in mutations:
        if source.count(old)!=1: raise RuntimeError('mutation anchor not unique: '+name)
        script.write_text(source.replace(old,new))
        p = subprocess.run([sys.executable,'-I','-O',str(script),'--test'],cwd=work,env=env,text=True,capture_output=True)
        log=(p.stdout+p.stderr).replace(str(script),'verify_exact.py')
        killed = p.returncode != 0 and ('FAIL:' in log or 'ERROR:' in log) and 'SyntaxError' not in log
        results['mutations'].append({'name':name,'killed':killed,'returncode':p.returncode,'log':log})
        if not killed: raise RuntimeError('mutation survived or failed to execute: '+name+'\n'+log)
print(json.dumps(results,indent=2,sort_keys=True))
