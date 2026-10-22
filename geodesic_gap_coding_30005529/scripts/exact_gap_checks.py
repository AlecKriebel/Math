from fractions import Fraction
import json

def check(D, M):
    roots = sorted(((Fraction(mu, m), m, mu) for m in range(1, M + 1) for mu in range(m) if (mu * mu - D) % m == 0))
    n = len(roots)
    gaps = [roots[(i + 1) % n][0] - roots[i][0] + (i == n - 1) for i in range(n)]
    if not sum(gaps) == 1:
        raise AssertionError('exact check failed')
    out = {'D': D, 'M': M, 'N': n, 'distinct_count': len(set((x[0] for x in roots))), 'zero_gaps': sum((x == 0 for x in gaps)), 'cyclic_gap_sum': str(sum(gaps)), 'roots': [{'x': str(x), 'm': m, 'mu': mu, 'form': [m, -2 * mu, (mu * mu - D) // m]} for x, m, mu in roots], 'gaps': [str(x) for x in gaps], 'horocycle_times_as_coefficient_of_1_over_sqrt_D': [str(M * x) for x in gaps], 'unit_mean_empirical_gaps': [str(n * x) for x in gaps]}
    for x, m, mu in roots:
        if not (-2 * mu) ** 2 - 4 * m * ((mu * mu - D) // m) == 4 * D:
            raise AssertionError('exact check failed')
        if not m <= M:
            raise AssertionError('exact check failed')
    return out
if __name__ == '__main__':
    cases = [check(2, 10), check(3, 10), check(6, 20), check(2, 100), check(3, 100), check(6, 100)]
    with open('exact_gap_results.json', 'w') as f:
        json.dump(cases, f, indent=2)
    print(json.dumps([{k: v for k, v in c.items() if k in ['D', 'M', 'N', 'distinct_count', 'zero_gaps', 'cyclic_gap_sum']} for c in cases], indent=2))
