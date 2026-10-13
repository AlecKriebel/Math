"""Fresh exact geometry; no imports or formulas copied from submitted checkers."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import sympy as s

HERE = Path(__file__).resolve().parent
checks = []
def zero(name, x):
    val = s.factor(s.simplify(x))
    if val != 0: raise AssertionError((name, val))
    checks.append(name)
def positive(name, x):
    val = s.simplify(x)
    if val.is_positive is not True: raise AssertionError((name, val))
    checks.append(name)
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return p.dot(q)
def area(points):
    return s.simplify(sum(det(points[i],points[(i+1)%len(points)]) for i in range(len(points)))/2)
def line_intersection(p,q):
    # Origin-antipedal lines: the normals are the actual original vertices.
    return s.simplify(s.Matrix([list(p),list(q)]).inv()*s.Matrix([dot(p,p),dot(q,q)]))
def constructions(points):
    pedals=[]; antip=[]
    for p,q in zip(points,points[1:]+points[:1]):
        e=q-p; n=s.Matrix([-e[1],e[0]]); h=dot(n,p)
        pedals.append(s.simplify(h*n/dot(n,n)))
        antip.append(line_intersection(p,q))
    return pedals,antip

# Local area identity is checked with six independent Cartesian symbols.
x,y,u,v,r,t=s.symbols('x y u v r t')
P=s.Matrix([x,y]); Q=s.Matrix([u,v]); R=s.Matrix([r,t])
X=line_intersection(R,P); Y=line_intersection(P,Q)
zero('local_actual_antipedal_area_identity', det(X,Y)-dot(P,P)*((dot(R,R)-dot(R,P))/det(R,P)+(dot(Q,Q)-dot(P,Q))/det(P,Q)))
edge=(dot(P,P)*(dot(Q,Q)-dot(P,Q))+dot(Q,Q)*(dot(P,P)-dot(P,Q)))/(2*det(P,Q))
F=(dot(P,P)*dot(Q,Q)-(dot(P,P)+dot(Q,Q))*dot(P,Q)/2)/det(P,Q)
zero('incident_terms_combine_into_submitted_F',edge-F)
zero('F_numerator_polarization',dot(P,P)*dot(Q,Q)-(dot(P,P)+dot(Q,Q))*dot(P,Q)/2-((dot(P,P)+dot(Q,Q))*dot(P-Q,P-Q)-(dot(P,P)-dot(Q,Q))**2)/4)

# Fresh verification of the canonical chord and foot uses formal addition
# coordinates and only the quadratic Jacobi relations, with no sampling.
S,C,D,t,cv,dv,b0,k=s.symbols('S C D t cv dv b0 k')
relations=[(C,1-S*S),(D,1-k*k*S*S),(cv,1-t*t),(dv,1-k*k*t*t),(b0,1-k*k)]
def jacobi_zero(name,expr):
    numerator=s.fraction(s.cancel(expr))[0]
    for variable,square in relations:
        numerator=s.rem(numerator,variable**2-square,variable)
    zero(name,numerator)
L=1-k*k*t*t*S*S;a=dv/cv;b=b0/cv
minus=s.Matrix([-a*(S*cv*dv-t*C*D)/L,b*(C*cv+S*t*D*dv)/L])
plus=s.Matrix([-a*(S*cv*dv+t*C*D)/L,b*(C*cv-S*t*D*dv)/L])
normal=s.Matrix([-S,C/b0])
jacobi_zero('canonical_chord_first_endpoint_on_actual_caustic_tangent',dot(normal,minus)-1)
jacobi_zero('canonical_chord_second_endpoint_on_actual_caustic_tangent',dot(normal,plus)-1)
jacobi_zero('canonical_chord_determinant',det(minus,plus)-2*a*b*t*cv*D/L)
jacobi_zero('canonical_confocality',a*a-b*b-k*k)
q=normal/dot(normal,normal)
qclaimed=s.Matrix([-b0*b0*S/(D*D),b0*C/(D*D)])
jacobi_zero('canonical_origin_foot_x',q[0]-qclaimed[0])
jacobi_zero('canonical_origin_foot_y',q[1]-qclaimed[1])
jacobi_zero('real_normal_angular_velocity',det(normal,s.Matrix([-C*D,-S*D/b0]))-D/b0)

def trajectory(name, points, aa,bb,ca,cb):
    n=len(points)
    positive(name+'_strict_caustic_minor',cb)
    positive(name+'_strict_outer_caustic_gap',bb-cb)
    zero(name+'_confocal',aa-ca-bb+cb)
    for j,p in enumerate(points):
        q=points[(j+1)%n]; prev=points[(j-1)%n]
        zero(f'{name}_outer_{j}',p[0]**2/aa+p[1]**2/bb-1)
        positive(f'{name}_angular_step_{j}',det(p,q))
        e=q-p; normal=s.Matrix([-e[1],e[0]]); h=dot(normal,p)
        zero(f'{name}_tangent_{j}',ca*normal[0]**2+cb*normal[1]**2-h**2)
        contact=s.Matrix([ca*normal[0]/h,cb*normal[1]/h])
        rho=s.simplify(dot(contact-p,e)/dot(e,e))
        zero(f'{name}_contact_on_segment_{j}',det(contact-p,e))
        positive(f'{name}_contact_inside_left_{j}',rho)
        positive(f'{name}_contact_inside_right_{j}',1-rho)
        nu=s.Matrix([p[0]/aa,p[1]/bb]); incoming=p-prev
        reflected=s.simplify(incoming-2*dot(incoming,nu)/dot(nu,nu)*nu)
        zero(f'{name}_reflection_parallel_{j}',det(reflected,e))
        positive(f'{name}_reflection_direction_{j}',dot(reflected,e))
    for j in range(n):
        for i in range(j): positive(f'{name}_distinct_{i}_{j}',dot(points[i]-points[j],points[i]-points[j]))
    pedal,antip=constructions(points)
    for j,p in enumerate(points):
        q=points[(j+1)%n]; foot=pedal[j]; corner=antip[j]
        zero(f'{name}_foot_actual_line_{j}',det(foot-p,q-p))
        zero(f'{name}_foot_actual_perpendicular_{j}',dot(foot,q-p))
        zero(f'{name}_antipedal_actual_first_line_{j}',dot(p,corner)-dot(p,p))
        zero(f'{name}_antipedal_actual_second_line_{j}',dot(q,corner)-dot(q,q))
        positive(f'{name}_pedal_edge_positive_{j}',det(pedal[j],pedal[(j+1)%n]))
    ap=area(pedal); au=area(antip)
    rev=points[::-1]; ar,ur=constructions(rev)
    zero(name+'_reverse_pedal',area(ar)+ap)
    zero(name+'_reverse_antipedal',area(ur)+au)
    zero(name+'_reverse_product',area(ar)*area(ur)-ap*au)
    repeated=points*3; rp,ru=constructions(repeated)
    zero(name+'_repeat_pedal',area(rp)-3*ap)
    zero(name+'_repeat_antipedal',area(ru)-3*au)
    zero(name+'_repeat_product',area(rp)*area(ru)-9*ap*au)
    return {'least_period':n,'outer_axes_squared':[str(aa),str(bb)],'caustic_axes_squared':[str(ca),str(cb)],'vertices':[[str(c) for c in p] for p in points],'original_area':str(area(points)),'origin_pedal_area':str(ap),'origin_antipedal_area':str(au),'product':str(s.simplify(ap*au))}

sq=s.sqrt
tri_top=[s.Matrix([0,sq(5)]),s.Matrix([-s.Rational(8,3),-sq(5)/3]),s.Matrix([s.Rational(8,3),-sq(5)/3])]
tri_side=[s.Matrix([2*sq(2),0]),s.Matrix([-4*sq(2)/3,s.Rational(5,3)]),s.Matrix([-4*sq(2)/3,-s.Rational(5,3)])]
triangles=[trajectory('triangle_top',tri_top,s.Integer(8),s.Integer(5),s.Rational(32,9),s.Rational(5,9)),trajectory('triangle_side',tri_side,s.Integer(8),s.Integer(5),s.Rational(32,9),s.Rational(5,9))]
zero('noncircular_N3_same_caustic_equal_product',s.sympify(triangles[0]['product'])-s.sympify(triangles[1]['product']))

diamond=[s.Matrix([sq(5),0]),s.Matrix([0,sq(3)]),s.Matrix([-sq(5),0]),s.Matrix([0,-sq(3)])]
al=s.sqrt(s.Rational(25,8)); be=s.sqrt(s.Rational(9,8))
rectangle=[s.Matrix([al,be]),s.Matrix([-al,be]),s.Matrix([-al,-be]),s.Matrix([al,-be])]
even=[trajectory('even_diamond',diamond,s.Integer(5),s.Integer(3),s.Rational(25,8),s.Rational(9,8)),trajectory('even_rectangle',rectangle,s.Integer(5),s.Integer(3),s.Rational(25,8),s.Rational(9,8))]
zero('excluded_N4_diamond_product',s.sympify(even[0]['product'])-s.Rational(225,4))
zero('excluded_N4_rectangle_product',s.sympify(even[1]['product'])-s.Rational(289,4))
positive('excluded_N4_unequal_products',s.sympify(even[1]['product'])-s.sympify(even[0]['product']))

# Circle R=2, equilateral triangle, lambda=3 and radius-one strict caustic.
circle=[s.Matrix([2,0]),s.Matrix([-1,sq(3)]),s.Matrix([-1,-sq(3)])]
cir=trajectory('circle_N3',circle,s.Integer(4),s.Integer(4),s.Integer(1),s.Integer(1))
zero('circle_N3_formula',s.sympify(cir['product'])-s.Rational(27,1))

# Complete elementary parity/lattice controls are proof consequences, not a
# finite-period replacement for the universal argument.
import math
controls=0
for n in range(3,202,2):
    for tau in range(1,(n+1)//2):
        if math.gcd(n,tau)!=1: continue
        assert len({(2*tau*j)%n for j in range(n)})==n
        assert (2*tau+n)%2==1
        assert tau%n in {(2*tau*j)%n for j in range(n)}
        controls+=1

data={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'symbolic_and_exact_checks':len(checks),'checks':checks,'primitive_odd_lattice_controls':controls,'noncircular_N3':triangles,'excluded_N4_same_caustic_counterexample':even,'circle_N3':cir,'diagnostic_scope':'Exact constructions corroborate the geometry and domain; universal invariance is audited separately by proof.'}
out=HERE/'CARTESIAN_EXACT_CHECKS.json'; out.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'status':data['status'],'exact_checks':len(checks),'lattice_controls':controls,'triangular_product':triangles[0]['product'],'excluded_N4_products':[x['product'] for x in even],'receipt_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
