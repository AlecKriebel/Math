"""Check the independently derived bridge to classical cyclic Jacobi identities.

Run with SymPy 1.14.0 and mpmath 1.3.0. Numerical diagnostics are not interval proofs.
No submitted verification program is imported.
"""
from pathlib import Path
import datetime
import hashlib
import json
import math
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
checks = []

def exact(name, expression):
    result = sp.factor(expression)
    assert result == 0, (name, result)
    checks.append(name)

h, m, p, r, t = sp.symbols('h m p r t', nonzero=True)
un = h-(r-p)*(t-p)/(h-m)
ut = r+t-p
vn = -h+(r+p)*(t+p)/(h+m)
vt = -r-t-p
for q in [r,t]:
    exact('positive antipedal line equation', (h-m)*(un-m)+(q-p)*(ut-p)-((h-m)**2+(q-p)**2))
    exact('opposite antipedal line equation', (-h-m)*(vn-m)+(-q-p)*(vt-p)-((-h-m)**2+(-q-p)**2))
exact('normal paired mean', (un+vn)/2-(h*p*(r+t)-m*(r*t+p*p))/(h*h-m*m))
exact('tangent paired mean', (ut+vt)/2+p)

x,y,a,b,A,B,k = sp.symbols('x y a b A B k', nonzero=True)
H = a*a*x*x+b*b*y*y
D = y*y/A**2+x*x/B**2
J = x*y*(1/B**2-1/A**2)
rt = (H*(x*x/A**2+y*y/B**2)-1)/D
coef = k*x*(2*H*y*y*(1/B**2-1/A**2)-(H*(x*x/A**2+y*y/B**2)-1)-(a*a-b*b)*y*y*D)/(b*b*D)
alpha = (A*A*B*B+A*A*b*b-B*B*a*a)/(b*b)
exact('Vieta/focal support paired coefficient',
      (coef-(k*x*alpha/(A*A*x*x+B*B*y*y)-k*x)).subs(y*y,1-x*x))
s,c,d = sp.symbols('s c d', nonzero=True)
factor = sp.factor(alpha.subs({A:a*d/c,B:b/c})*c*c/a**2)
H0 = 1-2*k*k*s*s+k*k*s**4
exact('normalized coefficient',factor.subs(d*d,1-k*k*s*s).subs(c*c,1-s*s)-H0/(1-s*s))
S,C,Dn = sp.symbols('S C Dn')
D0=1-k*k*s*s*S*S
snplus=(S*c*d+s*C*Dn)/D0
snminus=(S*c*d-s*C*Dn)/D0
exact('product reduction', sp.factor(snplus*snminus-(S*S-s*s)/D0).subs(
    {C*C:1-S*S,Dn*Dn:1-k*k*S*S,c*c:1-s*s,d*d:1-k*k*s*s}))
exact('rational trace reduction',S*S/D0-((S*S-s*s)/D0+s*s)/(1-k*k*s**4))
dnminus=(Dn*d+k*k*S*s*C*c)/D0
dnplus=(Dn*d-k*k*S*s*C*c)/D0
exact('dn telescoping reduction',S*C/D0-(dnminus-dnplus)/(2*k*k*s*c))
q=sp.symbols('q',positive=True)
exact('N4 paired factor', (H0/(c*c)).subs({k*k:1-q*q,s*s:1/(1+q),s**4:1/(1+q)**2,c*c:q/(1+q)})-2*q)
exact('N4 rational trace constant', (s*s/(1-k*k*s**4)).subs({k*k:1-q*q,s*s:1/(1+q),s**4:1/(1+q)**2})-1/(2*q))

mp.mp.dps=90
max_error=mp.mpf(0)
numeric_cases=[]
def intersect(n1,z1,n2,z2):
    det=n1[0]*n2[1]-n1[1]*n2[0]
    assert det != 0
    return ((z1*n2[1]-z2*n1[1])/det,(n1[0]*z2-n2[0]*z1)/det)
def anti(X,Y,M):
    qx=(X[0]-M[0],X[1]-M[1]);qy=(Y[0]-M[0],Y[1]-M[1])
    return intersect(qx,qx[0]*X[0]+qx[1]*X[1],qy,qy[0]*Y[0]+qy[1]*Y[1])
for kval in ['0.1','0.6','0.95','0.999']:
    km=mp.mpf(kval); mm=km*km; kp=mp.sqrt(1-mm); K=mp.ellipk(mm)
    sn=lambda z:mp.ellipfun('sn',z,mm)
    cn=lambda z:mp.ellipfun('cn',z,mm)
    dn=lambda z:mp.ellipfun('dn',z,mm)
    for N in [4,6,8,10,12,14,18,22,30]:
        for tau in range(1,N//2):
            if math.gcd(N,tau)!=1:continue
            v=2*K*tau/N;delta=2*v
            sv=sn(v);cv=cn(v);dv=dn(v)
            ae=dv/cv;be=kp/cv;Ao=ae*dv/cv;Bo=be/cv
            Hval=1-2*mm*sv**2+mm*sv**4
            phi=mp.atan2(sn(delta),cn(delta))
            Zdelta=mp.ellipe(phi,mm)-mp.ellipe(mm)*delta/K
            formula=km*(-1+Hval/(cv**2*(1-mm*sv**4))*(sv**2+Zdelta/(mm*sn(delta))))
            for phase in ['0','0.137','0.731']:
                u=mp.mpf(phase)*K
                parameters=[u+i*delta for i in range(N)]
                normals=[(-sn(z)/ae,cn(z)/be) for z in parameters]
                outer=[intersect(normals[i],mp.mpf(1),normals[(i+1)%N],mp.mpf(1)) for i in range(N)]
                expected=[(-Ao*sn(z+v),Bo*cn(z+v)) for z in parameters]
                assert max(abs(outer[i][j]-expected[i][j]) for i in range(N) for j in range(2))<mp.mpf('1e-70')
                for focus_sign in [1,-1]:
                    M=(focus_sign*km,mp.mpf(0))
                    U=[anti(outer[i],outer[(i+1)%N],M) for i in range(N)]
                    centroid=tuple(mp.fsum(P[j] for P in U)/N for j in range(2))
                    error=max(abs(centroid[0]-focus_sign*formula),abs(centroid[1]))
                    max_error=max(max_error,error)
                    assert error<mp.mpf('1e-65'),(kval,N,tau,phase,focus_sign,error)
                    for i in range(N):
                        mid=parameters[i]+2*v
                        V=((U[i][0]+U[(i+N//2)%N][0])/2,(U[i][1]+U[(i+N//2)%N][1])/2)
                        Dval=1-mm*sv**2*sn(mid)**2
                        Vexpected=(focus_sign*km*(-1+Hval/cv**2*sn(mid)**2/Dval),
                            -focus_sign*km*ae*Hval/(be*cv**2)*sn(mid)*cn(mid)/Dval)
                        assert max(abs(V[j]-Vexpected[j]) for j in range(2))<mp.mpf('1e-65')
                    numeric_cases.append(dict(k=kval,N=N,tau=tau,phase=phase,focus_sign=focus_sign,
                        error=mp.nstr(error,8),centroid_x=mp.nstr(centroid[0],18)))
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),symbolic_checks=len(checks),
    checks=checks,numeric_precision_dps=mp.mp.dps,numeric_cases=len(numeric_cases),
    maximum_numeric_error=mp.nstr(max_error,10),cases=numeric_cases,
    sympy=sp.__version__,mpmath=mp.__version__,numeric_is_not_interval_proof=True,
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'REDUCTION_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ['symbolic_checks','numeric_cases','maximum_numeric_error','sympy','mpmath']},indent=2))
