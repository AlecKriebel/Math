#!/usr/bin/env python3
"""Exact coefficient-dependent Mayer–Vietoris/Deligne control.
Models GP's normally oriented cochain convention, not Hom(IC_m(Z),Z).
No triangulation, cup-i operation or universal theorem is implemented.
"""
from fractions import Fraction
from itertools import combinations
from math import gcd
from pathlib import Path
import json

def zero(n,m):return [[0]*m for _ in range(n)]
def matmul(a,b):
    n=len(a); k=len(a[0]) if n else len(b);m=len(b[0]) if b else 0
    return [[sum(a[i][r]*b[r][j] for r in range(k)) for j in range(m)] for i in range(n)]
def rank(a,field=None):
    if not a:return 0
    b=[[x%2 if field==2 else Fraction(x) for x in row] for row in a]
    r=0
    for j in range(len(b[0])):
        piv=next((i for i in range(r,len(b)) if b[i][j]),None)
        if piv is None:continue
        b[r],b[piv]=b[piv],b[r]
        d=b[r][j]
        if field!=2:b[r]=[x/d for x in b[r]]
        for i in range(len(b)):
            if i!=r and b[i][j]:
                t=b[i][j]
                b[i]=[(b[i][k]+b[r][k])%2 for k in range(len(b[0]))] if field==2 else [b[i][k]-t*b[r][k] for k in range(len(b[0]))]
        r+=1
        if r==len(b):break
    return r

def product_sphere(dims,ds):
    getdim=lambda q:dims[q] if 0<=q<len(dims) else 0
    getd=lambda q:ds[q] if 0<=q<len(ds) else zero(getdim(q+1),getdim(q))
    nd=[getdim(q)+getdim(q-2) for q in range(7)];ns=[]
    for q in range(6):
        a=getd(q);b=getd(q-2);M=zero(nd[q+1],nd[q])
        for i,row in enumerate(a):
            for j,x in enumerate(row):M[i][j]=x
        for i,row in enumerate(b):
            for j,x in enumerate(row):M[getdim(q+1)+i][getdim(q)+j]=x
        ns.append(M)
    return nd,ns

def check_complex(ds):
    for d,e in zip(ds,ds[1:]):assert all(x==0 for row in matmul(e,d) for x in row)

def cohom_dims(dims,ds,field):
    ranks=[rank(d,field) for d in ds]
    return [dims[q]-(ranks[q] if q<len(ranks) else 0)-(ranks[q-1] if q else 0) for q in range(len(dims))]

# RP3 ordinary cellular cochains have δ^1=2, δ^0=δ^2=0.
# A cone has Deligne truncation τ_{<=1}; its degree1 is ker(2).
# Over Z that kernel is0; over F2 it isF2. Suspension = mapping fiber
# of the difference of the two cone restrictions into the equatorial RP3.
Yz_dims=[2,1,1,1,1]
Yz_d=[[[1,-1]],[[0]],[[-2]],[[0]]]
Yf_dims=[2,3,1,1,1]
Yf_d=[[[0,0],[0,0],[1,-1]],[[1,-1,0]],[[0]],[[0]]]
check_complex(Yz_d);check_complex(Yf_d)
Xz_dims,Xz_d=product_sphere(Yz_dims,Yz_d)
Xf_dims,Xf_d=product_sphere(Yf_dims,Yf_d)
check_complex(Xz_d);check_complex(Xf_d)

# Natural coefficient reduction at X degree3: Y^3 plus shifted Y^1.
R3=[[1,0],[0,0],[0,0],[0,1]]
# The missing class is the shifted matching north/south degree1 cone class.
c=[0,1,1,0]
assert all(sum(row[j]*c[j] for j in range(4))%2==0 for row in Xf_d[3])
with_c=[row+[c[i]] for i,row in enumerate(R3)]
assert rank(with_c,2)==rank(R3,2)+1
# It is not merely an exact class: append it to the degree2 boundary image.
with_c_boundary=[row+[c[i]] for i,row in enumerate(Xf_d[2])]
assert rank(with_c_boundary,2)==rank(Xf_d[2],2)+1

assert Xz_d[3]==[[0,0],[0,0]]
D=Xz_d[2]
# Exact Smith invariants for the degree3 integer cokernel (two rows, full rank).
g1=0
for row in D:
    for x in row:g1=gcd(g1,abs(x))
g2=0
for i,j in combinations(range(len(D[0])),2):g2=gcd(g2,abs(D[0][i]*D[1][j]-D[0][j]*D[1][i]))
assert (g1,g2//g1)==(1,2)
# Degree4 has no incoming boundary and outgoing differential [0,-2].
assert Xz_d[4]==[[0,-2]]
assert all(x==0 for row in Xz_d[3] for x in row)

out={
 'space':'X=(suspension RP3) x S2',
 'dimension':6,'singular_strata':'two copies of S2, codimension4, link RP3',
 'cohomology_convention':'GP §3.1 normally oriented allowable cochains / Deligne lower-middle complex; on compact oriented X, IH_m^q=I^m H_{6-q}. Not Hom(IC_m(Z),Z).',
 'lower_middle_at_codimension4':1,
 'finite_model_provenance':'Coefficient-dependent Deligne truncation + two-cone Mayer–Vietoris mapping fiber, tensor cellular S2. Not a triangulation or cup-i model.',
 'Y_integer_dimensions':Yz_dims,'Y_integer_differentials':Yz_d,
 'Y_mod2_dimensions':Yf_dims,'Y_mod2_differentials':Yf_d,
 'X_integer_dimensions':Xz_dims,'X_integer_differentials':Xz_d,
 'X_mod2_dimensions':Xf_dims,'X_mod2_differentials':Xf_d,
 'Y_integer_cohomology':['Z','0','0','Z/2','Z'],
 'Y_mod2_cohomology_dimensions':cohom_dims(Yf_dims,Yf_d,2),
 'X_integer_free_cohomology_ranks':cohom_dims(Xz_dims,Xz_d,None),
 'X_mod2_cohomology_dimensions':cohom_dims(Xf_dims,Xf_d,2),
 'X_integer_degree3_smith_invariants':[g1,g2//g1],
 'X_integer_degree3_group':'Z/2','X_integer_degree4_group':'Z',
 'degree3_reduction_matrix':R3,'missing_mod2_cocycle':c,
 'degree3_mod2_class_not_in_reduction_image':True,
 'same_perversity_allowed_integral_lift_with_allowed_halved_differential_possible_for_missing_class':False,
 'pairing':{'matrix':[[0,1],[1,0]],'provenance':'Analytic product intersection formula and F2 duality on suspension; no cup-i calculation implemented.','witt_class':0,'counterexample_to_target':False},
 'link_criteria':{'middle_cohomology_degree':2,'H2_RP3_integer':'Z/2','middle_Bockstein_criterion_holds':False,'top_cohomology_degree':3,'H3_RP3_integer':'Z','top_Bockstein_criterion_holds':True},
 'printed_GP_lemma_falsified':False,
 'printed_same_middle_lift_premise_falsified':True,
 'universal_theorem_computationally_verified':False
}
assert out['X_mod2_cohomology_dimensions'][3]==2
assert out['X_integer_free_cohomology_ranks'][4]==1
Path(__file__).with_name('EXACT_LIFT_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['X_mod2_cohomology_dimensions','X_integer_free_cohomology_ranks','X_integer_degree3_smith_invariants','X_integer_degree3_group','X_integer_degree4_group','missing_mod2_cocycle','printed_same_middle_lift_premise_falsified']},indent=2))
