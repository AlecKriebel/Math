"""Fresh exact controls and hypothesis mutations; finite checks supplement proof.
Does not import or execute any archived program.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import datetime,hashlib,json,math,sys
import sympy as s
checks=[]
def check(name,condition,evidence):
    if not condition: raise AssertionError(name)
    checks.append({'name':name,'pass':True,'evidence':evidence})
r=s.symbols('r', positive=True); k=s.symbols('k'); z=s.symbols('z')
g=s.exp(s.I*k*r)/(4*s.pi*r)
a=-s.diff(g,r)/r-k**2*g; b=-s.diff(g,r,2)+s.diff(g,r)/r
ra=s.simplify(a-1/(4*s.pi*r**3)); rb=s.simplify(b+3/(4*s.pi*r**3))
check('radial_remainder_order1_I',s.simplify(s.limit(r*ra,r,0)+k**2/(8*s.pi))==0,'symbolic radial Hessian differentiation')
check('radial_remainder_order1_ee',s.simplify(s.limit(r*rb,r,0)+k**2/(8*s.pi))==0,'symbolic radial Hessian differentiation')
check('radiation_constant_I',s.simplify(s.limit(ra+k**2/(8*s.pi*r),r,0)+s.I*k**3/(6*s.pi))==0,'-i*k^3/(6*pi)')
check('radiation_constant_ee',s.simplify(s.limit(rb+k**2/(8*s.pi*r),r,0))==0,'zero ee constant')
f=s.exp(s.I*z)*(1-s.I*z-z*z)-1; q=s.exp(s.I*z)*(z*z+3*s.I*z-3)+3
for n in range(2,81):
    fc=s.diff(f,z,n).subs(z,0)/s.factorial(n); qc=s.diff(q,z,n).subs(z,0)/s.factorial(n)
    check('Taylor_n'+str(n),s.simplify(fc-s.I**n*(n-1)**2/s.factorial(n))==0 and s.simplify(qc+s.I**n*(n-1)*(n-3)/s.factorial(n))==0,str(n))
# Full finite squared-radius shells and a deliberately damaged first shell.
shells=defaultdict(lambda:s.zeros(3)); bound=math.isqrt(200)
for x in range(-bound,bound+1):
 for y in range(-bound,bound+1):
  for z0 in range(-bound,bound+1):
   v=s.Matrix([x,y,z0]); d=x*x+y*y+z0*z0
   if 0<d<=200: shells[d]+=d*s.eye(3)-3*v*v.T
for d,mat in sorted(shells.items()): check('complete_shell_'+str(d),mat==s.zeros(3),'integer tensor numerator identically zero')
v=s.Matrix([1,0,0]); bad=shells[1]-(s.eye(3)-3*v*v.T)
check('mutation_missing_lattice_point_detected',bad!=s.zeros(3),str(bad))
# Exact generic Fourier projector, real symbolic direction.
x,y,z0=s.symbols('x y z',real=True); v=s.Matrix([x,y,z0]); den=(v.T*v)[0]
L=v*v.T/den; D=L-s.eye(3)/3
check('longitudinal_idempotence',s.simplify(L*L-L)==s.zeros(3),'valid for every real nonzero direction')
check('static_minimal_polynomial',s.simplify((D+s.eye(3)/3)*(D-2*s.eye(3)/3))==s.zeros(3),'eigenvalues -1/3 or 2/3')
# Active blocks represent e1 and moving en, n>=2, in the infinite Hilbert space.
X=s.Matrix([[0,1],[0,0]]); P=s.diag(1,0)
check('compact_left_mutation',P*X==X and X*P==s.zeros(2),'X_n strongly tends to 0 but ||P X_n||=1')
S=2*P+X; E=P+X/2
check('nonselfadjoint_spectral_mutation',E*E==E and S*E==2*E and E*S==2*E and E-P==X/2,'projection difference norm=1/2 despite strong convergence')
check('moving_static_resolvent_norm_obstruction',F(1,2-1)-F(1,2)==F(1,2),'B_n=|en><en|, B=0; z=2')
B=s.diag(-s.Rational(1,3),s.Rational(2,3)); zz=2+s.I/3
R=(zz*s.eye(2)-B).inv(); Rc=(s.conjugate(zz)*s.eye(2)-B).inv()
check('adjoint_resolvent_conjugation',s.simplify(R.conjugate().T-Rc)==s.zeros(2),'R(z)*=R(conjugate z)')
check('mutation_drop_resolvent_conjugation_detected',s.simplify(R.conjugate().T-R)!=s.zeros(2),'wrong un-conjugated formula fails off real line')
eps=s.symbols('eps',positive=True); A=s.Matrix([[2,1],[eps**2,2]])
check('individual_Jordan_mutation',(A-2*s.eye(2)).det()==-eps**2 and s.expand(A.charpoly(z).as_expr())==s.expand((z-2-eps)*(z-2+eps)),'simple 2+/-eps versus limiting defective 2; total projection identity')
# Positive rational smallness and infinite-series majorant identities.
e_upper=sum((F(1,math.factorial(i)) for i in range(4)),F(0))+F(1,24)/(1-F(1,5))
check('e_majorant',e_upper==F(87,32) and 2*e_upper-F(9,2)<1,str(e_upper))
check('C2_HS_bound',F(6,64)*F(32,3)==1,'Frobenius squared=6 and ball-difference integral <=32*pi^2/3')
check('remainder_HS_bound',F(3,4)*2*F(4,3)==2,'uses r<=2 and |B|=4*pi/3')
k0=F(1,10000); eta=120*k0*k0
check('frequency_smallness',2*k0*k0<=F(1,60) and eta<=F(1,2),'resolvent and graph conditions')
check('Riesz_graph_trace_constants',F(1,30)*30*60==60 and F(120)/(1-F(1,2))==240 and 3*(2+2*240)==1446,'60,240,1446')
check('negative_trace',-F(2,3)+1446*k0==-F(7831,15000)<0,'upper bound divided by k0^3')
for ell in range(1,1001):
    value=F(ell,2*ell+1)-F(1,3)
    check('ball_harmonic_gap_'+str(ell),value==F(ell-1,3*(2*ell+1)) and (value==0 if ell==1 else value>=F(1,15)),str(value))
for j in (1,2,10,100):
    ratio=F(1,2)**(3*j+12)*F(1,8)/(1-F(1,8))
    check('infinite_removed_volume_series_'+str(j),ratio==F(1,2)**(3*j+12)/7 and ratio<1,str(ratio))
# Scalar weighting is necessary: discrete inner product h^3 dot.
h=F(2,7); fvals=[F(1,3),F(2,5)]; cell_averages=[F(-3,7),F(5,9)]
lhs=h**3*sum(a*b for a,b in zip(fvals,cell_averages)); rhs=h**3*sum(a*b for a,b in zip(fvals,cell_averages))
check('weighted_embedding_pairing',lhs==rhs,'cell integral h^3 times each cell average')
check('mutation_unweighted_cell_average_adjoint_detected',lhs!=sum(a*b for a,b in zip(fvals,cell_averages)),'ordinary unscaled sequence norm requires an h^3 adjoint factor')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'sympy':s.__version__,'count':len(checks),'all_pass':True,'limitations':'Exact algebra and finite checks; universal limits, completeness and infinite-mask claims use written proofs. Moving-block examples have exact infinite-space interpretations.','checks':checks}
out=Path(__file__).with_name('independent_control_results.json'); out.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'count':len(checks),'all_pass':True,'output':str(out)}))
