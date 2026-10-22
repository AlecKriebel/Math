#!/usr/bin/env python3
"""Reviewer 02 independent exact derivations. Requires SymPy 1.14.0.
No package checker or stored result is imported. Explicit checks survive -O.
"""
import hashlib, json
from pathlib import Path
import sympy as s

checks=[]
def zero(label, expr):
    
    if isinstance(expr,s.MatrixBase):
        for j,e in enumerate(expr): zero(label+'_'+str(j),e)
        return
    value=s.factor(s.together(expr))
    if value != 0:
        raise RuntimeError(label+': '+str(value))
    checks.append(label)

def det(a,b): return a[0]*b[1]-a[1]*b[0]
def shoelace(poly):
    return s.simplify(sum(det(poly[j],poly[(j+1)%len(poly)]) for j in range(len(poly)))/2)
def invert(poly,f):
    result=[]
    for x,y in poly:
        d=s.simplify((x-f)**2+y*y)
        if d.is_positive is not True: raise RuntimeError('nonpositive focal square')
        result.append((s.simplify(f+(x-f)/d),s.simplify(y/d)))
    return result

r,t,x=s.symbols('r t x')
U,V,W=1-2*r*t+r*t*t,1-2*t+r*t*t,1-r*t*t
# Solve all three coefficients from the rational polynomial, independently
# of the package's generic decomposition. Let d=4 h cn(v) dn(v) a2.
A,B,d=s.symbols('A B d')
H=U**2-r*V**2*x
lhs=(1-r*t*x)*(U**2+r*V*(V+2*U)*x)
bases=[H**2,2*W*U*(1-r*x)*H,r*V*(1-r*x)*(U**2+(r*V**2-2*U**2)*x)]
mat=s.Matrix([[s.expand(b).coeff(x,j) for b in bases] for j in range(3)])
y=s.Matrix([s.expand(lhs).coeff(x,j) for j in range(3)])
# Fraction-free elimination avoids numerical samples.
sol=s.solve_linear_system(mat.row_join(y),A,B,d)
lam=U*(r*r*(t**3+t**2)-5*r*t+r+2)/(2*(1-r)**2*W**3)
expectedA=(1-t)/(U-V)**2
expectedd=(V**2-U**2*t)/((U**2-r*V**2)*(U-V))
zero('coefficient_a0_solved_from_three_equations',sol[A]-expectedA)
zero('coefficient_a1_solved_from_three_equations',sol[B]-(lam-expectedA)/2)
zero('derivative_coefficient_solved_from_three_equations',sol[d]-expectedd)
zero('U_squared_minus_rV_squared',(U**2-r*V**2)-(1-r)*W**2)
zero('positive_Lambda_representation',r*r*(t**3+t**2)-5*r*t+r+2-(2*(1-r)**2+5*r*(1-r)*(1-t)+r*r*(1-t)**2*(3+t)))
zero('V_zero_local_reduction',(1-r*t*x)-((1-t)+t*(1-r*x)))

# Two independent rational parameters for circle endpoints. The tangency
# residual factorizes into a positive scalar times the advertised relation,
# except on the diagonal where a chord is not defined.
p,q=s.symbols('p q',real=True)
z=s.Matrix([(1-p*p)/(1+p*p),2*p/(1+p*p)])
w=s.Matrix([(1-q*q)/(1+q*q),2*q/(1+q*q)])
normal=s.Matrix([w[1]-z[1],z[0]-w[0]])
support=(normal.dot(z))
bilinear=3*z[0]*w[0]+6*z[1]*w[1]+2
residual=support**2-s.Rational(4,9)*normal[0]**2-s.Rational(1,9)*normal[1]**2
factor=s.factor(residual/bilinear)
zero('circle_chord_tangency_equivalence',factor-4*(p-q)**2/(9*(1+p*p)*(1+q*q)))

X,Y,L=s.symbols('X Y L',real=True)
D=9*X**2+36*Y**2
n=s.Matrix([3*X,6*Y]); Jn=s.Matrix([-6*Y,3*X]); z0=s.Matrix([X,Y])
zp=(-2*n+L*Jn)/D; zm=(-2*n-L*Jn)/D
ring=s.groebner([X*X+Y*Y-1,L*L-(D-4)],L,X,Y)
def reducezero(label,expr):
    num=s.fraction(s.cancel(expr))[0]
    rem=ring.reduce(s.expand(num))[1]
    zero(label,rem)
for label,pt in [('plus',zp),('minus',zm)]:
    reducezero('neighbor_'+label+'_on_circle',pt.dot(pt)-1)
    zero('neighbor_'+label+'_tangent_linear',n.dot(pt)+2)
reducezero('two_neighbors_mutually_tangent',3*zp[0]*zm[0]+6*zp[1]*zm[1]+2)
# Exact orientation lower bound: det(z_plus-z,z_minus-z) at one point.
orientation=s.simplify(det(zp-z0,zm-z0).subs({X:1,Y:0,L:s.sqrt(5)}))
if orientation.is_positive is not True: raise RuntimeError('base triangle orientation')
zero('central_negation_plus_neighbor',zp.subs({X:-X,Y:-Y},simultaneous=True)+zp)
zero('central_negation_minus_neighbor',zm.subs({X:-X,Y:-Y},simultaneous=True)+zm)

# General Euclidean confocal reflection identity, using only outer incidence.
px,py,vx,vy=s.symbols('px py vx vy',real=True)
refpoly=s.expand(8*vy**2+5*vx**2-(-vy*px+vx*py)**2-40*(px*vx/8+py*vy/5)**2)
refbasis=s.groebner([px**2/8+py**2/5-1],px,py,vx,vy)
zero('full_family_confocal_reflection_identity',refbasis.reduce(refpoly)[1])

P=[(2*s.sqrt(2),s.Integer(0)),(-4*s.sqrt(2)/3,s.Rational(5,3)),(-4*s.sqrt(2)/3,-s.Rational(5,3))]
M=[(-a,-b) for a,b in P]; f=s.sqrt(3)
areas=[]
for tag,poly in [('P',P),('minusP',M)]:
    for j,a in enumerate(poly):
        b=poly[(j+1)%3]; prev=poly[(j-1)%3]
        zero(tag+'_outer_'+str(j),a[0]**2/8+a[1]**2/5-1)
        l=s.Matrix([b[1]-a[1],a[0]-b[0]]); S=l.dot(s.Matrix(a))
        zero(tag+'_support_'+str(j),s.Rational(32,9)*l[0]**2+s.Rational(5,9)*l[1]**2-S**2)
        T=s.Matrix([s.Rational(32,9)*l[0]/S,s.Rational(5,9)*l[1]/S]); edge=s.Matrix(b)-s.Matrix(a)
        fraction=s.simplify((T-s.Matrix(a)).dot(edge)/edge.dot(edge))
        if not (fraction>0 and fraction<1): raise RuntimeError('contact exterior')
        for h in range(2): zero(tag+'_contact_'+str(j)+'_'+str(h),T[h]-a[h]-fraction*edge[h])
        vi=s.Matrix(a)-s.Matrix(prev); vi=vi/s.sqrt(vi.dot(vi))
        vo=edge/s.sqrt(edge.dot(edge)); normal=s.Matrix([a[0]/8,a[1]/5])
        reflected=s.simplify(vi-2*vi.dot(normal)/normal.dot(normal)*normal)
        for h in range(2): zero(tag+'_specular_'+str(j)+'_'+str(h),reflected[h]-vo[h])
    areas.append((shoelace(poly),shoelace(invert(poly,f))))
zero('P_area',areas[0][0]-50*s.sqrt(2)/9)
zero('M_area',areas[1][0]-50*s.sqrt(2)/9)
zero('P_inverse_area',areas[0][1]-(8*s.sqrt(2)-s.sqrt(3))/80)
zero('M_inverse_area',areas[1][1]-(8*s.sqrt(2)+s.sqrt(3))/80)
D12=s.simplify(shoelace(P*4)*shoelace(invert(P*4,f))-shoelace(M*4)*shoelace(invert(M*4,f)))
zero('repeated_length_12_difference',D12+20*s.sqrt(6)/9)
if D12.is_negative is not True: raise RuntimeError('difference not strictly negative')

# Direct symbolic N4 coordinates, with positive a,b parametrization.
b,rho=s.symbols('b rho',positive=True); a=b*(1+rho*rho)/(2*rho); c=b*(1-rho*rho)/(2*rho)
quad=[(0,b),(-a,0),(0,-b),(a,0)]
zero('N4_original_area',shoelace(quad)-2*a*b)
zero('N4_inverse_area',shoelace(invert(quad,c))-2/(a*b))
zero('N4_product',shoelace(quad)*shoelace(invert(quad,c))-4)
result={'schema':'pr207-reviewer02-independent-exact-v1','status':'PASS','sympy':s.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'check_count':len(checks),'chord_residual_factor':str(factor),'base_orientation':str(orientation),'length12_difference':str(D12),'scope':'Exact finite identities and connected-family algebra; universal analytic steps require the accompanying reasoned review.'}
print(json.dumps(result,indent=2,allow_nan=False))
