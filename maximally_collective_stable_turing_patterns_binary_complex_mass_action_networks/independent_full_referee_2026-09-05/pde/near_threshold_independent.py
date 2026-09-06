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

e=s.symbols('e',positive=True); lam=s.symbols('lam')
A,B=derivative(3); r=s.Matrix([1,-(1+R(16,9)*e+e**2/2),-e,R(1,2)-R(13,18)*e])
ds=[s.factor(v/r[i]) for i,v in enumerate(A*r)]; D=s.diag(*ds); M=A-D
ell=M.T.nullspace()[0]; ell=ell/ell[-1]
c=s.Matrix([0,4,2,1]); rho=s.Matrix([2,-2,0,1])
forcing=-B(r,r)/4
border=A.row_join(rho).col_join(c.T.row_join(s.zeros(1)))
w0=(border.inv()*forcing.col_join(s.zeros(1,1)))[:-1,0]
w2=(A-4*D).inv()*forcing
cubic=s.factor((ell.T*(B(r,w0)+B(r,w2)/2))[0]/(ell.T*r)[0])
targetN=(18718533*e**12+746773020*e**11+6223086873*e**10+19157763816*e**9+12668661720*e**8-49876101168*e**7-103878539968*e**6-37609207926*e**5+68189826636*e**4+62316267192*e**3+9680484312*e**2-3464522928*e-238085568)
D1=81*e**4+531*e**3+708*e**2-1102*e-1182
D2=243*e**6+2133*e**5+7431*e**4+5047*e**3-10329*e**2-17415*e-3402
assert s.factor(cubic+targetN/(13608*D1*D2))==0
assert s.limit(cubic,e,0)==R(6,1379)
assert s.limit((cubic-R(6,1379))/e,e,0)==R(421985,11409846)
print("near threshold reaction-derived cubic and printed expansion PASS")
char=s.Poly(s.factor((lam*s.eye(4)-M).det()/lam),lam)
print("D",list(map(str,ds)))
print("eta",s.factor((ell.T*D*r)[0]/(ell.T*r)[0]))
print("first quotient",s.factor(char.as_expr()))
print("first RH",s.factor(char.all_coeffs()[1]*char.all_coeffs()[2]-char.all_coeffs()[3]))
print("NEAR_THRESHOLD_RECONSTRUCTION_PASS")

t,v,z=s.symbols('t v z',nonnegative=True)
g1=lam+2+t*ds[0]; g2=lam+1+t*ds[1]; gm=lam+5+t*ds[2]; gz=lam+4+t*ds[3]
poly=s.Poly(s.expand(g2*(g1*gm*gz-4*g1-4*gm+gz)-(gz*(4*g1+gm)-36)),lam)
aa=[s.factor(x) for x in poly.all_coeffs()]
p1,p2,p3,p4=aa[1:]
H2=s.factor(p1*p2-p3); H3=s.factor(p3*H2-p1**2*p4)
cert={}
for name,expr in [('a1',p1),('a2',p2),('a3',p3),('a4_over_t_minus_1',s.factor(p4/(t-1))),('H2',H2),('H3',H3)]:
 sub=s.factor(expr.subs({t:1+v,e:1/(1000*(1+z))}))
 n,d=s.fraction(sub); pn=s.Poly(n,v,z); pd=s.Poly(d,v,z)
 cn=pn.coeffs(); cd=pd.coeffs()
 if all(x<0 for x in cd): cn=[-x for x in cn]; cd=[-x for x in cd]
 ok=all(x>=0 for x in cn) and all(x>=0 for x in cd) and pn.eval({v:0,z:0})/pd.eval({v:0,z:0})>0
 print('NEAR_LINEAR_CERT',name,ok,len(cn),min(cn)>0,flush=True)
 assert ok
 cert[name]={'numerator_terms':len(cn),'denominator_terms':len(cd),'all_coefficients_nonnegative':True}
print('NEAR_THRESHOLD_ALL_HIGHER_MODES_AND_SIMPLE_FIRST_EXACT_PASS')
