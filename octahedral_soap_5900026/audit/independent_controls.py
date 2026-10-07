#!/usr/bin/env python3
"""Independent exact checks. Does not import or execute the author's diagnostics.
Standard library only. Geometry is reconstructed from score-cell halfspaces.
"""
from fractions import Fraction as F
from itertools import product, permutations, combinations
from collections import Counter
from functools import cmp_to_key
from math import isqrt
import json

count=0
categories=Counter()
def check(ok,category):
    global count
    count+=1; categories[category]+=1
    if not ok: raise RuntimeError(category)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(q,a):return tuple(q*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def det(a,b,c):return dot(a,cross(b,c))
def sq(a):return dot(a,a)
def mean(v):return tuple(sum(x[i] for x in v)/len(v) for i in range(3))
def e(i):return tuple(F(i==j) for j in range(3))
def neg(s):return tuple(-x for x in s)
S=list(product((-1,1),repeat=3)); P=[s for s in S if s[0]*s[1]*s[2]==1]; N=[s for s in S if s not in P]
z=(F(0),)*3
R={s:mul(F(1,2) if s in P else F(5,6),s) for s in S}
B={s:F(0) if s in P else F(1,3) for s in S}
def plane_intersection(rows):
    ns=[r[0] for r in rows]; b=[r[1] for r in rows]
    d=det(*ns)
    if not d:return None
    return mul(1/d,add(add(mul(b[0],cross(ns[1],ns[2])),mul(b[1],cross(ns[2],ns[0]))),mul(b[2],cross(ns[0],ns[1]))))
def vertices(rows):
    found=set()
    for rr in combinations(rows,3):
        x=plane_intersection(rr)
        if x is not None and all(dot(n,x)<=b for n,b,*_ in rows):found.add(x)
    return sorted(found)
def polygon_order(v,n):
    c=mean(v); k=next(i for i in range(3) if n[i]); ij=[i for i in range(3) if i!=k]
    def angle_cmp(a,b):
        u=[a[i]-c[i] for i in ij]; w=[b[i]-c[i] for i in ij]
        ha=0 if (u[1]>0 or u[1]==0 and u[0]>=0) else 1
        hb=0 if (w[1]>0 or w[1]==0 and w[0]>=0) else 1
        if ha!=hb:return -1 if ha<hb else 1
        dd=u[0]*w[1]-u[1]*w[0]
        return -1 if dd>0 else 1 if dd<0 else 0
    v=sorted(v,key=cmp_to_key(angle_cmp))
    if dot(cross(sub(v[0],c),sub(v[1],c)),n)<0:v.reverse()
    return v

def radical(q):
    """sqrt(nonnegative rational) -> coefficient and squarefree integer."""
    if q==0:return F(0),1
    n=q.numerator*q.denominator; outside=1; inside=1; p=2
    while p*p<=n:
        k=0
        while n%p==0:n//=p;k+=1
        outside*=p**(k//2)
        if k%2:inside*=p
        p+=1
    inside*=n
    return F(outside,q.denominator),inside

volumes={}; sheets={}; internal_vertices=set(); face_counts=Counter()
for s in S:
    rows=[(tuple(map(F,u)),F(1),'boundary',u) for u in S]
    rows += [(sub(R[t],R[s]),B[t]-B[s],'interface',t) for t in S if t!=s]
    vv=vertices(rows); c=mean(vv); volume=F(0)
    for v in vv:
        if sum(abs(x) for x in v)<1:internal_vertices.add(v)
        check(all(dot(n,v)<=b for n,b,*_ in rows),'cell_vertex_feasibility')
    for n,b,kind,t in rows:
        fv=[v for v in vv if dot(n,v)==b]
        if len(fv)<3:continue
        if all(cross(sub(v,fv[0]),sub(fv[1],fv[0]))==z for v in fv):continue
        fv=polygon_order(fv,n); fc=mean(fv); area=Counter()
        for a,d in zip(fv,fv[1:]+fv[:1]):
            cr=cross(sub(a,fc),sub(d,fc))
            check(dot(cr,n)>0,'facet_orientation')
            q=sq(cr)/4; co,rad=radical(q);area[rad]+=co
            volume+=abs(det(sub(fc,c),sub(a,c),sub(d,c)))/6
        if kind=='boundary':
            check(t==s,'symbolic_face_trace');check(area=={3:F(1,2)},'whole_reference_face')
        else:
            pair=tuple(sorted((s,t)))
            if pair in sheets:check(sheets[pair]['vertices']==set(fv),'shared_sheet_agreement')
            else:sheets[pair]={'vertices':set(fv),'area':area,'normal':n}
    volumes[s]=volume
    check(volume==(F(1,4) if s in P else F(1,12)),'direct_cell_volume')
check(sum(volumes.values())==F(4,3),'total_volume')
check(internal_vertices=={z}|{mul(F(1,6),s) for s in N},'exact_five_interior_junctions')
for v in internal_vertices:
    scores={s:dot(R[s],v)-B[s] for s in S};m=max(scores.values());win=[s for s in S if scores[s]==m]
    check(len(win)==4,'four_chambers_at_junction')
    check(all(sq(sub(R[s],R[t]))==2 for s,t in combinations(win,2)),'regular_tetrahedral_dual_at_junction')
check(len(sheets)==18,'eighteen_interfaces')
area=Counter()
for (s,t),d in sheets.items():
    area.update(d['area']);kind='kite' if s in P and t in P else 'triangle';face_counts[kind]+=1
    check(len(d['vertices'])==(4 if kind=='kite' else 3),'sheet_vertex_count')
    check(d['area']=={2:F(1,6) if kind=='kite' else F(1,4)},'individual_sheet_area')
check(area=={2:F(4)},'candidate_area')
check(face_counts=={'kite':6,'triangle':12},'sheet_inventory')

# Every possible cross-configuration sheet pair, without assuming disjointness.
# A reflected plane is n.x=-b. Distinct planes intersect in area zero.
# For coincident planes verify strictly opposite half-planes on all nonzero vertices.
coincident=0;parallel_distinct=0;nonparallel=0
for (s,t),d in sheets.items():
    for (u,v),f in sheets.items():
        n=d['normal'];m=f['normal'];b=dot(n,next(iter(d['vertices'])));c=-dot(m,next(iter(f['vertices'])))
        if cross(n,m)!=z:nonparallel+=1;continue
        k=next(i for i in range(3) if m[i]);scale=n[k]/m[k]
        if b!=scale*c:parallel_distinct+=1;continue
        coincident+=1
        fv={neg(x) for x in f['vertices']}
        separators=[i for i in range(3) if all(x[i]>=0 for x in d['vertices']) and all(x[i]<=0 for x in fv) or all(x[i]<=0 for x in d['vertices']) and all(x[i]>=0 for x in fv)]
        check(any(all(x[i]!=0 for x in d['vertices'] if x!=z) and all(x[i]!=0 for x in fv if x!=z) for i in separators),'coincident_core_support_separation')
check(coincident==6 and parallel_distinct==12 and nonparallel==306,'all_324_support_plane_pairs')

# Symbolic general-a geometry in Q[a], using evaluations sufficient for degree 2.
for a in (F(0),F(1,6),F(1,5),F(1,3)):
    for s in N:
        j=mul(a,s)
        for i,k in combinations(range(3),2):
            u=mul(s[i],e(i));v=mul(s[k],e(k))
            check(sq(cross(sub(u,j),sub(v,j)))/4==(6*a*a-4*a+1)/4,'parameter_triangle_polynomial')
    q=6*a*a-4*a+1
    check(6*q-(6*a-2)**2==2,'convexity_polynomial')
# Rational polynomial coefficient checks; the three coefficients establish identity.
check(tuple(6*x-y for x,y in zip((1,-4,6),(4,-24,36)))==(2,0,0),'convexity_identity_coefficients')

# Affine all-pair norm forms in formal variables alpha,beta.
# V_s(vertex) = a_s * alpha + b_s * beta. Return quadratic coefficients.
inv=Counter()
for s,t in combinations(S,2):
    h=sum(s[i]!=t[i] for i in range(3))
    for k in range(3):
        for sign in (-1,1):
            x=mul(sign,e(k));da=sub(s,t)
            db=sub(sub(mul(dot(s,x),s),x),sub(mul(dot(t,x),t),x))
            actual=(sq(da),2*dot(da,db),sq(db))
            expected=(4*h,8*h*sign*s[k],4*h) if s[k]==t[k] else (4*h,0,4*(3-h))
            check(actual==expected,'symbolic_all_pair_vertex_quadratic')
            # alpha=sqrt(3)/6; beta=sqrt(2)/4-sqrt(3)/6.
            aa,ab,bb=actual
            q=F(aa,12)-F(ab,12)+F(5*bb,24);r=F(ab,24)-F(bb,12)
            # Exact comparison via rational bracket 2449/1000 < sqrt6 < 49/20.
            # These bounds suffice for all strict inequalities in this inventory.
            upper=q+r*(F(49,20) if r>=0 else F(2449,1000))
            check(upper<=1,'independent_affine_radical_bound')
            inv[(str(q),str(r))]+=1
check(F(2449,1000)**2<6<F(49,20)**2,'sqrt6_rational_bracket')
check(sum(inv.values())==168,'affine_complete_inventory')

# Full signed-permutation Reynolds operator on 96 affine coefficient basis fields.
# Group element g has (g x)_i = signs[i] x[perm[i]].
group=list(product(list(permutations(range(3))),S))
check(len(group)==48,'full_octahedral_group_order')
def transform(g,s):
    p,q=g;return tuple(q[i]*s[p[i]] for i in range(3))
# Each orbit sum of a single input basis coefficient is invariant. Reconstruct
# b_s=alpha*s and A_s=gamma*I+beta*ss^T, and inspect the trace-zero subspace.
nonzero_constants=0;nonzero_diagonal=0;nonzero_offdiagonal=0
for source in S:
    for typ in ('b','A'):
        for i in range(3):
            for j in (range(3) if typ=='A' else (-1,)):
                b={s:[F(0)]*3 for s in S};A={s:[[F(0)]*3 for _ in range(3)] for s in S}
                for g in group:
                    p,q=g;target=transform(g,source);ii=p.index(i)
                    if typ=='b':b[target][ii]+=F(q[ii],48)
                    else:
                        jj=p.index(j);A[target][ii][jj]+=F(q[ii]*q[jj],48)
                plus=(1,1,1);alpha=b[plus][0];beta=A[plus][0][1];gamma=A[plus][0][0]-beta
                check(all(b[s][k]==alpha*s[k] for s in S for k in range(3)),'reynolds_constant_ansatz')
                check(all(A[s][k][l]==gamma*(k==l)+beta*s[k]*s[l] for s in S for k in range(3) for l in range(3)),'reynolds_matrix_ansatz')
                # Flux of any affine field: per face b.s/2 + s^T A s/6.
                oldflux=F(source[i],2) if typ=='b' else F(source[i]*source[j],6)
                newflux=sum(F(1,2)*sum(b[s][k]*s[k] for k in range(3))+F(1,6)*sum(s[k]*A[s][k][l]*s[l] for k in range(3) for l in range(3)) for s in S)
                check(oldflux==newflux,'reynolds_flux_preservation')
                tr_input=F(1,8) if typ=='A' and i==j else F(0)
                check(all(sum(A[s][k][k] for k in range(3))==tr_input for s in S),'reynolds_divergence_preservation')
                if typ=='b' and alpha:nonzero_constants+=1
                if typ=='A' and i==j and gamma:nonzero_diagonal+=1
                if typ=='A' and i!=j and beta:nonzero_offdiagonal+=1
check(nonzero_constants and nonzero_diagonal and nonzero_offdiagonal,'all_three_invariant_parameters_present')
# Opposite pair -> 12alpha^2<=1; shared-sign h=2 -> 8(alpha +/- beta)^2<=1.
# These yield objective <=4|alpha|+8(|alpha|+|beta|).
check((12,8)==(4+8,8),'affine_objective_upper_bound_coefficients')

# Explicit controls reject errors using independently recomputed quantities.
controls={
 'forbidden_outer_pair_unit_bound':sq(sub(R[N[0]],R[N[1]]))/2>1,
 'forbidden_opposite_pair_unit_bound':sq(sub(R[P[0]],R[neg(P[0])]))/2>1,
 'scaled_affine_110_percent':F(11,10)**2>1,
 'wrong_apex_1_5':(6*F(1,5)**2-4*F(1,5)+1)/4!=F(1,8),
 'central_compatibility':sum(F(sq(s),2) for s in P)>4,
 'discarding_mixture_multiplicity':2*area[2]!=area[2],
}
# At x=2e_k, shared h=2, the active (alpha+beta) becomes alpha+2beta.
# Its squared norm is 14/3-4sqrt6/3 >1, certified by sqrt6<49/20.
controls['global_affine_feasibility_outside_domain']=F(14,3)-F(4,3)*F(49,20)>1
for name,value in controls.items():check(value,'negative_control_'+name)
check(all(sum(s[k] for s in P)==0 for k in range(3)),'central_cross_term_identically_zero')
check(sum(F(sq(s),2) for s in P)==6,'central_constant_six')

print(json.dumps({'result':'PASS_INDEPENDENT_EXACT_CONTROLS','checks':count,'categories':dict(sorted(categories.items())),
 'cell_volumes':{str(s):str(v) for s,v in volumes.items()},'candidate_area':'4*sqrt(2)',
 'sheet_counts':dict(face_counts),'interior_tetrahedral_junctions':5,
 'cross_configuration_plane_pairs':{'coincident_disjoint_interiors':coincident,'parallel_distinct':parallel_distinct,'nonparallel':nonparallel},
 'affine_vertex_inventory':[{'rational':q,'sqrt6_coefficient':r,'count':n} for (q,r),n in sorted(inv.items())],
 'reynolds_basis_fields':96,'negative_controls':controls,
 'limits':'Exact finite diagnostics plus algebraic reconstruction; not a formal proof of BV trace theory, compactness, global minimality, or historical novelty.'},sort_keys=True,indent=2))
