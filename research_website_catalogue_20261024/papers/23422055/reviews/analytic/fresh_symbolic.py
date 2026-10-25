"""Fresh analytic verification, matrix/Pfaffian route; no published imports.
Exact symbolic identities do not verify compactness, patching, or cohomology.
"""
import sympy as S
from itertools import combinations, product
import json

checks=[]
def zero(label, expression):
    entries=list(expression) if isinstance(expression,S.MatrixBase) else [expression]
    bad=[S.simplify(x) for x in entries if S.simplify(x)!=0]
    if bad:raise RuntimeError(label+': '+str(bad))
    checks.append(label)

def skew(items):
    m=S.zeros(4)
    for (i,j),a in items.items():m[i,j]=a;m[j,i]=-a
    return m

def square_coefficient(a):
    # Pfaffian, twice because wedge squares repeat each matching.
    return 2*(a[0,1]*a[2,3]-a[0,2]*a[1,3]+a[0,3]*a[1,2])

def mixed(a,b):
    return S.expand((square_coefficient(a+b)-square_coefficient(a)-square_coefficient(b))/2)

u,v,x,t,eps=S.symbols('u v x t epsilon',real=True)
coords=(u,v,x,t)
R=S.Function('R')(*coords)
a,b,c=S.symbols('R_x R_t R_u',real=True)
A=skew({(0,2):1,(1,3):-1})
B0=skew({(0,3):1,(1,2):1})
B=skew({(0,1):c,(0,3):1,(1,2):1-a,(1,3):-b})
D=1-a-b*b/4
H=B-b*A/2
Jnum=A*H
zero('Pfaffian alpha square',square_coefficient(A)-2)
zero('Pfaffian beta square',square_coefficient(B)-2*(1-a))
zero('Pfaffian mixed wedge',mixed(A,B)-b)
zero('full cutoff orthogonal plane',mixed(A,H))
zero('full cutoff normalized square',square_coefficient(H)-2*D)
zero('full cutoff J squared without radicals',Jnum*Jnum+D*S.eye(4))
zero('full cutoff alpha anti-invariance',Jnum.T*A*Jnum+D*A)
zero('full cutoff beta anti-invariance',Jnum.T*B*Jnum+D*B)
zero('full cutoff third representative anti-invariance',Jnum.T*(u*A-v*B)*Jnum+D*(u*A-v*B))
zero('full cutoff complex type identity',(A+S.I*H/S.sqrt(D))*Jnum/S.sqrt(D)-S.I*(A+S.I*H/S.sqrt(D)))
zero('full cutoff determinant',Jnum.det()-D**2)
zero('zero jet returns product J',Jnum.subs({a:0,b:0,c:0})-S.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]))

def exterior_derivative_matrix(m):
    return {key:S.simplify(S.diff(m[key[1],key[2]],coords[key[0]])-S.diff(m[key[0],key[2]],coords[key[1]])+S.diff(m[key[0],key[1]],coords[key[2]])) for key in combinations(range(4),3)}

def d_one_form(z):
    return S.Matrix(4,4,lambda i,j:S.diff(z[j],coords[i])-S.diff(z[i],coords[j]))

delta=d_one_form(S.Matrix([0,R,0,0]))
bp=B0+delta
gp=u*A-v*B0-d_one_form(S.Matrix([0,R*v,0,0]))
zero('arbitrary-cutoff jet expansion',bp-B.subs({a:S.diff(R,x),b:S.diff(R,t),c:S.diff(R,u)}))
zero('arbitrary-cutoff exact third-form identity',gp-(u*A-v*bp))
for label,m in [('alpha',A),('beta',bp),('gamma',gp)]:
    for key,value in exterior_derivative_matrix(m).items():zero('closed '+label+' '+str(key),value)

# Local cohomology positivity, via the Pfaffian rather than a guessed metric.
p,q,r=S.symbols('p q r',real=True)
F=(p+r*u)*A+(q-r*v)*B0
zero('positive real holomorphic combination',square_coefficient(F)-2*((p+r*u)**2+(q-r*v)**2))
z,s,y,w,yp,qq=S.symbols('z s y w yprime qinf')
zero('sextic has no repeated root',S.gcd(z**6-1,6*z**5)-1)
zero('Riemann Hurwitz genus two',2-2*2-(2*2-6))
zero('local Jacobian determinant',S.Matrix([[1,0],[-w*yp/y**2,1/y]]).det()-1/y)
zero('first differential at infinity',(-1/s**2)/(qq/s**3)+s/qq)
zero('second differential at infinity',(1/s)*(-1/s**2)/(qq/s**3)+1/qq)
# Kunneth intersection form sanity check for Sigma_2 x T^2.
symp=S.Matrix([[0,1],[-1,0]])
q_mixed=-S.kronecker_product(S.diag(symp,symp),symp)
q_product=S.diag(S.Matrix([[0,1],[1,0]]),q_mixed)
zero('product intersection form involution',q_product*q_product-S.eye(10))
zero('product signature zero',S.trace(q_product))
if q_product.eigenvals()!={-1:5,1:5}:raise RuntimeError('product intersection signature')
checks.append('product b2=10 and bplus=bminus=5, consistent with three positive classes')

# Independent tensor calculation of ALL coordinate Nijenhuis components.
k=S.Function('k')(x)
J=Jnum.subs({a:1-k,b:0,c:0})/S.sqrt(k)
def bracket(U,V):
    return S.Matrix([S.simplify(sum(U[j]*S.diff(V[i],coords[j])-V[j]*S.diff(U[i],coords[j]) for j in range(4))) for i in range(4)])
ee=[S.eye(4)[:,i] for i in range(4)]
def nijenhuis(U,V):
    return (bracket(J*U,J*V)-J*bracket(J*U,V)-J*bracket(U,J*V)-bracket(U,V)).applyfunc(S.simplify)
N={(i,j):nijenhuis(ee[i],ee[j]) for i,j in combinations(range(4),2)}
zero('nonintegrability component N(u,x)',N[0,2]-S.diff(k,x)/(2*k)*ee[0])
zero('N origin for epsilon family',N[0,2].subs(k,1-eps*x).doit().subs(x,0)+eps*ee[0]/2)
for i,j in combinations(range(4),2):
    zero('tensor anti-linearity '+str((i,j)),nijenhuis(J*ee[i],ee[j])+J*N[i,j])

normalized=skew({(0,3):1/S.sqrt(k),(1,2):S.sqrt(k)})
derivs=exterior_derivative_matrix(normalized)
zero('normalization fails closedness as stated',derivs[0,2,3]-S.diff(k,x)/(2*k**S.Rational(3,2)))

negative=[]
if S.simplify(square_coefficient(A+S.I*B0.subs({})*2))==0:
    raise RuntimeError('unnormalized pair mutation escaped')
negative.append('dropping normalization generally destroys decomposability')
wrong=u*A-v*B0+d_one_form(S.Matrix([0,R*v,0,0]))
if all(S.simplify(val)==0 for val in wrong-(u*A-v*bp)):
    raise RuntimeError('wrong third-form sign escaped')
negative.append('wrong third-form perturbation sign breaks simultaneous plane')
if S.simplify(D.subs({a:0,b:2}))!=0:raise RuntimeError('degenerate boundary control')
negative.append('D=0 prevents smooth plane realization; strict smallness is essential')
if all(S.simplify(val)==0 for val in N[0,2]):raise RuntimeError('nonintegrability missing')
negative.append('closed unnormalized real pair does not force integrability')

# Exact rational jet sampling supplements the universal symbolic identities.
jet_count=0
for av,bv,cv in product([S.Rational(i,8) for i in range(-2,3)],[-1,S.Rational(-1,2),0,S.Rational(1,2),1],[-7,0,11]):
    dd=D.subs({a:av,b:bv});jj=Jnum.subs({a:av,b:bv,c:cv})
    if dd<S.Rational(1,2):raise RuntimeError('published uniform D bound')
    if jj*jj!=-dd*S.eye(4):raise RuntimeError('exact rational J square')
    jet_count+=1

print(json.dumps({'status':'PASS','sympy_version':S.__version__,'symbolic_identity_count':len(checks),
 'checks':checks,'exact_rational_jet_cases':jet_count,'negative_controls':negative,
 'general_J_numerator':str(Jnum),'general_J_denominator':'sqrt(1-R_x-R_t^2/4)',
 'core_Nijenhuis_components':{str(key):str(val) for key,val in N.items()},
 'limits':'Exact local identities only; global cohomology, compactification and smooth gluing are established analytically in REVIEW.md.'},indent=2))
