"""Independent extension-field and bimodule-cut diagnostics, not a universal proof."""
from itertools import product
import json

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def field(p):
    # F4=F2[t]/(t^2+t+1), F9=F3[t]/(t^2+1).
    def add(x,y):return ((x%p+y%p)%p)+p*((x//p+y//p)%p)
    def neg(x):return ((-x)%p)+p*((-(x//p))%p)
    def mul(x,y):
        a,b=x%p,x//p;c,d=y%p,y//p
        return ((a*c-b*d)%p)+p*((a*d+b*c-(b*d if p==2 else 0))%p)
    def inv(x):
        require(x!=0,'zero inverse')
        return next(y for y in range(1,p*p) if mul(x,y)==1)
    require(all(mul(x,inv(x))==1 for x in range(1,p*p)),'field inverses')
    return add,neg,mul,inv

def rank(rows,p):
    add,neg,mul,inv=field(p);a=[r[:] for r in rows];k=0
    for j in range(len(a[0]) if a else 0):
        hit=next((i for i in range(k,len(a)) if a[i][j]),None)
        if hit is None:continue
        a[k],a[hit]=a[hit],a[k];v=inv(a[k][j]);a[k]=[mul(x,v) for x in a[k]]
        for i in range(k+1,len(a)):
            c=a[i][j];a[i]=[add(x,neg(mul(c,y))) for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def main():
    cases=[]
    for p in [2,3]:
        for r,n in [(0,1),(1,2),(1,3),(2,1),(2,2),(2,3),(2,4),(3,2)]:
            ws=list(product(range(r),repeat=n));idx={w:i for i,w in enumerate(ws)};N=len(ws);b=[[0]*N for _ in ws];b2=[[0]*N for _ in ws]
            for j,w in enumerate(ws):
                rot=w[-1:]+w[:-1];twice=rot[-1:]+rot[:-1]
                for dest,c in [(w,1),(rot,-1)]:b[idx[dest]][j]=(b[idx[dest]][j]+c)%p
                for dest,c in [(w,1),(rot,-2),(twice,1)]:b2[idx[dest]][j]=(b2[idx[dest]][j]+c)%p
            hi=rank(b,p)-rank(b2,p)
            reps={min(w[i:]+w[:i] for i in range(n)) for w in ws}
            expected=sum(len({w[i:]+w[:i] for i in range(n)})%p==0 for w in reps)
            require(hi==expected,'extension-field orbit dimension mismatch')
            cases.append({'field_order':p*p,'r':r,'n':n,'higher_H0_and_H1':hi})
        for n in range(0,11):
            edges=[[((1 if i==j+1 else 0)-(1 if i==j else 0))%p for j in range(n)] for i in range(n+1)]
            require(rank(edges,p)==n,'bimodule word-cut incidence not injective')
    print(json.dumps({'status':'PASS','extension_cases':cases,'bimodule_cut_cases':22,'unlimited_proof':False},sort_keys=True,indent=2))

if __name__=='__main__':main()
