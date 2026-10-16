#!/usr/bin/env python3
"""Exact finite-matrix consistency checks; not certification of stochastic analysis.
Run with Python 3.10+ and SymPy (tested 1.14.0). No network or numerical tolerance.
"""
import json
from pathlib import Path
import sympy as s


def zero(M):
    return all(s.cancel(e) == 0 for e in M)


A = s.Matrix([[0,1,0],[0,0,1],[0,0,0]])
Q = s.diag(2,3,5)
X = s.Matrix([[4,1,0],[1,2,1],[0,1,3]])
L = s.Matrix([[1,0],[0,1],[1,1]])
z = s.symbols('z', real=True)
S = s.eye(3) + z*A + z*z*A*A/2
Cpoly = (S.T*Q*S).applyfunc(lambda e:s.integrate(e,(z,0,z)))
St,C = S.subs(z,1),Cpoly.subs(z,1)
B = St*L
Bp = A*B
D = s.eye(2)+2*L.T*C*L
Dp = 2*B.T*Q*B
V = D.inv()
psi = B*V*B.T
psip = Bp*V*B.T+B*V*Bp.T-B*V*Dp*V*B.T
assert zero(psip-(A*psi+psi*A.T-2*psi*Q*psi))
assert not zero(psip-(A*psi+psi*A.T+2*psi*Q*psi))
assert s.trace(V*Dp)/2 == s.trace(Q*psi)
alpha=s.Rational(3,2)
phi_prime=alpha*s.trace(Q*psi)
exponent_drift = phi_prime+s.trace(psip*X)-alpha*s.trace(Q*psi)-s.trace(X*(A*psi+psi*A.T))
assert s.simplify(exponent_drift+2*s.trace(X*psi*Q*psi)) == 0

# Noncommuting covariance and Laplace-test matrix; use a rational factor R instead of sqrt(v).
J = s.Matrix([[1,0],[0,1],[0,0]])
R = s.Matrix([[1,1],[0,1]])
v=R*R.T
c=J.T*C*J
b=J.T*St.T*X*St*J
factor_form = R*(s.eye(2)+2*R.T*c*R).inv()*R.T
ordered_form = v*(s.eye(2)+2*c*v).inv()
assert zero(factor_form-ordered_form)
assert (s.eye(2)+2*R.T*c*R).det()==(s.eye(2)+2*c*v).det()
assert not zero(ordered_form-(s.eye(2)+2*c*v).inv()*v)

# The two smoothing orders are genuinely different, even before infinite-dimensional limits.
assert not zero(St.T*Q*St-St*Q*St.T)

results={
 'riccati_identity':'PASS',
 'corrupted_riccati_sign_rejected':'PASS',
 'logdet_derivative':'PASS',
 'ito_drift_cancellation':'PASS',
 'finite_rank_resolvent_compression':'PASS',
 'finite_rank_determinant_compression':'PASS',
 'corrupted_factor_order_rejected':'PASS',
 'operator_order_difference_detected':'PASS',
 'scale_compression_determinant':str(c.det()),
 'arithmetic':'exact symbolic/rational',
 'scope':'These checks do not certify moving stochastic tests, conditional laws, or the finite-dimensional distribution theorem.'
}
Path(__file__).with_name('check_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
