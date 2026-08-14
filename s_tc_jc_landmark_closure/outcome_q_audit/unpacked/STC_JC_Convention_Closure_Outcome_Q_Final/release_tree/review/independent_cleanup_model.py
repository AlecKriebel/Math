#!/usr/bin/env python3
"""Clean-room sparse-polynomial replay of the root zipper JC tensor."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'certificates'/'independent_cleanup_model.json'
VARS=('alpha','beta','gamma','u','v','lambda')
N=len(VARS)

def mono(i):
 e=[0]*N;e[i]=1;return {tuple(e):Fraction(1)}
def const(c):return {(0,)*N:Fraction(c)}
def add(p,q):
 r=dict(p)
 for m,c in q.items():r[m]=r.get(m,Fraction(0))+c
 return {m:c for m,c in r.items() if c}
def mul(p,q):
 r={}
 for a,c in p.items():
  for b,d in q.items():
   m=tuple(x+y for x,y in zip(a,b));r[m]=r.get(m,Fraction(0))+c*d
 return {m:c for m,c in r.items() if c}
def sub(p,q):return add(p,{m:-c for m,c in q.items()})
def prod(*xs):
 r=const(1)
 for x in xs:r=mul(r,x)
 return r

def text(p):
 out=[]
 for m,c in sorted(p.items()):
  factors=[]
  for name,e in zip(VARS,m):
   if e:factors.append(name if e==1 else f'{name}^{e}')
  out.append((str(c),'*'.join(factors) or '1'))
 return out

def evaluate(p,d):
 s=Fraction(0)
 for m,c in p.items():
  t=c
  for name,e in zip(VARS,m):t*=d[name]**e
  s+=t
 return s

A,B,G,U,W,L=map(mono,range(N));ONE=const(1)
# Independent switching construction: parent 0 retains root->q and uses
# alpha,beta,u,v; parent 1 retains p->q and uses gamma,u,v.
choice0=prod(L,A,B,U,W)
choice1=prod(sub(ONE,L),G,U,W)
tensor=add(choice0,choice1)
expected=prod(U,W,add(prod(L,A,B),prod(sub(ONE,L),G)))
assert tensor==expected
vals={'alpha':Fraction(2,3),'beta':Fraction(3,4),'gamma':Fraction(5,8),
      'u':Fraction(7,9),'v':Fraction(8,11),'lambda':Fraction(2,5)}
assert evaluate(tensor,vals)==Fraction(161,495)
# Section checked on an exact rational grid; alpha=beta require sqrt(m), so
# choose square x values through t: x=t^2 and evaluate with exact t-derived
# section values.
section_checks=[]
for t in (Fraction(1,5),Fraction(1,3),Fraction(2,3),Fraction(4,5)):
 x=t*t;c=(1+x)/2;m=4*x/(1+x)**2;s=m.numerator;sden=m.denominator
 aa=(1+m)/2;bb=2*m/(1+m)
 d={'alpha':aa,'beta':bb,'gamma':m,'u':c,'v':c,'lambda':Fraction(1,2)}
 assert all(Fraction(0)<z<Fraction(1) for z in d.values())
 assert evaluate(tensor,d)==x
 section_checks.append({'x':str(x),'m':str(m),'effective':str(evaluate(tensor,d))})

cert={'status':'PROVED','variable_order':VARS,'source_switching_polynomial':text(tensor),
      'polynomial_sha256':sha256(repr(sorted(tensor.items())).encode()).hexdigest(),
      'rational_witness':'161/495','strict_section_grid':section_checks,
      'independence_note':'This implementation uses a sparse exponent dictionary and does not import SymPy, the primary graph evaluator, or the primary certificate.'}
OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
print(json.dumps(cert,indent=2,sort_keys=True));print('PASS independent cleanup model')
