"""Locally authored independent replay of explicit upstream JSON certificate data.
No producer program is imported or executed. Integer interval logs use 80-bit
fixed point and 32 series terms, independently of producer's 128/48 choices.
"""
from fractions import Fraction as F
from itertools import permutations,product
from functools import lru_cache
from math import isqrt,factorial
from pathlib import Path
import json,sys,hashlib
S=2**80;TERMS=32
count=0; groups={}
def ck(v,g):
 global count
 if not v:raise ValueError(g)
 count+=1;groups[g]=groups.get(g,0)+1
def ceildiv(a,b):return -((-a)//b)
def series(y):
 lo=y.numerator*S//y.denominator;hi=ceildiv(y.numerator*S,y.denominator)
 y2lo=lo*lo//S;y2hi=ceildiv(hi*hi,S);p,q=lo,hi;l=u=0
 for j in range(TERMS):
  l+=p//(2*j+1);u+=ceildiv(q,2*j+1)
  p=p*y2lo//S;q=ceildiv(q*y2hi,S)
 tail=ceildiv(9*S,4*(2*TERMS+1)*3**(2*TERMS+1))
 return 2*l,2*u+tail
LOG2=series(F(1,3))
@lru_cache(None)
def logbound(x):
 if x<=0:raise ValueError('log nonpositive')
 k=x.numerator.bit_length()-x.denominator.bit_length()
 scale=F(2**k) if k>=0 else F(1,2**(-k))
 u=x/scale
 if u<1:k-=1;u*=2
 if u>=2:k+=1;u/=2
 ck(1<=u<2,'log range')
 l,h=series((u-1)/(u+1))
 return (l+k*LOG2[0],h+k*LOG2[1]) if k>=0 else (l+k*LOG2[1],h+k*LOG2[0])
# Exact quadratic field for lower certificate.
def plus(x,y):return x[0]+y[0],x[1]+y[1]
def minus(x,y):return x[0]-y[0],x[1]-y[1]
def times(x,y):return x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def mul(x,a):return x[0]*a,x[1]*a
def sign(x):
 a,b=x
 if not b:return (a>0)-(a<0)
 if not a:return (b>0)-(b<0)
 if a*b>=0:return 1 if a>0 else -1
 d=a*a-3*b*b
 return ((d>0)-(d<0))*(1 if a>0 else -1)
Q=lambda a,b=0:(F(a),F(b))
sqrt=Q(0,1);a=Q(F(1,2),F(-1,4));b=Q(F(-3,4),F(1,2))
star=[Q(F(1,4)),a,a,b,a,b,b,mul(a,3)]
alpha=Q(F(1,2),F(-1,6));t=Q(F(3,2),F(-1,2));one=Q(1);zero=Q(0)
for x in range(8):
 prob=one
 for bit in range(3):prob=times(prob,t if x>>bit&1 else minus(one,t))
 prob=times(minus(one,alpha),prob)
 if x==0:prob=plus(prob,alpha)
 ck(prob==star[x] and sign(prob)>0,'parity mixture exact')
ck(sum(v[0] for v in star)==1 and sum(v[1] for v in star)==0,'parity normalization')
rows=[]
for x in range(8):
 for y in range(x+1,8):
  if x&y not in (x,y):
   row=[0]*8
   for i,c in [(x&y,1),(x|y,1),(x,-1),(y,-1)]:row[i]+=c
   rows.append(row)
   ck(sign(minus(times(star[x&y],star[x|y]),times(star[x],star[y])))>=0,'all supermodular inequalities')
ck(len(rows)==9,'nine incomparable rows')
active=[]
for x,y in [(3,5),(3,6),(5,6)]:
 row=[0]*8
 for i,c in [(x&y,1),(7,1),(x,-1),(y,-1)]:row[i]+=c
 active.append(row);ck(times(star[x&y],star[7])==times(star[x],star[y]),'active face')
for x in range(8):ck(minus(star[x],Q(F(1,4) if x.bit_count()%2==0 else 0))==mul(a,sum(r[x] for r in active)),'KKT exact gradient')
L=isqrt(3*S*S);ck(L*L<3*S*S<(L+1)**2,'sqrt interval')
slo,shi=F(L,S),F(L+1,S)
def qbounds(v):
 c,d=v
 return (c+d*slo,c+d*shi) if d>=0 else (c+d*shi,c+d*slo)
starlogs=[(logbound(qbounds(v)[0])[0],logbound(qbounds(v)[1])[1]) for v in star]
# c=-3/4 log(2sqrt3-3), an interval, not a decimal tolerance.
xlo,xhi=2*slo-3,2*shi-3
clo=-F(3,4)*logbound(xhi)[1];chi=-F(3,4)*logbound(xlo)[0]
E=tuple(F(1,4) if i.bit_count()%2==0 else F(0) for i in range(8));O=tuple(F(1,4)-x for x in E)
def delta(i):return tuple(F(int(i==j)) for j in range(8))
def roots(support):
 if support==(0,3,5,6):
  return [tuple(tuple(F(int(j in order[:k]),k) for j in range(8)) for k in range(1,5)) for order in permutations(support)]
 if support==(0,1,2,4,7):
  return [(delta(0),)+tuple(tuple(F(int(j in order[:k]),k) for j in range(8)) for k in range(1,5)) for order in permutations((1,2,4,7))]
 return [tuple(delta(i) for i in support)]
def sym(support,perm,flip):
 return tuple(sorted(sum(((x>>perm[i])&1)<<i for i in range(3))^flip for x in support))
reps=[(0,7),(0,3,5),(0,1,2,7),(0,3,5,6),(0,1,2,4,7),(0,1,2,5,6,7)]
allirr=[]
for mask in range(1,256):
 supp=tuple(i for i in range(8) if mask>>i&1)
 ok=True
 for bit in [1,2,4]:
  s0={x for x in supp if not x&bit};s1={x^bit for x in supp if x&bit}
  if s0<=s1 or s1<=s0:ok=False
 if ok:allirr.append(supp)
orbits=[{sym(s,p,f) for p in permutations(range(3)) for f in range(8)} for s in reps]
ck(set.union(*orbits)==set(allirr) and sum(map(len,orbits))==len(allirr)==50,'complete support orbits')
@lru_cache(None)
def entropy_upper(v):return sum((p*logbound(p)[1] for p in v if p),F(0))
def witness(w):
 if w['kind']=='star':
  ck(set(w)=={'kind','atom'} and type(w['atom'])==int and 0<=w['atom']<8,'star format')
  return [starlogs[x^w['atom']] for x in range(8)]
 ck(w['kind']=='mixture' and set(w)=={'kind','denominator','numerators'},'mixture format')
 den=w['denominator'];ns=w['numerators']
 ck(type(den)==int and den>0 and len(ns)==7 and all(type(x)==int and 0<=x<=den for x in ns),'mixture parameter membership')
 l,*params=[F(x,den) for x in ns];u=params[:3];v=params[3:]
 q=[]
 for x in range(8):
  p1=l;p2=1-l
  for i in range(3):p1*=u[i] if x>>(2-i)&1 else 1-u[i];p2*=v[i] if x>>(2-i)&1 else 1-v[i]
  q.append(p1+p2)
 ck(sum(q)==1 and min(q)>=0,'mixture normalization')
 return [logbound(x) if x else None for x in q]
def runfile(path):
 data=json.loads(path.read_text());support=tuple(data['support']);ck(data.get('format')=='rbm31-convex-cover-v1','certificate format');ck(support in reps,'allowed support')
 splits={};leaves={}
 for rec in data['splits']:
  ck(rec['path'] not in splits,'unique split');splits[rec['path']]=rec['edge']
 for rec in data['leaves']:
  ck(rec['path'] not in leaves and rec['path'] not in splits,'unique leaf');leaves[rec['path']]=rec['witness']
 reached=set();stack=[(str(i)+':',r,0) for i,r in enumerate(roots(support))];nleaf=nv=eq=depth=0;slack=None
 while stack:
  key,vertices,d=stack.pop();ck(key not in reached,'tree no repeated address');reached.add(key);depth=max(depth,d)
  if key in splits:
   edge=splits[key];ck(len(edge)==2 and all(type(x)==int and 0<=x<len(vertices) for x in edge) and edge[0]!=edge[1],'valid bisection')
   i,j=edge;m=tuple((x+y)/2 for x,y in zip(vertices[i],vertices[j]))
   for child,pos in [('0',i),('1',j)]:
    vs=list(vertices);vs[pos]=m;stack.append((key+child,tuple(vs),d+1))
  else:
   ck(key in leaves,'tree complete');w=leaves[key];logs=witness(w);nleaf+=1
   for v in vertices:
    nv+=1
    if v in (E,O):
     ck(w['kind']=='star' and w['atom'].bit_count()%2==(0 if v==E else 1),'exact parity equality');eq+=1
    else:
     ck(all(logs[i] is not None for i,p in enumerate(v) if p),'positive witness on target support')
     upper=entropy_upper(v)-sum((p*logs[i][0] for i,p in enumerate(v) if p),F(0))
     margin=clo-upper;ck(margin>0,'strict vertex KL bound');slack=margin if slack is None else min(slack,margin)
 ck(reached==set(splits)|set(leaves),'no orphan data')
 out={'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'leaves':nleaf,'vertices':nv,'parity_equalities':eq,'max_depth':depth,'strict_slack_lower_nats':str(slack/S)}
 print(json.dumps(out),flush=True);return out
if __name__=='__main__':
 source=Path(sys.argv[1]);names=['two','three','four','parity','five','six']
 for name,rep in zip(names,reps):ck(tuple(json.loads((source/(name+'.json')).read_text())['support'])==rep,'all six prescribed support files')
 results=[runfile(source/(name+'.json')) for name in names]
 out={'verdict':'PASS','assertions':count,'groups':groups,'certificates':results,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_code_executed':False,'scale_bits':80,'log_series_terms':32}
 Path('cover_verification.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',count)
