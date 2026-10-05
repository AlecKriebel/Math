"""Review-local exact checks. No import from candidate code or earlier reviews."""
import itertools, collections, json, sys
from fractions import Fraction as F
def require(c,m):
    if not c:raise RuntimeError(m)
# Positive-embedding Q(sqrt5) algebra, using pairs of rational coefficients.
def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def times(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(n,a):return (n*a[0],n*a[1])
# Cyclotomic ring with t^4=t^3-t^2+t-1, independently accumulated sparse terms.
def poly(terms):
    d=collections.defaultdict(int,terms)
    while any(k>=4 and c for k,c in d.items()):
        k=max(k for k,c in d.items()if k>=4 and c);c=d.pop(k)
        for offset,sign in [(1,1),(2,-1),(3,1),(4,-1)]:d[k-offset]+=sign*c
    return tuple(d.get(k,0)for k in range(4))
def power(n):return poly({n%10:1})
def product(a,b):
    d=collections.defaultdict(int)
    for i,x in enumerate(a):
        for j,y in enumerate(b):d[i+j]+=x*y
    return poly(d)
def sum_polys(items):return tuple(map(sum,zip(*items)))
def conjugate(a):return sum_polys([tuple(c*x for x in power(-j))for j,c in enumerate(a)])
one=power(0);rt5=sum_polys([one,tuple(2*x for x in power(2)),tuple(-2*x for x in power(3))])
require(product(rt5,rt5)==tuple(5*x for x in one),'sqrt5 algebra')
rho=(2,1,0,-1,-2);perms=list(itertools.permutations(range(5)))
def dot(x,y):return sum(a*b for a,b in zip(x,y))
lattice=[(a,b-a,c-b,d-c,-d)for a,b,c,d in itertools.product(range(5),repeat=4)]
require(len(set(lattice))==625,'quotient625')
require(all(sum(v)==0 for v in lattice),'root quotient')
records={}
for q in [1,2,3,4,6,7,-1,-2]:
    survivors=[];parts=[]
    for p in perms:
        w=tuple(rho[j]for j in p);sign=(-1)**sum(p[i]>p[j]for i in range(5)for j in range(i+1,5))
        v=tuple(q*r-s for r,s in zip(rho,w));counts=collections.Counter(dot(n,v)%5 for n in lattice)
        trivial=len({x%5 for x in v})==1
        require(counts==({0:625}if trivial else {i:125 for i in range(5)}),'full character histogram')
        if trivial:
            z=dot(rho,w);require(z%5==0,'survivorphase')
            survivors.append([list(w),sign,z,list(v)])
            parts.append(tuple(sign*x for x in power(-z//5)))
    require(len(survivors)==5,'survivorcount')
    B=sum_polys(parts);norm=product(B,conjugate(B))
    expected=sum_polys([tuple((11 if q%5 in(1,4) else 9)*x for x in one),tuple((2 if q%5 in(1,4) else 4)*x for x in rt5)])
    require(norm==expected,'phase norm')
    records[q]={'survivors':survivors,'B':B,'norm':norm}
A=sum_polys([tuple(((-1)**sum(p[i]>p[j]for i in range(5)for j in range(i+1,5)))*x for x in power(-2*dot(rho,tuple(rho[j]for j in p))))for p in perms])
require(A==sum_polys([tuple(10*x for x in one),tuple(-5*x for x in rt5)]),'S3Weyldenominator')
den=(225,-100);rationalizer=(225,100)
require(times(den,rationalizer)==(625,0),'rationalization')
targets=[(3475,1550),(4025,1800)]
if '--false-target'in sys.argv:targets[0]=(3476,1550)
for norm,target in [((11,2),targets[0]),((9,4),targets[1])]:require(times(rationalizer,norm)==target,'false normalized coefficient rejected')
require(times((F(9,2000),F(-4,2000)),times((100,40),(100,40)))==(1,0),'DinverseS00')
labels=[x for x in itertools.product(range(6),repeat=4)if sum(x)<=5]
sectors=collections.Counter(sum((j+1)*x for j,x in enumerate(lab))%5 for lab in labels)
require(len(labels)==126 and sectors=={0:26,1:25,2:25,3:25,4:25},'fullcenters')
# Translate the printed author vectors to Q(sqrt5): z100^20-z100^30=(sqrt5-1)/2.
def author_pair(a,b):return (F(a)-F(b,2),F(b,2))
DD=author_pair(125,-200);AA=author_pair(406250000,125000000);BB=author_pair(20312500000000,12500000000000)
require(AA==scale(50000,times(DD,(3475,1550))),'twoSwordnormalization')
require(BB==scale(50000**2,times(DD,(4025,1800))),'threeSwordnormalization')
require(plus(scale(50000,AA),scale(-1,BB))==author_pair(0,-6250000000000),'crossdifference')
require(all(any(x%5 for x in v)for w,s,z,v in records[1]['survivors'][1:]),'nonzero common residues retained')
print(json.dumps({'status':'PASS','ring':'Z[t]/Phi10, specified t=exp(pi*i/5)','full_center_sectors':dict(sectors),'lattice_size':len(lattice),'survivors_and_norms':records,'A':A,'positive_embedding':'t+t^-1=2cos36deg>1 selects (1+sqrt5)/2; sqrt5>0','targets':targets,'exact_matrix_normalization_powers':[50000,50000**2],'scope':'Finite verification of specialization, not new proof search or foundational category proof'},sort_keys=True,indent=2))
