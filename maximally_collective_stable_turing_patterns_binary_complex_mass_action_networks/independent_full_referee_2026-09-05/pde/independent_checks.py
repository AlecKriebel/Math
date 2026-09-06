import json
import sympy as s
import numpy as np
R=s.Rational
out={"exact":[],"spectral_probes":[]}
def reactions(m):
 return [({}, {0:1})]+[({0:1,i:1},{0:1,i+1:1}) for i in range(1,m-2)]+[({0:1,m-2:1},{m-1:2}),({m-1:2},{1:1}),({m:2},{0:1,m-1:1}),({0:1,m-1:1},{m:2})]
def derivative(m,exact=True):
 n=m+1; A=s.zeros(n) if exact else np.zeros((n,n)); ts=[]
 for src,dst in reactions(m):
  y=[src.get(j,0) for j in range(n)]; v=[dst.get(j,0)-y[j] for j in range(n)]
  if exact:
   y,v=s.Matrix(y),s.Matrix(v); A+=v*y.T; ts.append((v,y*y.T-s.diag(*y)))
  else: A+=np.outer(v,y)
 def B(u,v): return sum((b*(u.T*T*v)[0] for b,T in ts),s.zeros(n,1))
 return A,B
def selected(m):
 K=lambda i:91*m-181-i
 r=s.Matrix([1]+[-R(K(i),63*(m-2)) for i in range(2,m)]+[-R(2,9),R(5,14)])
 D=s.diag(R(23,63),*[R(1,K(i)) for i in range(2,m)],R(1,7),R(16,45))
 ell=s.Matrix([-R(266,815)]+[R(78260*(m-2),163*K(i-1)) for i in range(2,m)]+[R(18368,7335),1])
 return r,D,ell
def Ntarget(m,h):
 Q=589180301*m**3-3500015940*m**2+6930529579*m-4574434500
 PR=68605040480814208768*m**4-550882186169626030957*m**3+1658612632937449670852*m**2-2219226476204103501323*m+1113379274975809565700
 PC=652054120726848*m**4-5151971981328467*m**3+15265080924982572*m**2-20102347725659113*m+9927281930180400
 return PR/(s.Integer(286118780220)*(8*m-17)*Q)-215*PC*h/(s.Integer(11645046)*(8*m-17)*Q)
for m in (3,4,7,10):
 A,B=derivative(m); r,D,ell=selected(m)
 c=s.Matrix([0]+[4]*(m-2)+[2,1]); rho=s.Matrix([2]+[-2]*(m-2)+[0,1])
 assert A*rho==s.zeros(m+1,1) and c.T*A==s.zeros(1,m+1)
 assert (A-D)*r==s.zeros(m+1,1) and ell.T*(A-D)==s.zeros(1,m+1)
 forcing=-B(r,r)/4; assert (c.T*forcing)[0]==0
 border=A.row_join(rho).col_join(c.T.row_join(s.zeros(1)))
 sol=border.inv()*forcing.col_join(s.zeros(1,1)); assert sol[-1]==0
 w0=sol[:-1,0]; w2=(A-4*D).inv()*forcing
 N=(ell.T*(B(r,w0)+B(r,w2)/2))[0]
 h=sum(R(1,91*m-181-j) for j in range(1,m-1))
 assert s.factor(N-Ntarget(m,h))==0 and N>R(1,100)
 assert (ell.T*r)[0]<0 and (ell.T*D*r)[0]<0
 rec={"m":m,"cubic":float(N/(ell.T*r)[0]),"eta":float((ell.T*D*r)[0]/(ell.T*r)[0]),"N_ref":float(N)}
 if m in (3,4):
  L=s.symbols('L',positive=True)
  hi=[1]+[R(91*m-181-i,91*m-180-i)/L for i in range(2,m)]+[1,1]
  Hi=s.diag(*[s.Integer(1)/v for v in hi]); gauge=Hi*c
  tau=s.factor(-(gauge.T*w0)[0]/(gauge.T*rho)[0]); assert s.factor((gauge.T*(w0+tau*rho))[0])==0
  S=(ell.T*B(r,rho))[0]; assert s.factor(S+4*(1760850*h-10253)/462105)==0
  assert s.factor((ell.T*Hi*r)[0]+R(485873,924210)+R(11180,1467)*L*(m-2))==0
  Ns=(ell.T*(B(r,w0+tau*rho)+B(r,w2)/2))[0]; assert s.factor(Ns-N-tau*S)==0
  nu=m-2
  At=1494249120*h*L*nu**2-69786990*h*L*nu+108738630*L*nu**2+1214388*L*nu-8521*L-125249670*nu**2+1031940*nu
  Bt=32760*h*L*nu+32760*L*nu**2+4*L-4095*nu
  assert s.factor(tau+At/(15876*(8*nu-1)*Bt))==0
  rec["symbolic_L_gauge"]="PASS"
 out["exact"].append(rec)
q,rc,g1,gm,gz=s.symbols('q rc g1 gm gz',nonzero=True)
M=s.Matrix([[g1,1/rc,1,-2],[1,q,-2,0],[-1,-2/rc,gm,-2],[-2,0,-2,gz]])
F=g1*gm*gz-4*g1-4*gm+gz; G=gz*(4*g1+gm)-36
assert s.factor(rc*M.det()-(q*rc*F-G))==0
out["generic_schur"]="PASS"
x,y,z,ss,a,u=s.symbols('x y z ss a u',real=True); lam=x+s.I*y
def modulus(poly):
 p=s.Poly(s.expand(poly*s.conjugate(poly)),y)
 assert all(k[0]%2==0 for k,c in p.terms())
 return s.expand(sum(c*z**(k[0]//2) for k,c in p.terms()))
P=lam**4+12*lam**3+42*lam**2+47*lam+16; R0=5*lam**2+33*lam+16; F0=lam**3+11*lam**2+31*lam+16
g1=lam+2+R(23,63)*(1+ss); gm=lam+5+R(1,7)*(1+ss); gz=lam+4+R(16,45)*(1+ss)
F=g1*gm*gz-4*g1-4*gm+gz; G=gz*(4*g1+gm)-36
certs=[(35,modulus((1+lam)*P)-modulus(R0),(x,z)),(77,(R(91,90)**2+z)*modulus(F)-modulus(G),(x,z,ss)),(84,R(91,90)**2*(1+a*x+z/3)*modulus(F)-modulus(G),(x,z,ss)),(22,(1+(u+R(1,4))*x+R(5,4)*z)*modulus(F0)-modulus(R0),(x,z))]
for n,e,vv in certs:
 p=s.Poly(e,*vv); assert len(p.terms())==n and p.coeff_monomial(1)==0
 for k,c in p.terms(): assert all(v>=0 for v in s.Poly(c,a,u).coeffs())
 for v in vv: assert any(p.coeff_monomial(v**k).subs({a:1,u:0})>0 for k in range(1,8))
out["modulus_coefficients_and_equality_support"]="35/77/84/22 PASS"
print(json.dumps(out),flush=True)
for m in (3,4,20,148,149,150,256):
 A,_=derivative(m,False); _,D,_=selected(m); D=np.array(D,dtype=float); nu=m-2
 lo=1/np.sqrt(3) if nu==1 else np.sqrt(5/(4*nu)); hi=90*nu/(90*nu+1)
 cases=[("unit",None),("lower",lo),("upper",hi)]
 if m==149: cases.append(("outside_range_legacy",1/21))
 for name,L in cases:
  H=np.eye(m+1) if L is None else np.diag([1]+[(91*m-181-i)/(L*(91*m-180-i)) for i in range(2,m)]+[1,1])
  modes=[]
  for k in (0,1,2,3):
   vals=np.linalg.eigvals(H@(A-k*k*D))
   if k in (0,1):
    j=int(np.argmin(np.abs(vals))); assert abs(vals[j])<1e-7; vals=np.delete(vals,j)
   maximum=float(max(vals.real))
   if name!="outside_range_legacy": assert maximum<0
   if name=="outside_range_legacy" and k==0: assert maximum>0
   modes.append({"k":k,"complementary_abscissa":maximum})
  rec={"m":m,"case":name,"L":L,"modes":modes}; out["spectral_probes"].append(rec); print(json.dumps(rec),flush=True)
print("ALL_INDEPENDENT_CHECKS_PASS",flush=True)
try:
 from pathlib import Path
 Path('scratch/results.json').write_text(json.dumps(out,indent=2)+'\n')
except OSError as e: print("RESULT_FILE_WRITE_FAILED",str(e))
