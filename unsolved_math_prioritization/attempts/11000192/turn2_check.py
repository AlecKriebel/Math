#!/usr/bin/env python3
import json,hashlib
from pathlib import Path
from turn1_quaternion import *
checks=0;undefined=0
def ck(v):
 global checks
 assert v;checks+=1

def power(q,n):return prod(*([q if n>=0 else inv(q)]*abs(n)))
def based(t):
 a,b,c,d,x,y,z,w=t
 return (mul(a,inv(d)),mul(d,b),x,z)
def tupleconj(t,q):return tuple(conjug(q,x) for x in t)
def angle_h(t,h):
 a,b,c,d,x,y,z,w=t;delta=sub(b,c);v=mul(d,delta);u=conjug(inv(h),mul(a,delta))
 return dot(v,u)**2/(dot(v,v)*dot(u,u))
def family(n):
 a=F(1-n*n,1+n*n);b=F(2*n,1+n*n);A1=(a,F(0),b,F(0));A2=(F(1,2),)*4;A3=conjug(j,A2);B1=prod(A1,A2,j);B2=conjug(inv(A1),B1)
 return (A1,A2,A3,one,B1,B2,j,j)
for n in range(1,12):
 t=family(n);ck(relation(t));a0,b0,x0,z0=based(t)
 for name in 'CD':
  out=gen(t,name);aa,bb,xx,zz=based(out);ck(aa==a0);ck(xx==x0)
 out=gen(t,'E');aa,bb,xx,zz=based(out);ck(aa==prod(a0,inv(z0)));ck(xx==x0);ck(zz==z0)
 # The entire based-generator chain identity, with representation pullbacks.
 lhs=based(word(t,'ABC'*4));rhs=tupleconj(based(word(t,'EE')),inv(z0));ck(lhs==rhs)
 # W fixes bz exactly; its higher-power analogues need a fresh check.
 wout=word(t,'dcBCD');ck(prod(wout[4],wout[6])==prod(x0,z0))
 for name in 'BC':
  aa,bb,xx,zz=based(gen(t,name));ck(aa==a0);ck(zz==z0)
 # Exact compatible h=a gate for finite k diagnostics.
 for kk in range(-3,4):
  src=word(t,'E'*(2*kk) if kk>=0 else 'e'*(-2*kk));aa,bb,xx,zz=based(src)
  ck(prod(aa,power(zz,kk))==prod(a0,power(z0,-kk)))
# Fixed counterexample to the two naive R4 angle invariants.
a,b=F(3,5),F(4,5);A1=(a,F(0),b,F(0));A2=(F(1,2),)*4;A3=conjug(j,A2);B1=prod(A1,A2,j);B2=conjug(inv(A1),B1);t=(A1,A2,A3,one,B1,B2,j,j)
r2=word(t,'eedcBCDEE');r4=word(t,'eeeedcBCDEEEE')
ck(invariant(t)==F(1,100));ck(invariant(r2)==F(1,100));ck(invariant(r4)==F(16,25))
ck(angle_h(t,power(t[4],2))==F(22801,62500));ck(angle_h(r4,power(r4[4],2))==F(47089,62500))
print(json.dumps({'problem_id':11000192,'author_turn':2,'exact_controls':checks,'R2_Fb':'1/100','R4_Fb':'16/25','R4_Fb2_before':'22801/62500','R4_Fb2_after':'47089/62500','scope':'Exact based-generator chain identity, sufficient-criterion input controls and specific failed power/angle repairs. Neither a pseudo-Anosov example nor absence in the full stabilizer is certified.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
