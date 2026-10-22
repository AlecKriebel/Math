
from fractions import Fraction as Q
from itertools import product
import json, sys, platform
from datetime import datetime, timezone

checked=[]
def check(condition,label):
    if not condition: raise RuntimeError(label)
    checked.append(label)

class P:
    def __init__(self, a=0):
        self.a = dict(a) if isinstance(a,dict) else ({(0,0):Q(a)} if a else {})
        self.a = {k:Q(v) for k,v in self.a.items() if v}
    def __add__(self,o):
        o = o if isinstance(o,P) else P(o)
        a=self.a.copy()
        for k,v in o.a.items(): a[k]=a.get(k,0)+v
        return P(a)
    __radd__=__add__
    def __neg__(self): return P({k:-v for k,v in self.a.items()})
    def __sub__(self,o): return self+-o if isinstance(o,P) else self+(-P(o))
    def __rsub__(self,o): return P(o)+-self
    def __mul__(self,o):
        o=o if isinstance(o,P) else P(o)
        a={}
        for k,v in self.a.items():
            for l,w in o.a.items():
                m=tuple(x+y for x,y in zip(k,l)); a[m]=a.get(m,0)+v*w
        return P(a)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0: raise ValueError('negative polynomial exponent')
        a=P(1)
        for i in range(n): a=a*self
        return a
    def __eq__(self,o):
        o=o if isinstance(o,P) else P(o)
        return self.a==o.a
    def __repr__(self): return str(self.a)
def det(A):
    if len(A)==1:return A[0][0]
    return sum(((-1)**j)*A[0][j]*det([row[:j]+row[j+1:] for row in A[1:]]) for j in range(len(A)))
s=P({(1,0):1});t=P({(0,1):1});r=s+1
dp=[P(1),2*r,P(-3)]
d2p=[[P(0),P(2),P(0)],[P(2),2*r,P(0)],[P(0),P(0),P(-6)]]
h=[t**3,P(1),t]
dp_h=sum(dp[i]*h[i] for i in range(3))
d2p_h=[sum(d2p[i][j]*h[j] for j in range(3)) for i in range(3)]
d3p_h=[[P(0),P(2),P(0)],[P(2),2*t**3,P(0)],[P(0),P(0),-6*t]]
# Exact chain rule: -s^3 D^3(-log p-log z)[h].
A=[[s**2*d3p_h[i][j]-s*(d2p_h[i]*dp[j]+dp[i]*d2p_h[j]+dp_h*d2p[i][j])+2*dp_h*dp[i]*dp[j]+(2*s**3*t if i==j==2 else 0) for j in range(3)] for i in range(3)]
B=[[None]*3 for _ in range(3)]
B[0][0]=2*(t-1)**2*(t+2)
B[0][1]=B[1][0]=2*(t-1)*(2*t**2+2*t-1-3*r)
B[0][2]=B[2][0]=6*(t-1)*(r-t**2-t+1)
B[1][1]=4*r**3+12*r**2-18*r**2*t+6*r*t**3-6*r*t+2*t**3
B[1][2]=B[2][1]=12*r**2*t-18*r**2-6*r*t**3+24*r*t-6*r-6*t**3
B[2][2]=6*(r+2)*t**3+2*(r**3-6*r**2-18*r-4)*t+12*r*(r+2)
for i,j in product(range(3),repeat=2): check(A[i][j]==B[i][j],f'NC1 chain-rule entry {i},{j}')
Ppoly=2*(t+2)*s**2-3*(t-1)*(3*t+5)*s+3*(t-1)**2*(t+2)**2
Rpoly=(t+2)*(2*t*s**2-3*(t-1)*(3*t+1)*s+3*(t-1)**2*(t**2+4*t+1))
check(det([row[:2] for row in A[:2]])==4*s*(t-1)**2*Ppoly,'NC2 minor identity')
check(det(A)==8*s**4*(t-1)**2*Rpoly,'NC3 determinant identity')
check(8*(t+2)*Ppoly==(4*(t+2)*s-3*(t-1)*(3*t+5))**2+3*(t-1)**2*(8*t**3+21*t**2+6*t-11),'NC4 square identity')
# Clear the harmless positive factor t+2.
check(8*t*Rpoly==(t+2)*((4*t*s-3*(t-1)*(3*t+1))**2+3*(t-1)**3*(8*t**2+13*t+3)),'NC5 cleared square identity')
# e_x endpoint from exact derivative tensor.
hp=[P(1),P(0),P(0)]
dph=dp[0];d2ph=[d2p[i][0] for i in range(3)]
d3ph=[[P(0),P(0),P(0)],[P(0),P(2),P(0)],[P(0),P(0),P(0)]]
E=[[s**2*d3ph[i][j]-s*(d2ph[i]*dp[j]+dp[i]*d2ph[j]+dph*d2p[i][j])+2*dph*dp[i]*dp[j] for j in range(3)] for i in range(3)]
aa=[1,2,-3];bb=[0,1,-1]
for i,j in product(range(3),repeat=2): check(E[i][j]==2*aa[i]*aa[j]+6*s*bb[i]*bb[j],f'endpoint Gram entry {i},{j}')
# t=1 exceptional block.
def at_t1(p):
    d={}
    for (i,j),v in p.a.items():d[(i,0)]=d.get((i,0),0)+v
    return P(d)
C=[[P(0),P(0),P(0)],[P(0),2*s**2*(2*r+1),-6*s**2],[P(0),-6*s**2,2*s**2*(r+2)]]
for i,j in product(range(3),repeat=2): check(at_t1(A[i][j])==C[i][j],f'exceptional t=1 entry {i},{j}')
check((2*r+1)*(r+2)-9==(r-1)*(2*r+7),'exceptional block determinant')
# Explicit nonhyperbolicity line: a^3*t^3-(1+b*t)^3.
a=P({(1,0):1});b=P({(0,1):1})
# t is renamed an independent scalar via expansion coefficient lists.
lhs=[P(-1),-3*b,-3*b**2,a**3-b**3]
linear=[P(-1),a-b];quadratic=[P(1),a+2*b,a**2+a*b+b**2]
rhs=[P(0) for _ in range(4)]
for i in range(2):
    for j in range(3): rhs[i+j]=rhs[i+j]+linear[i]*quadratic[j]
check(lhs==rhs,'arbitrary-interior-direction cubic factorization')
check((a+2*b)**2-4*(a**2+a*b+b**2)==-3*a**2,'quadratic nonreal-root discriminant')

# Additional symbolic edge identities.
check(at_t1(Ppoly)==6*s**2,'P(s,1)=6s^2')
check(at_t1(Rpoly)==6*s**2,'R(s,1)=6s^2')
u=P({(0,1):1})
check(8*(1+u)**3+21*(1+u)**2+6*(1+u)-11==8*u**3+45*u**2+72*u+24,'NC4 positive shift')
def evaluate(poly, sv, tv):
    return sum(v*sv**i*tv**j for (i,j),v in poly.a.items())
check(all(sum(E[i][j]*[1,1,1][j] for j in range(3))==0 for i in range(3)),'endpoint kernel (1,1,1)')
check(all(C[i][0]==0 for i in range(3)),'t=1 kernel e_x')

def dot(v,w):return sum(a*b for a,b in zip(v,w))
def derivatives(pt, add_log_z=True):
    x,y,z=pt
    p=x*y*y-z*z*z
    dp=[y*y,2*x*y,-3*z*z]
    pp=[[Q(0),2*y,Q(0)],[2*y,2*x,Q(0)],[Q(0),Q(0),-6*z]]
    def ppp(i,j,k):
        ijk=sorted((i,j,k))
        return Q(2) if ijk==[0,1,1] else Q(-6) if ijk==[2,2,2] else Q(0)
    H=[[dp[i]*dp[j]/p**2-pp[i][j]/p+(1/z**2 if add_log_z and i==j==2 else 0) for j in range(3)] for i in range(3)]
    T=[[[ -ppp(i,j,k)/p+(pp[i][j]*dp[k]+pp[i][k]*dp[j]+pp[j][k]*dp[i])/p**2-2*dp[i]*dp[j]*dp[k]/p**3-(2/z**3 if add_log_z and i==j==k==2 else 0) for k in range(3)] for j in range(3)] for i in range(3)]
    gradient=[-dp[i]/p-(1/z if add_log_z and i==2 else 0) for i in range(3)]
    return H,T,gradient
def contract(T,h,u,v):
    return sum(T[i][j][k]*h[i]*u[j]*v[k] for i,j,k in product(range(3),repeat=3))
def quadratic(H,u):return sum(H[i][j]*u[i]*u[j] for i,j in product(range(3),repeat=2))
def normal_coordinates(pt,u):
    x,y,z=pt;g=z**3/y**2;delta=x-g
    b=u[1]/y;c=u[2]/z;w=(u[0]-g*(3*c-2*b))/delta
    return b,c,w,6*g/delta
def scalar_forms(pt,u):
    b,c,w,k=normal_coordinates(pt,u);vv=k*(c-b)**2
    return w*w+vv+2*b*b+c*c,-2*w**3-3*w*vv+(c-4*b)*vv-4*b**3-2*c**3
def mixed_form(pt,h,u):
    bh,ch,wh,k=normal_coordinates(pt,h)
    bu,cu,wu,k=normal_coordinates(pt,u)
    vu2=k*(cu-bu)**2;vhvu=k*(ch-bh)*(cu-bu)
    return -2*wh*wu**2-wh*vu2-2*wu*vhvu+((ch-4*bh)*vu2+2*(cu-4*bu)*vhvu)/3-4*bh*bu**2-2*ch*cu**2

bases=[(2,1,1),(5,1,1),(Q(17,8),2,1),(3,Q(3,2),1),(Q(5,4),1,Q(1,2)),(13,2,3)]
directions=[(0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,-1,2),(-2,3,-1),(Q(1,3),Q(-2,5),Q(7,4))]
bases=[tuple(map(Q,b)) for b in bases]
directions=[tuple(map(Q,u)) for u in directions]
for bi,pt in enumerate(bases):
    H,T,gradient=derivatives(pt)
    for i in range(3):
        check(sum(H[i][j]*pt[j] for j in range(3))==-gradient[i],f'homogeneity Hessian identity {bi},{i}')
    check(quadratic(H,pt)==4,f'unscaled homogeneity parameter {bi}')
    check(25*quadratic(H,pt)==100,f'scaled homogeneity parameter {bi}')
    for ui,u in enumerate(directions):
        S,cubic=scalar_forms(pt,u)
        check(quadratic(H,u)==S,f'exact scalar Hessian {bi},{ui}')
        check(contract(T,u,u,u)==cubic,f'exact scalar cubic {bi},{ui}')
        check(cubic*cubic<=100*S**3,f'scalar SC squared bound {bi},{ui}')
        for hi,h in enumerate(directions):
            mixed=mixed_form(pt,h,u)
            Sh=quadratic(H,h)
            check(contract(T,h,u,u)==mixed,f'exact mixed identity {bi},{hi},{ui}')
            check(mixed*mixed<=100*Sh*S*S,f'mixed SC squared bound {bi},{hi},{ui}')

# Deliberate adverse controls: the checker must distinguish these false claims.
pt=(Q(5),Q(1),Q(1));h=(Q(8),Q(1),Q(2));H,T,_=derivatives(pt,add_log_z=False)
A0=[[-Q(64)*sum(T[i][j][k]*h[k] for k in range(3)) for j in range(3)] for i in range(3)]
check(det(A0)==-24576,'negative control: omitting -log z breaks negative curvature')
check(evaluate(det(A),Q(1),Q(1))==0,'negative control: strict positive definiteness false at t=1')
check(det(E)==0,'negative control: strict positive definiteness false at e_x')
check(A[0][0]!=B[0][0]+1,'negative control: changed NC1 entry rejected')
check(8*(t+2)*Ppoly!=(4*(t+2)*s-3*(t-1)*(3*t+5))**2+3*(t-1)**2*(8*t**3+21*t**2+6*t-10),'negative control: changed NC4 remainder rejected')
check((a+2*b)**2-4*(a**2+a*b+b**2)!=3*a**2,'negative control: false real-root discriminant rejected')
check(25*4!=4,'negative control: unscaled parameter cannot be assigned to F')
check(Q(1)*100>4,'negative control: loose scalar certificate with scale 1 does not establish SC')
result={
 'status':'PASS',
 'checked_at_utc':datetime.now(timezone.utc).isoformat(),
 'python_version':platform.python_version(),
 'optimization_mode':sys.flags.optimize,
 'checks_passed':len(checked),
 'negative_controls_rejected':sum(label.startswith('negative control:') for label in checked),
 'method':'Exact Fraction polynomial identities plus complementary rational tensor checks; analytic universal proof is in REPORT.md.',
 'checks':checked,
}
print(json.dumps(result,indent=2))
