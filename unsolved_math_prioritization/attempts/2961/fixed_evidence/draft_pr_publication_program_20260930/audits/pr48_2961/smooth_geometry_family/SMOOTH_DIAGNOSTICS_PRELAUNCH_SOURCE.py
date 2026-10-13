"""Independent smooth-parameter and boundary diagnostics; not a geometry proof."""
import sympy as s, json, collections, itertools, fractions
assert __debug__
checks=collections.Counter()
def check(v,name):
 assert bool(v),name
 checks[name]+=1
t,u,c=s.symbols('t u c',real=True)
def P(v):return s.Matrix([[1+v**4,v],[v**3,1]])
# Determinant-one matrices define genuine smooth diffeomorphisms of RP1.
check(s.expand(P(t).det())==1,'RP1_family_det_one')
check(P(0)==s.eye(2),'RP1_family_initial_identity')
check(s.expand((P(t+u)-P(t)*P(u))[0,1])!=0,'RP1_family_not_one_parameter')
a=P(t*c);b=P(t)*a.inv()
check(s.simplify(b*a)==P(t),'cutoff_factorization_exact')
check(s.simplify(b.inv()*b)==s.eye(2),'second_cutoff_inverse')
check(s.simplify(a.inv()*a)==s.eye(2),'first_cutoff_inverse')
check(a.subs(c,0)==s.eye(2),'a_identity_on_zero_plateau')
check(s.simplify(b.subs(c,1))==s.eye(2),'b_identity_on_one_plateau')
check(a.subs(t,0)==s.eye(2),'a_initial_identity')
check(s.simplify(b.subs(t,0))==s.eye(2),'b_initial_identity')
check(s.simplify(b.subs(t,1)*a.subs(t,1))==P(1),'endpoint_product_order')
check(s.simplify(a.subs(t,1)*b.subs(t,1)-P(1))!=s.zeros(2),'reversed_endpoint_order_negative')
wrong=P(t*(1-c))
check(s.simplify(wrong*a-P(t))!=s.zeros(2),'one_parameter_subtraction_negative')
# Independent derivation in angular coordinates for the sphere cutoff.
phi,z=s.symbols('phi z',real=True)
x=s.sqrt(1-z*z)*s.cos(phi);y=s.sqrt(1-z*z)*s.sin(phi)
tau=s.simplify((1+2*x*y)/2)
phi_new=phi+tau
angle_jac=s.simplify(s.diff(phi_new,phi))
check(s.simplify(angle_jac.subs({phi:s.pi/2,z:0}))==0,'rotation_cutoff_zero_angular_derivative')
check(s.simplify(s.diff(phi_new,z).subs({phi:s.pi/2,z:0}))==0,'rotation_cutoff_cross_derivative_zero')
check(s.Matrix([[angle_jac,s.diff(phi_new,z)],[0,1]]).subs({phi:s.pi/2,z:0}).rank()==1,'rotation_cutoff_tangent_rank_one')
# Exact finite chart packing certificates are diagnostics for the written local-flow proof.
for dim in range(1,7):
 for n in [1,2,3,8,31]:
  rad=fractions.Fraction(1,4*n)
  centers=[fractions.Fraction(-1,2)+fractions.Fraction(2*i+1,2*n) for i in range(n)]
  check(all(abs(x)+rad<1 for x in centers),'chart_ball_inside_larger_chart')
  check(all(abs(x-y)>2*rad for x,y in itertools.combinations(centers,2)),'chart_ball_pairwise_disjoint')
  # Smooth contraction can be any positive scale; zero scale would not be a diffeomorphism.
  check(rad**dim>0,'local_contraction_positive_jacobian')
# Compact corridor translation margins: every straight trajectory stays inside the chosen compact rectangle.
for m in [1,2,4,9,25]:
 R=fractions.Fraction(3,2);L=4
 check(L>2*R,'strict_disk_displacement_distance')
 check(all(abs(i*L-j*L)>2*R for i,j in itertools.combinations(range(m+1),2)),'iterated_disk_disjointness')
 for t0 in [fractions.Fraction(0),fractions.Fraction(1,3),fractions.Fraction(m)]:
  check(-R-1 < -R+L*t0 <= R+L*t0 < L*m+R+1,'full_translation_trajectory_corridor_margin')
print(json.dumps({'schema':'pr48-smooth-geometry-independent-exact-diagnostics/v1','status':'PASS','assertions':sum(checks.values()),'checks':dict(checks),'sympy_version':s.__version__,'scope':'Exact parameter, derivative and packing diagnostics only; the written smooth support proofs and cited perfectness inputs remain necessary. No full four-dimensional result or novelty claimed.'},indent=2))
