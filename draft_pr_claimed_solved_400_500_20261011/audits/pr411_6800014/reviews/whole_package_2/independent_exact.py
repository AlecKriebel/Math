import sympy as sp
import json, platform
from pathlib import Path
a,b,k,v,x,y,z,w,u,t,c = sp.symbols('a b k v x y z w u t c', real=True)
M=sp.Matrix([[a,b-k,0,0],[b+k,-a,0,0],[x,y,0,v],[z,w,0,0]])
def norm2(B): return sp.expand(sum(q*q for q in B))
def simp(q): return sp.factor(sp.expand(q).subs(k**2,1+a*a+b*b))
# Raw structure constants and independent Koszul/curvature contraction.
n=5
br=[[[sp.S(0) for h in range(n)] for j in range(n)] for i in range(n)]
for j in range(4):
    for h in range(4):
        br[0][j+1][h+1]=M[h,j]; br[j+1][0][h+1]=-M[h,j]
G=[[[sp.expand((br[i][j][h]-br[j][h][i]+br[h][i][j])/2) for h in range(n)] for j in range(n)] for i in range(n)]
R=sp.zeros(n)
for j in range(n):
    for l in range(n):
        R[j,l]=sp.expand(sum(G[j][l][h]*G[i][h][i]-G[i][l][h]*G[j][h][i]-br[i][j][h]*G[h][l][i] for i in range(n) for h in range(n)))
S=(M+M.T)/2; comm=M*M.T-M.T*M
expected=sp.diag(-norm2(S),*(sp.S(0) for _ in range(4)))
expected[1:5,1:5]=comm/2
assert all(sp.expand(q)==0 for q in R-expected)
s=norm2(S);q=norm2(comm);P=simp(q-8*s*s)
h2=a*a+b*b;r2=x*x+y*y+z*z+w*w;d=w*x-y*z
Q=16*(2-v*v)*h2+2*(x+v*w)**2+2*(y-v*z)**2+2*(1-4*v*v)*(z*z+w*w)
rem=-12*h2*r2-24*a*k*(w*z+x*y)+12*b*k*(x*x+z*z-y*y-w*w)+4*v*(a*(w*y-x*z)-b*(w*x+y*z))+4*v*(k-1)*d-4*d*d
assert simp(P-Q-rem)==0
J=sp.Matrix([[0,-1],[1,0]])
A=sp.diag(J,sp.Matrix([[0,u],[0,0]]))
RA=R.subs(dict(zip((a,b,k,v,x,y,z,w),(0,0,1,u,0,0,0,0))))
assert RA==sp.diag(-u*u/2,0,0,u*u/2,-u*u/2)
assert sp.simplify(sp.trace(RA)**2/norm2(RA))==sp.Rational(1,3)
# Check required Ric-cI directly against every original bracket.
D=RA-c*sp.eye(5)
fails=sp.expand(D[2,2]-D[0,0]-D[1,1])
assert sp.solve(fails,c)==[-u*u/2]
assert sp.simplify((D[3,3]-D[0,0]-D[4,4]).subs(c,-u*u/2))==u*u
B=sp.Matrix([[0,-1,0,0],[1,0,0,0],[1,0,0,1],[0,-1,0,0]])
H=sp.diag(1,1,1/u,1);TB=sp.eye(4);TB[2:4,0:2]=sp.Matrix([[0,2],[1,0]])
assert TB*H*A*H.inv()*TB.inv()==B
sB=norm2((B+B.T)/2);qB=norm2(B*B.T-B.T*B)
assert (sB,qB)==(sp.Rational(3,2),8)
assert sB*sB/(sB*sB+qB/4)==sp.Rational(9,17)
# Exact ascent on actual conjugacy orbit, including excluded boundary.
ascent=simp(P.subs({a:0,b:0,k:1,x:0,w:0,z:t,y:v*t}))
assert sp.expand(ascent-(2*(1-4*v*v)*t*t-4*v*v*t**4))==0
assert ascent.subs(v,sp.Rational(1,2))==-t**4
# The rank-two nilpotent slice and rotation quotient have disjoint spectra;
# Sylvester's equation explicitly removes every L by similarity.
L=sp.Matrix([[x,y],[z,w]]);N=sp.Matrix([[0,v],[0,0]])
C=M[0:2,0:2];Y=(L*C+N*L) # since C^2=-I and N^2=0, solve Y C-NY=L
assert all(simp(e)==0 for e in (-Y*C+N*Y)-L)
# Positivity matrices: exact determinant, trace, and rational endpoint example.
K=sp.Matrix([[1,v],[v,1-3*v*v]])
assert K.det()==1-4*v*v
assert sp.expand(K.trace())==2-3*v*v
results={'python':platform.python_version(),'sympy':sp.__version__,'koszul_matrix_identity':True,'P_Q_R_identity':True,'candidate_Ric':str(RA),'nonglobal_F':'9/17','ascent_polynomial':str(ascent),'boundary_P':'-t^4','all_cross_blocks_similar':True,'limitations':'Exact symbolic identities plus analytic proof reconstruction; no finite sample claimed as neighborhood proof.'}
print(json.dumps(results,indent=2))
