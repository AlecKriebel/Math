"""Independent PR57 algebraic controls; no author or reviewer import.

The universal bounds are proved in PROOF.md. Finite symbolic and high precision
controls here check recurrences, inverse-coordinate matrix order, reconstruction,
and a genuinely negative curvature control when the r=1 correction is omitted.
This script only writes to stdout. Run with -B from this family.
"""
import hashlib
import json
import os
import platform
import sys
from pathlib import Path
import sympy as S
import mpmath as M

checks = []
def check(name, ok):
    if not bool(ok):
        raise AssertionError(name)
    checks.append(name)

x, y = S.symbols('x y', real=True)
rho = S.symbols('rho', positive=True)
s2 = x*x+y*y+rho*rho
z = x+S.I*y

# Polynomial coefficient norms give explicit n-independent estimates. These
# finite controls verify the recurrence mechanism, not all derivative orders.
for j in range(1, 8):
    for a in range(j+1):
        P = x if a else y
        variables = [x]*(a-1)+[y]*(j-a) if a else [y]*(j-1)
        for k, v in enumerate(variables, 1):
            P = S.expand(s2*S.diff(P,v)-2*k*v*P)
        poly = S.Poly(P,x,y,rho)
        check(f'log numerator homogeneous j={j},a={a}', all(sum(m)==j for m in poly.monoms()))
        cn = sum(abs(c) for c in poly.coeffs())
        check(f'log coefficient bound j={j},a={a}', cn <= 5**(j-1)*S.factorial(j-1))
        if j <= 4:
            literal = S.diff(S.log(s2)/2,x,a,y,j-a)
            check(f'log recurrence identity j={j},a={a}', S.cancel(literal-P/s2**j)==0)

for r in range(1,9):
    for k in range(r+1):
        for a in range(k+1):
            Q = z**(r+2)/2
            for j,v in enumerate([x]*a+[y]*(k-a)):
                Q = S.expand(s2*S.diff(Q,v)-2*(j+1)*v*Q)
            poly = S.Poly(Q,x,y,rho)
            check(f'bar numerator homogeneous r={r},k={k},a={a}', all(sum(m)==r+2+k for m in poly.monoms()))
            if k <= 2:
                literal=S.diff(z**(r+2)/(2*s2),x,a,y,k-a)
                check(f'bar recurrence identity r={r},k={k},a={a}',S.cancel(literal-Q/s2**(k+1))==0)

t = S.symbols('t', nonnegative=True)
check('first logarithmic envelope decreasing', S.simplify(S.diff(S.exp(-t)*(1+t),t)+t*S.exp(-t))==0)
check('second logarithmic envelope critical point',S.simplify(S.diff(S.exp(-t)*(1+t)**2,t)-S.exp(-t)*(1-t*t))==0)
check('second envelope maximum value',S.exp(-t).subs(t,1)*(1+t).subs(t,1)**2==4/S.E)
for r in range(1,13):
    jet=S.diff(x**(r+1)*S.log(x*x+rho*rho)/2,x,r+1).subs(x,0)
    check(f'exact top jet r={r}',S.simplify(jet-S.factorial(r+1)*S.log(rho))==0)

# A chart made of a nonlinear shear and an independent linear shear. Its inverse
# is explicit and its H H^T differs from H^T H. This is distinct from the author
# script's (x,y+x^2) chart and tests both components of the curvature drift.
u,v=S.symbols('u v',real=True)
F=S.Matrix([x+y*y,y+x+y*y])
G=S.Matrix([u-(v-u)**2,v-u])
J=F.jacobian([x,y]); H=J.inv(); A=H*H.T
drift=-H*S.Matrix([sum(A[i,j]*S.diff(fi,[x,y][i],[x,y][j]) for i in range(2) for j in range(2)) for fi in F])
check('inverse polynomial chart',all(S.expand(gi.subs({u:F[0],v:F[1]},simultaneous=True)-xi)==0 for gi,xi in zip(G,[x,y])))
check('noncommuting matrix-order negative control', A != H.T*H)
for test in [x,y,x*x+y*y,x*y,x**3+y**3,x*x*y+y**4]:
    target=test.subs({x:G[0],y:G[1]},simultaneous=True)
    literal=(S.diff(target,u,2)+S.diff(target,v,2)).subs({u:F[0],v:F[1]},simultaneous=True)
    operator=sum(A[i,j]*S.diff(test,[x,y][i],[x,y][j]) for i in range(2) for j in range(2))+sum(drift[i]*S.diff(test,[x,y][i]) for i in range(2))
    check('full pulled Laplacian '+str(test),S.expand(literal-operator)==0)
wrong=H.T*H
test=x*x
check('wrong inverse matrix order is detected',S.expand(sum((A[i,j]-wrong[i,j])*S.diff(test,[x,y][i],[x,y][j]) for i in range(2) for j in range(2)))!=0)

# General real Wirtinger coefficients, without assuming a specially shaped map.
p,q,c,d=S.symbols('p q c d',real=True)
norm=p*p+q*q
mr=(c*p+d*q)/norm; mi=(d*p-c*q)/norm
tensor=S.Matrix([[(1+mr)**2+mi**2,2*mi],[2*mi,(1-mr)**2+mi**2]])
JJ=S.Matrix([[p+c,-q+d],[q+d,p-c]])
for i in range(2):
    for j in range(i,2):
        check(f'exact metric reconstruction {i},{j}',S.cancel(norm*tensor[i,j]-(JJ.T*JJ)[i,j])==0)

# Exact leading r=1 boundary-layer diagnostic. It is not used as a replacement
# for the nonlinear uniform proof. Removing the correction produces a negative
# leading sign on the left of the origin, rather than an inconclusive error.
real_fz_increment=x*(S.log(s2)+(x*x+y*y)/(2*s2))
lap=S.diff(real_fz_increment,x,2)+S.diff(real_fz_increment,y,2)
expected=4*x*((x*x+y*y)**2+3*(x*x+y*y)*rho*rho+3*rho**4)/s2**3
check('r1 exact leading Laplacian',S.cancel(lap-expected)==0)
check('omitted correction negative leading coefficient',S.simplify((rho*expected).subs({x:-rho,y:0}))==-S.Rational(7,2))
T=(x*x+y*y+2*rho*rho)/s2**S.Rational(3,2)
check('radius leading trace on negative test point',S.simplify((rho*T).subs({x:-rho,y:0}))==3/(2*S.sqrt(2)))
Q=S.symbols('Q',nonnegative=True)
margin=S.expand((1+Q)**3*(Q+2)**2-Q*(Q*Q+3*Q+3)**2)
check('leading correction ratio has global bound 4',margin==Q**4+4*Q**3+7*Q**2+7*Q+4)

# Full nonlinear operator at selected exponentially small radii, with 80 digits.
# K=8 here is a diagnostic, not the universal K selected from C_0 in PROOF.md.
eps=S.symbols('eps',real=True)
L=S.log(s2)/2
FR=S.Matrix([x+eps*(x*x-y*y)*L,y+2*eps*x*y*L])
JR=FR.jacobian([x,y])
fza=(JR[0,0]+JR[1,1])/2
fzb=(JR[1,0]-JR[0,1])/2
hh=S.log(fza*fza+fzb*fzb)/2
ss=S.sqrt(s2)
def bundle(expr):
    return [S.diff(expr,x),S.diff(expr,y)]+[S.diff(expr,a,b) for a in [x,y] for b in [x,y]]
exprs=list(JR)+[S.diff(fi,a,b) for fi in FR for a in [x,y] for b in [x,y]]+bundle(hh)+bundle(ss)
for b in [S.log(1+x*x+y*y)/2,S.log(1+x*x+y*y)-S.log(2)]:
    exprs+=bundle(b)
evaluate=S.lambdify((x,y,rho,eps),exprs,'mpmath',cse=True)
M.mp.dps=80
diagnostics=[]
for n in [5,10,20,40]:
    rr=M.exp(-n); ee=M.mpf(1)/n
    vals=evaluate(-rr,0,rr,ee)
    jmat=M.matrix(2,2); jmat[:,:]=M.matrix([vals[:2],vals[2:4]])
    inv=jmat**-1; aa=inv*inv.T
    hessf=[M.matrix([vals[4+i*4:6+i*4],vals[6+i*4:8+i*4]]) for i in range(2)]
    drift=-inv*M.matrix([sum(aa[i,j]*hs[i,j] for i in range(2) for j in range(2)) for hs in hessf])
    def op(data):
        grad=data[:2]; hs=M.matrix([data[2:4],data[4:6]])
        return sum(aa[i,j]*hs[i,j] for i in range(2) for j in range(2))+sum(drift[i]*grad[i] for i in range(2))
    ho=op(vals[12:18]); so=op(vals[18:24])
    for bi,surface in enumerate(['plane','sphere']):
        bo=op(vals[24+bi*6:30+bi*6])
        no=bo+ho; yes=no+8*ee*so
        check(f'negative omitted curvature n={n},{surface}',no<0)
        check(f'positive corrected diagnostic n={n},{surface}',yes>0)
        diagnostics.append({'n':n,'surface':surface,'point':'(-exp(-n),0)','digits':80,'K_diagnostic':8,'uncorrected_pulled_Laplacian':M.nstr(no,30),'corrected_pulled_Laplacian':M.nstr(yes,30),'scaled_uncorrected':M.nstr(rr/ee*no,30),'scaled_corrected':M.nstr(rr/ee*yes,30)})

out={'schema':'pr57-endpoint-independent-controls/v1','process_pid':os.getpid(),'python':platform.python_version(),'sympy':S.__version__,'mpmath':M.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'check_count':len(checks),'checks':checks,'diagnostics':diagnostics,'universal_estimates_proved_in':'PROOF.md','author_or_historical_checker_imports':False,'finite_controls_are_not_uniform_proof':True}
print(json.dumps(out,indent=2,sort_keys=True))
