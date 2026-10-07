#!/usr/bin/env python3
"""Exact, bounded algebraic controls. They do not compute a general fusion obstruction."""
import itertools,json

def require(x,msg):
    if not x: raise RuntimeError(msg)

def rank(rows,p):
    a=[list(r) for r in rows]
    if not a:return 0
    k=0
    for j in range(len(a[0])):
        hit=next((i for i in range(k,len(a)) if a[i][j]%p),None)
        if hit is None:continue
        a[k],a[hit]=a[hit],a[k]
        t=pow(a[k][j]%p,-1,p);a[k]=[(v*t)%p for v in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]%p:
                t=a[i][j]%p;a[i]=[(v-t*w)%p for v,w in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

out={'scope':'Carry cocycles and invariant linear forms are method controls, not counterexamples to the fusion-preserving extension question.','cyclic_H2':[],'wreath_linear_forms':[],'coprime_cyclic_modules':[]}
for p in (2,3,5,7):
    one=list(range(1,p));two=list(itertools.product(one,repeat=2))
    def bvec(i):return [int(i==a) for a in one]
    def cvec(i,j):return [int((i,j)==a) for a in two]
    d1=[[ (x-y+z)%p for x,y,z in zip(bvec(j),bvec((i+j)%p),bvec(i))] for i,j in two]
    d2=[[ (a-b+c-d)%p for a,b,c,d in zip(cvec(j,k),cvec((i+j)%p,k),cvec(i,(j+k)%p),cvec(i,j))] for i,j,k in itertools.product(range(p),repeat=3)]
    carry=[(i+j)//p for i,j in two]
    require(all(sum(a*b for a,b in zip(row,carry))%p==0 for row in d2),'carry is a 2-cocycle')
    r1=rank(d1,p);r2=rank(d2,p)
    require(len(two)-r2-r1==1,'cyclic H2 dimension one')
    augmented=[row+[v] for row,v in zip(d1,carry)]
    require(rank(augmented,p)==r1+1,'carry not a coboundary')
    require(sum((i+1)//p for i in range(p))%p==1,'telescoping obstruction is one')
    out['cyclic_H2'].append({'p':p,'C1_dimension':len(one),'C2_dimension':len(two),'d1_rank':r1,'d2_rank':r2,'H2_dimension':1,'carry_not_coboundary':True})
for p in (2,3,5):
    for n in (p,p-1):
        forms=[]
        for a in itertools.product(range(p),repeat=n):
            if all(a[i]==a[i+1] for i in range(n-1)):forms.append(a)
        require(len(forms)==p,'invariant linear forms')
        diagonal=[sum(a)%p for a in forms]
        if n%p==0:require(set(diagonal)=={0},'no diagonal retraction in divisible case')
        else:require(1 in diagonal,'prime-to-p control has retraction')
        out['wreath_linear_forms'].append({'p':p,'n':n,'all_linear_forms_tested':p**n,'invariant_forms':len(forms),'diagonal_coefficients':diagonal,'retraction_exists':1 in diagonal})
# Periodic cyclic-group resolution on one-dimensional F_p modules.
# H^1=ker(N)/im(A-1), H^2=ker(A-1)/im(N).
for p in (2,3,5,7):
    for m in range(1,9):
        if m%p==0:continue
        for lam in range(1,p):
            if pow(lam,m,p)!=1:continue
            N=sum(pow(lam,j,p) for j in range(m))%p
            A=(lam-1)%p
            h1=int(N==0)-int(A!=0)
            h2=int(A==0)-int(N!=0)
            require(h1==h2==0,'coprime cyclic cohomology vanishes')
            out['coprime_cyclic_modules'].append({'p':p,'order':m,'action_scalar':lam,'norm_scalar':N,'H1_dimension':h1,'H2_dimension':h2})
print(json.dumps(out,sort_keys=True,indent=2))
