"""Exact finite controls. These do not prove the analytic estimator/AFEM claims."""
import json
from collections import Counter
import sympy as s
C=Counter()
def ck(p,k):
    assert p,k
    C[k]+=1
for n in range(2,8):
    m=n-1
    B=s.zeros(m,n)
    for i in range(m):
        B[i,i]=i+1
        B[i,n-1]=(-1)**i
    U=s.eye(n)
    for i in range(n):
        for j in range(i+1,n):U[i,j]=s.Rational(i+j+2,n+3)
    M=U.T*U+s.eye(n)
    G=M.inv()*B.T;S=B*G;R=G*S.inv()
    F=s.Matrix([s.Rational(i+2,i+1) for i in range(m)])
    c=s.Matrix([s.Rational((-1)**i,i+3) for i in range(m)])
    pM=S.inv()*F;sigM=G*pM
    ker=B.nullspace()[0]
    ck(B*R==s.eye(m),'right_inverse')
    ck((ker.T*M*R)==s.zeros(1,m),'minimum_norm_orthogonality')
    for delta in [s.Rational(1,17),s.Rational(1,3),s.Integer(1),s.Integer(5)]:
        q=(S+delta*s.eye(m)).inv()*(F+delta*c)
        sig=G*q;d=B*sig-F;e=sig-sigM
        ck(e==R*d,'exact_conservation_correction')
        ck(d==delta*(c-q),'computed_defect')
        ck((e.T*M*e)[0]==(d.T*S.inv()*d)[0],'exact_schur_energy')
        v=S.inv()*d
        ck((d.T*v)[0]==(e.T*M*G*v)[0],'dual_norm_extremizer')
        ck((q-pM)==delta*(S+delta*s.eye(m)).inv()*(c-pM),'pressure_multiplier')
        for a in [s.Rational(-3,2),s.Rational(2,5)]:
            lift=e+a*ker
            ck((lift.T*M*lift)[0]-(e.T*M*e)[0]==a*a*(ker.T*M*ker)[0],'minimum_norm_pythagoras')
for lam in [s.Rational(1,13),s.Rational(2,3),s.Integer(1),s.Integer(7),s.Integer(100)]:
    for delta in [s.Rational(1,101),s.Rational(1,7),s.Integer(2),s.Integer(37)]:
        ck(delta**2*lam/(lam+delta)**2<=delta/4,'sharp_sqrt_delta_bound_squared')
        ck(delta**2*lam/(lam+delta)**2<=delta**2/lam,'delta_over_beta_bound_squared')
        ck(delta*lam/(lam+delta)<=delta,'defect_multiplier_bound')
for root_theta in [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]:
    for L in [s.Rational(1,2),s.Integer(1),s.Integer(3)]:
        kappa=root_theta/(3*L)
        theta_star=((root_theta-L*kappa)/(1+L*kappa))**2
        ck(0<theta_star<root_theta**2,'positive_transferred_bulk')
        ck(0<L*kappa<1,'indicator_absorption')
        ck(s.simplify(s.sqrt(theta_star)*(1+L*kappa)-(root_theta-L*kappa))==0,'bulk_constant_identity')
x,y=s.symbols('x y');a,b,c=s.symbols('a b c')
psi=a+b*x+c*y;curlpsi=s.Matrix([s.diff(psi,y),-s.diff(psi,x)])
ck(s.diff(curlpsi[0],x)+s.diff(curlpsi[1],y)==0,'piecewise_linear_curl_divergence')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite rational Schur/lift/spectral/marking identities only. No mesh-uniform analytic, Helmholtz, trace, or adaptive convergence conclusion is inferred from samples.'},indent=2,sort_keys=True))
