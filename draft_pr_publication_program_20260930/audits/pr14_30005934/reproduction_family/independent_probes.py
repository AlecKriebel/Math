#!/usr/bin/env python3
"""New exact adversarial checks, independent of supplied computation code.

Run from repository root:
  .venv/bin/python draft_pr_publication_program_20260930/audits/pr14_30005934/reproduction_family/independent_probes.py

These checks establish finite algebra and selected examples; they cannot prove
the stochastic graph-norm approximation, conditional laws, or imported theorem.
"""
from datetime import datetime, timezone
from fractions import Fraction
import json
from pathlib import Path
import sys
import sympy as sp


results = []


def exact_zero(value):
    if isinstance(value, sp.MatrixBase):
        return all(sp.cancel(entry) == 0 for entry in value)
    return sp.cancel(value) == 0


def record(name, **evidence):
    results.append({'name': name, 'passed': True, **evidence})


# Universal 2x2 identities use unrestricted entries, not positive commuting
# assumptions. Invertibility is formal here; PSD inputs guarantee it later.
p, q, r, u, w, z = sp.symbols('p q r u w z')
Cgeneric = sp.Matrix([[p, q], [q, r]])
vgeneric = sp.Matrix([[u, w], [w, z]])
Egeneric = sp.eye(2) + 2*Cgeneric*vgeneric
Hgeneric = vgeneric*Egeneric.inv()
assert exact_zero(Hgeneric-Hgeneric.T)
assert exact_zero(Hgeneric-(sp.eye(2)+2*vgeneric*Cgeneric).inv()*vgeneric)
assert exact_zero(Egeneric.det()-(sp.eye(2)+2*vgeneric*Cgeneric).det())
record('universal_2x2_resolvent_symmetry_and_equivalent_orders')

a, d, e, f = sp.symbols('a d e f')
Rgeneric = sp.Matrix([[a, d], [e, f]])
vfactored = Rgeneric*Rgeneric.T
# This intertwining identity proves the square-root resolvent formula whenever
# the two inverses exist; its matrix polynomial form extends to any dimension.
assert exact_zero((sp.eye(2)+2*vfactored*Cgeneric)*Rgeneric
                  -Rgeneric*(sp.eye(2)+2*Rgeneric.T*Cgeneric*Rgeneric))
assert exact_zero((sp.eye(2)+2*Rgeneric.T*Cgeneric*Rgeneric).det()
                  -(sp.eye(2)+2*Cgeneric*vfactored).det())
record('universal_factor_pushthrough_and_sylvester_determinant')

# An entirely different nonnormal stable generator. Put x=e^{-t}; integration
# uses ds=-dx/x, so every identity stays rational/polynomial and exact.
x, y = sp.symbols('x y', positive=True)
A = sp.Matrix([[-2, 3], [0, -1]])
Q = sp.Matrix([[2, 1], [1, 3]])
S = sp.Matrix([[x*x, 3*(x-x*x)], [0, x]])
assert exact_zero(-x*sp.diff(S,x)-A*S)
assert S.subs(x,1) == sp.eye(2)
Sy = S.subs(x,y)
C = (Sy.T*Q*Sy/y).applyfunc(lambda entry: sp.integrate(entry,(y,x,1)))
assert exact_zero(-x*sp.diff(C,x)-S.T*Q*S)
wrong_C = (Sy*Q*Sy.T/y).applyfunc(lambda entry: sp.integrate(entry,(y,x,1)))
assert not exact_zero(C-wrong_C)
record('stable_nonnormal_semigroup_and_covariance_orientation', generator=str(A))

L = sp.Matrix([[1, 2], [2, -1]])
D = sp.eye(2)+2*L.T*C*L
psi = S*L*D.inv()*L.T*S.T
psi_prime = -x*sp.diff(psi,x)
assert exact_zero(psi_prime-A*psi-psi*A.T+2*psi*Q*psi)
assert exact_zero(-x*sp.diff(D.det(),x)/(2*D.det())-sp.trace(Q*psi))
assert exact_zero(psi.subs(x,1)-L*L.T)
record('stable_nonnormal_symbolic_riccati_and_logdet')

X = sp.Matrix([[5, 2], [2, 3]])
alpha = sp.Rational(7,3)
psihalf = psi.subs(x,sp.Rational(1,2))
dpsihalf = psi_prime.subs(x,sp.Rational(1,2))
qv = 4*sp.trace(X*psihalf*Q*psihalf)
phi_prime = alpha*sp.trace(Q*psihalf)
drift_forward_X = alpha*Q + X*A + A.T*X
# For psi_{T-s}, the exponent's time contribution is +psi'_r, +phi'_r.
backward_exponent_drift = phi_prime+sp.trace(dpsihalf*X)-sp.trace(psihalf*drift_forward_X)
assert exact_zero(backward_exponent_drift+qv/2)
bad_orientation = phi_prime+sp.trace(dpsihalf*X)-sp.trace(psihalf*(alpha*Q+A*X+X*A.T))
bad_clock = -phi_prime-sp.trace(dpsihalf*X)-sp.trace(psihalf*drift_forward_X)
assert not exact_zero(bad_orientation+qv/2)
assert not exact_zero(bad_clock+qv/2)
assert not exact_zero(dpsihalf-A.T*psihalf-psihalf*A+2*psihalf*Q*psihalf)
assert not exact_zero(dpsihalf-A*psihalf-psihalf*A.T-2*psihalf*Q*psihalf)
assert not exact_zero(backward_exponent_drift+qv/4)
record('backward_ito_drift_cancellation_and_five_mutations_rejected',
       qv=str(qv), adjoint_error_residual=str(sp.cancel(bad_orientation+qv/2)),
       time_error_residual=str(sp.cancel(bad_clock+qv/2)))

# Actual symmetric square-root orientation, checked universally in dimension
# two with no positivity restriction. Positivity is only needed to interpret
# the factors as roots, not for this polynomial coefficient identity.
r1,r2,r3,t1,t2,t3,v1,v2,v3=sp.symbols('r1 r2 r3 t1 t2 t3 v1 v2 v3')
Rroot=sp.Matrix([[r1,r2],[r2,r3]])
Troot=sp.Matrix([[t1,t2],[t2,t3]])
vtest=sp.Matrix([[v1,v2],[v2,v3]])
coefficients=sp.zeros(2)
for i in range(2):
    for j in range(2):
        E=sp.zeros(2); E[i,j]=1
        coefficients[i,j]=sp.trace(vtest*(Rroot*E*Troot+Troot*E.T*Rroot))
assert exact_zero(coefficients-2*Rroot*vtest*Troot)
assert exact_zero(sum(k*k for k in coefficients)
                  -4*sp.trace(Rroot*Rroot*vtest*Troot*Troot*vtest))
record('universal_symmetric_root_HS_representer_and_variance')

# Arbitrary positive factors need not be symmetric square roots. They define
# the same covariance X=RR^T, Q=TT^T, and allow each Brownian direction to be
# evaluated directly without assuming a coefficient formula.
for n in (1,2,4):
    R = sp.Matrix(n,n,lambda i,j: (i+2 if i==j else (1 if j==i+1 else 0)))
    T = sp.Matrix(n,n,lambda i,j: (j+3 if i==j else (-1 if i==j+1 else 0)))
    v = sp.Matrix(n,n,lambda i,j: (i+1)*(j+1) if i!=j else -(i+1))
    XX, QQ = R*R.T, T*T.T
    coordinates = []
    for i in range(n):
        for j in range(n):
            E = sp.zeros(n); E[i,j]=1
            # With arbitrary noise factor R E T^T, the symmetric companion is
            # T E^T R^T. The calculation does not import a formula from either
            # supplied script.
            coordinates.append(sp.trace(v*(R*E*T.T+T*E.T*R.T)))
    variance = sum(c*c for c in coordinates)
    assert variance == 4*sp.trace(XX*v*QQ*v)
    assert variance != 2*sp.trace(XX*v*QQ*v)
    assert variance != sp.trace(XX*v*QQ*v)
    if n>1:
        wrong = sum(sp.trace(v*(R*sp.eye(n)[:,i]*sp.eye(n)[j,:]*T.T))**2
                    for i in range(n) for j in range(n))
        assert wrong == variance/4
    record('all_brownian_matrix_directions_n'+str(n),
           basis_directions=n*n, quadratic_variation=str(variance))

# Noncommuting rank 0/1/2/3 examples, including an independently chosen
# nonsymmetric factor. In positive inputs all determinants are positive.
C3 = sp.Matrix([[3,1,1],[1,4,-1],[1,-1,5]])
b3 = sp.Matrix([[4,1,-1],[1,3,1],[-1,1,3]])
assert all(C3[:k,:k].det()>0 and b3[:k,:k].det()>0 for k in (1,2,3))
factors = [sp.zeros(3,1),sp.Matrix([[1],[2],[-1]]),
           sp.Matrix([[1,0],[1,2],[-1,1]]),
           sp.Matrix([[1,1,0],[0,2,1],[1,0,2]])]
for R in factors:
    v=R*R.T
    factor_D=sp.eye(R.cols)+2*R.T*C3*R
    ordered_E=sp.eye(3)+2*C3*v
    factor_H=R*factor_D.inv()*R.T
    ordered_H=v*ordered_E.inv()
    assert factor_D.det()==ordered_E.det()>0
    assert factor_H==ordered_H==ordered_H.T
    assert sp.trace(b3*factor_H)==sp.trace(b3*ordered_H)
    if v.rank()>0:
        assert not exact_zero(C3*v-v*C3)
        wrong_H=ordered_E.inv()*v
        assert not exact_zero(ordered_H-wrong_H)
        assert not exact_zero(sp.trace(b3*(ordered_H-wrong_H)))
    record('noncommuting_compression_rank_'+str(v.rank()),
           determinant=str(factor_D.det()),
           exponent_trace=str(sp.trace(b3*ordered_H)))

# Genuine noninjective C0 left shift on L2(0,1): S(t)f(r)=f(r+t)
# if r+t<1, and 0 otherwise. Q=I. For polynomial directions
# fi=(1-r)^2*r^i, i=0,1,2, the compression is a Gram matrix weighted by
# min(T,r). These directions lie in D(A^2): f(1)=f'(1)=0.
# Unlike the historical interval example, these directions overlap and give
# full non-diagonal covariance matrices.
r = sp.symbols('r', real=True)
for Ttime in (sp.Rational(1,10),sp.Rational(3,5),sp.Rational(1),sp.Rational(2)):
    cutoff=min(Ttime,1)
    gram=sp.Matrix(3,3,lambda i,j:
        sp.integrate(r**(i+j+1)*(1-r)**4,(r,0,cutoff))
        +(Ttime*sp.integrate(r**(i+j)*(1-r)**4,(r,cutoff,1)) if cutoff<1 else 0))
    minors=[gram[:k,:k].det() for k in (1,2,3)]
    assert all(m>0 for m in minors)
    record('noninjective_shift_overlap_gram_T_'+str(Ttime),
           matrix=str(gram), leading_minors=[str(m) for m in minors],
           directions='(1-r)^2*r^i, i=0,1,2; f(1)=f\'(1)=0',
           endpoint_semigroup_zero=bool(Ttime>=1))

# Completing the Gaussian integral for arbitrary positive integer m fixes
# alpha=m, determinant exponent -m/2, and covariance factor 2C. The proof
# for one summand is symbolic; summing independent squares multiplies powers.
v,c,mu,z=sp.symbols('v c mu z', positive=True)
lhs=v*z*z+(z-mu)**2/(2*c)
rhs=(1+2*c*v)/(2*c)*(z-mu/(1+2*c*v))**2+mu*mu*v/(1+2*c*v)
assert exact_zero(lhs-rhs)
for integer_alpha in (1,2,5):
    power=sp.Rational(integer_alpha,2)
    assert power==sum(sp.Rational(1,2) for _ in range(integer_alpha))
record('gaussian_square_normalization_alpha_over_two_scale_two_C',
       checked_integer_alphas=[1,2,5])

# Alpha=0 is not excluded by arithmetic. A zero-initial zero process has
# all transforms equal to 1. No sufficiency for other initial data is claimed.
assert (sp.eye(3)+2*C3).det()**sp.Integer(0)==1
assert sp.exp(-sp.trace(sp.zeros(3)))==1
record('alpha_zero_zero_initial_transform')

# Elementary negative-alpha witness: alpha=-2, c=1, b=1. Its scalar Laplace
# candidate (1+2r)*exp[-r/(1+2r)] exceeds 1 at r=1 since e^(1/3)<3/2<3.
# e^x <= 1/(1-x), 0<x<1, follows termwise from its power series.
assert Fraction(1,3)<1
assert 3*(1-Fraction(1,3))>1
record('negative_alpha_minus_two_laplace_upper_bound_violation',
       transform_at_r_1='3*exp(-1/3)>2>1',
       general_limit='alpha<0: (1+2cr)^(-alpha/2)*exp[-br/(1+2cr)] -> infinity for c>0,b>=0')

for alpha in [Fraction(-1),Fraction(0),Fraction(1,10),Fraction(1,2),
              Fraction(1),Fraction(3,2),Fraction(17,4),Fraction(801,8),Fraction(101)]:
    if alpha<0:
        outcome='negative_scalar_exclusion'
        n=1
    elif alpha.denominator==1:
        outcome='survives_parameter_sets_only'
        n=alpha.numerator+2
        for dim in (1,2,3,10,102):
            assert alpha in range(max(0,dim-1)) or alpha>=dim-1
    else:
        n=alpha.numerator//alpha.denominator+2
        assert alpha<n-1 and alpha not in range(n-1)
        outcome='excluded'
    record('parameter_arithmetic_alpha_'+str(alpha),
           dimension=n, outcome=outcome,
           theorem_status='parameter set assumed as stated in candidate; theorem not reproved here')

out={
    'generated_at_utc':datetime.now(timezone.utc).isoformat(),
    'source_head':'a81fa89f6613791dd55ad5b79bfe8053bd1585f3',
    'suite':'Fresh finite-rank algebra and deliberate mutation adversary',
    'python':sys.version,
    'sympy':sp.__version__,
    'arithmetic':'Exact symbolic and rational; no numerical tolerances',
    'passed':len(results), 'failed':0,
    'results':results,
    'scope_warning':'Cannot certify graph-norm stochastic approximation, regular conditional distributions, or imported noncentral Wishart theorem.',
}
Path(__file__).with_name('probe_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
