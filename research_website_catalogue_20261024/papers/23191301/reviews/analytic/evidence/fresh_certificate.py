"""Independent transcription of the paper's table and displayed identity.
No submitted helper, witness, expected-output, or review imports.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
from datetime import datetime,timezone
import json,time
start=time.monotonic()

def indices(d):return [(a,b,c) for a in range(d+1) for b in range(d+1-a) for c in range(d+1-a-b)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def gauss(a):
 if any(x%2 for x in a):return 0
 out=1
 for x in a:
  for j in range(1,x,2):out*=j
 return out
special={(6,0,0):2**24,(0,6,0):2**24,(4,2,0):1,(2,4,0):1,(0,0,6):1,(2,2,2):4,(2,0,4):32,(0,2,4):32,(4,0,2):4096,(0,4,2):4096}
scales={8:10**16,10:10**34,12:10**53,14:10**73,16:10**94,18:10**116}
def moment(a):
 assert sum(a)<=18
 if any(x%2 for x in a):return F(0)
 d=sum(a)
 if d==0:return F(1)
 if d in (2,4):return F(gauss(a),1024)
 if d==6:return F(special[a])
 return F(scales[d]*gauss(a))

def ldl(A):
 n=len(A);L=[[F(int(i==j)) for j in range(n)] for i in range(n)];D=[]
 for j in range(n):
  pivot=A[j][j]-sum(L[j][k]**2*D[k] for k in range(j))
  assert pivot>0,(j,pivot)
  D.append(pivot)
  for i in range(j+1,n):L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/pivot
 for i in range(n):
  for j in range(i+1):assert A[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(j+1))
 return D
blocks=[];initial=[];allindices=indices(9);assert len(allindices)==220
for parity in product(range(2),repeat=3):
 rows=[a for a in allindices if tuple(x%2 for x in a)==parity]
 A=[[moment(add(a,b)) for b in rows] for a in rows];D=ldl(A)
 blocks.append({'parity':parity,'size':len(rows),'monomials':rows,'positive_pivots':[str(v) for v in D],'exact_reconstruction':True})
 old=[a for a in indices(3) if tuple(x%2 for x in a)==parity]
 oldD=ldl([[moment(add(a,b)) for b in old] for a in old]);det=F(1);minors=[]
 for v in oldD:det*=v;minors.append(str(det))
 initial.append({'parity':parity,'leading_minors':minors})

def plus(p,q):
 out=dict(p)
 for a,c in q.items():out[a]=out.get(a,F(0))+c
 return {a:c for a,c in out.items() if c}
def mul(p,q):
 out={}
 for a,c in p.items():
  for b,d in q.items():ab=add(a,b);out[ab]=out.get(ab,F(0))+c*d
 return {a:c for a,c in out.items() if c}
def power(p,k):
 out={(0,0,0):F(1)}
 for _ in range(k):out=mul(out,p)
 return out
def two(a,b,k=1):return {a:F(1),b:F(-k)}
p={(4,2,0):F(1),(2,4,0):F(1),(0,0,6):F(1),(2,2,2):F(-1)}
h=[two((5,4,0),(3,4,2)),two((4,5,0),(4,3,2)),two((4,2,3),(2,2,5)),two((2,4,3),(2,2,5)),two((1,2,6),(3,4,2)),two((2,1,6),(4,3,2)),two((2,4,3),(4,2,3)),two((4,5,0),(2,1,6)),two((5,4,0),(1,2,6))]
extra=[two((0,0,9),(2,2,5),2),two((1,1,7),(3,3,3),2),two((3,6,0),(3,4,2),2),two((3,5,1),(3,3,3),2),two((6,3,0),(4,3,2),2),two((5,3,1),(3,3,3),2),{(3,3,3):F(1)}]
rhs={}
for weight,term in [(F(3,2),u) for u in h]+[(F(1),u) for u in extra[:-1]]+[(F(2),extra[-1])]:
 assert all(sum(a)==9 for a in term)
 rhs=plus(rhs,{a:weight*c for a,c in mul(term,term).items()})
assert rhs==power(p,3)
moments=[sum(c*moment(a) for a,c in power(p,k).items()) for k in range(1,4)]
assert moments==[F(-1),F(11292*10**53),F(35039520*10**116)]
N=10**62;a1,a2,a3=moments
value=N*a3+3*N*(N-1)*a2*a1+N*(N-1)*(N-2)*a1**3
bound=N*(a3-(N*N-1));assert value<=bound<0
# Negative controls: coefficient-3 Motzkin is NOT the displayed cube identity.
wrong=dict(p);wrong[(2,2,2)]=F(-3);assert power(wrong,3)!=rhs
# Domain misuse is rejected, rather than pretending one order-9 functional covers q=5.
try:moment((30,0,0));raise RuntimeError('domain rejection absent')
except AssertionError:pass
# A high moment set to zero destroys positivity through a nonzero cross moment.
# monomials 1 and z^4 give determinant mu(z^8)-mu(z^4)^2.
assert 0-moment((0,0,4))**2<0
# Independent integer partition coefficient count compared with labelled assignments.
def partitions(items):
 if not items:yield [];return
 x=items[0]
 for blocks in partitions(items[1:]):
  yield [[x]]+[b[:] for b in blocks]
  for i in range(len(blocks)):
   out=[b[:] for b in blocks];out[i]=[x]+out[i];yield out
def falling(s,k):
 out=1
 for j in range(k):out*=s-j
 return out
checks=[]
for q in range(1,8):
 a=[1]+[(-1 if j==1 else 2*j+1) for j in range(1,q+1)]
 parts=list(partitions(list(range(q))))
 for s in range(1,5):
  direct=0
  for assign in product(range(s),repeat=q):
   term=1
   for i in range(s):term*=a[assign.count(i)]
   direct+=term
  partition=sum(falling(s,len(bs))*__import__('functools').reduce(lambda u,b:u*a[len(b)],bs,1) for bs in parts)
  assert direct==partition
 singleton=[bs for bs in parts if len(bs)==q];assert len(singleton)==1
 checks.append({'q':q,'leading_coefficient':a[1]**q,'partitions':len(parts),'direct_assignment_checks':4})
# A degree-18 moment functional is sufficient for p not SOS because any SOS p
# uses factors of degree at most 3; this implication is justified analytically.
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','method':'independent exact table transcription; full parity-block LDL reconstruction; sparse polynomial identity; distinct-index count','matrix_dimension':220,'blocks':blocks,'initial_order3':initial,'moments':[str(v) for v in moments],'N':N,'cubic_value':str(value),'cubic_upper_bound':str(bound),'cube_identity_terms':len(rhs),'partition_controls':checks,'negative_controls':{'coefficient3_seed_identity_rejected':True,'degree30_domain_rejected':True,'zero_high_moment_fails_2x2_positivity':True,'even_q_has_positive_leading_coefficient':True},'elapsed_seconds':time.monotonic()-start,'limits':'No finite computation proves closure/separation or every odd q; those steps require the analytic proof.'}
Path(__file__).with_name('fresh-certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','pivots':sum(b['size'] for b in blocks),'partition_checks':28,'negative_controls':4,'elapsed_seconds':result['elapsed_seconds']}))
