#!/usr/bin/env python3
"""Fresh integer Pauli-label controls; no import of published verification code."""
import json,datetime
from pathlib import Path
checks=[]
def mul(a,b):
 x,z,p=a;y,w,q=b
 return x^y,z^w,(p+q+2*((z&y).bit_count()))%4
def word(w):
 x=z=p=0
 for j,c in enumerate(w):
  if c in 'XY':x|=1<<j
  if c in 'ZY':z|=1<<j
  if c=='Y':p+=1
 return x,z,p%4
def quarter(P,Q,inverse=False):
 x,z,_=P;y,w,_=Q
 if (((x&w).bit_count()+(z&y).bit_count())%2)==0:return Q
 a,b,c=mul(P,Q);return a,b,(c+(-1 if inverse else 1))%4
def axes(n,i):
 return tuple(word('I'*(2*i)+v+'I'*(2*(n-i-2))) for v in ['IZZI','XIXX'])
def conj(Q,n,i,inverse=False):
 Z,X=axes(n,i)
 if inverse:return quarter(X,quarter(Z,Q,True),True)
 return quarter(Z,quarter(X,Q))
def collect(ts):
 r={}
 for x,z,p in ts:r[x,z]=r.get((x,z),0)+(1j)**p
 return {k:v for k,v in r.items() if v}
def rterms(n,i):
 Z,X=axes(n,i);a,b,p=mul(Z,X)
 return [(0,0,0),(Z[0],Z[1],1),(X[0],X[1],1),(a,b,(p+2)%4)]
def check(name,condition):
 if not condition:raise RuntimeError(name)
 checks.append({'name':name,'pass':True})
for n in range(2,33):
 delta=[i for last in range(n-1,0,-1) for i in range(last)]
 for j in range(n-1):
  out=[]
  for t in rterms(n,j):
   for i in reversed(delta):t=conj(t,n,i)
   out.append(t)
  check(f'Garside orientation n={n}, generator={j+1}',collect(out)==collect(rterms(n,n-2-j)))
 # Each U or V has a distinct independent binary Pauli label. Gaussian elimination.
 basis={};rank=0
 for i in range(n-1):
  for x,z,_ in axes(n,i):
   v=x|(z<<(2*n))
   while v:
    b=v.bit_length()-1
    if b in basis:v^=basis[b]
    else:basis[b]=v;rank+=1;break
 check(f'quaternionic normal-word label rank n={n}',rank==2*(n-1))
 for i in range(n-1):
  for j in range(2*n):
   for c in ['X','Z']:
    q=word('I'*j+c+'I'*(2*n-j-1));a=conj(q,n,i);back=conj(a,n,i,True)
    check(f'Clifford action/inverse n={n}, i={i}, j={j},{c}',back==q)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(checks),'pass':True,'strands':list(range(2,33)),'checks':checks,'limitation':'Finite controls through 32 strands; the arbitrary-n statement rests on the written tensor-reversal/Garside and Pauli-label arguments, not this finite run.'}
Path(__file__).with_name('fresh-global-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
