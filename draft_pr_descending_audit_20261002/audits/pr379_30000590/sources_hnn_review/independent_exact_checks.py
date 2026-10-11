#!/usr/bin/env python3
"""Independent exact finite checks; accompanying proofs cover the infinite claims.
Never read candidate data. Standard library only. Full deterministic JSON output.
"""
from itertools import permutations
from fractions import Fraction
import json

def rank(a):
    a=[[Fraction(x) for x in row] for row in a]
    if not a:return 0
    m,n=len(a),len(a[0]);i=0
    for j in range(n):
        p=next((k for k in range(i,m) if a[k][j]),None)
        if p is None:continue
        a[i],a[p]=a[p],a[i];z=a[i][j];a[i]=[x/z for x in a[i]]
        for k in range(m):
            if k!=i and a[k][j]:
                z=a[k][j];a[k]=[x-z*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==m:break
    return i

G=list(permutations(range(3)));one=(0,1,2);swap=(1,0,2);H=[one,swap]
def mul(a,b):return tuple(a[b[i]] for i in range(3))
def inv(a):return tuple(a.index(i) for i in range(3))
T=[]
for g in G:
    if not any(g==mul(h,t) for h in H for t in T):T.append(g)
coords=[(t,h) for t in T for h in H]
def theta(g):
    return [int(mul(t,g)==h) for t,h in coords]
matrix=[[theta(g)[i] for g in G] for i in range(len(coords))]
left_checks=[]
for a in G:
 for g in G:
  lhs=theta(mul(a,g));rhs=[]
  # f(t a) is recovered by writing t a = h0 t0.
  for t,h in coords:
   h0,t0=next((h0,t0) for h0 in H for t0 in T if mul(t,a)==mul(h0,t0))
   rhs.append(int(mul(t0,g)==mul(inv(h0),h)))
  assert lhs==rhs
  left_checks.append({'a':list(a),'basis_g':list(g),'result':lhs})
right_checks=[]
for h1 in H:
 for g in G:
  lhs=theta(mul(g,h1));rhs=[int(mul(t,g)==mul(h,inv(h1))) for t,h in coords]
  assert lhs==rhs
  right_checks.append({'h':list(h1),'basis_g':list(g),'result':lhs})
assert rank(matrix)==len(G)
fi={'group':'S3','subgroup':'<swap01>, nonnormal index3','G':G,'H':H,'left_coset_reps':T,'coinduced_coordinates':coords,'Theta_matrix':matrix,'rank':rank(matrix),'left_G_checks':left_checks,'right_H_checks':right_checks,
    'induced_not_original_example':{'G':'Z','H':'2Z','original_H1_abelian_rank':1,'induced_subgroup_H1_abelian_rank':2,'induced_t_action_matrix':[[0,1],[1,0]],'restricted_original_subgroup_action':[[1]]}}

height=[]
for m in (1,2,3,4,7):
 cyc=[[int(i==j)-int(i==(j+1)%m) for j in range(m)] for i in range(m)]
 trunc=[[int(i==j)-int(i==j+1) for j in range(m)] for i in range(m)]
 kernel_vector=[1]*m
 assert all(sum(x*y for x,y in zip(row,kernel_vector))==0 for row in cyc)
 assert rank(cyc)==m-1 and rank(trunc)==m
 height.append({'m':m,'periodic_1_minus_T':cyc,'periodic_rank':rank(cyc),'periodic_kernel_vector':kernel_vector,'truncated_1_minus_T':trunc,'truncated_rank':rank(trunc),'truncated_cokernel_rank':m-rank(trunc)})

square=[]
for n in (1,2,3,5,8):
 # basis1,e0,...,e(n-1); left or right multiplication e0.
 M=[[int(i==1 and j==0) for j in range(n+1)] for i in range(n+1)]
 assert rank(M)==1
 square.append({'square_zero_rank_V':n,'multiplication_e0':M,'kernel_Z_rank':n,'cokernel_Z_rank':n,'kernel_action':'integer scalar only; every e_j acts as zero'})

# At augmentation a=1 the exact resolution matrix a-1 becomes [0].
flat={'ring':'Z[a,a^-1]','cochain_degrees':[0,1],'differential':'a-1','before_specialization_H0':'0 (Laurent domain)','before_specialization_H1':'Z','specialization':'a->1','specialized_matrix':[[0]],'specialized_H0_Z_rank':1,'specialized_H1_Z_rank':1,'Tor1_R_Z_Z':'Z','flat_specialization_claim_falsified':True}
out={'scope':'Exact finite falsifiers; no finite-output extrapolation','finite_index_right_actions':fi,'height_periodic_and_cutoff_falsifiers':height,'square_zero_finite_matrix_falsifier':square,'nonflat_specialization_falsifier':flat}
print(json.dumps(out,indent=2))
