#!/usr/bin/env python3
"""Independent exact source-forward polynomial/reference controls; no validator import."""
import json, hashlib, datetime

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
Z=(0,0); ONE=(1,0); I=(0,1)
def padd(a,b):
    n=max(len(a),len(b)); return [add(a[j] if j<len(a) else Z,b[j] if j<len(b) else Z) for j in range(n)]
def pmul(a,b):
    v=[Z]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b): v[j+k]=add(v[j+k],mul(x,y))
    return v

def direct_product(n,reverse=False):
    a=[[ [ONE], [Z] ],[ [Z], [ONE] ]]
    for t in (range(n-1,-1,-1) if reverse else range(n)):
        z=[Z]*(2**t)+[ONE]
        b=[[[ONE],[I]],[z,[(0,0)]*(2**t)+[(-1,0)]]]
        a=[[padd(pmul(a[r][0],b[0][c]),pmul(a[r][1],b[1][c])) for c in range(2)] for r in range(2)]
    return a

def norm_coefficients(a):
    d=max(len(p) for row in a for p in row)-1
    ans={k:Z for k in range(-d,d+1)}
    for row in a:
        for p in row:
            for j,x in enumerate(p):
                for l,y in enumerate(p): ans[j-l]=add(ans[j-l],mul(x,conj(y)))
    return ans

def evaluate(a,z):
    return [[sum((complex(*v)*complex(*z)**j for j,v in enumerate(p)),0j) for p in row] for row in a]

def main():
    rows=[]
    for n in range(7):
        a=direct_product(n); c=norm_coefficients(a)
        units=sum(x!=Z for row in a for p in row for x in p)
        ok_units=all(x==Z or x[0]**2+x[1]**2==1 for row in a for p in row for x in p)
        hermitian=all(c[-k]==conj(c[k]) for k in c)
        if c[0]!=(2**(n+1),0) or not ok_units or not hermitian:
            raise RuntimeError('independent algebra identity failed')
        rows.append({'n':n,'nonzero_units':units,'C0':c[0],'degree':max(c),'hermitian':hermitian,'coefficient_sha256':hashlib.sha256(json.dumps(sorted(c.items())).encode()).hexdigest()})
    f=norm_coefficients(direct_product(2)); r=norm_coefficients(direct_product(2,True))
    if f==r: raise RuntimeError('reversal sensitivity control failed')
    print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_order':'B(x)...B(2**(N-1)*x)','checks':rows,'N2_source_forward_C':sorted(f.items()),'N2_reverse_C':sorted(r.items()),'reversal_is_pointwise_sensitive':True},indent=2))
if __name__=='__main__': main()
