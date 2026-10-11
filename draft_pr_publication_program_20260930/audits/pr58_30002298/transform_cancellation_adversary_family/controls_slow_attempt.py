"""Independent exact transform/cancellation controls; stdout only.
No author checker or historical/fresh-family result imports. Universal claim
is proved in PROOF.md; these examples do not replace it.
"""
import hashlib,itertools,json,os,platform
from pathlib import Path
import sympy as S
import mpmath

checks=[]; cases=[]
def check(name,ok):
    if not bool(ok): raise AssertionError(name)
    checks.append(name)
def linear(v,U): return 1-sum(a*b for a,b in zip(v,U))
def simplex(V,U):
    d=len(U); D=abs(S.Matrix.hstack(*[S.Matrix(v)-S.Matrix(V[0]) for v in V[1:]]).det())
    return D/S.prod(linear(v,U) for v in V)
def denominator(F,U):
    N,D=S.fraction(S.cancel(F)); constant=D.subs(dict.fromkeys(U,0))
    check('denominator nonzero at zero '+str(len(checks)),constant!=0)
    return S.expand(D/constant)
def expected(F,V,U,name):
    Q=S.prod(linear(v,U) for v in set(V) if any(v))
    D=denominator(F,U)
    check(name+' exact reduced denominator',S.expand(D-Q)==0)
    factors=S.factor_list(D,*U)[1]
    check(name+' squarefree',all(power==1 for factor,power in factors))
    check(name+' gcd',S.Poly(S.gcd(*S.fraction(S.cancel(F))),*U).total_degree()==0)
    cases.append({'name':name,'denominator':str(S.factor(D)),'nonconstant_vertex_factor_count':len(factors)})
def rectangle(a,b,c,d,U):
    V=[(a,c),(b,c),(b,d),(a,d)]
    return simplex([V[0],V[1],V[2]],U)+simplex([V[0],V[2],V[3]],U)

# Rational interpolation with arbitrary symbolic projected vertices.
for d in range(1,6):
    lam=S.symbols('l0:'+str(d+1))
    rhs=sum(1/((1-a)*S.prod(a-b for b in lam if b!=a)) for a in lam)
    check(f'generic projection partial fractions d={d}',S.cancel(rhs-1/S.prod(1-a for a in lam))==0)

U=S.symbols('u v')
rect=rectangle(1,3,2,4,U); corners=[(1,2),(3,2),(3,4),(1,4)]
expected(rect,corners,U,'offset rectangle')
center=(2,3)
fan=sum(simplex([center,corners[i],corners[(i+1)%4]],U) for i in range(4))
check('artificial interior-vertex fan equality',S.cancel(fan-rect)==0)
expected(fan,corners,U,'interior artificial vertex cancels')
edge=(2,2)
fanedge=sum(simplex([corners[2],a,b],U) for a,b in [(corners[0],edge),(edge,corners[1]),(corners[3],corners[0])])
check('artificial collinear edge vertex equality',S.cancel(fanedge-rect)==0)
expected(fanedge,corners,U,'dependent edge vertex cancels')

# Unit union needs inclusion/exclusion. Two source vertices become interior;
# intersection corners become reentrant boundary vertices with surviving poles.
A=rectangle(0,2,0,2,U); B=rectangle(1,3,1,3,U); I=rectangle(1,2,1,2,U)
union=A+B-I
boundary=[(0,0),(2,0),(2,1),(3,1),(3,3),(1,3),(1,2),(0,2)]
expected(union,boundary,U,'overlapping-square union')
check('unit union mass',S.cancel(union).subs(dict.fromkeys(U,0))==14)
check('double-counted overlap is detected',S.cancel(A+B-union)!=0)
check('interior source corner poles absent',all(S.rem(denominator(union,U),linear(v,U),*U)!=0 for v in [(1,1),(2,2)]))

ring=rectangle(-2,2,-2,2,U)-rectangle(-1,1,-1,1,U)
ring_vertices=[(a,b) for k in [1,2] for a in [-k,k] for b in [-k,k]]
expected(ring,ring_vertices,U,'closed square ring modulo null inner boundary')
check('ring normalized mass',S.cancel(ring).subs(dict.fromkeys(U,0))==24)
check('ring has reentrant-vertex poles',all(S.rem(denominator(ring,U),linear(v,U),*U)==0 for v in [(-1,-1),(-1,1),(1,-1),(1,1)]))

tri=[(1,2),(4,2),(2,6)]
F=simplex(tri,U)
expected(F,tri,U,'nonstandard simplex')
check('simplex normalized mass',F.subs(dict.fromkeys(U,0))==12)
check('simplex first moment normalization',S.diff(F,U[0]).subs(dict.fromkeys(U,0))==12*sum(v[0] for v in tri))
check('simplex second moment normalization',S.diff(F,U[0],2).subs(dict.fromkeys(U,0))==12*(sum(v[0] for v in tri)**2+sum(v[0]**2 for v in tri)))

# Formal opposite-simplex parity for dimensions 1..6, without imposing a
# general-position condition on all geometric vertices.
L=S.symbols('L')
for d in range(1,7):
    X=S.symbols('x1:'+str(d+1))
    raw=1/(L*S.prod(L-a for a in X))+1/(L*S.prod(L+a for a in X))
    N,D=S.fraction(S.cancel(raw))
    check(f'odd/even apex cancellation d={d}',S.rem(D,L,L,*X)==0 if d%2==0 else S.rem(D,L,L,*X)!=0)
    check(f'parity numerator gcd d={d}',S.Poly(S.gcd(N,D),L,*X).total_degree()==0)
    h=S.symbols('h0:'+str(d))
    indicator=S.expand(S.prod(h)+S.prod(1-a for a in h))
    coefficient=S.Poly(indicator,*h).coeff_monomial(S.prod(h))
    check(f'orthant indicator top coefficient d={d}',coefficient==(0 if d%2 else 2))
    for values in itertools.product([0,1],repeat=d):
        check(f'orthant boolean indicator d={d},{values}',indicator.subs(dict(zip(h,values)))==(1 if all(values) or not any(values) else 0))

X=S.symbols('x y z'); apex=(2,3,4)
zero=(0,0,0)
def opposite(v):
    plus=[v]+[tuple(v[j]+(i==j) for j in range(3)) for i in range(3)]
    minus=[v]+[tuple(v[j]-(i==j) for j in range(3)) for i in range(3)]
    return simplex(plus,X)+simplex(minus,X),plus[1:]+minus[1:]
FO,vo=opposite(zero); FT,vt=opposite(apex)
expected(FO,vo,X,'origin opposite tetrahedra')
expected(FT,vt,X,'translated opposite tetrahedra')
check('origin unit convention',linear(zero,X)==1)
check('nonzero canceled essential apex changes requested equality',S.expand(denominator(FT,X)-S.prod(linear(v,X) for v in vt+[apex]))!=0)

# Lower-dimensional unit ambient mass is zero; literal triangulation vertices
# can remain. The isolated point does not create a transform pole.
q=(7,11); appendage=rect
check('isolated ambient-null appendage has no pole',S.rem(denominator(appendage,U),linear(q,U),*U)!=0)
check('pure ambient-null set denominator',denominator(S.Integer(0),U)==1)
check('pure nonzero segment literal target differs',S.expand(S.prod(linear(v,U) for v in [(4,5),(6,9)]))!=1)

# Measure countercontrols: surface/atomic density and the higher polynomial
# density transform do not satisfy the squarefree unit-volume statement.
a,b=(4,5),(6,9); La,Lb=linear(a,U),linear(b,U)
surface=(La+Lb)/(La**2*Lb**2) # nonzero length constant omitted
atomic=2/La**3
check('surface-measure repeated endpoint factors',S.expand(denominator(surface,U)-La**2*Lb**2)==0)
check('atomic repeated vertex factor',S.expand(denominator(atomic,U)-La**3)==0)
w=S.symbols('w'); unit_interval=1/((1-w)*(1-2*w)); polynomial_transform=S.diff(unit_interval,w)
check('polynomial-density higher transform repeated factors',S.expand(denominator(polynomial_transform,[w])-(1-w)**2*(1-2*w)**2)==0)
check('one-dimensional direct integral normalization',S.cancel((1/(1-2*w)-1/(1-w))/w-unit_interval)==0)

# Nonorthogonal generators; signs must be obtained from one generic vector,
# not separately chosen incompatible convergence domains.
Q=S.Matrix([[1,-2,1],[1,1,0],[0,1,-1]]); eta=S.Matrix([3,5,7])
check('cone generator independence',Q.det()!=0)
signs=[S.sign((eta.T*Q[:,i])[0]) for i in range(3)]
check('generic flip vector',all(sign!=0 for sign in signs))
Qplus=Q*S.diag(*signs)
def cone(matrix):
    return -abs(matrix.det())/S.prod((matrix[:,i].T*S.Matrix(X))[0] for i in range(3))
check('nonorthogonal signed flip valuation',S.cancel(cone(Q)-S.prod(signs)*cone(Qplus))==0)
for d in range(1,6):
    check(f'convergent orthant sign d={d}',(-1)**d/S.prod([-1]*d)==1)

print(json.dumps({'schema':'pr58-independent-transform-controls/v1','process_pid':os.getpid(),'python':platform.python_version(),'sympy':S.__version__,'mpmath':mpmath.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks_passed':len(checks),'checks':checks,'cases':cases,'author_or_history_imports':False,'universal_proof':'PROOF.md','finite_controls_not_universal_proof':True},indent=2,sort_keys=True))
