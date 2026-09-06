#!/usr/bin/env python3
"""Reproduce certificate-label false acceptance without touching released files."""
import copy, importlib, json, pathlib, shutil, sys
from audit_driver import ENV, HERE, SOURCE, SCRATCH, run

if not __debug__: raise SystemExit('Run with assertions enabled')
root=SCRATCH/'variable_order'
if root.exists(): shutil.rmtree(root)
shutil.copytree(SOURCE,root)
p=root/'independent_verifier/improved_modulus_certificate.json'
payload=json.loads(p.read_text())
section=payload['homogeneous']
original=copy.deepcopy(section)
section['variables']=list(reversed(section['variables']))
p.write_text(json.dumps(payload,indent=2)+'\n')
sys.path.insert(0,str(root/'independent_verifier'))
import sympy as sp
x,z=sp.symbols('x z')
def interp(s):
    variables=[sp.Symbol(v) for v in s['variables']]
    return sp.expand(sum(sp.Rational(t['coefficient'])*sp.prod(v**k for v,k in zip(variables,t['powers'])) for t in s['terms']))
baseline=interp(original); mutant=interp(section)
y=sp.Symbol('y'); lam=x+sp.I*y; bar=x-sp.I*y
P=lambda v:v**4+12*v**3+42*v**2+47*v+16
R=lambda v:5*v**2+33*v+16
even=sp.Poly(sp.expand((1+lam)*(1+bar)*P(lam)*P(bar)-R(lam)*R(bar)),y)
if any(k[0]%2 for k,c in even.terms()): raise RuntimeError('Unexpected odd power')
actual=sp.expand(sum(c*z**(k[0]//2) for k,c in even.terms()))
if sp.expand(actual-baseline)!=0: raise RuntimeError('Original polynomial mismatch')
point={x:1,z:2}
if sp.expand(actual-mutant)==0: raise RuntimeError('mutation is not mathematical')
results={'original_variables':original['variables'],'mutated_variables':section['variables'],
 'point':{'x':1,'z':2},'original_polynomial_at_point':str(actual.subs(point)),
 'mutated_polynomial_at_point':str(mutant.subs(point)),
 'difference_at_point':str((mutant-actual).subs(point))}
results['direct_reader_status']=run('variable_order_direct',['python','independent_verifier/verify_mode_isolation.py'],root)
results['unchanged_table_aggregate_status']=run('variable_order_unchanged_table',['python','independent_verifier/frontier_verify_exposition_identities.py'],root,expected=1)
results['generator_status']=run('variable_order_generate',['python','computation/generate_tables.py'],root)
results['regenerated_table_aggregate_status']=run('variable_order_regenerated_table',['python','independent_verifier/verify_symbolic_certificates.py'],root)
results['mutated_header']=' & '.join([rf'$\deg_{{{v}}}$' for v in section['variables']]+['coefficient'])
results['header_found']=results['mutated_header'] in (root/'data/certificate_tables.tex').read_text()
expected=(results['direct_reader_status']==0 and results['unchanged_table_aggregate_status']!=0 and results['generator_status']==0 and results['regenerated_table_aggregate_status']==0 and results['header_found'])
if not expected: raise RuntimeError('witness changed: '+str(results))
(HERE/'VARIABLE_ORDER_WITNESS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
