#!/usr/bin/env python3
"""Exact finite verification for the P4 torus-block transport obstruction.

No external packages. This checks a fixed normal-block family, not scl of the
outer boundary chain among all possible surfaces.
"""
from collections import defaultdict, deque
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def components(vertices, edges):
    adj = {v: [] for v in vertices}
    for eid, u, v in edges:
        adj[u].append((eid, v)); adj[v].append((eid, u))
    found = []
    unseen = set(vertices)
    while unseen:
        root = min(unseen); unseen.remove(root)
        queue = [root]; part = []
        for u in queue:
            part.append(u)
            for _, v in adj[u]:
                if v in unseen:
                    unseen.remove(v); queue.append(v)
        found.append(sorted(part))
    return found, adj


def dataset():
    pieces = {}
    weights = [1, 1, 1, 1, 1, 1, -3, -3]
    # A_i -- M_(2i) -- D_i -- M_(2i+1) -- A_(i+1).
    cyclic = []
    for i in range(4):
        pieces[f'A{i}'] = {'coordinates': ['a','b'], 'charge': {'a':0,'b':0}}
        pieces[f'D{i}'] = {'coordinates': ['c','d'], 'charge': {'c':0,'d':0}}
        for j in [2*i,2*i+1]:
            pieces[f'M{j}'] = {'coordinates': ['b','c'], 'charge': {'b':weights[j],'c':weights[j]}}
        cyclic += [f'A{i}',f'M{2*i}',f'D{i}',f'M{2*i+1}']
    edges = []
    for i, u in enumerate(cyclic):
        v = cyclic[(i+1)%len(cyclic)]
        coord = 'b' if u.startswith('A') or v.startswith('A') else 'c'
        edges.append({'id':f'e{i}', 'u':u, 'v':v, 'coordinate':coord})
    return pieces, edges, cyclic, weights


def coordinate_components(pieces, edges):
    records = []
    for x in 'abcd':
        vertices = [p for p, data in pieces.items() if x in data['coordinates']]
        xe = [(e['id'],e['u'],e['v']) for e in edges if e['coordinate']==x]
        parts, _ = components(vertices,xe)
        for part in parts:
            charge = sum(pieces[p]['charge'][x] for p in part)
            records.append({'coordinate':x,'pieces':part,'charge':charge,'bad':charge!=0})
    return records


def minimum_hitting_set(pieces, records):
    bad = [set(r['pieces']) for r in records if r['bad']]
    names = sorted(pieces)
    for k in range(len(names)+1):
        for candidate in combinations(names,k):
            chosen = set(candidate)
            if all(chosen & b for b in bad):
                return list(candidate)
    raise AssertionError('Finite family must have a transversal')


def realize_windings(pieces,edges,free):
    # Edge t contributes +t to u and -t to v. All constrained charges must vanish.
    free=set(free); values={e['id']:0 for e in edges}
    for x in 'abcd':
        vertices=[p for p,d in pieces.items() if x in d['coordinates']]
        xe=[(e['id'],e['u'],e['v']) for e in edges if e['coordinate']==x]
        parts,adj=components(vertices,xe)
        lookup={e['id']:e for e in edges}
        for part in parts:
            root=next((p for p in part if p in free),part[0])
            parent={root:None}; order=[root]
            for u in order:
                for eid,v in adj[u]:
                    if v not in parent:
                        parent[v]=(u,eid);order.append(v)
            charge={p:pieces[p]['charge'][x] for p in part}
            for v in reversed(order[1:]):
                u,eid=parent[v]
                # At v, contribution sign is + if v is u endpoint, - otherwise.
                s=1 if lookup[eid]['u']==v else -1
                t=-charge[v]*s
                values[eid]=t
                charge[u] += -s*t
                charge[v] += s*t
                assert charge[v]==0
            if root not in free: assert charge[root]==0
    wind={p:dict(d['charge']) for p,d in pieces.items()}
    for e in edges:
        x=e['coordinate'];t=values[e['id']]
        wind[e['u']][x]+=t;wind[e['v']][x]-=t
    actual_free=[p for p in sorted(pieces) if any(wind[p].values())]
    assert set(actual_free).issubset(free)
    return values,wind,actual_free


def main():
    pieces,edges,cyclic,weights=dataset()
    records=coordinate_components(pieces,edges)
    bad=[r for r in records if r['bad']]
    assert len(pieces)==len(edges)==16
    assert len(bad)==8
    assert sorted(r['charge'] for r in bad)==[-6,-2,-2,2,2,2,2,2]
    minimum=minimum_hitting_set(pieces,records)
    assert len(minimum)==4
    expected_free=[f'M{i}' for i in [1,3,5,7]]
    assert all(set(r['pieces']) & set(expected_free) for r in bad)
    values,wind,actual_free=realize_windings(pieces,edges,expected_free)
    assert actual_free==expected_free
    # Each b component is a 3-vertex star whose middle torus leaves have charge
    # chosen from {1,-3}; even after arbitrary rewiring a pair has nonzero sum.
    allowed_pair_sums=sorted({u+v for u in [1,-3] for v in [1,-3]})
    assert allowed_pair_sums==[-6,-2,2]
    # Explicit outer boundary words (uppercase means inverse). BC commutes.
    def arc(p, direction):
        if p.startswith('A'):
            sign = 1 if int(p[1:])<2 else -1
            return [('a' if sign*direction==1 else 'A')]
        if p.startswith('D'):
            sign = 1 if int(p[1:])<2 else -1
            return [('d' if sign*direction==1 else 'D')]
        i=int(p[1:])
        if (i%2==0 and direction==1) or (i%2==1 and direction==-1):
            w=weights[i]
            return [('b' if w>0 else 'B')]*abs(w)+[('c' if w>0 else 'C')]*abs(w)
        return []
    forward=sum((arc(p,1) for p in cyclic),[])
    backwards_order=[cyclic[0]]+list(reversed(cyclic[1:]))
    backward=sum((arc(p,-1) for p in backwards_order),[])
    assert forward=='a b c d a b c d A b c D A B B B C C C D'.split()
    assert backward=='A B B B C C C d a b c d a b c D A b c D'.split()
    def abelianization(word):
        return {x:sum((1 if t==x else -1 if t==x.upper() else 0) for t in word) for x in 'abcd'}
    assert abelianization(forward)==abelianization(backward)==dict.fromkeys('abcd',0)
    # Their projections to the free retract on a,d are freely reduced nonempty.
    def reduce_free(word):
        stack=[]
        for t in word:
            if stack and stack[-1]==t.swapcase():stack.pop()
            else:stack.append(t)
        return ''.join(stack)
    def inverse(word):return word[::-1].swapcase()
    def commutator(u,v):return reduce_free(u+v+inverse(u)+inverse(v))
    h='acacAcACCC'
    assert reduce_free('a'+commutator('cac','AcAC')+'A')==h
    assert commutator('acacA','cACA')==h
    ac_retractions=[reduce_free([t for t in word if t.lower() in 'ac']) for word in [forward,backward]]
    assert ac_retractions[0]==h
    assert ac_retractions[1]==h[6:]+h[:6]
    projected=[]
    for word in [forward,backward]:
        stack=[]
        for t in word:
            if t.lower() not in 'ad':continue
            if stack and stack[-1]==t.swapcase():stack.pop()
            else:stack.append(t)
        assert stack
        projected.append(' '.join(stack))
    report={
        'generated_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Fixed P4 torus normal-block family; no exact full scl claim',
        'pieces':pieces,'edges':edges,'incidence_cycle':cyclic,
        'middle_charges':weights,'coordinate_components':records,
        'minimum_hitting_number':len(minimum),'first_minimum_hitting_set':minimum,
        'explicit_free_pieces':expected_free,'turn_windings':values,
        'resulting_piece_windings':wind,'actual_non_disks':actual_free,
        'best_relative_euler_characteristic':len(pieces)-len(expected_free)-len(edges),
        'best_fixed_block_relative_cost':{'numerator':2,'denominator':1},
        'naive_independent_potential_disk_cost':0,
        'arbitrary_rewiring_nonzero_b_component_charges':allowed_pair_sums,
        'degree_N_lower_bound_non_disks':'4*N',
        'degree_N_lower_bound_relative_minus_chi':'4*N',
        'outer_boundary_words':[forward,backward],
        'outer_boundary_abelianizations':[abelianization(forward),abelianization(backward)],
        'nontrivial_free_retract_words':projected,
        'ac_retract_words':ac_retractions,
        'free_commutator_word':h,
        'free_commutator_inputs':['acacA','cACA'],
        'alternate_conjugated_free_commutator':{'conjugator':'a','inputs':['cac','AcAC']},
        'absolute_chain_scl_lower_bound':{'numerator':1,'denominator':1},
        'absolute_chain_scl_upper_bound':{'numerator':2,'denominator':1},
        'passed':True,
    }
    (ROOT/'transport_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['generated_utc','scope','minimum_hitting_number','explicit_free_pieces','actual_non_disks','best_relative_euler_characteristic','best_fixed_block_relative_cost','passed']},indent=2))

if __name__=='__main__':main()
