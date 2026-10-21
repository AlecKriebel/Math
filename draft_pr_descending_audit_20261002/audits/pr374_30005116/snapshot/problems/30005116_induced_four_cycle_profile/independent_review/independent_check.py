import itertools,json,math
from fractions import Fraction as Q
import sympy as S
N=0
def ck(v):
 global N
 assert v;N+=1
def profile_above(p,c):
 q=1-p
 if q==0:return c<=0
 r=q.denominator//q.numerator;d=((r+1)*q-1)/r
 A=(1+6*r*d+r*(r*r-r+1)*d*d)/(r+1)**3;B=4*r*(r-1)*d/(r+1)**3
 # F=3(q²-A+B√d); compare exactly without numerical square root.
 v=c/3-q*q+A
 return v<=0 or v*v<=B*B*d
# Exhaustive weighted four-vertex hosts; independent induced-pattern counts,
# including sampled repetitions and recognition of the sole forbidden P4.
n=4;pairs=list(itertools.combinations(range(n),2));weights=[Q(i,10) for i in [1,2,3,4]]
for mask in range(64):
 adj=[[0]*n for _ in range(n)]
 for j,(u,v) in enumerate(pairs):adj[u][v]=adj[v][u]=(mask>>j)&1
 deg=[sum(row) for row in adj];is_p4=(sorted(deg)==[1,1,2,2] and sum(deg)==6)
 if is_p4:continue
 p=sum(weights[i]*weights[j]*adj[i][j] for i in range(n) for j in range(n));c=Q(0)
 for v in itertools.product(range(n),repeat=4):
  ds=[sum(adj[v[i]][v[j]] for j in range(4) if i!=j) for i in range(4)]
  if ds==[2]*4:c+=math.prod(weights[x] for x in v)
 ck(profile_above(p,c))
# Independently enumerate latent-product edge patterns with rational f values.
for f in [(Q(1,3),Q(2,3)),(Q(1,2),Q(1)),(Q(0),Q(3,4)),(Q(1,4),Q(1,2),Q(1))]:
 n=len(f);ms={j:sum(x**j for x in f)/n for j in [1,2,3]};c=Q(0)
 for v in itertools.product(range(n),repeat=4):
  for missing in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]:
   prob=Q(1,n**4)
   for i,j in pairs:
    edge=f[v[i]]*f[v[j]];prob*=1-edge if (i,j) in missing else edge
   c+=prob
 ck(c==3*(ms[2]**2-ms[3]**2)**2)
 p=ms[1]**2;R=3*p*p/16 if p<=Q(1,2) else 3*p**4*(1-p)**2
 ck(c<=R);ck(ms[3]*ms[1]>=ms[2]**2)
# Universal symbolic identities for first variation and moment derivative.
a,b,r=S.symbols('a b r');q=r*a*a+b*b
ck(S.expand(q-(a*a+a*b+b*b)-((r-1)*a*a-a*b))==0)
p=S.symbols('p');ck(S.factor(S.diff(3*p**4*(1-p)**2,p)-6*p**3*(1-p)*(2-3*p))==0)
ck(S.Rational(3,2)-3*S.Rational(3,4)**4==S.Rational(141,256))
ck((p*p*(1+p+p*p+p**3)-1).subs(p,S.Rational(3,4))==S.Rational(551,1024))
# Coupled union-density and gap controls, respecting x<=w.
for den in range(3,24):
 for i in range(den//2+1,den):
  x=Q(i,den)
  for j in range(i,den):
   w=Q(j,den);q=1-x;child=(x-(1-w)**2)/(w*w)
   ck(child>=x)
   ck((1-w**4)*Q(3,2)*q*q-Q(3,8)*(1-w)**4>=Q(3,8)*(1-w)*q*q*(4-q))
print(json.dumps({'status':'PASS','independent_assertions':N,'scope':'Independent weighted cograph motif counts, latent-product pattern integration, symbolic derivative/gap identities and coupled union controls; universal proofs audited separately.'},indent=2))
