#!/usr/bin/env python3
"""Adversarial exact positive-scaling and conservation-boundary checks.
Uses only the independent reaction reconstruction created in this audit.
"""
import itertools,json
from pathlib import Path
import sympy as s
from independent_algebra_check import model,hurwitz,check,COUNTS
rows=[]
for m in (3,4,5,7):
 for a,b in ((s.Rational(1,10**8),s.Integer(10**8)),(s.Integer(10**8),s.Rational(1,10**8)),(s.Rational(1,10**8),s.Rational(2,10**8))):
  h=[s.Integer(10)**((-1)**i*(3*i+1)) for i in range(m+1)]
  A=model(m,a,b)[4];J=A*s.diag(*h)
  for k in range(1,min(m,5)):
   for I in itertools.combinations(range(m+1),k):
    check(hurwitz(J.extract(I,I)),'extreme_exact_principal_hurwitz',(m,a,b,I))
  rows.append(dict(m=m,a=str(a),b=str(b),h=[str(i) for i in h]))
lam=s.symbols('lam')
for m in range(3,9):
 A=model(m)[4];nu=m-2
 H=s.diag(*([s.Integer(1)]*m+[s.Rational(1,8*nu)]));J=A*H
 chi=J.charpoly(lam).as_expr()
 check(J.rank()==m,'T_equal_one_rank')
 check(s.expand(chi).coeff(lam)==0,'T_equal_one_nonsimple_zero')
 Hlow=s.diag(*([s.Integer(1)]*m+[s.Rational(1,16*nu)]));Jlow=A*Hlow
 check(s.expand(Jlow.charpoly(lam).as_expr()).coeff(lam)<0,'T_below_one_positive_real_root_sign')
out=dict(status='PASS',checks=COUNTS,extreme_scalings=rows,conservation_boundary_dimensions=list(range(3,9)),interpretation='T(H)=1 has a nonsimple conservation zero; T(H)<1 has a positive real eigenvalue by characteristic-polynomial sign.')
Path('boundary_stress_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
