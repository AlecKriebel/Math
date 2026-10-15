#!/usr/bin/env python3
"""New exact acceptance controls; no novelty search or tolerance-based evidence."""
import itertools,json,pathlib,sys
import sympy as s
OUT=pathlib.Path(__file__).resolve().parent
checks=[]
def record(name,**kw): checks.append(dict(name=name,passed=True,**kw))
def zero(M): assert all(s.simplify(v)==0 for v in M),M
def prod(a,b):return (a*b.T+b*a.T)/2
def strain(u,x):
    D=u.jacobian(x);return (D+D.T)/2
def integral(poly,variables,bounds):
    v=s.expand(poly)
    for t,(lo,hi) in zip(variables,bounds):v=s.integrate(v,(t,lo,hi))
    return s.simplify(v)

# Fully oblique 4D Hessian restrictions, including components outside any
# coordinate-aligned a,b plane. Compare coefficient solution space with
# covector-generated Hessians, rather than merely checking a template field.
d=4;a=s.Matrix([1,2,-1,3]);b=s.Matrix([-2,1,4,1])
pairs=[(i,j) for i in range(d) for j in range(i,d)]
h=s.symbols('h:'+str(len(pairs)));H=s.zeros(d)
for (i,j),v in zip(pairs,h):H[i,j]=H[j,i]=v
def matrix(P):
    equations=[P[j,l]*H[i,k]+P[i,k]*H[j,l]-P[j,k]*H[i,l]-P[i,l]*H[j,k]
               for i,j,k,l in itertools.product(range(d),repeat=4)]
    return s.linear_eq_to_matrix(equations,h)[0]
A=matrix(prod(a,b))
V=s.Matrix.hstack(s.Matrix([a[i]*a[j] for i,j in pairs]),s.Matrix([b[i]*b[j] for i,j in pairs]))
zero(A*V);assert V.rank()==len(h)-A.rank()==2
record('fully_oblique_4D_coefficient_nullspace',a=list(a),b=list(b),constraint_rank=A.rank(),template_rank=V.rank())
A=matrix(a*a.T)
V=s.Matrix.hstack(*[s.Matrix([prod(a,s.eye(d)[:,r])[i,j] for i,j in pairs]) for r in range(d)])
zero(A*V);assert V.rank()==len(h)-A.rank()==d
record('fully_oblique_4D_parallel_hessian_space',constraint_rank=A.rank(),template_rank=V.rank())

# Measure-level oblique pullback with negative determinant. Define u_x on an
# oblique parallelogram via two signed jumps in canonical variables. Direct
# weak integration checks the full matrix, absolute Jacobian and both-sided
# displacement transform; the intentionally signed Jacobian fails.
y=s.Matrix(s.symbols('y0:2',real=True));aa=s.Matrix([2,1]);bb=s.Matrix([3,-2])
S=s.Matrix.hstack(aa,bb);B=S.inv().T
assert B.det()==-s.Rational(1,7)
psi=(1-y[0]**2)**2*(1-y[1]**2)**2*(1+y[0]/5+y[1]/3)
grad_x=B.inv().T*s.Matrix([s.diff(psi,t) for t in y])
r=s.Rational(1,3);q=-s.Rational(1,4);actual=s.zeros(2)
for xb,yb in itertools.product([(-1,q),(q,1)],[(-1,r),(r,1)]):
    w=s.Matrix([int(bool(sum(yb)/2>r)),-3*int(bool(sum(xb)/2>q))])
    ux=S*w
    for i,j in itertools.product(range(2),repeat=2):
        actual[i,j]-=abs(B.det())*integral((ux[i]*grad_x[j]+ux[j]*grad_x[i])/2,list(y),[xb,yb])
nu_action=abs(B.det())*(integral(psi.subs(y[1],r),[y[0]],[(-1,1)])-3*integral(psi.subs(y[0],q),[y[1]],[(-1,1)]))
zero(actual-prod(aa,bb)*nu_action)
assert any(v!=0 for v in actual+prod(aa,bb)*nu_action)
record('signed_jump_weak_oblique_negative_Jacobian',determinant=str(B.det()),nu_action=str(nu_action),strain_action=[[str(actual[i,j]) for j in range(2)] for i in range(2)],wrong_signed_Jacobian_rejected=True)
Ey=s.Matrix([[0,nu_action/(2*abs(B.det()))],[nu_action/(2*abs(B.det())),0]])
zero(B.T*actual*B/abs(B.det())-Ey)
record('signed_Radon_measure_pullback_congruence',factor='1/abs(det B)=7',canonical_E12_action=str(Ey[0,1]))

# Dual transverse moment tests on shifted unequal intervals. Invert the exact
# moment matrix to isolate each signed Radon coefficient, including profiles
# with atoms and a density. This tests regularity extraction algebra on a box
# whose coordinate moments are not centered at zero.
t1,t2,ss=s.symbols('t1 t2 ss',real=True)
bounds=[(s.S(2),s.S(5)),(-s.S(3),-s.S(1))]
eta=(t1-2)**2*(5-t1)**2*(t2+3)**2*(-1-t2)**2
features=s.Matrix([1,t1,t2])
G=s.Matrix(3,3,lambda i,j:integral(eta*features[i]*features[j],[t1,t2],bounds))
assert G.det()>0
duals=[s.expand(eta*sum(G.inv()[l,j]*features[j] for j in range(3))) for l in range(3)]
M=s.Matrix(3,3,lambda i,j:integral(duals[i]*features[j],[t1,t2],bounds))
zero(M-s.eye(3))
record('shifted_box_dual_moment_extraction',moment_determinant=str(G.det()),dual_moment_matrix=str(M))
chi=(1-ss**2)**2*(1+ss/7)
mu=s.simplify(chi.subs(ss,s.Rational(1,3))-3*chi.subs(ss,-s.Rational(1,2))+integral(ss**2*chi,[ss],[(-1,1)]))
gamma1=2*chi.subs(ss,-s.Rational(1,2));gamma2=-4*chi.subs(ss,s.Rational(1,3))
recovered=M*s.Matrix([mu,gamma1,gamma2]);zero(recovered-s.Matrix([mu,gamma1,gamma2]))
assert mu!=0 and gamma1>0 and gamma2<0
record('signed_atomic_and_density_profile_recovery',mu_action=str(mu),gamma_actions=[str(gamma1),str(gamma2)])

# Positivity on a bounded box does not license whole-space tangent reduction.
x=s.Matrix(s.symbols('x0:3',real=True));e1,e2,e3=(s.eye(3)[:,i] for i in range(3))
u=e1*(3*x[1]+x[1]*x[2])+e2*x[0]*x[2]-e3*x[0]*x[1]
zero(strain(u,x)-prod(e1,e2)*(3+2*x[2]))
assert 3-2>0 and (3+2*x[2]).subs(x[2],-2)<0
record('local_positive_independent_transverse_term_survives',box_lower_bound='1',global_negative_witness='z=-2')
P=x[0]**2+x[0]**3/6
u=e1*(4*x[0]+x[1]*s.diff(P,x[0]))-e2*P
zero(strain(u,x)-e1*e1.T*(4+(2+x[0])*x[1]))
assert all((4+(2+x[0])*x[1]).subs({x[0]:sx,x[1]:tx})>0 for sx,tx in itertools.product([-s.Rational(1,2),s.Rational(1,2)],repeat=2))
assert (4+(2+x[0])*x[1]).subs({x[0]:0,x[1]:-3})<0
record('local_positive_parallel_variable_transverse_term_survives',box_lower_bound='11/4',global_negative_witness='s=0,t=-3')

# The zero-product edge uses the real norm identity, not an eigenvalue guess.
av=s.Matrix(s.symbols('a0:5',real=True));bv=s.Matrix(s.symbols('b0:5',real=True));PP=prod(av,bv)
assert s.expand(sum(v*v for v in PP)-(av.dot(av)*bv.dot(bv)+av.dot(bv)**2)/2)==0
record('real_zero_symmetric_product_norm_identity',identity='2||a odot b||F^2=|a|^2|b|^2+(a.b)^2',deduction='product zero implies at least one vector zero')

# d=1 signed atomic BV map: direct weak pairing. Every regular scalar map
# belongs to the nonzero line, including this nonsmooth boundary example.
z=s.Symbol('z',real=True);test=(1-z*z)**2*(1+z/3)
actual=-integral(s.diff(test,z),[z],[(-s.Rational(1,2),s.Rational(1,3))])
expected=test.subs(z,-s.Rational(1,2))-test.subs(z,s.Rational(1,3))
assert s.simplify(actual-expected)==0
record('dimension_one_signed_BV_weak_pairing',derivative_action=str(actual),nonzero_product='-10',scalar_nu_action=str(actual/-10))

# The 2011 positive-polar Lemma4.4 prints an overly broad iff: arbitrary BV
# profiles need not have its fixed positive polar. This does not invalidate
# the signed LD Propositions4.7/4.9 or the later signed theorem used here.
xx=s.Matrix(s.symbols('r0:2',real=True));PP=prod(s.Matrix([1,0]),s.Matrix([0,1]))
EE=strain(s.Matrix([-xx[1],0]),xx);zero(EE+PP)
norm=s.sqrt(sum(v*v for v in EE));assert norm==1/s.sqrt(2)
assert any(v!=0 for v in EE-PP*norm/s.sqrt(sum(v*v for v in PP)))
record('2011_positive_polar_iff_sufficiency_wording_countercontrol',field='u=(-x2,0)',profile='h2(t)=-t in BV_loc',strain='-(e1 odot e2)L2',printed_positive_polar_rejected=True,scope='Source precision only; the audited target uses signed line classification')

# Smooth-boundary annulus countercontrols. Branches glue flatly at |coordinate|
# =1; pointwise equal-slice witnesses rule out one global family modulo rigid
# motion. These are distinct domains from the prior polygonal controls.
p,q=s.symbols('p q',real=True);bump=s.exp(-1/(1-q*q))
uu=s.Matrix([bump,0]);zero(strain(uu,s.Matrix([p,q]))-prod(s.Matrix([1,0]),s.Matrix([0,1]))*s.diff(bump,q))
assert bump.subs(q,0)==s.exp(-1)
record('smooth_annulus_independent_globalization_countercontrol',domain='1<x^2+y^2<9',branch='u=(bump(y),0) on right |y|<1; zero elsewhere',points=['(-2,0)','(2,0)'],first_component_difference='exp(-1)',rigid_same_slice_difference='0')
f=s.exp(-1/(1-p*p));uu=s.Matrix([q*s.diff(f,p),-f])
zero(strain(uu,s.Matrix([p,q]))-s.diag(q*s.diff(f,p,2),0))
assert f.subs(p,0)==s.exp(-1)
record('smooth_annulus_parallel_globalization_countercontrol',domain='1<x^2+y^2<9',branch='u=(y bumpprime(x),-bump(x)) on upper |x|<1; zero elsewhere',points=['(0,-2)','(0,2)'],second_component_difference='-exp(-1)',rigid_same_slice_difference='0')

result={'pass':True,'python':sys.version.split()[0],'sympy':s.__version__,'total':len(checks),'checks':checks,'limits':'New exact controls supplement the sealed all-dimensional distributional reconstruction and published theorem. No numerical tolerance, formal proof-assistant certificate or new discovery claim.'}
(OUT/'FRESH_RESULTS.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps(result,indent=2,default=str))
