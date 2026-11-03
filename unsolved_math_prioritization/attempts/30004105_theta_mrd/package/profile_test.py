"""Exact invariant dimensions; coefficients lie in the prime field F_3."""
import json, math
P=3; N=7

def rref(rows):
    a=[list(r) for r in rows]; piv=[]; k=0
    for j in range(N):
        pivot=next((i for i in range(k,len(a)) if a[i][j]%P),None)
        if pivot is None: continue
        a[k],a[pivot]=a[pivot],a[k]
        inv=pow(a[k][j],-1,P); a[k]=[(v*inv)%P for v in a[k]]
        for i in range(len(a)):
            if i!=k:
                v=a[i][j];a[i]=[(x-v*y)%P for x,y in zip(a[i],a[k])]
        piv.append(j);k+=1
    return a[:k],piv

def perp(rows):
    a,piv=rref(rows); out=[]
    for j in range(N):
        if j not in piv:
            v=[0]*N;v[j]=1
            for row,k in zip(a,piv):v[k]=-row[j]%P
            out.append(v)
    return out

def shift(row,s): return [row[(j-s)%N] for j in range(N)]
def e(j):return [int(i==j) for i in range(N)]
C=[e(0),e(1),e(3)]
H=[[int(i in (0,3)) for i in range(N)],e(1),e(2)]
out={}
for name,G in [('monomial_013',C),('twisted_eta1',H)]:
    out[name]={}
    for s in range(1,7):
        sums=[];intersections=[]; rows=[];dual=[]
        for i in range(8):
            rows += [shift(r,i*s) for r in G]
            dual += [shift(r,i*s) for r in perp(G)]
            sums.append(len(rref(rows)[0]));intersections.append(N-len(rref(dual)[0]))
        out[name][str(s)]={'sums':sums,'intersections':intersections}
print(json.dumps(out,indent=2))
