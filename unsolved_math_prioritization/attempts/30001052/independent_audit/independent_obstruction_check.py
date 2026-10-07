#!/usr/bin/env python3
"""Independent controls using unnormalized cochains and finite-field DomainMatrix."""
from itertools import product,permutations
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import GF
import json

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def rank(rows,p):return DomainMatrix.from_list(rows,GF(p)).rank()
result={'status':'PASS','cochain_convention':'unnormalized, independent of author matrices','cyclic_H2':[],'wreath':[],'coprime_modules':[]}
for p in (2,3,5,7):
    one=list(range(p)); pairs=list(product(one,repeat=2)); triples=list(product(one,repeat=3))
    d1=[]
    for i,j in pairs:
        row=[0]*p
        row[j]+=1;row[(i+j)%p]-=1;row[i]+=1
        d1.append(row)
    d2=[]
    for i,j,k in triples:
        row=[0]*(p*p)
        row[j*p+k]+=1;row[((i+j)%p)*p+k]-=1
        row[i*p+(j+k)%p]+=1;row[i*p+j]-=1
        d2.append(row)
    carry=[int(i+j>=p) for i,j in pairs]
    need(all(sum(x*y for x,y in zip(row,carry))%p==0 for row in d2),'carry cocycle')
    r1,r2=rank(d1,p),rank(d2,p)
    need(p*p-r1-r2==1,'H2 dimension')
    need(rank([row+[c] for row,c in zip(d1,carry)],p)==r1+1,'nontrivial carry class')
    need(all(sum(d2[i][k]*d1[k][j] for k in range(p*p))%p==0 for i in range(len(d2)) for j in range(p)),'d2 d1 zero')
    result['cyclic_H2'].append({'p':p,'C1':p,'C2':p*p,'d1_rank':r1,'d2_rank':r2,'H2':1,'carry_nontrivial':True})
for p in (2,3,5):
    for n in (p,p-1):
        perms=list(permutations(range(n)))
        fixed=[a for a in product(range(p),repeat=n) if all(tuple(a[i] for i in sigma)==a for sigma in perms)]
        diagonal=[sum(a)%p for a in fixed]
        need(len(fixed)==p,'fixed forms')
        need((1 in diagonal)==(n%p!=0),'diagonal retraction criterion')
        result['wreath'].append({'p':p,'n':n,'all_forms':p**n,'all_permutations':len(perms),'fixed_forms':len(fixed),'diagonal_coefficients':diagonal})
for p in (2,3,5,7):
    for m in range(1,9):
        if m%p==0:continue
        for lam in range(1,p):
            if pow(lam,m,p)!=1:continue
            action=lambda x:((lam-1)*x)%p
            norm=lambda x:sum(pow(lam,k,p)*x for k in range(m))%p
            image_action={action(x) for x in range(p)}
            kernel_norm={x for x in range(p) if norm(x)==0}
            image_norm={norm(x) for x in range(p)}
            kernel_action={x for x in range(p) if action(x)==0}
            need(image_action==kernel_norm and image_norm==kernel_action,'cyclic cohomology exactness')
            result['coprime_modules'].append({'p':p,'m':m,'lambda':lam,'H1_zero':True,'H2_zero':True})
print(json.dumps(result,indent=2,sort_keys=True))
