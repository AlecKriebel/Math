"""Independent definitions/identity checks; no assert statements; source-family audit."""
import sys
from pathlib import Path
import sympy as s

checks = 0

def require(condition, label):
    global checks
    if not condition:
        raise RuntimeError(label)
    checks += 1

def eq(x, y, label):
    require(s.simplify(x-y) == 0, label)

def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def area(points): return s.simplify(sum(cross(p,q) for p,q in zip(points, points[1:]+points[:1]))/2)
def outer(points,a,b):
    result=[]
    for p,q in zip(points,points[1:]+points[:1]):
        matrix=s.Matrix([[p[0]/a**2,p[1]/b**2],[q[0]/a**2,q[1]/b**2]])
        require(s.simplify(matrix.det())!=0, 'parallel tangents excluded')
        result.append(tuple((matrix.inv()*s.ones(2,1)).applyfunc(s.simplify)))
    return result

def pedal(points,a,b,M):
    result=[]
    for p in points:
        n=s.Matrix([p[0]/a**2,p[1]/b**2]); d=n.dot(n)
        require(s.simplify(d)>0, 'real projection denominator positive')
        q=s.Matrix(M)+(1-n.dot(s.Matrix(M)))*n/d
        eq(n.dot(q),1,'foot belongs to tangent')
        eq(cross(q-s.Matrix(M),n),0,'foot displacement parallel to normal')
        result.append(tuple(q.applyfunc(s.simplify)))
    return result

# A single pair of support lines and their local area contribution.
h,k,c,t=s.symbols('h k c t', nonzero=True, real=True)
# c=cos Delta, t=sin Delta; avoid trigonometric assumptions by c^2+t^2=1.
v=s.Matrix([h,(k-c*h)/t]); u=s.Matrix([(h-c*k)/t, k])
# Each edge's outgoing/incoming tangent-coordinate contributions combine to this.
eq((h*(k-h*c)+k*(h-k*c))/(2*t), (h*k-(h*h+k*k)*c/2)/t,'outer support-pair formula')

# Exact telescoping of the anisotropic part of pedal quadratic coefficients.
p,q=s.symbols('p q', real=True)
for expr in [s.sin(q-p)*s.cos(p+q)-(s.sin(2*q)-s.sin(2*p))/2,
             s.sin(q-p)*s.sin(p+q)-(s.cos(2*p)-s.cos(2*q))/2]:
    require(s.trigsimp(s.expand_trig(expr))==0,'quadratic anisotropy telescopes')

# Distinct exact six-period controls, rebuilt directly from the definitions.
a=s.Integer(2); b=s.Integer(1); lam=s.Rational(4,9)
H=[(2,0),(s.Rational(4,3),s.sqrt(5)/3),(-s.Rational(4,3),s.sqrt(5)/3),(-2,0),(-s.Rational(4,3),-s.sqrt(5)/3),(s.Rational(4,3),-s.sqrt(5)/3)]
V=[(0,1),(-4*s.sqrt(2)/3,s.Rational(1,3)),(-4*s.sqrt(2)/3,-s.Rational(1,3)),(0,-1),(4*s.sqrt(2)/3,-s.Rational(1,3)),(4*s.sqrt(2)/3,s.Rational(1,3))]
u,v=s.symbols('u v',real=True)
for name,P in [('H',H),('V',V)]:
    P=[tuple(map(s.sympify,p)) for p in P]
    for p,q in zip(P,P[1:]+P[:1]):
        eq(p[0]**2/a**2+p[1]**2/b**2,1,'ellipse membership')
        # Chord coefficient normal ell, normalized ell dot p=1.
        ell=s.Matrix([[p[0],p[1]],[q[0],q[1]]]).inv()*s.ones(2,1)
        eq((a*a-lam)*ell[0]**2+(b*b-lam)*ell[1]**2,1,'chord caustic tangency')
    A=area(P); Ap=area(outer(P,a,b)); BM=area(pedal(P,a,b,(u,v)))
    eq(BM/A,(u*u+v*v+9)/8,'six-period direct B/A formula')
    eq(Ap*BM,40*(u*u+v*v+9)/9,'six-period direct product')
    eq(area(pedal(P,a,b,(-u,-v))),BM,'central pedal dependence even in M')
    print(name, 'A =',A, 'A_prime =',Ap, 'B_M =',s.factor(BM), 'product =',s.factor(Ap*BM))

# Exact odd-period repetition boundary: two primitive triangles, then traverse twice.
# The source table itself does not explicitly print the word primitive.
lam3=4*(2*s.sqrt(13)-5)/9
alpha=2*(s.sqrt(13)-1)/3; beta=(4-s.sqrt(13))/3
gamma=s.sqrt(2*s.sqrt(13)-5)
triangles=[[(2,0),(-alpha,gamma/3),(-alpha,-gamma/3)],
           [(0,1),(-4*gamma/3,-beta),(4*gamma/3,-beta)]]
products=[]
for P in triangles:
    P=[tuple(map(s.sympify,p)) for p in P]
    for p,q in zip(P,P[1:]+P[:1]):
        eq(p[0]**2/4+p[1]**2,1,'triangle ellipse membership')
        ell=s.Matrix([[p[0],p[1]],[q[0],q[1]]]).inv()*s.ones(2,1)
        eq((4-lam3)*ell[0]**2+(1-lam3)*ell[1]**2,1,'triangle caustic tangency')
    AP=area(outer(P,a,b)); BM=area(pedal(P,a,b,(1,0)))
    products.append(s.simplify(4*AP*BM))
difference=s.simplify(products[0]-products[1])
require(difference.is_positive is True,'exact positive repeated-orbit counterexample difference')
print('Twice-traversed triangle products at M=(1,0):')
for value in products: print(s.N(value,35), '; exact =',s.simplify(value))
print('difference =',s.N(products[0]-products[1],35))
print('Exact explicit checks passed:',checks)
