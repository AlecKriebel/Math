#!/usr/bin/env python3
"""Second implementation: symbolic CRT, resultants and modular irreducibility."""
import itertools
import json
from pathlib import Path
import sympy as s

x,a=s.symbols('x a')
data=json.loads(Path(__file__).with_name('results.json').read_text())
ms=[1,2,3,4,6]
mods=[s.Poly(s.cyclotomic_poly(m,x),x,domain=s.QQ) for m in ms]
P=s.Poly(s.prod(h.as_expr() for h in mods),x,domain=s.QQ)
basis=[(P.exquo(h)*s.invert(P.exquo(h),h)).rem(P) for h in mods]
options=[[1,-1],[1,-1],[1,-1,x,-x,x+1,-x-1],[1,-1,x,-x],[1,-1,x,-x,x-1,1-x]]
rs=[]
for v in itertools.product(*options):
    r=sum((b*s.Poly(c,x,domain=s.QQ) for b,c in zip(basis,v)),s.Poly(0,x,domain=s.QQ)).rem(P)
    if all(c.q==1 for c in r.all_coeffs()):rs.append(r)
assert len(rs)==24
asc=lambda p: [int(c) for c in reversed(s.Poly(p,x).all_coeffs())]
poly=lambda c: sum(v*x**i for i,v in enumerate(c))
def A(n,f):
    h=s.cyclotomic_poly(n,x)
    # Put the higher-degree polynomial first, then explicitly normalize the order.
    return int((-1)**(s.degree(f,x)*s.degree(h,x))*s.resultant(f,h,x))
expected={tuple(z['residue']) for z in data['d9_quartic_certificates']}
assert {tuple(asc(r)) for r in rs}==expected
assert {tuple(asc(r)) for r in rs if r.degree()==7 and r.LC()==1}=={tuple(r) for r in data['d7_all_candidates_for_E_ge_6']}
checks=0
for z in data['d9_quartic_certificates']:
    f=P.as_expr()*(x+a)+poly(z['residue'])
    q=s.Poly(s.resultant(s.cyclotomic_poly(5,x),f,x)-1,a)
    assert [int(c) for c in reversed(q.all_coeffs())]==z['quartic']
    roots=sorted(int(t) for t in s.polys.polytools.ground_roots(q) if t.q==1)
    assert roots==z['integer_roots'];checks+=1
for z in data['d8_C5_survivors']:
    f=poly(z['f'])
    assert [A(n,f) for n in range(1,9)]==z['norms_Res_Phi_f'];checks+=8
for z in data['d9_C5_survivors']:
    assert int(s.resultant(s.cyclotomic_poly(7,x),poly(z['f']),x))==z['C7'];checks+=1
for z in data['witnesses']:
    f=poly(z['f']);assert s.Poly(f,x,modulus=z['prime']).is_irreducible
    assert [A(n,f) for n in range(1,z['E0']+2)]==z['norms_Res_Phi_f'];checks+=z['E0']+1
# Independent finite diagnostics for the proved all-order root-of-unity formula.
root_checks=0
for m in range(2,81):
    Q=max(int(p)**int(e) for p,e in s.factorint(m).items())
    first=m//Q;f=s.cyclotomic_poly(m,x)
    assert first-1<int(s.totient(m))
    for n in range(1,first+1):
        b=int(s.resultant(x**n-1,f,x))
        assert (abs(b)==1)==(n<first);root_checks+=1
print('PASS: symbolic CRT, 24 exact quartics, complete integer roots, witness irreducibility.')
print(f'Exact symbolic quartic/resultant checks: {checks}.')
print(f'Root-of-unity resultant controls: {root_checks} for orders 2 through 80.')
print('Full target remains unsolved; only the stated scoped results are certified.')
