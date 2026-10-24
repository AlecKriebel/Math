#!/usr/bin/env python3
"""Independent exhaustive reconciliation of the at-most-five-vertex reduction.
Uses only prior independent review modules, never author census implementations.
"""
from pathlib import Path
import json
from independent_dimension_two_census import generate
from independent_graph_census import orbit, edge_set

ORDERS={59:[4,3,2,0,1],185:[4,0,2,1,3],187:[4,0,1,2,3]}


def peo(mask,order):
    edges=edge_set(5,mask)
    remaining=set(range(5))
    checks=[]
    for v in order:
        neighbors=sorted(w for w in remaining-{v} if tuple(sorted((v,w))) in edges)
        clique=all(tuple(sorted((a,b))) in edges
                   for a in neighbors for b in neighbors if a!=b)
        assert clique
        checks.append({'vertex':v,'remaining_neighbors':neighbors,'clique':clique})
        remaining.remove(v)
    assert not remaining
    return checks


def main():
    accepted=generate(5)
    certificate={'scope':'all labelled finite graphs on at most five vertices; no larger graphs',
                 'perfect_elimination_checks':{str(mask):peo(mask,order) for mask,order in ORDERS.items()},
                 'classes':[]}
    house={(0,1),(1,2),(2,3),(0,3),(0,4),(1,4)}
    assert edge_set(5,221)==house
    cycle={(0,1),(1,2),(2,3),(0,3)}
    triangle={(0,1),(0,4),(1,4)}
    assert house==cycle|triangle and cycle&triangle=={(0,1)}
    cross={(a,b) for a in (0,1) for b in (2,3,4)}
    assert edge_set(5,254)==cross|{(2,3)}
    remaining=set(range(1 << 10))
    counts={}
    while remaining:
        base=min(remaining)
        current=orbit(5,base)
        assert current <= remaining
        remaining-=current
        if current <= accepted[5]:
            route,degree='expanded triangle-free / three-free-factor closure',9
        else:
            assert not current & accepted[5]
            if base in ORDERS:
                route,degree='chordal coherent RAAG prior CAT(0) theorem',2
            elif base==221:
                route,degree='house clique-amalgam polynomial filling lemma',5
            elif base==254:
                route,degree='two-limit-group product prior theorem',18
            else:
                raise AssertionError(('unaccounted class',base))
        counts[str(degree)]=counts.get(str(degree),0)+len(current)
        certificate['classes'].append({'canonical_mask':base,'labelled_orbit_size':len(current),
                                       'route':route,'polynomial_upper_degree':degree})
    assert len(certificate['classes'])==34
    assert sum(counts.values())==1024
    assert counts['9']==754
    assert all(len(accepted[n]) == 1 << (n*(n-1)//2) for n in range(5))
    certificate['labelled_graphs_at5_by_degree_upper_bound']=counts
    certificate['all_isomorphism_classes_at5']=len(certificate['classes'])
    certificate['all_at_most4_in_expanded_class']=True
    certificate['maximum_degree_upper_bound']=18
    certificate['comparison']='PASS: exhaustive classification leaves no five-vertex isomorphism class uncovered'
    Path(__file__).with_suffix('.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({k:v for k,v in certificate.items() if k!='classes'},indent=2))


if __name__=='__main__':
    main()
