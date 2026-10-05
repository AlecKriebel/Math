#!/usr/bin/env python3
"""Independent KOU-21.114 finite controls, standard library only.

Written from the statements and author result schema without reading/importing
verify_math.py. Groups are generated as faithful permutations. The lattice walk
uses normal index-p extensions, rather than the author's arbitrary adjunction
algorithm. By the normalizer condition for finite p-groups it reaches every
subgroup. No external group databases, source files or network are needed.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path


def compose(a, b):
    """a after b."""
    return tuple(a[i] for i in b)


def affine_generators(p, exponent, inversion_only=False):
    modulus = p ** exponent
    units = [modulus - 1] if inversion_only else list(range(1, modulus, p))
    return [tuple((i + 1) % modulus for i in range(modulus))] + [
        tuple(u * i % modulus for i in range(modulus)) for u in units if u != 1
    ]


def cyclic_generators(p):
    return [tuple((i + 1) % p for i in range(p))]


def wreath_generators(base_generators, p):
    d = len(base_generators[0])
    degree = d * p
    out = []
    for block in range(p):
        for g in base_generators:
            t = list(range(degree))
            for i in range(d):
                t[block * d + i] = block * d + g[i]
            out.append(tuple(t))
    out.append(tuple(((i // d + 1) % p) * d + i % d for i in range(degree)))
    return out


def unitriangular_generators():
    # Elementary upper-unitriangular matrices act on all column vectors of F_2^4.
    return [tuple(v ^ ((((v >> (i + 1)) & 1) << i)) for v in range(16)) for i in range(3)]


class PermutationGroup:
    def __init__(self, generators):
        self.degree = len(generators[0])
        identity = tuple(range(self.degree))
        assert all(sorted(g) == list(identity) for g in generators)
        reached = {identity}
        queue = deque([identity])
        while queue:
            a = queue.popleft()
            for s in generators:
                b = compose(a, s)
                if b not in reached:
                    reached.add(b)
                    queue.append(b)
        self.elements = sorted(reached)
        self.index = {g: i for i, g in enumerate(self.elements)}
        assert self.elements[0] == identity
        self.order = len(self.elements)
        self.all = frozenset(range(self.order))
        self.table = [[self.index[compose(a, b)] for b in self.elements] for a in self.elements]
        self.inverse = []
        for i, row in enumerate(self.table):
            choices = [j for j, v in enumerate(row) if v == 0 and self.table[j][i] == 0]
            assert len(choices) == 1
            self.inverse.append(choices[0])
        self.commutators = [[self.table[self.table[self.table[self.inverse[x]][self.inverse[y]]][x]][y]
                              for y in range(self.order)] for x in range(self.order)]
        self.generators = tuple(self.index[g] for g in generators)

    def generate(self, generators):
        generators = sorted(set(generators) - {0})
        reached = {0}
        queue = deque([0])
        while queue:
            a = queue.popleft()
            for s in generators:
                b = self.table[a][s]
                if b not in reached:
                    reached.add(b)
                    queue.append(b)
        return frozenset(reached)

    def validate_table(self):
        t, n = self.table, self.order
        for a in range(n):
            assert t[a][0] == a == t[0][a]
            assert len(set(t[a])) == n
            for b in range(n):
                abrow, brow = t[t[a][b]], t[b]
                assert all(abrow[c] == t[a][brow[c]] for c in range(n))
        return n ** 3

    def subgroup_ok(self, h):
        assert 0 in h
        assert all(self.inverse[x] in h for x in h)
        assert all(self.table[x][y] in h for x in h for y in h)

    def commutator_subgroup(self, h, k):
        return self.generate(self.commutators[x][y] for x in h for y in k)

    def derived(self, h):
        d = self.commutator_subgroup(h, h)
        assert d <= h
        # Independent quotient sanity check: normality and commuting cosets.
        assert all(self.table[self.table[self.inverse[x]][y]][x] in d for x in h for y in d)
        return d

    def ab(self, h):
        d = self.derived(h)
        assert len(h) % len(d) == 0
        return len(h) // len(d)

    def series(self, lower=False):
        out = [self.all]
        while len(out[-1]) > 1:
            nxt = self.commutator_subgroup(out[-1], self.all if lower else out[-1])
            assert nxt < out[-1]
            out.append(nxt)
        return [len(x) for x in out]

    def lattice(self, p):
        # Every proper H<K in a finite p-group has H<N_K(H); N_K(H)/H
        # has an order-p subgroup. Thus index-p normal extensions suffice.
        assert self.order > 0
        n = self.order
        while n % p == 0:
            n //= p
        assert n == 1
        seen = {frozenset([0]): ()}
        queue = deque([frozenset([0])])
        t, inv = self.table, self.inverse
        while queue:
            h = queue.popleft()
            for x in self.all - h:
                xp = 0
                powers = []
                for _ in range(p):
                    powers.append(xp)
                    xp = t[xp][x]
                if xp not in h:
                    continue
                if not all(t[t[inv[x]][y]][x] in h for y in h):
                    continue
                k = frozenset(t[u][y] for u in powers for y in h)
                assert len(k) == p * len(h)
                if k not in seen:
                    seen[k] = seen[h] + (x,)
                    queue.append(k)
        for h, generators in seen.items():
            self.subgroup_ok(h)
            assert self.generate(generators) == h
        assert self.all in seen
        return sorted(seen, key=lambda h: (len(h), tuple(sorted(h))))

    def summary(self, name, exhaustive, p):
        derived, lower = self.series(), self.series(True)
        out = dict(name=name, permutation_degree=self.degree, order=self.order,
                   abelianization_order=derived[0] // derived[1],
                   derived_series_orders=derived, lower_central_series_orders=lower,
                   derived_length=len(derived)-1, nilpotency_class=len(lower)-1,
                   associativity_triples_checked=self.validate_table(),
                   permutation_elements_sha256=sha256(json.dumps(self.elements, separators=(',', ':')).encode()).hexdigest())
        if exhaustive:
            subgroups = self.lattice(p)
            data = [(len(h), self.ab(h)) for h in subgroups]
            out.update(all_subgroups_enumerated=len(subgroups),
                       max_subgroup_abelianization_order=max(a for _, a in data),
                       weakly_ab_maximal=all(a <= out['abelianization_order'] for _, a in data),
                       strictly_ab_maximal=all(a < out['abelianization_order'] for size, a in data if size < self.order),
                       subgroup_order_abelianization_histogram=[[size, a, count] for (size, a), count in sorted(Counter(data).items())])
        return out


def compute():
    cases, groups = [], {}
    specifications = []
    for p, exponent in [(2,2),(2,3),(2,4),(3,2),(3,3),(5,2)]:
        specifications.append((f'C{p**exponent}_semidirect_SylowAut', affine_generators(p, exponent), p, True))
    specifications.append(('C8_semidirect_inversion', affine_generators(2,3,True),2,True))
    w2 = wreath_generators(cyclic_generators(2),2)
    specifications.extend([('(C2)_wr_C2',w2,2,True),
                           ('((C2)_wr_C2)_wr_C2',wreath_generators(w2,2),2,False),
                           ('(C3)_wr_C3',wreath_generators(cyclic_generators(3),3),3,False),
                           ('UT4(2)',unitriangular_generators(),2,True)])
    for name, generators, p, exhaustive in specifications:
        g = PermutationGroup(generators)
        groups[name] = g
        s = g.summary(name, exhaustive, p)
        if name == '((C2)_wr_C2)_wr_C2':
            base = frozenset(i for i,e in enumerate(g.elements) if all(e[j]//4 == j//4 for j in range(8)))
            g.subgroup_ok(base)
            d = g.derived(base)
            center = frozenset(i for i in g.all if all(g.table[i][j] == g.table[j][i] for j in g.all))
            s['disqualifying_section'] = dict(subgroup='base W2 x W2',order=len(base),derived_order=len(d),abelianization_order=len(base)//len(d))
            s['central_product_obstruction'] = dict(center_order=len(center),center_is_contained_in_base_derived=center <= d)
        elif name == '(C3)_wr_C3':
            base = frozenset(i for i,e in enumerate(g.elements) if all(e[j]//3 == j//3 for j in range(9)))
            g.subgroup_ok(base)
            d = g.derived(base)
            s['disqualifying_section'] = dict(subgroup='base C3^3',order=len(base),derived_order=len(d),abelianization_order=len(base)//len(d))
        cases.append(s)
        print(f"Verified {name}: order {g.order}; lattice {s.get('all_subgroups_enumerated', 'explicit witness')}", flush=True)
    # Explicit embedding and subgroup failures, rather than only matching invariants.
    by_name = {c['name']: c for c in cases}
    assert by_name['(C2)_wr_C2']['weakly_ab_maximal']
    assert not by_name['(C2)_wr_C2']['strictly_ab_maximal']
    assert by_name['((C2)_wr_C2)_wr_C2']['derived_length'] == 3
    for p, exponent in [(2,2),(2,3),(2,4),(3,2),(3,3),(5,2)]:
        row = by_name[f'C{p**exponent}_semidirect_SylowAut']
        assert row['weakly_ab_maximal'] and row['derived_length'] == 2
        assert row['nilpotency_class'] == exponent
    ambient = groups['C8_semidirect_SylowAut']
    dihedral = groups['C8_semidirect_inversion']
    embedding = [ambient.index[e] for e in dihedral.elements]
    assert all(embedding[dihedral.table[i][j]] == ambient.table[embedding[i]][embedding[j]]
               for i in dihedral.all for j in dihedral.all)
    rotations = ambient.generate([ambient.index[tuple((i+1)%8 for i in range(8))]])
    assert len(rotations) == 8 and ambient.ab(rotations) == 8
    assert ambient.ab(frozenset(embedding)) == 4
    ut = groups['UT4(2)']
    rectangle_generators = [tuple(v ^ (((v>>j)&1)<<i) for v in range(16)) for i in range(2) for j in range(2,4)]
    rectangle = ut.generate(ut.index[e] for e in rectangle_generators)
    assert len(rectangle) == 16 and ut.ab(rectangle) == 16
    # Family inequalities are sanity samples, never substitutes for symbolic proofs.
    wreath_samples = []
    for p in [2,3,5,7,11]:
        for exponent in range(1,12):
            m = p**exponent
            value = 1
            for _ in range(m-1):
                value *= p
                if value > m:
                    break
            allowed = value <= m
            assert allowed == (p == 2 and m == 2)
            wreath_samples.append([p,exponent,allowed])
    rectangular_samples = [[n,(n//2)*(n-n//2),n-1] for n in range(4,101)]
    assert all(a>b for n,a,b in rectangular_samples)
    return dict(problem_id=2623, problem_number='KOU-21.114', result='unresolved_after_five_approaches',
                method='Independent permutation-generator reconstruction; normal index-p extension lattice enumeration',
                cases=cases, negative_controls=dict(dihedral_embedding_verified=True,
                  ambient_ab=8,dihedral_ab=4,rotation_ab=8,rectangular_subgroup_order=16,
                  strict_vs_weak_separated=True),
                wreath_inequality_samples=55, unitriangular_rectangular_witness_samples=97)


def compare_author(result, path):
    author = json.loads(path.read_text())
    theirs = {c['name']: c for c in author['cases']}
    compared = []
    keys = ['order','abelianization_order','derived_series_orders','lower_central_series_orders',
            'derived_length','nilpotency_class','all_subgroups_enumerated','max_subgroup_abelianization_order',
            'weakly_ab_maximal','strictly_ab_maximal','subgroup_order_abelianization_histogram',
            'disqualifying_section','central_product_obstruction']
    assert set(theirs) == {c['name'] for c in result['cases']}
    for c in result['cases']:
        for key in keys:
            if key in theirs[c['name']]:
                assert c[key] == theirs[c['name']][key], (c['name'],key,c[key],theirs[c['name']][key])
                compared.append([c['name'],key])
        assert c['associativity_triples_checked'] == theirs[c['name']]['all_associativity_triples_checked']
    return dict(author_results_sha256=sha256(path.read_bytes()).hexdigest(),
                all_compared_fields_match=True, invariant_comparisons=len(compared),
                table_hashes_compared=False,reason='Different faithful permutation representations and labelings')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--compare-author',type=Path)
    parser.add_argument('--check',type=Path)
    args = parser.parse_args()
    result = compute()
    if args.compare_author:
        result['author_comparison'] = compare_author(result,args.compare_author)
    payload = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        previous=json.loads(args.check.read_text())
        previous.pop('author_comparison',None)
        candidate=dict(result);candidate.pop('author_comparison',None)
        assert candidate == previous, 'Saved independent results differ'
        print('Saved independent results match exactly.')
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload)

if __name__ == '__main__':
    main()
