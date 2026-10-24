#!/usr/bin/env python3
"""Independent exact audit of a fixed-block P4 construction.

Does not import or execute the author's verifier. All comparisons below are
against data independently reconstructed here. Finite checks supplement the
mathematical proofs in AUDIT.md; they do not prove arbitrary RAAG rationality.
"""
import hashlib
import itertools
import json
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'graph_decomposition'


def free_reduce(w):
    answer = []
    for x in w:
        if answer and answer[-1] == x.swapcase():
            answer.pop()
        else:
            answer.append(x)
    return ''.join(answer)


def inv(w):
    return w[::-1].swapcase()


def connected_components(vertices, edges):
    # Deliberately use disjoint-set union, rather than the author's BFS.
    parent = {v: v for v in vertices}
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for u, v in edges:
        parent[find(u)] = find(v)
    answer = {}
    for v in vertices:
        answer.setdefault(find(v), set()).add(v)
    return sorted((sorted(p) for p in answer.values()))


def reproduce():
    frozen = json.loads((AUTHOR / 'FROZEN_MANIFEST.json').read_text())
    delta = json.loads((AUTHOR / 'REVIEW_DELTA_MANIFEST.json').read_text())
    # This exact delta was reviewed as a clarification of compatible endpoints
    # plus its research-log entry. Do not accept arbitrary future author edits.
    accepted_delta = {
        'P4_PROMOTION_OBSTRUCTION.md': {
            'sha256':'d63b5ed01f04dcb1f5b3868d4360da3ff23f619e9353cdcd74a9f3c8f340df49',
            'bytes':8172},
        'RESEARCH_LOG.md': {
            'sha256':'83b98b4952de0e0fb7df2c46baeab83daa4ba44bd944c1b67b21d056170e9a40',
            'bytes':2733},
    }
    assert delta['changed_files']==accepted_delta
    hashes = {}
    for name, expected in frozen['files'].items():
        expected = accepted_delta.get(name,expected)
        data = (AUTHOR / name).read_bytes()
        actual = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        assert actual == expected, (name, actual, expected)
        hashes[name] = actual
    cert = json.loads((AUTHOR / 'transport_certificate.json').read_text())

    # The 16 blocks are vertices of a ribbon cycle. Prefixes name target tori.
    cycle = [x for i in range(4) for x in (f'A{i}', f'M{2*i}', f'D{i}', f'M{2*i+1}')]
    weights = dict(zip((f'M{j}' for j in range(8)), (1,1,1,1,1,1,-3,-3)))
    coords = {v: ('ab' if v[0]=='A' else 'cd' if v[0]=='D' else 'bc') for v in cycle}
    charges = {v: {x: weights[v] if v[0]=='M' else 0 for x in coords[v]} for v in cycle}
    oriented = [(cycle[k],cycle[(k+1)%16]) for k in range(16)]
    edge_x = [next(iter(set(coords[u]) & set(coords[v]))) for u,v in oriented]
    assert edge_x == ['b','c','c','b'] * 4
    assert [e['coordinate'] for e in cert['edges']] == edge_x
    assert [(e['u'],e['v']) for e in cert['edges']] == oriented

    components = []
    for x in 'abcd':
        vertices = [v for v in cycle if x in coords[v]]
        edges = [uv for uv,y in zip(oriented,edge_x) if y==x]
        for part in connected_components(vertices,edges):
            charge = sum(charges[v][x] for v in part)
            components.append({'coordinate':x,'pieces':part,'charge':charge,'bad':charge!=0})
    assert components == cert['coordinate_components']
    bad = [set(c['pieces']) for c in components if c['bad']]
    assert len(bad)==8
    # Audit every one of the 65,536 possible non-disk sets, rather than stopping
    # at the first feasible set as the author's checker does.
    names = sorted(cycle)
    counts = Counter()
    minima = []
    for mask in range(1<<16):
        chosen = {v for j,v in enumerate(names) if mask & (1<<j)}
        if all(chosen.intersection(b) for b in bad):
            counts[len(chosen)] += 1
            if len(chosen)==4:
                minima.append(sorted(chosen))
    assert min(counts)==cert['minimum_hitting_number']==4
    assert cert['first_minimum_hitting_set'] in minima

    # Verify every integer edge current directly; do not reuse flow algorithm.
    final = {v: dict(c) for v,c in charges.items()}
    for k,((u,v),x) in enumerate(zip(oriented,edge_x)):
        t = cert['turn_windings'][f'e{k}']
        assert isinstance(t,int)
        final[u][x] += t
        final[v][x] -= t
    assert final==cert['resulting_piece_windings']
    actual = sorted(v for v,c in final.items() if any(c.values()))
    assert actual==['M1','M3','M5','M7']==cert['actual_non_disks']
    residual = [[final[v]['b'],final[v]['c']] for v in actual]
    assert residual==[[2,2],[2,2],[-2,2],[-2,-6]]
    assert list(map(sum,zip(*residual)))==[0,0]

    # Recover the two exterior faces using ribbon permutations. Each block has
    # an incoming and outgoing port. sigma exchanges its two ports, and alpha
    # pairs outgoing(i) with incoming(i+1). Faces are cycles of alpha*sigma.
    darts = list(itertools.product(range(16),(0,1)))
    sigma = {(i,d):(i,1-d) for i,d in darts}
    alpha = {}
    for i in range(16):
        alpha[(i,1)] = ((i+1)%16,0)
        alpha[((i+1)%16,0)] = (i,1)
    face = {d:alpha[sigma[d]] for d in darts}
    def arc(dart):
        i,side = dart
        v=cycle[i]
        if v[0] in 'AD':
            letter=v[0].lower()
            exponent=(1 if int(v[1:])<2 else -1)*(1 if side==0 else -1)
            return letter if exponent==1 else letter.upper()
        j=int(v[1:])
        if (j%2==0 and side==0) or (j%2==1 and side==1):
            w=weights[v]
            return ('b'*w+'c'*w) if w>0 else ('B'*(-w)+'C'*(-w))
        return ''
    unseen=set(darts)
    faces=[]
    for start in [(0,0),(0,1)]:
        assert start in unseen
        f=[]
        d=start
        while d in unseen:
            unseen.remove(d); f.append(d); d=face[d]
        assert d==start
        faces.append(f)
    assert not unseen and list(map(len,faces))==[16,16]
    words=[''.join(arc(d) for d in f) for f in faces]
    assert words==[''.join(w) for w in cert['outer_boundary_words']]
    abelianizations=[{x:w.count(x)-w.count(x.upper()) for x in 'abcd'} for w in words]
    assert abelianizations==[dict.fromkeys('abcd',0)]*2
    ad=[free_reduce(x for x in w if x.lower() in 'ad') for w in words]
    assert all(ad)
    ac=[free_reduce(x for x in w if x.lower() in 'ac') for w in words]
    h='acacAcACCC'
    u,v='acacA','cACA'
    assert free_reduce(u+v+inv(u)+inv(v))==h
    assert ac==[h,h[6:]+h[:6]]
    assert free_reduce(h)==h and h[0]!=h[-1].swapcase()

    # Underlying ribbon-cycle thickening is an annulus; replace four disks by
    # annuli. This adds four boundary components without adding handles.
    V,E,non_disks=16,16,4
    chi=V-non_disks-E
    B=len(faces)+non_disks
    genus=Fraction(2-B-chi,2)
    assert (chi,B,genus)==(-4,6,0)
    covers=[]
    for degree in range(1,65):
        # Oriented boundary monodromies +1,-1 repeated three times.
        mon=[1,-1,1,-1,1,-1]
        assert sum(mon)==0
        # Each shift +/-1 is one cycle on Z/N; hence every boundary has a
        # single lift of degree N and the full cover is connected.
        assert all(len({(k*m)%degree for k in range(degree)})==degree for m in mon)
        covered_chi=degree*chi
        covered_genus=Fraction(2-6-covered_chi,2)
        capped_chi=covered_chi-2
        capped_genus=Fraction(2-2-capped_chi,2)
        objective=Fraction(-capped_chi,2*degree)
        assert covered_genus==2*degree-2
        assert capped_genus==2*degree+1
        assert objective==2+Fraction(1,degree)
        covers.append({'degree':degree,'cover_chi':covered_chi,'cover_boundary_count':6,
                       'cover_genus':int(covered_genus),'capped_chi':capped_chi,
                       'capped_boundary_count':2,'capped_genus':int(capped_genus),
                       'objective':[objective.numerator,objective.denominator]})

    # Rewiring is allowed only between compatible ends of the same graph edge:
    # ab <-> bc on b; bc <-> cd on c. Every A is then the unique degree-2
    # center of its b-component, with distinct M leaves (each b-degree one).
    possible_pair_sums=sorted({x+y for x,y in itertools.product((1,-3),repeat=2)})
    assert possible_pair_sums==[-6,-2,2]
    return {'generated_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'Independent finite certificate and topology audit; no exact absolute scl or general rationality claim',
            'reviewed_author_files':hashes,'all_reviewed_hashes_match':True,
            'historical_frozen_files':frozen['files'],
            'accepted_review_delta':accepted_delta,
            'coordinate_component_count':len(components),'bad_component_count':8,
            'transversal_size_counts':dict(sorted(counts.items())),
            'all_minimum_transversals':minima,'minimum_hitting_number':4,
            'all_integer_windings_match':True,'non_disk_residual_vectors':residual,
            'ribbon_face_lengths':list(map(len,faces)),'reconstructed_outer_words':words,
            'outer_abelianizations':abelianizations,'ad_projections':ad,'ac_projections':ac,
            'free_commutator_inputs':[u,v],'free_commutator_value':h,
            'relative_surface':{'chi':chi,'boundary_count':B,'genus':int(genus)},
            'cover_checks':covers,'compatible_rewiring_pair_charges':possible_pair_sums,
            'passed':True}


if __name__=='__main__':
    report=reproduce()
    target=HERE/'INDEPENDENT_RESULTS.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('generated_utc','bad_component_count','minimum_hitting_number','all_integer_windings_match','relative_surface','passed')},indent=2))
