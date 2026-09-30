"""Exploratory degree-three Magnus obstruction; no result certified by this script alone."""
import sympy as s, json
from itertools import combinations
from functools import cmp_to_key
from collections import defaultdict
from pathlib import Path
a=(1+s.sqrt(5))/2
def simp(z): return s.radsimp(s.simplify(s.expand(z)))
def sign(z):
    z=s.expand(simp(z)); p=z.coeff(s.sqrt(5),0); q=z.coeff(s.sqrt(5),1)
    assert p.is_Rational and q.is_Rational
    if q==0:return int(bool(p>0))-int(bool(p<0))
    if p==0:return int(bool(q>0))-int(bool(q<0))
    if p*q>0:return 1 if p>0 else -1
    d=p*p-5*q*q
    assert d!=0
    return (1 if p>0 else -1)*(1 if d>0 else -1)
lines=[(0,1,0),(0,1,-1),(1,-a,0),(1,-a,a),(a,-1,0),(a,-1,-a),(1,0,0),(1,0,-1)]
points={}
for i,j in combinations(range(8),2):
    A,B,C=lines[i];D,E,F=lines[j]
    den=simp(A*E-B*D)
    if den==0:continue
    x=simp((B*F-C*E)/den);y=simp((C*D-A*F)/den)
    points.setdefault((x,y),set()).update((i,j))
for beta in [2,3,5,7,11,13]:
    ts=[simp(x+beta*y) for x,y in points]
    if len(set(ts))==len(ts) and all(simp(B-A*beta)!=0 for A,B,C in lines):break
events=sorted([(simp(x+beta*y),sorted(L)) for (x,y),L in points.items()],key=cmp_to_key(lambda x,y:sign(x[0]-y[0])))
t0=events[0][0]-1
height=lambda i:simp(-(lines[i][0]*t0+lines[i][2])/(lines[i][1]-lines[i][0]*beta))
order=sorted(range(8),key=cmp_to_key(lambda i,j:sign(height(i)-height(j))))
one={():1}
def add(A,B,scale=1):
    C=dict(A)
    for m,v in B.items():
        C[m]=C.get(m,0)+scale*v
        if not C[m]:del C[m]
    return C
def mul(A,B):
    C=defaultdict(int)
    for m,u in A.items():
        for n,v in B.items():
            if len(m+n)<=3:C[m+n]+=u*v
    return {m:v for m,v in C.items() if v}
def inv(A):
    q=add(A,one,-1)
    return add(add(add(one,q,-1),mul(q,q)),mul(mul(q,q),q),-1)
def comm(A,B):return mul(mul(mul(A,B),inv(A)),inv(B))
def relators(sign=1):
    labels=order[:]
    words=[{():1,(i,):1} for i in order]
    out=[]
    for t,L in events:
        pos=sorted(labels.index(i) for i in L)
        assert pos==list(range(pos[0],pos[-1]+1)),(t,L,labels)
        P=one
        for i in pos:P=mul(P,words[i])
        for i in pos[:-1]:out.append(add(comm(words[i],P),one,-1))
        # Positive or negative half twist on the contiguous block.
        for end in range(pos[-1],pos[0],-1):
            for i in range(pos[0],end):
                U,V=words[i],words[i+1]
                words[i:i+2]=[mul(mul(U,V),inv(U)),U] if sign==1 else [V,mul(mul(inv(V),U),V)]
                labels[i],labels[i+1]=labels[i+1],labels[i]
    return out
def row_add(basis,row,p,comb=None):
    r={j:v%p for j,v in row.items() if v%p}
    c=None if comb is None else {j:v%p for j,v in comb.items() if v%p}
    while r:
        k=min(r);v=r[k]
        if k not in basis:
            z=pow(v,-1,p)
            r={j:u*z%p for j,u in r.items()}
            if c is not None:c={j:u*z%p for j,u in c.items()}
            basis[k]=(r,c)
            return True
        b,bc=basis[k]
        for j,u in b.items():
            w=(r.get(j,0)-v*u)%p
            if w:r[j]=w
            elif j in r:del r[j]
        if c is not None:
            for j,u in bc.items():
                w=(c.get(j,0)-v*u)%p
                if w:c[j]=w
                elif j in c:del c[j]
    return False
def reduce(basis,row,p,wantcomb=False):
    r={j:v%p for j,v in row.items() if v%p};c={}
    for k,(b,bc) in sorted(basis.items()):
        v=r.get(k,0)
        if not v:continue
        for j,u in b.items():
            w=(r.get(j,0)-v*u)%p
            if w:r[j]=w
            elif j in r:del r[j]
        if wantcomb:
            for j,u in bc.items():
                w=(c.get(j,0)+v*u)%p
                if w:c[j]=w
                elif j in c:del c[j]
    return r,c
def idx(m):
    v=0
    for i in m:v=8*v+i
    return v
pairs=list(combinations(range(8),2))
def test(p,perm,sign=1):
    rel=relators(sign)
    r2=[{m:v for m,v in r.items() if len(m)==2} for r in rel]
    r3=[{m:v for m,v in r.items() if len(m)==3} for r in rel]
    B={}
    for k,r in enumerate(r2):row_add(B,{idx(m):v for m,v in r.items()},p,{k:1})
    assert len(B)==len(rel)
    W={}
    for r in r2:
        for j in range(8):
            for left in [True,False]:
                row_add(W,{idx((j,)+m if left else m+(j,)):v for m,v in r.items()},p)
    def red3(v):return reduce(W,{idx(m):u for m,u in v.items()},p)[0]
    equations={};count=0;inconsistent=False
    for rr,base3 in zip(r2,r3):
        rp={idx(tuple(perm[i] for i in m)):v for m,v in rr.items()}
        remain,alpha=reduce(B,rp,p,True)
        assert not remain,('r2_not_preserved',perm)
        const={tuple(perm[i] for i in m):v for m,v in base3.items()}
        for j,c in alpha.items():const=add(const,r3[j],-c)
        columns={224:{j:-v%p for j,v in red3(const).items()}}
        for i in range(8):
            if not any(i in m for m in rr):continue
            for k,(a,b) in enumerate(pairs):
                d=defaultdict(int)
                for (u,v),coef in rr.items():
                    if u==i:
                        d[(a,b,perm[v])]+=coef;d[(b,a,perm[v])]-=coef
                    if v==i:
                        d[(perm[u],a,b)]+=coef;d[(perm[u],b,a)]-=coef
                col=red3(d)
                if col:columns[i*28+k]=col
        rows=defaultdict(dict)
        for col,vv in columns.items():
            for row,c in vv.items():
                if c%p:rows[row][col]=c%p
        for row in rows.values():
            row_add(equations,row,p);count+=1
            if 224 in equations:
                inconsistent=True;break
        if inconsistent:break
    return {'p':p,'permutation':perm,'sign':sign,'relators':len(rel),'r2_rank':len(B),'cubic_ideal_rank':len(W),'equations_processed':count,'augmented_rank':len(equations),'inconsistent':inconsistent}
if __name__=='__main__':
    sigma=[2,3,6,7,0,1,4,5]
    perms=[list(range(8)),[sigma[sigma[i]] for i in range(8)],sigma]
    results=[]
    print('beta',beta,'events',[(str(t),L) for t,L in events],'initial_order',order,flush=True)
    for p in [5,3,2,7]:
        for perm in perms:
            for twist_sign in [1,-1]:
                r=test(p,perm,twist_sign);results.append(r);print(r,flush=True)
    Path(__file__).with_name('class3_results.json').write_text(json.dumps(results,indent=2)+'\n')
