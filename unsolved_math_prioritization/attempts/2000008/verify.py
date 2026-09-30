from pathlib import Path
import sympy as s
import json,hashlib,random
count=0
def ck(x):
 global count
 assert x;count+=1
f=s.symbols('f0:9');h=s.symbols('h0:9');F=s.Matrix(3,3,f);H=s.Matrix(3,3,h);q=s.Matrix(3,3,range(1,10));p=s.Rational(3,2);tau=s.symbols('tau');C=F.cofactor_matrix();det=F.det()
for i in range(9):ck(s.expand(s.diff(det,f[i])-C[i])==0)
for i in range(9):ck(s.expand(s.diff((F+tau*H).cofactor_matrix()[i],tau).subs(tau,0)-sum(s.diff(C[i],f[j])*h[j] for j in range(9)))==0)
ck(s.expand(s.diff((F+tau*H).det(),tau).subs(tau,0)-sum(C[i]*h[i] for i in range(9)))==0)
L=sum(q[i]*C[i] for i in range(9))+p*det
stress=s.Matrix(3,3,[s.diff(L,v) for v in f]);x,y,z=s.symbols('x y z');coords=(x,y,z)
for k in range(1,9):
 u=s.Matrix([x+k*x*y+y*z, y+k*y*z+x*z, z+k*x*z+x*y])
 G=u.jacobian(coords);subs=dict(zip(f,G));S=stress.subs(subs,simultaneous=True);CG=G.cofactor_matrix()
 for i in range(3):
  ck(s.expand(sum(s.diff(S[i,j],coords[j]) for j in range(3)))==0)
  ck(s.expand(sum(s.diff(CG[i,j],coords[j]) for j in range(3)))==0)
 # Integrate a zero-boundary polynomial variation on the cube.
 phi=s.Matrix([x*(1-x)*y*(1-y)*z*(1-z)*v for v in (1,x+y,z+x)])
 integrand=s.expand(sum(S[i,j]*s.diff(phi[i],coords[j]) for i in range(3) for j in range(3)))
 ck(s.integrate(integrand,(x,0,1),(y,0,1),(z,0,1))==0)
r={'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'exact_assertions':count,'polynomial_deformations':8,'scope':'Symbolic first variations, Piola divergence and integrated null-Lagrangian identities; no general PDE uniqueness or counterexample computation.','dependency':'sympy'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
