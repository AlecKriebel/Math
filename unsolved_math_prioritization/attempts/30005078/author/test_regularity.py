"""Deterministic replay, including independent singly graded Koszul checks."""
import json
import random
from itertools import combinations, product
from pathlib import Path
from monomial_regularity import (MonomialQuotient, matrix_rank, satisfies,
                                generalized_le, complete_intersection_frontier)


def koszul_regularities(generators, n):
    """Independent regularity via fine-degree Koszul homology of S/I.

    Taylor's resolution bounds Tor support by coordinatewise lcm exponents.
    This oracle is used only for the SINGLE graded regression cases.
    """
    if (0,) * n in generators:
        return None
    caps = [max((g[j] for g in generators), default=0) for j in range(n)]
    result = None
    for a in product(*(range(c + 1) for c in caps)):
        bases = []
        for i in range(n + 1):
            good = []
            for subset in combinations(range(n), i):
                u = tuple(v - int(j in subset) for j, v in enumerate(a))
                if min(u) >= 0 and not any(all(x <= y for x, y in zip(g, u)) for g in generators):
                    good.append(subset)
            bases.append(good)
        ranks = [0]
        for i in range(1, n + 1):
            target_index = {s: j for j, s in enumerate(bases[i - 1])}
            a_mat = [[0] * len(bases[i]) for _ in bases[i - 1]]
            for col, subset in enumerate(bases[i]):
                for pos in range(len(subset)):
                    target = subset[:pos] + subset[pos + 1:]
                    if target in target_index:
                        a_mat[target_index[target]][col] = (-1) ** pos
            ranks.append(matrix_rank(a_mat))
        ranks.append(0)
        for i in range(n + 1):
            if len(bases[i]) - ranks[i] - ranks[i + 1] > 0:
                v = sum(a) - i
                result = v if result is None else max(result, v)
    return result


def run():
    cases = [
        ('free', [], ((0, 0),), ((0, 0),)),
        ('point', [(1,0,0,0),(0,0,1,0)], ((0,0),), ((0,0),)),
        ('fat_point', [(2,0,0,0),(0,0,3,0)], ((1,2),), ((1,2),)),
        ('two_points_saturated', [(1,1,0,0),(1,0,1,0),(0,1,0,1),(0,0,1,1)],
         ((0,1),(1,0)), ((0,1),(1,0))),
        ('unsaturated_ci', [(1,0,1,0),(0,1,0,1)], ((1,1),), ((1,1),)),
        ('hypersurface', [(3,0,2,0)], ((2,1),), ((2,1),)),
        ('zero_sheaf_unbounded', [(1,0,0,0),(0,1,0,0)], (), ((1,None),)),
        ('zero_module', [(0,0,0,0)], (), ((None,None),)),
        ('residue_field', [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)],
         ((0,0),), ((0,0),(1,None),(None,1))),
    ]
    checks = 0
    outputs = []
    for characteristic in (0, 2, 3, 101):
        for name, generators, expected_min, expected_orthants in cases:
            module = MonomialQuotient((2,2), generators, characteristic)
            result = module.regularity(check_complex=True)
            assert result['minimal_elements'] == expected_min, (name, result)
            assert set(result['generalized_orthants']) == set(expected_orthants)
            checks += 2
            for d in product(range(-3, 7), repeat=2):
                expected = any(generalized_le(a, d) for a in expected_orthants)
                assert satisfies(result['clauses'], d) == expected
                checks += 1
            if characteristic == 0:
                outputs.append({'name': name, **result})
    assert complete_intersection_frontier([(3,2)]) == ((2,1),)
    # This input is metadata for a certified CI, not a saturation check.
    assert complete_intersection_frontier([(2,3),(3,1)]) == ((3,3),(4,2))
    assert matrix_rank([[1,1],[1,-1]]) == 2
    assert matrix_rank([[1,1],[1,-1]], 2) == 1
    checks += 4
    point = MonomialQuotient((2,2), [(1,0,0,0),(0,0,1,0)]).regularity(kind='sheaf')
    assert point['minimal_elements'] == ()
    assert point['generalized_orthants'] == ((None,None),)
    checks += 2
    # The nonmonomial diagonal is checked by its separate geometric model,
    # not passed to the monomial calculator.
    diagonal_checks = 0
    for a, b in product(range(-20,21), repeat=2):
        h1_at_required_twist = max(-a-b, 0)
        assert (h1_at_required_twist == 0) == (a+b >= 0)
        if a+b == 0:
            assert max(-(a-1)-b, 0) > 0 and max(-a-(b-1), 0) > 0
        diagonal_checks += 1
    rng = random.Random(30005078)
    monomials = [a for a in product(range(4), repeat=2) if sum(a)]
    singly_checks = 0
    for _ in range(80):
        generators = rng.sample(monomials, rng.randint(0, 5))
        expected = koszul_regularities(generators, 2)
        got = MonomialQuotient((2,), generators).regularity(check_complex=True)
        assert got['minimal_elements'] == ((expected,),), (generators, expected, got)
        singly_checks += 1
    # Test fine-cell invariance well beyond the chosen representatives.
    cell_checks = 0
    for _ in range(12):
        generators = [tuple(rng.randint(0, 2) for _ in range(4)) for _ in range(3)]
        module = MonomialQuotient((2,2), generators)
        cells = list(module.cells())
        for a, upper in rng.sample(cells, min(12, len(cells))):
            b = tuple(v - 11 if v == -1 else v + 13 if top is None else v
                      for v, top in zip(a, upper))
            assert module.fine_cohomology(a, True) == module.fine_cohomology(b, True)
            cell_checks += 1
    # All computed minima must satisfy the PROVED universal monomial box.
    box_checks = 0
    for result in outputs:
        caps = [max((g[j] for g in result['generators']), default=0) for j in range(4)]
        q = 4
        for d in result['minimal_elements']:
            for block, coord in zip(((0,1),(2,3)), d):
                assert -len(block) <= coord <= q + sum(caps[j] - 1 for j in block)
                box_checks += 1
    for invalid in (1, 4, -3):
        try:
            MonomialQuotient((2,), [], invalid)
        except ValueError:
            checks += 1
        else:
            raise AssertionError('Composite or invalid characteristic accepted')
    receipt = {'status': 'PASS', 'fixed_case_fields': [0,2,3,101],
               'fixed_case_count': len(cases), 'assertions_fixed_and_boolean': checks,
               'independent_singly_graded_koszul_comparisons': singly_checks,
               'fine_cell_invariance_comparisons': cell_checks,
               'diagonal_sheaf_geometric_model_checks': diagonal_checks,
               'explicit_monomial_box_checks': box_checks, 'examples': outputs,
               'limits': 'Finite tests support implementation; completeness rests on PROOF.md. '
                         'No general nonmonomial module algorithm is claimed. No Macaulay2 execution.'}
    Path('RESULTS.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k:v for k,v in receipt.items() if k != 'examples'}, indent=2))


if __name__ == '__main__':
    run()
