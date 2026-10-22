"""Independent exact algebra. No historical checker or proof imports."""
import json
from pathlib import Path
import sympy as s
u=s.symbols('u', positive=True)
J=s.Matrix([[0,-1],[1,0]])
N=s.Matrix([[0,u],[0,0]])
A=s.diag(J,N)
def comm(X,Y): return X*Y-Y*X
def frob(X): return s.trace(X.T*X)
def curvature(B):
    S=(B+B.T)/2
    R=s.diag(-s.trace(S*S), comm(B,B.T)/2-s.trace(B)*S)
    scal=s.trace(R)
    return R,scal,s.factor(scal**2/frob(R))
def gap(B):
    S=(B+B.T)/2
    return frob(comm(B,B.T))-8*s.trace(S*S)**2
# Direct structure constants/Koszul verification at a completely generic 4x4 A.
b=s.Matrix(4,4,s.symbols('b:16'))
c={}
for i in range(1,5):
    for j in range(1,5):
        c[0,i,j]=b[j-1,i-1]
        c[i,0,j]=-b[j-1,i-1]
def cv(i,j,k): return c.get((i,j,k),s.S.Zero)
g={(i,j,k):(cv(i,j,k)-cv(j,k,i)+cv(k,i,j))/2 for i in range(5) for j in range(5) for k in range(5)}
ric=s.zeros(5)
for j in range(5):
 for k in range(5):
  for i in range(5):
   ric[j,k]+=sum(g[j,k,m]*g[i,m,i]-g[i,k,m]*g[j,m,i]-cv(i,j,m)*g[m,k,i] for m in range(5))
Sb=(b+b.T)/2
expected=s.diag(-s.trace(Sb*Sb), comm(b,b.T)/2-s.trace(b)*Sb)
if any(s.expand(x)!=0 for x in ric-expected): raise RuntimeError('Koszul/Ricci identity failed')
R,scalar,F=curvature(A)
if s.simplify(F-s.Rational(1,3))!=0: raise RuntimeError('base F')
a,bb,c0,d,p,q,r,t=s.symbols('a b c d p q r t', real=True)
X=s.Matrix([[a,bb,p,q],[bb,-a,r,t],[p,r,c0,d],[q,t,d,-c0]])
A1=comm(X,A); A2=comm(X,A1)
S0=(A+A.T)/2; S1=(A1+A1.T)/2; S2=(A2+A2.T)/2
C0=comm(A,A.T); C1=comm(A1,A.T)+comm(A,A1.T)
C2=comm(A2,A.T)+2*comm(A1,A1.T)+comm(A,A2.T)
q0=s.trace(S0*S0); q1=2*s.trace(S0*S1); q2=2*s.trace(S1*S1)+2*s.trace(S0*S2)
g1=s.factor(2*s.trace(C0.T*C1)-16*q0*q1)
g2=s.factor(2*s.trace(C1.T*C1)+2*s.trace(C0.T*C2)-16*(q1*q1+q0*q2))
variables=[a,bb,c0,d,p,q,r,t]
H=s.simplify(s.hessian(g2,variables)/2) # g''=x^T H x
if g1!=0: raise RuntimeError('nonstationary gap')
# transverse Hessian is g2 with c=d=0; it has a,b diagonal and crossblock.
Hcross=H.extract([4,5,6,7],[4,5,6,7])
eigs={str(s.factor(k)):v for k,v in Hcross.eigenvals().items()}
# complete local chart rank using 5 orthogonal generators and 7 orbit params.
U=s.symbols('U', positive=True)
AU=A.subs(u,U)
Z=s.Matrix([[a,bb,p,q],[bb,-a,r,t],[p,r,0,0],[q,t,0,0]])
tangents=[]
for i,j in [(0,2),(0,3),(1,2),(1,3),(2,3)]:
 Q=s.zeros(4);Q[i,j]=1;Q[j,i]=-1;tangents.append(comm(Q,AU))
for v in [a,bb,p,q,r,t]: tangents.append(comm(Z.diff(v),AU))
tangents.append(AU.diff(U))
Jac=s.Matrix.hstack(*[T.reshape(16,1) for T in tangents])
rank=Jac.rank()
if rank!=12: raise RuntimeError('local chart rank')
# Rational same-orbit comparison via diagonal change: rotation becomes elliptic block.
D=s.diag(s.Rational(2),1,2/u,1)
B=s.simplify(D*A*D.inv())
_,_,FB=curvature(B)
comparison=s.factor(FB-s.Rational(1,3))
# Solvsoliton test: D=Ric-c I derivation gives [D_n,A]=d_0 A.
# rotational block forces d_0=0; hence c=Ric00 and nilpotent block commutator u^2 N nonzero.
solv_residual=comm(R[1:5,1:5],A)
result={'sympy':s.__version__,'ricci':str(R),'scalar':str(scalar),'F':str(F),'gap_first_derivative':str(g1),'gap_second_derivative':str(g2),'gap_hessian':str(H),'cross_eigenvalues':eigs,'chart_rank':rank,'comparison_matrix':str(B),'comparison_F':str(FB),'comparison_minus_one_third':str(comparison),'derivation_residual':str(solv_residual)}
Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
