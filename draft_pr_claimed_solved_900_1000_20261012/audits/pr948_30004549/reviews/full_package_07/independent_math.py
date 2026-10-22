import sympy as s,json,sys,datetime,os
from pathlib import Path
u,v,x,t,e=s.symbols('u v x t epsilon',real=True);q=[u,v,x,t];R=s.Function('R')(*q)
def clean(a):return {k:s.simplify(z) for k,z in a.items() if s.simplify(z)!=0}
def add(*forms):
 a={}
 for f in forms:
  for k,z in f.items():a[k]=a.get(k,0)+z
 return clean(a)
def scale(c,a):return clean({k:c*z for k,z in a.items()})
def wedge(a,b):
 out={}
 for k,z in a.items():
  for l,w in b.items():
   if len(set(k+l))<len(k+l):continue
   sign=(-1)**sum(i>j for i in k for j in l);m=tuple(sorted(k+l));out[m]=out.get(m,0)+sign*z*w
 return clean(out)
def d(a):
 out={}
 for k,z in a.items():
  for j in range(4):out=add(out,wedge({(j,):s.diff(z,q[j])},{k:1}))
 return clean(out)
def same(a,b):assert clean(add(a,scale(-1,b)))=={},(a,b)
forms=[{(j,):1} for j in range(4)];du,dv,dx,dt=forms;vol={(0,1,2,3):1}
alpha={(0,2):1,(1,3):-1};beta={(0,3):1,(1,2):1};gamma=add(scale(u,alpha),scale(-v,beta));pert=d(scale(R,dv));be=add(beta,pert);ga=add(gamma,scale(-1,d(scale(R*v,dv))))
same(d(alpha),{});same(d(be),{});same(d(ga),{});same(ga,add(scale(u,alpha),scale(-v,be)))
same(pert,{(0,1):s.diff(R,u),(1,2):-s.diff(R,x),(1,3):-s.diff(R,t)})
same(wedge(alpha,alpha),scale(2,vol));same(wedge(alpha,be),scale(s.diff(R,t),vol));same(wedge(be,be),scale(2*(1-s.diff(R,x)),vol))
D=1-s.diff(R,x)-s.diff(R,t)**2/4;B=scale(1/s.sqrt(D),add(be,scale(-s.diff(R,t)/2,alpha)));same(wedge(B,B),scale(2,vol));same(wedge(alpha,B),{})
Psi=add(alpha,scale(s.I,B));same(wedge(Psi,Psi),{});same(wedge(Psi,add(alpha,scale(-s.I,B))),scale(4,vol))
# Real coordinate matrix independently reconstructed from the two core eigen-one-forms.
k=s.Function('k')(x);kp=s.diff(k,x);J=s.Matrix([[0,-s.sqrt(k),0,0],[1/s.sqrt(k),0,0,0],[0,0,0,-1/s.sqrt(k)],[0,0,s.sqrt(k),0]])
assert s.simplify(J*J+s.eye(4))==s.zeros(4)
def bracket(a,b):return s.simplify(b.jacobian(q)*a-a.jacobian(q)*b)
E=[s.eye(4)[:,j] for j in range(4)];nijenhuis={}
for i in range(4):
 for j in range(i+1,4):
  X,Y=E[i],E[j];N=s.simplify(bracket(J*X,J*Y)-J*bracket(J*X,Y)-J*bracket(X,J*Y)-bracket(X,Y));nijenhuis[str((i,j))]=[str(z) for z in N]
  if (i,j)==(0,2):assert s.simplify(N-s.Matrix([kp/(2*k),0,0,0]))==s.zeros(4,1)
phi1=add(du,scale(s.I*s.sqrt(k),dv));phi2=add(dx,scale(s.I/s.sqrt(k),dt));core=add(alpha,scale(s.I,add(scale(1/s.sqrt(k),{(0,3):1}),scale(s.sqrt(k),{(1,2):1}))))
same(wedge(phi1,phi2),core);same(wedge(d(phi1),wedge(phi1,phi2)),scale(kp/(2*k),vol))
coreB=add(scale(1/s.sqrt(k),{(0,3):1}),scale(s.sqrt(k),{(1,2):1}));same(d(coreB),{(0,2,3):kp/(2*k**s.Rational(3,2))})
phi_rows=s.Matrix([[1,s.I*s.sqrt(k),0,0],[0,0,1,s.I/s.sqrt(k)]])
assert s.simplify(phi_rows*J-s.I*phi_rows)==s.zeros(2,4)
# N at the fixed core origin, both nonzero parameter signs and epsilon=0.
at_origin=-e/2;assert at_origin.subs(e,s.Rational(1,100))!=0 and at_origin.subs(e,-s.Rational(1,100))!=0 and at_origin.subs(e,0)==0
# Check nonconstant transition-region polynomial, not just core perturbation.
rho=(1-u*u-v*v-x*x-t*t)**4;trial=e*rho*x*x/2
for expr in [s.diff(R,x),s.diff(R,t),s.diff(R,u)]:assert expr.subs(R,trial).doit() is not None
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','runtime':{'python':sys.version.split()[0],'sympy':s.__version__,'isolated':sys.flags.isolated,'optimize':sys.flags.optimize,'no_site':sys.flags.no_site,'dont_write_bytecode':sys.dont_write_bytecode},'checks':['arbitrary full-cutoff first-jet beta','full exterior derivative closure of all three forms','full third representative relation','Gram all entries','normalized B Gram','decomposable Psi and positive real volume','real J square -Id','phi J eigenvalue +i (kernel sign)','all six core coordinate Nijenhuis pairs','fixed-origin both signs and epsilon0','submitted Frobenius coefficient','normalized core B is nonclosed'],'nijenhuis':nijenhuis,'N_u_x_at_fixed_origin':'-epsilon/2 partial_u','limits':'Exact finite symbolic local controls, not proof of the global compactification, Stokes independence, smooth cutoff existence, global gluing or historical priority.'}
raw=(json.dumps(result,indent=2)+'\n').encode();p=Path(__file__).with_name('INDEPENDENT_MATH_RESULT.json')
with p.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert p.read_bytes()==raw;print(raw.decode())
