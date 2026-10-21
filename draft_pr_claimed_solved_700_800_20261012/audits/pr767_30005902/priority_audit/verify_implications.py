#!/usr/bin/env python3
"""Exact supporting checks for priority implication, no source or adjacent input reads."""
import itertools,json,math
from functools import lru_cache
P=3
B=list(itertools.product(range(3),repeat=3)); pos={b:i for i,b in enumerate(B)}
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def delta(b,cross=True):
    a,d,c=b; ans={}
    for i in range(a+1):
        for j in range(d+1):
            for u in range(c+1):
                for v in range(c-u+1):
                    w=c-u-v
                    if w and not cross:continue
                    left=(i+w,j,u);right=(a-i,d-j+w,v)
                    if max(left+right)>=3:continue
                    coef=math.comb(a,i)*math.comb(d,j)*math.factorial(c)//(math.factorial(u)*math.factorial(v)*math.factorial(w))
                    key=(pos[left],pos[right]);ans[key]=(ans.get(key,0)+coef)%P
    return {k:v for k,v in ans.items() if v}
D=[delta(b) for b in B]
def conv(f,g,table=D):return tuple(sum(co*f[i]*g[j] for (i,j),co in d.items())%P for d in table)
def sub(f,g):return tuple((a-b)%P for a,b in zip(f,g))
def ev(b):return tuple(int(c==b) for c in B)
E=ev((0,0,0));X=ev((1,0,0));Y=ev((0,1,0));Z=ev((0,0,1));zero=(0,)*27
def power(f,n):
    q=E
    for _ in range(n):q=conv(q,f)
    return q
def rank(m):
    a=[list(r) for r in m];r=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]%P),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];iv=pow(a[r][c],-1,P);a[r]=[(x*iv)%P for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                n=a[i][c];a[i]=[(x-n*y)%P for x,y in zip(a[i],a[r])]
        r+=1
    return r
def deriv(m,which,right=False):
    a,b,c=m;out={}
    def put(t,k):
        if k:out[t]=out.get(t,0)+k
    if which==0:
        if a:put((a-1,b,c),a)
        if right and c:put((a,b+1,c-1),c)
    elif which==1:
        if b:put((a,b-1,c),b)
        if not right and c:put((a+1,b,c-1),c)
    else:
        if c:put((a,b,c-1),c)
    return {t:k for t,k in out.items() if k}
def apply(poly,which,right):
    ans={}
    for mon,k in poly.items():
        for t,v in deriv(mon,which,right).items():ans[t]=ans.get(t,0)+k*v
    return {t:k for t,k in ans.items() if k}
def subtract(f,g):
    return {t:f.get(t,0)-g.get(t,0) for t in f.keys()|g.keys() if f.get(t,0)!=g.get(t,0)}
def main():
    need(sub(conv(X,Y),conv(Y,X))==Z,'dual Heisenberg commutator')
    need(sub(conv(X,Z),conv(Z,X))==zero,'X,Z centrality')
    need(sub(conv(Y,Z),conv(Z,Y))==zero,'Y,Z centrality')
    for f in (X,Y,Z):need(power(f,3)==zero,'restricted cube')
    rows=[conv(conv(power(X,a),power(Y,b)),power(Z,c)) for a,b,c in B]
    rk=rank(rows);need(rk==27,'PBW dual pairing rank')
    mutation=[delta(b,cross=False) for b in B]
    need(sub(conv(X,Y,mutation),conv(Y,X,mutation))==zero,'cross-term deletion mutation')
    mons=list(itertools.product(range(7),repeat=3))
    for right in (False,True):
        for m in mons:
            pol={m:1}
            bracket=subtract(apply(apply(pol,1,right),0,right),apply(apply(pol,0,right),1,right))
            expected={t:(-1 if right else 1)*k for t,k in apply(pol,2,right).items()}
            need(bracket==expected,'rational invariant derivation bracket')
    return {'status':'PASS','finite_field':3,'finite_dimension':27,'pbw_pairing_rank':rk,
      'dual_commutator':'[X,Y]=Z','restricted_cubes_zero':True,
      'FS_L_bracket':'[L_x,L_y]=L_z','tensor_induction_R_bracket':'[R_x,R_y]=-R_z',
      'rational_monomials_checked_per_orientation':len(mons),'cross_term_deletion_detected':True,
      'scope':'exact supplemental arithmetic; written proof determines derivations on all polynomials'}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
