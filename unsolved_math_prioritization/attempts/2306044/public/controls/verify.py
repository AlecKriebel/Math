#!/usr/bin/env python3
"""Finite controls for 2306044. No claim to formalize the analytic proof."""
from fractions import Fraction as F
from math import factorial, exp, cos, sin, pi
import json
import platform

checks = []
def require(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

# Small exact polynomial ring Q[t,u,v], with d/dt(u)=-u and d/dt(v)=0.
class P:
    def __init__(self, value=0):
        self.c = value if isinstance(value, dict) else ({(0,0,0): F(value)} if value else {})
        self.c = {m:F(a) for m,a in self.c.items() if a}
    def __add__(self, other):
        other = other if isinstance(other,P) else P(other)
        out = dict(self.c)
        for m,a in other.c.items(): out[m]=out.get(m,F(0))+a
        return P(out)
    __radd__=__add__
    def __neg__(self): return P({m:-a for m,a in self.c.items()})
    def __sub__(self,other): return self+-other if isinstance(other,P) else self+P(-other)
    def __rsub__(self,other): return -self+other
    def __mul__(self,other):
        other=other if isinstance(other,P) else P(other)
        out={}
        for m,a in self.c.items():
            for n,b in other.c.items():
                k=tuple(x+y for x,y in zip(m,n));out[k]=out.get(k,F(0))+a*b
        return P(out)
    __rmul__=__mul__
    def __pow__(self,n):
        out=P(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,other):return self.c==(other if isinstance(other,P) else P(other)).c
    def dt(self):
        out=P()
        for (i,j,k),a in self.c.items():
            if i:out+=P({(i-1,j,k):i*a})
            if j:out+=P({(i,j,k):-j*a})
        return out
    def at(self,t,u,v):return sum(a*t**i*u**j*v**k for (i,j,k),a in self.c.items())

t=P({(1,0,0):1});u=P({(0,1,0):1});v=P({(0,0,1):1})
A=2*t*v
B=(4*t*t-4*t)*v*v+1-u*u
require('A differential identity', A.dt()==2*v)
require('B differential identity', B.dt()==4*v*A-4*v*v+2*u*u)
require('A initial condition', A.at(F(0),F(1),F(2,3))==0)
require('B initial condition', B.at(F(0),F(1),F(2,3))==0)
require('wrong numerator is detected', B.dt()!=4*v*A-4*v*v)

# Exact truncated reciprocal / numerator algebra for p_t: use t as formal q.
den=[P(1),2*t,P(1)]
inv=[P(1),-2*t,4*t*t-1]
prod=[sum((den[j]*inv[n-j] for j in range(n+1)),P()) for n in range(3)]
require('denominator reciprocal through order two',prod==[P(1),P(),P()])
p=[inv[0],inv[1],inv[2]-inv[0]]
require('vector field expansion',p==[P(1),-2*t,4*t*t-2])

# T=1/2: terminal u=v. B=1-2v^2, A=v, so Koebe composition yields 3v,1+5v^2.
require('T half coefficients',
        all(A.at(F(1,2),x,x)+2*x==3*x and
            B.at(F(1,2),x,x)+4*x*A.at(F(1,2),x,x)+3*x*x==1+5*x*x
            for x in [F(1,3),F(2,3),F(7,8)]))
# Formal identity, rather than only the preceding rational spot-checks.
terminalA=v
terminalB=1-2*v*v
require('terminal Koebe algebra',terminalA+2*v==3*v and terminalB+4*v*terminalA+3*v*v==1+5*v*v)

# e is represented by formal t; clear all denominators before checking the margin.
# 24 e^2 times [ (1+5/e)^2/3 - (9/(2e))^2/2 -(1+2/e^2) ].
margin_numerator=8*(t+5)**2-243-24*t*t-48
factor=-16*(t-F(7,4))*(t-F(13,4))
require('cleared denominator and factorization',margin_numerator==factor)
require('ordinary Hadamard mutation differs',
        24*(t+5)**2-972-24*t*t-48 != margin_numerator)
require('sign mutation is detected', margin_numerator!=-factor)

# Rigorous rational enclosure for e, with the geometric tail starting at n=N+1.
N=18
elo=sum((F(1,factorial(n)) for n in range(N+1)),F(0))
ehi=elo+F(N+2,(N+1)*factorial(N+1))
require('elementary sign enclosure',F(7,4)<2<elo<ehi<3<F(13,4))
# Delta = (2/3)*(e-7/4)*(13/4-e)/e^2, each factor positive.
dlo=F(2,3)*(elo-F(7,4))*(F(13,4)-ehi)/(ehi*ehi)
dhi=F(2,3)*(ehi-F(7,4))*(F(13,4)-elo)/(elo*elo)
require('certified positive obstruction margin',0<dlo<dhi)
require('quantified margin exceeds 0.046',dlo>F(46,1000))

# Negative control T=0: the flow is identity and f=k; k tensor k=k.
require('Koebe baseline has no false obstruction',F(3)-F(1,2)*F(2)**2-(F(1)+2/(elo*elo))<0)
require('Koebe weighted convolution coefficient control',all(F(n*n,n)==n for n in range(1,31)))

# Supplementary floating-point RK4 checks. No validated integration or global proof.
def rhs(time,w):
    q=exp(time-.5)
    return -w*(1-w*w)/(1+2*q*w+w*w)
def flow(z,n):
    w=z;dt=.5/n;mx=abs(w)
    for i in range(n):
        s=i*dt
        k1=rhs(s,w);k2=rhs(s+dt/2,w+dt*k1/2)
        k3=rhs(s+dt/2,w+dt*k2/2);k4=rhs(s+dt,w+dt*k3)
        w+=dt*(k1+2*k2+2*k3+k4)/6;mx=max(mx,abs(w))
    return w,mx
zs=[r*complex(cos(2*pi*j/16),sin(2*pi*j/16)) for r in [.1,.5,.9] for j in range(16)]
max_mesh_delta=0.0
for z in zs:
    w,mx=flow(z,512);w2,_=flow(z,1024);wc,_=flow(z.conjugate(),512)
    require('flow radius sample '+str(len(checks)),mx<=abs(z)+1e-12)
    require('conjugation sample '+str(len(checks)),abs(wc-w.conjugate())<1e-13)
    max_mesh_delta=max(max_mesh_delta,abs(w-w2))
require('sample mesh agreement',max_mesh_delta<1e-8)

out={
 'problem_id':2306044,
 'passed':True,
 'exact_and_sample_assertions':len(checks),
 'checks':checks,
 'rigorous_e_interval':{'lower':str(elo),'upper':str(ehi)},
 'rigorous_margin_interval':{'lower':str(dlo),'upper':str(dhi)},
 'margin_decimal_illustration':[float(dlo),float(dhi)],
 'supplementary_flow':{'grid_points':len(zs),'time_interval':[0,.5],'mesh_steps':[512,1024],'max_mesh_difference':max_mesh_delta},
 'environment':{'python':platform.python_version(),'dependencies':'standard library only'},
 'limits':[
  'Exact algebra and rational intervals do not prove analytic flow existence or univalence.',
  'The analytic proof is in proof.md and uses the sourced Fekete–Szegő theorem.',
  'The RK4 controls are unvalidated floating-point samples, not an exhaustive search or proof.',
  'No collision points or local-univalence failure are claimed.',
  'The primary Bshouty article was not read; prior-result matching uses Hayman–Lingham Update 6.44.'
 ]}
print(json.dumps(out,indent=2))
