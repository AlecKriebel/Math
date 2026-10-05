#!/usr/bin/env python3
"""Independent audit: generator-closure symmetries, spin characters, Shannon cover.

Reads the public hash-pinned Appendix and JSON as data. No producer or author
verifier is imported. Writes only a JSON receipt to standard output. All checks
use explicit exceptions and remain enabled with python -O.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
import re
import sys

SUPPORT = (0, 1, 2, 4, 7, 9, 10, 12)
PINS = {
    'appendix.md': '7e4ac6e492f2e1278f82b4c91dddd15de8f7e014beb3c2d62a63a6f3fe04e3f0',
    'certificate.json': '451797a35b04ef35c603b872cc965fc6adebaf43da49dc4b1ac3a6e32b34f1e7',
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def read_rows(text):
    # The row grammar is whole-line anchored; every multiset repetition remains.
    grammar = re.compile(r'^\|\s*(\d+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|$', re.M)
    rows = []
    for no, left, right, degree, outside in grammar.findall(text):
        require(int(no) == len(rows)+1, 'row numbering')
        rows.append((tuple(map(int,left.split(','))), tuple(map(int,right.split(','))), int(degree),int(outside)))
    require(len(rows) == 42, 'expected 42 complete printed rows')
    return rows

def check_json(data, rows):
    require(data['support'] == list(SUPPORT), 'JSON support')
    require(len(data['cuts']) == len(rows), 'JSON row count')
    for cut,(left,right,_,_) in zip(data['cuts'],rows):
        cl,cr = Counter(),Counter()
        for state,mult in cut['left']:
            require(type(state) is int and 0 <= state < 128, 'JSON joint state')
            require(type(mult) is int and mult > 0, 'JSON positive integer exponent')
            cl[state] += mult
        for vertex,hidden,mult in cut['right']:
            require(type(vertex) is int and 0 <= vertex < 8, 'JSON support position')
            require(type(hidden) is int and 0 <= hidden < 8, 'JSON hidden label')
            require(type(mult) is int and mult > 0, 'JSON positive integer exponent')
            cr[8*SUPPORT[vertex]+hidden] += mult
        require(cl == Counter(left) and cr == Counter(right), 'JSON/print mismatch')

# Walsh characters in least-significant-bit order, instead of Boolean features
# in the manuscript's most-significant-bit order. The bases are related by an
# invertible affine change: sigma=1-2x, tau=1-2h, sigma*tau=1-2x-2h+4xh.
CHARACTER_MASKS = (0,) + tuple(1 << k for k in range(7)) + tuple((1 << i)|(1 << j) for i in range(3,7) for j in range(3))

def identity(left,right):
    require(left and len(left) == len(right), 'degree')
    require(all(type(s) is int and 0 <= s < 128 for s in left+right), 'joint index')
    require(all(s >> 3 in SUPPORT for s in right), 'right visible support')
    for mask in CHARACTER_MASKS:
        a = sum(1 if (s & mask).bit_count()%2 == 0 else -1 for s in left)
        b = sum(1 if (s & mask).bit_count()%2 == 0 else -1 for s in right)
        require(a == b, 'spin character imbalance')
    outside = sum((s >> 3) not in SUPPORT for s in left)
    require(outside > 0 and len(left) <= 4*outside, 'leakage ratio')
    return len(left),outside

def cube_group(n):
    # Closure under n coordinate flips and n-1 adjacent coordinate transpositions.
    # No permutation-list construction is used.
    identity_map = tuple(range(2**n))
    generators = [tuple(x^(1<<i) for x in identity_map) for i in range(n)]
    for i in range(n-1):
        generators.append(tuple(x if ((x>>i)&1) == ((x>>(i+1))&1) else x^(3<<i) for x in identity_map))
    seen = {identity_map}
    pending = [identity_map]
    while pending:
        old = pending.pop()
        for generator in generators:
            new = tuple(generator[x] for x in old)
            if new not in seen:
                seen.add(new)
                pending.append(new)
    return sorted(seen)

def patterns_from_rows(rows):
    visible_full = cube_group(4)
    hidden = cube_group(3)
    visible = [g for g in visible_full if set(map(g.__getitem__, SUPPORT)) == set(SUPPORT)]
    require(len(visible_full) == 384 and len(visible) == 6 and len(hidden) == 48, 'symmetry group sizes')
    require(all(g[0] == 0 and g[8] == 8 for g in visible), 'visible group must fix first bit axis')
    position = {s:i for i,s in enumerate(SUPPORT)}
    patterns = set()
    multiplicity_histogram = Counter()
    degree_ratio = Fraction(0)
    transformations = 0
    for left,right,degree,outside in rows:
        require(identity(left,right) == (degree,outside), 'printed D or o')
        multiplicity_histogram[degree] += 1
        degree_ratio = max(degree_ratio,Fraction(degree,outside))
        for vg in visible:
            for hg in hidden:
                ll = tuple(8*vg[s>>3]+hg[s&7] for s in left)
                rr = tuple(8*vg[s>>3]+hg[s&7] for s in right)
                require(identity(ll,rr) == (degree,outside), 'transformed D or o')
                assignments = [-1]*8
                for state in rr:
                    i,h = position[state>>3],state&7
                    require(assignments[i] in (-1,h), 'conflicting selector requirements')
                    assignments[i] = h
                patterns.add(tuple(assignments))
                transformations += 1
    return sorted(patterns),{'visible_cube_group':len(visible_full),'visible_stabilizer':len(visible),'hidden_cube_group':len(hidden),'base_identities':len(rows),'transformed_identities':transformations,'distinct_unrestricted_patterns':len(patterns),'cylinder_cardinalities_with_overlaps':sum(8**p.count(-1) for p in patterns),'degree_histogram':dict(sorted(multiplicity_histogram.items())),'maximum_degree_over_outside':str(degree_ratio)}

def shannon_uncovered(patterns, dimension):
    """Count the complement of a union of cylinders by Shannon restriction.

    At a node, a completely free pattern covers its whole subcube. No patterns
    leave the entire subcube uncovered. Otherwise disjoint children fix the
    next hidden-state label in 0..7, deleting that coordinate from all compatible
    patterns. The sum of child complement counts is exact. Memoization merges
    equal residual problems, not merely symmetry-equivalent problems.
    """
    nodes_by_dimension = Counter()
    @lru_cache(None)
    def recurse(rows,n):
        nodes_by_dimension[n] += 1
        if (-1,)*n in rows:
            return 0
        if not rows:
            return 8**n
        require(n > 0, 'nonterminal zero-dimensional cover')
        total = 0
        for h in range(8):
            residual = tuple(sorted({r[1:] for r in rows if r[0] in (-1,h)}))
            total += recurse(residual,n-1)
        return total
    count = recurse(tuple(sorted(set(patterns))),dimension)
    info = {'uncovered':count,'covered':8**dimension-count,'domain':8**dimension,'recursive_nodes':sum(nodes_by_dimension.values()),'nodes_by_dimension':dict(sorted(nodes_by_dimension.items())),'memo_hits':recurse.cache_info().hits}
    recurse.cache_clear()
    return info

def matrix_cover(patterns):
    """Independent four-plus-four truth-table circuit evaluation, no cylinders marked.

    One 4096-bit row stores the disjunction of all right-half pattern predicates
    whose left-half predicates accept that row label. Every matrix bit corresponds
    bijectively to one unrestricted selector. This is direct predicate evaluation.
    """
    halves = list(product(range(8),repeat=4))
    right_predicates = {}
    def truth(p):
        if p not in right_predicates:
            right_predicates[p] = sum(1 << i for i,h in enumerate(halves) if all(a == -1 or a == b for a,b in zip(p,h)))
        return right_predicates[p]
    # Interleaved partition deliberately differs from Shannon's variable order.
    left_pos,right_pos = (0,2,4,6),(1,3,5,7)
    pred = [(tuple(p[i] for i in left_pos),truth(tuple(p[i] for i in right_pos))) for p in patterns]
    all_bits = (1 << 4096)-1
    covered = 0
    digest = sha256()
    for half in halves:
        union = 0
        for condition,bits in pred:
            if all(a == -1 or a == b for a,b in zip(condition,half)):
                union |= bits
                if union == all_bits:
                    break
        covered += union.bit_count()
        digest.update(union.to_bytes(512,'little'))
    return {'domain':8**8,'covered':covered,'uncovered':8**8-covered,'truth_matrix_bytes':4096*512,'truth_matrix_sha256':digest.hexdigest(),'partition':[[0,2,4,6],[1,3,5,7]]}

def controls(rows,data,patterns):
    def rejects(fn):
        try:
            fn()
        except (ValueError,KeyError,TypeError,IndexError):
            return True
        return False
    tests = {}
    tests['changed_state_rejected'] = rejects(lambda:identity((rows[0][0][0]^1,)+rows[0][0][1:],rows[0][1]))
    tests['missing_repeated_factor_rejected'] = rejects(lambda:identity(rows[27][0][:-1],rows[27][1]))
    tests['swapped_sides_rejected'] = rejects(lambda:identity(rows[0][1],rows[0][0]))
    tests['identity_without_forbidden_factor_rejected'] = rejects(lambda:identity(rows[0][1],rows[0][1]))
    corrupt = json.loads(json.dumps(data)); corrupt['cuts'][0]['left'][0][1] = -1
    tests['negative_exponent_rejected'] = rejects(lambda:check_json(corrupt,rows))
    corrupt = json.loads(json.dumps(data)); corrupt['cuts'][0]['right'][0][2] += 1
    tests['changed_exponent_rejected'] = rejects(lambda:check_json(corrupt,rows))
    corrupt = json.loads(json.dumps(data)); corrupt['support'][0] = 15
    tests['changed_support_rejected'] = rejects(lambda:check_json(corrupt,rows))
    tests['empty_cover_is_uncovered'] = shannon_uncovered([],8)['uncovered'] == 8**8
    tests['single_fixed_selector_covers_one'] = shannon_uncovered([(0,)*8],8)['covered'] == 1
    tests['one_free_variable_counts_eight'] = shannon_uncovered([(0,)*7+(-1,)],8)['covered'] == 8
    tests['single_certificate_pattern_is_insufficient'] = shannon_uncovered(patterns[:1],8)['uncovered'] > 0
    tests['matrix_empty_cover_is_uncovered'] = matrix_cover([])['uncovered'] == 8**8
    tests['matrix_single_pattern_exact'] = matrix_cover(patterns[:1])['covered'] == 8**patterns[0].count(-1)
    tests['matrix_shannon_partial_cover_agree'] = matrix_cover(patterns[:50])['uncovered'] == shannon_uncovered(patterns[:50],8)['uncovered']
    # Random small domains compare recursion against completely direct enumeration.
    rng = random.Random(20002559)
    comparisons = 0
    for n in range(1,5):
        states = list(product(range(8),repeat=n))
        for trial in range(12):
            pats = [tuple(rng.choice((-1,0,1,2,3,4,5,6,7)) for _ in range(n)) for _ in range(trial)]
            direct = sum(not any(all(a == -1 or a == b for a,b in zip(p,h)) for p in pats) for h in states)
            require(shannon_uncovered(pats,n)['uncovered'] == direct,'Shannon/direct small-domain disagreement')
            comparisons += 1
    tests['small_domain_comparisons'] = comparisons == 48
    require(all(tests.values()),'adversarial or coverage control failed')
    return tests

def positive_arithmetic():
    epsilon = Fraction(1,2**25)
    inside = (1-epsilon)/8 + epsilon/16
    outside = epsilon/16
    leakage = 8*outside
    rhs = (inside/8)**4
    require(inside > 0 and outside > 0 and 8*(inside+outside) == 1,'positive target')
    require(leakage < rhs,'positive exclusion')
    tv = 4*(abs(Fraction(1,8)-inside)+outside)
    require(tv == Fraction(1,2**26),'target TV')
    require(Fraction(15,1024)**4 > epsilon and Fraction(1,128) > epsilon,'uniform TV bound')
    return {'normalization':'1','inside':str(inside),'outside':str(outside),'off_support_mass':str(leakage),'strict_inequality_margin':str(rhs-leakage),'target_shift_tv':str(tv),'uniform_exclusion_tv_lower_bound':str(epsilon),'positive_exclusion_tv_lower_bound':str(epsilon-tv)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('appendix',type=Path)
    parser.add_argument('certificate',type=Path)
    args=parser.parse_args()
    ab,cb=args.appendix.read_bytes(),args.certificate.read_bytes()
    require(sha256(ab).hexdigest() == PINS['appendix.md'],'appendix hash pin')
    require(sha256(cb).hexdigest() == PINS['certificate.json'],'certificate hash pin')
    rows=read_rows(ab.decode()); data=json.loads(cb)
    check_json(data,rows)
    patterns,stats=patterns_from_rows(rows)
    shannon=shannon_uncovered(patterns,8)
    require(shannon['uncovered'] == 0,'uncovered selector in Shannon proof')
    matrix=matrix_cover(patterns)
    require(matrix['uncovered'] == 0,'uncovered selector in matrix proof')
    normalized={p[1:] for p in patterns if p[0] in (-1,0)}
    normal_check=shannon_uncovered(normalized,7)
    require(normal_check['uncovered'] == 0,'normalized selector gap')
    result={'status':'PASS','implementation':'fresh Walsh-character and generated-group check; exact Shannon and interleaved truth-matrix coverage','python_optimized':sys.flags.optimize,'input_sha256':PINS,'statistics':stats,'full_shannon_cover':shannon,'full_matrix_cover':matrix,'normalized_patterns':len(normalized),'normalized_cylinder_cardinalities_with_overlaps':sum(8**p.count(-1) for p in normalized),'normalized_shannon_cover':normal_check,'controls':controls(rows,data,patterns),'positive_arithmetic':positive_arithmetic()}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
