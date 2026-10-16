"""New finite reconstruction controls, not a proof of global existence or priority."""
import json,itertools,sys
import sympy as s

def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def zero(z):require(s.cancel(s.together(z))==0,'Nonzero residual '+str(z))
x=s.symbols('x0:3');u=s.symbols('u0:3'); n=3
# A fresh three-dimensional scalar-jet chain-rule example with cubic chart terms.
h=s.Matrix([u[0]+u[1]*u[2]+u[0]**3,u[1]+u[0]**2,u[2]+u[1]**2])
J=h.jacobian(u); origin={q:0 for q in u};require(J.subs(origin).det()==1,'chart rank')
g=s.eye(3)+s.Matrix(x)*s.Matrix(x).T+s.diag(*[1+x[i]**2 for i in range(3)])
C=lambda i,j,k:s.Integer(1+i+j+k)+sum(x)
Q=lambda i,j,k:(s.diff(g[j,k],x[i])+s.diff(g[i,k],x[j])+s.diff(g[i,j],x[k])-C(i,j,k))/2
at={q:0 for q in x}; q=sum(g[i,j].subs(at)*x[i]*x[j]/2 for i,j in itertools.product(range(n),repeat=2))+sum(Q(i,j,k).subs(at)*x[i]*x[j]*x[k]/6 for i,j,k in itertools.product(range(n),repeat=3))
qu=q.subs(dict(zip(x,h)),simultaneous=True)
gu=J.T*g.subs(dict(zip(x,h)),simultaneous=True)*J
count=0; tensor_false=0
for i,j,k in itertools.product(range(n),repeat=3):
 cu=sum(C(a,b,c).subs(dict(zip(x,h)),simultaneous=True)*J[a,i]*J[b,j]*J[c,k] for a,b,c in itertools.product(range(n),repeat=3))
 wanted=(s.diff(gu[j,k],u[i])+s.diff(gu[i,k],u[j])+s.diff(gu[i,j],u[k])-cu)/2
 actual=s.diff(qu,u[i],u[j],u[k]).subs(origin);zero(actual-wanted.subs(origin));count+=1
 tensor_only=sum(Q(a,b,c).subs(at)*J[a,i]*J[b,j]*J[c,k] for a,b,c in itertools.product(range(n),repeat=3)).subs(origin)
 tensor_false+=int(actual!=tensor_only)
require(tensor_false>0,'tensor-only negative control insensitive')
# Rank of full0..3 jets for 120 common polynomial features on a nonlinear R3 graph in R7.
e=[x[0],x[1],x[2],x[0]*x[1],x[1]*x[2],x[0]**2+x[2]**2,x[0]*x[1]*x[2]]
def multis(n,d):return [a for a in itertools.product(range(d+1),repeat=n) if sum(a)<=d]
alpha=multis(3,3);powers=multis(7,3)
F=[s.prod(e[i]**a[i] for i in range(7)) for a in powers]
def deriv(f,a):
 for z,k in zip(x,a):f=s.diff(f,z,k)
 return f
E=s.Matrix([[deriv(f,a).subs(at) for f in F] for a in alpha]);require(E.shape==(20,120),'feature count');require(E.rank()==20,'full jet rank')
R=E.T*(E*E.T).inv();require(E*R==s.eye(20),'right inverse')
# Degree2 features cannot carry arbitrary3-jets on the affine R3 immersion.
F2=[s.prod(x[i]**a[i] for i in range(3)) for a in multis(3,2)]
E2=s.Matrix([[deriv(f,a) for f in F2] for a in alpha]);require(E2.rank()==10,'quadratic negative control')
# Direct ambient polynomial extension of an exact cubic-feature curve; actual Hessian,
# not just a manufactured matrix. Complement coordinates need no normal-frame claim.
t,c,y,z=s.symbols('t c y z');V=s.Matrix([1,t,t*t,t**3]);metric=1+t*t;cubic=1+t**3;gamma=(s.diff(metric,t)-cubic)/2
Ev=s.Matrix.vstack(*[V.diff(t,k).T for k in range(4)])
a=Ev.inv()*s.Matrix([0,0,metric,s.diff(metric,t)+gamma]);phi=-a
for res in [phi.dot(V.diff(t)),phi.diff(t).dot(V.diff(t))-metric,phi.diff(t).dot(V.diff(t,2))-gamma]:zero(res)
nu=s.Matrix([c-1,y-t*t,z-t**3]); normalphi=s.Matrix([phi[0],phi[2],phi[3]])
# At each exact basepoint choose the same trace-HS correction mechanism in the graph frame.
P0=(normalphi.T*nu)[0];H0=s.hessian(P0,(t,c,y,z));curve={c:1,y:t*t,z:t**3}
T=s.Matrix([0,1,2*t,3*t*t]); # Ambient coordinate order below is (c,t,y,z).
H0=s.hessian(P0,(c,t,y,z)).subs(curve)
W=s.Matrix.hstack(T,s.Matrix([1,0,0,0]),s.Matrix([0,0,1,0]),s.Matrix([0,0,0,1]));blocks=s.simplify(W.T*H0*W)
zero(blocks[0,0]-metric);require(blocks[1:,1:]==s.zeros(3),'linear fiber normal block')
B=blocks[:1,1:];tau=s.simplify(sum(v*v for v in B)/metric);lam=1+tau
Psi=P0+lam*(nu.T*nu)[0];H=s.hessian(Psi,(c,t,y,z)).subs(curve)
zero((H*T-phi.diff(t))[0]); # Full derivative check uses ambient gradient ordering.
for i in range(4):zero((H*T)[i]-phi.diff(t)[i])
completed=s.simplify(W.T*H*W)
for entry in completed[1:,1:]-2*lam*s.eye(3):zero(entry)
samples=[]
for v in [s.Rational(-7,3),s.Integer(0),s.Rational(11,2)]:
 Hv=H.subs(t,v);minors=[s.factor(Hv[:i,:i].det()) for i in range(1,5)];require(all(p>0 for p in minors),'actual Hessian positivity')
 induced=s.factor((V.diff(t,2).T*H*V.diff(t))[0].subs(t,v));require(induced==gamma.subs(t,v),'induced connection')
 samples.append({'t':str(v),'leading_principal_minors':[str(p) for p in minors],'lowered_induced_connection':str(induced)})
# Wrong conormal sign and omitted connection are sensitive failures.
require(s.expand(a.diff(t).dot(V.diff(t))+metric)==0,'wrong-sign negative control')
wrong=-Ev.inv()*s.Matrix([0,0,metric,s.diff(metric,t)]);zero(wrong.diff(t).dot(V.diff(t,2)));require(gamma!=0,'connection omission sensitivity')
print(json.dumps(dict(status='PASS',python=sys.version.split()[0],sympy=s.__version__,three_dimensional_chain_rule_entries=count,tensor_only_failures=tensor_false,full_jet_shape=list(E.shape),full_jet_rank=20,right_inverse_exact=True,quadratic_negative_rank=10,actual_ambient_hessian_samples=samples,connection_and_sign_negative_controls=True,limits='Finite exact checks only; no arbitrary-manifold global extension, source interpretation, novelty, or priority certification.'),indent=2))
