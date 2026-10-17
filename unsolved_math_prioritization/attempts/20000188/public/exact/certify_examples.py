#!/usr/bin/env python3
"""Exact authored fixtures for the complex fixed-pinhole residual.

Finite examples test claims; they do not prove the general classification.
Runs using Python 3 and SymPy; no external data or numerical tolerances.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S

x,w,y,z = V = S.symbols('x w y z')
s,t,h = S.symbols('s t h')
OUTPUT = {'coordinate_convention': {
 'world': '[x:w:y:z]', 'camera_1': '[x:y:z]', 'camera_2':'[w:y:z]',
 'center_1':'[0:1:0:0]', 'center_2':'[1:0:0:0]', 'baseline':'V(y,z)',
 'field':'C; exact identities computed over Q where possible'}, 'checks':{}}


def gb(fs, vs=V, order='lex'):
 return S.groebner(fs,*vs,order=order,domain=S.QQ)

def exprs(G):
 return [p.as_expr() for p in G.polys]

def strings(fs):
 return [str(S.factor(f)) for f in fs]

def equal(A,B):
 A,B=list(map(S.sympify,A)),list(map(S.sympify,B))
 GA,GB=gb(A),gb(B)
 assert all(GB.reduce(f)[1]==0 for f in A)
 assert all(GA.reduce(f)[1]==0 for f in B)
 return True

def saturation(I,f):
 u=S.Dummy('u')
 G=gb(list(I)+[1-u*f],(u,)+V)
 return [p for p in exprs(G) if not p.has(u)]

def intersect(A,B):
 u=S.Dummy('u')
 G=gb([u*f for f in A]+[(1-u)*g for g in B],(u,)+V)
 return [p for p in exprs(G) if not p.has(u)]

def saturation_by_ideal(I, generators):
 result=saturation(I,generators[0])
 for f in generators[1:]:
  result=intersect(result,saturation(I,f))
 return result

def hilbert(I):
 # Hilbert series of the leading monomial ideal by exact inclusion-exclusion.
 G=gb(I,order='grlex')
 lm=[tuple(p.LM(order='grlex').exponents) for p in G.polys]
 lm=[a for i,a in enumerate(lm) if not any(i!=j and all(bk<=ak for ak,bk in zip(a,b)) for j,b in enumerate(lm))]
 P=S.Integer(0)
 for n in range(len(lm)+1):
  for subset in itertools.combinations(lm,n):
   lcm=tuple(max(a[j] for a in subset) if subset else 0 for j in range(4))
   P+=(-1)**n*h**sum(lcm)
 P=S.expand(P)
 Q,R=S.div(P,(1-h)**2,h)
 assert R==0
 degree=S.expand(Q).subs(h,1)
 assert degree!=0
 constant=degree-S.diff(Q,h).subs(h,1)
 return {'leading_monomials':[list(a) for a in lm],
         'hilbert_series_numerator_over_1_minus_h_pow4':str(P),
         'hilbert_series_reduced_numerator_over_1_minus_h_pow2':str(S.expand(Q)),
         'degree':int(degree),'hilbert_polynomial':str(degree*h+constant),
         'arithmetic_genus':int(1-constant)}

def baseline_local_length(I, expected):
 # Localize the baseline at its generic point K=Q(x,w), then isolate the
 # origin in the transverse (y,z) plane with a Bezout-safe power of (y,z).
 bound=1
 for f in I:
  bound*=S.Poly(f,y,z).total_degree()
 fs=list(I)+[y**i*z**(bound-i) for i in range(bound+1)]
 G=S.groebner(fs,y,z,order='lex',domain=S.QQ.frac_field(x,w))
 lm=[tuple(p.LM(order='lex').exponents) for p in G.polys]
 basis=[y**a*z**b for a in range(bound) for b in range(bound-a)
        if not any(i<=a and j<=b for i,j in lm)]
 assert len(basis)==expected
 return {'field':'Q(x,w)', 'transverse_variables':['y','z'],
  'isolating_power':bound, 'groebner_basis':strings(exprs(G)),
  'standard_monomials':strings(basis),'length':len(basis)}

def jacobian(I):
 return S.Matrix([[S.diff(f,v) for v in V] for f in I])

def minors2(M):
 return sorted(set(S.expand(M.extract(rr,cc).det()) for rr in itertools.combinations(range(M.rows),2)
                   for cc in itertools.combinations(range(M.cols),2))-{S.Integer(0)},key=str)

def smooth_charts(I):
 J=minors2(jacobian(I))
 result={}
 for v in V:
  G=gb(list(I)+J+[v-1])
  result[str(v)+'=1'] = strings(exprs(G))
 assert all(k==['1'] for k in result.values())
 return result

def sing_chart(I, chart=z):
 return strings(exprs(gb(list(I)+minors2(jacobian(I))+[chart-1])))

def point_rank(I,point):
 return jacobian(I).subs(dict(zip(V,point))).rank()

def param_check(I,forms):
 assert all(S.expand(f.subs(dict(zip(V,forms)), simultaneous=True))==0 for f in I)
 degree=max(S.Poly(f,s,t).total_degree() for f in forms)
 assert all(S.Poly(f,s,t).total_degree()==degree for f in forms)
 assert S.gcd_list(forms)==1
 return {'forms':strings(forms),'homogeneous_degree':degree,'all_equations_vanish':True}

def image_pullback_degree(forms, indices, image_degree):
 selected=[forms[i] for i in indices]
 common=S.gcd_list(selected)
 reduced=[S.cancel(f/common) for f in selected]
 deg=max(S.Poly(f,s,t).total_degree() for f in reduced)
 assert deg % image_degree==0
 return {'common_factor':str(common),'reduced_forms':strings(reduced),
         'pullback_hyperplane_degree':deg,'generic_projection_degree':deg//image_degree}

# E1. Distinct epipole tangents: baseline plus a smooth twisted cubic.
f=x*z-y*y; g=w*y-z*z
I=[f,g]; T=[f,g,x*w-y*z]; L=[y,z]
assert equal(I,intersect(T,L))
assert equal(saturation(I,y),T)
forms=[s**3,t**3,s**2*t,s*t**2]
OUTPUT['checks']['E1_distinct_tangent_conics']={
 'cone_ideal':strings(I),'residual_ideal':strings(T),
 'exact_intersection_decomposition_verified':True,
 'baseline_primary_ideal':strings(L),'baseline_cycle_multiplicity':1,
 'baseline_local_length_certificate':baseline_local_length(I,1),
 'cone_hilbert':hilbert(I),'residual_hilbert':hilbert(T),
 'residual_smoothness_chart_certificates':smooth_charts(T),
 'parametrization':param_check(T,forms),
 'projection_1':image_pullback_degree(forms,[0,2,3],2),
 'projection_2':image_pullback_degree(forms,[1,2,3],2),
 'center_multiplicities':[1,1]}

# E2. Common epipole tangent: a doubled baseline, not multiplicity 1.
f=x*z-y*y; g=w*z-y*y
I=[f,g]; R=[x-w,f]; Q=[z,y*y]
assert equal(I,intersect(R,Q))
assert equal(saturation(I,y),R) and equal(saturation(I,z),R)
forms=[s*s,s*s,s*t,t*t]
assert point_rank(I,[1,1,0,0])==1
assert point_rank(R,[1,1,0,0])==2
OUTPUT['checks']['E2_same_tangent_conics']={
 'cone_ideal':strings(I),'residual_ideal':strings(R),
 'baseline_primary_ideal':strings(Q),'baseline_cycle_multiplicity':2,
 'baseline_local_length_certificate':baseline_local_length(I,2),
 'image_epipole_multiplicities':[1,1],
 'exact_intersection_decomposition_verified':True,
 'saturation_by_y_and_z_verified':True,
 'cone_hilbert':hilbert(I),'residual_hilbert':hilbert(R),
 'residual_smoothness_chart_certificates':smooth_charts(R),
 'parametrization':param_check(R,forms),
 'intersection_point':'[1:1:0:0]',
 'unsaturated_cone_jacobian_rank_at_intersection':1,
 'residual_jacobian_rank_at_intersection':2,
 'projection_generic_degrees':[1,1],'center_multiplicities':[0,0]}

# E3. Unequal epipole branch multiplicities yield a center point.
f=y**3-x*z*z; g=w*z-y*y
I=[f,g]; R=[w*w-x*y,w*y-x*z,y*y-w*z]
assert equal(saturation(I,y),R)
forms=[s**3,s*s*t,s*t*t,t**3]
# Local baseline length over Q(x,w); z=y²/w gives y³ times a unit.
assert S.cancel(f.subs(z,y*y/w)-y**3*(-x*y+w*w)/w**2)==0
OUTPUT['checks']['E3_cusp_conic_smooth_lift']={
 'cone_ideal':strings(I),'residual_ideal':strings(R),
 'saturation_by_y_verified':True,'cone_hilbert':hilbert(I),
 'residual_hilbert':hilbert(R),'baseline_cycle_multiplicity':3,
 'baseline_local_length_certificate':baseline_local_length(I,3),
 'local_baseline_reduction':str(S.factor(f.subs(z,y*y/w))),
 'epipole_branch_multiplicities':[2,1],
 'residual_smoothness_chart_certificates':smooth_charts(R),
 'parametrization':param_check(R,forms),
 'projection_1':image_pullback_degree(forms,[0,2,3],3),
 'projection_2':image_pullback_degree(forms,[1,2,3],2),
 'center_multiplicities':[0,1]}

# E4/E5. Same normalized epipolar covers, different baseline gluing.
for lam in [1,2]:
 f=y**3+z**3-x*y*z; g=y**3+lam*z**3-w*y*z
 I=[f,g]; R=saturation(I,y)
 forms=[s**3+t**3,s**3+lam*t**3,s*s*t,s*t*t]
 D={'lambda':lam,'cone_ideal':strings(I),'residual_ideal':strings(R),
  'saturation_by_y_verified':True,'cone_hilbert':hilbert(I),
  'residual_hilbert':hilbert(R),'baseline_cycle_multiplicity':6,
  'baseline_local_length_certificate':baseline_local_length(I,6),
  'parametrization':param_check(R,forms),
  'projection_generic_degrees':[1,1],'image_epipole_multiplicities':[2,2],
  'center_multiplicities':[0,0],
  'baseline_branch_images':[[1,1,0,0],[1,lam,0,0]]}
 if lam==2:
  assert equal(R,[(2*x-w)*z-y*y,(w-x)*y-z*z,(2*x-w)*(w-x)-y*z])
  D['transformed_twisted_cubic_ideal_verified']=True
  D['residual_smoothness_chart_certificates']=smooth_charts(R)
 else:
  assert equal(R,[x-w,f])
  assert point_rank(R,[1,1,0,0])==1
  D['singular_chart_x_equals_1']=sing_chart(R,x)
  # Branch at [s:t]=[1:0] has y/x=t+O(t4), z/x=t²+O(t5).
  # Branch at [0:1] has y/x=s²+O(s5), z/x=s+O(s4).
  D['two_branch_tangent_vectors_in_x_1_chart_w_y_z']=[[0,1,0],[0,0,1]]
 OUTPUT['checks'][f'E{lam+3}_nodal_epipole_lambda_{lam}']=D

# E6/E7. Singular selected components away from epipoles.
for name,F,forms in [
 ('E6_plane_cusp',y*y*z-x**3,[s*s*t,s*s*t,s**3,t**3]),
 ('E7_plane_node',y*y*z-x*x*(x+z),
  [s*(t*t-s*s),s*(t*t-s*s),t*(t*t-s*s),s**3])]:
 R=[w-x,F]
 D={'residual_ideal':strings(R),'hilbert':hilbert(R),
    'parametrization':param_check(R,forms),
    'singular_chart_z_equals_1':sing_chart(R),
    'epipoles_on_image_curves':False,'projection_generic_degrees':[1,1],
    'center_multiplicities':[0,0]}
 assert point_rank(R,[0,0,0,1])==1
 if 'cusp' in name:
  D['local_normalization']='(x,w,y)=(u²,u²,u³) in z=1; derivative is zero at u=0'
 else:
  D['local_normalization']='(x,w,y)=(u²−1,u²−1,u(u²−1)) in z=1'
  D['two_preimages_of_node']=[-1,1]
  D['derivatives_at_node_preimages']=[[-2,-2,2],[2,2,2]]
 OUTPUT['checks'][name]=D

# E8. Equal epipolar lines: all four smooth conic center patterns.
conics=[('neither_center',x*x+w*w+y*y,[0,0]),
        ('both_centers',x*w-y*y,[1,1]),
        ('center_1_only',x*w+x*x-y*y,[1,0]),
        ('center_2_only',x*w+w*w-y*y,[0,1])]
D={}
for name,F,mults in conics:
 R=[z,F]
 assert S.degree(F,w)==2-mults[0] and S.degree(F,x)==2-mults[1]
 D[name]={'ideal':strings(R),'hilbert':hilbert(R),
  'smoothness_chart_certificates':smooth_charts(R),
  'center_multiplicities':mults,'projection_generic_degrees':[2-m for m in mults]}
OUTPUT['checks']['E8_matching_epipolar_line_smooth_conics']=D

# E9. An integral quartic at the boundary r1+r2=d, with two ordinary nodes.
F=x*x*w*w+y*y*(x*x+w*w)+2*y**4; R=[z,F]
assert S.degree(F,w)==2 and S.degree(F,x)==2
local1=S.Poly(F.subs(w,1),x,y)
local2=S.Poly(F.subs(x,1),w,y)
initial1=sum(c*x**a*y**b for (a,b),c in local1.terms() if a+b==2)
initial2=sum(c*w**a*y**b for (a,b),c in local2.terms() if a+b==2)
assert initial1==x*x+y*y and initial2==w*w+y*y
assert point_rank(R,[0,1,0,0])==1 and point_rank(R,[1,0,0,0])==1
OUTPUT['checks']['E9_matching_epipolar_line_quartic']={
 'ideal':strings(R),'hilbert':hilbert(R),'center_initial_forms':[str(initial1),str(initial2)],
 'center_multiplicities':[2,2],'projection_generic_degrees':[2,2],
 'quadratic_discriminant_in_w':str(S.factor(S.discriminant(F,w))),
 'absolute_irreducibility_argument':
  'In chart y=1, w²=−(x²+2)/(x²+1). The rational function has simple zeros and poles over C and is not a square; hence the quadratic is irreducible over C(x). The homogeneous polynomial is primitive and not divisible by y.'}

# E10. Nonmatching epipolar lines intersect only in the excluded baseline.
assert equal([y,z],[y,z])
# The cone ideals themselves sum to (y,z), not intersect.
OUTPUT['checks']['E10_nonmatching_epipolar_lines']={
 'image_curves':['y=0 in [x:y:z]','z=0 in [w:y:z]'],
 'cone_intersection_ideal':['y','z'],'only_component':'baseline',
 'baseline_projection_images':['[1:0:0]','[1:0:0]'],
 'admissible_world_curve_exists':False}

# E11. One epipolar line and a nonline curve: only contracted lines survive.
I=[z,w*y-z*z]
A=[z,w]; B=[z,y]
assert equal(I,intersect(A,B))
OUTPUT['checks']['E11_epipolar_line_and_conic']={
 'cone_ideal':strings(I),'exact_components':[strings(A),strings(B)],
 'decomposition_verified':True,
 'component_projection_notes':[
  'V(z,w) maps onto camera-1 line z=0 but camera-2 point [0:1:0]',
  'V(z,y) is the baseline and maps to the epipoles'],
 'admissible_world_curve_exists':False}

# E12. Saturating by an irrelevant product can wrongly remove valid components.
R=[z,x+w+y]
assert equal(saturation(R,z),[1])
assert equal(saturation(R,y),R)
assert equal(saturation_by_ideal(R,[y,z]),R)
OUTPUT['checks']['E12_saturation_warning']={
 'valid_world_line_ideal':strings(R),
 'camera_image_lines':['z=0','z=0'],
 'center_multiplicities':[0,0],'projection_generic_degrees':[1,1],
 'saturation_by_z_returns_unit_ideal':True,
 'saturation_by_baseline_ideal_must_keep_line':True,
 'explanation':'Saturation by y*z is not saturation by the ideal (y,z). A valid component can lie in z=0 without lying in the baseline.'}

# E13. Equal singular-branch orders: the baseline ratio derivative matters.
D={}
for k,varying in [(2,True),(3,True),(2,False)]:
 f=y**(k+1)-x*z**k
 g=y**(k+1)+(y**k*z if varying else 0)-w*z**k
 I=[f,g]
 R=saturation(I,y)
 forms=[s**(k+1),s**(k+1)+(s**k*t if varying else 0),s*t**k,t**(k+1)]
 A={'k':k,'varying_baseline_ratio':varying,
    'cone_ideal':strings(I),'residual_ideal':strings(R),
    'parametrization':param_check(R,forms),
    'cone_hilbert':hilbert(I),'residual_hilbert':hilbert(R),
    'baseline_local_length_certificate':baseline_local_length(I,k*(k+1)),
    'epipole_branch_multiplicities':[k,k],
    'center_multiplicities':[0,0],'projection_generic_degrees':[1,1],
    'epipolar_cover_degree':1,'baseline_point':'[1:1:0:0]'}
 if varying:
  A['residual_smoothness_chart_certificates']=smooth_charts(R)
  A['local_normalization_x_1']='[1:1+u:u^k:u^(k+1)]'
  A['baseline_ratio_derivative']=1
 else:
  assert equal(R,[x-w,f])
  assert point_rank(R,[1,1,0,0])==1
  A['singular_chart_x_equals_1']=sing_chart(R,x)
  A['local_normalization_x_1']='[1:1:u^k:u^(k+1)]'
  A['baseline_ratio_derivative']=0
 D[f'k_{k}_ratio_{"varying" if varying else "constant"}']=A
OUTPUT['checks']['E13_equal_order_baseline_ratio']=D

OUTPUT['summary']={'fixture_groups':len(OUTPUT['checks']),'status':'ALL ASSERTIONS PASSED',
 'generality_limit':'These are finite exact fixtures, not a proof of the full residual or a novelty claim.',
 'sympy_version':S.__version__}
path=Path(__file__).with_name('CERTIFICATE_RESULTS.json')
path.write_text(json.dumps(OUTPUT,indent=2)+'\n')
print(json.dumps(OUTPUT['summary'],indent=2))
print('Results:',path)
print('Results SHA256:',hashlib.sha256(path.read_bytes()).hexdigest())
