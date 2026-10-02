"""Independent exact controls for the random-order-type audit.
No author checker is imported. Analytic measure/geometric proofs remain essential.
"""
from fractions import Fraction as F
from math import comb,factorial
from itertools import combinations,product
from collections import Counter
import json
C=Counter()
def ck(name,ok):
 if not ok:raise AssertionError(name)
 C[name]+=1
# Different abscissae and sample sizes from the author's strip grids.
for n in (13,17,23):
 delta=F(1,16*n*n)
 xx=[F(3*i+1,3*n) for i in range(n)]
 for x,y,z in combinations(xx,3):
  for ex,ey,ez in product((-delta,delta),repeat=3):
   D=(y-x)*(z-x)*(z-y)+ex*(z-y)-ey*(z-x)+ez*(y-x)
   ck('parabolic_determinant_new_sizes',D>=(z-x)*((y-x)*(z-y)-2*delta)>0)
# Reconstruct the arrangement count and accumulated unlabeled lower bound.
L=1
for j in range(2,81):
 regions=1+comb(j,2)+j*(j-2)+(3*comb(j,4) if j>=4 else 0)
 ck('joining_line_regions',regions*8==j**4-6*j**3+23*j*j-26*j+8)
 ck('region_growth_bound',128*regions>(j+1)**4)
 L*=regions;n=j+1
 ck('unlabeled_factorial_lower_bound',F(L,factorial(n))>=F(1024*factorial(n)**3,128**n))
# Verify strip-selection budget constants at a range of rational masses.
for den in (7,13,29):
 for num in range(1,den+1):
  m=F(num,den)
  for n in (3,10,31):
   value=8*n/m;N=(value.numerator+value.denominator-1)//value.denominator
   ck('quantitative_interval_rounding',m*N/8>=n and N<=9*n/m)
   ck('bad_interval_budget',F(1,16)*m*m/(m/(4*N))==m*N/4)
   ck('strip_mass_constant',m/(8*N**3)>=m**4/(5832*n**3))
# A heavy dyadic interval control with an allowed atomic vertical measure.
atoms=[(F(j,17),F(j+1,153)) for j in range(17)]
lo,hi=F(0),F(1);mass=sum(w for x,w in atoms)
for k in range(1,31):
 mid=(lo+hi)/2
 choices=[(lo,mid),(mid,hi)]
 lo,hi=max(choices,key=lambda I:sum(w for x,w in atoms if I[0]<=x<=I[1]))
 local=sum(w for x,w in atoms if lo<=x<=hi)
 ck('heavy_closed_dyadic_interval',local>=mass/F(2**k) and hi-lo==F(1,2**k))
# Exact variance for a bounded iid kernel with diagonal index tuples removed.
# Kernel: all selected Bernoulli marks equal one; this tests the general pool
# identity, not a geometric population model.
q=F(2,5)
for n in (3,4,5):
 for M in (20,50,100):
  factor=F(factorial(M),factorial(M-n)*M**n)
  ex=ex2=F(0)
  for h in range(M+1):
   prob=comb(M,h)*q**h*(1-q)**(M-h)
   u=F(factorial(h),factorial(h-n)*M**n) if h>=n else F(0)
   ex+=prob*u;ex2+=prob*u*u
  ck('empirical_distinct_index_expectation',ex==factor*q**n)
  ck('empirical_overlap_variance',0<=ex2-ex*ex<=F(n*n,M))
# Opposite orientations under swapping two common underlying points.
for k in range(1,61):
 p=(F(0),F(0));q=(F(k),F(1));r=(F(1),F(k+2))
 orient=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 ck('color_overlap_orientation_contradiction',orient(p,q,r)==-orient(q,p,r)!=0)
for d in (F(1),F(4,5),F(3,5)):
 for ss in (F(0),F(1,2),F(1)):
  ck('singular_product_exponent', (3-2*ss/d>0)==(d>2*ss/3))
# Infinite-mixture proof: finite exact controls on its separate ingredients.
for i in range(1,51):
 xi=F(1,2**i)
 ck('separating_gradient_bound',1+4*xi*xi<4)
 ck('own_ball_negative',-xi*xi/16+xi*xi/64<0)
 for j in range(1,51):
  if j==i:continue
  xj=F(1,2**j)
  value=(xj-xi)**2-xi*xi/16
  ck('other_balls_positive',value-xj*xj/64>=F(14,64)*xj*xj>0)
# Ordered full binary trees and invariance under inserted unary chains.
from functools import lru_cache
@lru_cache(None)
def trees(n):
 if n==1:return (None,)
 return tuple((a,b) for k in range(1,n) for a in trees(k) for b in trees(n-k))
def paths(tree,prefix='',extra=False):
 if tree is None:return [prefix]
 out=[]
 for bit,child in enumerate(tree):
  padding='0'*(1+(len(prefix)%3)) if extra else ''
  out+=paths(child,prefix+str(bit)+padding,extra)
 return out
def lcp(a,b):
 k=0
 while k<min(len(a),len(b)) and a[k]==b[k]:k+=1
 return k
def sign(a,b,c):return 1 if lcp(a,b)<lcp(b,c) else -1
for n in range(1,9):
 ts=trees(n)
 ck('Catalan_tree_count',len(ts)==comb(2*n-2,n-1)//n and len(ts)<=4**(n-1))
 for tr in ts:
  a=paths(tr);b=paths(tr,extra=True)
  for i,j,k in combinations(range(n),3):
   ck('compressed_trie_orientation',sign(a[i],a[j],a[k])==sign(b[i],b[j],b[k]))
# Finite occupancy coefficient identity for a nonnegative test sequence.
weights=[F(1,2),F(1,3),F(1,6)]
pms=[F(1,2**max(0,m-2)**2) for m in range(10)]
coeff=[F(1)]
for w in weights:
 poly=[pms[m]*w**m/factorial(m) for m in range(10)]
 new=[F(0)]*(len(coeff)+len(poly)-1)
 for i,x in enumerate(coeff):
  for j,y in enumerate(poly):new[i+j]+=x*y
 coeff=new
for n in range(9):
 raw=F(0)
 for i in range(n+1):
  for j in range(n-i+1):
   k=n-i-j
   raw+=factorial(n)*pms[i]*pms[j]*pms[k]*weights[0]**i*weights[1]**j*weights[2]**k/F(factorial(i)*factorial(j)*factorial(k))
 ck('occupancy_generating_coefficient',raw==factorial(n)*coeff[n])
for z in (F(1,3),F(2),F(7)):
 G=sum(a*z**i for i,a in enumerate(coeff))
 for n in range(9):ck('positive_series_coefficient_bound',coeff[n]<=G/z**n)
for alpha in (2,3,5):
 for H in range(2,31):
  # Finite partial tails lie below the infinite integral upper bound.
  tail=sum(F(1,j**alpha) for j in range(H+1,301))
  ck('power_tail_integral_bound',tail<=F(1,(alpha-1)*H**(alpha-1)))
  for n in range(3,15):
   ck('odd_component_weight_bound',all(F(1,(2*j-1)**alpha)>=F(1,(4*n)**alpha) for j in range(n,2*n)))
for n in range(3,41):
 w=F(1,7)
 lower=F(1024*factorial(n)**3,128**n)*w**n/F(4**(n-1))
 ck('separate_actual_gap_constant',lower==4096*factorial(n)**3*(w/512)**n)
print(json.dumps({'status':'PASS_INDEPENDENT_CONTROLS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Independent exact geometry, counting, trace-selection constants, empirical kernels, binary-tree coding and positive generating-series controls. Infinite-dimensional and asymptotic statements are reviewed analytically, not inferred from these finite checks.'},indent=2,sort_keys=True))
