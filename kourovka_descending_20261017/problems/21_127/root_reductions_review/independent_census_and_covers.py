#!/usr/bin/env python3
"""Independent partition-existence membership and adjacent-transposition orbits.
Does not compute complement connected components or canonize via all permutations.
"""
from itertools import combinations
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

def partitions(items):
    if not items:yield ();return
    first,*rest=items
    for p in partitions(rest):
        yield ((first,),)+p
        for i in range(len(p)):
            yield p[:i]+((first,)+p[i],)+p[i+1:]

def eligible(n,edges):
    for blocks in partitions(list(range(n))):
        labels={v:k for k,block in enumerate(blocks) for v in block}
        if any(labels[i]!=labels[j] and (i,j) not in edges for i,j in combinations(range(n),2)):continue
        # A block is a cluster iff no triple spans exactly two edges.
        if any(sum(tuple(sorted((i,j))) in edges for i,j in combinations(triple,2))==2
               for block in blocks for triple in combinations(block,3)):continue
        return True
    return False

def main():
    folder=Path(__file__).resolve().parent;auth=folder.parent/'root_reductions'
    expected=json.loads((auth/'graph_subclass.json').read_text())['rows'];rows=[]
    for n in range(1,6):
        pairs=list(combinations(range(n),2));positions={e:k for k,e in enumerate(pairs)}
        swapmaps=[]
        for k in range(n-1):
            def perm(v):return k+1 if v==k else k if v==k+1 else v
            swapmaps.append([positions[tuple(sorted((perm(i),perm(j))))] for i,j in pairs])
        masks=range(1<<len(pairs));values={}
        def edge_set(mask):return {e for i,e in enumerate(pairs) if mask>>i&1}
        for mask in masks:values[mask]=eligible(n,edge_set(mask))
        done=set();orbits=[]
        for mask in masks:
            if mask in done:continue
            orbit={mask};frontier=[mask]
            while frontier:
                a=frontier.pop()
                for mapping in swapmaps:
                    b=sum((1<<mapping[i]) for i in range(len(pairs)) if a>>i&1)
                    if b not in orbit:orbit.add(b);frontier.append(b)
            done.update(orbit)
            assert len({values[x] for x in orbit})==1
            orbits.append((mask,len(orbit),values[mask]))
        row={'vertices':n,'labelled_total':len(values),'labelled_inside':sum(values.values()),'isomorphism_classes':len(orbits),'classes_inside':sum(v for _,_,v in orbits)}
        exp=expected[n-1]
        assert all(row[key]==exp[key] for key in row)
        if n==4:
            bad=[edge_set(mask) for mask,_,v in orbits if not v]
            signatures=sorted(tuple(sorted(sum(v in e for e in edges) for v in range(n))) for edges in bad)
            assert signatures==[(0,1,1,2),(1,1,2,2)]
            row['outside_degree_signatures']=signatures
        rows.append(row)
    covers=[]
    for N in range(1,256,2):
        sigma=[(x+1)%N for x in range(N)];tau=[2*x%N for x in range(N)]
        assert len(set(tau))==N
        si=[0]*N;ti=[0]*N
        for x,y in enumerate(sigma):si[y]=x
        for x,y in enumerate(tau):ti[y]=x
        comm=[sigma[tau[si[ti[x]]]] for x in range(N)]
        assert comm==[(x-1)%N for x in range(N)]
        seen=set();x=0
        while x not in seen:seen.add(x);x=comm[x]
        assert len(seen)==N and x==0
        for k in range(1,9):
            chi=N*(1-2*k);genus=(1-chi)//2
            assert 1-2*genus==chi
            assert genus==N*k-(N-1)//2
            if k==1:assert genus==N//2+1
        covers.append({'odd_degree':N,'single_boundary_cycle':True,'genus_k1':N//2+1})
    result={'utc':datetime.now(timezone.utc).isoformat(),'method':'All set partitions as join decomposition candidates; no induced P3 in each factor; graph isomorphism orbits via adjacent swaps; exact odd permutation covers','graph_rows':rows,'cover_degrees_checked':len(covers),'max_odd_cover_degree':255,'handle_genera_checked':list(range(1,9)),'status':'PASS','inputs_sha256':{name:hashlib.sha256((auth/name).read_bytes()).hexdigest() for name in ['FINITE_SUPPORT_AND_JOINS.md','COMMUTATOR_TEST_FAMILY.md','graph_subclass.py','graph_subclass.json']}}
    (folder/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
