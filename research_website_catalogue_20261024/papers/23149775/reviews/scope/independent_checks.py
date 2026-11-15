"""Owned exact checks; no deposited code imported. Run with shared SymPy 1.14."""
import sympy as s
import json
t=s.symbols('t',positive=True)
a,f=s.symbols('a f',real=True)
d=2*t+1
A2=t*(t+2)/d
records=[]
def red(x):
    num,den=s.together(x).as_numer_denom()
    for v,relation in [(f,f*f-(A2-1)),(a,a*a-A2)]:
        num=s.rem(s.Poly(num,v),s.Poly(relation,v)).as_expr()
    return s.factor(num),s.factor(den)
def ck(name,x):
    r,den=red(x)
    records.append({'name':name,'residual':str(r),'denominator_before_reduction':str(den)})
    if r!=0:raise RuntimeError((name,r))
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def area(v):return sum(det(v[i],v[(i+1)%len(v)]) for i in range(len(v)))/2
def foot(n,h,F):
    q=(h-n.dot(F))/n.dot(n)
    return F+q*n
# Work with y scaled by sqrt(d): Euclidean projection retains the factor.
root=s.sqrt(d)
P=[s.Matrix([a,0]),s.Matrix([-a*t/(t+1),root/(t+1)]),s.Matrix([-a*t/(t+1),-root/(t+1)])]
V=[s.Matrix([a,root]),s.Matrix([-a*(t+1)/t,0]),s.Matrix([a,-root])]
side_normals=[s.Matrix([1/a,root]),s.Matrix([1,0]),s.Matrix([1/a,-root])]
side_h=[1,-a*t/(t+1),1]
tangent_normals=[s.Matrix([1,0]),s.Matrix([-t/a,root]),s.Matrix([-t/a,-root])]
tangent_h=[a,t+1,t+1]
for i,p in enumerate(P):ck('boundary_'+str(i),p[0]**2/A2+p[1]**2-1)
for i in range(3):
    for j in [i,(i+1)%3]:ck('side_incidence_'+str(i)+'_'+str(j),side_normals[i].dot(P[j])-side_h[i])
    for j in [i,(i+1)%3]:ck('outer_incidence_'+str(i)+'_'+str(j),tangent_normals[j].dot(V[i])-tangent_h[j])
ck('outer_to_original_area',area(V)/area(P)-(t+1)**2/t)
o=(A2-1)/(2*a*(t+1));h=(t*t-A2)/(2*a*t)
R2=(a-o)**2;RE2=(a-h)**2+d
ck('synchronized_centers',h-2*(t+1)*o)
ck('radius_factor',RE2-4*R2)
for sign in [-1,1]:
    F=s.Matrix([sign*f,0])
    pedal=area([foot(n,H,F) for n,H in zip(side_normals,side_h)])
    outer=area([foot(n,H,F) for n,H in zip(tangent_normals,tangent_h)])
    power=R2-(sign*f-o)**2;powerE=RE2-(sign*f-h)**2
    ck('focal_power_factor_'+str(sign),powerE-2*(t+1)*power)
    ck('Querret_original_'+str(sign),pedal-area(P)*power/(4*R2))
    ck('Querret_outer_'+str(sign),outer-area(V)*powerE/(4*RE2))
    ck('all_t_multiplier_'+str(sign),outer-(t+1)**3/(2*t)*pedal)
ck('D_expression',((t*t+t+1)/d)**2-A2*A2+A2-1)
ck('t_inverse',(((t*t+t+1)/d)-1)/(A2-(t*t+t+1)/d)-t)
ck('circle_multiplier_limit',s.limit((t+1)**3/(2*t),t,1)-4)
# Independently check the all-phase locus/Euler elimination, retaining its
# classical theorem assumptions explicitly rather than inferring phase from shape.
D=(t*t+t+1)/d;n=A2-D;m=D-1;q=A2-1;rho=2*t/(t+1)**2
ix2,ox2=s.symbols('ix2 ox2',real=True)
I2=ix2+n*n*(1-A2*ix2/(m*m))
O2=ox2+m*m*(1-4*A2*ox2/(n*n))/4
alpha=1-A2*n*n/(m*m)
ck('phase_square_relation',I2+4*rho*O2-(A2+1-4*rho*D)-alpha*(ix2-4*m*m*ox2/(n*n)))
ck('alpha_positive_factor',alpha-2*(t-1)*(t+1)/(t*d))
U=D-q;V=A2+1+2*D-q
ck('phase_power_factor',V/U-2*(t+1))
ck('classical_all_phase_multiplier',V/(2*rho*U)-(t+1)**3/(2*t))
ck('focal_nonzero_margin',U*U-q*n*n/A2-d/(t*(t+2)))
# Exact note example maps to t=3/2, Y=16. Its two positive ratios differ.
ck('example_axes',A2.subs(t,s.Rational(3,2))*16-21)
ck('example_multiplier',((t+1)**3/(2*t)).subs(t,s.Rational(3,2))-s.Rational(125,24))
ratio=(7*s.sqrt(21)+s.sqrt(5))/(7*s.sqrt(21)-s.sqrt(5))
if not bool(ratio>1) or not bool(1/ratio<1):raise RuntimeError('exact ratio order')
print(json.dumps({'status':'PASS','sympy':s.__version__,'exact_zero_checks':len(records),'records':records,'exact_example_ratio':str(ratio),'independence':'No deposited modules imported. Generic axial-triangle geometry and direct Euclidean projections; t>1 with a positive square root and f^2=a^2-1. Algebraic denominator factors recorded; geometry supplies nonzero a,t,t+1,2t+1 and positive normal norms.'},indent=2))
