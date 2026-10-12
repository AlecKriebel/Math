#!/usr/bin/env python3
"""Independently inspect minimal repair and execute actual ck AST at both optimization levels."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import ast, hashlib, json

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'original_source_authentication_20261006/original_attempt'
NEW=ROOT.parent/'repaired_diagnostics_v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
proofs=[NEW/'ANALYTIC_CRITERION.md',NEW/'author_replay/ANALYTIC_CRITERION.md']
results=[]
for label,old,new,needle,replacement in [
    ('author',OLD/'verify.py',NEW/'verify.py',' assert bool(b),k',' if not bool(b):raise RuntimeError(k)'),
    ('old_independent',OLD/'review/independent_checks.py',NEW/'independent_checks.py',
     '    assert bool(value),name','    if not bool(value):raise RuntimeError(name)')]:
    original=old.read_text(); repaired=new.read_text()
    if original.count(needle)!=1 or original.replace(needle,replacement)!=repaired:
        raise RuntimeError('unexpected code difference: '+label)
    tree=ast.parse(repaired)
    if any(isinstance(n,ast.Assert) for n in ast.walk(tree)):
        raise RuntimeError('remaining assert')
    for version,path in [('original',old),('repaired',new)]:
        tree=ast.parse(path.read_text())
        ck=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ck')
        module=ast.Module(body=[ck],type_ignores=[])
        for optimize in [0,2]:
            ns={'C':Counter(),'checks':{}}
            exec(compile(module,str(path),'exec',optimize=optimize),ns)
            rejected=False; exception=None
            try: ns['ck']('forced_false_control',False)
            except (AssertionError,RuntimeError) as e:
                rejected=True; exception=type(e).__name__
            ns['ck']('true_control',True)
            counters=dict(ns['C']) or ns['checks']
            if counters.get('true_control')!=1: raise RuntimeError('true control count')
            if version=='repaired' and (not rejected or 'forced_false_control' in counters):
                raise RuntimeError('repaired false check counted or accepted')
            results.append({'label':label,'version':version,'compile_optimize':optimize,
                            'false_rejected':rejected,'exception':exception,'counts':counters,
                            'source_sha256':sha(path)})
if any(sha(p)!=sha(OLD/'ANALYTIC_CRITERION.md') for p in proofs):
    raise RuntimeError('proof changed')

# Exact counterexample to the discarded auxiliary q chart being spacelike.
a,b,c=Q(1,10000),Q(1,10),Q(1)
sp2,q2=Q(999,1000),Q(1,36)
f2=a*sp2+b*(1-sp2); h2=a*(1-sp2)+b*sp2
d2=(a-b)**2*sp2*(1-sp2); k2=c*f2/(a*b); den=1+q2*k2
e=f2/den+2*d2*q2*k2/(f2*den**2)+(h2*q2*k2-c)*q2*k2*d2/(f2*f2*den**3)
if not e<0: raise RuntimeError('auxiliary chart counterexample')
out={'status':'PASS_MINIMAL_GUARD_REPAIR','proof_sha256':sha(OLD/'ANALYTIC_CRITERION.md'),
     'proof_bytes_unchanged':True,'code_difference':'Exactly one assert-to-RuntimeError truth guard per checker; all other source bytes identical.',
     'compiled_actual_function_controls':results,
     'auxiliary_q_chart_exact_negative_metric':{'a':str(a),'b':str(b),'c':str(c),
        'sin_phi_squared':str(sp2),'q_squared':str(q2),'g_phi_phi':str(e)},
     'scope':'Repairs optimization-dependent truth enforcement. It does not expand finite diagnostic checks into a global mathematical certificate.'}
(ROOT/'REPAIR_ASSESSMENT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
