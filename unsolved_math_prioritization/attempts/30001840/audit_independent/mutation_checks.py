#!/usr/bin/env python3
"""Run isolated mathematical mutants in real optimized Python children."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/'public'/'checks.py'
CORRECTED=HERE/'checks_corrected.py'
MUTATIONS=[
    ('chebyshev_sign','x**5-5*x**3+5*x','x**5+5*x**3+5*x'),
    ('affine_slope_omission','a in range(1,5)','a in range(1,4)'),
    ('vanishing_second_generator','V=(1,0,neg(c),1)','V=(1,0,0,1)'),
    ('wrong_branch_coefficient','c=add(2%p,w)','c=add(1%p,w)'),
    ('wrong_ring_relation','x*v+y*z-y*v','x*v+y*z+y*v'),
    ('wrong_fifth_power','powmat(prod(U,V),5)','powmat(prod(U,V),4)'),
    ('projective_for_linear_order','3:120,5:15000','3:60,5:15000'),
    ('wrong_order_fingerprint','3:20,4:30,5:24','3:20,4:29,5:24'),
    ('wrong_determinant_target','neg(mul(b,c)))==1','neg(mul(b,c)))==0'),
]

def run(path,optimized,primes):
    driver='import json,runpy,sys; print(json.dumps({"optimize":sys.flags.optimize,"debug":__debug__}),file=sys.stderr); sys.argv=[sys.argv[1],"--primes"]+sys.argv[2:]; runpy.run_path(sys.argv[0],run_name="__main__")'
    cmd=[sys.executable]+(['-O'] if optimized else [])+['-c',driver,str(path)]+[str(p) for p in primes]
    r=subprocess.run(cmd,capture_output=True,text=True)
    lines=r.stderr.splitlines()
    meta=json.loads(lines[0])
    if meta!={'optimize':1 if optimized else 0,'debug':not optimized}:
        raise RuntimeError(('Incorrect child mode',meta))
    return {'exit_code':r.returncode,**meta,'diagnostic':lines[-1] if len(lines)>1 else None,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()},r.stdout

def main():
    baseline=(HERE.parent/'public'/'FINITE_CHECKS.json').read_text()
    out={'scope':'Isolated subprocesses; -O is passed to the Python executable. No assertion is used by this harness.','baselines':[],'mutations':[]}
    for tag,source in [('original',ORIGINAL),('corrected',CORRECTED)]:
        for optimized in (False,True):
            rec,stdout=run(source,optimized,[2,3,5,7])
            if rec['exit_code']!=0 or stdout!=baseline:raise RuntimeError(('Baseline mismatch',tag,optimized,rec))
            out['baselines'].append({'version':tag,**rec,'matches_frozen_output':True})
        text=source.read_text()
        with tempfile.TemporaryDirectory(prefix='genus-two-mutants-') as td:
            for name,before,after in MUTATIONS:
                if text.count(before)!=1:raise RuntimeError(('Nonunique mutation target',tag,name,text.count(before)))
                p=Path(td)/(name+'.py');p.write_text(text.replace(before,after))
                for optimized in (False,True):
                    rec,_=run(p,optimized,[3])
                    expected_rejected=(tag=='corrected' or not optimized)
                    if (rec['exit_code']!=0)!=expected_rejected:raise RuntimeError(('Unexpected mutation outcome',tag,name,optimized,rec))
                    out['mutations'].append({'version':tag,'mutation':name,**rec,'rejected':rec['exit_code']!=0})
    out['summary']={'mutants':len(MUTATIONS),'original_regular_rejected':9,'original_optimized_rejected':0,'corrected_regular_rejected':9,'corrected_optimized_rejected':9}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
