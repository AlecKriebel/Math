import sympy as s,json,datetime,os
from pathlib import Path
p,q,r=s.symbols('R_u R_x R_t',real=True);D=1-q-r*r/4;h=s.sqrt(D)
A=s.Matrix([[0,0,1,0],[0,0,0,-1],[-1,0,0,0],[0,1,0,0]])
Be=s.Matrix([[0,p,0,1],[-p,0,1-q,-r],[0,q-1,0,0],[-1,r,0,0]])
B=(Be-r*A/2)/h;J=-A.inv()*B
checks=[]
def equal(name,L,H):
 if s.simplify(L-H)!=s.zeros(*L.shape):raise RuntimeError(name)
 checks.append(name)
equal('full cutoff J^2=-Id',J*J,-s.eye(4));equal('full cutoff alpha anti-invariance',J.T*A*J,-A);equal('full cutoff beta_e anti-invariance',J.T*Be*J,-Be)
u,v=s.symbols('u v',real=True);Ga=u*A-v*Be;equal('full cutoff gamma_e anti-invariance',J.T*Ga*J,-Ga)
J0=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]);equal('kernel convention fixes J0 at zero jet',J.subs({p:0,q:0,r:0}),J0)
assert s.simplify(J[2,1])==-p/h and s.simplify(J[3,0])==-p/h;checks.append('R_u retained in real J off-diagonal entries')
for Q in [-s.Rational(1,4),s.Rational(1,4)]:
 for T in [-1,1]:assert D.subs({q:Q,r:T})>=s.Rational(1,2)
checks.append('all exact corners of stated positivity box')
# Reject a wrongly signed third-form correction at a concrete admissible jet.
beta0=Be.subs({p:0,q:0,r:0});beta_new=Be.subs({p:0,q:s.Rational(1,4),r:0});gamma_bad=A-beta0+(beta_new-beta0)
vec=lambda m:s.Matrix([m[i,j] for i in range(4) for j in range(i+1,4)])
assert s.Matrix.hstack(vec(A),vec(beta_new),vec(gamma_bad)).rank()==3;checks.append('wrong third-correction sign produces rank3 and is rejected')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':checks,'general_J':str(J),'limits':'Algebraic full-jet controls only. Positive square root D>0 and geometric gluing are proved in prose.'};raw=(json.dumps(result,indent=2)+'\n').encode();target=Path(__file__).with_name('GENERAL_MATRIX_RESULT.json')
with target.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert target.read_bytes()==raw;print(json.dumps({'status':'PASS','checks':len(checks)}))
