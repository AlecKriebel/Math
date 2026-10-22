"""Round04 exact finite support for independently written initial attack."""
import sympy as s,json,datetime,pathlib
ru,rx,rt=s.symbols('ru rx rt',real=True);D=1-rx-rt**2/4
A=s.Matrix([[0,0,1,0],[0,0,0,-1],[-1,0,0,0],[0,1,0,0]])
F=s.Matrix([[0,ru,0,1],[-ru,0,1-rx,-rt],[0,rx-1,0,0],[-1,rt,0,0]])
G=F-rt*A/2;Q=-A.inv()*G;checks=[]
def zero(label,M):
 if any(s.simplify(x)!=0 for x in M):raise RuntimeError(label)
 checks.append(label)
zero('full-cutoff unnormalized J square is -D identity',Q*Q+D*s.eye(4));zero('full-cutoff alpha anti-invariance',Q.T*A*Q+D*A);zero('full-cutoff beta anti-invariance',Q.T*F*Q+D*F)
u,v,x,t,e=s.symbols('u v x t e',real=True);coords=(u,v,x,t);k=1-e*x;J=Q.subs({ru:0,rt:0,rx:e*x})/s.sqrt(k)
U=s.eye(4)[:,0];X=s.eye(4)[:,2]
def bracket(a,b):return b.jacobian(coords)*a-a.jacobian(coords)*b
N=bracket(J*U,J*X)-J*bracket(J*U,X)-J*bracket(U,J*X)
zero('core Nijenhuis correct sign and convention',N+e/(2*k)*U);zero('parameter zero recovers correct J0 sign',J.subs(e,0)-s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]))
for value in (s.Rational(-1,10),s.Rational(1,10)):
 if s.simplify(N[0].subs({e:value,x:0}))==0:raise RuntimeError('nonzero sign lost')
checks.append('both parameter signs nonzero at origin')
if s.simplify(N[0].subs(e,0))!=0:raise RuntimeError('integrable limit wrong')
checks.append('integrable parameter limit zero obstruction')
O=pathlib.Path(__file__).parent;out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':checks,'sympy':s.__version__,'limits':'Finite algebra only. Smooth compactification, class independence, global gluing and topology follow from the written proof, not these checks. Zero new author proof responses.'};p=O/'INDEPENDENT_ALGEBRA.json';q=p.with_suffix('.json.tmp');q.write_text(json.dumps(out,indent=2)+'\n');q.replace(p);print(json.dumps(out))
