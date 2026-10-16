"""Independent finite adversarial checks; mathematical proof is in the comparison.

Run with PYTHONDONTWRITEBYTECODE=1. Uses only the Python standard library.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from pathlib import Path
import datetime
import json


def loopless_matroid_ranks(n):
    """Enumerate independent-set systems, check axioms, then compute all ranks."""
    subsets = list(range(1 << n))
    required = {0} | {1 << i for i in range(n)}
    optional = [s for s in subsets if s not in required]
    for bits in range(1 << len(optional)):
        independent = required | {
            s for j, s in enumerate(optional) if bits & (1 << j)
        }
        if any((s ^ (1 << i)) not in independent
               for s in independent for i in range(n) if s & (1 << i)):
            continue
        if any(not any((a | (1 << i)) in independent
                       for i in range(n) if (b & ~a) & (1 << i))
               for a in independent for b in independent
               if a.bit_count() < b.bit_count()):
            continue
        yield [max(i.bit_count() for i in independent if i & ~s == 0)
               for s in subsets]


def comparison_factor(rank, values):
    return max(max(Q(rank[s]) / values[s.bit_count()],
                   values[s.bit_count()] / rank[s])
               for s in range(1, len(rank)))


def main():
    results = {"run_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "matroid_enumeration": [], "failures": [],
               "arithmetic": "exact rational; 80-digit decimal for square-root submodularity"}
    cardinality_checks = 0
    with localcontext() as ctx:
        ctx.prec = 80
        sq = [Decimal(k).sqrt() for k in range(65)]
        tolerance = Decimal('1e-75')
        for t in range(65):
            for a in range(65 - t):
                for c in range(65 - t - a):
                    gap = sq[t+a] + sq[t+c] - sq[t+a+c] - sq[t]
                    assert gap >= -tolerance, (t, a, c, str(gap))
                    cardinality_checks += 1
    results["square_root_submodularity_cardinality_cases"] = cardinality_checks
    rational_checks = 0
    for m in range(1, 17):
        n = m*m
        vals = [Q(0)] + [1+Q(k-1, m) for k in range(1, n+1)]
        assert vals[1] == 1
        increments = [vals[k+1]-vals[k] for k in range(n)]
        assert all(x >= 0 for x in increments)
        assert all(a >= b for a,b in zip(increments, increments[1:]))
        for R in range(1, n+1):
            alpha = max(Q(R)/vals[R], vals[n]/R)
            assert alpha >= 1 and alpha*alpha+alpha >= m
            assert 2*alpha*alpha >= m
            rational_checks += 1
    results["rational_rank_boundary_cases"] = rational_checks
    for n in range(1,5):
        ranks = list(loopless_matroid_ranks(n))
        expected_square = min(max(Q(R),Q(n,R*R)) for R in range(1,n+1))
        observed_square = min(max(max(Q(rank[s]**2,s.bit_count()),
                                       Q(s.bit_count(),rank[s]**2))
                                   for s in range(1,1<<n)) for rank in ranks)
        assert observed_square == expected_square
        concave_profiles = 0
        for slopes_ascending in combinations_with_replacement(
                [Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)],n-1):
            slopes = [Q(1)] + list(reversed(slopes_ascending))
            values = [Q(0)]
            for x in slopes:
                values.append(values[-1]+x)
            for A,B in product(range(1<<n),repeat=2):
                assert values[A.bit_count()]+values[B.bit_count()] >= (
                    values[(A|B).bit_count()]+values[(A&B).bit_count()])
            expected = min(max(Q(R)/values[R],values[n]/R)
                           for R in range(1,n+1))
            observed = min(comparison_factor(rank,values) for rank in ranks)
            assert observed == expected
            concave_profiles += 1
        results["matroid_enumeration"].append({
            "n":n,"loopless_matroids":len(ranks),
            "all_independent_set_systems_tested":1<<((1<<n)-n-1),
            "square_root_optimal_factor_squared":str(observed_square),
            "concave_profiles_tested":concave_profiles,
            "all_compared_against_uniform_optimum":True})
    results["passed"] = True
    results["limitations"] = (
        "Finite checks corroborate but do not establish the universal proof. "
        "Matroid enumeration is exhaustive only through n=4; the square-root "
        "inequality check uses finite-precision decimal with stated tolerance. "
        "The exact rational checks use no floating-point comparisons.")
    output = Path(__file__).with_name('VALIDATION_RESULTS.json')
    output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
