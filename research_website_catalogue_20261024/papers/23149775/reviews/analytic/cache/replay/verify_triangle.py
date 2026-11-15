"""Independent rational-parameter, signed-pedal, and actual triangle checks."""
import sympy as s
print('SymPy',s.__version__)
t,Y=s.symbols('t Y',positive=True)
X=Y*t*(t+2)/(2*t+1)
D=Y*(t*t+t+1)/(2*t+1)
n=X-D; m=D-Y; q=X-Y
rho=2*m*n/q**2; U=D-q; V=X+Y+2*D-q
def check(label,z):
    z=s.factor(s.cancel(z))
    print(label,':',z)
    assert z==0,(label,z)
check('D quadratic relation',D**2-X**2+X*Y-Y**2)
check('ratio m/n=t',m-t*n)
check('rho rational parameter',rho-2*t/(t+1)**2)
check('V/U=2(t+1)',V/U-2*(t+1))
M=s.factor(V/(2*rho*U))
check('M=(t+1)^3/(2t)',M-(t+1)**3/(2*t))
alpha=1-X*n**2/(Y*m**2)
check('alpha positive factorization',alpha-2*(t-1)*(t+1)/(t*(2*t+1)))
check('caustic confocality',X*m**2/q**2-Y*n**2/q**2-q)
check('caustic Cayley closure',m/q+n/q-1)
print('focal-factor minimum squared margin',s.factor(U**2-q*n**2/X))
print('M circle limit',s.limit(M,t,1,dir='+'))
print('M high-eccentricity normalized limit',s.limit(M/(X/Y)**2,t,s.oo))
assert s.limit(M,t,1,dir='+')==4
assert s.limit(M/(X/Y)**2,t,s.oo)==2

def cross(A,B): return s.det(s.Matrix.hstack(A,B))
def area(P): return s.factor(sum(cross(P[i],P[(i+1)%3]) for i in range(3))/2)
def pedal(P,Z):
    Q=[]
    for i in range(3):
        A=P[i]; B=P[(i+1)%3]; d=B-A
        Q.append(s.simplify(A+d*((Z-A).dot(d))/d.dot(d)))
    return area(Q)
# Universal signed identity independently proved in affine coordinates.
h,u,v,x,y=s.symbols('h u v x y',real=True,nonzero=True)
P=[s.Matrix([0,0]),s.Matrix([h,0]),s.Matrix([u,v])]
O=s.Matrix([h/2,(u*u+v*v-h*u)/(2*v)])
R2=O.dot(O); Z=s.Matrix([x,y])
check('universal signed triangle pedal identity',pedal(P,Z)-area(P)*(R2-(Z-O).dot(Z-O))/(4*R2))

# Actual N=3 ellipse billiard, exact squared axes (21,16).
a=s.sqrt(21); b=s.Integer(4); XX=21; YY=16; DD=19; qq=5
ac=3*a/5; bc=s.Rational(8,5)
P=[s.Matrix([a,0]),s.Matrix([-3*a/5,s.Rational(16,5)]),s.Matrix([-3*a/5,-s.Rational(16,5)])]
def line(A,B): return s.Matrix([A[1]-B[1],B[0]-A[0],cross(A,B)])
for i,p in enumerate(P):
    check('actual boundary incidence '+str(i),p[0]**2/XX+p[1]**2/YY-1)
    L=line(p,P[(i+1)%3])
    check('actual caustic tangency '+str(i),L[2]**2-ac**2*L[0]**2-bc**2*L[1]**2)
    left=P[(i-1)%3]-p; right=P[(i+1)%3]-p
    bisector=s.simplify(left/s.sqrt(left.dot(left))+right/s.sqrt(right.dot(right)))
    normal=s.Matrix([p[0]/XX,p[1]/YY])
    check('actual reflection normal cross '+str(i),cross(bisector,normal))
    assert s.simplify(bisector.dot(normal))<0

side=[s.simplify(s.sqrt((P[(i+1)%3]-P[(i+2)%3]).dot(P[(i+1)%3]-P[(i+2)%3]))) for i in range(3)]
I=s.simplify(sum((side[i]*P[i] for i in range(3)),s.zeros(2,1))/sum(side))
O=s.Matrix([1/a,0]); R2=s.Rational(400,21); H=2*O-I
E=[]
for i in range(3):
    E.append(s.simplify(sum(((-1 if j==i else 1)*side[j]*P[j] for j in range(3)),s.zeros(2,1))/(sum(side)-2*side[i])))
print('actual centers I O H',I.T,O.T,H.T)
print('actual original/excentral signed areas',area(P),area(E))
check('actual Bevan center vector',H-s.Matrix([5/a,0]) if False else H[0]-5/a)
for i,p in enumerate(E):
    check('actual excentral circumradius '+str(i),(p-H).dot(p-H)-4*R2)
    # Consecutive excenters form the tangent at the opposite original vertex.
    L=line(E[(i+1)%3],E[(i+2)%3])
    check('actual outer tangent through original vertex '+str(i),L[0]*P[i][0]+L[1]*P[i][1]+L[2])
    check('actual outer line normal '+str(i),L[0]*P[i][1]/YY-L[1]*P[i][0]/XX)
check('actual excentral area ratio',area(E)/area(P)-s.Rational(25,6))
for sign in [-1,1]:
    F=s.Matrix([sign*s.sqrt(5),0])
    A=pedal(P,F); B=pedal(E,F)
    check('actual common focal M '+str(sign),B-s.Rational(125,24)*A)
    print('actual focal signed areas',sign,A,B)
    assert A>0 and B>0
    Pr=list(reversed(P)); Er=list(reversed(E))
    check('reversal signed original '+str(sign),pedal(Pr,F)+A)
    check('reversal signed outer '+str(sign),pedal(Er,F)+B)
print('All exact independent identities passed. Numerical phase checks are separate supplemental evidence.')
