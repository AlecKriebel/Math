#!/usr/bin/env python3
"""Audit via implicit algebraic recurrences, independent of Catalan composition."""
from fractions import Fraction as Q
from dataclasses import dataclass
from pathlib import Path
from math import isqrt
import json,runpy,contextlib,io,hashlib
import mpmath as mp
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'submission'
@dataclass(frozen=True)
class G:
 r:Q=Q(0)
 i:Q=Q(0)
 def __add__(self,b):
  if not isinstance(b,G):b=G(Q(b))
  return G(self.r+b.r,self.i+b.i)
 __radd__=__add__
 def __neg__(self):return G(-self.r,-self.i)
 def __sub__(self,b):return self+-b
 def __mul__(self,b):
  if not isinstance(b,G):b=G(Q(b))
  return G(self.r*b.r-self.i*b.i,self.r*b.i+self.i*b.r)
 __rmul__=__mul__
 def __truediv__(self,b):return G(self.r/b,self.i/b)
 def n2(self):return self.r*self.r+self.i*self.i

def slit(q,u,N):
 # s*(1-u*z)^2=q*z*(1-u*s)^2; solve coefficient by coefficient.
 s=[u*0]*(N+1)
 s[1]=u*0+q
 for k in range(2,N+1):
  s[k]=2*u*(1-q)*s[k-1]-u*u*s[k-2]+q*u*u*sum((s[j]*s[k-1-j] for j in range(1,k-1)),u*0)
 return s

def terminal(s,q):
 # F*(1-s)^2=s/q; solve directly, no inverse-series composition.
 N=len(s)-1;zero=s[0]*0
 d=[zero]*(N+1);d[0]=zero+1
 for k in range(1,N+1):d[k]=-2*s[k]+sum((s[j]*s[k-j] for j in range(1,k)),zero)
 a=[zero]*(N+1)
 for k in range(1,N+1):a[k]=s[k]/q-sum((d[j]*a[k-j] for j in range(1,k+1)),zero)
 return a

def compose(a,b):
 # Explicit powers, distinct from the packet's Horner implementation.
 N=len(a)-1;zero=a[0]*0;r=[zero]*(N+1);p=[zero]*(N+1);p[0]=zero+1
 for k in range(N+1):
  for j in range(N+1):r[j]+=a[k]*p[j]
  p=[sum((p[j]*b[m-j] for j in range(m+1)),zero) for m in range(N+1)]
 return r

def exact_bounds(z):
 x=z.n2(); D=10**50
 r=isqrt(x.numerator*D*D//x.denominator)
 lo=Q(r,D);hi=lo if lo*lo==x else Q(r+1,D)
 assert lo*lo<=x<=hi*hi
 return lo,hi

with contextlib.redirect_stdout(io.StringIO()):
 v=runpy.run_path(str(ROOT/'reproduction'/'verify.py'))
records=json.loads((SOURCE/'CHECKS.json').read_text())['results']
checks=[];cache={};coef_matches=0
for row in records:
 q=Q(row['q']);u=G(*map(Q,row['u']));key=(q,u)
 if key not in cache:
  a=terminal(slit(q,u,9),q);cache[key]=a
  original=v['coeff'](q,(u.r,u.i))
  assert [(x.r,x.i) for x in a]==original
  coef_matches+=10
 a=cache[key];n=row['n'];ab=[exact_bounds(a[j]) for j in range(1,2*n,2)]
 lo=sum(x[0] for x in ab)-a[n].n2();hi=sum(x[1] for x in ab)-a[n].n2()
 assert lo>=0
 # Compare genuinely distinct precision bounds against every archived interval.
 assert Q(row['lower'])<=lo<=hi<=Q(row['upper'])
 checks.append({'q':str(q),'u':[str(u.r),str(u.i)],'n':n,'lower':str(lo),'upper':str(hi)})

mp.mp.dps=120;mins=[]
for file in ['loewner_search.json','two_switch_search.json']:
 for row in json.loads((SOURCE/'exploratory'/file).read_text()):
  x=list(map(lambda a:mp.mpf(str(a)),row['x']));n=row['n'];N=2*n-1
  if len(x)==2:q=x[0];s=slit(q,mp.exp(mp.j*x[1]),N)
  else:
   q=x[0]*x[1]
   s=compose(slit(x[1],mp.exp(mp.j*x[3]),N),slit(x[0],mp.exp(mp.j*x[2]),N))
  a=terminal(s,q);delta=sum(abs(a[j]) for j in range(1,2*n,2))-abs(a[n])**2
  assert delta>0
  mins.append({'source':file,'n':n,'dps':120,'delta':mp.nstr(delta,100),'sign':int(mp.sign(delta)),'certified':False})
out={'method':'Implicit algebraic recurrence for slit and terminal functions; no Catalan coefficients. Exact Gaussian rationals for grid; 120-digit independent arithmetic for numerical diagnostics.','grid_instances':len(cache),'coefficients_compared':coef_matches,'certified_grid_inequalities':len(checks),'zero_lower_bounds':sum(Q(c['lower'])==0 for c in checks),'all_120_pass':True,'numeric_minima':mins,'exact_records':checks}
(ROOT/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='exact_records'},indent=2))
