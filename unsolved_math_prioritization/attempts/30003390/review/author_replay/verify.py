#!/usr/bin/env python3
"""Exact diagnostics for the CIR information partial; no rate simulation."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from hashlib import sha256
import json
import sympy as s
count=0;groups={}
def check(value,group):
 global count
 assert bool(value),group
 count+=1;groups[group]=groups.get(group,0)+1
a,b,sigma,T,z=s.symbols('a b sigma T z',positive=True);c=sigma**2*T/4
check(s.simplify(a*T/c-4*a/sigma**2)==0,'normalization')
check(s.simplify(b*T*c/c-b*T)==0,'normalization')
check(s.simplify(sigma*s.sqrt(T)*s.sqrt(c*z)/c-2*s.sqrt(z))==0,'normalization')
for A,S,TT,X in product(range(1,4),repeat=4):
 C=Q(S*S*TT,4);Z=Q(X)/C
 check(C*Z==X,'rational normalization');check(Q(4*A,S*S)==Q(A*TT)/C,'rational normalization')
u=s.symbols('u',positive=True);mu=a-b*u;g=sigma*s.sqrt(u)
bracket=s.diff(mu,u)*g-mu*s.diff(g,u)-g*g*s.diff(g,u,2)/2
check(s.simplify(bracket+sigma*b*s.sqrt(u)/2-sigma*(sigma**2-4*a)/(8*s.sqrt(u)))==0,'local bracket identity')
check(s.simplify(bracket.subs({a:sigma**2/4,b:0}))==0,'local bracket degeneracy')
for weights in product(range(1,4),repeat=3):
 total=sum(weights);probs=[Q(w,total) for w in weights];xs=[Q(0),Q(1),Q(3)]
 med=next(x for k,x in enumerate(xs) if sum(probs[:k+1])>=Q(1,2))
 risk=sum(p*abs(x-med) for p,x in zip(probs,xs));mean=sum(p*x for p,x in zip(probs,xs))
 meanrisk=sum(p*abs(x-mean) for p,x in zip(probs,xs))
 pair=sum(p*q*abs(x-y) for p,x in zip(probs,xs) for q,y in zip(probs,xs))
 check(pair/2<=risk<=meanrisk<=pair,'conditional two-copy inequalities')
 for q in [Q(k,2) for k in range(-2,9)]:check(risk<=sum(p*abs(x-q) for p,x in zip(probs,xs)),'conditional median optimality')
 check(med<=2*mean,'median integrability control')
u,v,l,h=s.symbols('u v l h',real=True)
check(s.expand((v+u+2*l)**2-(v-u)**2-4*(u+l)*(v+l))==0,'bridge reflection identity')
# Choose each interval length 2/log(2), making every evaluated factor rational.
def cdf(ys,l):
 l0=max(0,-min(ys))
 if l<l0:return Q(0)
 val=Q(1)
 for u,v in zip(ys,ys[1:]):
  exponent=(u+l)*(v+l);assert exponent>=0
  val*=1-Q(1,2**exponent)
 return val
for n in range(1,4):
 for r in range(3):
  for ends in product(range(-2,3),repeat=n):
   ys=(r,)+tuple(r+w for w in ends);l0=max(0,-min(ys));f0=cdf(ys,l0)
   check(ys[-1]+l0>=0,'monotone square support');check(0<=f0<1,'bridge CDF range')
   if l0>0 or min(ys)==0:check(f0==0,'barrier endpoint and atom')
   f1=cdf(ys,l0+1);f2=cdf(ys,l0+2)
   check(f0<f1<f2<1,'bridge CDF strict increase');check(cdf(ys,l0+4)>Q(1,2),'median finite bracket')
check(cdf((1,1),0)==Q(1,2),'zero atom equality threshold')
check(cdf((2,2),0)==Q(15,16),'zero atom strict threshold')
check(cdf((0,0),0)==0,'zero initial value no atom')
w=s.symbols('w',real=True);k=s.symbols('k',positive=True);q=(-w+s.sqrt(w*w+k))/2
check(s.simplify(4*q*(w+q)-k)==0,'single bridge quadratic quantile')
check(s.simplify((w+q)-(w+s.sqrt(w*w+k))/2)==0,'single bridge estimator')
c0,q0,F=s.symbols('c q F',real=True)
check(s.expand(2*(c0+q0)*F-2*(c0+q0)*(1-F)-2*(c0+q0)*(2*F-1))==0,'risk derivative')
lam=s.symbols('lambda',positive=True);x=s.symbols('x',nonnegative=True);m=s.log(2)/lam
risk=s.integrate(1-s.exp(-lam*x),(x,0,m))+s.integrate(s.exp(-lam*x),(x,m,s.oo))
check(s.simplify(risk-m)==0,'conditional exponential risk')
b,h=s.symbols('b h',positive=True)
var=(s.exp(b*h)-1)/b-4*(s.exp(b*h/2)-1)**2/(b*b*h)
check(s.simplify(s.limit(var/h**3,h,0)-b*b/48)==0,'weighted noise variance leading term')
check(s.simplify(s.limit(var,b,0))==0,'zero reversion variance')
t=s.symbols('t',real=True)
for start,length,slope in product(range(3),range(1,4),range(1,4)):
 f=1+slope*t;first=s.integrate(f,(t,start,start+length));second=s.integrate(f*f,(t,start,start+length));residual=s.simplify(second-first**2/length)
 check(residual==Q(slope*slope*length**3,12),'Gaussian projection identity');check(residual>0,'strict observation information loss')
b,t=s.symbols('b t',positive=True);clock=(s.exp(b*t)-1)/b
check(s.simplify(s.diff(clock,t)-s.exp(b*t))==0,'time change clock')
check(s.simplify(s.exp(b*t/2)**2-s.diff(clock,t))==0,'time change Brownian variance')
receipt={'verdict':'PASS','assertions':count,'groups':groups,'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':s.__version__,'scope':'Exact finite diagnostics for normalization, median decisions, bridge laws and information loss; no asymptotic-rate certification.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
