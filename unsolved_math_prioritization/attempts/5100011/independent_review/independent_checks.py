#!/usr/bin/env python3
"""Independent k203,a reviewer controls: exact algebra and geometric diagnostics.
Written separately from the author checker. No downloaded executable code.
"""
from fractions import Fraction as F
from math import gcd
from collections import Counter
from pathlib import Path
import json
import sympy as sp
C=Counter();D=Counter()
def check(g,b):assert b,g;C[g]+=1
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return sum(a*b for a,b in zip(p,q))
def sub(p,q):return tuple(a-b for a,b in zip(p,q))
def area(p):return sum(cross(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2

def pedal(p,M):
 out=[]
 for i,x in enumerate(p):
  y=p[(i+1)%len(p)];d=sub(y,x);n=(-d[1],d[0]);s=(dot(M,n)-dot(x,n))/dot(n,n)
  out.append(tuple(M[j]-s*n[j] for j in range(2)))
 return out

# Exact matrix form of the radial telescoping identity, without unit tangents.
a,b,c,d,x,y=sp.symbols('a b c d x y');t=sp.Matrix([a,b]);s=sp.Matrix([c,d]);M=sp.Matrix([x,y])
pt=t*(t.dot(M))/(t.dot(t));ps=s*(s.dot(M))/(s.dot(s))
gt=cross(t,M)*t.dot(M)/t.dot(t);gs=cross(s,M)*s.dot(M)/s.dot(s)
rhs=(x*x+y*y)*cross(t,s)*t.dot(s)/(2*t.dot(t)*s.dot(s))+(gt-gs)/2
check('symbolic_radial_telescope',sp.cancel(cross(pt,ps)-rhs)==0)
# The exact edge cross-product numerator reduction used by the area trace.
su,sv,cu,cv,du,dv,k2=sp.symbols('su sv cu cv du dv k2');den=1-k2*su**2*sv**2
snplus=(su*cv*dv+sv*cu*du)/den;snminus=(su*cv*dv-sv*cu*du)/den
cnplus=(cu*cv-su*sv*du*dv)/den;cnminus=(cu*cv+su*sv*du*dv)/den
expr=sp.factor((cnminus*snplus-snminus*cnplus)-2*sv*cv*du/den)
num=sp.fraction(expr)[0];num=sp.expand(num).subs(cu**2,1-su**2).subs(dv**2,1-k2*sv**2)
check('symbolic_area_addition_numerator',sp.expand(num)==0)
# Universal even Laurent vector times odd neighbor difference: at most simple.
e=sp.symbols('e');A=sp.Matrix(sp.symbols('A0:2'));B=sp.Matrix(sp.symbols('B0:2'));V=sp.Matrix(sp.symbols('V0:2'));W=sp.Matrix(sp.symbols('W0:2'))
la=sp.expand(cross(A/e**2+B,2*e*V+e**3*W)/2)
check('Laurent_order_reduction',all(la.coeff(e,j)==0 for j in [-4,-3,-2]))
check('Laurent_residue',sp.expand(la.coeff(e,-1)-cross(A,V))==0)

for N in range(4,101,4):
 m=N//2
 for tau in range(1,N//2):
  if gcd(N,tau)>1:continue
  shift_classes=[(j*tau)%m for j in range(N)]
  check('real_period_bezout',gcd(tau,m)==1)
  check('pole_residue_multiplicity',Counter(shift_classes)==Counter({j:2 for j in range(m)}))
  check('quarter_shift_period',(N//4*tau)%m==N//4)
  for target in range(m):
   singular=[i for i,j in enumerate(shift_classes) if j==target]
   check('two_simultaneous_nonadjacent_vertices',len(singular)==2 and (singular[1]-singular[0])%N==m)
   incident=[{(j-1)%N,j} for j in singular]
   check('incident_edge_groups_disjoint',incident[0].isdisjoint(incident[1]))

# Direct finite geometric witness, many external M; no caustic projection formula.
pD=[(F(4),F(0)),(F(0),F(3)),(F(-4),F(0)),(F(0),F(-3))]
pR=[(F(16,5),F(9,5)),(-F(16,5),F(9,5)),(-F(16,5),-F(9,5)),(F(16,5),-F(9,5))]
for x in range(-7,8):
 for y in range(-7,8):
  M=(F(x,3),F(y,2));aa=area(pD)*area(pedal(pD,M));bb=area(pR)*area(pedal(pR,M))
  check('exact_arbitrary_point_four_period',aa==bb==F(165888,625))
  check('exact_radial_M_reflection',area(pedal(pD,M))==area(pedal(pD,(M[0],-M[1]))))

# Independent high-precision tests, including complex points arbitrarily near
# the simultaneous pole phases. They are diagnostics, not interval proofs.
import mpmath as mp
mp.mp.dps=90;errmax=mp.mpf(0);families=0;stars=0

def near(g,a,b):
 global errmax
 err=abs(a-b)/max(mp.mpf(1),abs(a),abs(b));errmax=max(errmax,err)
 assert err<mp.mpf('1e-54'),(g,mp.nstr(err,12))
 D[g]+=1

for modulus in [mp.mpf('.31'),mp.mpf('.67'),mp.mpf('.89')]:
 par=modulus**2;kp=mp.sqrt(1-par);K=mp.ellipk(par);Ki=mp.ellipk(1-par);al=mp.mpf('1.7');be=al*kp
 sn=lambda z:mp.ellipfun('sn',z,par);cn=lambda z:mp.ellipfun('cn',z,par);dn=lambda z:mp.ellipfun('dn',z,par)
 def qm(z,M):
  n=(-sn(z)/al,cn(z)/be);s=(dot(n,M)-1)/dot(n,n)
  return tuple(M[j]-s*n[j] for j in range(2))
 for N in [4,8,12,16]:
  for tau in range(1,N//2):
   if gcd(N,tau)>1:continue
   families+=1;stars+=tau>1
   v=2*tau*K/N;step=2*v;ae=al*dn(v)/cn(v);bo=be/cn(v);h=4*K/N
   S=lambda z:sum(dn(z+j*step) for j in range(N))
   for M in [(mp.mpf('0'),mp.mpf('0')),(mp.mpf('1.3'),mp.mpf('-2.1')),(mp.mpf('7.7'),mp.mpf('5.2'))]:
    T=lambda z:area([qm(z+j*step,M) for j in range(N)])
    products=[];ratios=[]
    for phase in ['.119','.467','.913']:
     w=mp.mpf(phase)*K;p=[(-ae*sn(w+j*step),bo*cn(w+j*step)) for j in range(N)]
     contact=[(-al*sn(w+v+j*step),be*cn(w+v+j*step)) for j in range(N)]
     a0=area(p);am=area(pedal(p,M));ai=area(contact)
     near('direct_vs_meromorphic_projection_area',am,T(w+v))
     near('universal_area_trace',a0,ae*bo*sn(v)*cn(v)/dn(v)*S(w))
     products.append(a0*am);ratios.append(am/ai)
    for i in [1,2]:near('full_arbitrary_M_product',products[i],products[0]);near('pedal_contact_proportionality',ratios[i],ratios[0])
    coefficient=T(mp.mpf('.239')*K)/S(mp.mpf('.239')*K+K)
    generic=mp.mpf('.183')*K+mp.mpf('.237')*1j*Ki
    for z in [generic,K+1j*Ki+mp.mpf('1e-9')*(1+mp.mpf('.2')*1j)]:
     near('complex_meromorphic_proportionality',T(z)/S(z+K),coefficient)
     near('complex_quotient_real_period',T(z+h),T(z))
     near('complex_imaginary_antiperiod',T(z+2j*Ki),-T(z))
    r=K+1j*Ki;eps=mp.mpf('1e-8')*(1+mp.mpf('.3')*1j)
    for j in range(2):near('projection_even_near_double_pole',qm(r+eps,M)[j],qm(r-eps,M)[j])
    near('no_even_double_pole_in_area',eps**2*(T(r+eps)+T(r-eps)),0)

result={'status':'PASS','exact_assertions':sum(C.values()),'exact_groups':dict(C),'numerical_diagnostics':sum(D.values()),'numerical_groups':dict(D),'precision_digits':90,'maximum_scaled_error':mp.nstr(errmax,14),'primitive_families':families,'star_families':stars,'limits':'Exact algebra/finite controls and non-interval numerical diagnostics corroborate the separately audited proof. No numerical test establishes the universal theorem.'}
print(json.dumps(result,indent=2));Path(__file__).with_name('independent_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
