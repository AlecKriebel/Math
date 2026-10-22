#!/usr/bin/env python3
"""Verify the 24 obstruction rows using exact tangent-cone linear algebra.
This checker does not import the face-diagram generator.
"""
import itertools,json,sys
from fractions import Fraction as F
from pathlib import Path

def inv(p):return tuple(p.index(i)+1 for i in range(1,len(p)+1))
def comp(p,q):return tuple(p[i-1] for i in q)
def lng(p):return sum(x>y for i,x in enumerate(p) for y in p[i+1:])
def rows(p):return [tuple(i for i in range(1,len(p)+1) if p[i-1]>r) for r in range(len(p))]
def solve(a,b):
    m=[list(map(F,r))+[F(s)] for r,s in zip(a,b)];n=len(a)
    for j in range(n):
        k=next(k for k in range(j,n) if m[k][j]);m[j],m[k]=m[k],m[j]
        z=m[j][j];m[j]=[v/z for v in m[j]]
        for k in range(n):
            if k!=j:
                z=m[k][j];m[k]=[v-z*u for v,u in zip(m[k],m[j])]
    return [m[j][-1] for j in range(n)]
def active(p):
    n=len(p);coord=[(r,k) for r in range(1,n) for k in range(n-r)];rr=rows(p);ret=[]
    for r,k in coord:
        for j,sign in [(k,1),(k+1,-1)]:
            if rr[r][k]!=rr[r-1][j]:continue
            a=[0]*len(coord);a[coord.index((r,k))]=sign
            if r>1:a[coord.index((r-1,j))]-=sign
            ret.append((((r,k),(r-1,j)),a))
    assert len(ret)==len(coord)
    mat=[a for _,a in ret];roots=[]
    for t in range(len(coord)):
        d=solve(mat,[int(j==t) for j in range(len(coord))])
        weight=[sum(d[k] for k,c in enumerate(coord) if c[0]==r) for r in range(1,n)]
        nz=[i for i,x in enumerate(weight) if x]
        assert nz==list(range(min(nz),max(nz)+1))
        assert all(weight[i]==weight[nz[0]] for i in nz)
        sign=weight[nz[0]];assert sign in (-1,1)
        aa,bb=min(nz)+1,max(nz)+2
        roots.append((aa,bb) if sign==1 else (bb,aa))
    return [(eq,root) for (eq,_),root in zip(ret,roots)]
def check(cert):
    w=(2,4,1,3);n=4;perms=set(itertools.permutations(range(1,5)))
    assert {tuple(x['b']) for x in cert}==perms and len(cert)==24
    checks=0
    for z in cert:
        b=tuple(z['b']);s=tuple(z['sigma']);u=tuple(z['predecessor']);t=tuple(z['sigma_predecessor'])
        eq=tuple(map(tuple,z['equality']))
        assert s==comp(b,w) and t==comp(b,u)
        diff=[i for i in range(n) if u[i]!=w[i]]
        assert len(diff)==2 and sorted(u[i] for i in diff)==sorted(w[i] for i in diff)
        assert lng(u)==lng(w)-1
        bi=inv(b);retained={e for e,(i,j) in active(s) if bi[i-1]>bi[j-1]}
        assert eq in retained
        v=rows(t);(r,k),(q,l)=eq
        assert v[r][k]!=v[q][l]
        assert [v[r][k],v[q][l]]==z['top_labels_at_predecessor']
        checks+=1
    # Fixed-flag rank conditions for the claimed smooth incidence variety.
    def bruhat(u,w):
        return all(sum(a<=q for a in u[:p])>=sum(a<=q for a in w[:p]) for p in range(1,5) for q in range(1,5))
    interval={u for u in perms if bruhat(u,w)}
    incidence={u for u in perms if u[0]<=2 and {1,2}<=set(u[:3])}
    assert interval==incidence and len(interval)==8
    assert w not in ((3,4,1,2),(4,2,3,1))
    return {'certificate_rows_verified':checks,'borels_covered':len(perms),'all_predecessor_vertices_outside':True,'length':lng(w),'rank_condition_fixed_flags':len(interval),'arithmetic':'exact fractions and integers'}
if __name__=='__main__':
    c=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('certificate.json')
    print(json.dumps(check(json.loads(c.read_text())),sort_keys=True,indent=2))
