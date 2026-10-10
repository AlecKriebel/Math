from itertools import product
from pathlib import Path
import json

def lr(lam,mu,nu):
 if any(nu[i]<lam[i] for i in range(3)) or nu[2]<0:return 0
 rows=[list(range(lam[i]+1,nu[i]+1)) for i in range(3)]
 if sum(map(len,rows))!=sum(mu):raise AssertionError('degree')
 out=0
 for twos in product(*(range(len(row)+1) for row in rows)):
  if sum(twos)!=mu[1]:continue
  vals={}
  for i,row in enumerate(rows):
   for j,col in enumerate(row): vals[i,col]=1 if j<len(row)-twos[i] else 2
  okay=True
  for col in range(1,max(nu)+1):
   cv=[vals[i,col] for i in range(3) if (i,col) in vals]
   if any(a>=b for a,b in zip(cv,cv[1:])):okay=False;break
  if not okay:continue
  balance=0
  for i,row in enumerate(rows):
   for col in reversed(row):
    balance += 1 if vals[i,col]==1 else -1
    if balance<0:okay=False;break
   if not okay:break
  if okay:out+=1
 return out
checks=0
for N in range(1,11):
 for k in range(1,N//2+1):
  for a in range(k-1,N-k+2):
   for c in range(k-1,N-k+2):
    delta=a-c
    if delta%3:continue
    h=delta//3
    val=lr((N,N-a,0),(N,c,0),(N+k-h,N-h,N-k-h))
    expected=k+int(min(a,N-a)>=k) if delta==0 else max(0,k-2*abs(h)+1)
    assert val==expected,(N,k,a,c,val,expected)
    checks+=1
# Independently check the diagonal formula over all k, including zero/empty rows.
for a in range(9):
 for b in range(9):
  N=a+b
  for k in range(N+1):
   val=lr((N,b,0),(N,a,0),(N+k,N,N-k))
   assert val==min(a,b,k,N-k)+1,(a,b,k,val)
   checks+=1
out={'status':'PASS','independent_direct_tableau_enumerations':checks,'stable_strip_height_max':10,'diagonal_labels_each_max':8,'note':'Direct skew tableau enumeration checks the frozen multiplicity formulas; not a new author search or universal proof by finite enumeration.'}
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
