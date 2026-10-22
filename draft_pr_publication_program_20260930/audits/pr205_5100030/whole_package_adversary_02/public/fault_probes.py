#!/usr/bin/env python3
"""Extra explicit-rejection probes. Run ordinarily and with Python -O.

Requires mpmath==1.3.0 (installed or --runtime external/site-packages).
Use --verifier PATH to an extracted verification/verify.py.
Historical AST controls use --historical PATH to materials/original_submitted_head.
"""
import argparse
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--runtime',type=Path)
p.add_argument('--verifier',type=Path,required=True)
p.add_argument('--historical',type=Path,required=True)
a=p.parse_args()
if a.runtime:sys.path.insert(0,str(a.runtime.resolve()))
import mpmath as mp
mp.mp.dps=100
s=importlib.util.spec_from_file_location('subject_verifier',a.verifier)
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
done=[]
def reject(name,call):
    try:call()
    except v.VerificationError as e:done.append({'name':name,'exception':str(e)});return
    raise RuntimeError('Probe accepted: '+name)

for bad in [mp.nan,mp.inf,-mp.inf,mp.mpc(2,1),True]:
    for position in [0,1]:
        xs=[mp.mpf(2),mp.mpf(3)];xs[position]=bad
        reject('total:'+str(bad)+':'+str(position),lambda xs=xs:v.total(xs))
        reject('maximum:'+str(bad)+':'+str(position),lambda xs=xs:v.largest(xs))
    reject('close.actual:'+str(bad),lambda bad=bad:v.close(bad,1,mp.mpf('1e-40'),'probe'))
    reject('close.expected:'+str(bad),lambda bad=bad:v.close(1,bad,mp.mpf('1e-40'),'probe'))
    reject('close.tol:'+str(bad),lambda bad=bad:v.close(1,1,bad,'probe'))
for fn in [v.total,v.largest]:reject('empty:'+fn.__name__,lambda fn=fn:fn([]))
for bad in [(5,2.0),(5,True),(mp.nan,1),(9,3),(15,5),(5,-1)]:
    reject('period:'+str(bad),lambda bad=bad:v.period(*bad))
for bad in [0,-1,mp.nan,mp.inf,mp.mpc(1,1)]:
    reject('tolerance:'+str(bad),lambda bad=bad:v.close(1,1,bad,'probe'))
reject('wrong finite identity',lambda:v.close(mp.mpf(8),mp.mpf(9),mp.mpf('1e-40'),'wrong'))
reject('parameter vs modulus confusion',lambda:v.close(v.normalized_value(mp.mpf('.5'),3)[0],v.normalized_value(mp.sqrt(mp.mpf('.5')),3)[0],mp.mpf('1e-40'),'wrong parameter'))

# Probe a current program execution with corrupted mathematical input.
old=v.normalized_value
def wrong(m,N):
    x=list(old(m,N));x[0]*=mp.mpf('1.01');return tuple(x)
v.normalized_value=wrong
sys.argv=[str(a.verifier),'--digits','50']
reject('main with corrupted analytic normalization',v.main)
v.normalized_value=old

# Probe nonfinite values arriving from a dependency before any reduction.
oldfun=mp.ellipfun
mp.ellipfun=lambda *args,**kwargs:mp.nan
reject('dependency NaN in classical_checks',lambda:v.classical_checks(v.geometry(2,1,mp.mpf('.5')),5,mp.mpf('1e-40')))
mp.ellipfun=oldfun

# Execute the exact archived near function AST without importing sympy or running
# either historical suite. This proves the particular reported vulnerability.
h=a.historical/'independent_review/independent_check.py';tree=ast.parse(h.read_text())
near=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='near')
historical=[]
for optimize in [0,1]:
    for bad in [mp.mpf(1),mp.nan]:
        env={'mp':mp,'worst':mp.mpf(0),'numeric':Counter()}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[near],type_ignores=[])),str(h),'exec',optimize=optimize),env)
        accepted=True
        try:env['near'](bad,0,'injected')
        except AssertionError:accepted=False
        if accepted != bool(optimize):raise RuntimeError('Historical near behavior disagrees')
        historical.append({'function':'near','optimize':optimize,'input':str(bad),'accepted':accepted,'worst':str(env['worst'])})

hc=a.historical/'check_candidate.py';tree=ast.parse(hc.read_text())
fold=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='max' and 'qplus' in ast.unparse(n))
env={'mp':mp,'maxerr':mp.mpf(0),'qplus':[mp.nan],'formula':mp.mpf(1)}
exec(compile(ast.fix_missing_locations(ast.Module(body=[fold],type_ignores=[])),str(hc),'exec'),env)
if env['maxerr']!=0:raise RuntimeError('Candidate historical NaN mask not reproduced')
print(json.dumps({'status':'PASS','optimized':bool(sys.flags.optimize),'extra_current_rejections':len(done),'rejections':done,
 'historical_near_AST_execution':historical,'historical_candidate_exact_fold_maxerr':str(env['maxerr']),
 'bindings':{str(x.name):hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),a.verifier,h,hc]}},indent=2,allow_nan=False))
