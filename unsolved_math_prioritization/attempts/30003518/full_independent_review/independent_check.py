#!/usr/bin/env python3
"""Independent exact kinetic checks, using Newton traces and Routh elimination.
No author source code is imported; no floating eigenvalues or simulations.
"""
import sympy as S
from fractions import Fraction as Q
import json, math
checks=0
def ck(v):
 global checks
 assert bool(v);checks+=1
class Box:
 def __init__(self,l,h=None):self.l=Q(l);self.h=Q(l if h is None else h);assert self.l<=self.h
 def __add__(self,v):v=box(v);return Box(self.l+v.l,self.h+v.h)
 __radd__=__add__
 def __neg__(self):return Box(-self.h,-self.l)
 def __sub__(self,v):return self+-box(v)
 def __rsub__(self,v):return box(v)+-self
 def __mul__(self,v):v=box(v);a=[self.l*v.l,self.l*v.h,self.h*v.l,self.h*v.h];return Box(min(a),max(a))
 __rmul__=__mul__
 def __truediv__(self,v):v=box(v);assert v.l*v.h>0;return self*Box(1/v.h,1/v.l)
 def __rtruediv__(self,v):return box(v)/self
 def sign(self):return 1 if self.l>0 else -1 if self.h<0 else 0
 def receipt(self):return [str(self.l),str(self.h)]
def box(v):return v if isinstance(v,Box) else Box(v)
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Box(0)) for j in range(len(B[0]))] for i in range(len(A))]
e=S.symbols('e');u=[S.Rational(8),S.Rational(8)];v=[S.Rational(2),S.Rational(256)];w=[S.Rational(2),S.Rational(256)];d=[S.Rational(2),S.Rational(4),S.Rational(1,128)]
a=[u[i]/(v[i]+w[i]) for i in range(2)];q=[w[i]*a[i] for i in range(2)]
p=[S.Integer(1),q[0]*e/(d[1]+q[1]*e)];p.append(q[1]*e*p[-1]/d[2])
c0=S.cancel((8-e)/(e*sum(a[i]*p[i] for i in range(2))))
C=[S.cancel(c0*z) for z in p];B=[S.cancel(a[i]*e*C[i]) for i in range(2)];r=S.cancel(256-sum(C)-sum(B))
flux=S.cancel(r*r-(d[0]+q[0]*e)*C[0]);P=S.Poly(S.fraction(flux)[0],e).primitive()[1]
if P.LC()<0:P=-P
ck(P.all_coeffs()==[1082212609,-15125744400,54877391424,-14188516224,1182559232,-31653888,262144])
ck(S.gcd(P,P.diff()).degree()==0);ck(P.count_roots(0,8)==6);ck(P.count_roots(-S.oo,S.oo)==6)
# Build original reaction balances, then differentiate symbolically.
y=S.symbols('C0 C1 C2 B0 B1');cs=list(y[:3]);bs=list(y[3:]);ee=8-sum(bs);rr=256-sum(y)
F=[]
F.append(rr*rr-d[0]*cs[0]-u[0]*ee*cs[0]+v[0]*bs[0])
F.append(w[0]*bs[0]-d[1]*cs[1]-u[1]*ee*cs[1]+v[1]*bs[1])
F.append(w[1]*bs[1]-d[2]*cs[2])
F.extend(u[i]*ee*cs[i]-(v[i]+w[i])*bs[i] for i in range(2))
J=S.Matrix(F).jacobian(y)
subs=dict(zip(y,C+B))
for z in F:
 num=S.Poly(S.fraction(S.cancel(z.subs(subs)))[0],e)
 ck(num.rem(P).is_zero)
ck(S.cancel(e+sum(B)-8)==0)
# Evaluate rational expressions using outward rational interval arithmetic.
def polynomial(expr,x):
 out=Box(0)
 for z in S.Poly(expr,e).all_coeffs():out=out*x+Q(z)
 return out
def rational(expr,x):
 nu,de=S.fraction(S.cancel(expr));return polynomial(nu,x)/polynomial(de,x)
Jr=J.subs(subs).applyfunc(S.cancel)
intervals=S.intervals(P,eps=S.Rational(1,10**30));rows=[]
for idx,((l,h),mult) in enumerate(intervals,1):
 ck(mult==1 and P.count_roots(l,h)==1);E=Box(Q(l),Q(h));R=rational(r,E)
 ck(R.sign()!=0);row={'root_index':idx,'e_interval':E.receipt(),'physical':R.sign()==1,'r_sign':R.sign()}
 for expr in C+B+[e,8-e]:ck(rational(expr,E).sign()==1)
 if R.sign()==1:
  mat=[[rational(Jr[i,j],E) for j in range(5)] for i in range(5)]
  power=[[Box(int(i==j)) for j in range(5)] for i in range(5)];traces=[]
  for k in range(1,6):power=mm(power,mat);traces.append(sum((power[i][i] for i in range(5)),Box(0)))
  # Newton identities for det(lambda I - J), distinct from principal-minor enumeration.
  coeff=[Box(1)]
  for k in range(1,6):coeff.append(-sum((coeff[k-j]*traces[j-1] for j in range(1,k+1)),Box(0))/k)
  table=[[coeff[0],coeff[2],coeff[4]],[coeff[1],coeff[3],coeff[5]]]
  for k in range(2,6):
   before,prev=table[-2],table[-1];ck(prev[0].sign()!=0)
   table.append([(prev[0]*before[j+1]-before[0]*prev[j+1])/prev[0] for j in range(2)]+[Box(0)])
  signs=[row[0].sign() for row in table];ck(all(signs))
  changes=sum(a!=b for a,b in zip(signs,signs[1:]));ck(changes==(1 if idx==3 else 0))
  row.update(routh_first_column_signs=signs,right_half_plane_roots=changes,routh_first_column_outward_integers=[[math.floor(z[0].l),math.ceil(z[0].h)] for z in table])
 rows.append(row)
ck([r['root_index'] for r in rows if r['physical']]==[2,3,6])
# General-chain construction with independently selected positive rational rates.
for N in range(1,11):
 ds=[S.Rational(i+2,i+1) for i in range(N+1)];us=[S.Rational(i+3,i+2) for i in range(N)];vs=[S.Rational(i+4,i+1) for i in range(N)];ws=[S.Rational(i+2,i+3) for i in range(N)]
 aa=[us[i]/(vs[i]+ws[i]) for i in range(N)];qq=[ws[i]*aa[i] for i in range(N)]
 pp=[S.Integer(1)]
 for i in range(1,N):pp.append(S.cancel(qq[i-1]*e*pp[-1]/(ds[i]+qq[i]*e)))
 pp.append(S.cancel(qq[-1]*e*pp[-1]/ds[-1]))
 QQ=S.prod(ds[i]+qq[i]*e for i in range(1,N));PP=[S.cancel(QQ*z) for z in pp]
 for i,z in enumerate(PP):ck(S.Poly(z,e).degree()<=(N if i==N else N-1))
 for i in range(1,N):ck(S.cancel(qq[i-1]*e*pp[i-1]-(ds[i]+qq[i]*e)*pp[i])==0)
 ck(S.cancel(qq[-1]*e*pp[-2]-ds[-1]*pp[-1])==0)
 for ee0 in [S.Rational(1,3),S.Rational(3,2)]:
  cstar=[S.Rational(2,5)*z.subs(e,ee0) for z in pp];bstar=[aa[i]*ee0*cstar[i] for i in range(N)]
  for z in cstar+bstar:ck(z>0)
  free_r=S.Rational(7,3);free_m=S.Rational(11,4);kk=(ds[0]+qq[0]*ee0)*cstar[0]/(free_r*free_m)
  ck(kk>0);ck(S.cancel(kk*free_r*free_m-sum(ds[i]*cstar[i] for i in range(N+1)))==0)
# Shared-rate geometric identities and strict positive decomposition.
z=S.symbols('z')
for N in range(1,31):
 geom=sum(z**i for i in range(N));ck(S.expand((1-z)*geom+z**N-1)==0)
 ck(S.expand(1-z**N-N*z**N*(1-z)-(1-z)*(geom-N*z**N))==0)
 for zz in [S.Rational(1,100),S.Rational(1,2),S.Rational(99,100)]:ck((geom-N*z**N).subs(z,zz)>0)
# Actual retained-coordinate Jacobian negative cycle and conservation for shared rates.
for N in range(2,9):
 rr0=S.symbols('r');DD,ET,uu,vv,ww,nu,kk=S.symbols('D ET u v w nu k',positive=True);CC=S.symbols('c:'+str(N+1));BB=S.symbols('b:'+str(N));EE=ET-sum(BB);vars=[rr0,*CC,*BB]
 FF=[-kk*rr0*(rr0+DD)+nu*sum(CC),kk*rr0*(rr0+DD)-nu*CC[0]-uu*CC[0]*EE+vv*BB[0]]
 FF.extend(ww*BB[i-1]-nu*CC[i]-uu*CC[i]*EE+vv*BB[i] for i in range(1,N));FF.append(ww*BB[N-1]-nu*CC[N]);FF.extend(uu*CC[i]*EE-(vv+ww)*BB[i] for i in range(N))
 jac=S.Matrix(FF).jacobian(vars);ck(S.expand(sum(FF))==0)
 for j in range(len(vars)):ck(S.expand(sum(jac[:,j]))==0)
 iC1=2;iB0=N+2;iB1=N+3
 ck(S.expand(jac[iC1,iB0]-(ww+uu*CC[1]))==0);ck(S.expand(jac[iB1,iC1]-uu*EE)==0);ck(S.expand(jac[iB0,iB1]+uu*CC[0])==0)
print(json.dumps({'status':'PASS','exact_assertions':checks,'stability_method':'independent interval Newton traces plus regular Routh elimination','root_rows':rows,'all_N_checks_through':10,'shared_identities_through':30,'negative_cycle_N_through':8,'floating_point_used':False},indent=2))
