#!/usr/bin/env python3
"""Offline exact controls. No third-party packages, no network, no global-optimum claim."""
from fractions import Fraction as F
from itertools import permutations, combinations
from pathlib import Path
import hashlib,json,sys

COUNT=0
def check(c,msg):
 global COUNT
 COUNT+=1
 if not c: raise AssertionError(msg)
class P:
 """Finite rational Laurent polynomial in ell=log(2)."""
 def __init__(self,x=0):
  if isinstance(x,P):self.c=dict(x.c)
  elif isinstance(x,dict):self.c={int(k):F(v) for k,v in x.items() if v}
  else:self.c={} if x==0 else {0:F(x)}
 def __add__(self,o):
  o=P(o);d=dict(self.c)
  for k,v in o.c.items():d[k]=d.get(k,F(0))+v
  return P(d)
 __radd__=__add__
 def __neg__(self):return P({k:-v for k,v in self.c.items()})
 def __sub__(self,o):return self+-P(o)
 def __rsub__(self,o):return P(o)+-self
 def __mul__(self,o):
  o=P(o);d={}
  for a,x in self.c.items():
   for b,y in o.c.items():d[a+b]=d.get(a+b,F(0))+x*y
  return P(d)
 __rmul__=__mul__
 def __truediv__(self,o):return self*F(1,o)
 def __eq__(self,o):return self.c==P(o).c
 def bounds(self,lo,hi):
  low=high=F(0)
  for k,c in self.c.items():
   a,b=(lo**k,hi**k) if k>=0 else (hi**k,lo**k)
   if c>=0:low+=c*a;high+=c*b
   else:low+=c*b;high+=c*a
  return low,high

def power(k):return F(2)**k
def theta(k,h):
 a,b=power(k),power(h)
 if k==h:return P(a),P(F(1,2)),P(F(1,2))
 z=k-h
 return P({-1:(a-b)/z}),P({-1:F(1,z),-2:(-1+b/a)/(z*z)}),P({-1:-F(1,z),-2:(-1+a/b)/(z*z)})

def graph(n):
 states=list(permutations(range(n)));idx={s:i for i,s in enumerate(states)};adj=[[] for _ in states]
 for i,s in enumerate(states):
  for a,b in combinations(range(n),2):
   t=tuple(b if x==a else a if x==b else x for x in s)
   adj[i].append(idx[t])
 return states,adj

def forms(n,exponents,psi,rate_factor=F(1),omit_density=False,half=F(1,2)):
 states,adj=graph(n);N=len(states);q=F(2,n*(n-1))*rate_factor;mu=F(1,N)
 r=[power(k) for k in exponents];psi=list(map(F,psi))
 lr=[q*sum((r[j]-r[i] for j in adj[i]),F(0)) for i in range(N)]
 lp=[q*sum((psi[j]-psi[i] for j in adj[i]),F(0)) for i in range(N)]
 A=B=On=P()
 for i in range(N):
  for j in adj[i]:
   if i>=j:continue
   th,ta,tb=theta(exponents[i],exponents[j]);g=psi[j]-psi[i]
   A+=mu*q*g*g*th
   term=P() if omit_density else half*(ta*lr[i]+tb*lr[j])*g*g
   B+=mu*q*(term-th*g*(lp[j]-lp[i]))
   On+=mu*q*q*g*g*(2*th+F(1,2)*(r[j]-r[i])*(ta-tb))
 return A,B,On

def log2_bounds(terms=50):
 # log2=2 sum_{j>=0}(1/3)^(2j+1)/(2j+1); geometric upper bound on tail.
 x=F(1,3);lo=2*sum((x**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
 tail=2*x**(2*terms+1)/(F(2*terms+1)*(1-x*x))
 return lo,lo+tail

def run():
 lo,hi=log2_bounds()
 check(lo>F(2,3),'log2 lower bound')
 check(hi-lo<F(1,10**45),'log2 interval precision')
 enumeration=0
 for n in range(2,7):
  states,adj=graph(n);N=len(states);enumeration+=N
  d=n*(n-1)//2;q=F(1,d)
  check(all(len(set(v))==d for v in adj),'degree')
  check(all(i in adj[j] for i in range(N) for j in adj[i]),'undirected graph')
  f=[int(s[0]==0) for s in states]
  A,B,_=forms(n,[0]*N,f)
  check(B==n*q*A,'spectral quotient')
  for k in [1,2,4]:
   ex=[k if s[0]==0 else 0 for s in states];A,B,_=forms(n,ex,f);t=power(k)
   R=P(n*q/2)+P({-1:q*(t+n-2-F(n-1)/t)/(2*k)})
   check(B==A*R,'one-card formula')
   A2,B2,_=forms(n,ex,f,F(3,7))
   check(A2==F(3,7)*A,'A rate scaling');check(B2==F(9,49)*B,'B rate scaling')
  parity=[sum(s[i]>s[j] for i in range(n) for j in range(i+1,n))%2 for s in states]
  for k in [0,1,3]:
   ex=[k if p==0 else 0 for p in parity];A,B,_=forms(n,ex,parity)
   th,ta,tb=theta(k,0);a=power(k);b=F(1)
   check((B-2*A)*2*th==A*(b-a)*(ta-tb),'parity formula')
   if k==0:check(B==2*A,'parity uniform exact')
 # Published S3 local obstruction, transported to explicit bipartition.
 states,adj=graph(3);parity=[sum(s[i]>s[j] for i in range(3) for j in range(i+1,3))%2 for s in states]
 ev=[i for i,p in enumerate(parity) if not p];od=[i for i,p in enumerate(parity) if p]
 for k in [1,2,4,8,16]:
  ex=[-k]*6;psi=[1]*6
  for j,i in enumerate(od):ex[i]=0 if j==0 else -2*k;psi[i]=0 if j==0 else 2
  A,B,On=forms(3,ex,psi);e=power(-k);M=P({1:k});Z=P(1-e*e)+2*e*M
  check(A==P({-1:(1-e)*(1+2*e)/(6*k)}),'S3 A formula')
  check(On*6*e*M==A*Z,'S3 diagonal formula')
  check((B-On)*3*M*(1+2*e)==A*Z,'S3 off-diagonal formula')
  check(B*6*e*M*(1+2*e)==A*(1+4*e)*Z,'S3 full formula')
 # Exact witness.
 ex=[0,0,4,4,0,0];psi=[5,-5,8,-8,5,-5];A,B,_=forms(3,ex,psi)
 EA=P({0:F(4496,18),-1:F(135,18)})
 EB=P({0:F(251392,1152),-1:F(480,1152),-2:F(6075,1152)})
 check(A==EA,'witness A exact');check(B==EB,'witness B exact')
 gap=F(9,10)*A-B
 check(gap.bounds(lo,hi)[0]>0,'strict kappa3 upper witness')
 check((B-F(2,3)*A).bounds(lo,hi)[0]>0,'witness is not matching lower bound')
 rational_gap=F(37888)*F(2,3)**2+F(36480)*F(2,3)-30375
 check(rational_gap==F(97057,9)>0,'elementary rational sign proof')
 al,ah=A.bounds(lo,hi);bl,bh=B.bounds(lo,hi)
 check(al>0,'positive action')
 # Mathematical negative controls: deliberately invalid variants must fail.
 _,bad,_=forms(3,ex,psi,omit_density=True);check(bad!=EB,'omitted density-derivative rejected')
 _,bad,_=forms(3,ex,psi,half=1);check(bad!=EB,'missing one-half rejected')
 aa,bb,_=forms(3,ex,psi,F(1,2));check(bb*EA!=aa*EB,'half-rate same-curvature rejected')
 check(B!=A,'uniform spectral sharpness rejected')
 check(B!=F(2,3)*A,'off-diagonal sharpness does not give full sharpness')
 result={'status':'passed','arithmetic_assertions':COUNT,'permutation_states_enumerated':enumeration,'witness_ratio_interval':[str(bl/ah),str(bh/al)],'witness_strict_bound':'kappa_3 < 9/10','global_optimum_certified':False,'all_n_order_solved':False,'dependencies':'Python standard library only'}
 manifest_path=Path(__file__).with_name('MANIFEST.json')
 if manifest_path.exists():
  manifest=json.loads(manifest_path.read_text());base=manifest_path.parent
  for row in manifest['files']:
   b=(base/row['path']).read_bytes()
   check(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'manifest '+row['path'])
  # Mutation tests are in-memory only, leave frozen files unchanged.
  row=next(x for x in manifest['files'] if x['path']=='PROOF.md');b=(base/row['path']).read_bytes();mut=bytes([b[0]^1])+b[1:]
  check(hashlib.sha256(mut).hexdigest()!=row['sha256'],'one-bit corruption rejected')
  check(len(b[:-1])!=row['bytes'],'truncation rejected')
  result['manifest_checks']='passed including one-bit and truncation negative controls'
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':run()
