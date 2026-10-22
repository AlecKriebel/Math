import datetime,json,pathlib,sympy as s
O=pathlib.Path(__file__).parent
u,v,x,t,e=s.symbols('u v x t e',real=True); p,q,r=s.symbols('p q r',real=True)
a=s.sqrt(1-q-r*r/4); coords=(u,v,x,t); events=[]
def zero(name,z):
 z=s.Matrix(z) if isinstance(z,(list,tuple)) else z
 if isinstance(z,s.MatrixBase): ok=all(s.simplify(k)==0 for k in z)
 else: ok=s.simplify(z)==0
 if not ok: raise RuntimeError(name+': '+str(z))
 events.append(name)
A=s.zeros(4); A[0,2]=1; A[1,3]=-1; A=A-A.T
B=s.zeros(4); B[0,3]=1; B[1,2]=1-q; B[1,3]=-r; B[0,1]=p; B=B-B.T
C=(B-r*A/2)/a; J=-A.inv()*C
zero('full arbitrary jet real J squares minus identity',J*J+s.eye(4))
zero('full alpha anti-invariance',J.T*A*J+A)
zero('full beta anti-invariance including Ru',J.T*B*J+B)
zero('full gamma variable-plane anti-invariance',J.T*(u*A-v*B)*J+(u*A-v*B))
f1=s.Matrix([[1,-r/2+s.I*a,0,0]])
f2=s.Matrix([[0,s.I*p/a,1-s.I*r/(2*a),s.I/a]])
zero('independent full-cutoff coframe factorization',f1.T*f2-f2.T*f1-A-s.I*C)
realrows=s.Matrix([[1,-r/2,0,0],[0,a,0,0],[0,0,1,0],[0,p/a,-r/(2*a),1/a]])
zero('real coframe determinant positive one',realrows.det()-1)
k=1-e*x; core=J.subs({p:0,q:e*x,r:0})
U=s.eye(4)[:,0]; X=s.eye(4)[:,2]
def bracket(F,G):return s.Matrix([sum(F[j]*s.diff(G[i],coords[j])-G[j]*s.diff(F[i],coords[j]) for j in range(4)) for i in range(4)])
N=bracket(core*U,core*X)-core*bracket(core*U,X)-core*bracket(U,core*X)
zero('core Nijenhuis actual convention',N+e*U/(2*k))
for val in [s.Rational(1,10),-s.Rational(1,10)]:
 if N.subs({e:val,x:0})==s.zeros(4,1):raise RuntimeError('nonzero sign lost')
 events.append('nonintegrable parameter '+str(val))
zero('epsilon zero matrix limit is product J',core.subs(e,0)-s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]))
# This is deliberately a different full-cutoff jet, not a rho=1 specialization.
R=e*x*x*(1+u+v*t+x*t)/2
dR=[s.diff(R,c) for c in coords]
zero('full cutoff d(Rv) minus v dR has only dv term',s.Matrix([s.diff(v*R,c)-v*dR[i]-(R if i==1 else 0) for i,c in enumerate(coords)]))
# An omitted-cutoff mutation has d beta contribution epsilon*x*d rho^dx^dv.
rho=1+u+v*t+x*t
if s.diff(rho,u)*e*x==0:raise RuntimeError('omitted-cutoff negative control unreachable')
events.append('omitted-cutoff derivative negative control nonzero')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','python_sympy':s.__version__,'checks':events,'count':len(events),'limits':'Independent finite local identities and controls; global proof is in initial attack, not inferred from code.'}
(O/'INDEPENDENT_MATH.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out))
