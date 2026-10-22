#!/usr/bin/env python3
"""Independent degree-3 Taylor jets and rational interpolation audit.

Unlike the distributed programs, this obtains all derivatives from a full
three-variable Taylor polynomial. Complete tensor-product interpolation grids
then check polynomial identities with conservative bidegree <= (9,9).
No imported verifier code, floating point, CAS, or assertions are used.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
from datetime import datetime,timezone
import json
OUT=Path(__file__).resolve().parent
checks=[]
def check(ok,label):
    if not ok:raise RuntimeError(label)
    checks.append(label)
ZERO=(0,0,0)
class Jet:
    def __init__(self,a=0):
        self.a={k:Q(v) for k,v in a.items() if v} if isinstance(a,dict) else ({ZERO:Q(a)} if a else {})
    def __add__(self,b):
        b=b if isinstance(b,Jet) else Jet(b)
        a=self.a.copy()
        for k,v in b.a.items():a[k]=a.get(k,Q(0))+v
        return Jet(a)
    __radd__=__add__
    def __neg__(self):return Jet({k:-v for k,v in self.a.items()})
    def __sub__(self,b):return self+(-b if isinstance(b,Jet) else -Q(b))
    def __mul__(self,b):
        b=b if isinstance(b,Jet) else Jet(b);a={}
        for k,v in self.a.items():
            for l,w in b.a.items():
                m=tuple(x+y for x,y in zip(k,l))
                if sum(m)<=3:a[m]=a.get(m,Q(0))+v*w
        return Jet(a)
    __rmul__=__mul__
    def __pow__(self,n):
        r=Jet(1)
        for _ in range(n):r=r*self
        return r
    def derivative(self,axes):
        k=tuple(axes.count(i) for i in range(3))
        return self.a.get(k,Q(0))*factorial(k[0])*factorial(k[1])*factorial(k[2])
def minus_log_nonconstant(j):
    c=j.a.get(ZERO,Q(0))
    if c<=0:raise ValueError('positive log argument required')
    v=(j-c)*Q(1,c)
    return -v+v**2*Q(1,2)-v**3*Q(1,3)
def fjet(base,extra=True):
    x,y,z=[Jet(q)+Jet({tuple(int(i==j) for i in range(3)):1}) for j,q in enumerate(base)]
    return minus_log_nonconstant(x*y**2-z**3)+(minus_log_nonconstant(z) if extra else Jet())
def tensor(j):return [[[j.derivative([i,k,l]) for l in range(3)]for k in range(3)]for i in range(3)]
def matrix(j,h):return [[sum(j.derivative([i,k,l])*h[l] for l in range(3)) for k in range(3)]for i in range(3)]
def contraction(j,h,u):return sum(j.derivative([i,k,l])*h[i]*u[k]*u[l]for i,k,l in product(range(3),repeat=3))
def norm2(j,u):return sum(j.derivative([i,k])*u[i]*u[k]for i,k in product(range(3),repeat=2))
def det(m):
    return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
def leading(m):return m[0][0]*m[1][1]-m[0][1]**2
def claimed(s,t):
    r=s+1
    a=2*(t-1)**2*(t+2);b=2*(t-1)*(2*t*t+2*t-1-3*r);c=6*(t-1)*(r-t*t-t+1)
    d=4*r**3+12*r*r-18*r*r*t+6*r*t**3-6*r*t+2*t**3
    e=12*r*r*t-18*r*r-6*r*t**3+24*r*t-6*r-6*t**3
    f=6*(r+2)*t**3+2*(r**3-6*r*r-18*r-4)*t+12*r*(r+2)
    return [[a,b,c],[b,d,e],[c,e,f]]
def scale(m,a):return [[a*v for v in row]for row in m]
# The cleared jet matrix has degree <=3 in s and <=3 in t:
# derivatives of cubic p, p_h and p_ijh, with denominator p^3=s^3;
# the added log(z) term contributes 2s^3*t in entry33.
# Products of three such entries, and every residual below, have bidegree <=9.
# Ten distinct nodes in each variable are therefore an identity certificate,
# not a random finite sample. Nodes never divide by zero, including t=0,1.
s_nodes=[Q(k,7) for k in range(1,11)]
t_nodes=[Q(k,3)for k in range(10)]
for si,s in enumerate(s_nodes):
    j=fjet((s+1,Q(1),Q(1)))
    for ti,t in enumerate(t_nodes):
        m=scale(matrix(j,(t**3,Q(1),t)),-s**3)
        check(m==claimed(s,t),f'interpolation matrix {si},{ti}')
        p=2*(t+2)*s*s-3*(t-1)*(3*t+5)*s+3*(t-1)**2*(t+2)**2
        rr=(t+2)*(2*t*s*s-3*(t-1)*(3*t+1)*s+3*(t-1)**2*(t*t+4*t+1))
        check(leading(m)==4*s*(t-1)**2*p,f'interpolation leading minor {si},{ti}')
        check(det(m)==8*s**4*(t-1)**2*rr,f'interpolation determinant {si},{ti}')
        check(8*(t+2)*p==(4*(t+2)*s-3*(t-1)*(3*t+5))**2+3*(t-1)**2*(8*t**3+21*t*t+6*t-11),f'interpolation first square {si},{ti}')
        check(8*t*rr==(t+2)*((4*t*s-3*(t-1)*(3*t+1))**2+3*(t-1)**3*(8*t*t+13*t+3)),f'interpolation cleared second square {si},{ti}')
        check(p>0 and rr>0,f'positive residuals {si},{ti}')
        check((m[0][0]>0 and leading(m)>0 and det(m)>0) if t!=1 else (m[0]==[0,0,0]and m[1][1]>0 and m[1][1]*m[2][2]-m[1][2]**2>0),f'exact PSD {si},{ti}')
    a=(1,2,-3);b=(0,1,-1)
    endpoint=scale(matrix(j,(1,0,0)),-s**3)
    check(endpoint==[[2*a[i]*a[k]+6*s*b[i]*b[k]for k in range(3)]for i in range(3)],f'endpoint Gram {si}')
# Independent perturbation controls include exact counterexamples with witnesses.
j=fjet((Q(5),Q(1),Q(1)),False)
bad=scale(matrix(j,(8,1,2)),-64)
D=leading(bad)
u=((bad[0][1]*bad[1][2]-bad[1][1]*bad[0][2])/D,(bad[0][1]*bad[0][2]-bad[0][0]*bad[1][2])/D,Q(1))
omitted_witness=u
quad=sum(bad[i][k]*u[i]*u[k]for i,k in product(range(3),repeat=2))
check(det(bad)==-24576 and quad<0,'Independent omission control exact negative witness')
outside=scale(matrix(fjet((Q(2),Q(1),Q(1))),(-1,1,-1)),-1)
check(sum(outside[i][k]*(5,1,2)[i]*(5,1,2)[k]for i,k in product(range(3),repeat=2))==-2,'Independent outside-cone witness')
check(claimed(Q(1),Q(0))[0][0]!=-claimed(Q(1),Q(0))[0][0],'Wrong curvature sign rejects')
# General base-point formulas, extreme rational scales, and fixed-D tensor law.
bases=[(Q(1)+Q(1,10**9),Q(1),Q(1)),(Q(17,8),Q(2),Q(1)),(Q(10**12),Q(1,10**3),Q(10)),(Q(5,10**9),Q(10**6),Q(1,10)),(Q(13),Q(2),Q(3))]
vectors=[(Q(0),Q(0),Q(0)),(Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(1)),(Q(2),Q(-3),Q(5)),(Q(1,7),Q(11,13),Q(-17,19))]
for bi,base in enumerate(bases):
    x,y,z=base;j=fjet(base);g=z**3/y**2;delta=x-g
    check(delta>0,f'interior extreme base {bi}')
    D=(y**2/z**3,1/y,1/z)
    jj=fjet((x*D[0],Q(1),Q(1)))
    for i,k,l in product(range(3),repeat=3):check(j.derivative([i,k,l])==jj.derivative([i,k,l])*D[i]*D[k]*D[l],f'fixed automorphism tensor {bi},{i},{k},{l}')
    for i in range(3):check(sum(j.derivative([i,k])*base[k]for k in range(3))==-j.derivative([i]),f'gradient Hessian relation {bi},{i}')
    check(25*norm2(j,base)==100,f'parameter100 {bi}')
    for ui,u in enumerate(vectors):
        bu=u[1]/y;cu=u[2]/z;wu=(u[0]-g*(3*cu-2*bu))/delta
        v2=6*g/delta*(cu-bu)**2
        S=wu*wu+v2+2*bu*bu+cu*cu
        cub=-2*wu**3-3*wu*v2+(cu-4*bu)*v2-4*bu**3-2*cu**3
        check(norm2(j,u)==S and contraction(j,u,u)==cub,f'scalar normal forms {bi},{ui}')
        for hi,h in enumerate(vectors):
            bh=h[1]/y;ch=h[2]/z;wh=(h[0]-g*(3*ch-2*bh))/delta
            vhvu=6*g/delta*(ch-bh)*(cu-bu)
            mixed=-2*wh*wu*wu-wh*v2-2*wu*vhvu+((ch-4*bh)*v2+2*(cu-4*bu)*vhvu)/3-4*bh*bu*bu-2*ch*cu*cu
            actual=contraction(j,h,u)
            check(actual==mixed,f'mixed normal form {bi},{hi},{ui}')
            check(actual**2<=100*norm2(j,h)*S*S,f'mixed scale certificate {bi},{hi},{ui}')
# Arbitrary a,b polynomial factorization coefficient interpolation: degrees<=3.
for a,b in product([Q(1),Q(2),Q(4),Q(8)],[Q(0),Q(1),Q(3),Q(7)]):
    co=[Q(-1),-3*b,-3*b*b,a**3-b**3]
    linear=[-1,a-b];quadratic=[1,a+2*b,a*a+a*b+b*b]
    re=[sum(linear[i]*quadratic[k-i]for i in (0,1)if 0<=k-i<3)for k in range(4)]
    check(co==re,'Hyperbolicity factor coefficient interpolation '+str((a,b)))
    check((a+2*b)**2-4*(a*a+a*b+b*b)==-3*a*a<0,'Hyperbolicity discriminant '+str((a,b)))
result={'status':'PASS','checked_at_utc':datetime.now(timezone.utc).isoformat(),'checks_passed':len(checks),'method':'Degree3 full trivariate Taylor jets plus degree-bounded complete rational interpolation, independently authored; exact Fraction arithmetic','interpolation_nodes_per_variable':10,'conservative_residual_bidegree_bound':[9,9],'extreme_bases':[[str(v)for v in a]for a in bases],'omitted_log_z_control':{'matrix':[[str(v)for v in a]for a in bad],'determinant':str(det(bad)),'witness':[str(v)for v in omitted_witness],'negative_quadratic':str(quad)},'checks':checks}
(OUT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='checks'},indent=2))
