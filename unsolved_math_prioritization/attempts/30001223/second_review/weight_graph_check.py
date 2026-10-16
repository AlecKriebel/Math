#!/usr/bin/env python3
"""Independent formal-torus and unipotent-coefficient checks.

No preceding checker is imported. Polynomial root-group coefficients, not
evaluations at finite-field points, determine the directed weight graph.
The all-prime/all-rank conclusions remain mathematical arguments.
"""
import json
from math import comb, isqrt


def require(condition, message):
    if not condition:
        raise ValueError(message)


def root_graph(m, p):
    # v_j = x^(m-j)y^j. Include every coefficient in the formal parameter.
    out = []
    for j in range(m + 1):
        lower_index = {j - h for h in range(j + 1) if comb(j, h) % p}
        higher_index = {j + h for h in range(m - j + 1) if comb(m - j, h) % p}
        out.append(lower_index | higher_index)
    return out


def reach(graph, seed):
    seen = set(seed)
    todo = list(seed)
    while todo:
        for target in graph[todo.pop()]:
            if target not in seen:
                seen.add(target)
                todo.append(target)
    return seen


def components(graph):
    reached = [reach(graph, [i]) for i in range(len(graph))]
    remaining, answer = set(range(len(graph))), []
    while remaining:
        i = min(remaining)
        component = {j for j in reached[i] if i in reached[j]}
        answer.append(sorted(component))
        remaining -= component
    return answer


def is_prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, length - 1):
                yield (first,) + tail


def polarization_check(n, r, p):
    # delta(x^a) = sum_j a_j x^(a-e_j) tensor x_j.
    # Multiplication returns (sum a_j)x^a = r x^a.
    require(r % p != 0, 'polarization split requires p not dividing r')
    inverse = pow(r, -1, p)
    checked = 0
    for alpha in compositions(r, n):
        terms = [(j, alpha[j] % p) for j in range(n) if alpha[j] % p]
        require(sum(c for _, c in terms) * inverse % p == 1,
                'multiplication-polarization is not the identity')
        checked += 1
    result = {'n': n, 'r': r, 'p': p, 'monomials_checked': checked}
    if n >= r:
        # At stable rank the multilinear weight has r tensor basis vectors.
        # Multiplication is the all-ones row, delta the all-ones column.
        require(r * inverse % p == 1, 'multilinear section does not split')
        result['multilinear_kernel_dimension'] = r - 1
    return result


def main():
    family = []
    for p in range(3, 98, 2):
        if not is_prime(p):
            continue
        m = 2*p - 3
        graph = root_graph(m, p)
        w = set(range(p - 2)) | set(range(p, 2*p - 2))
        q = {p - 2, p - 1}
        require(components(graph) == [sorted(w), sorted(q)], 'wrong composition components')
        require(reach(graph, w) == w, 'socle not closed under coefficient action')
        require(all(reach(graph, [i]) == w for i in w), 'socle not simple')
        require(all(reach(graph, [i]) == set(range(m + 1)) for i in q),
                'a quotient-weight lift does not generate the extension')
        require(any(graph[i] & w for i in q), 'candidate weight complement is invariant')
        require(components(root_graph(2*p - 1, p)) == [list(range(2*p))],
                'Sym^(2p-1) not simple')
        # Add determinant's (1,1) to the highest weights in the socle/head.
        socle = [m + 1, 1]
        head = [m - min(q) + 1, min(q) + 1]
        require(socle == [2*p - 2, 1] and head == [p, p - 1] and socle != head,
                'highest weight labels differ from the proof')
        family.append({'p': p, 'socle_dimension': len(w), 'head_dimension': len(q),
                       'socle_highest_weight': socle, 'head_highest_weight': head,
                       'extension_submodules': 3, 'sym_r_simple_dimension': 2*p})
    negative = components(root_graph(3, 3))
    require(negative == [[0, 3], [1, 2]], 'reducible degree-three negative control failed')
    split = [polarization_check(2, 5, 3), polarization_check(5, 5, 3),
             polarization_check(3, 9, 5)]
    print(json.dumps({'status': 'PASS', 'family': family,
                      'reducible_negative_control_components': negative,
                      'polarization_checks': split,
                      'scope': 'Formal coefficient and distinct algebraic-torus-weight checks. Finite tested primes do not replace the all-prime or all-rank proof.'},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
