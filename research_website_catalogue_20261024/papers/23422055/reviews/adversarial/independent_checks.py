"""Fresh exact checks, written from the published equations before reading archived code.

These certify symbolic local identities, not the global Stokes/cohomology argument.
Run: python3 independent_checks.py
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import sympy as S

u,v,x,t,eps=S.symbols('u v x t eps',real=True)
coords=(u,v,x,t)
checks=[]
def simp(a): return S.simplify(a)
def clean(a): return {k:simp(z) for k,z in a.items() if simp(z)!=0}
def plus(*forms):
    out={}
    for a in forms:
        for k,z in a.items(): out[k]=out.get(k,0)+z
    return clean(out)
def scale(c,a): return clean({k:c*z for k,z in a.items()})
def wedge(a,b):
    out={}
    for ka,va in a.items():
        for kb,vb in b.items():
            seq=ka+kb
            if len(set(seq))<len(seq): continue
            sign=(-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))
            key=tuple(sorted(seq));out[key]=out.get(key,0)+sign*va*vb
    return clean(out)
def d(a):
    out={}
    for k,z in a.items():
        for i,q in enumerate(coords): out=plus(out,wedge({(i,):S.diff(z,q)},{k:1}))
    return out
def matrix(a):
    m=S.zeros(4)
    for (i,j),z in a.items():m[i,j]=z;m[j,i]=-z
    return m
def zero(name,a):
    if isinstance(a,dict): residual=clean(a)
    elif isinstance(a,S.MatrixBase):residual=a.applyfunc(simp);residual=[] if residual==S.zeros(*a.shape) else str(residual)
    else:residual=simp(a)
    if residual: raise RuntimeError(f'{name}: {residual}')
    checks.append({'name':name,'pass':True})

du,dv,dx,dt=[{(i,):S.Integer(1)} for i in range(4)]
vol={(0,1,2,3):S.Integer(1)}
alpha=plus(wedge(du,dx),scale(-1,wedge(dv,dt)))
beta=plus(wedge(du,dt),wedge(dv,dx))
gamma=plus(scale(u,alpha),scale(-v,beta))
R=S.Function('R')(*coords)
pert=d(scale(R,dv));be=plus(beta,pert)
ge=plus(gamma,scale(-1,d(scale(v*R,dv))))
zero('unperturbed gamma closed',d(gamma))
zero('arbitrary smooth R beta remains closed',d(be))
zero('arbitrary smooth R gamma remains closed',d(ge))
zero('full-cutoff third-class relation',plus(ge,scale(-u,alpha),scale(v,be)))
zero('d(Rv dv)=v d(R dv)',plus(d(scale(v*R,dv)),scale(-v,pert)))
zero('alpha squared',plus(wedge(alpha,alpha),scale(-2,vol)))
zero('alpha beta Gram entry',plus(wedge(alpha,be),scale(-S.diff(R,t),vol)))
zero('beta squared',plus(wedge(be,be),scale(-2*(1-S.diff(R,x)),vol)))

ru,rx,rt=S.symbols('ru rx rt',real=True)
jet={S.diff(R,u):ru,S.diff(R,x):rx,S.diff(R,t):rt}
E=matrix(be).subs(jet);A=matrix(alpha)
D=1-rx-rt**2/4
C=E-rt*A/2
K=-A.inv()*C
zero('algebraic real J numerator squared',K*K+D*S.eye(4))
zero('alpha anti-invariance with reconstructed J',K.T*A*K+D*A)
zero('beta anti-invariance with reconstructed J',K.T*E*K+D*E)
G=u*A-v*E
zero('gamma anti-invariance with reconstructed J',K.T*G*K+D*G)
zero('determinant J numerator',K.det()-D**2)
zero('complex Pfaffian vanishes',S.expand((A+S.I*C/S.sqrt(D)).det()))
zero('undeformed J is standard',K.subs({ru:0,rx:0,rt:0})-S.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]))

k=1-eps*x
J=K.subs({ru:0,rt:0,rx:eps*x})/S.sqrt(k)
phi1=plus(du,scale(S.I*S.sqrt(k),dv))
phi2=plus(dx,scale(S.I/S.sqrt(k),dt))
Bcore=plus(scale(1/S.sqrt(k),wedge(du,dt)),scale(S.sqrt(k),wedge(dv,dx)))
zero('coframe realizes normalized complex form',plus(wedge(phi1,phi2),scale(-1,alpha),scale(-S.I,Bcore)))
zero('integrability obstruction wedge',plus(wedge(d(phi1),wedge(phi1,phi2)),scale(eps/(2*k),vol)))
zero('normalized imaginary form is not closed',plus(d(Bcore),scale(-eps/(2*k**S.Rational(3,2)),wedge(dx,wedge(du,dt)))))
def bracket(X,Y):
    return S.Matrix([sum(X[j]*S.diff(Y[i],coords[j])-Y[j]*S.diff(X[i],coords[j]) for j in range(4)) for i in range(4)])
U=S.eye(4)[:,0];X=S.eye(4)[:,2]
N=(bracket(J*U,J*X)-J*bracket(J*U,X)-J*bracket(U,J*X)-bracket(U,X)).applyfunc(simp)
zero('Nijenhuis independently computed at origin',N.subs(x,0)-S.Matrix([-eps/2,0,0,0]))
zero('epsilon zero is integrable control',N.subs(eps,0))
if N.subs({x:0,eps:S.Rational(1,10)})==S.zeros(4,1):raise RuntimeError('nonintegrability control failed')
checks.append({'name':'nonzero parameter gives nonzero N at origin, even though J equals J0 there','pass':True})
wrong= (J.T*matrix(gamma)*J+matrix(gamma)).subs({u:0,v:1,x:1,eps:S.Rational(1,10)})
if wrong==S.zeros(4):raise RuntimeError('omitted third-form correction undetected')
checks.append({'name':'negative control: original uncorrected third form fails anti-invariance','pass':True})
unnormalized=wedge(plus(alpha,scale(S.I,plus(beta,scale(eps*x,wedge(dx,dv))))),plus(alpha,scale(S.I,plus(beta,scale(eps*x,wedge(dx,dv))))))
zero('unnormalized pair not decomposable away from eps*x=0',plus(unnormalized,scale(-2*eps*x,vol)))

# Exact interval-corner controls supplement, but do not prove, the elementary D>=1/2 bound.
for xr in [S.Rational(-1,4),0,S.Rational(1,4)]:
    for tr in [-1,0,1]:
        if D.subs({rx:xr,rt:tr})<S.Rational(1,2):raise RuntimeError('D bound failed')
        checks.append({'name':f'Gram determinant boundary rx={xr},rt={tr}','pass':True})
z=S.symbols('z');zero('six finite roots are simple',S.gcd(z**6-1,6*z**5)-1)
# Holomorphic-coordinate Jacobian is 1/y, nonzero at y=i.
zz,ww=S.symbols('zz ww');yy=S.Function('y')(zz)
zero('local normal-form coordinate Jacobian',S.Matrix([[1,0],[S.diff(ww/yy,zz),S.diff(ww/yy,ww)]]).det()-1/yy)

result={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'sympy':S.__version__,'passed':len(checks),'checks':checks,'independent_N_u_x':str(N),'limitations':'Exact local symbolic identities plus finite boundary/negative controls. Global compactness, Stokes, patching, and topology checked in written report; not formal verification.'}
Path(__file__).with_name('independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
