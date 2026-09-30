#!/usr/bin/env python3
"""Exact finite-module checks in independent, generally nontriangular bases.
Ranks use cardinalities of images, not Gaussian elimination. No Floer
realization is claimed. Standard library only.
"""
from collections import Counter
import json,random
counts=Counter()
rng=random.Random(2853)
def test(x,name):
 assert x,name
 counts[name]+=1
def partitions(n,cap=None):
 if n==0:
  yield ()
  return
 if cap is None:cap=n
 for j in range(min(cap,n),0,-1):
  for rest in partitions(n-j,j):yield (j,)+rest
def jordan(parts):
 columns=[];offset=0
 for length in parts:
  columns.append(0)
  for j in range(1,length):columns.append(1<<(offset+j-1))
  offset+=length
 return columns
def apply(columns,v):
 result=0
 while v:
  bit=(v&-v).bit_length()-1
  result^=columns[bit]
  v&=v-1
 return result
def logdimension(S):
 length=len(S)
 test(length>0 and length&(length-1)==0,'subspace_cardinality')
 return length.bit_length()-1
def mixed_basis(columns):
 A=list(columns);n=len(A)
 if n<2:return A
 for _ in range(3*n):
  p,q=rng.sample(range(n),2)
  def shear(v):return v^((1<<p) if (v>>q)&1 else 0)
  A=[shear(apply(A,shear(1<<j))) for j in range(n)]
 return A
case_count=0
for n in range(9):
 for parts in partitions(n):
  base=jordan(parts)
  for A in [base,mixed_basis(base)]:
   vectors=set(range(1<<n))
   images=[vectors]
   for k in range(max(n+1,2)):images.append({apply(A,v) for v in images[-1]})
   ranks=[logdimension(S) for S in images]
   test(images[n]=={0},'nilpotence')
   kernel={v for v in vectors if apply(A,v)==0}
   intersection=kernel&images[1]
   m1=parts.count(1)
   test(n-2*ranks[1]+ranks[2]==m1,'rank_second_difference')
   test(logdimension(kernel)-logdimension(intersection)==m1,'kernel_quotient_dimension')
   dual={f for f in vectors if all((f&col).bit_count()%2==0 for col in A)}
   ordered=sorted(kernel)
   functionals={sum(((f&v).bit_count()%2)<<i for i,v in enumerate(ordered)) for f in dual}
   test(logdimension(functionals)==m1,'restricted_dual_pairing_rank')
   for j in range(1,n+1):
    test(ranks[j-1]-2*ranks[j]+ranks[j+1]==parts.count(j),'all_block_multiplicities')
   case_count+=1
# A concrete length-two block: full evaluation is perfect, restricted pairing zero.
A=jordan((2,))
ker=[v for v in range(4) if apply(A,v)==0]
dual=[f for f in range(4) if all((f&col).bit_count()%2==0 for col in A)]
test(ker==[0,1] and dual==[0,2],'length_two_kernels')
test(all((x&f).bit_count()%2==0 for x in ker for f in dual),'length_two_pairing_zero')
test(all(any((x&f).bit_count()%2 for f in range(4)) for x in range(1,4)),
     'full_duality_perfect')
# The grading in the proposed abstract free chain complex.
test(-3-1==2*(-2)+0,'differential_maslov_degree')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),
                  'module_cases':case_count,'dimensions':list(range(9)),
                  'checks_by_category':dict(sorted(counts.items())),
                  'method':'Every Jordan partition through dimension eight, in its Jordan basis and a fixed-seed conjugate basis; image cardinalities and direct dual evaluations.',
                  'limitation':'Abstract finite F2[U]-module identities only; no knot or manifold counterexample and no Floer realization certificate.'},
                 indent=2,sort_keys=True))
