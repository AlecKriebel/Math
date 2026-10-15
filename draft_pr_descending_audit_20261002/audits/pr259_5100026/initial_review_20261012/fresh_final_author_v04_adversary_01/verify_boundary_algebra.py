#!/usr/bin/env python3
"""New first-principles boundary/algebra controls; no research verifier imports."""
from pathlib import Path
import sys,json,datetime,itertools,math
V=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor')
sys.path.insert(0,str(V))
import sympy as s
O=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr259_5100026/initial_review_20261012/fresh_final_author_v04_adversary_01')
checks=[]
def ck(ok,n):
 if not ok:raise AssertionError(n)
 checks.append(n)
def zero(x,n):ck(s.factor(s.simplify(x))==0,n)
def dot(x,y):return (x.T*y)[0]
def det(x,y):return s.det(s.Matrix.hstack(x,y))
def I(X,Y,M):
 L=s.Matrix.vstack((X-M).T,(Y-M).T);v=s.Matrix([dot(X-M,X),dot(Y-M,Y)])
 return L.inv()*v
# Generic shared boundary tangent, derived directly from defining line equations.
h,r,t,f,g=s.symbols('h r t f g',real=True)
X=s.Matrix([h,r]);Y=s.Matrix([h,t]);M=s.Matrix([f,g])
U=s.Matrix([h-(r-g)*(t-g)/(h-f),r+t-g])
zero(dot(X-M,U-X),'raw_first_antipedal_line');zero(dot(Y-M,U-Y),'raw_second_antipedal_line')
zero(det(X-M,Y-M)-(h-f)*(t-r),'raw_line_determinant')
Uopp=s.Matrix([-h-(-r-g)*(-t-g)/(-h-f),-r-t-g])
P=(U+Uopp)/2
zero(P[0]-(h*g*(r+t)-f*(r*t+g*g))/(h*h-f*f),'opposite_pair_normal');zero(P[1]+g,'opposite_pair_tangent')
# Exact rectangle formula checked directly in arbitrary orthonormal side axes.
l,m,n=s.symbols('l m n',real=True);verts=[s.Matrix([h,l]),s.Matrix([-h,l]),s.Matrix([-h,-l]),s.Matrix([h,-l])];F=s.Matrix([m,n])
mean=sum((I(verts[i],verts[(i+1)%4],F) for i in range(4)),s.zeros(2,1))/4
claimed=s.Matrix([m*((l*l-n*n)/(h*h-m*m)-1)/2,n*((h*h-m*m)/(l*l-n*n)-1)/2])
zero(mean[0]-claimed[0],'general_rectangle_x');zero(mean[1]-claimed[1],'general_rectangle_y')
b=s.symbols('b',positive=True)
zero(claimed[0].subs({h*h:b*b+m*m,l*l:b*b+n*n},simultaneous=True),'focal_support_rectangle_x_zero');zero(claimed[1].subs({h*h:b*b+m*m,l*l:b*b+n*n},simultaneous=True),'focal_support_rectangle_y_zero')
# The Jacobi proof's residue statement is a general two-normal equation, not numerical cancellation.
lx,ly,qx,qy,mx,my=s.symbols('lx ly qx qy mx my')
L=s.Matrix([lx,ly]);Q=s.Matrix([qx,qy]);F=s.Matrix([mx,my]);J=lambda x:s.Matrix([-x[1],x[0]])
R=lambda F,Q:-dot(L,L)*J(Q-F)/det(L,Q-F)
zero(dot(L,R(F,Q))-dot(L,L),'residue_singular_line');zero(dot(Q-F,R(F,Q)),'residue_regular_line')
zero(R(F,Q)[0]+R(F,-Q)[0]-R(-F,Q)[0]-R(-F,-Q)[0],'four_incident_residue_x');zero(R(F,Q)[1]+R(F,-Q)[1]-R(-F,Q)[1]-R(-F,-Q)[1],'four_incident_residue_y')
# Existing-proof compact curve: square completion, global root exchange, both charts and regular grouping.
d,e,z,w,x=s.symbols('d e z w x');curve=d*z*z*w*w-z*z-w*w+2*e*z*w+d
poly=d*z**4+(e*e-d*d-1)*z*z+d
zero(((d*z*z-1)*w+e*z)**2-poly-(d*z*z-1)*curve,'curve_square_completion')
result=s.factor(s.resultant(poly,s.diff(poly,z),z));zero(result-16*d**3*((d-1)**2-e**2)**2*((d+1)**2-e**2)**2,'squarefree_resultant')
other=-z-2*e*w/(d*w*w-1)
zero(s.factor(curve.subs({z:w,w:other},simultaneous=True))-curve,'rootexchange_preservescurve')
zero(s.expand(x*x*curve.subs(z,1/x))-((d-x*x)*w*w+2*e*x*w+d*x*x-1),'zinfinity_chart')
zero(s.expand(x*x*curve.subs(w,1/x))-((d-x*x)*z*z+2*e*x*z+d*x*x-1),'winfinity_chart')
zero(-2*e*z*z/(d*z*z-1)+2*e/(d-z**-2),'incident_trace_holomorphic_form')
zero(curve.subs(e,0).subs({z:w,w:-z},simultaneous=True)-curve.subs(e,0),'eta0_step')
# Odd least-3 physical billiard: exact defining geometry, common confocal caustic, specular certificate.
q=(4-s.sqrt(13))/3;T=s.sqrt(1-q*q);lam=1-q*q;F=s.Matrix([s.sqrt(3),0])
ck(bool(q>0) and bool(q<s.Rational(1,3)) and bool(lam>0) and bool(lam<1),'odd_witness_strict_domain')
zero(3*q*q-8*q+1,'odd_witness_quadratic')
tri=[s.Matrix([0,1]),s.Matrix([2*T,-q]),s.Matrix([-2*T,-q])]
for i,X in enumerate(tri):zero(X[0]**2/4+X[1]**2-1,'odd_boundary_'+str(i))
caustic=s.diag(4-lam,1-lam)
for i,X in enumerate(tri):
 Y=tri[(i+1)%3];normal=J(Y-X);level=dot(normal,X)
 zero(dot(normal,caustic*normal)-level*level,'odd_confocal_tangency_'+str(i))
 contact=caustic*normal/level;rho=s.simplify(dot(contact-X,Y-X)/dot(Y-X,Y-X))
 ck(bool(rho>0) and bool(rho<1),'odd_interior_contact_'+str(i))
# P1 incoming/outgoing unit tangential components agree; explicit signs select reflection.
ell2=4*T*T+(1+q)**2
zero(T*T*(1-3*q)**2-4*q*q*ell2,'odd_unit_reflection_squared_certificate')
ck(bool(1-3*q>0) and bool(q>0) and bool(T>0),'odd_reflection_correct_unsquared_sign')
ck(bool(1+q>0),'odd_incoming_normal_positive');ck(bool(-T/2<0),'odd_outgoing_normal_negative')
# At P0 symmetry reflects the two equal flights; at P2 mirror reflection handles the remaining vertex.
ck(len({tuple(X) for X in tri})==3,'odd_least_period3')
def outer(V):
 out=[]
 for i,X in enumerate(V):
  Y=V[(i+1)%len(V)];N=s.Matrix([[X[0]/4,X[1]],[Y[0]/4,Y[1]]]);out.append(s.simplify(N.inv()*s.ones(2,1)))
 return out
def centroid(V):
 R=outer(V);U=[]
 for i,X in enumerate(R):
  Y=R[(i+1)%len(R)];ck(s.simplify(det(X-F,Y-F))!=0,'odd_antipedal_finite_'+str(len(checks)));U.append(I(X,Y,F))
 return s.simplify(sum(U,s.zeros(2,1))/len(U))
C=centroid(tri);Cneg=centroid([-X for X in tri]);zero(C[1]+6,'odd_mean_y_minus6');zero(Cneg[1]-6,'central_odd_mean_y_plus6');zero(C[1]-Cneg[1]+12,'odd_phase_difference_nonzero')
# Repetition preserves the defining list mean exactly, independently of period nomenclature.
zero(centroid(tri+tri)[1]-C[1],'padded_even6_odd_mean_unchanged');zero(centroid([-X for X in tri+tri])[1]-Cneg[1],'padded_even6_central_mean_unchanged')
# Bounded incidence sanity checks; the general modular argument is recorded separately.
periodcases=0
for N in range(6,65,2):
 for tau in range(1,N//2):
  if math.gcd(N,tau)!=1:continue
  ck(tau%2==1,'odd_coprime_winding_'+str((N,tau)))
  poleindices=[j for j in range(N) if (tau*j)%(N//2)==0]
  ck(poleindices==[0,N//2],'twoopposite_endpointpoles_'+str((N,tau)))
  ck(len({N-1,0,N//2-1,N//2})==4,'fourdistinct_incidentedges_'+str((N,tau)));periodcases+=1
result={'schema':'independent-v04-selective-boundary-and-algebra-controls','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'bounded_star_cases':periodcases,'exact_algebra_or_geometry_checks':len(checks)-3*periodcases,'odd_triangle_mean_y':str(C[1]),'central_triangle_mean_y':str(Cneg[1]),'no_numeric_sampling':True,'sympy_version':s.__version__,'runtime_library_path':str(V),'imports_no_preparer_submitted_candidate_sibling_checker':True,'finite_controls_do_not_replace_analytic_all_period_proof':True,'checks':checks}
(O/'BOUNDARY_ALGEBRA_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
