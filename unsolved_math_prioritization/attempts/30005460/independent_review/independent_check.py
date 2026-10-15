#!/usr/bin/env python3
"""Independent exact audit, standard library only. No author code is imported."""
import json,math,sys,hashlib
from fractions import Fraction as F
from collections import Counter
from itertools import product
from pathlib import Path
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
counts=Counter()
def ck(t,k):
 counts[k]+=1
 if not t:raise AssertionError((k,counts[k]))
def indices(n,d):
 if n==1:return [(i,) for i in range(d+1)]
 return [(i,)+rest for i in range(d+1) for rest in indices(n-1,d-i)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def normal(a):
 if any(x%2 for x in a):return 0
 return math.prod(math.prod(range(1,x,2)) for x in a)
M6={(6,0,0):2**24,(0,6,0):2**24,(4,2,0):1,(2,4,0):1,(0,0,6):1,(2,2,2):4,(2,0,4):32,(0,2,4):32,(4,0,2):4096,(0,4,2):4096}
T={8:10**16,10:10**34,12:10**53,14:10**73,16:10**94,18:10**116}
def mu(a):
 d=sum(a);ck(d<=18,'moment_domain')
 if any(x%2 for x in a):return F(0)
 if d==0:return F(1)
 if d in (2,4):return F(normal(a),1024)
 if d==6:return F(M6[a])
 return F(normal(a)*T[d])

def bareiss(A,label):
 """All leading principal minors, with no row swaps or numerical pivots."""
 A=[r[:] for r in A];n=len(A);prev=1;minors=[]
 for k in range(n):
  pivot=A[k][k];ck(pivot>0,label+'_positive_leading_minor');minors.append(pivot)
  if k==n-1:break
  for i in range(k+1,n):
   for j in range(i,n):
    val=pivot*A[i][j]-A[i][k]*A[k][j]
    quotient,remainder=divmod(val,prev)
    ck(remainder==0,label+'_fraction_free_exact_division')
    A[i][j]=quotient;A[j][i]=quotient
  for i in range(k+1,n): A[i][k]=A[k][i]=0
  prev=pivot
 return minors

basis=sorted(indices(3,9),key=lambda a:(sum(a),a))
ck(len(basis)==220,'basis_count')
parities=list(product(range(2),repeat=3)); cert=[]
for parity in parities:
 B=[a for a in basis if tuple(x%2 for x in a)==parity]
 A=[]
 for a in B:
  row=[]
  for b in B:
   v=1024*mu(add(a,b));ck(v.denominator==1,'integer_scaled_matrix');row.append(v.numerator)
  A.append(row)
 minors=bareiss(A,'order_nine')
 cert.append({'parity':list(parity),'monomials':[list(a) for a in B],'dimension':len(B),'scaled_leading_principal_minors':[str(v) for v in minors]})
for i,a in enumerate(basis):
 for b in basis[i+1:]:
  if tuple(x%2 for x in a)!=tuple(x%2 for x in b):ck(mu(add(a,b))==0,'all_cross_parity_entries_zero')

# Polynomial arithmetic and a separately transcribed a=1 published seed identity.
def plus(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,0)+v
 return {k:v for k,v in c.items() if v}
def scale(a,c):return {k:c*v for k,v in a.items() if c*v}
def times(a,b):
 c={}
 for i,v in a.items():
  for j,w in b.items():k=add(i,j);c[k]=c.get(k,0)+v*w
 return {k:v for k,v in c.items() if v}
def power(p,n):
 q={(0,)*len(next(iter(p))):1}
 for _ in range(n):q=times(q,p)
 return q
p={(4,2,0):1,(2,4,0):1,(0,0,6):1,(2,2,2):-1}
pairs=[((5,4,0),(3,4,2)),((4,5,0),(4,3,2)),((4,2,3),(2,2,5)),((2,4,3),(2,2,5)),((1,2,6),(3,4,2)),((2,1,6),(4,3,2)),((2,4,3),(4,2,3)),((4,5,0),(2,1,6)),((5,4,0),(1,2,6))]
extra=[((0,0,9),(2,2,5)),((1,1,7),(3,3,3)),((3,6,0),(3,4,2)),((3,5,1),(3,3,3)),((6,3,0),(4,3,2)),((5,3,1),(3,3,3))]
rhs={}
for a,b in pairs:rhs=plus(rhs,scale(power({a:1,b:-1},2),F(3,2)))
for a,b in extra:rhs=plus(rhs,power({a:1,b:-2},2))
rhs=plus(rhs,{(6,6,6):2})
lhs=power(p,3)
for a in indices(3,18):ck(lhs.get(a,0)==rhs.get(a,0),'all_cube_coefficients')
for a in set(lhs)|set(rhs):ck(sum(a)==18,'cube_homogeneity')
values=[sum(c*mu(a) for a,c in power(p,j).items()) for j in (1,2,3)]
ck(values==[-1,11292*10**53,35039520*10**116],'independent_seed_moments')
ck(sum(c*normal(a) for a,c in power(p,2).items())==11292,'Gaussian_square_value')
ck(sum(c*normal(a) for a,c in power(p,3).items())==35039520,'Gaussian_cube_value')
N=10**62;a1,a2,a3=values
exact=N*a3+3*N*(N-1)*a2*a1+N*(N-1)*(N-2)*a1**3
ck(a3<N*N-1,'dimension_bound')
ck(a2>=1,'second_moment_lower_bound')
ck(exact<=N*(a3-N*N+1)<0,'strict_negative_tensor_cube')
# Algebraic difference behind the displayed bound: 3N(N-1)(a2-1).
ck(N*(a3-N*N+1)-exact==3*N*(N-1)*(a2-1),'cubic_upper_bound_difference')

# A smaller genuinely coupled total-degree tensor matrix, built directly from
# split multi-indices, not from a tensor routine. Scaled by1024² to be integral.
B2=sorted(indices(6,3),key=lambda a:(sum(a),a));A2=[]
for a in B2:
 row=[]
 for b in B2:
  c=add(a,b);v=1024**2*mu(c[:3])*mu(c[3:]);ck(v.denominator==1,'two_block_integer_scaling');row.append(v.numerator)
 A2.append(row)
small_minors=bareiss(A2,'two_block_total_degree_three')
ck(len(B2)==84,'two_block_total_degree_basis')

for blocks in range(1,13):
 hist=Counter(tuple(sorted(Counter(f).values())) for f in product(range(blocks),repeat=3))
 ck(hist[(3,)]==blocks,'partition_single_block')
 ck(hist[(1,2)]==3*blocks*(blocks-1),'partition_two_blocks')
 ck(hist[(1,1,1)]==blocks*(blocks-1)*(blocks-2),'partition_three_blocks')
 actual=sum(F(count)*math.prod(values[i-1] for i in typ) for typ,count in hist.items())
 expected=blocks*a3+3*blocks*(blocks-1)*a1*a2+blocks*(blocks-1)*(blocks-2)*a1**3
 ck(actual==expected,'partition_evaluation')

# Turn1's explicit binomial split, all small odd parameter pairs.
for q in [1,3,5,7]:
 for t in [1,3,5,7]:
  deg=q+t-1
  left={(i,deg-i):math.comb(deg,i) for i in range(deg+1)}
  right={}
  for i in range(q):right[(i,deg-i)]=math.comb(deg,i)
  for j in range(t):right[(q+j,t-1-j)]=math.comb(deg,q+j)
  ck(left==right,'formal_binomial_split')
  for out in range(1,deg,2):
   i=min(q-1,out);j=out-i
   ck(i<q and j<t and math.comb(out,i)>0,'formal_ideal_obstruction')

certificate={'arithmetic':'Integer Bareiss elimination; matrices independently rebuilt from the written moment table. Scaling is positive1024.','order_nine_parity_blocks':cert,'two_block_total_degree_three':{'dimension':84,'matrix_scale':1024**2,'leading_principal_minors_sha256':hashlib.sha256(json.dumps([str(x) for x in small_minors]).encode()).hexdigest(),'all_positive':True},'seed_moments':[str(x) for x in values],'N':str(N),'negative_tensor_cube_value':str(exact)}
out=Path(__file__).with_name('INDEPENDENT_CERTIFICATE.json');out.write_text(json.dumps(certificate,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'full_moment_matrix_dimension':220,'positive_leading_minors':sum(x['dimension'] for x in cert),'independent_two_block_matrix_dimension':84,'certificate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'floating_point_used':False,'scope':'Exact finite certificate; arbitrary finite tensor positivity and source scope require the accompanying written review.'},indent=2,sort_keys=True))
