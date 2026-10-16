#!/usr/bin/env python3
"""Exact symbolic checks accompanying EULER_AND_MELLIN.md; not a proof substitute."""
import json
from pathlib import Path
import sympy as s
X,U,V,K,p=s.symbols('X U V K p')
den=(1-X*U)*(1-X*V)
g=X**2*U*V/den
raw=s.cancel(den*(1+(K/X-1)*g))
expected=1-X*U-X*V+X*K*U*V
checks={
 'corrected_swap_local_polynomial': s.cancel(raw-expected)==0,
 'collision_prime_divides_h':s.cancel(1+(p-1)/(p-1)**2-p/(p-1))==0,
 'collision_prime_not_divides_h':s.cancel(1-1/(p-1)**2-p*(p-2)/(p-1)**2)==0,
 'odd_h_prime_two_zero':s.cancel((1-1/(p-1)**2).subs(p,2))==0,
 'h_series_residue_local_factor_at_k_1':s.cancel((1+(K/X-1)*g).subs(K,X)-1)==0,
}
assert all(checks.values()), checks
out={"status":"PASS","method":"exact SymPy rational-function simplification","checks":checks,
 "identifications":{"X":"p^(-1)","U":"p^(-u)","V":"p^(-v)","K":"p^(-k)"},
 "scope":"Local polynomial and collision checks only; convergence and contour proofs are in the authored note."}
Path(__file__).with_name('LOCAL_ALGEBRA_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
