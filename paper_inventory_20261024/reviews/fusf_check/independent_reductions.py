from fractions import Fraction as F
from itertools import combinations
import json

def parent(w):return w+(0,) if all(a==0 for a in w) else w[:-1]
def neighbors(w):return [(0,),(1,),(2,)] if not w else [w[:-1],w+(0,),w+(1,)]
def descendants(w,depth):
    seen={w};front=[w]
    for _ in range(depth):
        nxt=[]
        for u in front:
            for v in neighbors(u):
                if v!=parent(u):seen.add(v);nxt.append(v)
        front=nxt
    return seen

def network(vertices,remove=frozenset()):
    conduct={}
    for u in vertices:
        for v in (parent(u),parent(parent(u))):
            if v in vertices:
                e=frozenset((u,v))
                if e not in remove:conduct[e]=F(1)
    return conduct

def reduce(vertices,conduct,keep):
    conduct=conduct.copy()
    for u in sorted(vertices-set(keep),key=lambda w:(-len(w),w)):
        incident=[(next(iter(e-{u})),c) for e,c in conduct.items() if u in e]
        total=sum(c for v,c in incident)
        for (v,a),(w,b) in combinations(incident,2):
            e=frozenset((v,w));conduct[e]=conduct.get(e,F(0))+a*b/total
        for v,c in incident:del conduct[frozenset((u,v))]
    return conduct
out={'branch_checks':[],'induced_checks':[]}
a=();b=parent(a);c=parent(b)
for m in range(5):
    interior=descendants(a,m)
    verts=interior|{b,c}
    reduced=reduce(verts,network(verts, {frozenset((b,c))}),{b,c})
    k=reduced[frozenset((b,c))]
    expected=F(1,2)
    for _ in range(m):expected=(1+2*expected)/(2+2*expected)
    assert k==expected
    out['branch_checks'].append({'m':m,'vertices':len(verts),'k':str(k)})
for n in [2,3]:
    verts=descendants((0,)*n,2*n)
    reduced=reduce(verts,network(verts),{a,b,c})
    A=reduced[frozenset((a,b))];B=reduced[frozenset((b,c))];C=reduced[frozenset((a,c))]
    rt=1/(A+B*C/(B+C));rg=1/(C+A*B/(A+B))
    expected={2:(F(7,3),F(17,10),F(1)),3:(F(12,5),F(6236,2669),F(1))}[n]
    assert (A,B,C)==expected
    out['induced_checks'].append({'n':n,'vertices':len(verts),'triangle':[str(x) for x in (A,B,C)],'Rtree':str(rt),'Rgrandparent':str(rg)})
out['status']='PASS_INDEPENDENT_EXACT_REDUCTIONS'
out['scope']='New tuple-word network construction and exact Schur/star-mesh elimination; finite checks supplement written recurrence and contraction review.'
print(json.dumps(out,indent=2))
