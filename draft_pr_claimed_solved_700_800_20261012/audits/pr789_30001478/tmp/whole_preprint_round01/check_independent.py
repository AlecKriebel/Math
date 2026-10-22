"""Independent diagnostics and exact integer identities. Not a universal proof checker."""
from itertools import product
from math import comb
import json

def need(ok,msg):
 if not ok:raise ValueError(msg)

def clean(d,p=None):return {w:(c%p if p else c) for w,c in d.items() if (c%p if p else c)}
def rels():
 # coefficient keys encode alpha,beta exponents; word indices 0..3
 return [[((1,0),(0,0),1),((0,0),(0,2),-1),((0,0),(2,0),1),((1,0),(2,2),-1)],
 [((1,0),(0,1),1),((0,0),(0,3),-1),((0,0),(2,1),1),((1,0),(2,3),-1)],
 [((1,0),(1,0),1),((0,0),(1,2),-1),((0,0),(3,0),1),((1,0),(3,2),-1)],
 [((1,0),(1,1),1),((0,0),(1,3),-1),((0,0),(3,1),1),((1,0),(3,3),-1)],
 [((0,1),(0,0),1),((0,0),(0,1),-1),((0,0),(3,0),1),((0,1),(3,1),-1)],
 [((0,1),(0,2),1),((0,0),(0,3),-1),((0,0),(3,2),1),((0,1),(3,3),-1)]]
def exact():
 out=[]
 for r in rels():
  d={}
  for c,w,v in r:
   k=(c,tuple(i%2 for i in w));d[k]=d.get(k,0)+v
  out.append(clean(d))
 q={((0,1),(0,0)):1,((0,0),(0,1)):-1,((0,0),(1,0)):1,((0,1),(1,1)):-1}
 need(out==[{}, {}, {}, {}, q,q],"six relation substitutions")
 # theta on second tensor factor, polynomial coefficient exponent in beta.
 d={}
 for (c,w),v in q.items():
  need(c[0]==0,"unexpected alpha exponent")
  for j in range(2):
   e=c[1]+(j!=w[1]);k=(e,(w[0],j));d[k]=d.get(k,0)+v
 d=clean(d)
 need(d=={(2,(0,1)):1,(0,(0,1)):-1,(0,(1,0)):1,(2,(1,0)):-1},"tensor transform identity")
 return {'six_relation_images':'0,0,0,0,Q,Q over Z[alpha,beta]','id_tensor_theta_Q':'(beta^2-1)(s tensor t - t tensor s) over Z[beta]','characteristic_two_valid':True}
def rank(rows,p):
 piv={}
 for row in rows:
  a=clean(dict(row),p)
  while a:
   j=min(a)
   if j not in piv:
    f=pow(a[j],-1,p);piv[j]={k:v*f%p for k,v in a.items()};break
   f=a[j];a=clean({k:a.get(k,0)-f*piv[j].get(k,0) for k in set(a)|set(piv[j])},p)
 return len(piv)
def diagnostic(p,b,n):
 Q={(0,0):b,(0,1):-1,(1,0):1,(1,1):-b}; rows=[]
 for i in range(n-1):
  for l in product(range(2),repeat=i):
   for r in product(range(2),repeat=n-i-2):
    rows.append({int(''.join(map(str,l+w+r)),2):c for w,c in Q.items()})
 return 2**n-rank(rows,p)
def gf4mul(a,b):
 c=0
 for i in range(2):
  for j in range(2):
   if (a>>i)&1 and (b>>j)&1:c^=1<<(i+j)
 if c&4:c^=7
 return c

def gf4dim(b,n):
 rows=[]
 for i in range(n-1):
  for l in product(range(2),repeat=i):
   for r in product(range(2),repeat=n-i-2):
    row=[0]*(2**n)
    for w,c in [((0,0),b),((0,1),1),((1,0),1),((1,1),b)]:
     row[int(''.join(map(str,l+w+r)),2)]=c
    rows.append(row)
 piv={}
 for row in rows:
  for j in range(len(row)):
   if row[j]:
    if j in piv:
     f=row[j];row=[x^gf4mul(f,y) for x,y in zip(row,piv[j])]
    else:
     inv=gf4mul(row[j],row[j]);piv[j]=[gf4mul(inv,x) for x in row];break
 return 2**n-len(piv)

def main():
 e=exact(); tests=[]
 for p in [2,3,5,7,11]:
  for b in range(p):
   if (b*b-1)%p:
    ds=[diagnostic(p,b,n) for n in range(1,8)]
    need(ds==list(range(2,9)),str((p,b,ds)))
    tests.append({'p':p,'beta':b,'dimensions_degrees_1_to_7':ds})
 gf4=[]
 for b in [2,3]:
  ds=[gf4dim(b,n) for n in range(1,9)];need(ds==list(range(2,10)),"GF4 dimensions");gf4.append({'beta':b,'dimensions_degrees_1_to_8':ds})
 # singular relation has nonzero linear factors; check char2 repeated factor degree3 exception.
 need(diagnostic(2,1,3)==5,"singular characteristic2 control")
 result={'result':'PASS','exact_identities':e,'finite_quotient_dimensions':tests,'case_count':len(tests),'gf4_checks':gf4,'singular_char2_beta1_degree3_dimension':5,'scope':'Exact integer polynomial identities plus finite modular ranks through degree7; universal kernel/domain/THCR/sigma-ampleness are proved separately in REPORT.md.'}
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
