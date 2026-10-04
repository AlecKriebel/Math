#!/usr/bin/env python3
"""Exact symbolic controls of the degeneration obstruction, over Z."""
import json,pathlib,platform
import sympy as s
x,y,z,t=s.symbols('x y z t');F=s.Matrix([[x*x-z*z,y*y-z*z,x*y,x*z,y*z]])
L=s.Matrix([[0,0,0,z,y],[0,x,0,-z,0],[-z,-y,-z,0,-x],[y,z,0,-x,0],[0,0,x,y,z]])
r=s.Matrix([-x*x+z*z,-y*z,y*y-z*z,-x*y,x*z])
assert all(s.expand(v)==0 for v in F*L)
assert all(s.expand(v)==0 for v in L*r)
assert s.expand(L[:4,:4].det()-x*y*z*z)==0
assert s.gcd_list(list(r))==1
assert s.expand(1-(1+3*t+t*t)*(1-t)**3)==5*t*t-5*t**3+t**5
G=s.groebner(list(F),x,y,z,order='lex');expected=[x*x-z*z,x*y,x*z,y*y-z*z,y*z,z**3]
assert [v.as_expr() for v in G.polys]==expected
out={'field':'identities over Z; proof valid over every field','generators':[str(f) for f in F], 'linear_syzygy_matrix':[[str(v) for v in row] for row in L.tolist()], 'second_syzygy':[str(v) for v in r], 'rank_four_minor':str(x*y*z*z), 'groebner_basis':[str(v) for v in expected], 'ideal_hilbert_numerator':'5*t**2-5*t**3+t**5', 'quotient_hilbert_series':'1+3*t+t**2','python':platform.python_version(),'sympy':s.__version__}
p=pathlib.Path(__file__).resolve().parent/'symbolic-results.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
