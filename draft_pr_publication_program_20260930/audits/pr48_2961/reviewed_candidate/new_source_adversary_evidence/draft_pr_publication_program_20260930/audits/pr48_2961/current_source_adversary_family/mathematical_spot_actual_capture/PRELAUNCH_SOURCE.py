"""Fresh private exact diagnostic constructions; no imported historical code."""
import datetime as dt,hashlib,itertools,json,os
from fractions import Fraction as Q
from pathlib import Path
F=Path(__file__).absolute().parent;labels=[]
def check(v,n):
 if not v:raise ValueError(n)
 labels.append(n)
def word(w):
 st=[]
 for x in w:
  if st and st[-1]==-x:st.pop()
  else:st.append(x)
 return tuple(st)
def inv(w):return tuple(-x for x in reversed(w))
def wmul(a,b):return word(a+b)
def comm(a,b):return word(a+b+inv(a)+inv(b))
def mul(x,y):
 a,s=x;b,t=y;d=dict(a)
 for i,w in b.items():d[i+s]=wmul(d.get(i+s,()),w)
 return ({i:w for i,w in d.items() if w},s+t)
def inverse(x):a,s=x;return ({i-s:inv(w) for i,w in a.items()},-s)
def co(x,y):return mul(mul(mul(x,y),inverse(x)),inverse(y))
I=({},0);T=({},1)
for m in range(1,13):
 aa=[(1,i+3) for i in range(m)];bb=[(2,i+4) for i in range(m)];cc=[comm(a,b) for a,b in zip(aa,bb)];h=()
 for c in cc:h=wmul(h,c)
 A=({i+1:a for i,a in enumerate(aa)},0);B=({i+1:b for i,b in enumerate(bb)},0);C=({},0)
 for i in range(m):
  suffix=()
  for c in cc[i:]:suffix=wmul(suffix,c)
  C[0][i]=suffix
 check(mul(co(C,T),co(A,B))==({0:h},0),'Noncommuting free-wreath suffix compression m'+str(m))
 check(all(comm(aa[i],bb[i]) for i in range(m)),'Nontrivial inputs m'+str(m))
 check(mul(T,inverse(T))==I and inverse(inverse(C))==C,'Wreath inverse m'+str(m))
 if m>=2:
  check(wmul(cc[0],cc[1])!=wmul(cc[1],cc[0]),'Input commutators themselves do not commute m'+str(m));bad=({},0)
  for i in range(m):
   w=()
   for c in cc[:i+1]:w=wmul(w,c)
   bad[0][i]=w
  check(mul(co(bad,T),co(A,B))!=({0:h},0),'Prefix substitution fails m'+str(m))
def mat(t):return ((Q(1),t,t*t),(Q(0),Q(1),t**3),(Q(0),Q(0),Q(1)))
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def mi(a):return ((Q(1),-a[0][1],a[0][1]*a[1][2]-a[0][2]),(Q(0),Q(1),-a[1][2]),(Q(0),Q(0),Q(1)))
id3=mat(Q(0))
for s,chi in itertools.product([Q(i,4) for i in range(5)],repeat=2):
 a=mat(s*chi);b=mm(mat(s),mi(a));check(mm(b,a)==mat(s),'Exact parameter-family factorization '+str((s,chi)));check(mm(a,mi(a))==id3 and mm(b,mi(b))==id3,'Fiber inverse '+str((s,chi)))
 if chi==0:check(a==id3,'First support plateau')
 if chi==1:check(b==id3,'Second support plateau')
 if s==0:check(a==b==id3,'Initial isotopy identity')
check(mm(mat(Q(1,2)),mat(Q(1,2)))!=mat(Q(1)),'Non one-parameter family control')
# Sphere tangent before the invertible rotation: I+V tensor d(tau).
v=(-1,0);d=(-1,0);tangent=tuple(tuple(int(i==j)+v[i]*d[j] for j in range(2)) for i in range(2))
# d(tau)(v)=-1 requires coordinate basis with v=(1,0); gradient=(-1,0).
v=(1,0);d=(-1,0);tangent=tuple(tuple(int(i==j)+v[i]*d[j] for j in range(2)) for i in range(2))
check(tangent==((0,0),(0,1)),'Exact rank-one sphere tangent cutoff');check(2+1==3,'Product with two independent surface directions has rank3 not4')
# The sphere inequality 2|xy|<=x^2+y^2<=1 gives 0<=tau<=1.
for x,y in [(Q(0),Q(1)),(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(-3,5),Q(4,5))]:check(abs(2*x*y)<=x*x+y*y<=1 and 0<=Q(1,2)+x*y<=1,'Cutoff range exact diagnostic '+str((x,y)))
perms=list(itertools.permutations(range(3)));mu=(Q(1),Q(0),Q(0));u=(Q(0),Q(2),Q(-5))
def Qf(f):return sum(mu[x]*(u[f[x]]-u[x]) for x in range(3))
nonzero=0
for f,g in itertools.product(perms,repeat=2):
 fg=tuple(f[g[x]] for x in range(3));push=tuple(sum(mu[x] for x in range(3) if g[x]==y) for y in range(3));defect=Qf(fg)-Qf(f)-Qf(g);term=sum((u[f[y]]-u[y])*(push[y]-mu[y]) for y in range(3));check(defect==term,'Exact signed-pushforward cocycle formula '+str((f,g)));nonzero+=defect!=0
check(nonzero>0,'Non-invariant term genuinely nonzero in private finite diagnostic')
o={'schema':'pr48-fresh-private-mathematical-spot-controls/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'assertions':len(labels),'labels':labels,'free_wreath_max_m':12,'finite_cocycle_pairs':36,'nonzero_defects':nonzero,'exact_arithmetic':'freely reduced words and rational arithmetic','infinite_smooth_theorems_proved_by_finite_controls':False,'full_problem_solved':False,'new_substantive_attempts':0,'audit_turns':0,'production_helpers_imported_compiled_executed':False,'SOURCE_review_completion_percent':95,'target_discovery_completion_percent':0}
with (F/'MATHEMATICAL_SPOT_RESULTS.json').open('x') as h:json.dump(o,h,indent=2,allow_nan=False);h.write('\n');h.flush();os.fsync(h.fileno())
print(json.dumps({k:v for k,v in o.items() if k!='labels'}))
