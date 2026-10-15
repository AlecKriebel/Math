#!/usr/bin/env python3
"""Independent exact geometric checks; SymPy 1.14.0; no author-source imports."""
import json
import sympy as s
r,k,v,a,b,c,d,t=s.symbols('r k v a b c d t',real=True)
B=s.Matrix([[r,-k],[k,-r]])
D=s.Matrix([[0,v],[0,0]])
X=s.Matrix([[a,b],[c,d]])
A=B.row_join(X).col_join(s.zeros(2).row_join(D))
S=(A+A.T)/2
C=A*A.T-A.T*A
T=s.trace(S*S)
P=s.expand(s.trace(C*C)-8*T*T)
# k^2=1+r^2 is enforced after expansion.
P=s.rem(P,s.Poly(k*k-1-r*r,k),k).as_expr()
Q=s.expand(P.subs({r:t*r,a:t*a,b:t*b,c:t*c,d:t*d})).coeff(t,2).subs(k,1)
expected=16*(2-v*v)*r*r+2*((b-v*c)**2+(d+v*a)**2)+2*(1-4*v*v)*(a*a+c*c)
assert s.expand(Q-expected)==0
assert P.subs({r:0,a:0,b:0,c:0,d:0})==0
for z in (r,a,b,c,d):assert s.diff(P,z).subs({r:0,a:0,b:0,c:0,d:0})==0
# At the threshold, a same-orbit rank-two coupling strictly raises F.
Pboundary=s.factor(P.subs({r:0,k:1,v:s.Rational(1,2),b:0,c:0,d:-a/2}))
assert Pboundary==-a**4
# Derive Ric from Koszul coefficients, using no pre-encoded Ric formula.
AA=s.Matrix(4,4,lambda i,j:s.Symbol('A%d%d'%(i,j)))
n=5
f=[[[s.S.Zero for z in range(n)] for y in range(n)] for x in range(n)]
for i in range(4):
 for j in range(4):f[0][i+1][j+1]=AA[j,i];f[i+1][0][j+1]=-AA[j,i]
Gamma=[[[s.expand((f[i][j][z]-f[j][z][i]+f[z][i][j])/2) for z in range(n)] for j in range(n)] for i in range(n)]
def R(i,j,l,z):
 return s.expand(sum(Gamma[j][l][m]*Gamma[i][m][z]-Gamma[i][l][m]*Gamma[j][m][z]-f[i][j][m]*Gamma[m][l][z] for m in range(n)))
Ric=s.Matrix(n,n,lambda j,l:s.expand(sum(R(i,j,l,i) for i in range(n))))
SS=(AA+AA.T)/2
expected_Ric=s.diag(-s.trace(SS*SS),*((AA*AA.T-AA.T*AA)/2-s.trace(AA)*SS).diagonal())
expected_Ric[1:,1:]=(AA*AA.T-AA.T*AA)/2-s.trace(AA)*SS
assert (Ric-expected_Ric).applyfunc(s.expand)==s.zeros(n)
# Standard example: value and exact necessary derivation obstruction.
u=s.symbols('u',positive=True)
A0=s.diag(s.Matrix([[0,-1],[1,0]]),s.Matrix([[0,u],[0,0]]))
R0=Ric.subs(dict(zip(list(AA),list(A0))))
assert R0==s.diag(-u*u/2,0,0,u*u/2,-u*u/2)
assert s.factor(s.trace(R0)**2/s.trace(R0*R0))==s.Rational(1,3)
lam=s.symbols('lambda',real=True)
DD=R0-lam*s.eye(n)
obstruction=s.expand(DD[1:,1:]*A0-A0*DD[1:,1:]-DD[0,0]*A0)
assert obstruction[0,1]==-lam-u*u/2
assert s.simplify(obstruction[2,3].subs(lam,-u*u/2))==u**3
out={'sympy_version':s.__version__,'koszul_Ricci_identity':'PASS generic 4x4 A, including nonzero trace','transverse_quadratic_identity':'PASS','flat_family_gradient':'PASS','threshold_P':str(Pboundary),'standard_Ricci':str(R0),'standard_F':'1/3','derivation_obstruction':'rotation forces lambda=-u^2/2, nilpotent residual u^3','P_expanded':str(s.factor(P)),'quadratic':str(expected)}
print(json.dumps(out,indent=2))
