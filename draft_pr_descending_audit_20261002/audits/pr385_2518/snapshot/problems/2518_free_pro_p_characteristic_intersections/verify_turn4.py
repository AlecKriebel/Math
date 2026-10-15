#!/usr/bin/env python3
import itertools,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1
cases=[]
for p in (2,3,5):
 for e in (1,2):
  q=p**e;cases.append((p,'C'+str(q),list(range(q)),0,lambda a,b,q=q:(a+b)%q))
 pts=list(itertools.product(range(p),repeat=3))
 cases.append((p,'Heisenberg_'+str(p),pts,(0,0,0),lambda a,b,p=p:((a[0]+b[0])%p,(a[1]+b[1])%p,(a[2]+b[2]+a[0]*b[1])%p)))
summary=[]
for p,name,A,e,op in cases:
 def bm(a,b):return tuple(op(x,y) for x,y in zip(a,b))
 def shift(a,k):return tuple(a[(i-k)%p] for i in range(p))
 def mul(x,y):a,i=x;b,j=y;return bm(a,shift(b,i)),(i+j)%p
 ident=(tuple([e]*p),0);s=(tuple([e]*p),1);si=(tuple([e]*p),p-1)
 ck(mul(s,si)==ident)
 for a in A:
  if a==e:continue
  base=[e]*p;base[0]=a;x=(tuple(base),0)
  conjugate=mul(mul(s,x),si)
  ck(conjugate!=x);ck(conjugate==(shift(x[0],1),0))
  orbit={mul(mul((s[0],j),x),(s[0],(-j)%p)) for j in range(p)}
  ck(len(orbit)==p)
 summary.append({'lamp_group':name,'lamp_order':len(A),'top_order':p})
for p in (2,3,5,7):
 def m(a,b):return ((a[0]+b[0])%p,(a[1]+b[1])%p,(a[2]+b[2]+a[0]*b[1])%p)
 def inv(a):return (-a[0]%p,-a[1]%p,(-a[2]+a[0]*a[1])%p)
 x=(1,0,0);y=(0,1,0);z=m(m(m(x,y),inv(x)),inv(y))
 ck(z==(0,0,1));ck(z!=(0,0,0))
print(json.dumps({'turn':4,'assertions':checks,'finite_wreath_controls':summary,'scope':'finite p-group separators; Hall theorem and universal property remain explicit proof inputs'},sort_keys=True,indent=2))
