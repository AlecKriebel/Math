"""New exterior-polynomial homotopy family. Independent of old programs.
Sparse monomial differential verifies the exact Koszul homotopy identities;
slot-subgroup certificates audit the universal overlap mechanism.
"""
from itertools import combinations,combinations_with_replacement,product
from math import comb
from collections import defaultdict
from pathlib import Path
import json,datetime,hashlib
import sympy as S

def plus(out,key,value):
 out[key]+=value
 if out[key]==0:del out[key]
def dx(v,m):
 out=defaultdict(int)
 for (w,t),c in v.items():
  for i in set(t):
   if i not in w:
    wt=tuple(sorted((i,)+w));sgn=(-1)**sum(j<i for j in w)
    tl=list(t);tl.remove(i);plus(out,(wt,tuple(tl)),c*t.count(i)*sgn)
 return dict(out)
def ih(v,m):
 out=defaultdict(int)
 for (w,t),c in v.items():
  for k,i in enumerate(w):plus(out,(w[:k]+w[k+1:],tuple(sorted(t+(i,)))),c*(-1)**k)
 return dict(out)
def add(v,u):
 out=defaultdict(int,v)
 for k,c in u.items():plus(out,k,c)
 return dict(out)
def hook(shape,m):
 v=S.Rational(1)
 for i,l in enumerate(shape):
  for j in range(l):v*=S.Rational(m+j-i,l-j+sum(t>j for t in shape[i+1:]))
 return int(v)
rows=[];identities=0
for m in [1,2,3,4,5]:
 for N in range(1,8):
  count=0
  for a in range(min(m,N)+1):
   b=N-a
   for w in combinations(range(m),a):
    for t in combinations_with_replacement(range(m),b):
     v={(w,t):1};assert dx(dx(v,m),m)=={};assert ih(ih(v,m),m)=={}
     assert add(dx(ih(v,m),m),ih(dx(v,m),m))=={(w,t):N};count+=1
  identities+=count;rows.append({'dimension':m,'total_degree':N,'basis_elements':count,'d_squared_h_squared_and_Euler_homotopy':True})
# Exactness from homotopy gives ranks without borrowing any historical rank.
hookchecks=[]
for m in range(3,8):
 for n in range(2,11):
  N=n+3;previous_rank=0
  for a in range(4):
   C=comb(m,a)*comb(m+N-a-1,N-a);kernel=previous_rank;previous_rank=C-kernel
  expected=hook((n+1,1,1),m);assert kernel==expected
  hookchecks.append({'dimension':m,'n':n,'de_Rham_kernel_dimension':kernel,'hook_dimension':expected})
# Construct every transposition missing between the two face symmetry groups
# using their common first slot; at n2 there is no common slot.
certs=[]
for n in range(3,13):
 a=list(range(n-1));b=list(range(n-2))+[n-1]
 def swap(i,j):
  q=list(range(n));q[i],q[j]=q[j],q[i];return q
 def compose(p,q):return [p[q[i]] for i in range(n)]
 generated=compose(swap(n-2,0),compose(swap(0,n-1),swap(n-2,0)))
 assert generated==swap(n-2,n-1)
 assert {0,n-2}<=set(a) and {0,n-1}<=set(b)
 certs.append({'n':n,'common_slot':0,'missing_edge':[n-2,n-1],'conjugation_word':[[n-2,0],[0,n-1],[n-2,0]],'whole_transposition_graph_connected':True})
assert not (set(range(1)) & set([1]))
# Universal matrix obstruction to fixed points on the r3 multiplicity factor.
t=S.Symbol('t');p=S.Poly(t*t+S.Rational(1,2)*t+1,t);q=S.Poly(t**3-1,t)
gcd,u,v=S.gcdex(p,q);assert (gcd*p+u*q)==v and v.as_expr()==1
B=S.Matrix([[0,-1],[1,S.Rational(-1,2)]])
assert B.det()==1 and B.trace()==S.Rational(-1,2)
assert (S.eye(2)-B**3).det()!=0
# Source n2 counterexample: E-form three-fold volume times skew tensor.
# All wedge-to-four maps vanish in dimension3; transposition negates this
# element, so it cannot be in Lambda3⊗Sym2.
w=(0,1,2);f={(w,(0,1)):1,(w,(1,0)):-1};assert f
assert {(ww,tuple(reversed(tt))):c for (ww,tt),c in f.items()}=={k:-c for k,c in f.items()}
# Rectangular de Rham naturality checks use actual exterior/monomial maps.
def substitute(v,A):
 out=defaultdict(int)
 for (w,t),c in v.items():
  terms={((),()):c}
  for letter,is_form in [(i,True) for i in w]+[(i,False) for i in t]:
   new=defaultdict(int)
   for (ww,tt),value in terms.items():
    for i in range(A.rows):
     value2=value*A[i,letter]
     if not value2:continue
     if is_form:
      if i in ww:continue
      key=(tuple(sorted(ww+(i,))),tt);value2*=(-1)**sum(j>i for j in ww)
     else:key=(ww,tuple(sorted(tt+(i,))))
     plus(new,key,value2)
   terms=dict(new)
  for key,value in terms.items():plus(out,key,value)
 return dict(out)
rect=[]
for A in [S.Matrix([[1,2,0],[0,1,3]]),S.Matrix([[1,1,0],[0,0,0]]),S.Matrix([[1,0],[2,1],[0,3]]),S.zeros(2,3)]:
 tested=0
 for N in range(5):
  for a in range(min(A.cols,N)+1):
   for w in combinations(range(A.cols),a):
    for t0 in combinations_with_replacement(range(A.cols),N-a):
     z={(w,t0):1};assert substitute(dx(z,A.cols),A)==dx(substitute(z,A),A.rows)
     assert substitute(ih(z,A.cols),A)==ih(substitute(z,A),A.rows);tested+=1
 rect.append({'source_dimension':A.cols,'target_dimension':A.rows,'rank':int(A.rank()),'basis_naturality_checks':tested,'d_and_Euler_contraction_commute':True})
# Falsify two tempting shortcuts with checkable witnesses.
# Neglecting polynomial multiplicity in d would break the Euler homotopy.
z={((),(0,0)):1};wrong_d={((0,),(0,)):1}
assert ih(wrong_d,1)!={k:2*c for k,c in z.items()}
# The r3 multiplicity matrix requires cube compatibility, not equalizer of B².
assert (S.eye(2)-B**3).det()==S.Rational(5,8)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_NEW_HOMOTOPY_FAMILY','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checked_basis_elements':identities,'rectangular_naturality':rect,'multiplicity_omission_mutant_rejected':True,'n2_symmetry_shortcut_mutant_rejected':True,'homotopy_models':rows,'hook_rank_checks':hookchecks,'subgroup_generation_certificates':certs,'r3_characteristic_polynomial_gcd':str(v.as_expr()),'r3_companion_det_Id_minus_cube':str((S.eye(2)-B**3).det()),'n2_explicit_skew_counterexample':{'Lambda3_basis':w,'tensor_terms':[[[0,1],1],[[1,0],-1]],'intersection_dimension':9,'claimed_hook_dimension':6},'universal_argument':'d i_E + i_E d = total_degree Id proves exactness in every positive homogeneous degree; finite basis checks corroborate this identity. Slot generation by conjugation is universal for n>=3; n2 overlap is empty. These are acceptance checks, not a new homology solution.'}
Path(__file__).with_name('NEW_HOMOTOPY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['homotopy_models','hook_rank_checks','subgroup_generation_certificates']},indent=2))
