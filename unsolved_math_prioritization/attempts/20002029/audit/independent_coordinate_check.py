"""Independent reviewer computation from coordinate metrics, not author K/frame formulas."""
from itertools import product
from functools import lru_cache
from pathlib import Path
import json
import sympy as s
r=s.symbols('r',positive=True)
Q=s.Rational

def metric_check(p):
    n=len(p)+1; ids=range(n)
    g=[s.Integer(1)]+[r**(2*x) for x in p]
    gi=[1/x for x in g]
    def d(f,a): return s.diff(f,r) if a==0 else s.S.Zero
    @lru_cache(None)
    def G(u,a,b):
        return s.expand(gi[u]*(d(g[u],a)*int(u==b)+d(g[u],b)*int(u==a)-d(g[a],u)*int(a==b))/2)
    @lru_cache(None)
    def R(a,b,c,dd):
        return s.expand(-g[dd]*(d(G(dd,b,c),a)-d(G(dd,a,c),b)+sum(G(dd,a,u)*G(u,b,c)-G(dd,b,u)*G(u,a,c) for u in ids)))
    ric=[[s.simplify(sum(gi[a]*R(a,b,a,dd) for a in ids)) for dd in ids] for b in ids]
    assert all(v==0 for row in ric for v in row)
    raw={(a,b,c,dd):R(a,b,c,dd) for a,b,c,dd in product(ids,repeat=4)}
    raw={k:v for k,v in raw.items() if v}
    R1={k:v.subs(r,1) for k,v in raw.items()}
    def at1(k):return R1.get(k,0)
    A=B=s.S.Zero
    for a,b,c,dd,e,f in product(ids,repeat=6):
        v=at1((a,b,c,dd))
        if v:
            A+=v*at1((c,dd,e,f))*at1((e,f,a,b))
            B+=v*at1((a,e,c,f))*at1((b,e,dd,f))
    D=s.S.Zero
    for m in ids:
        for ind in product(ids,repeat=4):
            val=d(R(*ind),m)
            for j in range(4):
                for u in ids:
                    gamma=G(u,m,ind[j])
                    if gamma:
                        other=list(ind);other[j]=u
                        val-=gamma*R(*other)
            D+=s.expand(val).subs(r,1)**2
    # Raw coordinate tensor contractions, including all metric factors.
    M={}
    for c,dd in product(ids,repeat=2):
        M[c,dd]=s.expand(sum(raw.get((c,e,f,h),0)*raw.get((dd,e,f,h),0)*gi[e]*gi[f]*gi[h] for e,f,h in product(ids,repeat=3)))
    T1={};T2={}
    for a,b in product(ids,repeat=2):
        T1[a,b]=s.expand(sum(raw.get((a,c,b,dd),0)*M[c,dd]*gi[c]*gi[dd] for c,dd in product(ids,repeat=2)))
        t=s.S.Zero
        for c,dd,e in product(ids,repeat=3):
            v=raw.get((a,c,dd,e),0)
            if v:
                t+=v*gi[c]*gi[dd]*gi[e]*sum(raw.get((b,c,f,h),0)*raw.get((dd,e,f,h),0)*gi[f]*gi[h] for f,h in product(ids,repeat=2))
        T2[a,b]=s.expand(t)
    def div2(T):
        q={a:s.expand(sum(gi[b]*(d(T[a,b],b)-sum(G(u,b,a)*T[u,b]+G(u,b,b)*T[a,u] for u in ids)) for b in ids)) for a in ids}
        return s.simplify(sum(gi[a]*(d(q[a],a)-sum(G(u,a,a)*q[u] for u in ids)) for a in ids))
    trace=s.expand(sum(gi[a]*T2[a,a] for a in ids))
    assert trace.subs(r,1)==A
    lap=s.expand(sum(gi[a]*(d(d(trace,a),a)-sum(G(u,a,a)*d(trace,u) for u in ids)) for a in ids))
    U1=div2(T1).subs(r,1);U2=(div2(T2)-lap/6).subs(r,1)
    out={'n':n,'p':list(map(str,p)),'ricci_zero':True,'D':str(D),'A':str(A),'B':str(B),'U1':str(U1),'U2':str(U2)}
    print(json.dumps(out),flush=True)
    return out
ps=[(Q(-1,3),Q(2,3),Q(2,3),0,0),(Q(-1,2),Q(1,2),Q(1,2),Q(1,2),0),(Q(-3,5),Q(2,5),Q(2,5),Q(2,5),Q(2,5))]
res=[metric_check(p) for p in ps]
# Products with flat factors change no contractions or divergences; verify n=8 directly too.
res += [metric_check(p+(0,0)) for p in ps[:2]]
det6=s.det(s.Matrix([[s.sympify(x[k]) for k in ('D','A','B')] for x in res[:3]]))
det8=s.det(s.Matrix([[s.sympify(x[k]) for k in ('U1','U2')] for x in res[3:]]))
assert det6==-Q(65536,3125)
assert det8==-Q(448,9)
output={'coordinate_checks':res,'determinant_6':str(det6),'determinant_8':str(det8),'passed':True}
Path(__file__).with_suffix('.result.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
