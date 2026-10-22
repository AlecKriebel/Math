import itertools,json
from fractions import Fraction
import sympy as s
def require(ok):
    if not ok: raise RuntimeError("Exact verification failed")
z=(-1+s.sqrt(3)*s.I)/2
M=s.Matrix([[0,0,0,-1,-z,-s.expand(z*z),1,1,1],[1,1,1,0,0,0,-1,-z,-s.expand(z*z)],[-1,-z,-s.expand(z*z),1,1,1,0,0,0]])
G=(M.conjugate().T*M/2).applyfunc(s.simplify)
require((G*G-3*G).applyfunc(s.simplify)==s.zeros(9))
require(all(s.simplify(G[i,j]*s.conjugate(G[i,j]))==s.Rational(1,4) for i in range(9) for j in range(9) if i!=j))
blocks=[]
for m in range(2,9):
    r=Fraction(m,1+(m-1)*Fraction(1,4))
    if r.denominator!=1:continue
    for inds in itertools.combinations(range(9),m):
        H=G.extract(inds,inds)
        if (H*H-s.Rational(m,r.numerator)*H).applyfunc(s.simplify)==s.zeros(m):blocks.append(inds)
partitions=[]
for k in range(1,4):
    for chosen in itertools.combinations(blocks,k):
        inds=sum((list(t) for t in chosen),[])
        if len(set(inds))==len(inds):partitions.append(chosen)
result={'parameters':{'n':9,'d':3,'q':'1/4'},'proper_nonsingleton_tight_blocks_zero_based':blocks,'partitions_with_remaining_singletons':{str(k):sum(len(p)==k for p in partitions) for k in range(1,4)},'total_nontrivial_partitions':len(partitions),'verification':'Exact symbolic arithmetic in Q(sqrt(-3)); no numerical tolerance.'}
print(json.dumps(result,indent=2))
open('exact_results.json','w').write(json.dumps(result,indent=2)+'\n')
