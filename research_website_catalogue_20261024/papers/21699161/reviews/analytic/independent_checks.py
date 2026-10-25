"""Fresh checks from manuscript equations, without importing published code."""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as s

OUT=Path(__file__).resolve().parent
R=s.Rational
def z(expr): assert s.simplify(expr)==0, expr
def zm(m):
    for x in m: z(x)

# Rational witness, derived directly from matrices and the Born rule.
I=s.eye(2); X=s.Matrix([[0,1],[1,0]])
Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
M=[s.Matrix([[16,-4],[-4,1]])/25,
   s.Matrix([[1,-4],[-4,16]])/25,
   8*s.Matrix([[1,1],[1,1]])/25]
zm(sum(M,s.zeros(2))-I)
for m in M:
    z(m.det()); assert 0<m.trace()<1
psi=s.Matrix([1,0,0,1])/s.sqrt(2)
def expectation(a,b):
    return s.simplify((psi.conjugate().T*s.kronecker_product(a,b)*psi)[0])
A=[(Z+X)/s.sqrt(2),(Z-X)/s.sqrt(2)]
S=expectation(A[0],Z)+expectation(A[0],X)+expectation(A[1],Z)-expectation(A[1],X)
T=R(3,5)*expectation(M[0],(I+Z)/2)+R(3,5)*expectation(M[1],(I-Z)/2)+R(4,5)*expectation(M[2],(I+X)/2)
z(S-2*s.sqrt(2));z(T-R(16,25))
U=20*s.sqrt(2)+R(3,5)+(4+3*s.sqrt(2))/250
gap=s.simplify(10*S+T-U)
z(gap-3*(2-s.sqrt(2))/250);assert gap>0

# Global robust discrimination inequality: polynomial identity on its full box.
eta,x,y,r,q=s.symbols('eta x y r q',real=True)
rad=(-1+eta*(3*x-4*y))**2+24*(1-eta**2)*(1-r)
H=8-3*x-4*y
cert=2*eta*(eta*(8*(1-y)*(4-3*x)+12*(1-r))+(q-1)*H+8*(1-y))
z(s.expand((q+eta*H)**2-rad-cert).subs(q**2,25-24*r))

# Projective inverse and exceptional fibers are checked with fresh symbols.
a,b,c,d=s.symbols('a b c d',real=True); e=a+b+c+d-R(1,2)
g=s.Matrix([[0,R(1,2),a,b],[R(1,2),0,c,d],[a,c,0,e],[b,d,e,0]])
x0,x1,x2,x3=s.symbols('x0 x1 x2 x3')
v=s.Matrix([x0,x1,x2,x3])
phi=s.Matrix([x2*(x0+x3),x3*(x0+x2),x2*(x1+x3),x3*(x1+x2)])
f0,f1,f2,f3=phi
inverse=s.Matrix([(f0-f1)*(f0-f2)*(f1-f3),(f2-f3)*(f0-f2)*(f1-f3),
                  (f0*f3-f1*f2)*(f0-f2),(f0*f3-f1*f2)*(f1-f3)])
zm(inverse-x2*x3*(x2-x3)*(x0-x1)**2*v)
p,q,Aa,Bb=s.symbols('p q Aa Bb')
n01=(s.Matrix([1,1,p,q]).T*g*s.Matrix([1,1,p,q]))[0]
n23=(s.Matrix([p,q,1,1]).T*g*s.Matrix([p,q,1,1]))[0]
z(s.resultant(n01,Bb*p*(1+q)-Aa*q*(1+p),p)+(q+1)*(Bb+q*(Aa*(2*a+2*c-1)+2*Bb*(b+d))))
z(s.resultant(n23,Bb*(p+1)-Aa*(q+1),p)+(q+1)*(Aa*q+2*Aa*(a+b)+2*Bb*(c+d)-Bb))
for vec,target in [(s.Matrix([-1,-1,p,1]),(1-2*(b+d))*(1-p)),
                   (s.Matrix([-1,-1,1,p]),(1-2*(a+c))*(1-p))]:
    z((vec.T*g*vec)[0]-target)

# A non-maximally entangled example with complex effects: no real-plane shortcut.
alice=[(I+Y)/2,(I-Y)/2,*M]
By=R(3,5)*Y+R(4,5)*Z
bob=[(I+By)/2,(I-By)/2,*M]
Xi=s.diag(s.sqrt(R(3,5)),s.sqrt(R(2,5)))
def coord(m): return s.Matrix([s.trace(m*t)/2 for t in [I,X,Y,Z]])
EA=s.Matrix.hstack(*(coord(m) for m in alice[:4]))
EB=s.Matrix.hstack(*(coord(m) for m in bob[:4]))
J=s.diag(1,-1,-1,-1); ga=EA.T*J*EA;gb=EB.T*J*EB
P=s.Matrix(4,4,lambda i,j:s.simplify(s.trace(alice[i]*Xi*bob[j].T*Xi.conjugate().T)))
assert EA.det()!=0 and EB.det()!=0 and P.det()!=0
zm(P.T*ga.inv()*P-4*abs(Xi.det())**2*gb)
u=s.Matrix([1,1,0,0]); rays=[s.eye(4)[:,i] for i in range(4)]+[s.Matrix([1,1,-1,-1])]
z((u.T*P*u)[0]-1)
for j,rj in enumerate(rays):
    z((rj.T*P.T*ga.inv()*P*rj)[0])
    steer=Xi*bob[j].T*Xi.conjugate().T
    zm(coord(steer)-EA.T.inv()*P*rj/2)
    assert s.simplify((u.T*P*rj)[0])>0
    for i,ri in enumerate(rays):
        z((ri.T*P*rj)[0]-s.trace(alice[i]*steer))

# General polynomial Hessian identity, not a fixed numerical matrix instance.
def symmetric(prefix):
    vals=iter(s.symbols(prefix+':10'));mat=s.zeros(4)
    for i in range(4):
        for j in range(i,4): mat[i,j]=mat[j,i]=next(vals)
    return mat
Q=symmetric('q'); HH=symmetric('h')
xx=s.Matrix(s.symbols('v:4'));dx=s.Matrix(s.symbols('w:4'))
delta=dx-HH*Q*xx
half=(dx.T*Q*dx-2*dx.T*Q*HH*Q*xx+xx.T*Q*HH*Q*HH*Q*xx)[0]
assert s.expand(half-(delta.T*Q*delta)[0])==0

# Exhaustive finite rational transportation check, including zero capacities.
count=0; boundary_count=0;n=8
compositions=[(i,j,n-i-j) for i in range(n+1) for j in range(n+1-i)]
for c12,c13,c23 in compositions:
    cc=[[F(0),F(c12,2*n),F(c13,2*n)],
        [F(c12,2*n),F(0),F(c23,2*n)],
        [F(c13,2*n),F(c23,2*n),F(0)]]
    degree=[sum(row) for row in cc]
    for nums in compositions:
        aa=[F(i,2*n) for i in nums];bb=[degree[i]-aa[i] for i in range(3)]
        if min(bb)<0:continue
        dd=[(bb[i]-aa[i])/2 for i in range(3)]
        lows=[-cc[0][1]/2,dd[0]-cc[0][2]/2,-dd[1]-cc[1][2]/2]
        highs=[cc[0][1]/2,dd[0]+cc[0][2]/2,-dd[1]+cc[1][2]/2]
        t=max(lows);assert t<=min(highs)
        flow=[[F(0),t,dd[0]-t],[-t,F(0),dd[1]+t],[-dd[0]+t,-dd[1]-t,F(0)]]
        transport=[[cc[i][j]/2+flow[i][j] for j in range(3)] for i in range(3)]
        assert [sum(row) for row in transport]==bb
        assert [sum(transport[i][j] for i in range(3)) for j in range(3)]==aa
        assert all(0<=transport[i][j]<=cc[i][j] for i in range(3) for j in range(3))
        count+=1; boundary_count+=int(min(c12,c13,c23)==0 or min(aa+bb)==0)

result={'sympy_version':s.__version__,'published_code_imported':False,
        'simple_strategy_value':str(10*S+T),'certified_gap':str(gap),
        'robust_discrimination_identity':'passed','projective_inverse_and_exceptional_resultants':'passed',
        'complex_effects_nonmaximally_entangled_incidence_reconstruction':'passed',
        'general_symbolic_Hessian_identity':'passed',
        'rational_transportation_instances':count,'boundary_transportation_instances':boundary_count}
(OUT/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
