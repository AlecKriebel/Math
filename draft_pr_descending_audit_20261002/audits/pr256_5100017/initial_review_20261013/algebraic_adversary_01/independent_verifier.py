"""Independent Laurent algebra plus Cartesian signed-shoelace falsifiers.

Does not import, execute, or read the submitted verifier.  Numeric families are
obtained by explicit inner-ellipse tangents and bisection, not Jacobi sampling.
"""
from __future__ import annotations
import json, math, sys
from datetime import datetime, timezone
from pathlib import Path
import sympy as s
import mpmath as mp

HERE = Path(__file__).resolve().parent
CHECKS = []

def zero(expression, name):
    result = s.factor(s.cancel(s.together(expression)))
    assert result == 0, (name, result)
    CHECKS.append(name)

def check(condition, name):
    assert condition, name
    CHECKS.append(name)

I = s.I
A, B, L = s.symbols('A B L', positive=True)
H, E, D = s.symbols('H E D', real=True)
d = 1-L/A-L/B
F = (A+B)*d/2+2*L
e = (A-B)/2
# Derive equation (5) from the chord identity in eccentric angles.
left_coeff_x = A*(1+L/A-L/B)
left_coeff_y = B*(1-L/A+L/B)
zero(left_coeff_x-(F+e*d), 'bilinear_x_coefficient')
zero(left_coeff_y-(F-e*d), 'bilinear_y_coefficient')
zero(F+e*d-(A-L*(A/B-1)), 'denominator_factor_plus')
zero(F-e*d-(B+L*(1-B/A)), 'denominator_factor_minus')

# Independent unit-circle Laurent arithmetic: formal conjugation sends x->1/x.
x, y, h, k, t, tb = s.symbols('x y h k t tb', nonzero=True)
def conj(expr):
    return s.expand(expr).xreplace({x:1/x, y:1/y, t:tb, tb:t, I:-I})
def cross(p, q):
    return s.expand((conj(p)*q-p*conj(q))/(2*I))
Z, W = x*x, y*y
delta_cos = (y/x+x/y)/2
sigma_cos = (x*y+1/(x*y))/2
hx = H+E*(x*x+x**-2)/2
hy = H+E*(y*y+y**-2)/2
hh = D*delta_cos+E*sigma_cos
zero(hx*hy-hh**2-(H**2-E**2-(D**2-E**2)*delta_cos**2
     +2*E*(H-D)*sigma_cos*delta_cos), 'squared_support_identity')
# This establishes equation (7) after hx*hy=hh^2.
zero(2*sigma_cos*delta_cos-(Z+1/Z+W+1/W)/2,
     'doubled_normal_cosine_sum')
zero(cross(Z,W)*(Z+W)+I*(1+(W/Z+Z/W)/2)*(W-Z),
     'cyclic_lemma_edge_identity')
# Remaining lemma term has cross + endpoint coboundary in its imaginary part.
Xi, Yi, Xj, Yj = s.symbols('Xi Yi Xj Yj', real=True)
zero((Xi+Xj)*(Yj-Yi)-(Xi*Yj-Xj*Yi)-(Xj*Yj-Xi*Yi),
     'cyclic_lemma_second_telescope')
zero(hh*cross(x,y)-D*cross(Z,W)/2
     -E*(y*y-x*x+x**-2-y**-2)/(4*I), 'origin_area_coboundary')

# Extract surviving terms from scratch, as half the antipodal pair contribution.
p, q = h*x-t*Z, k*y-t*W
ap, aq = -h*x-t*Z, -k*y-t*W
paired_area = s.expand((cross(p,q)+cross(ap,aq))/2)
zero(paired_area-h*k*cross(x,y)-t*tb*cross(Z,W),
     'antipodal_area_all_terms')
paired_moment = s.expand((cross(p,q)*(p+q)+cross(ap,aq)*(ap+aq))/2)
poly = s.Poly(paired_moment, t, tb)
check(set(poly.monoms()) == {(1,0),(0,1),(2,1)},
      'antipodal_moment_only_two_linear_and_one_cubic_terms')
linear_t = s.expand(2*I*poly.coeff_monomial(t))
linear_tb = s.expand(2*I*poly.coeff_monomial(tb))
substitution = {h*h:hx, k*k:hy, h*k:hh}
linear_t = s.expand(linear_t).subs(substitution, simultaneous=True)
linear_tb = s.expand(linear_tb).subs(substitution, simultaneous=True)
R = Z/W-W/Z
U = Z*Z/W-W*W/Z
zero(linear_t-D*U-3*E*R/2-(D+H)*(Z-W)-E*(Z*Z-W*W),
     'first_linear_coefficient_exact_coboundary')
zero(linear_tb-(D/2+H)*R-E*U/2-E*(Z-W)/2-E*(1/W-1/Z),
     'second_linear_coefficient_exact_coboundary')
zero(poly.coeff_monomial(t*t*tb)+cross(Z,W)*(Z+W),
     'cubic_coefficient_exact')
zero(U+2*I*cross(Z,W)*(Z+W)-(W-Z), 'R2_moment_telescope')

# Resulting aggregate moment is equation (12), without presupposing a centroid.
S, v, rr, z, zb = s.symbols('S v rr z zb', real=True)
Tv = -2*S*(t*(D*v+3*E/2+v*t*tb)+tb*(D/2+H+E*v/2))
area = S*(D/2+t*tb)
centroid = z/2+Tv.subs({t:zb/2,tb:z/2}, simultaneous=True)/(6*area.subs({t:zb/2,tb:z/2}, simultaneous=True))
centroid = centroid.subs(z*zb,rr)
claim = z/2-(z*(D+2*H+E*v)+zb*(2*D*v+3*E+v*rr/2))/(3*(2*D+rr))
zero(centroid-claim, 'moment_to_centroid_formula')
# Cross multiply only the already proved nonzero common denominator, avoiding
# unnecessary expansion of a nested rational expression in the CAS.
zero(2*e*((A+B)/2-F/d)*d*d+4*e*L*d,
     'v_parameter_elimination')

def determinant(p,q):
    return p[0]*q[1]-p[1]*q[0]
def raw_area_moment(points):
    edges=[determinant(p,points[(i+1)%len(points)]) for i,p in enumerate(points)]
    return s.expand(sum(edges)/2), tuple(s.expand(sum(edges[i]*(points[i][j]+points[(i+1)%len(points)][j]) for i in range(len(points)))) for j in (0,1))

# The d=0 domain: direct unrestricted-M rectangle calculation.
aa, bb, mx, my = s.symbols('aa bb mx my', real=True)
ar, moments = raw_area_moment([(aa,my),(mx,bb),(-aa,my),(mx,-bb)])
zero(ar-2*aa*bb, 'N4_area_all_M')
zero(moments[0]-2*ar*mx, 'N4_x_centroid_all_M')
zero(moments[1]-2*ar*my, 'N4_y_centroid_all_M')

# Exact noncircular primitive 8/3 control: Cartesian projections for symbolic M.
A0=s.Rational(221,96); B0=s.Rational(27625,20736); L0=s.Rational(125,96)
a0,b0=s.sqrt(A0),s.sqrt(B0)
pairs=[(0,1),(-s.Rational(12,13),-s.Rational(5,13)),(1,0),(-s.Rational(12,13),s.Rational(5,13)),(0,-1),(s.Rational(12,13),s.Rational(5,13)),(-1,0),(s.Rational(12,13),-s.Rational(5,13))]
points=[(a0*u,b0*w) for u,w in pairs]
check(len(set(points))==8, 'star_eight_distinct_vertices')
check(A0>L0>0 and B0>L0, 'star_nondegenerate_elliptic_caustic')
check(A0-L0==1 and B0-L0==s.Rational(625,20736), 'star_caustic_axes_squared')
for i,P in enumerate(points):
    Q=points[(i+1)%8]; previous=points[(i-1)%8]
    edge=(Q[0]-P[0],Q[1]-P[1]); normal=(-edge[1],edge[0]); c=normal[0]*P[0]+normal[1]*P[1]
    zero(P[0]*P[0]/A0+P[1]*P[1]/B0-1, f'star_on_ellipse_{i}')
    zero(c*c-(A0-L0)*normal[0]**2-(B0-L0)*normal[1]**2, f'star_tangent_{i}')
    check(s.simplify(determinant(P,Q))>0, f'star_ccw_chord_{i}')
    incoming=s.Matrix([P[0]-previous[0],P[1]-previous[1]])
    outgoing=s.Matrix(edge)
    incoming=incoming/s.sqrt(incoming.dot(incoming)); outgoing=outgoing/s.sqrt(outgoing.dot(outgoing))
    outward=s.Matrix([P[0]/A0,P[1]/B0])
    reflected=incoming-2*incoming.dot(outward)/outward.dot(outward)*outward
    for j in (0,1):
        zero(s.simplify(reflected[j]-outgoing[j]), f'star_reflection_{i}_{j}')
d0=s.factor(d.subs({A:A0,B:B0,L:L0})); F0=s.factor(F.subs({A:A0,B:B0,L:L0}))
H0=(A0+B0)/2; e0=(A0-B0)/2
v0=s.factor(-4*e0*L0*d0/(F0*F0-e0*e0*d0*d0)); rho2=s.factor(-2*F0/d0)
check((d0,F0,v0,rho2)==(-s.Rational(120,221),s.Rational(2795,1728),s.Rational(7,13),s.Rational(123539,20736)), 'star_exact_constants')
feet=[]
for P in points:
    n=(P[0]/A0,P[1]/B0); norm=n[0]**2+n[1]**2
    offset=(1-n[0]*mx-n[1]*my)/norm
    feet.append((s.expand(s.simplify(mx+offset*n[0])),s.expand(s.simplify(my+offset*n[1]))))
star_ar, star_T=raw_area_moment(feet)
origin_ar=s.factor(star_ar.subs({mx:0,my:0}))
zero(star_ar-origin_ar*(2*F0+d0*(mx*mx+my*my))/(2*F0), 'star_area_polynomial_all_M')
zz=mx+I*my; zzb=mx-I*my; G0=2*F0+d0*(mx*mx+my*my)
claimed=zz/2-(zz*(F0+2*H0*d0+e0*v0*d0)+zzb*(2*F0*v0+3*e0*d0+v0*d0*(mx*mx+my*my)/2))/(3*G0)
zero(star_T[0]+I*star_T[1]-6*star_ar*claimed, 'star_moment_polynomial_all_M')
zero(star_ar.subs({mx:13*s.sqrt(731)/144,my:0}), 'star_exact_zero_area_point')
check(s.factor(star_T[0].subs({mx:13*s.sqrt(731)/144,my:0}))!=0, 'star_zero_area_point_nonzero_first_moment')
(HERE/'EXACT_CHECKPOINT.json').write_text(json.dumps({
    'status':'PASS', 'timestamp_utc':datetime.now(timezone.utc).isoformat(),
    'exact_checks':CHECKS, 'count':len(CHECKS),
    'star_radius_squared':str(rho2), 'star_area_polynomial':str(s.factor(star_ar)),
    'star_x_moment_polynomial':str(s.factor(star_T[0])),
    'star_y_moment_polynomial':str(s.factor(star_T[1]))}, indent=2)+'\n')

# Independent geometric period generator, all arithmetic below double precision.
def step(P,a,b,lam):
    ac,bc=math.sqrt(a*a-lam),math.sqrt(b*b-lam)
    Y=(P[0]/ac,P[1]/bc); r2=Y[0]*Y[0]+Y[1]*Y[1]; root=math.sqrt(r2-1)
    choices=[]
    for sign in (-1,1):
        U=((Y[0]-sign*Y[1]*root)/r2,(Y[1]+sign*Y[0]*root)/r2)
        direction=(ac*U[0]-P[0],bc*U[1]-P[1])
        if determinant(P,direction)>0:
            den=direction[0]**2/(a*a)+direction[1]**2/(b*b)
            distance=-2*(P[0]*direction[0]/(a*a)+P[1]*direction[1]/(b*b))/den
            choices.append((P[0]+distance*direction[0],P[1]+distance*direction[1]))
    assert len(choices)==1
    return choices[0]

def orbit(a,b,lam,N,phase):
    points=[(a*math.cos(phase),b*math.sin(phase))]
    for _ in range(N): points.append(step(points[-1],a,b,lam))
    return points

def winding_sum(points):
    return math.fsum(math.atan2(determinant(p,q),p[0]*q[0]+p[1]*q[1]) for p,q in zip(points,points[1:]))

def tune(a,b,N,k):
    if N==4: return a*a*b*b/(a*a+b*b)
    lower=1e-10*b*b; upper=(1-1e-10)*b*b
    for _ in range(60):
        mid=(lower+upper)/2
        if winding_sum(orbit(a,b,mid,N,0))<2*math.pi*k: lower=mid
        else: upper=mid
    return (lower+upper)/2

# Near a degenerate caustic, bisection in double precision is not reliable.
# Generate every tested family with 90-digit arithmetic, then independently
# evaluate Cartesian projection/moment diagnostics in ordinary floating arithmetic.
mp.mp.dps=90
def mp_step(P,a,b,lam):
    ac,bc=mp.sqrt(a*a-lam),mp.sqrt(b*b-lam)
    Y=(P[0]/ac,P[1]/bc); r2=Y[0]*Y[0]+Y[1]*Y[1]; root=mp.sqrt(r2-1)
    for sign in (-1,1):
        U=((Y[0]-sign*Y[1]*root)/r2,(Y[1]+sign*Y[0]*root)/r2)
        direction=(ac*U[0]-P[0],bc*U[1]-P[1])
        if determinant(P,direction)>0:
            den=direction[0]**2/(a*a)+direction[1]**2/(b*b)
            distance=-2*(P[0]*direction[0]/(a*a)+P[1]*direction[1]/(b*b))/den
            return (P[0]+distance*direction[0],P[1]+distance*direction[1])
    raise AssertionError('no_ccw_mp_tangent')
def mp_orbit(a,b,lam,N,phase):
    points=[(a*mp.cos(phase),b*mp.sin(phase))]
    for _ in range(N): points.append(mp_step(points[-1],a,b,lam))
    return points
def mp_tune(a,b,N,k):
    aa,bb=mp.mpf(str(a)),mp.mpf(str(b)); lower=mp.mpf('1e-60')*bb*bb; upper=(1-mp.mpf('1e-60'))*bb*bb
    for _ in range(160):
        mid=(lower+upper)/2; pts=mp_orbit(aa,bb,mid,N,mp.mpf(0))
        angle=mp.fsum(mp.atan2(determinant(p,q),p[0]*q[0]+p[1]*q[1]) for p,q in zip(pts,pts[1:]))
        if angle<2*mp.pi*k: lower=mid
        else: upper=mid
    return (lower+upper)/2

def am_float(points):
    edges=[determinant(p,points[(i+1)%len(points)]) for i,p in enumerate(points)]
    area=math.fsum(edges)/2
    moment=tuple(math.fsum(edges[i]*(points[i][j]+points[(i+1)%len(points)][j]) for i in range(len(points))) for j in (0,1))
    return area,moment

WORST={key:0. for key in ('closure','reflection','antipodal','area','moment','orientation_reversal','scale')}
def near(value,key,case,tolerance=2e-8):
    value=abs(float(value)); WORST[key]=max(WORST[key],value)
    assert value<tolerance, (key,value,case)

family_count=0; phase_count=0; pedal_count=0; singular_count=0; high_precision_families=[]
for ratio in (1.01,1.7,4.3):
    a,b=ratio,1.
    for N in range(4,31,2):
        for winding in range(1,N//2):
            if math.gcd(N,winding)!=1: continue
            high_precision=True
            if N==4:
                mp_lam=mp.mpf(str(a))**2*mp.mpf(str(b))**2/(mp.mpf(str(a))**2+mp.mpf(str(b))**2)
            else:
                mp_lam=mp_tune(a,b,N,winding)
            lam=float(mp_lam)
            if (mp.mpf(str(b))**2-mp_lam)<mp.mpf('1e-8'):
                high_precision_families.append({'ratio':ratio,'N':N,'winding':winding,'caustic_gap':str(mp.mpf(str(b))**2-mp_lam)})
            hh=(a*a+b*b)/2; ee=(a*a-b*b)/2; dd=1-lam/a**2-lam/b**2
            ff=hh*dd+2*lam; vv=-4*ee*lam*dd/(ff*ff-ee*ee*dd*dd)
            if N==4: dd=0.; vv=0.
            family_count+=1
            for phase in (0.,.317,1.171,2.429):
                case=(ratio,N,winding,phase)
                if high_precision:
                    full=[tuple(map(float,p)) for p in mp_orbit(mp.mpf(str(a)),mp.mpf(str(b)),mp_lam,N,mp.mpf(str(phase)))]
                else:
                    full=orbit(a,b,lam,N,phase)
                P=full[:-1]
                near(math.dist(full[-1],full[0])/(1+a+b),'closure',case)
                phase_count+=1
                for i,p0 in enumerate(P):
                    opp=P[(i+N//2)%N]
                    near(math.hypot(p0[0]+opp[0],p0[1]+opp[1])/(1+a+b),'antipodal',case)
                    prev=P[(i-1)%N]; nxt=P[(i+1)%N]
                    inc=(p0[0]-prev[0],p0[1]-prev[1]); out=(nxt[0]-p0[0],nxt[1]-p0[1])
                    il=math.hypot(*inc); ol=math.hypot(*out); inc=(inc[0]/il,inc[1]/il); out=(out[0]/ol,out[1]/ol)
                    nn=(p0[0]/(a*a),p0[1]/(b*b)); n2=nn[0]**2+nn[1]**2
                    prod=inc[0]*nn[0]+inc[1]*nn[1]
                    reflected=(inc[0]-2*prod*nn[0]/n2,inc[1]-2*prod*nn[1]/n2)
                    near(math.dist(reflected,out),'reflection',case)
                def feet(M,scale=1.):
                    Q=[]
                    for p0 in P:
                        # Tangent equation in unnormalized coordinates.
                        nn=(p0[0]/(a*a*scale),p0[1]/(b*b*scale)); n2=nn[0]**2+nn[1]**2
                        factor=(1-nn[0]*M[0]-nn[1]*M[1])/n2
                        Q.append((M[0]+factor*nn[0],M[1]+factor*nn[1]))
                    return Q
                S0,_=am_float(feet((0.,0.)))
                assert S0>0
                Ms=[(0.,0.),(.71,-.43),(2.3,1.7),(-5.,3.)]
                if dd<0: Ms.append((math.sqrt(-2*ff/dd),0.))
                for M in Ms:
                    zz=complex(*M); radius=abs(zz)**2; gg=2*ff+dd*radius
                    Q=feet(M); area_num,moment_num=am_float(Q)
                    near((area_num-S0*gg/(2*ff))/(1+abs(S0)+abs(area_num)),'area',case)
                    # Multiply denominator out: valid check even on the zero locus.
                    numerator=zz*(ff+2*hh*dd+ee*vv*dd)+zz.conjugate()*(2*ff*vv+3*ee*dd+vv*dd*radius/2)
                    predicted_moment=S0/ff*(3*gg*zz/2-numerator)
                    observed_moment=complex(*moment_num)
                    near((observed_moment-predicted_moment).__abs__()/(1+abs(observed_moment)+abs(predicted_moment)),'moment',case)
                    rev_area,rev_moment=am_float(list(reversed(Q)))
                    near((rev_area+area_num)/(1+abs(area_num)),'orientation_reversal',case)
                    for j in (0,1): near((rev_moment[j]+moment_num[j])/(1+abs(moment_num[j])),'orientation_reversal',case)
                    scaled_area,scaled_moment=am_float(feet((M[0]*3.7,M[1]*3.7),3.7))
                    near((scaled_area-3.7**2*area_num)/(1+abs(scaled_area)),'scale',case)
                    for j in (0,1): near((scaled_moment[j]-3.7**3*moment_num[j])/(1+abs(scaled_moment[j])),'scale',case)
                    pedal_count+=1
                    singular_count+=abs(gg)<1e-9

result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'python':sys.version,'sympy':s.__version__,'exact_checks':CHECKS,
        'exact_star':{'a_squared':str(A0),'b_squared':str(B0),'lambda':str(L0),
                      'd':str(d0),'F':str(F0),'v':str(v0),'radius_squared':str(rho2),
                      'origin_signed_area':str(origin_ar),
                      'area_polynomial':str(s.factor(star_ar)),
                      'x_moment_polynomial':str(s.factor(star_T[0])),
                      'y_moment_polynomial':str(s.factor(star_T[1]))},
        'numeric':{'families':family_count,'phases':phase_count,'pedal_cases':pedal_count,
                   'zero_area_cases':singular_count,'max_normalized_residuals':WORST,
                   'high_precision_families':high_precision_families,
                   'generation_precision_decimal_digits':mp.mp.dps,
                   'generator':'Explicit inner-ellipse tangent contact, second outer-ellipse intersection, and caustic-parameter bisection; no elliptic-function sampling.'}}
(HERE/'INDEPENDENT_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
