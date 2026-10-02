"""Exact finite controls for the actual smoothed family and validation algebra."""
from fractions import Fraction as F
from itertools import product
from math import factorial,comb
from collections import Counter
import json
C=Counter()
def ck(v,k):assert v,k;C[k]+=1
def kernel(h,j):return h**j/F(factorial(j)) if j>=0 else F(0) # common e^-h removed
for weights in product(range(3),repeat=4):
 if not sum(weights):continue
 pi=[F(t,sum(weights)) for t in weights];support=[i for i,t in enumerate(pi) if t];lo=min(support);m=max(support)
 for h in [F(1,3),F(1),F(3)]:
  q=lambda z:sum(pi[t]*kernel(h,z-t) for t in support)
  aa=lambda z:(z+1)*q(z+1)/q(z)-h if q(z) else F(0)
  for z in range(lo,9):
   ck((z+1)*q(z+1)-h*q(z)==sum(t*pi[t]*kernel(h,z+1-t) for t in support),'convolution_recurrence')
   ck(aa(z)>=0,'first_step_nonnegative')
   if z>=m:ck(aa(z)<=m*h/F(z+1-m),'summable_tail_envelope')
  for v in support:
   W=lambda z:sum(pi[t]*kernel(h,z-t) for t in support if t>=v)/q(z) if q(z) else F(0)
   for z in range(-1,9):ck(W(z+1)>=W(z),'posterior_tail_monotonicity')
   for Z in [m,m+1,m+4]:
    lhs=sum(sum(pi[t]*kernel(h,z-t) for t in support if t>=v)*aa(z) for z in range(lo,Z+1))
    rhs=sum(t*pi[t]*sum(kernel(h,j)*W(t+j-1) for j in range(max(0,Z+2-t))) for t in support)
    ck(lhs==rhs,'exact_truncated_shifted_suffix_identity')
  for sv,tv,z in product(range(4),range(4),range(-1,7)):
   if sv<tv:ck(kernel(h,z+1-tv)*kernel(h,z-sv)>=kernel(h,z-tv)*kernel(h,z+1-sv),'Poisson_kernel_TP2_minors')
# Weighted PAVA and exact final-suffix formula on arbitrary rational target arrays.
def pava(x,w):
 blocks=[]
 for i,(v,wt) in enumerate(zip(x,w)):
  blocks.append([i,i,wt,wt*v])
  while len(blocks)>1 and blocks[-2][3]/blocks[-2][2]>blocks[-1][3]/blocks[-1][2]:
   b=blocks.pop();a=blocks.pop();blocks.append([a[0],b[1],a[2]+b[2],a[3]+b[3]])
 out=[0]*len(x)
 for i,j,wt,total in blocks:
  for k in range(i,j+1):out[k]=total/wt
 return out
for x in product([F(0),F(1,2),F(2),F(5)],repeat=4):
 for w in product([F(1),F(2)],repeat=4):
  out=pava(x,w);last=max(sum(w[j]*x[j] for j in range(i,4))/sum(w[i:]) for i in range(4))
  ck(out[-1]==last,'last_isotonic_value_is_max_suffix')
  ck(all(out[i]<=out[i+1] for i in range(3)) and min(out)>=0,'PAVA_monotonicity_nonnegativity')
  ck(sum(out[i]*w[i] for i in range(4))==sum(x[i]*w[i] for i in range(4)),'PAVA_preserves_empirical_mean')
# Exact thinning coefficients, after cancelling the identical e^-lambda factor.
for u,v in product(range(9),repeat=2):
 for alpha,lam in product([F(1,3),F(3,4)],[F(0),F(1,2),F(3)]):
  eta=1-alpha
  left=lam**(u+v)/factorial(u+v)*comb(u+v,u)*alpha**u*eta**v
  right=(alpha*lam)**u/factorial(u)*(eta*lam)**v/factorial(v)
  ck(left==right,'exact_independent_Poisson_thinning')
for alpha,lam,V,g,h in product([F(1,3),F(4,5)],[F(0),F(1),F(3)],[F(0),F(1),F(5)],[F(0),F(1,2),F(3)],[F(0),F(2)]):
 eta=1-alpha;e=V-eta*lam
 score=(g-alpha*V/eta)**2-(h-alpha*V/eta)**2
 loss=(g-alpha*lam)**2-(h-alpha*lam)**2
 ck(score==loss-2*alpha*(g-h)*e/eta,'validation_difference_centering_and_sign')
 ck((g-h)**2<=2*(g-alpha*lam)**2+2*(h-alpha*lam)**2,'variance_loss_comparison')
for k in range(2,81):ck(factorial(k)>=2*3**(k-2),'Bernstein_Taylor_coefficient_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Finite algebra and projection controls only; the written proof gives infinite-sum and concentration arguments. Original full-data regret target remains unresolved.'},sort_keys=True,indent=2))
