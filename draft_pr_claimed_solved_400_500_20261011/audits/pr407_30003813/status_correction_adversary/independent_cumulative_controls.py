#!/usr/bin/env python3
"""Independent cumulative-coordinate alcove checks; imports no candidate/audit code."""
import collections,hashlib,itertools,json,math,sys
from fractions import Fraction

def require(ok,label):
    if not ok: raise RuntimeError(label)

def determinant(matrix):
    a=[[Fraction(x) for x in r] for r in matrix];v=Fraction(1)
    for k in range(len(a)):
        row=next((j for j in range(k,len(a)) if a[j][k]),None)
        if row is None:return 0
        if row!=k:a[k],a[row]=a[row],a[k];v=-v
        p=a[k][k];v*=p
        for j in range(k+1,len(a)):
            q=a[j][k]/p
            for i in range(k+1,len(a)):a[j][i]-=q*a[k][i]
    return v

def cube_count(n,sign,m):
    dp=[1]*(m+1)
    for s in sign:
        dp=[sum(dp[b] for b in range(m+1) if (a+b>=m if s else a+b<=m)) for a in range(m+1)]
    return sum(dp)

def main():
    counters=collections.Counter();digest=hashlib.sha256()
    for n in range(1,8):
        cells=collections.defaultdict(list)
        for ranks in itertools.permutations(range(1,n+1)):
            # y_0=0. Integer height increases precisely at a fractional descent.
            ranks=(0,)+ranks;k=[0]
            for j in range(1,n+1):k.append(k[-1]+int(ranks[j]<ranks[j-1]))
            mid=[Fraction(k[j])+Fraction(ranks[j],n+1) for j in range(n+1)]
            x=[mid[j]-mid[j-1] for j in range(1,n+1)]
            require(all(0<a<1 for a in x),'strict cube')
            sign=tuple(int(x[i]+x[i+1]>1) for i in range(n-1))
            require(all(x[i]+x[i+1]!=1 for i in range(n-1)),'interior signed chamber')
            order=sorted(range(1,n+1),key=lambda j:ranks[j])
            verts=[]
            for cut in range(n+1):
                one=set(order[cut:]);verts.append(tuple(k[j]+int(j in one) for j in range(1,n+1)))
            verts=tuple(sorted(verts));base=verts[0]
            matrix=[[verts[j+1][i]-base[i] for j in range(n)] for i in range(n)]
            require(abs(determinant(matrix))==1,'unit cumulative lattice determinant')
            for y in verts:
                y=(0,)+y;z=[y[j]-y[j-1] for j in range(1,n+1)]
                require(all(0<=a<=1 for a in z),'closed vertex cube')
                require(all((z[i]+z[i+1]>=1 if s else z[i]+z[i+1]<=1) for i,s in enumerate(sign)),'closed signed vertex')
            cells[sign].append(verts);counters['alcoves']+=1
        require(len(cells)==2**(n-1),'all sign words represented')
        for sign,vs in sorted(cells.items()):
            counts=[cube_count(n,sign,m) for m in range(n+2)]
            h=[sum((-1)**j*math.comb(n+1,j)*counts[i-j] for j in range(i+1)) for i in range(n+2)]
            require(h[-1]==0,'finite h-star degree')
            facets=collections.defaultdict(list)
            for j,v in enumerate(vs):
                for omitted in range(n+1):facets[v[:omitted]+v[omitted+1:]].append(j)
            graph=[set() for _ in vs]
            for shared in facets.values():
                require(len(shared)<=2,'facet incidence')
                if len(shared)==2:
                    a,b=shared;graph[a].add(b);graph[b].add(a)
            for root in sorted(set([0,len(vs)//2,len(vs)-1])):
                dist={root:0};todo=collections.deque([root])
                while todo:
                    a=todo.popleft()
                    for b in graph[a]:
                        if b not in dist:dist[b]=dist[a]+1;todo.append(b)
                require(len(dist)==len(vs),'connected finite graph')
                indeg=[0]*(n+2)
                for a,neighbours in enumerate(graph):
                    require(all(abs(dist[a]-dist[b])==1 for b in neighbours),'bipartite edge direction')
                    indeg[sum(dist[b]<dist[a] for b in neighbours)]+=1
                require(indeg==h,'root-independent graph numerator vs original coordinates')
                counters['root_choices']+=1
            counters['sign_words']+=1;counters['direct_ehrhart_evaluations']+=len(counts)
            digest.update(json.dumps([n,sign,counts,h],separators=(',',':')).encode())
    # Unrestricted rational-simplex claim is false even for this integral interval.
    require([2*m+1 for m in range(3)]==[1,3,5],'interval counterexample')
    require([1,3-2,5-2*3+1]==[1,1,0],'interval numerator 1+z, not 1')
    out={'result':'PASS','independent_mechanism':'fractional cumulative chambers, determinant-one cells, facet graph/BFS vs original signed-coordinate DP','max_dimension':7,'counts':dict(counters),'semantic_sha256':digest.hexdigest(),'rational_simplex_negative_control':'[0,2] has Ehrhart numerator 1+z; denominators alone wrongly predict 1','scope':'Finite controls, not a substitute for the all-dimensional reduction and prior theorem; no candidate imports or native writes.'}
    json.dump(out,sys.stdout,indent=2);print()
if __name__=='__main__':main()
