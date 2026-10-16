from pathlib import Path
import sympy as S, random, json, math, hashlib, datetime
u,v,a,b,x,y,z,w,k,c=S.symbols('u v a b x y z w k c',real=True)
J=S.Matrix([[0,-1],[1,0]]);Au=S.diag(J,S.Matrix([[0,u],[0,0]]))
C=S.Matrix([[a,b-k],[b+k,-a]]);L=S.Matrix([[x,y],[z,w]]);N=S.Matrix([[0,v],[0,0]])
M=C.row_join(S.zeros(2)).col_join(L.row_join(N));sym=(M+M.T)/2
norm2=lambda T:S.expand(sum(q*q for q in T))
comm=M*M.T-M.T*M;s=norm2(sym);q=norm2(comm);P=S.expand(q-8*s*s)
P=S.rem(S.Poly(P,k),S.Poly(k*k-(1+a*a+b*b),k)).as_expr()
Q=16*(2-v*v)*(a*a+b*b)+2*(x+v*w)**2+2*(y-v*z)**2+2*(1-4*v*v)*(z*z+w*w)
h2=a*a+b*b;r2=x*x+y*y+z*z+w*w;d=w*x-y*z
R=-12*h2*r2-24*a*k*(w*z+x*y)+12*b*k*(x*x+z*z-y*y-w*w)+4*v*(a*(w*y-x*z)-b*(w*x+y*z))+4*v*(k-1)*d-4*d*d
assert S.expand(P-Q-R)==0
assert S.expand(s-(2*h2+(r2+v*v)/2))==0
# Independent Ricci trace from structure constants using Koszul coefficients.
A=Au;n=5
br=[[[S.Integer(0) for m in range(n)] for j in range(n)] for i in range(n)]
for j in range(4):
 for m in range(4):br[0][j+1][m+1]=A[m,j];br[j+1][0][m+1]=-A[m,j]
conn=[[[S.simplify((br[i][j][m]-br[j][m][i]+br[m][i][j])/2) for m in range(n)] for j in range(n)] for i in range(n)]
def curvature(i,j,l,m):return S.simplify(sum(conn[j][l][p]*conn[i][p][m]-conn[i][l][p]*conn[j][p][m]-br[i][j][p]*conn[p][l][m] for p in range(n)))
ric=S.Matrix(n,n,lambda j,l: S.simplify(sum(curvature(i,j,l,i) for i in range(n))))
expected=S.diag(-u*u/2,0,0,u*u/2,-u*u/2);assert ric==expected
Scal=S.trace(ric);F=S.factor(Scal**2/norm2(ric));assert F==S.Rational(1,3)
dd=[ric[i,i]-c for i in range(5)]
obstructions=[S.factor(dd[2]-dd[0]-dd[1]),S.factor(dd[3]-dd[0]-dd[4])]
assert S.solve(obstructions,c)==[]
# A completely unrestricted slice with nilpotent block is conjugate:
# solve NC? For T=[I,0;Y,I], lower block Y C - N Y=L.
Y=S.Matrix(2,2,S.symbols('p0:4'));sol=S.solve(list(Y*C-N*Y-L),list(Y),dict=True)[0]
assert all(S.simplify(t)==0 for t in (Y*C-N*Y-L).subs(sol))
# explicit comparison
B=S.Matrix([[0,-1,0,0],[1,0,0,0],[1,0,0,1],[0,-1,0,0]])
TB=S.eye(4);TB[2,1]=2;TB[3,0]=1
H=S.diag(1,1,1/u,1)
assert H*Au*H.inv()==Au.subs(u,1);assert TB*Au.subs(u,1)*TB.inv()==B
sB=norm2((B+B.T)/2);qB=norm2(B*B.T-B.T*B);assert sB==S.Rational(3,2) and qB==8
# exact endpoint counterexample in the same full slice; Q=0,P=-t^4.
t=S.symbols('t',real=True);endpoint=S.factor(P.subs({a:0,b:0,k:1,v:S.Rational(1,2),x:-t/2,y:0,z:0,w:t}))
assert endpoint==-t**4
# random matrices P in radius far below constructive local bound, including u near boundary
rng=random.Random(6800014);samples=0;worst=math.inf
pf=S.lambdify((a,b,x,y,z,w,v,k),P,'math')
for u0 in (0.01,0.1,0.25,0.49,0.499):
 vp=(u0+0.5)/2;vm=u0/2;c0=1-4*vp**2;radius=c0/100
 for _ in range(800):
  vals=[rng.uniform(-1,1) for _ in range(6)];r=math.sqrt(sum(t*t for t in vals));vals=[t*radius*rng.uniform(0.01,1)/max(r,1) for t in vals]
  vv=rng.uniform(vm,vp);kk=math.sqrt(1+vals[0]**2+vals[1]**2);pval=pf(*vals,vv,kk);rho2=sum(t*t for t in vals)
  assert pval>=.5*c0*rho2-1e-25
  worst=min(worst,pval/(c0*rho2));samples+=1
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sympy':S.__version__,'exact_slice_identity':True,'koszul_direct_Ricci':str(ric),'derivation_obstructions':list(map(str,obstructions)),'global_F':'9/17','endpoint_half_exact_P':str(endpoint),'sample_seed':6800014,'samples':samples,'minimum_ratio_P_over_c0_rho2':worst,'independent_formula_artifact_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('independent_reconstruction_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
