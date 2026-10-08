#!/usr/bin/env python3
"""Independent exact dual-number check; does not verify topology theorems."""
import json

class AuditFailure(Exception):
    pass

def require(condition, message):
    if not condition:
        raise AuditFailure(message)

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def neg(a):
    return (-a[0], -a[1])

def mul(a, b):
    return (a[0] * b[0], a[0] * b[1] + a[1] * b[0])

def power(a, n):
    require(type(n) is int and n >= 0, 'invalid exponent')
    out = (1, 0)
    for _ in range(n):
        out = mul(out, a)
    return out

def evaluate(coeffs, node):
    out = (0, 0)
    for coefficient in reversed(coeffs):
        out = add(mul(out, node), coefficient)
    return out

def difference(values):
    return add(add(values[2], neg(values[1])), add(neg(values[1]), values[0]))

def main():
    q = (1, 1)
    require(mul(q, (1, -1)) == (1, 0), 'Laurent inverse')
    require(add(q, (-1, 0)) == (0, 1), 'q-minus-one image')
    require(mul(add(q, (-1, 0)), add(power(q, 2), (-1, 0))) == (0, 0), 'Habiro level-two kernel')
    # Control: level one cannot define the same first-jet map.
    require(add(q, (-1, 0)) != (0, 0), 'level-one negative control')
    nodes = [power(q, n) for n in [1, 2, 3]]
    # All six Z-basis vectors of D[t] of degree at most two.
    # Evaluation and second difference are Z-linear, so this is an exact
    # exhaustive basis identity, rather than random coefficient sampling.
    for j in range(3):
        for basis in [(1, 0), (0, 1)]:
            coeffs = [(0, 0)] * 3
            coeffs[j] = basis
            require(difference([evaluate(coeffs, node) for node in nodes]) == (0, 0), 'universal basis identity')
    for node in nodes:
        product = (1, 0)
        for root in nodes:
            product = mul(product, add(node, neg(root)))
        require(product == (0, 0), 'three-node quotient evaluation')
    term_one = mul(mul(q, add((1, 0), q)), add((1, 0), neg(power(q, 3))))
    require(term_one == (0, -6), 'Poincare first coefficient')
    values = [0, -6, -24]
    residual = values[2] - 2 * values[1] + values[0]
    require(residual == -12 and residual != 0, 'actual contradiction')
    require(values[2] != 2 * values[1], 'false-affine negative control')
    require((-12) - 2 * values[1] + values[0] == 0, 'affine positive control')
    # Rank-dependent rescaling is not a permissible common convention change.
    for common_scale in [-2, -1, 1, 2]:
        require(common_scale * residual != 0, 'uniform parameter-change control')
    no_rank_one = [-n * (n*n - 1) for n in [2, 3, 4]]
    require(no_rank_one[2] - 2 * no_rank_one[1] + no_rank_one[0] == -18, 'rank-one omission control')
    return {'status': 'PASS', 'identity_basis_vectors': 6, 'first_coefficients': values,
            'second_difference': residual, 'rank_2_3_4_second_difference': -18,
            'scope': 'Exact finite algebra; cited topology is established by mathematical/source review.'}

if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, separators=(',', ':')))
