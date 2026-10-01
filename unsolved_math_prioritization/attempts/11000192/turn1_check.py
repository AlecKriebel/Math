#!/usr/bin/env python3
import json,hashlib,itertools
from pathlib import Path
from turn1_quaternion import *
checks=0;skips=0
def ck(x):
 global checks
 assert x;checks+=1
# Exact Artin action on the free group of rank6: a finite certificate of word identities.
def red(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inverse(w):return tuple(-x for x in w[::-1])
def subst(w,a):return red(sum((a[x-1] if x>0 else inverse(a[-x-1]) for x in w),()))
I=tuple((i,) for i in range(1,7))
def artin(c):
 n=ord(c.upper())-ord('A')+1;v=list(I)
 if c.isupper():v[n-1]=(n,n+1,-n);v[n]=(n,)
 else:v[n-1]=(n+1,);v[n]=(-(n+1),n,n+1)
 return tuple(v)
def aut(s):
 out=I
 for c in s:out=tuple(subst(w,out) for w in artin(c))
 return out
for a in 'ABCDE':ck(aut(a+a.lower())==I);ck(aut(a.lower()+a)==I)
for a,b in zip('ABCD','BCDE'):ck(aut(a+b+a)==aut(b+a+b))
for a,b in itertools.combinations('ABCDE',2):
 if ord(b)-ord(a)>1:ck(aut(a+b)==aut(b+a))
R='eedcBCDEE'
ck(aut('CD'+'C'+'dc')==aut('D'))
ck(aut('DE E DE E'.replace(' ',''))==aut('DEDEDE'))
ck(aut('EE DEE D'.replace(' ',''))==aut('DEDEDE'))
ck(aut('DEED eed'.replace(' ',''))==aut('eeDEE'))
ck(aut(R+'C')==aut('C'+R))
# Exact positive-measure nonconstancy witnesses (smoothness established analytically).
values=[]
for n in range(1,16):
 a=F(1-n*n,1+n*n);b=F(2*n,1+n*n)
 t=((a,b,F(0),F(0)),k,inv(k),one,i,i,j,j)
 ck(relation(t));ck(invariant(t)==a*a);values.append(str(invariant(t)))
 ck(dot(i,j)==0);ck(mul(i,j)!=mul(j,i))
# Generic rational test family, all source-generator inverses, both braid controls.
for n in range(1,11):
 a=F(1-n*n,1+n*n);b=F(2*n,1+n*n);A1=(a,F(0),b,F(0));A2=(F(1,2),)*4;A3=conjug(j,A2);B1=prod(A1,A2,j);B2=conjug(inv(A1),B1);t=(A1,A2,A3,one,B1,B2,j,j)
 ck(relation(t));f=invariant(t)
 for name in 'ABCDE':
  for sign in (1,-1):ck(gen(gen(t,name,sign),name,-sign)==t)
 ck(word(t,'CDC')==word(t,'DCD'));ck(word(t,'BCB')==word(t,'CBC'))
 for w in ['C','D',R,'C'+R,'D'+R]:
  try:ck(invariant(word(t,w))==f)
  except ZeroDivisionError:skips+=1
 ck(word(t,R+'C')==word(t,'C'+R))
# A specific countercontrol rules out the naive opposite-conjugation repair.
a,b=F(3,5),F(4,5);A1=(a,F(0),b,F(0));A2=(F(1,2),)*4;A3=conjug(j,A2);B1=prod(A1,A2,j);B2=conjug(inv(A1),B1);t=(A1,A2,A3,one,B1,B2,j,j)
ck(invariant(t)==F(1,100));ck(invariant(word(t,'eeCDBdcEE'))==F(961,62500));ck(F(1,100)!=F(961,62500))
print(json.dumps({'problem_id':11000192,'author_turn':1,'exact_controls':checks,'undefined_domain_cases_recorded':skips,'witness_values':values,'naive_opposite_conjugation_values':['1/100','961/62500'],'scope':'Exact Artin-word identities and rational quaternion controls support the unreviewed scoped partial. No pseudo-Anosov example or full original resolution is certified.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'quaternion_module_sha256':hashlib.sha256(Path(__file__).with_name('turn1_quaternion.py').read_bytes()).hexdigest()},indent=2,sort_keys=True))
