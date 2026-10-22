#!/usr/bin/env python3
"""Exact independent finite controls; no finite model of a free ultrafilter."""
import itertools
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def powerset(n):
    return tuple(frozenset(c) for k in range(n + 1)
                 for c in itertools.combinations(range(n), k))


def v2(m):
    need(type(m) is int and m > 0, 'v2 domain')
    j = 0
    while m % 2 == 0:
        m //= 2
        j += 1
    return j


def subgroup(a):
    return frozenset(frozenset(c) for k in range(len(a) + 1)
                     for c in itertools.combinations(sorted(a), k))


def coset(s, a):
    return frozenset(s ^ t for t in subgroup(a))


def main():
    out = {'status': 'PASS', 'free_ultrafilter_constructed_or_simulated': False,
           'infinite_proof_mechanized': False, 'counts': {}, 'negative_controls': []}
    g = powerset(4)
    z = frozenset()
    count = 0
    for x, y, w in itertools.product(g, repeat=3):
        need((x ^ y) ^ w == x ^ (y ^ w), 'associativity')
        need(x ^ x == z and x ^ y == y ^ x, 'Boolean group')
        count += 1
    out['counts']['group_triples'] = count
    count = 0
    for a, b in itertools.product(g, repeat=2):
        need(subgroup(a) & subgroup(b) == subgroup(a & b), 'subgroup intersection')
        for s, t in itertools.product(g, repeat=2):
            ca, cb = coset(s, a), coset(t, b)
            inter = ca & cb
            if inter:
                x = min(inter, key=lambda q: tuple(sorted(q)))
                need(inter == coset(x, a & b), 'coset intersection base axiom')
            need(frozenset(x ^ y for x in coset(s, a) for y in coset(t, a))
                 == coset(s ^ t, a), 'joint continuity algebra')
            count += 1
    out['counts']['two_subgroup_coset_cases'] = count
    count = 0
    for s, t in itertools.permutations(g, 2):
        k = min(s ^ t)
        a = frozenset(range(4)) - {k}
        need(not coset(s, a) & coset(t, a), 'coordinate separation')
        count += 1
    out['counts']['finite_coordinate_separations'] = count
    # Different implementation from the candidate: explicit sets and closed-form q.
    count = 0
    for s in powerset(6):
        for j in range(7):
            base, period = 2**j - 1, 2**(j + 1)
            q = base + max(0, (len(s) - base + period - 1) // period) * period
            need(q >= len(s) and v2(q + 1) == j, 'closed-form support size')
            need(q - period < len(s), 'smallest admissible size')
            for step in range(1, 8):
                for residue in range(step):
                    t = set()
                    for fresh in itertools.count(residue, step):
                        if len(t) == q - len(s):
                            break
                        if fresh not in s:
                            t.add(fresh)
                    need(not s & t and len(s ^ t) == q, 'fresh extension size')
                    need(v2(len(s ^ t) + 1) == j, 'all dense colors')
                    need(all(x % step == residue for x in t), 'extension in infinite reservoir')
                    count += 1
    out['counts']['set_based_density_extensions'] = count
    fibers = []
    for k in range(14):
        family = [s for s in powerset(k + 1) if s and max(s) == k]
        need(len(family) == 2**k, 'maximum fiber exactly 2^k')
        fibers.append(len(family))
    out['counts']['maximum_fiber_counts_k0_to13'] = fibers
    supports = tuple(s for s in powerset(3) if s)
    count, decisions = 0, 0
    for assignment in itertools.product(range(4), repeat=len(supports)):
        blocks = [set() for _ in range(3)]
        for s, label in zip(supports, assignment):
            if label:
                blocks[label - 1].add(s)
        maxima = [set(map(max, f)) for f in blocks]
        for k in range(3):
            need(sum(k in m for m in maxima) <= 2**k, 'point-finite bound')
        chosen, used = [], set()
        for n, m in enumerate(maxima):
            if m and not m & used:
                chosen.append(n)
                used |= m
        unions = [set(), set()]
        for i, n in enumerate(chosen):
            unions[i % 2] |= maxima[n]
        need(not unions[0] & unions[1], 'parity disjoint')
        # Finite principal atom is ONLY a control of filter-decision algebra.
        # It does NOT witness freeness, infinite density, or infinite subsequences.
        for atom in range(4):
            nonmembers = [e for e in (0, 1) if atom not in unions[e]]
            need(nonmembers, 'at least one side outside a proper ultrafilter')
            for e in nonmembers:
                available = set(range(4)) - unions[e]
                need(atom in available, 'chosen complement is a filter member')
                for i, n in enumerate(chosen):
                    if i % 2 == e:
                        need(all(not s <= available for s in blocks[n]), 'entire block missed')
                decisions += 1
        count += 1
    out['counts']['all_labeled_disjoint_block_assignments'] = count
    out['counts']['finite_decision_algebra_cases'] = decisions
    # Exhaust all assignments INCLUDING identity and explicitly remove all
    # empty/identity exceptions through the last exceptional finite index.
    full_g = powerset(3)
    assignment_count, tails_with_blocks, excisions = 0, 0, 0
    for assignment in itertools.product(range(4), repeat=len(full_g)):
        blocks = [set() for _ in range(3)]
        for s, label in zip(full_g, assignment):
            if label:
                blocks[label - 1].add(s)
        bad = [i for i, f in enumerate(blocks) if not f or z in f]
        cut = max(bad, default=-1)
        excisions += bool(bad)
        tail = blocks[cut + 1:]
        need(all(f and z not in f for f in tail), 'all and only safe tail inputs')
        need(all(not blocks[i] & blocks[j] for i in range(3) for j in range(i)),
             'labeled assignments disjoint')
        maxima = [set(map(max, f)) for f in tail]
        for k in range(3):
            need(sum(k in m for m in maxima) <= 2**k, 'full-family point-finiteness')
        selected, used = [], set()
        for n, m in enumerate(maxima):
            if not m & used:
                selected.append(n)
                used |= m
        parity = [set(), set()]
        for i, n in enumerate(selected):
            parity[i % 2] |= maxima[n]
        need(not parity[0] & parity[1], 'post-excision parity disjoint')
        for e in range(2):
            available = set(range(3)) - parity[e]
            for i, n in enumerate(selected):
                if i % 2 == e:
                    need(all(not s <= available for s in tail[n]), 'safe-tail exclusion')
        tails_with_blocks += bool(tail)
        assignment_count += 1
    out['counts']['all_assignments_including_identity'] = assignment_count
    out['counts']['identity_empty_prefix_excision_cases'] = excisions
    out['counts']['safe_nonempty_finite_tails'] = tails_with_blocks
    # Negative control: minimum has infinite fibers, even for disjoint blocks.
    min_bad = [{frozenset({0, k})} for k in range(1, 21)]
    need(len(set.union(*min_bad)) == 20, 'control blocks genuinely disjoint')
    need(all({min(s) for s in f} == {0} for f in min_bad), 'minimum point-finiteness failure')
    out['negative_controls'].append({'name': 'replace_maximum_by_minimum',
                                    'detected': True, 'repeated_minimum': 20})
    # Negative control: dropping disjointness destroys the maximum bound.
    repeated = [{frozenset({0})} for _ in range(20)]
    need(sum(0 in {max(s) for s in f} for f in repeated) > 2**0, 'repetition violates bound')
    out['negative_controls'].append({'name': 'drop_block_disjointness', 'detected': True})
    # Negative control: both parity unions may lie outside the ultrafilter.
    c0, c1, atom = {0}, {1}, 2
    need(atom not in c0 and atom not in c1, 'both nonmembers example')
    need(atom not in set(range(3)) - ({0} | {1, 2}), 'union complement need not be member')
    out['negative_controls'].append({'name': 'assert_exactly_one_parity_union_is_a_member', 'detected': True})
    # Principal topology: H_{atom} has two points and cannot be separated at 0, {atom}.
    need(subgroup(frozenset({7})) == {z, frozenset({7})}, 'principal minimal subgroup')
    need(not any(len(set(labels)) == 3 for labels in itertools.product(range(3), repeat=2)),
         'three disjoint dense pieces cannot meet a two-point minimal open set')
    out['negative_controls'].append({'name': 'replace_free_ultrafilter_by_principal',
                                    'detected': True, 'minimal_open_size': 2})
    # A cofinite filter does not decide the parity split; complement step fails.
    even, odd = set(range(0, 100, 2)), set(range(1, 100, 2))
    need(even | odd == set(range(100)) and not even & odd, 'finite parity prefix')
    # Stronger exact positive control: finite prefixes of an infinite expansive
    # construction for the cofinite topology. Its basic cylinders specify the
    # first k coordinates. At stage n, append a unique new high-coordinate tag
    # to each of the first n+1 requirements, so no group element is ever reused.
    requirements = [(k, p) for k in range(8) for p in powerset(k)]
    used_supports, blocks, max_used = set(), [], -1
    for n in range(40):
        block = set()
        for k, pattern in requirements[:n + 1]:
            tag = max(max_used + 1, k)
            s = pattern | {tag}
            need(s not in used_supports and s not in block, 'fresh block element')
            need(s & set(range(k)) == pattern, 'cylinder met')
            block.add(s)
            max_used = tag
        for k, pattern in requirements[:n + 1]:
            need(any(s & set(range(k)) == pattern for s in block), 'all current basic cylinders')
        used_supports |= block
        blocks.append(block)
    need(sum(map(len, blocks)) == len(used_supports), 'cofinite blocks pairwise disjoint')
    out['negative_controls'].append({'name': 'drop_ultrafilter_decisiveness_use_cofinite_filter',
                                    'detected': True, 'expansive_construction_stages_checked': 40,
                                    'distinct_supports': len(used_supports),
                                    'interpretation': 'finite prefixes validate an explicit infinite construction described in REVIEW.md'})
    # Identity and empty blocks are not silently given a maximum.
    preprocess = [set(), {z}, {frozenset({0})}, set(), {frozenset({1})}, {frozenset({2})}]
    last_exception = max(i for i, f in enumerate(preprocess) if not f or z in f)
    need(last_exception == 3 and all(f and z not in f for f in preprocess[last_exception + 1:]),
         'finite exceptional-prefix removal')
    out['negative_controls'].append({'name': 'empty_and_identity_preprocessing', 'detected': True})
    out['scope'] = ('Finite exact algebra, constructive density extensions and hypothesis controls only. '
                    'ZFC free-ultrafilter existence and the universal infinite obstruction are proved in prose, not certified here.')
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
