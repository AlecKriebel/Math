"""Independent exact controls, authored before reading submitted helper code.

These computations corroborate the geometric proof. They do not certify Bertini,
Nakai--Moishezon, or the existence of the chosen generic pencil by enumeration.
"""
from pathlib import Path
from fractions import Fraction
import json
import sympy as s

OUT = Path(__file__).parent
d, a, q = s.symbols('d a q', integer=True)
X, Y, Z, x, y, t, w, v = s.symbols('X Y Z x y t w v')

def N(e):
    return e*(e+3)/2

assert s.expand(N(d)-N(a)-N(d-a)) == a*d-a*a
# Minimum codimension: a(d-a)-(d-1)=(a-1)(d-a-1)>=0.
assert s.expand(a*(d-a)-(d-1)-(a-1)*(d-a-1)) == 0

# Coefficient-vector intersection pairing on the blowup of d^2 simple points.
def dot(v1, v2):
    return v1[0]*v2[0]-sum(u*v for u,v in zip(v1[1:],v2[1:]))

lattice_rows=[]
for deg in range(3, 31):
    n=deg*deg
    H=[1]+[0]*n
    E1=[0,1]+[0]*(n-1)
    F=[deg]+[-1]*n
    K=[-3]+[1]*n
    A=[2*u+v for u,v in zip(F,E1)]
    Kplus=[u+2*v for u,v in zip(K,F)]
    assert dot(F,F)==0 and dot(F,E1)==1 and dot(E1,E1)==-1
    assert dot(A,A)==3 and dot(A,F)==dot(A,E1)==1
    assert dot(Kplus,Kplus)==3*(deg-1)*(deg-3)
    assert dot(Kplus,E1)==1
    assert dot(Kplus,F)==deg*(deg-3)
    assert dot(K,F)==deg*(deg-3)
    # Genus of the degree-d plane fibre, unchanged by simple smooth basepoint blowups.
    genus=Fraction((deg-1)*(deg-2),2)
    assert 2*genus-2 == dot(K,F)+dot(F,F)
    # Degree-two cover doubles pairings of pullbacks, but one split fibre maps with degree1.
    assert 2*dot(A,A)==6
    quotient=Fraction(dot(A,F),deg-1)
    delta=(deg-3)**3-6*(deg-1)
    lattice_rows.append({'d':deg,'base_points':n,'A2':dot(A,A),'N2':dot(Kplus,Kplus),'KS2':2*dot(Kplus,Kplus),'L2':6,'L_dot_split_C':dot(A,F),'curve_multiplicity':deg-1,'seshadri_upper_bound':str(quotient),'strict_comparison_polynomial':delta,'violates_via_this_curve':deg>=4 and delta>0})

# Symbolic formulas using the diagonal lattice directly, separately from fibre identities.
assert s.expand((2*d)**2-(1+4*(d*d-1)))==3
assert s.expand((2*d-3)**2-d*d-3*(d-3)*(d-1))==0
P=(d-3)**3-6*(d-1)
assert s.expand(P.subs(d,d+1)-P-(3*(d-3)**2+3*(d-3)-5))==0
# Translation d=q+7 gives an all-nonnegative-coefficient positivity proof for every q>=0.
assert s.expand(P.subs(d,q+7))==q**3+12*q**2+42*q+28
assert s.expand(((d-3)**4-6*(d-1)*(d-3))-(d-3)*P)==0

singularity_rows=[]
for deg in range(3, 16):
    f=Z*(X**(deg-1)-Y**(deg-1))+X**deg
    assert s.gcd(X**(deg-1)-Y**(deg-1),X**deg)==1
    affine=f.subs({X:x,Y:y,Z:1})
    terms=s.Poly(affine,x,y).terms()
    mult=min(sum(exp) for exp,c in terms if c)
    assert mult==deg-1
    tangent=s.expand(sum(c*x**exp[0]*y**exp[1] for exp,c in terms if sum(exp)==mult))
    assert tangent==x**(deg-1)-y**(deg-1)
    assert s.gcd(t**(deg-1)-1,s.diff(t**(deg-1)-1,t))==1
    # Finite chart singular set: any additional singular point would make this
    # ideal non-unit after imposing x !=0; f_y forces y=0, f_z then x=0.
    assert s.diff(f,Y)==-(deg-1)*Z*Y**(deg-2)
    assert s.diff(f,Z)==X**(deg-1)-Y**(deg-1)
    # Only point on Z=0 is [0:1:0], whose f_Z is -1.
    assert s.diff(f,Z).subs({X:0,Y:1,Z:0})==-1
    # A rational parametrization independently corroborates the ordinary singular curve.
    sub={X:(1-t**(deg-1)),Y:t*(1-t**(deg-1)),Z:-1}
    assert s.expand(f.subs(sub,simultaneous=True))==0
    # At an unramified cover point even a singular fibre causes no singularity
    # of the total covering surface: w^2=1+f has nonzero w derivative at p,w=1.
    cover=w*w-(1+affine)
    assert s.diff(cover,w).subs({x:0,y:0,w:1})==2
    # At a smooth branch fibre choose local parameter t; w^2-t has derivative -1.
    assert s.diff(w*w-t,t)==-1
    singularity_rows.append({'d':deg,'primitive_linear_in_Z':True,'multiplicity':mult,'tangent_cone_squarefree':True,'point_at_infinity_smooth':True,'parametrization_identity':True,'unbranched_total_space_jacobian':2})

# Formal double-cover base curve: four simple branch points and unbranched t=0.
Q=(t-1)*(t-2)*(t-3)*(t-4)
assert s.gcd(Q,s.diff(Q,t))==1 and Q.subs(t,0)==24
out={'status':'PASS','scope':'exact algebraic controls only; analytic proof remains essential','sympy_version':s.__version__,'lattice_rows':lattice_rows,'singularity_rows':singularity_rows,'symbolic_identities':{'reducible_codimension':'a(d-a)','codimension_lower_bound_difference':'(a-1)(d-a-1)','join_complement_codimension_at_least':'d-2','all_d_comparison_after_d_eq_q_plus_7':'q^3+12q^2+42q+28','canonical_square':'6(d-1)(d-3)'},'local_cover_controls':{'branch_equation':'w^2-t','branch_partial_t':-1,'unbranched_equation':'w^2-(1+f_d(x,y,1))','unbranched_partial_w_at_0_0_1':2,'quartic_branch_sample':'(t-1)(t-2)(t-3)(t-4)','squarefree':True,'unbranched_value_zero':24},'negative_controls':{'d4_comparison':-17,'d5_comparison':-16,'d6_comparison':-3,'d7_comparison':28,'degree_two_whole_preimage_not_used_as_single_test_curve':True}}
(OUT/'fresh_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'lattice_degrees':[3,30],'singularity_degrees':[3,15],'symbolic_all_d_comparison':out['symbolic_identities']['all_d_comparison_after_d_eq_q_plus_7']}))
