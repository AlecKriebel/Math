#!/usr/bin/env python3
"""Independent finite controls for the published note; not a proof of its theorems.

Written from the displayed equations, without importing the publication's checks.
Exact polynomial identities use SymPy. Angular checks are numerical diagnostics.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import math
import numpy as np
import sympy as S
from scipy.integrate import quad
from scipy.special import expit

OUT = Path(__file__).resolve().parent
checks = []

def record(name, passed, evidence, kind="exact"):
    checks.append(dict(name=name, passed=bool(passed), evidence=evidence, kind=kind))
    if not passed:
        raise AssertionError(name + ": " + str(evidence))

x, y, e = S.symbols("x y e", real=True)

def sphere_integral(poly):
    """Integral over S^1 divided by pi, via exact beta moments."""
    total = S.Integer(0)
    for (i, j), coefficient in S.Poly(S.expand(poly), x, y).terms():
        if i % 2 or j % 2:
            continue
        a, b = i // 2, j // 2
        total += coefficient * S.Rational(
            2 * math.factorial(2*a) * math.factorial(2*b),
            4**(a+b) * math.factorial(a) * math.factorial(b) * math.factorial(a+b))
    return S.simplify(total)

g11, g12, g22 = S.symbols("g11 g12 g22", real=True)
G = S.Matrix([[g11, g12], [g12, g22]])
w = S.Matrix([x,y])
stress = ((w.T*G*w)[0] * (4*w*w.T-2*S.eye(2))).applyfunc(sphere_integral)
record("inner_product_stress", stress == 2*G-S.trace(G)*S.eye(2), str(stress))
rank_one = (x*x*(4*w*w.T-2*S.eye(2))).applyfunc(sphere_integral)
record("rank_one_stress", rank_one == S.diag(1,-1), str(rank_one))
d11,d12,d21,d22 = S.symbols("d11 d12 d21 d22", real=True)
D = S.Matrix([[d11,d12],[d21,d22]])
A = S.eye(2) + e*D
derivative = S.diff(S.trace(A.T*G*A)/A.det(), e).subs(e,0)
pairing = sum(stress[i,j]*D[i,j] for i in range(2) for j in range(2))
record("inner_product_domain_variation", S.simplify(derivative-pairing)==0, str(derivative))
R = S.Matrix([[S.Rational(3,5),-S.Rational(4,5)],[S.Rational(4,5),S.Rational(3,5)]])
newG=R.T*G*R
covariance = 2*newG-S.trace(newG)*S.eye(2)-R.T*stress*R
record("stress_rotation_covariance", covariance.applyfunc(S.simplify)==S.zeros(2), str(R))

integral = lambda f: S.integrate(S.integrate(S.expand(f),(x,0,1)),(y,0,1))
for k in [S.Integer(-3),S.Integer(1),S.Integer(10)]:
    p=k*x*(1-x)*y*(1-y)
    f=y+p
    energy=integral(S.diff(f,x)**2+S.diff(f,y)**2)
    correction=integral(S.diff(p,x)**2+S.diff(p,y)**2)
    record("scalar_calibration_"+str(k), energy==1+correction,
           {"energy":str(energy), "extra_nonnegative":str(correction)})
p=x*x*(1-x)**2*y*y*(1-y)**2
for k,l in [(1,2),(10000,-3000),(-7000,2000)]:
    F=x+k*p; H=y+l*p
    jac=S.diff(F,x)*S.diff(H,y)-S.diff(F,y)*S.diff(H,x)
    jac_int=integral(jac)
    record("exact_form_boundary_control_"+str(k),jac_int==1,
           {"integrated_jacobian":str(jac_int),
            "jacobian_at_3_4_1_2":str(jac.subs({x:S.Rational(3,4),y:S.Rational(1,2)}))})
t=S.symbols("t",real=True)
left,right=S.Rational(1,16),S.Rational(3,16)
psi=(t-left)**2*(right-t)**2*x*x*(1-x)**2
first=S.integrate(S.integrate(-4*t*psi,(t,left,right)),(x,0,1))
direct=S.integrate(S.integrate(2*t*t*S.diff(psi,t),(t,left,right)),(x,0,1))
record("KS_decreasing_variation",first==direct and first<0,
       {"first_variation":str(first),"interval":[str(left),str(right)],
        "note":"Polynomial is W_0^{1,2}; smooth nonnegative approximants preserve the strict sign."})
m=S.sqrt(17)-4
record("distortion_constant",S.simplify(m*m+8*m-1)==0 and S.simplify(1/m-(4+S.sqrt(17)))==0,
       {"m_lower_bound":str(m),"Q":str(1/m)})
distortion=[{"t":"1/"+str(2**k),"ratio":4**k} for k in range(3,21)]
record("unbounded_distortion_sequence",all(d["ratio"]>0 for d in distortion),distortion)

def H(r):
    if r<=0: return 0.0
    if r>=1: return 1.0
    return float(expit(-1/r+1/(1-r)))

def a(t):
    eta=1-H((16*t*t-1)/3)
    return eta*t*t+1-eta

c,err=quad(lambda t:1-a(t),0,.5,epsabs=1e-13,epsrel=1e-13,points=[.25])
record("smooth_transition_range",all(0<=a(t)<=1 for t in np.linspace(-2,2,10001)) and 47/192<c<.5,
       {"c":c,"quad_error_estimate":err,"analytic_lower_bound":"47/192", "energy_excess_4pi_c":4*math.pi*c},"numerical_diagnostic")
record("piecewise_transition_values",a(0)==0 and abs(a(.125)-.125**2)<1e-15 and a(.5)==1 and a(1)==1,
       {str(t):a(t) for t in [0,.125,.25,.5,1]},"numerical_diagnostic")

# Numerical diagnostics for the nonsmooth-seminorm angular change of variables.
N=2**17
theta=(np.arange(N)+.5)*(2*np.pi/N)
W=np.column_stack((np.cos(theta),np.sin(theta)))
norms={
    "euclidean":lambda V:np.sqrt(np.sum(V*V,axis=1)),
    "l1":lambda V:np.sum(np.abs(V),axis=1),
    "linfinity":lambda V:np.max(np.abs(V),axis=1),
    "weighted_linf":lambda V:np.maximum(2*np.abs(V[:,0]),.3*np.abs(V[:,1])),
    "rank_one":lambda V:np.abs(V[:,0]+.7*V[:,1]),
    "zero":lambda V:np.zeros(len(V)),
}
matrices=[np.array([[1.2,.3],[-.2,.9]]),np.array([[2.,0.],[0.,.5]]),np.array([[.8,.6],[-.6,.8]])]
directions=[np.array([[1.,.3],[.7,-.5]]),np.array([[0.,1.],[0.,0.]]),np.array([[1.,0.],[0.,1.]])]
numeric_rows=[]
for name,norm in norms.items():
    sq=norm(W)**2
    T=2*np.mean(sq[:,None,None]*(4*W[:,:,None]*W[:,None,:]-2*np.eye(2)),axis=0)
    for j,A in enumerate(matrices):
        det=np.linalg.det(A)
        lhs=2*np.mean(norm(W@A.T)**2)/det
        denominator=np.sum((W@np.linalg.inv(A).T)**2,axis=1)**2
        rhs=2*np.mean(sq/denominator)/(det*det)
        error=abs(lhs-rhs)
        record(f"angular_change_{name}_{j}",error<2e-7*max(1,abs(lhs)),
               {"left":lhs,"right":rhs,"absolute_error":error,"samples":N},"numerical_diagnostic")
    for j,D in enumerate(directions):
        def F(eps):
            A=np.eye(2)+eps*D
            return 2*np.mean(norm(W@A.T)**2)/np.linalg.det(A)
        eps=2e-5
        finite=(F(eps)-F(-eps))/(2*eps)
        predicted=float(np.sum(T*D))
        error=abs(finite-predicted)
        record(f"stress_derivative_{name}_{j}",error<5e-5*max(1,abs(predicted)),
               {"finite_difference":finite,"stress_pairing":predicted,"absolute_error":error,"step":eps,"samples":N},"numerical_diagnostic")
    if name in ["l1","linfinity"]:
        record("fourfold_balance_"+name,np.max(np.abs(T))<1e-11,
               {"stress":T.tolist(),"norm_is_inner_product":False},"numerical_diagnostic")

result={"status":"PASS","timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "check_count":len(checks),"checks":checks,
        "limits":"Finite exact identities and floating-point diagnostics support, but do not replace, the independent written analytic proof review. Numerical errors are not rigorous enclosures."}
(OUT/'fresh_controls.json').write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
