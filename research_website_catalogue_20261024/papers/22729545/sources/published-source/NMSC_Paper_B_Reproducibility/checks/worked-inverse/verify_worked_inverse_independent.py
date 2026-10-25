#!/usr/bin/env python3
"""Exact raw-event calculation for Example ex:worked-inverse.

No paper implementation, fixture or generator is imported. Finite symbolic
expressions are rational sums of exp(A*t+B*u+C); times/rates here are rational.
"""
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

if not __debug__:
    raise SystemExit("Run without -O: exact identity assertions must be enabled.")

ZERO = (F(0), F(0), F(0))
T = (F(1), F(0), F(0))
U = (F(0), F(1), F(0))


def fixed(n):
    return (F(0), F(0), F(n))


def linear_add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def linear_scale(x, y):
    return tuple(F(y) * a for a in x)


def exp_term(coefficient=1, exponent=ZERO):
    return {} if coefficient == 0 else {tuple(exponent): F(coefficient)}


def add(*expressions):
    result = defaultdict(F)
    for expression in expressions:
        for exponent, coefficient in expression.items():
            result[exponent] += coefficient
    return {e: c for e, c in result.items() if c}


def multiply(x, y):
    return add(*(exp_term(a * b, linear_add(e, f))
                 for e, a in x.items() for f, b in y.items()))


def scale(x, c):
    return {e: a * c for e, a in x.items() if a * c}


def derivative_t(x):
    return {e: a * e[0] for e, a in x.items() if e[0]}


def encode(x):
    return [{"coefficient": str(c), "exponent_t_u_constant": [str(v) for v in e]}
            for e, c in sorted(x.items())]


def canonical(blocks):
    return tuple(sorted((tuple(sorted(labels)), edge) for labels, edge in blocks))


class RawProcess:
    def __init__(self, manifest):
        self.m = manifest
        self.arcs = [tuple(a) for a in manifest["arcs"]]
        self.parents = defaultdict(list)
        self.children = defaultdict(list)
        for parent, child in self.arcs:
            self.parents[child].append(parent)
            self.children[parent].append(child)

    def rate(self, edge):
        return F(self.m["rate_overrides"].get(edge, self.m["default_rate"]))

    def initial(self, labels):
        return {canonical([((s,), self.parents[s][0] + ">" + s) for s in labels]): exp_term()}

    def flow(self, states, start, end):
        result = {}
        duration = linear_add(end, linear_scale(start, -1))
        for state, weight in states.items():
            total = sum(self.rate(edge1) for i, (labels1, edge1) in enumerate(state)
                        for labels2, edge2 in state[i + 1:] if edge1 == edge2)
            result[state] = multiply(weight, exp_term(1, linear_scale(duration, -total)))
        return result

    def boundary(self, states, vertex):
        result = {}
        for state, weight in states.items():
            choices = []
            for labels, edge in state:
                if edge.split(">")[0] != vertex:
                    choices.append([(labels, edge, F(1))])
                elif vertex == self.m["reticulation"]:
                    choices.append([(labels, parent + ">" + vertex, F(*p))
                                    for parent, p in self.m["routing"].items()])
                else:
                    target = "ROOT" if vertex == self.m["root"] else self.parents[vertex][0] + ">" + vertex
                    choices.append([(labels, target, F(1))])
            for assignment in itertools.product(*choices):
                coefficient = F(1)
                for labels, edge, p in assignment:
                    coefficient *= p
                key = canonical([(labels, edge) for labels, edge, p in assignment])
                result[key] = add(result.get(key, {}), scale(weight, coefficient))
        return result

    def mark(self, states, left, right):
        result = {}
        left, right = tuple(sorted(left)), tuple(sorted(right))
        for state, weight in states.items():
            positions = {labels: (i, edge) for i, (labels, edge) in enumerate(state)}
            if left not in positions or right not in positions:
                continue
            i, edge1 = positions[left]
            j, edge2 = positions[right]
            if edge1 != edge2:
                continue
            key = canonical([(labels, edge) for k, (labels, edge) in enumerate(state)
                             if k not in (i, j)] + [(left + right, edge1)])
            result[key] = add(result.get(key, {}), scale(weight, self.rate(edge1)))
        return result

    def through(self, labels, vertices):
        states, previous = self.initial(labels), fixed(0)
        for vertex in vertices:
            at = fixed(self.m["ages"][vertex])
            states = self.boundary(self.flow(states, previous, at), vertex)
            previous = at
        return states, previous


def mass(states, predicate=lambda state: True):
    return add(*(weight for state, weight in states.items() if predicate(state)))


def occupied(state, left, right):
    places = {labels: edge for labels, edge in state}
    return places[tuple(left)] == places[tuple(right)]


def main():
    base = Path(__file__).resolve().parent
    source = base / "worked_inverse_manifest.json"
    m = json.loads(source.read_text())
    p = RawProcess(m)
    checks = []

    def equal(name, actual, expected):
        assert actual == expected, (name, encode(actual), encode(expected))
        checks.append({"identity": name, "expression": encode(actual)})

    ages = m["ages"]
    assert all(ages[parent] > ages[child] for parent, child in p.arcs)
    internal = [v for v in ages if p.children[v]]
    assert len({ages[v] for v in internal}) == len(internal)
    for parent in p.parents[m["reticulation"]]:
        incident = [a for a in p.arcs if parent in a]
        ordinary = [a for a in incident if a[1] != m["reticulation"]]
        assert len(ordinary) == 2

    pair, start = p.through(["a", "b"], ["V"])
    pair_pre_h = p.flow(pair, start, fixed(2))
    equal("child_pair_mass", mass(pair_pre_h), exp_term(1, fixed(-1)))
    triple, start = p.through(["a", "b", "z"], ["V"])
    triple_pre_h = p.flow(triple, start, fixed(2))
    q3 = mass(triple_pre_h, lambda s: occupied(s, ["a"], ["b"]) and not occupied(s, ["a"], ["z"]))
    equal("own_triple_grouping_mass", q3, exp_term(1, fixed(-1)))

    pair_h = p.boundary(pair_pre_h, "H")
    pair_short = p.flow(pair_h, fixed(2), T)
    raw_f = mass(p.mark(pair_short, ["a"], ["b"]))
    expected_f = add(exp_term(F(1, 9), (-F(1), F(0), F(1))),
                     exp_term(F(8, 9), (-F(2), F(0), F(3))))
    equal("actual_pair_density_below_earlier_parent", raw_f, expected_f)

    triple_h = p.boundary(triple_pre_h, "H")
    first = p.mark(p.flow(triple_h, fixed(2), T), ["a"], ["b"])
    at_t_parent = p.boundary(p.flow(first, T, fixed(3)), "T")
    second_time = linear_add(fixed(3), U)
    second = p.mark(p.flow(at_t_parent, fixed(3), second_time), ["a", "b"], ["z"])
    density = mass(second)
    equal("raw_first_second_merger_density", density,
          exp_term(F(1, 3), (-F(1), -F(3), F(1))))
    u_zero = add(*(exp_term(c, (e[0], F(0), e[2])) for e, c in density.items()))
    g1 = exp_term(1, (-F(1), F(0), F(2)))
    equal("diagnostic_limit_recovers_g1", u_zero, multiply(exp_term(F(1, 3), fixed(-1)), g1))
    g2 = exp_term(2, (-F(2), F(0), F(4)))
    equal("scalar_pair_subtraction_recovers_g2", raw_f,
          multiply(exp_term(1, fixed(-1)), add(scale(g1, F(1, 9)), scale(g2, F(4, 9)))))

    az, start = p.through(["a", "z"], ["V", "H", "T"])
    equal("oriented_inheritance_at_parent", mass(az, lambda s: occupied(s, ["a"], ["z"])), exp_term(F(1, 3)))
    az_long = p.flow(az, start, T)
    az_q = mass(az_long, lambda s: occupied(s, ["a"], ["z"]))
    az_f = mass(p.mark(az_long, ["a"], ["z"]))
    equal("ordinary_rate_ratio", az_f, scale(az_q, 3))

    pair_at_3 = p.boundary(p.flow(pair_h, fixed(2), fixed(3)), "T")
    pair_long = p.flow(pair_at_3, fixed(3), T)
    q1 = mass(pair_long, lambda s: all(edge == "U>T" for labels, edge in s))
    q2 = mass(pair_long, lambda s: all(edge == "U>H" for labels, edge in s))
    raw_q = mass(pair_long, lambda s: occupied(s, ["a"], ["b"]))
    equal("known_first_route_propagation", q1, exp_term(F(1, 9), (-F(3), F(0), F(7))))
    equal("longer_isolated_arm_mass", q2, exp_term(F(4, 9), (-F(2), F(0), F(3))))
    equal("actual_pair_cooccupancy_decomposition", raw_q, add(q1, q2))
    equal("longer_arm_logarithmic_hazard", derivative_t(q2), scale(q2, -2))
    assert all(c > 0 for c in q2.values())

    # The same state computation must reject substantive wrong formulas.
    negative_controls = {
        "gamma_instead_of_gamma_squared": scale(density, 3),
        "missing_ordinary_rate_factor": scale(density, F(1, 3)),
        "wrong_longer_rate": exp_term(F(4, 9), (-F(1), F(0), F(1))),
        "omitted_first_route_survival": exp_term(F(1, 9), (-F(3), F(0), F(8))),
    }
    assert negative_controls["gamma_instead_of_gamma_squared"] != density
    assert negative_controls["missing_ordinary_rate_factor"] != density
    assert negative_controls["wrong_longer_rate"] != q2
    assert negative_controls["omitted_first_route_survival"] != q1
    result = {"status": "PASS", "manifest_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "exact_symbolic_identities": len(checks), "identities": checks,
              "negative_controls_rejected": sorted(negative_controls),
              "scope": "raw-event symbolic verification of one worked graph; not universal network enumeration"}
    (base / "worked_inverse_independent_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "identities"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
