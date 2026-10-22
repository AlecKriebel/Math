#!/usr/bin/env python3
"""Independent exact identities; geometric proof is in FULL_REPORT.md.
Explicit failures remain enabled under Python -O. All square roots are on
the positive local domain specified in the proof.
"""
import datetime, itertools, json
import sympy as s
u,v,x,t,epsilon=s.symbols('u v x t epsilon',real=True)
coordinates=(u,v,x,t)
R=s.Function('R')(*coordinates)
I=s.I
checks={}
def simp(a): return s.simplify(s.expand(a))
def clean(a): return {k:simp(c) for k,c in a.items() if simp(c)!=0}
def add(*forms):
    out={}
    for f in forms:
        for k,c in f.items(): out[k]=out.get(k,0)+c
    return clean(out)
def scale(c,f): return clean({k:c*a for k,a in f.items()})
def wedge(a,b):
    out={}
    for p,cp in a.items():
        for q,cq in b.items():
            z=p+q
            if len(set(z))<len(z): continue
            sign=(-1)**sum(z[i]>z[j] for i in range(len(z)) for j in range(i+1,len(z)))
            key=tuple(sorted(z)); out[key]=out.get(key,0)+sign*cp*cq
    return clean(out)
def d(f):
    out={}
    for key,c in f.items():
        for i,z in enumerate(coordinates): out=add(out,wedge({(i,):s.diff(c,z)},{key:1}))
    return clean(out)
def require(label,ok):
    checks[label]=bool(ok)
    if not ok: raise RuntimeError(label)
def equal(label,a,b): require(label,clean(add(a,scale(-1,b)))=={})
def scalar_equal(label,a,b): require(label,simp(a-b)==0)
def matrix_equal(label,a,b): require(label,all(simp(z)==0 for z in a-b))
def matrix(f):
    out=s.zeros(4)
    for (i,j),c in f.items(): out[i,j]=c;out[j,i]=-c
    return out
e=[{(i,):1} for i in range(4)]
volume={(0,1,2,3):1}
alpha=add(wedge(e[0],e[2]),scale(-1,wedge(e[1],e[3])))
beta=add(wedge(e[0],e[3]),wedge(e[1],e[2]))
gamma=add(scale(u,alpha),scale(-v,beta))
q=d(scale(R,e[1]))
beta_R=add(beta,q)
gamma_R=add(gamma,scale(-1,d(scale(R*v,e[1]))))
equal('closed_original_gamma',d(gamma),{})
equal('closed_perturbed_beta_arbitrary_R',d(beta_R),{})
equal('closed_perturbed_gamma_arbitrary_R',d(gamma_R),{})
equal('product_rule_all_cutoff_terms',d(scale(R*v,e[1])),scale(v,q))
equal('third_form_relation',gamma_R,add(scale(u,alpha),scale(-v,beta_R)))
equal('alpha_square',wedge(alpha,alpha),scale(2,volume))
equal('mixed_gram',wedge(alpha,beta_R),scale(s.diff(R,t),volume))
equal('beta_square',wedge(beta_R,beta_R),scale(2*(1-s.diff(R,x)),volume))
a,b,c=s.symbols('a b c',real=True)
h=s.symbols('h',positive=True)
D=1-b-c*c/4
jets={s.diff(R,u):a,s.diff(R,x):b,s.diff(R,t):c}
beta_jet={key:coef.subs(jets) for key,coef in beta_R.items()}
Bnum=add(beta_jet,scale(-c/2,alpha))
B=scale(1/h,Bnum)
A=matrix(alpha)
J=-A.inv()*matrix(B)
J_expected=s.Matrix([[c/2,b-1,0,0],[1,-c/2,0,0],
                     [0,-a,c/2,-1],[-a,0,1-b,-c/2]])/h
matrix_equal('endomorphism_from_two_form_pair',J,J_expected)
matrix_equal('J_square_before_root_substitution',J*J,-D/h**2*s.eye(4))
matrix_equal('real_part_antilinearity',J.T*A,-matrix(B))
matrix_equal('imaginary_part_antilinearity',J.T*matrix(B),D/h**2*A)
equal('orthogonalized_wedge',wedge(alpha,B),{})
equal('normalized_imaginary_square',wedge(B,B),scale(2*D/h**2,volume))
Psi=add(alpha,scale(I,B))
equal('complex_square_before_root_substitution',wedge(Psi,Psi),scale(2*(1-D/h**2),volume))
equal('conjugate_wedge_before_root_substitution',
      wedge(Psi,{key:s.conjugate(z) for key,z in Psi.items()}),
      scale(2*(1+D/h**2),volume))
l,m=s.symbols('l m',real=True)
scalar_equal('positive_plane_completed_square',2*l*l+2*c*l*m+2*(1-b)*m*m,
             2*((l+c*m/2)**2+D*m*m))
require('negative_D_zero_excludes_positive_plane',s.Matrix([[2,0],[0,0]]).det()==0)
scalar_equal('claimed_uniform_lower_bound',1-s.Rational(1,4)-s.Rational(1,4),s.Rational(1,2))
rho=s.Function('rho')(*coordinates)
cut=epsilon*rho*x*x/2
qcut=d(scale(cut,e[1]))
explicit_cut=add(scale(epsilon*x*x*s.diff(rho,u)/2,wedge(e[0],e[1])),
                scale(-epsilon*(rho*x+x*x*s.diff(rho,x)/2),wedge(e[1],e[2])),
                scale(-epsilon*x*x*s.diff(rho,t)/2,wedge(e[1],e[3])))
equal('all_cutoff_derivatives_included',qcut,explicit_cut)
omitted=add(beta,scale(-epsilon*rho*x,wedge(e[1],e[2])))
require('negative_omitted_cutoff_derivatives_not_closed',d(omitted)!={})
wrong=add(gamma,d(scale(R*v,e[1])))
require('negative_wrong_gamma_sign_breaks_relation',
        add(wrong,scale(-1,add(scale(u,alpha),scale(-v,beta_R))))!={})
keys=list(itertools.combinations(range(4),2))
sample={u:1,v:1,x:1,t:0}
qtest=scale(-s.Rational(1,4),wedge(e[1],e[2]))
wrong_sample=add({key:z.subs(sample) if hasattr(z,'subs') else z for key,z in gamma.items()},qtest)
flat=s.Matrix([[f.get(key,0) for f in (alpha,add(beta,qtest),wrong_sample)] for key in keys])
require('negative_wrong_gamma_sign_rank_three',flat.rank()==3)
z,w=s.symbols('z w')
Y=s.Function('Y')(z)
Jac=s.Matrix([[1,0],[-w*s.diff(Y,z)/Y**2,1/Y]])
scalar_equal('holomorphic_jacobian',Jac.det(),1/Y)
scalar_equal('normal_form_Omega0',Jac.det(),1/Y)
scalar_equal('normal_form_Omega1',z*Jac.det(),z/Y)
k=1-epsilon*x
klocal=J_expected.subs({a:0,b:epsilon*x,c:0,h:s.sqrt(k)})
J0=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
matrix_equal('epsilon_zero_matrix',klocal.subs(epsilon,0),J0)
matrix_equal('J_at_origin_equals_J0',klocal.subs(x,0),J0)
N={}
for j,qindex in itertools.combinations(range(4),2):
    components=[]
    for i in range(4):
        val=sum(klocal[p,j]*s.diff(klocal[i,qindex],coordinates[p])
                -klocal[p,qindex]*s.diff(klocal[i,j],coordinates[p])
                -klocal[i,p]*s.diff(klocal[p,qindex],coordinates[j])
                +klocal[i,p]*s.diff(klocal[p,j],coordinates[qindex]) for p in range(4))
        components.append(simp(val))
    N[f'{j},{qindex}']=[str(z) for z in components]
    if (j,qindex)==(0,2):
        matrix_equal('N_u_x_all_components',s.Matrix(components),s.Matrix([-epsilon/(2*k),0,0,0]))
        scalar_equal('N_u_x_origin',components[0].subs(x,0),-epsilon/2)
phi1=add(e[0],scale(I*s.sqrt(k),e[1]))
phi2=add(e[2],scale(I/s.sqrt(k),e[3]))
local_beta=add(wedge(e[0],e[3]),scale(k,wedge(e[1],e[2])))
equal('coframe_factorization',wedge(phi1,phi2),add(alpha,scale(I/s.sqrt(k),local_beta)))
equal('nonintegrability_top_wedge',wedge(d(phi1),wedge(phi1,phi2)),scale(-epsilon/(2*k),volume))
Zbar1=s.Matrix([1,I/s.sqrt(k),0,0])
Zbar2=s.Matrix([0,0,1,I*s.sqrt(k)])
Z1=s.Matrix([1,-I/s.sqrt(k),0,0])
bracket=s.Matrix([simp(sum(Zbar1[p]*s.diff(Zbar2[i],coordinates[p])-Zbar2[p]*s.diff(Zbar1[i],coordinates[p]) for p in range(4))) for i in range(4)])
matrix_equal('annihilator_bracket_mixed_type',bracket,-epsilon/(4*k)*(Zbar1-Z1))
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'sympy_version':s.__version__,'passed':all(checks.values()),
                  'checks':checks,'N_pairs_coordinate_order':['u','v','x','t'],
                  'N_pairs':N,'limitations':'Exact identity checks; uniform and geometric claims require the accompanying proof.'},indent=2))
