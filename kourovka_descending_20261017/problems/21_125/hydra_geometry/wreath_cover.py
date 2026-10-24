#!/usr/bin/env python3
"""Construct exact regular wreath-product covers; inspect actual specialness defects."""
from cover_search import alpha_perms,hyperplanes,inv,mul
from itertools import combinations
from pathlib import Path
import json

def wreath_action(k, modulus=2):
    # Base C_modulus^k, cyclic top C_k; enumerate all group elements.
    from itertools import product
    elements=[(v,r) for v in product(range(modulus),repeat=k) for r in range(k)]
    index={x:i for i,x in enumerate(elements)}
    def product_(x,y):
        v,r=x;w,t=y
        return (tuple((v[j]+w[(j-r)%k])%modulus for j in range(k)),(r+t)%k)
    s=((1,)+(0,)*(k-1),0);top=((0,)*k,1)
    return tuple(index[product_(x,s)] for x in elements),tuple(index[product_(x,top)] for x in elements),elements

def defects(arr):
    roots,cross=hyperplanes(arr);n=len(arr[0]);m=len(arr)-1
    inverses=[inv(p) for p in arr]
    # A germ (label,sign) based at v; hyperplane ID for underlying positive edge.
    def h(v,g):
        x,sign=g
        return roots[x*n+(v if sign==1 else inverses[x][v])]
    corners=[set() for _ in range(n)]
    # Each lift of s A_i A_prev^-1 A_i^-1.
    for i in range(1,m+1):
        prev=0 if i==1 else i-1
        for v in range(n):
            path=[(0,1),(i,1),(prev,-1),(i,-1)];at=v;states=[]
            for x,sgn in path:
                states.append((at,(x,sgn)))
                at=(arr[x] if sgn==1 else inverses[x])[at]
            assert at==v
            for j in range(4):
                corner_v,outgoing=states[j];previous=path[(j-1)%4]
                incoming=(previous[0],-previous[1])
                corners[corner_v].add(tuple(sorted((incoming,outgoing))))
    crossing_pairs=set()
    for v in range(n):
        for g1,g2 in corners[v]:crossing_pairs.add(tuple(sorted((h(v,g1),h(v,g2)))))
    direct=[];indirect=[];inter=[]
    germs=[(x,sgn) for x in range(m+1) for sgn in (-1,1)]
    for v in range(n):
        for g1,g2 in combinations(germs,2):
            if tuple(sorted((g1,g2))) in corners[v]:continue
            a,b=h(v,g1),h(v,g2)
            if a==b:
                (direct if g1[1]==g2[1] else indirect).append([v,list(g1),list(g2),a])
            elif tuple(sorted((a,b))) in crossing_pairs:
                inter.append([v,list(g1),list(g2),a,b])
    return {'degree':n,'rank':m,'hyperplanes':len(set(roots)),'self_crossing_square_count':len(cross),'direct_self_osculation_count':len(direct),'indirect_self_osculation_count':len(indirect),'inter_osculation_count':len(inter),'first_direct_self_osculations':direct[:10],'first_inter_osculations':inter[:10],'two_sided':'yes: every square identifies opposite positive orientations','A_special':not(cross or direct or inter)}

if __name__=='__main__':
    rows=[]
    for k,modulus in [(3,2),(4,2),(3,3)]:
        s,t,elts=wreath_action(k,modulus)
        for rank in (2,3,4,5):
            arr=alpha_perms(s,t,rank);assert arr
            r=defects(arr);r['wreath_top_order']=k;r['wreath_base_modulus']=modulus;rows.append(r)
            print(k,modulus,rank,r['degree'],r['self_crossing_square_count'],r['direct_self_osculation_count'],r['inter_osculation_count'])
    Path(__file__).with_name('wreath_cover_results.json').write_text(json.dumps({'rows':rows,'scope':'finite explicit canonical cube covers; A-special tests follow Haglund-Wise 2007 corrected Thm1.1'},indent=2)+'\n')
