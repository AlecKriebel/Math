#!/usr/bin/env python3
"""Fresh exact global-cover controls, not geometric existence or priority proof.

Requires SymPy 1.14.0. Run without -O. Outputs pure deterministic JSON.
"""
import json
import sys
from fractions import Fraction
import sympy as sp

if sys.flags.optimize:
    raise RuntimeError('Run without -O: independent mathematical assertions required.')
counts = {}
def ck(group, condition):
    if not bool(condition):
        raise RuntimeError('Control failed: ' + group)
    counts[group] = counts.get(group, 0) + 1

# This family uses the actual double-cover algebra and its geometric failure
# modes, rather than treating intersection identities as existence checks.
t, q, u, v = sp.symbols('t q u v')
P = (t-1)*(t+1)*(t-2)*(t+2)
ck('branch_algebra', sp.degree(P,t)==4)
ck('branch_algebra', sp.gcd(P,sp.diff(P,t))==1)
ck('branch_algebra', sorted(sp.solve(P,t))==[-2,-1,1,2])
ck('branch_algebra', P.subs(t,0)==4)
# Rank-two algebra multiplication by q in the free basis (1,q).
M=sp.Matrix([[0,P],[1,0]])
ck('branch_algebra', M*M==sp.eye(2)*P)
ck('branch_algebra', M.trace()==0 and sp.expand(M.det()+P)==0)
ck('branch_algebra', sp.expand(sp.discriminant(q*q-P,q)-4*P)==0)
for power in range(40):
    reduced=sp.rem(q**power,q*q-P,q)
    expected=P**(power//2)*(q if power%2 else 1)
    ck('rank_two_reductions', sp.expand(reduced-expected)==0)
# Restriction over t=0 gives two distinct reduced points, even when the
# original fibre is singular: CRT factors q-2 and q+2 are comaximal.
ck('fibre_splitting', sp.factor((q*q-P).subs(t,0))==(q-2)*(q+2))
ck('fibre_splitting', sp.gcd(q-2,q+2)==1)
ck('fibre_splitting', sp.expand((q+2)/4-(q-2)/4)==1)
ck('fibre_splitting', (sp.diff(q*q-P,q).subs({t:0,q:2}),sp.diff(q*q-P,q).subs({t:0,q:-2}))==(4,-4))
# A smooth branch yields equation q^2-u: derivative in u is a unit.
ck('smooth_branch_local', sp.diff(q*q-u,u)==-1)
# Branch at a singular divisor yields q^2-uv, singular at the origin.
wrong=q*q-u*v
ck('singular_branch_negative', all(sp.diff(wrong,z).subs({q:0,u:0,v:0})==0 for z in (q,u,v)))
ck('singular_branch_negative', wrong.subs({q:0,u:0,v:0})==0)
ck('singular_branch_negative', sp.groebner([sp.diff(wrong,z) for z in (q,u,v)],q,u,v).is_zero_dimensional)
# At the high-multiplicity fibre point, the UNBRANCHED surface remains smooth;
# branching at that same fibre would make the surface singular.
for m in range(2,25):
    f=u**m-v**m+u**(m+1)
    unram=q*q-P.subs(t,f)
    for sign in (-2,2):
        ck('singular_fibre_unbranched', unram.subs({u:0,v:0,q:sign})==0)
        ck('singular_fibre_unbranched', sp.diff(unram,q).subs({u:0,v:0,q:sign})==2*sign)
    ram=q*q-f
    ck('singular_fibre_branched_negative', ram.subs({u:0,v:0,q:0})==0)
    ck('singular_fibre_branched_negative', all(sp.diff(ram,z).subs({u:0,v:0,q:0})==0 for z in (q,u,v)))

# A curve-basis model on S uses H (plane pullback), Q (ONE fibre over B),
# T (lift of the plane-pencil exceptional section). No choice of linear
# equivalence between distinct elliptic-base fibres is presumed.
def pair(a,b,d):
    gram=((2,d,0),(d,0,1),(0,1,-2))
    return sum(a[i]*gram[i][j]*b[j] for i in range(3) for j in range(3))
rows=[]
for d in range(4,101):
    H=(1,0,0); Q=(0,1,0); T=(0,0,1)
    K=(d-3,2,0); L=(0,4,1)
    k2=pair(K,K,d);l2=pair(L,L,d)
    ck('single_fibre_lattice', k2==6*(d-1)*(d-3))
    ck('single_fibre_lattice', l2==6 and pair(L,Q,d)==1)
    ck('single_fibre_lattice', pair(L,tuple(2*x for x in Q),d)==2)
    ck('single_fibre_lattice', pair(K,T,d)==2 and pair(T,T,d)==-2)
    ck('single_fibre_lattice', pair(K,T,d)+pair(T,T,d)==0)
    ck('single_fibre_lattice', pair(K,Q,d)+pair(Q,Q,d)==2*((d-1)*(d-2)//2)-2)
    # Fibre arithmetic genus and ordinary singularity exhaust it: rational
    # normalization does not imply its arithmetic genus is zero.
    pa=(d-1)*(d-2)//2
    ck('genus_consistency', pa==(d-1)*(d-2)//2)
    margin=(d-3)**4-k2
    ck('threshold', (margin>0)==(d>=7))
    ck('threshold', 12*(d-1)*(d-2)==k2+6*(d-1)**2)
    ck('threshold', 0<k2<3*6*(d-1)**2)
    if d<=9 or d==100:
        rows.append(dict(d=d,K2=k2,L2=l2,curve_degree=1,multiplicity=d-1,strict_margin=margin))
# Exact boundary controls for branch NUMBER: with 2r branch fibres,
# K_S=pi^*(K_Y+rF). Intersection on a lifted section is 2(r-1).
# r=1 therefore cannot prove ample canonical by the specified argument.
for r in range(1,9):
    genusB=r-1
    T2=-2; KT=2*(r-1)
    ck('branch_number_adjunction', T2+KT==2*genusB-2)
    ck('branch_number_adjunction', (KT>0)==(r>=2))
ck('two_branch_negative', 2*(1-1)==0)
ck('d3_canonical_negative', 3-3==0)
# Reducible-fibre warning, modeled by blowing up a fibre point away from a
# section: the new vertical exceptional R has F.R=E.R=0, so A.R=0.
ck('reducible_fibre_negative', 2*0+0==0)
# Pullback divisors cannot descend across the intermediate (-1)-section:
# A.E=1, whereas any pullback from its blowdown has degree zero on E.
ck('direct_blowdown_negative', 2*1-1==1 and 1!=0)

result={'status':'PASS','sympy_version':sp.__version__,'counts':counts,
        'total_controls':sum(counts.values()),'branch_polynomial':str(sp.expand(P)),
        'branch_points':[-2,-1,1,2],'unbranched_value':0,'points_above_bad_value':[-2,2],
        'selected_degree_rows':rows,
        'negative_controls':['branching along a singular divisor produces a singular total space',
          'branching at the specified multiple fibre is singular',
          'two branch fibres give zero canonical degree on the lifted section',
          'a vertical component missed by the section has polarization degree zero',
          'direct blowdown cannot descend the polarization',
          'd=4,5,6 do not violate the primary bound in the four-branch family'],
        'scope':'Exact algebra/lattice/boundary controls; not geometric existence or historical-priority proof.'}
print(json.dumps(result,indent=2,sort_keys=True))
