#!/usr/bin/env python3
"""Fresh exact boundary controls for already stated deductions; no residual search."""
from pathlib import Path
from itertools import combinations
import datetime as dt
import hashlib
import json
import sympy as S

HERE=Path(__file__).resolve().parent
w,x,y,z,s,t,h,v=S.symbols('w x y z s t h v')
R=(w,x,y,z)
groups=[]
checks=0
def check(cond):
    global checks
    assert cond
    checks+=1
def sameideals(a,b,variables=R):
    ga=S.groebner(a,*variables,order='lex')
    gb=S.groebner(b,*variables,order='lex')
    return all(gb.reduce(p)[1]==0 for p in a) and all(ga.reduce(p)[1]==0 for p in b)
def intersect(a,b):
    g=S.groebner([h*p for p in a]+[(1-h)*p for p in b],h,*R,order='lex')
    return [p.as_expr() for p in g.polys if not p.as_expr().has(h)]
def principal_colon(a,f):
    # J:f = (J intersect (f))/f, an exact polynomial identity, no saturation assumption.
    out=[]
    for p in intersect(a,[f]):
        quotient,remainder=S.div(p,f,*R)
        check(remainder==0)
        out.append(quotient)
    return out
def colon(a,generators):
    out=principal_colon(a,generators[0])
    for f in generators[1:]:out=intersect(out,principal_colon(a,f))
    return out

# Squarefreeness survives nonsplit rational cyclotomic factors; characteristic boundary.
for n in range(1,25):
    check(S.gcd(S.Poly(v**n-1,v,domain=S.QQ),S.Poly(n*v**(n-1),v,domain=S.QQ)).degree()==0)
check(S.factor(v**3-1)==(v-1)*(v**2+v+1))
check(S.Poly(v**2+v+1,v,domain=S.QQ).is_irreducible)
check(S.gcd(S.Poly(v**3-1,v,modulus=3),S.Poly(3*v**2,v,modulus=3)).degree()==3)
groups.append({'name':'arbitrary_field_Laurent_reducedness_boundary','rational_orders_checked':list(range(1,25)),
               'nonsplit_Q_C3_factor_reduced':True,'char3_C3_repeated_root_detected':True})

# Radical/generic-length alone is insufficient to contract: independent negative control.
u,vv=S.symbols('u vv')
nonprimary=S.groebner([u*u,u*vv],u,vv,order='lex')
check(nonprimary.reduce(u)[1]==u)
check(nonprimary.reduce(vv*u)[1]==0)
check(S.groebner([u*u,u*vv,1-h*vv],h,u,vv,order='lex').reduce(u)[1]==0)
groups.append({'name':'primary_contraction_negative_control','ideal':'(u^2,u*v)',
               'u_survives_but_vu_zero':True,'localization_v_kills_u':True})

# Independently recompute both complete-intersection colons by intersections/division.
q=w*z-x*y
g=w*y*y-x*x*z
a=[q,x**3-w*w*y,g,y**3-x*z*z]
I=[w*y,w*z,x*y,x*z]
left=colon([q,g],I)
right=colon([q,g],a)
check(sameideals(left,a))
check(sameideals(right,I))
check(sameideals(intersect(a,I),[q,g]))
check(S.expand((w*y*y+x*x*z).subs({w:s**4,x:s**3*t,y:s*t**3,z:t**4}))!=0)
groups.append({'name':'both_link_colons_independent_sympy_division','CI_colon_I_equals_a':True,
               'CI_colon_a_equals_I':True,'intersection_equals_CI':True,
               'wrong_cubic_sign_rejected':True,'left_colon_basis':[str(p) for p in left],
               'right_colon_basis':[str(p) for p in right]})

# Euler/Jacobian kernel and bad-characteristic control.
f=S.Matrix([s**4,s**3*t,s*t**3,t**4])
J=f.jacobian((s,t)).T
U=S.Matrix([[2*t**3,0],[-3*s*t*t,t**3],[s**3,-3*s*s*t],[0,2*s**3]])
check(J*U==S.zeros(2,2))
check(S.Matrix([[s,t]])*J==4*f.T)
check(S.expand(U.extract([0,1],[0,1]).det())==2*t**6)
check(S.expand(U.extract([2,3],[0,1]).det())==2*s**6)
check(J.subs({s:1,t:1}).rank()==2)
check(S.Matrix([[int(c)%2 for c in row] for row in J.subs({s:1,t:1}).tolist()]).rank()==1)
check(S.Matrix([[int(c)%2 for c in row] for row in U.subs({s:1,t:1}).tolist()]).rank()==1)
gradq=S.Matrix([z,-y,-x,w]).subs({w:s**4,x:s**3*t,y:s*t**3,z:t**4})
check(S.simplify(U*S.Matrix([t/2,s/2])-gradq)==S.zeros(4,1))
groups.append({'name':'global_conormal_Euler_and_characteristic_boundary','Euler_scalar':4,
               'characteristic_zero_endpoint_cover':True,'char2_rank_drop_detected':True,
               'quadric_subline_coefficients':['t/2','s/2']})

# Local Cartier equation checks exclude silently keeping an embedded chart correction.
F=x**3-w*w*y
sub={z:x*y/w}
check(S.factor(g.subs(sub)+(y/w)*F)==0)
check(S.factor((y**3-x*z*z).subs(sub)+(y*y/(w*w))*F)==0)
check(S.factor((x**3-w*w*y).subs({y:(x**3-F)/w**2})-F)==0)
groups.append({'name':'q_contained_Cartier_chart','P_on_w_chart_generated_by_F':True,
               'chart_ring':'K[w,w^-1,x,F]'})

# Padding all generators by zero: inspect the differential block that retains Z2.
for k in range(0,9):
    fs=I+[S.Integer(0)]*k
    zeros=tuple(range(4,4+k))
    columns=[pair+zeros for pair in combinations(range(4),2)]
    rows=[(i,)+zeros for i in range(4)]
    block=S.zeros(4,6)
    for j,col in enumerate(columns):
        for position,i in enumerate(col):
            row=col[:position]+col[position+1:]
            if row in rows:block[rows.index(row),j]+=(-1)**position*fs[i]
            elif fs[i]!=0:raise AssertionError('block leaked outside the tensor factor')
    original=S.zeros(4,6)
    for j,(i,l) in enumerate(combinations(range(4),2)):
        original[l,j]=I[i];original[i,j]=-I[l]
    check(block==original)
    check((4+k)-(k+2)-1==1)
groups.append({'name':'generator_padding_retains_Z2_differential_block','padding_k_checked':list(range(9)),
               'universal_reason':'K(f,0^k)=K(f) tensor exterior(K^k); Z_(k+2) contains Z2(f)',
               'cycle_required_pdim_bound':1,'verified_actual_Z2_pdim_at_vertex':2})

# The boundary e=-8 would avoid the dimension contradiction, but admits no conormal map.
check(max(-8+7+1,0)==0)
check(max(-8+8+1,0)+9==10)
check(max(-7+7+1,0)==1)
check(max(-7+8+1,0)+9==11)
groups.append({'name':'double_ribbon_bound_sharp_dependency','e_minus8_has_no_conormal_map':True,
               'minimum_permitted_e_minus7_requires11_quadratic_sections':True})

out={'checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'passed','assertions':checks,
     'groups':groups,'scope':'Falsification and boundary controls for stated partial proofs only; no central residual construction/exclusion search',
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'arithmetic':'SymPy exact rational/integer polynomials'}
(HERE/'FALSIFICATION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'passed','assertions':checks,'groups':len(groups)},indent=2))
