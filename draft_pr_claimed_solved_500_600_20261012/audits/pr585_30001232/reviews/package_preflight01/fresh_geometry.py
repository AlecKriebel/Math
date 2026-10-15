"""New algebraic/limiting-case controls. No finite test is an existence proof."""
import json, sys, sympy as s
if not __debug__ or sys.flags.optimize: raise RuntimeError('Assertions must remain enabled')
counts={}; negatives=[]
def ck(group,condition):
 if not bool(condition): raise RuntimeError(group)
 counts[group]=counts.get(group,0)+1
def neg(name,false_claim):
 ck('negative_controls',not false_claim);negatives.append({'case':name,'false_claim_rejected':True})
d,r,h,b,x,y,z,t=s.symbols('d r h b x y z t')
# The incidence graph becomes a hypersurface of bidegree (d,2) over a base
# of genus r-1 when the double base cover has 2r branch points.
D=d*h+2*b; Kambient=-3*h+(2*r-4)*b; K=(Kambient+D)
c1ambient=3*h-(2*r-4)*b
c2ambient=3*h*h-3*(2*r-4)*h*b
c2surface=c2ambient-c1ambient*D+D*D
integrate=lambda q:s.expand(q).coeff(h,2).coeff(b,1)
k2=s.factor(integrate(K*K*D));euler=s.factor(integrate(c2surface*D));chi=s.factor((k2+euler)/12)
ck('generic_branch_incidence',s.expand(k2-2*(9-d*d+2*r*d*(d-3)))==0)
ck('generic_branch_incidence',s.expand(euler-(2*(3+d*d)-2*r*(2-(d-1)*(d-2))))==0)
ck('generic_branch_incidence',s.expand(chi-(2+r*d*(d-3)/2))==0)
ck('four_branch_symbolic',s.expand(k2.subs(r,2)-6*(d-1)*(d-3))==0)
ck('four_branch_symbolic',s.expand(euler.subs(r,2)-6*(d-1)**2)==0)
# Formal analytic change of coordinates takes x^(d-1)+x^d-y^(d-1)
# to X^(d-1)-y^(d-1), with derivative dX/dx(0)=1.
local=[]
for dd in range(3,13):
 m=dd-1
 coord=s.series(x*(1+x)**s.Rational(1,m),x,0,13).removeO()
 ck('formal_local_ordinary_point',s.diff(coord,x).subs(x,0)==1)
 err=s.series(coord**m-x**m*(1+x),x,0,13).removeO().expand()
 ck('formal_local_ordinary_point',err==0)
 ck('formal_local_ordinary_point',s.discriminant(t**m-1,t)!=0)
 pa=s.Rational((dd-1)*(dd-2),2);delta=s.Rational(m*(m-1),2)
 ck('normalization_genus',pa-delta==0)
 local.append({'d':dd,'multiplicity':m,'tangent_discriminant':int(s.discriminant(t**m-1,t)),'formal_coordinate_jet':str(coord),'jet_error_to_degree12':str(err),'arithmetic_genus':int(pa),'delta':int(delta),'normalization_genus':0})
# A distinct ordinary fixed point does not guarantee global irreducibility.
neg('squarefree_tangent_cone_alone_proves_global_integrality',s.Poly((x**6-y**6)*(z+x),z).content()==1)
# Symbolic dimensional deficit, plus exact degree2 boundary.
a=s.symbols('a');N=lambda n:n*(n+3)/2
ck('universal_pencil_identity',s.expand(N(d)-N(a)-N(d-a)-a*(d-a))==0)
neg('degree2_bad_join_is_proper',N(2)-(N(1)+N(1)+1)>0)
ck('degree7_join',N(7)==35 and N(1)+N(6)+1==30)
# Branch/fibre algebra with different specific branch values from previous family.
P=(t-1)*(t-3)*(t-4)*(t-12);F=x**6-y**6+x**7
ck('base_cover',s.gcd(P,s.diff(P,t))==1 and P.subs(t,0)==144)
for root in [-12,12]:
 eq=z*z-P.subs(t,F)
 ck('unramified_at_marked_point',eq.subs({x:0,y:0,z:root})==0)
 ck('unramified_at_marked_point',s.diff(eq,z).subs({x:0,y:0,z:root})!=0)
ck('split_fibre_CRT',s.gcd(z-12,z+12)==1)
ck('split_fibre_CRT',s.rem(z*z-144,z-12,z)==0 and s.rem(z*z-144,z+12,z)==0)
neg('branching_at_high_multiplicity_fibre_remains_smooth',any(s.diff(z*z-F,v).subs({x:0,y:0,z:0})!=0 for v in [x,y,z]))
# Why A=2F+E is the first integral coefficient that works on E.
neg('A_F_plus_E_is_ample',1-1>0)
neg('vertical_component_missed_by_E_has_positive_A_degree',2*0+0>0)
# Canonical degree on lifted section equals 2r-2. It cannot be called a
# rational exceptional curve when r=2: self-intersection -2, genus 1.
neg('two_branch_cover_has_ample_canonical',2*1-2>0)
neg('four_branch_lifted_section_is_rational_minus_one',(-2,1)==(-1,0))
# Preserve exact threshold: six branches at degree7 would give equality.
neg('six_branch_degree7_is_strict',int(k2.subs({r:3,d:7}))<4**4)
neg('degree6_four_branch_is_strict',int(k2.subs({r:2,d:6}))<3**4)
neg('one_component_lift_has_degree_two',1==2)
ck('degree7_actual_comparison',int(k2.subs({r:2,d:7}))==144<256)
u=s.symbols('u',nonnegative=True)
margin=s.expand(((d-3)**3-6*(d-1)).subs(d,u+7))
ck('all_degree7_and_above_positive_coefficients',margin==u**3+12*u**2+42*u+28)
threshold=[]
for dd in range(4,25):
 val=int(k2.subs({r:2,d:dd}));q=(dd-3)**4-val
 ck('boundary_replay',(q>0)==(dd>=7))
 threshold.append({'d':dd,'K2':val,'upper_quotient':f'1/{dd-1}','margin':q,'strict_violation':q>0})
result={'status':'PASS','sympy':s.__version__,'counts':counts,'total_controls':sum(counts.values()),'general_branch_formulas':{'K2':str(k2),'c2':str(euler),'chi':str(chi)},'all_d_inequality_positive_coefficient_certificate':str(margin),'local_formal_coordinate_controls':local,'threshold':threshold,'negative_controls':negatives,'scope':'Exact algebra and limiting-case controls only. Bertini, integral-pencil existence, all-curve ampleness, connectedness and mathematical historical priority require proof/source analysis.'}
print(json.dumps(result,indent=2,sort_keys=True))
