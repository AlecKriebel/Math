#!/usr/bin/env python3
"""Exact supplementary controls, including the separate formulation counterexample."""
import sympy as s
import json
checks=0
def check(v):
 global checks
 assert v
 checks+=1
def zero(x):check(s.simplify(x)==0)
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def area(P):return s.simplify(sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2)
def foot(F,X,Y):
 d=sub(Y,X);t=s.cancel(dot(sub(F,X),d)/dot(d,d));Q=tuple(s.simplify(x+t*z) for x,z in zip(X,d))
 zero(det(sub(Q,X),d));zero(dot(sub(Q,F),d));return Q
# Generic focal foot and auxiliary-circle identity, modulo exact conic equations.
A,B,k,S,C=s.symbols('A B k S C')
G=s.groebner([C*C+S*S-1,B*B-A*A+k*k],C,B,A,k,S)
n=(-S/A,C/B);F=(k,0);lam=(1-dot(n,F))/dot(n,n)
q=(A*(k-A*S)/(A-k*S),A*B*C/(A-k*S))
for expr in [q[0]-k-lam*n[0],q[1]-lam*n[1],dot(q,q)-A*A]:
 num=s.fraction(s.cancel(expr))[0];check(G.reduce(s.expand(num))[1]==0)
# Strict source-domain triangle and its opposite phase.
z=s.Integer(0);r=s.sqrt(21);f=s.sqrt(5)
P=[(r,z),(-3*r/5,s.Rational(16,5)),(-3*r/5,-s.Rational(16,5))]
ca=(s.Rational(189,25),s.Rational(64,25));zero(21-ca[0]-(16-ca[1]));check(ca[0]>5 and ca[1]>0)
records=[]
for sign in (1,-1):
 V=[(sign*x,sign*y) for x,y in P]
 for x,y in V:zero(x*x/21+y*y/16-1)
 tangents=[(x/21,y/16) for x,y in V]
 outer=[]
 for i,n in enumerate(tangents):
  m=tangents[(i+1)%3];D=det(n,m);check(D!=0)
  U=(s.simplify((m[1]-n[1])/D),s.simplify((n[0]-m[0])/D));zero(dot(U,n)-1);zero(dot(U,m)-1);outer.append(U)
 check(area(V)>0);check(area(outer)>0)
 for i,X in enumerate(V):
  prev=V[(i-1)%3];Y=V[(i+1)%3];vin=sub(X,prev);vout=sub(Y,X)
  vin=tuple(s.simplify(x/s.sqrt(dot(vin,vin))) for x in vin);vout=tuple(s.simplify(x/s.sqrt(dot(vout,vout))) for x in vout)
  n=tangents[i]
  for j in range(2):zero(vout[j]-vin[j]+2*dot(vin,n)*n[j]/dot(n,n))
  edge=sub(Y,X);n=(-edge[1],edge[0]);h=dot(n,X)
  zero(ca[0]*n[0]**2+ca[1]*n[1]**2-h*h)
  contact=(s.simplify(ca[0]*n[0]/h),s.simplify(ca[1]*n[1]/h));zero(dot(n,contact)-h)
  t=s.simplify(dot(sub(contact,X),edge)/dot(edge,edge));check(t>0 and t<1)
 aa=[];bb=[]
 for fs in (1,-1):
  F=(fs*f,z);Q=[foot(F,V[i],V[(i+1)%3]) for i in range(3)];T=[foot(F,outer[i],outer[(i+1)%3]) for i in range(3)]
  Aq=area(Q);Bq=area(T);zero(Aq-s.Rational(84,625)*(7*r+sign*fs*f));zero(Bq-s.Rational(7,10)*(7*r+sign*fs*f));zero(Bq-s.Rational(125,24)*Aq);check(Aq>0 and Bq>0);aa.append(Aq);bb.append(Bq)
 zero(aa[0]*bb[1]-aa[1]*bb[0]);records.append({'original':list(map(str,aa)),'outer':list(map(str,bb)),'ratio':str(s.simplify(aa[0]/aa[1]))})
R=(7*r+f)/(7*r-f);check(R>1);check(1/R<1);zero(s.sympify(records[0]['ratio'])*s.sympify(records[1]['ratio'])-1)
# Exact reduced-lattice incidence and nonadjacent-original-pole controls.
from fractions import Fraction as Q
from math import gcd
periods=0
for N in range(3,25):
 for tau in range(1,(N+1)//2):
  if gcd(N,tau)!=1:continue
  delta=Q(tau,N);v=delta/2;r=Q(1,4)
  orbit=[(i*delta)%1 for i in range(N)];check(len(set(orbit))==N)
  # Original root is r in contact phase; outer roots r±v.
  for j in range(N):
   phase=(r-v-j*delta)%1
   original=[i for i in range(N) if (phase+v+i*delta-r)%1==0]
   outside=[i for i in range(N) if (phase+i*delta-(r-v))%1==0 or (phase+i*delta-(r+v))%1==0]
   check(original==[j]);check(set(outside)=={j,(j+1)%N})
  periods+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'lattice_period_turning_pairs':periods,'triangle_phases':records,'scope':'Exact algebra, source-domain reflection/contact/side-line checks, separate nonconstancy certificate and finite lattice controls. Universal analytic proof is in focal_pedal_ratios.pdf.'},indent=2))
