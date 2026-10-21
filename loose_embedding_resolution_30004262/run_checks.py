"""Run normal/-O exact sanity checks and negative mutation controls."""
from pathlib import Path
import json, subprocess, sys, tempfile
p=Path(__file__).resolve().parent
src=(p/'check_n1.py').read_text()
variants={'baseline':src,'triangle':src.replace('Q(1, 2 ** i) + Q(1, 2 ** (j + 1))','Q(100)'),'equality':src.replace('return 0 if i == 0 else 2 ** (i - 1)','return 0 if i == 0 else 2 ** (i - 1) + (1 if i == 35 else 0)')}
results=[]
for name,code in variants.items():
    if name!='baseline' and code==src:raise RuntimeError('Mutation did not apply')
    for opt in (False,True):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'check.py';f.write_text(code)
            r=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(f)],text=True,capture_output=True)
        expected=0 if name=='baseline' else 1
        if r.returncode!=expected:raise RuntimeError(f'Unexpected result: {name}, -O={opt}, {r.returncode}')
        if name!='baseline' and 'AssertionError' not in r.stderr:raise RuntimeError('Mutation failed without AssertionError')
        results.append({'variant':name,'optimized':opt,'exit_code':r.returncode,'expected_exit_code':expected,'stdout':r.stdout,'failure_type':'AssertionError' if 'AssertionError' in r.stderr else None})
(p/'CHECK_RESULTS.json').write_text(json.dumps({'scope':'Finite sanity checks, not general proofs','runs':results},indent=2)+'\n')
print('PASS: normal/-O baseline and both negative controls; checks remain active under optimization.')
