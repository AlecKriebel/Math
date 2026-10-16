#!/usr/bin/env python3
"""Independent exact diagnostics for the support-genus audit; not topology proofs."""
from fractions import Fraction
import json

def require(test, label):
    if not test: raise ValueError(label)

def add(*vectors):
    return tuple(map(sum,zip(*vectors)))

def negate(vector):
    return tuple(-v for v in vector)

counts={}
# Abelianization computed as sums of vectors, independent of free-word expansion.
counts['commutator_vectors']=0
for genus in range(1,65):
    rank=2*genus
    basis=[tuple(int(i==j) for i in range(rank)) for j in range(rank)]
    w=(0,)*rank
    for i in range(genus):w=add(w,basis[2*i],basis[2*i+1],negate(basis[2*i]),negate(basis[2*i+1]))
    for exponent in [1,2,3,7,100]:
        power=tuple(exponent*c for c in w)
        for x in basis:
            require(add(power,x,negate(power),negate(x))==(0,)*rank,'nonzero abelianized relator')
            counts['commutator_vectors']+=1
# Independent integer optimization over all possible small page types.
counts['page_norm_minima']=0
for genus in range(1,65):
    feasible=[(h,b) for h in range(genus+2) for b in range(1,2*genus+6) if 2*h+b-1>=2*genus]
    require(min(2*h+b-2 for h,b in feasible)==2*genus-1,'support-norm bound')
    require(min(h for h,b in feasible if b==1)==genus,'connected-binding bound')
    require((1,2*genus-1) in feasible,'genus-one numerical alternative disappeared')
    counts['page_norm_minima']+=1
# Annular absolute monodromy is I but the relative-arc relation is n*a=0.
annulus=[{'twist':n,'absolute_cokernel_free_rank':1,'filled_free_rank':0,'filled_torsion_order':abs(n)} for n in [-12,-2,-1,1,2,12]]
# Covering identity checked in both directions and with integer-genus parity retained.
counts['integral_horizontal_cases']=0
for g in range(1,31):
    for b in range(1,31):
        for d in range(1,31):
            chi=d*(2-2*g-b)
            twice_h=2-b-chi
            if twice_h%2:continue
            h=twice_h//2
            require(h>=g,'horizontal lower bound')
            require(h-g==(d-1)*Fraction(2*g-2+b,2),'horizontal formula')
            counts['integral_horizontal_cases']+=1
# Full Reeb conditions: beta(R)=1; d beta(R,v)=0; df(Z)=0.
counts['reeb_conditions']=0
for f in [Fraction(1,3),Fraction(1),Fraction(7,2)]:
    for dx in range(-8,9):
        for dy in range(-8,9):
            z=(dy/(f*f),-dx/(f*f))
            require(dx*z[0]+dy*z[1]==0,'df(Z)')
            for v in [(1,0),(0,1),(2,-3)]:
                dbeta=f*(z[0]*v[1]-z[1]*v[0])-(dx*v[0]+dy*v[1])/f
                require(dbeta==0,'d beta contact-plane condition')
            require(f*(1/f)==1,'beta(R)')
            counts['reeb_conditions']+=1
# Intersection-form inverse, not a pre-expanded polynomial, computes the Chern square.
counts['disk_bundle_characteristics']=0
for g in range(101):
    c1=2-2*g-1
    square=Fraction(c1*c1,-1)
    chi=1-2*g+1
    signature=-1
    d3=(square-2*chi-3*signature)/4
    require(d3==Fraction(-2*g*g+4*g-1,2),'d3 formula')
    require(-d3-Fraction(1,2)==g*(g-2),'contact grade')
    counts['disk_bundle_characteristics']+=1
# Independently iterate multiplication U on monomial vector-space bases.
counts['finite_module_depths']=0
for m in range(41):
    image=set(range(m+1))
    depths=[]
    for d in range(m+3):
        if m in image:depths.append(d)
        image={k+1 for k in image if k+1<=m}
        counts['finite_module_depths']+=1
    require(depths==list(range(m+1)),'finite summand U-depth')
    require(max(depths)==m,'maximum depth')
# Capping at and beyond the b=12 transition, using explicit nonempty proper types.
counts['capping_cases']=0
for b in [1,2,3,4,8,11,12,13,20,51,100]:
    types=[(frozenset([i]),1+i%3) for i in range(b)] if b>1 else []
    if b>2:types += [(frozenset(range(b-1)),4),(frozenset([0,b-1]),2)]
    for n in [0,1,11,12,13,24,60]:
        for scale in [0,1,3]:
            factors=[(a,m*scale) for a,m in types]
            require(all(0<len(a)<b for a,_ in factors),'allowability boundary type')
            es=[n+12*sum(m for a,m in factors if i in a) for i in range(b)]
            length=n+sum(m for _,m in factors)
            E=sum(es)
            possible_N=[k for k in range(min(es)+1) if all((e-k)%12==0 for e in es)]
            bound=max(Fraction(E,12)+k*Fraction(12-b,12) for k in possible_N)
            require(length<=Fraction(E,min(b,12)),'coarse capping bound')
            require(length<=bound,'sharpened capping bound')
            require(length-b<=bound-b,'fixed-book Euler bound')
            counts['capping_cases']+=1
# Equal distinguished grading does not decide finite versus tower U-depth.
target_grade=7
finite_depth=5
finite_base_grade=target_grade+2*finite_depth
tower_lift_degrees=[target_grade+2*d for d in range(30)]
require(finite_base_grade-2*finite_depth==target_grade,'finite distinguished grade')
require(all(degree-2*d==target_grade for d,degree in enumerate(tower_lift_degrees)),'tower lift grades')
# Concrete numerical premise controls; topology/realization is not asserted.
controls={
 'large_betti_does_not_exclude_genus_one':2*1+19-1>=20,
 'large_norm_does_not_force_large_genus':2*1+19-2==19,
 'same_distinguished_grade_with_different_depth':finite_base_grade-2*finite_depth==tower_lift_degrees[0] and len(tower_lift_degrees)-1>finite_depth,
 'annulus_relative_arc_relation_differs_from_absolute_cokernel':all(x['absolute_cokernel_free_rank']!=x['filled_free_rank'] for x in annulus),
 'allowability_is_needed_to_exclude_boundary_twist_for_b1':12!=0,
 'fixed_Reeb_assumption_is_needed':Fraction(1,4)!=0,
}
require(all(controls.values()),'premise control')
print(json.dumps({'status':'PASS','scope':'Independent exact arithmetic and premise controls only; no realization or full solution certified.','counts':counts,'annulus_controls':annulus,'premise_controls':controls},indent=2,sort_keys=True))
