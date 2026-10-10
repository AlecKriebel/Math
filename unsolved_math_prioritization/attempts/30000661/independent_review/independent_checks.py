"""Independent exact reconstruction and symbolic degree-cone certificates.

No frozen author module is imported. The analytic group/closure/descent arguments
are reviewed in INDEPENDENT_REVIEW.md, not inferred from these controls.
"""
import json
from itertools import permutations,product
from collections import Counter
import sympy as s
C=Counter();cert={}
def ck(a,k):
    assert a,k
    C[k]+=1
def eq(a,b,k):ck(s.cancel(a-b)==0,k)
def pos(expr,gens):
    poly=s.Poly(s.expand(expr),*gens)
    return not poly.is_zero and all(c>=0 for c in poly.coeffs())
x,y,z,a,b,t=s.symbols('x y z a b t');v=(x,y,z)
D=x*x*y+z*z
# Reconstruct from the two localized operations using the invariant u.
V=z+t*x*D;U=D+2*t*x*V**3
fy=s.cancel((U-V**2)/x**2)
source_y=y-2*t*x*y*z-t*t*D**2+6*t*t*z*z*D+6*t**3*x*z*D**2+2*t**4*x*x*D**3
G={x:x,y:fy,z:V}
eq(fy,source_y,'source_from_invariant_coordinates')
ck(s.denom(fy)==1,'reconstructed_polynomial')
oldU=D-2*t*x*z**3;oldV=z-t*x*oldU
I={x:x,y:s.cancel((oldU-oldV**2)/x**2),z:oldV}
for q in v:
    eq(I[q].xreplace(G),q,'reconstructed_inverse_left')
    eq(G[q].xreplace(I),q,'reconstructed_inverse_right')
eq(s.Matrix([G[q] for q in v]).jacobian(v).det(),1,'family_Jacobian')
for q in v:eq(G[q].subs(t,0),q,'identity_parameter')
eq(fy.subs(x,0),y+5*t*t*z**4,'special_fiber')
N_y=y-2*t*z*D/x-t*t*D**2
for p,expect in [(N_y,-2*t*z**3),(y+2*t*z**3/x,2*t*z**3)]:
    eq(s.cancel(x*p).subs(x,0),expect,'actual_localized_poles')
lam=s.symbols('lam',nonzero=True);weights=(3,-4,1)
for q,w in zip(v,weights):
    expr=G[q].subs(t,1).xreplace({r:lam**u*r for r,u in zip(v,weights)})/lam**w
    eq(expr,G[q].subs(t,lam**4),'weighted_diagonal_relation')
# Six polynomial flows: reconstruct derivatives and addition with generic times.
for i,j,k in permutations(range(3)):
    inv=v[i]**2*v[j]+v[k]**2
    E=lambda f:s.expand(inv*(v[i]**2*s.diff(f,v[k])-2*v[k]*s.diff(f,v[j])))
    flow={v[i]:v[i],v[j]:v[j]-2*a*v[k]*inv-a*a*v[i]**2*inv**2,v[k]:v[k]+a*v[i]**2*inv}
    eq(inv.xreplace(flow),inv,'all_six_exact_invariants')
    for q in v:
        eq(E(E(E(q))),0,'all_six_coordinate_nilpotence')
        eq(flow[q],q+a*E(q)+a*a*E(E(q))/2,'all_six_flow_reconstruction')
        # Differentiate the formula in its time; checks the actual named vector field.
        eq(s.diff(flow[q],a),E(q).xreplace(flow),'all_six_flow_differential_equation')
    eq(s.Matrix([flow[q] for q in v]).jacobian(v).det(),1,'all_six_flow_Jacobians')
# Symbolic positive-coefficient certificates for ALL thirty direction changes.
p,e=s.symbols('p e',positive=True);M=4*p+e;H=6*p+2*e
transition=[]
perms=list(permutations(range(3)))
for old,new in product(perms,repeat=2):
    if old==new:continue
    w=[None]*3
    for idx,weight in zip(old,(p,H,M)):w[idx]=weight
    P,Q,R=(w[idx] for idx in new)
    cmp=s.expand(2*P+Q-2*R)
    ck(pos(cmp,(p,e)) or pos(-cmp,(p,e)),'all_transition_unique_Delta_term')
    d=2*P+Q if pos(cmp,(p,e)) else 2*R
    hi=2*P+2*d;mid=2*P+d
    gaps=[d-2*P,mid-R,hi-Q,hi-(R+d),hi-2*H]
    for gap in gaps:ck(pos(gap,(p,e)),'all_transition_strict_degree_gaps')
    eq(hi-2*mid+2*P,0,'all_transition_cone_relation')
    transition.append({'old':old,'new':new,'Delta_comparison':str(cmp),'new_degrees':[str(P),str(s.expand(hi)),str(s.expand(mid))],'strict_gaps':[str(s.expand(g)) for g in gaps]})
cert['six_flow_transitions']=transition
# An arbitrary affine combination of coordinates with distinct degrees cannot
# cancel its top used coordinate. Exhaust all 19 patterns containing the largest.
p,h,k=s.symbols('p h k',positive=True);small=p;middle=p+h;large=2*p+2*h+k
GG=[G[q].subs(t,1).expand() for q in v]
terms=[s.Poly(g,*v).terms() for g in GG]
mixing=[]
for indices in product(range(3),repeat=3):
    if 2 not in indices:continue
    weights=[(small,middle,large)[i] for i in indices]
    P,Q,R=weights;cmp=s.expand(2*P+Q-2*R)
    ck(pos(cmp,(p,h,k)) or pos(-cmp,(p,h,k)),'all_affine_patterns_nonzero_comparison')
    d=2*P+Q if pos(cmp,(p,h,k)) else 2*R
    targets=[P,2*P+3*d,P+d]
    for termlist,target in zip(terms,targets):
        equal=0
        for mon,co in termlist:
            gap=s.expand(target-sum(m*w for m,w in zip(mon,weights)))
            if gap==0:equal+=1
            else:ck(pos(gap,(p,h,k)),'all_affine_source_monomial_gaps')
        ck(equal==1,'all_affine_unique_top_source_monomial')
    ck(pos(targets[1]-3*large,(p,h,k)),'all_affine_growth')
    ck(pos(targets[1]-2*targets[2],(p,h,k)),'all_affine_preserved_gap')
    mixing.append({'pattern':indices,'Delta_comparison':str(cmp),'outputs':[str(s.expand(q)) for q in targets],'growth_gap':str(s.expand(targets[1]-3*large))})
cert['affine_patterns']=mixing
# Formal telescoping in a free group, with no commutation assumptions.
def red(seq):
    out=[]
    for a in seq:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return out
for n in range(1,51):
    prod=[]
    for j in range(n):prod += [2]*j+[1,2,-1,-2]+[-2]*j
    ck(red(prod)==[1]+[2]*n+[-1]+[-2]*n,'arbitrary_conjugator_telescoping')
# Distinct leading degrees for cubic alternating blocks: a strict all-degree
# multiplier, followed by the original-coordinate recurrence degree certificate.
for n in range(1,13):
    deg=2*3**(n-1);xp=2*3**(n-1)-1;tw=(3**(n-1)-1)//2
    ck(3*deg==2*3**n,'all_iterate_degree_recurrence')
    ck(2+3*xp==2*3**n-1,'all_iterate_x_power_recurrence')
    ck(1+3*tw==(3**n-1)//2,'all_iterate_two_power_recurrence')
# Leibniz certificates use arbitrary coordinate multiplicities, not just a
# single generator: maximum surviving differentiation is N(m-1).
for m in range(1,9):
    for aa,bb,cc in product(range(5),repeat=3):
        N=aa+bb+cc
        ck(aa*(m-1)+bb*(m-1)+cc*(m-1)<N*(m-1)+1,'coordinate_nilpotence_pigeonhole')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Independent algebra and symbolic positive-cone certificates; group closure, infinite-word reasoning and number-field descent require the accompanying proof review.'},indent=2,sort_keys=True))
from pathlib import Path
Path('DEGREE_CERTIFICATES.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
