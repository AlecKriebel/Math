#!/usr/bin/env python3
"""Exact checks of the obstruction examples; does not test or prove the full braid target."""
import json
from pathlib import Path
import sympy as s
x=s.symbols('x');I=s.eye(2)
U=s.Matrix([[1,1],[0,1]]);V=s.Matrix([[1,0],[-1,1]])
assert U*V*U==V*U*V
assert (U*V)**3==-I
assert ((2*U)*(2*V))**3==-64*I
assert (2*U).det()==(2*V).det()==4
A=s.diag(x,1);B=U
for k in range(-5,6): assert s.simplify(A**k*B*A**(-k)-s.Matrix([[1,x**k],[0,1]]))==s.zeros(2)
polys=[x-2,2*x-3,x*x-2,x*x+x+1,x**3-x-1]
for p in polys:
 P=s.Poly(p,x);word=I
 for (k,),c in P.terms():word=word*(A**k*B**int(c)*A**(-k))
 assert s.simplify(word-s.Matrix([[1,p],[0,1]]))==s.zeros(2)
 assert word!=I
 assert s.rem(word[0,1],p,x)==0
out={'scope':'Examples and identities only; no full-resolution or finite-word faithfulness certificate','braid_relation':True,'untwisted_center':'-I','twisted_center':'-64 I','central_kernel_control':True,'conjugation_identities':11,'algebraic_specialization_kernel_examples':len(polys),'all_passed':True,'sympy_version':s.__version__}
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
