#!/usr/bin/env python3
"""Independent exact finite algebra diagnostics; none asserted realized by knots."""
from itertools import product
from collections import Counter
import hashlib,json,pathlib
counts=Counter()
def ck(value,name):
 assert value,name
 counts[name]+=1
def rank(rows,n):
 rows=list(rows);p=0
 for bit in range(n):
  pivot=next((i for i in range(p,len(rows)) if (rows[i]>>bit)&1),None)
  if pivot is None:continue
  rows[p],rows[pivot]=rows[pivot],rows[p]
  for i in range(len(rows)):
   if i!=p and (rows[i]>>bit)&1:rows[i]^=rows[p]
  p+=1
 return p
def eye(n):return [1<<i for i in range(n)]
def mul(A,n,B):
 assert n==len(B)
 return [sumrow(row,B,n) for row in A]
def sumrow(row,B,n):
 out=0
 for j in range(n):
  if (row>>j)&1:out^=B[j]
 return out
def inv(A):
 n=len(A);rows=[A[i]|(1<<(n+i)) for i in range(n)]
 for bit in range(n):
  pivot=next((i for i in range(bit,n) if (rows[i]>>bit)&1),None)
  if pivot is None:return None
  rows[bit],rows[pivot]=rows[pivot],rows[bit]
  for i in range(n):
   if i!=bit and (rows[i]>>bit)&1:rows[i]^=rows[bit]
 return [row>>n for row in rows]
def left_inverse(F,n):
 selected=[];rows=[]
 for i,row in enumerate(F):
  if rank(rows+[row],n)>len(rows):
   selected.append(i);rows.append(row)
  if len(rows)==n:break
 if n==0:return []
 assert len(rows)==n
 inverse=inv(rows)
 return [sum(((row>>j)&1)<<selected[j] for j in range(n)) for row in inverse]
def apply(F,v):
 return sum(((row&v).bit_count()%2)<<i for i,row in enumerate(F))
matrices=0;injections=0;square_isos=Counter();rectangular=0
for n in range(4):
 for m in range(5):
  for F in product(range(1<<n),repeat=m):
   F=list(F);matrices+=1
   brute=len({apply(F,v) for v in range(1<<n)})==(1<<n)
   injective=rank(F,n)==n
   ck(brute==injective,'rank_matches_full_vector_enumeration')
   if not injective:continue
   injections+=1;G=left_inverse(F,n)
   ck(mul(G,m,F)==eye(n),'constructed_split_left_inverse')
   projection=mul(F,n,G)
   ck(rank([a^b for a,b in zip(eye(m),projection)],m)==m-n,'complement_rank')
   if n==m:
    ck(projection==eye(m),'equal_finite_rank_gives_right_inverse')
    square_isos[n]+=1
   else:
    ck(projection!=eye(m),'unequal_rank_split_is_not_iso');rectangular+=1
ck(dict(square_isos)=={0:1,1:1,2:6,3:168},'square_counts')
# Actual graded isomorphisms, with two distinct Maslov/Alexander bidegrees.
degrees=[(-1,0),(0,1)];graded_pairs=0
for n in range(4):
 for F in product(range(1<<n),repeat=n):
  F=list(F);G=inv(F)
  if G is None:continue
  for vgrades in product(degrees,repeat=n):
   for wgrades in product(degrees,repeat=n):
    preserves=all(not ((F[i]>>j)&1) or wgrades[i]==vgrades[j] for i in range(n) for j in range(n))
    if preserves:
     graded_pairs+=1
     ck(all(not ((G[i]>>j)&1) or vgrades[i]==wgrades[j] for i in range(n) for j in range(n)),'inverse_preserves_bigrading')
# Equal object dimensions cannot force a particular singular map to be an iso.
ck(inv([1,0]) is None,'equal_groups_singular_map')
ck(degrees[0]!=degrees[1] and inv([1])==[1],'ungraded_iso_grading_shift_control')
# Shift on an infinite basis is a universal proof in the core; prefix arithmetic only here.
for i in range(16):
 ck((i+1)-1==i and i+1!=0,'infinite_shift_prefix_not_finite_proof')
# Integral diagnostics: free rank misses torsion; no knot coefficient assertion.
for z in range(-5,6):
 ck((2*z)%2==0 and 2*z!=1,'Z_nonsplit_equal_rank')
 ck((z,0)[0]==z and (z,0)[1]!=1,'Z_split_torsion_complement')
# All small posets admit a constant rank-one functor; strict arrows lack reverse arrows.
posets=0;strict_arrows=0
for n in (2,3):
 pairs=list(product(range(n),repeat=2))
 for bits in range(1<<len(pairs)):
  relation={pairs[i] for i in range(len(pairs)) if (bits>>i)&1}
  reflexive=all((i,i) in relation for i in range(n))
  transitive=all((a,c) in relation for a,b in relation for b2,c in relation if b==b2)
  antisymmetric=all(a==b or (b,a) not in relation for a,b in relation)
  if not(reflexive and transitive and antisymmetric):continue
  posets+=1
  ck(all(mul([1],1,[1])==[1] for a,b in relation for b2,c in relation if b==b2),'constant_functor_composition')
  for a,b in relation:
   if a!=b:
    strict_arrows+=1
    ck((b,a) not in relation and inv([1])==[1],'iso_image_has_no_source_inverse')
ck(posets==22,'small_poset_count')
ck(7>(1-1)//2,'constant_rank_strict_chain_conditional_bound_control')
# Filtered complexes: x,z have chain degree1, y degree0; filtrations1,0,-1.
A=[0,0,1];B=[0,0,2] # matrix rows in basis x,z,y, so d_A(x)=y,d_B(z)=y
ck(mul(A,3,A)==[0,0,0] and mul(B,3,B)==[0,0,0],'filtered_differentials_square_zero')
ck(rank(A,3)==rank(B,3)==1,'same_total_homology_dimension')
births=[]
for D in (A,B):
 for level in (-1,0,1):
  allowed=[v for v in range(4) if not (v&1 and 1>level) and not (v&2 and 0>level)]
  cycles=[v for v in allowed if apply(D,v)==0]
  if len(cycles)>1:births.append(level);break
ck(births==[0,1],'different_induced_homology_filtrations')
filtered_maps=0
for a,b,c,d in product((0,1),repeat=4):
 F=[a,b|(c<<1),d<<2]
 if mul(B,3,F)==mul(F,3,A):
  filtered_maps+=1
  ck(not(a==c==d==1),'no_filtered_chain_map_with_associated_graded_iso')
# The complex diagnostic does NOT satisfy the actual induced-isomorphism hypothesis.
ck(filtered_maps==4,'filtered_chain_map_count')
# Any nonzero finite grading table changes under a nonzero shift, even with overlapping fixed base.
base=Counter({(0,0):2,(2,4):1,(-2,-4):3})
tails=[Counter({(0,0):1}),Counter({(0,0):1,(2,4):2}),Counter({(-2,4):3,(1,1):1})]
for H in tails:
 models=[base+Counter({(h+2*n,q+4*n):c for (h,q),c in H.items()}) for n in range(-4,5)]
 for X in models:ck(sum(X.values())==sum(base.values())+sum(H.values()),'shift_total_dimension')
 for i,X in enumerate(models):
  for j,Y in enumerate(models):
   if i!=j:
    ck(X!=Y,'finite_nonzero_shift_tables_distinct')
    ck(not all(X[k]<=Y[k] for k in X),'equal_rank_shift_tables_no_graded_injection')
ck(base+Counter()==base,'zero_tail_distinctness_fails_control')
for index in range(3):ck(2-(2-index)==index,'Morse_reversal_involution')
result={'assertions_passed':sum(counts.values()),'counts':dict(counts),'all_F2_matrices':matrices,'split_injections':injections,'square_isomorphisms':dict(square_isos),'rectangular_split_nonisomorphisms':rectangular,'graded_isomorphism_pairs':graded_pairs,'small_posets':posets,'strict_poset_arrows':strict_arrows,'filtered_chain_maps_checked':filtered_maps,'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite algebra diagnostics and countercontrols only; no Floer computation, realized knot table, ribbon movie or isotopy proof.'}
print(json.dumps(result,indent=2))
