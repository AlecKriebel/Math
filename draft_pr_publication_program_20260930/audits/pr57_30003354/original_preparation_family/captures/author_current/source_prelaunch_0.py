#!/usr/bin/env python3
"""Exact algebra/jet controls; the uniform estimates are proved in CANDIDATE.md."""
from pathlib import Path
from math import factorial
import hashlib,json
import sympy as S
x,y,rho,eps=S.symbols('x y rho eps',real=True,positive=True)
# Positivity assumptions on x,y only simplify radicals; identities are rational
# and hence hold for all real x,y by polynomial continuation.
a,b,c,d,q=S.symbols('a b c d q',real=True)
z=x+S.I*y
s2=x*x+y*y+rho*rho
rad=S.sqrt(s2)
L=S.log(s2)/2
checks={}
def ck(name,v):
    assert bool(v),name
    checks[name]='PASS'
def zero(f):return S.simplify(S.expand(f))==0
def euler(f):return x*S.diff(f,x)+y*S.diff(f,y)+rho*S.diff(f,rho)
# Beltrami-to-metric algebra, without differentiability or numerical sampling.
J=S.Matrix([[a+c,-b+d],[b+d,a-c]])
ck('jacobian_wirtinger',zero(J.det()-(a*a+b*b-c*c-d*d)))
muR=(a*c+b*d)/(a*a+b*b)
muI=(a*d-b*c)/(a*a+b*b)
M=S.Matrix([[1+muR,muI],[muI,1-muR]])
ck('metric_pullback_exact',all(zero(v) for v in J.T*J-(a*a+b*b)*(M.T*M)))
ck('metric_beltrami_determinant',zero((M.T*M).det()-(1-muR**2-muI**2)**2))
Tw=S.Matrix([[1,0],[q,1]])
ck('radial_twist_metric',Tw.T*Tw==S.Matrix([[1+q*q,q],[q,1]]))
ck('radial_twist_orientation',Tw.det()==1)
# Background curvature and radial correction identities.
for name,bg,expected in [('cigar',S.log(1+x*x+y*y)/2,2/(1+x*x+y*y)),('round',S.log(1+x*x+y*y)-S.log(2),S.Integer(1))]:
    lap=S.diff(bg,x,2)+S.diff(bg,y,2)
    ck(name+'_curvature',zero(S.exp(2*bg)*lap-expected))
H=S.hessian(rad,(x,y))
ck('radius_hessian',all(zero(v) for v in H-(S.eye(2)/rad-S.Matrix([x,y])*S.Matrix([[x,y]])/rad**3)))
ck('radius_hessian_determinant',zero(H.det()-rho**2/s2**2))
ck('radius_laplacian',zero(S.trace(H)-(x*x+y*y+2*rho*rho)/rad**3))
ck('radius_laplacian_lower_bound_difference',zero(S.trace(H)-1/rad-rho*rho/rad**3))
ck('radius_gradient_bound',zero(1-S.diff(rad,x)**2-S.diff(rad,y)**2-rho*rho/s2))
# All coordinate derivatives in these bounded degree families.
for k in range(1,5):
    for j in range(k+1):
        f=S.diff(L,x,j,y,k-j)
        ck(f'log_homogeneity_{k}_{j}',zero(euler(f)+k*f))
for r in range(1,5):
    w=z**(r+1)*L
    db=(S.diff(w,x)+S.I*S.diff(w,y))/2
    B=z**(r+2)/(2*s2)
    ck(f'bar_derivative_r{r}',zero(db-B))
    for k in range(r+1):
        for j in range(k+1):
            D=S.diff(B,x,j,y,k-j)
            ck(f'bar_derivative_homogeneity_{r}_{k}_{j}',zero(euler(D)-(r-k)*D))
# The top jet is exact, rather than a floating-point asymptotic.
for r in range(1,7):
    f=eps*x**(r+1)*S.log(x*x+rho*rho)/2
    jet=S.diff(f,x,r+1).subs(x,0)
    ck(f'fixed_top_jet_r{r}',zero(jet-eps*factorial(r+1)*S.log(rho)))
    ck(f'normalized_top_jet_r{r}',zero(jet.subs(eps,-1/S.log(rho))+factorial(r+1)))
# For r=1 the third derivatives have no logarithmic term and degree -1.
w=z*z*L
for j in range(4):
    D=S.diff(w,x,j,y,3-j)
    ck(f'critical_third_derivative_homogeneity_{j}',zero(euler(D)+D))
    ck(f'critical_third_derivative_no_log_{j}',not S.cancel(S.expand(D)).has(S.log))
# Chain rule for a nonlinear chart with explicit inverse, independently testing
# both the principal coefficient and the drift coefficient.
F=S.Matrix([x,y+x*x]);G=S.Matrix([x,y-x*x]);JF=F.jacobian([x,y]);Ji=JF.inv();A=Ji*Ji.T
B=S.Matrix([-sum(Ji[i,k]*sum(A[j,l]*S.diff(F[k],[x,y][j],[x,y][l]) for j in range(2) for l in range(2)) for k in range(2)) for i in range(2)])
for i,v in enumerate((x,y,x*x,x*y,y*y,x**3+y**3)):
    LHS=sum(S.diff(v.subs({x:G[0],y:G[1]},simultaneous=True),u,2) for u in (x,y)).subs({x:F[0],y:F[1]},simultaneous=True)
    RHS=sum(A[j,k]*S.diff(v,[x,y][j],[x,y][k]) for j in range(2) for k in range(2))+sum(B[j]*S.diff(v,[x,y][j]) for j in range(2))
    ck(f'pulled_laplacian_chain_rule_{i}',zero(LHS-RHS))
result={'status':'PASS','assertions':len(checks),'sympy_version':S.__version__,'candidate_sha256':hashlib.sha256(Path(__file__).with_name('CANDIDATE.md').read_bytes()).hexdigest(),'scope':'Exact bounded algebra, homogeneity, curvature-sign identities and jets. These do not replace the all-r estimates, completeness or uniqueness proof.','checks':checks}
print(json.dumps(result,indent=2,sort_keys=True))
