"""Exact signed-permutation controls for a necessary geometric restriction."""
from itertools import permutations,product
from math import gcd,lcm
from collections import Counter
import json
import sympy as S
C=Counter()
def ck(p,k):assert p,k;C[k]+=1
def compose(A,B):
 p,s=A;q,t=B
 return tuple(p[q[i]] for i in range(len(p))),tuple(t[i]*s[q[i]] for i in range(len(p)))
def power(A,k):
 n=len(A[0]);out=(tuple(range(n)),(1,)*n)
 for _ in range(k):out=compose(A,out)
 return out
def cycles(A):
 p,s=A;seen=set();out=[]
 for start in range(len(p)):
  if start in seen:continue
  i=start;word=[];sign=1
  while i not in seen:seen.add(i);word.append(i);sign*=s[i];i=p[i]
  out.append((tuple(word),sign))
 return out
def kind(A):return sorted((len(w),e) for w,e in cycles(A))
for n in range(5):
 I=(tuple(range(n)),(1,)*n)
 for p in permutations(range(n)):
  for signs in product((-1,1),repeat=n):
   A=(p,signs);cyc=cycles(A);r=lcm(*(len(w)*(1 if e==1 else 2) for w,e in cyc))
   ck(power(A,r)==I,'signed_cycle_order_upper')
   for d in range(1,r):
    if r%d==0:ck(power(A,d)!=I,'signed_cycle_order_exact')
   change=[1]*n;expected=[1]*n
   for w,e in cyc:
    for i,j in zip(w,w[1:]):change[j]=change[i]*signs[i]
    expected[w[-1]]=e
   new=tuple(change[i]*signs[i]*change[p[i]] for i in range(n))
   ck(new==tuple(expected),'explicit_orientation_normalization')
   for m in range(r,25,r):
    good=all(e==1 or 2*len(w)==m for w,e in cyc)
    if good and any(e==-1 for w,e in cyc):
     ck(r==m,'negative_geometric_condition_implies_faithfulness')
     ck(m<=2*n,'negative_geometric_order_bound')
    if good and r<m:ck(all(e==1 for w,e in cyc),'nonfaithful_geometric_condition_unsigned')
    for a in range(1,m+1):
     if gcd(a,m)==1:ck(kind(power(A,a))==kind(A),'all_tested_primitive_generator_changes')
# Three abstract homomorphisms that violate the proved necessary condition.
for m,A in [(4,((0,),(-1,))),(8,((1,0),(1,-1))),(12,((1,0,3,4,2),(1,-1,1,1,1)))]:
 I=(tuple(range(len(A[0]))),(1,)*len(A[0]));ck(power(A,m)==I,'excluded_example_is_abstract_homomorphism')
 ck(any(e==-1 and 2*len(w)!=m for w,e in cycles(A)),'excluded_example_violates_geometry')
A=((1,0,3,4,2),(1,-1,1,1,1));ck(lcm(*(len(w)*(1 if e==1 else 2) for w,e in cycles(A)))==12,'faithful_excluded_example')
# Orientation-reversing ambient control: period4, reversal on invariant circle.
H=S.diag(1,-1,S.Matrix([[0,-1],[1,0]]))
ck(H.T*H==S.eye(4),'ambient_countercontrol_orthogonal')
ck(H.det()==-1,'ambient_countercontrol_wrong_orientation')
ck(H**4==S.eye(4) and H**2!=S.eye(4),'ambient_countercontrol_order_four')
ck(H[:2,:2].det()==-1 and H[:2,:2]**2==S.eye(2),'invariant_circle_reversed')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite signed-permutation and orthogonal-matrix checks only; the periodic-reversal lemma and all-order nonrealization restriction are proved analytically. No sufficiency or link construction is inferred.'},indent=2,sort_keys=True))
