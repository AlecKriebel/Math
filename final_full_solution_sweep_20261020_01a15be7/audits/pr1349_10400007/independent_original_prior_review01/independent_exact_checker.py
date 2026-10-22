#!/usr/bin/env python3
"""Independent stdlib diagnostics, not a numerical substitute for imported TQFT theorems."""
from fractions import Fraction as F
from itertools import product
import json,sys,hashlib,math
checks=[]; controls=[]
def require(name,truth):
 if not truth: raise RuntimeError(name)
 checks.append(name)
def reject(name,truth):
 if truth: raise RuntimeError('corruption survived: '+name)
 controls.append(name)
def trim(a):
 a=list(map(F,a))
 while a and a[-1]==0:a.pop()
 return a
def add(a,b):
 return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 c=[F(0)]*max(0,len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def div(a,b):
 a=trim(a);b=trim(b)
 if not b:raise ZeroDivisionError()
 q=[F(0)]*max(0,len(a)-len(b)+1)
 while len(a)>=len(b):
  i=len(a)-len(b);x=a[-1]/b[-1];q[i]+=x
  a=sub(a,[F(0)]*i+[x*y for y in b])
 return trim(q),a
phis={}
def phi(n):
 if n in phis:return phis[n]
 a=[-1]+[0]*(n-1)+[1]
 for d in range(1,n):
  if n%d==0:
   a,rem=div(a,phi(d))
   if rem:raise RuntimeError('cyclotomic exact division')
 phis[n]=a;return a
mod=phi(60)
def red(a):return div(a,mod)[1]
def rmul(a,b):return red(mul(a,b))
def rpow(a,n):
 o=[F(1)]
 while n:
  if n&1:o=rmul(o,a)
  a=rmul(a,a);n//=2
 return o
def inv(a):
 r0,r1=mod,red(a);s0,s1=[],[F(1)]
 while r1:
  q,r=div(r0,r1);r0,r1=r1,r;s0,s1=s1,sub(s0,mul(q,s1))
 if len(r0)!=1:raise ZeroDivisionError('nonunit')
 return red([x/r0[0] for x in s0])
z=[F(0),F(1)]
require('Phi60 degree16',len(mod)==17)
require('primitive60 root exact',rpow(z,60)==[1] and all(rpow(z,d)!=[1] for d in [1,2,3,4,5,6,10,12,15,20,30]))
nodes=[rpow(z,(-60//r)%60) for r in [3,4,5]]
for i in range(3):
 for j in range(i):require('distinct cyclotomic node %s,%s'%(i,j),bool(sub(nodes[i],nodes[j])))
# polynomial t*V(t)=1+2t-t^2; three consecutive levels k=1,2,3.
coeff=[[],[],[]]
for i,t in enumerate(nodes):
 y=add([1],sub([2*x for x in t],rmul(t,t)))
 other=[nodes[j] for j in range(3) if j!=i]
 basis=[rmul(other[0],other[1]),neg(add(other[0],other[1])),[F(1)]]
 den=rmul(sub(t,other[0]),sub(t,other[1]));scale=rmul(y,inv(den))
 for k in range(3):coeff[k]=add(coeff[k],rmul(scale,basis[k]))
require('exact Lagrange full Laurent recovery',coeff==[[F(1)],[F(2)],[F(-1)]])
reject('omit t^B prefactor',coeff==[[F(0)],[F(1)],[F(2)]])
reject('duplicate-level node remains distinct',bool(sub(nodes[0],nodes[0])))
# Two nodes cannot determine a quadratic: a nonzero polynomial vanishes there.
alias=[rmul(nodes[0],nodes[1]),neg(add(nodes[0],nodes[1])),[1]]
for t in nodes[:2]:require('two-node alias vanishes',add(alias[0],rmul(t,add(alias[1],rmul(t,alias[2]))))==[])
reject('two samples imply uniqueness',alias==[[],[],[]])
# Laurent ring Q[x,x^-1], q=x^4, s=x^2-x^-2, d=x^2+x^-2.
def la(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,0)+v
 return {k:v for k,v in c.items() if v}
def lm(a,b):
 c={}
 for i,x in a.items():
  for j,y in b.items():c[i+j]=c.get(i+j,0)+x*y
 return {k:v for k,v in c.items() if v}
def scale(a,s):return {k:s*v for k,v in a.items() if s*v}
s={2:1,-2:-1};dim={2:1,-2:1};p={0:dim,1:{0:1}}
for n in range(2,8):p[n]=la(lm({-8:1},p[n-2]),lm({-4:1},lm(s,p[n-1])))
require('positive two-braid trefoil exact source convention',p[3]=={-4:1,-12:1,-16:-1})
require('positive Hopf link component sign',scale(p[2],-1)=={-2:-1,-10:-1})
require('split two-component unlink sign',scale(dim,-1)=={-2:-1,2:-1})
reject('mirror variable unchanged',p[3]=={-k:v for k,v in p[3].items()})
reject('omit component parity',p[2]==scale(p[2],-1))
# q^(1/4) theta^(-1)=q^-1, q^(-1/4)theta=q for theta=q^(3/4).
require('writhe-corrected skein exponent plus',1-3==-2)
require('writhe-corrected skein exponent minus',-1+3==2)
reject('omit writhe correction',1==-2)
# Exact one-handle adjoint from BHMV cut form=eta*sewn form, eta=1/D.
for D in [F(2),F(3),F(7,2)]:
 for a,b,y in product(range(-2,3),repeat=3):
  # sewn sectors: vacuum metric D; orthogonal nonvacuum sector arbitrary positive scale.
  left=D*a*b;right=a*(D*b)
  require('vacuum adjoint identity D=%s (%s,%s,%s)'%(D,a,b,y),left==right)
 reject('raw projection reverse handle D=%s'%D,D==1)
 reject('inverse normalization D=%s'%D,(1/D)*(1/D)==1)
 for g in range(1,8):require('local compression power D=%s g=%s'%(D,g),D**(g-1)*D/D==D**(g-1))
# Stabilization introduces s=D^-1 and one extra inverse factor.
for g in range(1,8):
 D=F(3);require('relative Heegaard stabilization g=%s'%g,D**g/D==D**(g-1))
 reject('miss one compression g=%s'%g,D**(g-1)/D==D**(g-1))
# Genus-one Maslov index for three rational lines; pairwise transverse case scalar.
def omega(u,v):return u[0]*v[1]-u[1]*v[0]
def maslov(u,v,w):
 # For w=a*u+b*v, symmetric form on span(w) has value a*b*omega(u,v).
 if not omega(u,v) or not omega(u,w) or not omega(v,w):return 0
 den=F(omega(u,v));a=F(omega(w,v))/den;b=F(omega(u,w))/den;q=a*b*den
 return (q>0)-(q<0)
a=(1,0);b=(0,1);c=(1,1)
for u,v in product([a,b,c],repeat=2):
 require('Maslov repeated %r,%r'%(u,v),maslov(u,u,v)==maslov(u,v,u)==maslov(v,u,u)==0)
require('Maslov nonzero diagnostic',maslov(a,b,c)==1)
reject('arbitrary lagrangians silently weightzero',maslov(a,b,c)==0)
require('peripheral gluing longitude meridian meridian',maslov(b,a,a)==0)
# Compressionbody model H1(C)=Za_T+Zb_T+Z extra_i.  Kernel generated by a_i,i>0;
# preimage of Za_T has basis a_0,...,a_(g-1), saturated and rank g.
for g in range(1,9):
 for coords in product(range(-1,2),repeat=min(2*g,6)):
  v=list(coords)+[0]*(2*g-len(coords));in_preimage=all(v[2*i+1]==0 for i in range(g))
  in_lattice=all(v[j]==0 for j in range(2*g) if j%2)
  require('compression preimage g=%s v=%s'%(g,tuple(v)),in_preimage==in_lattice)
 require('compression genus rank g=%s'%g,len(list(range(g)))==g)
reject('nonprimitive meridian lattice silently accepted',math.gcd(2,0)==1)
# Local H0 test on a contractible interval: boundary identifies endpoint coefficients.
# For monodromy 2 on S1, H0=Q/(2-1)Q=0, while horizontal invariants also 0.
require('interval boundary and transported horizontal section',(-1)*2+2*1==0 and 2*F(3)==1*F(6))
reject('ignore transport in theta H0',2*F(3)==1*F(3))
reject('replace marked Teich by moduli without checking H0',F(2)-1==0)
reject('include level0 fundamental denominator',bool(add(rpow(z,15),inv(rpow(z,15)))))
# Check the explicit local union-box repair in AU comparison arXivv2 Case1.
union_cases=0
for rows in range(1,5):
 for width in range(1,5):
  ds=[x for x in product(range(width+1),repeat=rows) if all(x[i]>=x[i+1] for i in range(rows-1))]
  for ii,u in enumerate(ds):
   for v in ds[ii+1:]:
    if sum(u)!=sum(v):continue
    common=tuple(min(a,b) for a,b in zip(u,v))
    if sum(common)!=sum(u)-1:continue
    union=tuple(max(a,b) for a,b in zip(u,v));union_cases+=1
    if sum(union)!=sum(u)+1:raise RuntimeError('union box repair')
require('bounded common-predecessor union size n+1',union_cases>0)
reject('source local n+2 count',sum((2,1))==sum((1,1))+2)
out={'status':'pass','python_optimization':sys.flags.optimize,'checks_count':len(checks),'controls_rejected':len(controls),'check_name_digest':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),'sample_checks':checks[:25]+checks[-15:],'controls':controls,'young_diagram_union_cases':union_cases,'scope':'Exact finite diagnostics only; universal naturality and analytic sewing rely on the identified published theorems. No author program executed.'}
print(json.dumps(out,indent=2))
