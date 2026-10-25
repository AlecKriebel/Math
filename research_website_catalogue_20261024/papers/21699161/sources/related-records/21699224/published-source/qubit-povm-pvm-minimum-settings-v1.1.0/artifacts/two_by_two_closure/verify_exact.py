#!/usr/bin/env python3
"""Independent exact checks for the two-setting qubit POVM/PVM closure dossier.

This verifier checks the algebraic certificate identities.  The dimension and
convexity arguments remain human-readable finite-dimensional proofs in the dossier.
No floating-point arithmetic is used.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import sympy as sp


def check_zero(name: str, expr) -> None:
    z = sp.simplify(expr)
    if z != 0:
        raise AssertionError(f"{name} failed: {z}")
    print(f"[PASS] {name}")


def check_matrix_zero(name: str, M: sp.Matrix) -> None:
    M = M.applyfunc(sp.simplify)
    if M != sp.zeros(*M.shape):
        raise AssertionError(f"{name} failed:\n{M}")
    print(f"[PASS] {name}")


# ---------------------------------------------------------------------------
# 1. Local Lorentz metric and the four-parameter affine family.
# ---------------------------------------------------------------------------
a,b,c,d = sp.symbols('a b c d')
e = a+b+c+d-sp.Rational(1,2)
g = sp.Matrix([
    [0, sp.Rational(1,2), a, b],
    [sp.Rational(1,2), 0, c, d],
    [a, c, 0, e],
    [b, d, e, 0],
])
u = sp.Matrix([1,1,0,0])
v = sp.Matrix([1,1,-1,-1])
rs = [sp.eye(4)[:,i] for i in range(4)] + [v]
for i,r in enumerate(rs,1):
    check_zero(f"metric null ray r{i}", (r.T*g*r)[0])
check_zero("metric normalization u^T g u = 1", (u.T*g*u)[0]-1)

A1,B1,C1,D1 = sp.symbols('A1 B1 C1 D1')
H = sp.Matrix([
    [0,0,A1,B1],
    [0,0,C1,D1],
    [A1,C1,0,A1+B1+C1+D1],
    [B1,D1,A1+B1+C1+D1,0],
])
x0,x1,x2,x3 = sp.symbols('x0 x1 x2 x3')
x = sp.Matrix([x0,x1,x2,x3])
phi = sp.Matrix([
    x2*(x0+x3),
    x3*(x0+x2),
    x2*(x1+x3),
    x3*(x1+x2),
])
check_zero("metric derivative equals 2 phi pairing",
           (x.T*H*x)[0]-2*(A1*phi[0]+B1*phi[1]+C1*phi[2]+D1*phi[3]))

# ---------------------------------------------------------------------------
# 2. Quadratic null-ray map: exact rational inverse and exceptional fibers.
# ---------------------------------------------------------------------------
P0 = x2*(x0+x3)
P1 = x3*(x0+x2)
P2 = x2*(x1+x3)
P3 = x3*(x1+x2)
Delta0 = P0-P1
Delta1 = P2-P3
Delta2 = P0-P2
Delta3 = P1-P3
Minor = sp.expand(P0*P3-P1*P2)
Psi = sp.Matrix([
    Delta0*Delta2*Delta3,
    Delta1*Delta2*Delta3,
    Minor*Delta2,
    Minor*Delta3,
])
common = x2*x3*(x2-x3)*(x0-x1)**2
check_matrix_zero("Cremona inverse identity", Psi-common*x)
check_zero("minor identity", Minor-x2*x3*(x0-x1)*(x2-x3))

# x2=0 exceptional fiber and its only cross-branch null point.
t = sp.symbols('t')
z = sp.Matrix([-1,-1,t,1])
check_zero("x2=0 cross-branch null factor",
           sp.factor((z.T*g*z)[0]-(1-2*(b+d))*(1-t)))
z = sp.Matrix([-1,-1,1,t])
check_zero("x3=0 cross-branch null factor",
           sp.factor((z.T*g*z)[0]-(1-2*(a+c))*(1-t)))

# Direct exceptional branches: t=0 is the base ray and the remaining factor is linear.
t,TB,TD,TA,TC = sp.symbols('t TB TD TA TC')
z = sp.Matrix([t*TB,t*TD,0,1])
check_zero("x2=0 direct-branch null polynomial",
           sp.expand((z.T*g*z)[0]-(t**2*TB*TD+2*t*(b*TB+d*TD))))
z = sp.Matrix([t*TA,t*TC,1,0])
check_zero("x3=0 direct-branch null polynomial",
           sp.expand((z.T*g*z)[0]-(t**2*TA*TC+2*t*(a*TA+c*TC))))

# x0=x1 exceptional plane.  The resultant has the base root q=-1 and one residual root.
p,q,TA,TB = sp.symbols('p q TA TB')
N_equal01 = 1+2*(a+c)*p+2*(b+d)*q+2*e*p*q
R_equal01 = TB*p*(1+q)-TA*q*(1+p)
res01 = sp.factor(sp.resultant(N_equal01,R_equal01,p))
expected01 = -(q+1)*(TB+q*(TA*(2*a+2*c-1)+2*TB*(b+d)))
check_zero("x0=x1 exceptional-fiber resultant", res01-expected01)
check_zero("x0=x1 base-root null factor",
           sp.factor(N_equal01.subs(q,-1)-(1-2*(b+d))*(1+p)))

# x2=x3 exceptional plane.
p,q,TA,TC = sp.symbols('p q TA TC')
N_equal23 = p*q+2*(a+b)*p+2*(c+d)*q+2*e
R_equal23 = TC*(p+1)-TA*(q+1)
res23 = sp.factor(sp.resultant(N_equal23,R_equal23,p))
expected23 = -(q+1)*(TA*q+2*TA*(a+b)+2*TC*(c+d)-TC)
check_zero("x2=x3 exceptional-fiber resultant", res23-expected23)
check_zero("x2=x3 base-root null factor",
           sp.factor(N_equal23.subs(q,-1)-(2*(a+b)-1)*(p+1)))

# If z0=z1=0 in the x2=x3 target case, strict e>0 forces a base ray.
z2s,z3s = sp.symbols('z2s z3s')
z = sp.Matrix([0,0,z2s,z3s])
check_zero("x2=x3 cross-branch null monomial",
           sp.expand((z.T*g*z)[0]-2*e*z2s*z3s))

# The only possible 'identically linear equation' degeneracies factor into forbidden
# strict-boundary factors.
AA,BB = sp.symbols('AA BB')
check_zero("exceptional degeneracy factorization",
           (2*AA-1)*(2*BB-1) - (4*AA*BB-2*AA-2*BB+1))

# ---------------------------------------------------------------------------
# 3. Exact pure-state Lorentz relation on an algebraic trine example.
# ---------------------------------------------------------------------------
I2 = sp.eye(2)
sq2 = sp.sqrt(2)
sq3 = sp.sqrt(3)
X = sp.Matrix([[0,1],[1,0]])
Y = sp.Matrix([[0,-sp.I],[sp.I,0]])
Z = sp.diag(1,-1)
sigmas = [X,Y,Z]
eta = sp.diag(1,-1,-1,-1)

def hvec(M: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([sp.trace(M)/2] + [sp.trace(M*S)/2 for S in sigmas])

E = [(I2+Z)/2,(I2-Z)/2,
     (I2+X)/3,
     (I2-X/2+sq3*Y/2)/3]
E5 = I2-E[2]-E[3]
EE = sp.Matrix.hstack(*[hvec(M) for M in E])
gtri = sp.simplify(EE.T*eta*EE)
# Bob uses the same five effects and |Phi+>; transpose is the y-reflection.
Tref = sp.diag(1,1,-1,1)
L = Tref/2
P = sp.simplify(2*EE.T*L*EE)
Q = sp.simplify(gtri.inv())
check_matrix_zero("pure-state conformal Lorentz relation",
                  sp.simplify(P.T*Q*P-gtri))  # 4|det(I/sqrt2)|^2=1
check_zero("trine fifth effect normalization", sp.trace((E5-(I2-X/2-sq3*Y/2)/3).H*(E5-(I2-X/2-sq3*Y/2)/3)))

# ---------------------------------------------------------------------------
# 4. Weighted Hessian square completion, checked over exact rational matrices.
# ---------------------------------------------------------------------------
# This identity is dimension-independent.  A nontrivial exact 4x4 instance catches
# transpose/order/sign mistakes without sharing the proof's coordinate derivation.
g0 = sp.Matrix([[2,1,0,0],[1,3,1,0],[0,1,4,1],[0,0,1,5]])
Q0 = g0.inv()
P0m = sp.Matrix([[1,2,0,1],[0,1,1,0],[2,0,1,1],[1,1,0,2]])
dP = sp.Matrix([[1,0,2,0],[0,-1,0,1],[1,1,0,0],[0,1,-1,1]])
dg = sp.Matrix([[1,1,0,0],[1,0,1,0],[0,1,-1,1],[0,0,1,2]])
lam = [sp.Rational(2),sp.Rational(3),sp.Rational(5),sp.Rational(7),sp.Rational(11)]
Lam = sp.diag(*lam[:4])+lam[4]*(v*v.T)
# Expand F(eps)=sum lambda_r (P+eps dP)r)^T(g+eps dg)^-1(...)
eps = sp.symbols('eps')
Pe = P0m+eps*dP
Qe = (g0+eps*dg).inv()
Fe = sum(lam[i]*(Pe*rs[i]).dot(Qe*(Pe*rs[i])) for i in range(5))
second = sp.simplify(sp.diff(Fe,eps,2).subs(eps,0))
Delta = dP-dg*Q0*P0m
square = sp.simplify(2*sp.trace(Q0*Delta*Lam*Delta.T))
check_zero("weighted Hessian square completion", second-square)

# The five rank-one matrices r_i r_i^T are independent.
mu = sp.symbols('m0:5')
Lmu = sum((mu[i]*(rs[i]*rs[i].T) for i in range(5)), sp.zeros(4))
# off-diagonal (0,1) equals mu_5; then diagonal entries recover the rest.
check_zero("Lambda map offdiagonal witness", Lmu[0,1]-mu[4])
for i in range(4):
    check_zero(f"Lambda map diagonal witness {i}", Lmu[i,i]-(mu[i]+mu[4]))

# ---------------------------------------------------------------------------
# 5. Rank-zero deterministic simulation identities.
# ---------------------------------------------------------------------------
c12,c13,c23,a1,a2,a3,b1,b2,b3,tflow = sp.symbols(
    'c12 c13 c23 a1 a2 a3 b1 b2 b3 tflow')
d1=(b1-a1)/2; d2=(b2-a2)/2; d3=(b3-a3)/2
f12=tflow; f13=d1-tflow; f23=d2+tflow
Qflow=sp.Matrix([
    [0,c12/2+f12,c13/2+f13],
    [c12/2-f12,0,c23/2+f23],
    [c13/2-f13,c23/2-f23,0],
])
# Substitute the Gram row-sum identities c12+c13=a1+b1, etc.
subs_rows={c13:a1+b1-c12, c23:a2+b2-c12,
           a3+b3:(a1+b1-c12)+(a2+b2-c12)}
check_zero("flow row 1", sp.simplify(sum(Qflow[0,j] for j in range(3))-b1).subs(subs_rows))
check_zero("flow row 2", sp.simplify(sum(Qflow[1,j] for j in range(3))-b2).subs(subs_rows))
check_zero("flow column 1", sp.simplify(sum(Qflow[i,0] for i in range(3))-a1).subs(subs_rows))
check_zero("flow column 2", sp.simplify(sum(Qflow[i,1] for i in range(3))-a2).subs(subs_rows))
# The third row/column use c13+c23=a3+b3 and total a=total b.
expr_r3=sp.simplify(sum(Qflow[2,j] for j in range(3))-b3)
expr_c3=sp.simplify(sum(Qflow[i,2] for i in range(3))-a3)
expr_r3=expr_r3.subs(c23,a3+b3-c13).subs(b3,a1+a2+a3-b1-b2)
expr_c3=expr_c3.subs(c23,a3+b3-c13).subs(b3,a1+a2+a3-b1-b2)
check_zero("flow row 3", sp.simplify(expr_r3))
check_zero("flow column 3", sp.simplify(expr_c3))

# Exact trine rank-zero example: capacities 1/6, choose an oriented 3-cycle.
Qcycle=sp.Matrix([[0,sp.Rational(1,6),0],[0,0,sp.Rational(1,6)],[sp.Rational(1,6),0,0]])
for i in range(3):
    check_zero(f"trine cycle row {i}", sum(Qcycle[i,j] for j in range(3))-sp.Rational(1,6))
    check_zero(f"trine cycle col {i}", sum(Qcycle[j,i] for j in range(3))-sp.Rational(1,6))

print("\nAll exact algebraic closure checks passed.")
