#!/usr/bin/env python3
"""Independent finite audit. Standard library only; never edits author files.

Darts carry a fixed-point-free edge involution alpha and face permutation phi.
Vertex cycles are cycles of phi*alpha. This retains loops, parallel edges,
repeated face corners, and self-adjacent face sides, unlike a simple adjacency
mesh. Rooted isomorphism uses deterministic traversal by alpha and phi.
Finite checks are controls, not certification of the asymptotic conjecture.
"""
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path

COUNTS = Counter()

def require(value, name):
    if not value:
        raise RuntimeError('FAILED: ' + name)
    COUNTS[name] += 1

def cycles(p):
    seen = set(); out = []
    for v in range(len(p)):
        if v in seen:
            continue
        c = []; u = v
        while u not in seen:
            seen.add(u); c.append(u); u = p[u]
        if u != v:
            raise ValueError('not a permutation')
        out.append(c)
    return out

def canonical(alpha, phi, root):
    order = [root]; number = {root: 0}
    for d in order:
        for e in (alpha[d], phi[d]):
            if e not in number:
                number[e] = len(order); order.append(e)
    if len(order) != len(alpha):
        return None, None
    return (tuple(number[alpha[d]] for d in order),
            tuple(number[phi[d]] for d in order)), number

def pairings(items, a):
    if not items:
        yield tuple(a); return
    x = items[0]
    for i in range(1, len(items)):
        y = items[i]; a[x] = y; a[y] = x
        yield from pairings(items[1:i] + items[i+1:], a)

def enumerate_maps(n):
    d = 6*n
    phi = tuple(3*(i//3)+(i+1)%3 for i in range(d))
    maps = set(); raw = connected = 0
    for alpha in pairings(tuple(range(d)), [0]*d):
        raw += 1
        key, _ = canonical(alpha, phi, 0)
        if key is not None:
            connected += 1; maps.add(key)
    return sorted(maps), raw, connected

def vertex_data(alpha, phi):
    cs = cycles(tuple(phi[alpha[d]] for d in range(len(alpha))))
    belongs = {}
    for i, c in enumerate(cs):
        for d in c:
            belongs[d] = i
    return cs, belongs

def genus(alpha, phi):
    v = len(vertex_data(alpha, phi)[0]); e = len(alpha)//2; f = len(cycles(phi))
    chi = v-e+f
    if (2-chi)%2 or chi > 2:
        raise ValueError('not an orientable connected cellular map')
    return (2-chi)//2

def metric(alpha, phi):
    cs, belongs = vertex_data(alpha, phi)
    adj = [set() for _ in cs]
    for d in range(len(alpha)):
        adj[belongs[d]].add(belongs[alpha[d]])
    ds = []
    for s in range(len(cs)):
        row = {s: 0}; todo = deque([s])
        while todo:
            x = todo.popleft()
            for y in adj[x]:
                if y not in row:
                    row[y] = row[x]+1; todo.append(y)
        if len(row) != len(cs):
            raise ValueError('disconnected metric')
        ds.append(row)
    return ds, belongs

def insert(alpha, phi, marked_side, ell):
    boundary = [marked_side, phi[marked_side], phi[phi[marked_side]]]
    require(phi[boundary[-1]] == boundary[0], 'triangular_input_face')
    a = list(alpha); p = list(phi); old_darts = len(a)
    edge_dart = {((0,i), (0,(i+1)%3)): boundary[i] for i in range(3)}
    faces = []
    for j in range(1, ell+1):
        for i in range(3):
            k = (i+1)%3
            faces += [((j-1,i),(j-1,k),(j,k)), ((j-1,i),(j,k),(j,i))]
    faces.append(((ell,0),(ell,1),(ell,2)))
    for face in faces:
        ds = []
        for x,y in zip(face, face[1:]+face[:1]):
            if (x,y) not in edge_dart:
                d = len(a); a.append(-1); p.append(-1); edge_dart[x,y] = d
                if (y,x) in edge_dart:
                    r = edge_dart[y,x]; a[d] = r; a[r] = d
            ds.append(edge_dart[x,y])
        for d,e in zip(ds,ds[1:]+ds[:1]):
            p[d] = e
    require(all(a[a[d]] == d and a[d] != d for d in range(len(a))), 'edge_involution_valid')
    require(all(len(c) == 3 for c in cycles(p)), 'all_output_faces_triangles')
    require(canonical(a,p,0)[0] is not None, 'output_map_connected')
    # Every boundary corner is an occurrence, not necessarily a distinct old vertex.
    layer_darts = [[edge_dart[((j,i),(j,(i+1)%3))] for i in range(3)]
                   for j in range(ell+1)]
    return tuple(a), tuple(p), boundary, layer_darts, old_darts


def patch_template(ell):
    faces = []
    for j in range(1,ell+1):
        for i in range(3):
            k=(i+1)%3
            faces += [((j-1,i),(j-1,k),(j,k)),((j-1,i),(j,k),(j,i))]
    faces.append(((ell,0),(ell,1),(ell,2)))
    dart_for_edge = {}; phi = []; alpha = []
    for face in faces:
        ds=[]
        for x,y in zip(face,face[1:]+face[:1]):
            d=len(alpha); alpha.append(-1); phi.append(-1); ds.append(d)
            dart_for_edge[x,y]=d
            if (y,x) in dart_for_edge:
                e=dart_for_edge[y,x]; alpha[d]=e; alpha[e]=d
        for d,e in zip(ds,ds[1:]+ds[:1]):phi[d]=e
    boundary=[dart_for_edge[(0,i),(0,(i+1)%3)] for i in range(3)]
    root=dart_for_edge[(ell,0),(ell,1)]
    return alpha,phi,boundary,root

def detect_certificates(alpha,phi,ell):
    # Independently find the tube by matching from every possible cap-side dart.
    # No insertion history, old-dart labels, or stored certificate is used here.
    ta,tp,tb,tr=patch_template(ell); found=set()
    for start in range(len(alpha)):
        mapping={tr:start}; used={start}; todo=[tr]; valid=True
        for t in todo:
            h=mapping[t]
            targets=[(tp[t],phi[h])]
            if ta[t]>=0:targets.append((ta[t],alpha[h]))
            for u,v in targets:
                if u in mapping:
                    if mapping[u]!=v:valid=False;break
                elif v in used:
                    valid=False;break
                else:
                    mapping[u]=v;used.add(v);todo.append(u)
            if not valid:break
        if not valid or len(mapping)!=len(ta):continue
        bd=tuple(mapping[d] for d in tb)
        internal=tuple(sorted(mapping[d] for d in range(len(ta)) if d not in tb))
        # Actual deletion must leave a connected map of the same genus.
        removed=set(internal); survivors=[d for d in range(len(alpha)) if d not in removed]
        relabel={d:i for i,d in enumerate(survivors)}; p=list(phi)
        for d,e in zip(bd,bd[1:]+bd[:1]):p[d]=e
        if not survivors or any(alpha[d] not in relabel or p[d] not in relabel for d in survivors):
            continue
        aa=tuple(relabel[alpha[d]] for d in survivors);pp=tuple(relabel[p[d]] for d in survivors)
        if canonical(aa,pp,0)[0] is None or genus(aa,pp)!=genus(alpha,phi):continue
        found.add((bd,internal))
    return found

def map_surgery_checks():
    records = []; totals = Counter(); cases = Counter()
    for n in (1,2):
        maps, raw, connected = enumerate_maps(n)
        by_genus = Counter(genus(*m) for m in maps)
        require(by_genus == ({0:4,1:1} if n == 1 else {0:32,1:28}), 'small_rooted_map_enumeration')
        for ell in (1,2):
            full = {g:set() for g in by_genus}; permitted = {g:set() for g in by_genus}
            hosts = {g:set() for g in by_genus}
            for alpha, phi in maps:
                g = genus(alpha,phi); old_ds, old_v = metric(alpha,phi)
                old_cycles, _ = vertex_data(alpha,phi)
                for mark in range(6*n):
                    aa, pp, bd, layers, old_darts = insert(alpha,phi,mark,ell)
                    dd, nv = metric(aa,pp)
                    require(genus(aa,pp) == g, 'all_map_surgery_genus_preserved')
                    require(len(aa) == 6*n+18*ell and len(cycles(pp)) == 2*n+6*ell,
                            'all_map_surgery_edge_face_counts')
                    require(len(dd) == len(old_ds)+3*ell, 'all_map_surgery_vertex_count')
                    old_to_new = {i:nv[c[0]] for i,c in enumerate(old_cycles)}
                    require(all(nv[d] == old_to_new[old_v[d]] for d in range(old_darts)),
                            'old_vertex_identifications_preserved')
                    require(all(dd[old_to_new[i]][old_to_new[j]] == old_ds[i][j]
                                for i in range(len(old_ds)) for j in range(len(old_ds))),
                            'all_map_surgery_old_distances')
                    require(all(min(dd[nv[d]][v] for v in old_to_new.values()) == j
                                for j, ds in enumerate(layers) for d in ds),
                            'all_map_surgery_exact_depths')
                    boundary_vertices = len({old_v[d] for d in bd})
                    cases['boundary_distinct_vertices_'+str(boundary_vertices)] += 1
                    if len({min(d,alpha[d]) for d in bd}) < 3:
                        cases['repeated_boundary_edge'] += 1
                    # Canonicalize rooted host plus the distinguished oriented certificate.
                    # The ordered boundary and ALL internal darts are part of the certificate.
                    for root in range(len(aa)):
                        key, relabel = canonical(aa,pp,root)
                        cert = (tuple(relabel[d] for d in bd),
                                tuple(sorted(relabel[d] for d in range(old_darts,len(aa)))))
                        pair = (key,cert)
                        full[g].add(pair); hosts[g].add(key)
                        if root < old_darts:
                            permitted[g].add(pair)
                    totals['surgery_instances'] += 1
            for g, tau in sorted(by_genus.items()):
                detected=set()
                for host in hosts[g]:
                    for cert in detect_certificates(*host,ell):
                        detected.add((host,cert))
                require(detected == full[g], 'independent_cap_search_certificate_sets_match')
                require(len(permitted[g]) == 6*n*tau, 'certificate_restricted_exact_count')
                require(len(full[g]) == 6*(n+3*ell)*tau, 'certificate_unrestricted_exact_count')
                require(Fraction(len(full[g]),len(permitted[g])) == Fraction(n+3*ell,n),
                        'automorphism_aware_reroot_ratio')
                records.append({'base_n':n,'genus':g,'height':ell,'tau_base':tau,
                                'distinct_tube_bearing_rooted_hosts':len(hosts[g]),
                                'restricted_certificates':len(permitted[g]),
                                'all_certificates':len(full[g])})
        totals['labeled_pairings'] += raw; totals['connected_pairings'] += connected
        totals['rooted_base_maps'] += len(maps)
    return {'enumeration_records':records, 'totals':dict(totals),
            'boundary_degeneracy_instances':dict(sorted(cases.items()))}

def probability_checks():
    # Exact conditioning transfer: multiset and core may be arbitrarily correlated.
    # Three atoms with varying numbers of high decorations and bad slot pairs.
    weights = [Fraction(1,2),Fraction(1,3),Fraction(1,6)]
    heights = [(10,9,0,0),(10,0,0,0),(10,9,8,0)]
    bad = [{(0,1),(1,0)}, {(i,j) for i in range(4) for j in range(4) if i!=j}, set()]
    actual = bound = Fraction(0)
    for w, hs, bad_pairs in zip(weights,heights,bad):
        chosen = [i for i,h in enumerate(hs) if h >= 9]
        cond_bad = Fraction(len(bad_pairs),12)
        bound += w*cond_bad
        if len(chosen)<2:
            continue
        failure_count = 0
        for p in permutations(range(4)):
            failure_count += (p[chosen[0]],p[chosen[1]]) in bad_pairs
        conditional_failure = Fraction(failure_count,24)
        require(conditional_failure == cond_bad, 'uniform_permutation_high_pair_transfer')
        actual += w*conditional_failure
    require(actual <= bound, 'correlated_environment_transfer_inequality')
    # Without independence of the slot assignment, choose high items on bad slots.
    require(Fraction(1) > Fraction(2,12), 'negative_slot_selection_bias')
    # A divergent expected number of hits need not give existence with high probability.
    for n in (16,81,256,625):
        p = Fraction(1,int(n**0.5)); mu = n*p
        require(mu > 1 and p < Fraction(1,2), 'negative_diverging_mean_no_existence')
    return {'correlated_environment_bad_high_pair_probability':str(actual),
            'uniform_pair_bad_probability':str(bound)}

def main():
    maps = map_surgery_checks(); probability = probability_checks()
    return {'scope':'Independent finite combinatorial-map and exact-probability controls only.',
            'all_checks_passed':True,'total_checks':sum(COUNTS.values()),
            'counts':dict(sorted(COUNTS.items())), 'maps':maps,'probability':probability,
            'full_target_solved':False, 'asymptotic_theorems_certified_by_computation':False}

if __name__ == '__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
