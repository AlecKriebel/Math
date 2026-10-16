"""Fresh exact finite attacks, illustrative rather than PDE certification."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def main():
    # Constant wrong rank-one branch despite an arbitrarily small split.
    c, s = F(5, 13), F(12, 13)
    u = [[c, -s], [s, c]]
    need = lambda ok: None if ok else (_ for _ in ()).throw(ValueError('exact check'))
    need(c*c+s*s == 1)
    branch = mul(mul(u, [[F(1), F(0)], [F(0), F(0)]]), transpose(u))
    difference = [[branch[0][0]-1, branch[0][1]], [branch[1][0], branch[1][1]]]
    need(mul(difference, difference) == [[s*s, 0], [0, s*s]])
    qs = [3, 6, 9, 11]
    forbidden = set()
    for q in qs:
        for m in product(range(1, 14), repeat=3):
            a_squared = F(sum(j*j for j in m), q)
            if 9 < a_squared < 16:
                forbidden.add(a_squared)
    chosen = F(17, 5)
    need(3 < chosen < 4 and chosen*chosen not in forbidden)
    need(all((q*chosen*chosen).denominator != 1 for q in qs))
    tails = []
    for n in range(1, 25):
        end = 2*n+1
        finite = sum((F(1, 2**(j+2)) for j in range(n, end)), F(0))
        rest = F(1, 2**(end+1))
        need(finite+rest == F(1, 2**(n+1)))
        tails.append({'n': n, 'tail': str(finite+rest), 'birth_plus_tail': str(F(1, 2**n)+finite+rest)})
    # theta(t)=3t^2-2t^3 on [0,1]: its derivative energy is 6/5.
    energy = F(36, 3)-F(72, 4)+F(36, 5)
    need(energy == F(6, 5))
    result = {'status': 'PASS_FINITE_EXACT_DIAGNOSTICS_ONLY',
              'wrong_branch_distance': str(s), 'whole_cluster_distance': '0',
              'nonresonance': {'d': 3, 'protected_units_pi2_over4': qs,
                              'width_interval': [3, 4], 'integer_coordinate_bound': 13,
                              'forbidden_squared_widths': len(forbidden), 'chosen': str(chosen)},
              'cutoff_profile_energy_over_radial_factor': str(energy), 'tails': tails,
              'limit': 'No finite calculation here proves capacity, operator limits, apertures or eigenbasis completeness.'}
    (Path(__file__).resolve().parent/'EXACT_CONTROLS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
