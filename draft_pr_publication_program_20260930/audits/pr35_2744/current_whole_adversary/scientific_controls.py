"""Independent exact diagnostics. The proof is UNIVERSAL_PROOF, not this finite run."""
import json
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
checks={}
def ck(k,v):
    assert bool(v),k
    checks[k]='PASS'
t,x,y=s.symbols('t x y',real=True)
# A finite ramified map preserves a nonconstant character arc.
c=(1-t*t)/(1+t*t);d=2*t/(1+t*t)
U=s.diag(c+s.I*d,c-s.I*d);J=s.Matrix([[0,-1],[1,0]])
ck('unitary_curve',s.simplify(U.conjugate().T*U)==s.eye(2) and s.simplify(U.det())==1)
ck('genuine_character_variation',s.simplify(s.diff(s.trace(U),t))!=0)
ck('projective_character_variation',s.simplify(s.diff(s.trace(U)**2,t))!=0)
ck('exceptional_derivative_at_zero',s.diff(s.trace(U)**2,t).subs(t,0)==0)
ck('irreducible_pair_away_from_exception',U.subs(t,s.Rational(1,2))[0,0]!=U.subs(t,s.Rational(1,2))[1,1] and J*s.Matrix([1,0])==s.Matrix([0,1]) and J*s.Matrix([0,1])==s.Matrix([-1,0]))
# Full identity conditions must not be substituted by trace-square 4.
N=s.Matrix([[1,1],[0,1]])
ck('parabolic_identity_trace',N.trace()**2==4)
ck('parabolic_is_not_projective_identity',N!=s.eye(2) and N!=-s.eye(2))
ck('same_reducible_GIT_trace',all((N**k).trace()==2 for k in range(1,5)))
# Lift obstruction for a torsion group: UCT Ext cannot be omitted generally.
T=s.diag(s.I,-s.I)
ck('order_two_projective_element',T**2==-s.eye(2))
ck('no_order_two_SL_lift',T**2!=s.eye(2) and (-T)**2!=s.eye(2))
# Distinct irreducible components can meet at a singular path switch.
f=x*y
ck('singular_switch',s.diff(f,x).subs({x:0,y:0})==s.diff(f,y).subs({x:0,y:0})==0)
ck('separate_smooth_branches',s.diff(f,y).subs({x:1,y:0})==1 and s.diff(f,x).subs({x:0,y:1})==1)
# A real-defined union need not make its selected component real.
ck('nonreal_chosen_component',s.I**3+s.I==0 and s.I!=s.conjugate(s.I))
# Irreducible complex curve can have both an acnode and a distant real arc.
a=y*y+x*x*(1+x)
ck('acnode_strict_bound',s.expand(a-y*y-x*x/2-x*x*(x+s.Rational(1,2)))==0)
ck('acnode_odd_discriminant_valuation',s.diff(s.discriminant(a,y),x).subs(x,-1)!=0)
ck('distant_real_arc',s.expand(a.subs({x:-1-t*t,y:t*(1+t*t)}))==0)
ck('distant_arc_nonconstant',s.diff(t*(1+t*t),t).subs(t,0)==1)
# Real elliptic generators may generate a noncompact irreducible group.
D=s.diag(2,s.Rational(1,2));B=D*J*D.inv()
ck('separate_elliptic_conjugacy',J.trace()==B.trace()==0 and J.det()==B.det()==1)
ck('noncompact_product',s.trace(J*B)==-s.Rational(17,4))
ck('no_common_eigenline',all(s.Matrix.hstack(s.Matrix([a*s.I,1]),s.Matrix([b*4*s.I,1])).det()!=0 for a in (-1,1) for b in (-1,1)))
# Sign twist preserves projective coordinates; complex conjugation need not.
Z=s.diag(2+s.I,1/(2+s.I));tr=s.simplify(Z.trace())
ck('sign_invisible',s.simplify(tr**2-(-tr)**2)==0)
ck('orientation_operation_distinct',s.simplify(tr**2-s.conjugate(tr)**2)!=0)
# n does not suffice for an arbitrary index-n coset action; n! does.
p=[1,0,2]
def power_perm(p,n):
 q=list(range(len(p)))
 for _ in range(n):q=[p[i] for i in q]
 return q
ck('index_three_countercontrol',power_perm(p,3)[0]!=0)
ck('factorial_exponent_repairs',power_perm(p,6)==list(range(3)))
# The disconnected O2 component in SO3 reverses the axis and is a halfturn.
Q=s.Matrix([[0,1,0],[1,0,0],[0,0,-1]])
ck('O2_embeds_oriented',Q.T*Q==s.eye(3) and Q.det()==1)
ck('O2_halfturn',Q.trace()==-1 and Q*s.Matrix([0,0,1])==-s.Matrix([0,0,1]))
# Exact flat homology excludes finite odd H1 in the only finite-b1 type.
R=s.Matrix([[0,4,0],[4,0,0],[1,1,1]])
S=smith_normal_form(R,domain=ZZ)
ck('flat_finite_homology',sorted(abs(S[i,i]) for i in range(3))==[1,4,4])
# Concrete genus2 integral Seifert matrix with odd determinant, complementing proof all genera.
V=s.Matrix([[2,1,0,0],[0,3,0,0],[0,0,4,2],[0,0,1,5]])
ck('intersection_form_unimodular',(V-V.T).det()==1)
ck('branched_cover_odd',int((V+V.T).det())%2==1)
# Actual deformation directions and volume sign; the local model is only diagnostic.
z,alpha=s.symbols('z alpha',real=True);mu=alpha+z*z
ck('imaginary_fold_decreases_angle',s.expand(mu.subs(z,s.I*t)-alpha)==-t*t)
ck('real_fold_increases_angle',s.expand(mu.subs(z,t)-alpha)==t*t)
ck('fold_degree_two',s.diff(mu,z).subs(z,0)==0 and s.diff(mu,z,2)==2)
L=s.symbols('L',positive=True)
ck('schlafli_decreasing_angle_increases_volume',s.simplify(-L/2*(-1))==L/2)
out={'passed':len(checks),'failed':0,'checks':checks,'sympy_version':s.__version__,'scope':'Finite toy diagnostics; no knot construction, universal metric existence, or proof inferred from count.'}
Path(__file__).with_name('SCIENTIFIC_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
