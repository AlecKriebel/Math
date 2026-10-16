#!/usr/bin/env python3
"""Independent exact algebra checks for the narrow Wishart obstruction.

Run: python independent_checks.py
Requires SymPy. These checks are diagnostics, not a proof of stochastic analysis.
"""
import json
from fractions import Fraction
from pathlib import Path
import sympy as sp

results = []

def record(name, **details):
    results.append({'name': name, 'passed': True, **details})

def zero_matrix(M):
    return all(sp.cancel(x) == 0 for x in M)

# Build semigroups and covariances independently from matrix exponentials and
# integration, rather than importing the author's construction/check script.
t, s = sp.symbols('t s', real=True, nonnegative=True)
cases = [
    ('zero_generator', sp.zeros(2), sp.Matrix([[2,1],[1,3]]), sp.Matrix([[1],[2]])),
    ('nonnormal_2d', sp.Matrix([[0,1],[0,0]]), sp.Matrix([[2,1],[1,3]]), sp.eye(2)),
    ('rectangular_3d', sp.Matrix([[0,1,0],[0,0,1],[0,0,0]]),
     sp.Matrix([[2,1,0],[1,3,1],[0,1,2]]), sp.Matrix([[1,0],[0,1],[1,1]])),
]
for name,A,Q,L in cases:
    S = (t*A).exp()
    Ss = S.subs(t,s)
    C = (Ss.T*Q*Ss).applyfunc(lambda x: sp.integrate(x,(s,0,t)))
    D = sp.eye(L.cols)+2*L.T*C*L
    psi = S*L*D.inv()*L.T*S.T
    assert zero_matrix(sp.diff(psi,t)-A*psi-psi*A.T+2*psi*Q*psi)
    assert sp.cancel(sp.diff(D.det(),t)/(2*D.det())-sp.trace(Q*psi)) == 0
    assert zero_matrix(psi.subs(t,0)-L*L.T)
    assert D.subs(t,0) == sp.eye(L.cols)
    record('riccati_'+name, dimension=A.rows, columns=L.cols)

# Coordinate evaluation of every Brownian matrix direction. R,T are actual
# symmetric positive square roots of X=R^2 and Q=T^2; v need not be positive.
for n in (1,2,3):
    R = sp.Matrix(n,n,lambda i,j: 2+i if i==j else 1)
    T = sp.Matrix(n,n,lambda i,j: 3+2*i if i==j else (-1 if abs(i-j)==1 else 0))
    v = sp.Matrix(n,n,lambda i,j: (-1)**(i+j)*(i+j+1))
    X,Q = R*R,T*T
    coeff = sp.zeros(n)
    for i in range(n):
        for j in range(n):
            E = sp.zeros(n); E[i,j]=1
            coeff[i,j] = sp.trace(v*(R*E*T+T*E.T*R))
    assert coeff == 2*R*v*T
    variance = sum(c*c for c in coeff)
    expected = 4*sp.trace(X*v*Q*v)
    assert variance == expected
    record('brownian_coordinates_'+str(n), variance=str(variance))

C = sp.Matrix([[2,1,0],[1,3,1],[0,1,2]])
b = sp.Matrix([[3,1,1],[1,2,0],[1,0,2]])
roots = [sp.zeros(3),sp.diag(1,0,0),sp.Matrix([[1,1,0],[1,2,1],[0,1,2]])]
for k,P in enumerate(roots):
    v=P*P
    D=sp.eye(3)+2*P*C*P
    E=sp.eye(3)+2*C*v
    assert D.det()==E.det()
    assert P*D.inv()*P == v*E.inv()
    # The noncentral factor must use this order; v and C need not commute.
    assert sp.trace(b*P*D.inv()*P)==sp.trace(b*v*E.inv())
    record('resolvent_rank_'+str(v.rank()), determinant=str(D.det()))

# A genuine infinite-dimensional noninjective C0 semigroup, represented by
# exact integrals on indicator directions. On L2(0,1), the left shift has
# C_T equal to multiplication by min(T,r) for Q=I. Every interval direction
# has positive covariance, even for T>=1 when S(T)=0.
r = sp.symbols('r', real=True)
intervals = [(sp.Rational(0),sp.Rational(1,4)),(sp.Rational(1,4),sp.Rational(1,2)),
             (sp.Rational(1,2),sp.Rational(1))]
for T in (sp.Rational(1,8),sp.Rational(1,2),sp.Rational(1),sp.Rational(2)):
    diag=[]
    for a,z in intervals:
        first=sp.integrate(r,(r,a,min(z,T))) if a<T else 0
        second=T*(z-max(a,T)) if z>T else 0
        value=sp.cancel((first+second)/(z-a))
        assert value>0
        diag.append(str(value))
    record('left_shift_T_'+str(T), compressed_covariance_diagonal=diag,
           endpoint_semigroup_zero=bool(T>=1))

# Direct normalization check against one real Gaussian square. If Z has
# mean m and variance c, completing the square gives exponent -m^2*v/(1+2cv)
# and determinant power -1/2, so alpha=1, scale=2c, noncentrality=m^2.
v,c,m,z=sp.symbols('v c m z',positive=True)
quadratic=sp.expand(v*z*z+(z-m)**2/(2*c))
completed=sp.expand((1+2*c*v)/(2*c)*(z-m/(1+2*c*v))**2+m*m*v/(1+2*c*v))
assert sp.cancel(quadratic-completed)==0
record('gaussian_normalization_alpha_1')

# Exact obstruction-dimension choices, including a large noninteger.
for alpha in (Fraction(1,10),Fraction(1,2),Fraction(3,2),Fraction(17,4),Fraction(801,8)):
    n=alpha.numerator//alpha.denominator+2
    assert alpha<n-1 and alpha.denominator!=1
    assert not (alpha in range(n-1) or alpha>=n-1)
    record('gindikin_exclusion_'+str(alpha), dimension=n)

out={'suite':'Independent Wishart algebra and boundary diagnostics',
     'arithmetic':'exact rational and symbolic (SymPy)',
     'passed':len(results), 'failed':0,
     'scope_warning':'Does not independently certify stochastic analytic steps or the imported distribution theorem.',
     'results':results}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
