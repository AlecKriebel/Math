#!/usr/bin/env python3
"""Independent finite controls, not a proof of any infinite-process theorem."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json


def run():
    counts = Counter()
    def check(v, family):
        if not v:
            raise AssertionError(family)
        counts[family] += 1

    # A different closed-form route: exact remainder and complete-group cutoffs.
    def tail(k):
        return F(2, k*(k+1))
    def atom(k):
        return (tail(k)-tail(k+1))/2**k
    def best_omitted(m):
        # Complete groups through n consume 2^(n+1)-2 atoms.
        n = (m+2).bit_length()-2
        residual = m-(2**(n+1)-2)
        return tail(n+1)-residual*atom(n+1)

    for k in range(1,2001):
        check(2**k*atom(k) == F(4,k*(k+1)*(k+2)), 'group_identity')
        check(atom(k+1)/atom(k) == F(k,2*(k+3)), 'atom_order')
        check(best_omitted(2**(k+1)-2) == tail(k+1), 'complete_group_cutoff')
        # For the partition 1,...,k,>k, compare to the geometric law lumped
        # into the same partition. The finite Gibbs bound is <= this cost.
        cost = 2-F(4,k+2)+k*tail(k+1)
        check(cost == 2-F(2,k+1) and cost < 2, 'finite_entropy_cost')

    # Literal sorted atom enumeration supplies a check independent of the formula.
    atoms = sorted([atom(k) for k in range(1,10) for _ in range(2**k)], reverse=True)
    covered = F(0)
    for m,a in enumerate(atoms,1):
        covered += a
        check(1-covered == best_omitted(m), 'enumerated_omitted_mass')
    candidates = list(range(1,5001)) + [2**k+delta for k in range(13,121) for delta in (-2,-1,0,1,2)]
    for m in candidates:
        K = (m-1).bit_length()+1
        check(best_omitted(m) >= F(1,K*(K+1)), 'tail_lower_bound')
        check(2**K >= 2*m, 'threshold_ceil')

    for d in range(1,5):
        for r in range(6):
            volume = (2*r+1)**d
            for b in range(1,6):
                m = b**volume
                K = (m-1).bit_length()+1
                check(best_omitted(m) >= F(1,K*(K+1)), 'source_cardinality_bound')

    # Exhaust every three-valued function on several finite binary-block
    # supports, including dependent and zero-probability cylinder examples.
    words = list(product((0,1), repeat=3))
    supports = [words, [w for w in words if sum(w)%2==0], words[:3], [words[0]]]
    maps = 0
    for support in supports:
        masses = [F(i+1, len(support)*(len(support)+1)//2) for i in range(len(support))]
        for values in product(range(3), repeat=len(support)):
            maps += 1
            marginal = [sum((m for a,m in zip(values,masses) if a==z), F(0)) for z in range(3)]
            decided = set()
            forced = {}
            for center in (0,1):
                indices = [i for i,w in enumerate(support) if w[1]==center]
                possible = {values[i] for i in indices}
                if len(possible)==1:
                    forced[center] = next(iter(possible))
                    decided.update(indices)
            omitted = 1-sum((masses[i] for i in decided),F(0))
            check(omitted >= 1-sum(sorted(marginal,reverse=True)[:2]), 'cylinder_support_inequality')
            check(len(set(forced.values())) <= 2, 'decided_symbol_cardinality')
            check(all(values[i]==forced[support[i][1]] for i in decided), 'extension_consistency')
            # Replace undecided positions by zero; the error is bounded by
            # undecided probability, even when the source has correlations.
            error = sum((masses[i] for i in range(len(support))
                         if forced.get(support[i][1],0)!=values[i]), F(0))
            check(error <= omitted, 'default_symbol_error')

    # Negative controls are rejected statements, not claimed counterexamples
    # to any of the propositions under their stated hypotheses.
    negative = {}
    # Eight output symbols from three fair input bits are a radius-one code.
    negative['replace_block_word_count_by_single_site_count'] = F(0) < 1-F(2,8)
    check(negative['replace_block_word_count_by_single_site_count'], 'negative_control')
    # Finite input alphabet cannot be dropped: the proposed countable law is
    # exactly its own radius-zero source, whereas every finite M misses mass.
    negative['apply_finite_source_bound_to_countable_identity'] = F(0) < best_omitted(8)
    check(negative['apply_finite_source_bound_to_countable_identity'], 'negative_control')
    # Radius-zero test must demand constancy on the whole positive cylinder.
    # Injective ternary output on 000,001,010 has two observed middle symbols.
    support = [words[0],words[1],words[2]]
    negative['one_sample_agreement_is_local_determination'] = len(support)>len({w[1] for w in support})
    check(negative['one_sample_agreement_is_local_determination'], 'negative_control')
    return {'status':'PASS','assertions':sum(counts.values()),'families':dict(counts),
            'finite_maps_exhausted':maps,'negative_controls_rejected':negative,
            'arithmetic':'exact integers and rational numbers',
            'infinite_process_theorems_proved_by_computation':False,
            'original_finite_valued_target':'UNRESOLVED','approaches_used':'5/5'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
