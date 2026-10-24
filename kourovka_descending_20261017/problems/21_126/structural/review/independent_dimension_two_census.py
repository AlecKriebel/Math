#!/usr/bin/env python3
"""Forward grammar census with all triangle-free graphs as seeds.
Reuses only this reviewer's prior independent graph encoding/orbit code.
It never imports either author census module.
"""
from itertools import combinations
from pathlib import Path
import json
from independent_graph_census import pairs, edge_set, encode, multipartite3, relabel, orbit_summary


def triangle_free(n,edges):
    return not any({(a,b),(a,c),(b,c)} <= edges
                   for a,b,c in combinations(range(n),3))


def generate(max_n):
    accepted=[]
    for n in range(max_n+1):
        current={mask for mask in range(1 << (n*(n-1)//2))
                 if triangle_free(n,edge_set(n,mask)) or multipartite3(n,edge_set(n,mask))}
        for k in range(1,n):
            for left in combinations(range(n),k):
                right=tuple(v for v in range(n) if v not in left)
                for a in accepted[k]:
                    ea=relabel(k,a,left)
                    for b in accepted[n-k]:
                        current.add(encode(n,ea | relabel(n-k,b,right)))
        if n:
            for vertex in range(n):
                other=tuple(v for v in range(n) if v!=vertex)
                star={tuple(sorted((vertex,v))) for v in other}
                for mask in accepted[n-1]:
                    current.add(encode(n,star | relabel(n-1,mask,other)))
        accepted.append(current)
    return accepted


def main():
    accepted=generate(6)
    result={'method':'forward triangle-free/multipartite grammar generation; adjacent-transposition orbits',
            'labelled_counts':[],'isomorphism_counts':[]}
    for n,current in enumerate(accepted):
        result['labelled_counts'].append({'vertices':n,'inside':len(current),
                                         'outside':(1 << (n*(n-1)//2))-len(current)})
        if n<=5:
            result['isomorphism_counts'].append(orbit_summary(n,current))
    author=json.loads(Path(__file__).parents[1].joinpath('dimension_two_census.json').read_text())
    assert result['labelled_counts']==author['labelled_counts']
    assert result['isomorphism_counts']==author['isomorphism_counts']
    assert all(len(accepted[n]) == 1 << (n*(n-1)//2) for n in range(5))
    expected=[]
    for mask in result['isomorphism_counts'][5]['outside_canonical_masks']:
        expected.append({'mask':mask,'edges':[list(e) for e in sorted(edge_set(5,mask))]})
    assert expected==author['outside_5vertex_graphs']
    result['outside_5vertex_graphs']=expected
    result['comparison']='PASS: all expanded counts, canonical masks and edge lists reproduced'
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
