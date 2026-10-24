#!/usr/bin/env python3
"""Independent, read-only check of the rank-five finite quotient certificate.

No author module is imported. Words use a leading-one binary encoding, row
reduction uses greatest pivots, and the ambient Lie algebra is independently
reconstructed by standard bracketings of Lyndon words.
"""
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "hydra_geometry" / "rank5_lie_certificate.json"
EXPECTED = "7bfdf7d30b708866c271499003af3844e24905e6995eb5ca728f72af49044b56"
raw = INPUT.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED
C = json.loads(raw)
P, CAP = 101, 10
assert (C["prime"], C["class_bound"], C["rank"]) == (P, CAP, 5)
assert all(P % n for n in range(2, 11))


def encode(word):
    return int("1" + word.replace("x", "0").replace("y", "1"), 2)


def degree(word):
    return word.bit_length() - 1


def convert(poly):
    for w, a in poly.items():
        assert 1 <= len(w) <= CAP and set(w) <= set("xy")
        assert type(a) is int and 1 <= a < P
    return {encode(w): a for w, a in poly.items()}


def combine(*terms):
    result = {}
    for scalar, poly in terms:
        for w, a in poly.items():
            v = (result.get(w, 0) + scalar * a) % P
            if v:
                result[w] = v
            else:
                result.pop(w, None)
    return result


def multiply(a, b):
    result = {}
    blocks = [[] for _ in range(CAP + 1)]
    for w, bw in b.items():
        blocks[degree(w)].append((w, bw))
    for v, av in a.items():
        for dw in range(CAP - degree(v) + 1):
            for w, bw in blocks[dw]:
                vw = (v << dw) + w - (1 << dw)
                result[vw] = (result.get(vw, 0) + av * bw) % P
    return {w: a for w, a in result.items() if a}


def commutator(a, b):
    return combine((1, multiply(a, b)), (-1, multiply(b, a)))


UNIT = {1: 1}


def series(a, coefficients):
    result, power = {}, UNIT
    for coefficient in coefficients:
        result = combine((1, result), (coefficient, power))
        power = multiply(power, a)
    return result


factorial = 1
EXP = [1]
for n in range(1, CAP + 1):
    factorial = factorial * n % P
    EXP.append(pow(factorial, -1, P))
LOG = [0] + [pow(n, -1, P) * (-1) ** (n + 1) % P for n in range(1, CAP + 1)]


def exp(a):
    return series(a, EXP)


def log(a):
    return series(combine((1, a), (-1, UNIT)), LOG)


def inv(a):
    return series(combine((1, a), (-1, UNIT)), [(-1) ** n for n in range(CAP + 1)])


def power(a, exponent):
    result = UNIT
    while exponent:
        if exponent & 1:
            result = multiply(result, a)
        a = multiply(a, a)
        exponent >>= 1
    return result


class Span:
    def __init__(self, vectors=()):
        self.rows = {}
        for v in vectors:
            assert self.insert(v), "Dependent purported certificate basis"

    def reduce(self, vector):
        vector = dict(vector)
        for pivot in sorted(self.rows, reverse=True):
            if pivot in vector:
                vector = combine((1, vector), (-vector[pivot], self.rows[pivot]))
        return vector

    def insert(self, vector):
        residual = self.reduce(vector)
        if not residual:
            return False
        pivot = max(residual)
        self.rows[pivot] = combine((pow(residual[pivot], -1, P), residual))
        return True

    def includes(self, vector):
        return not self.reduce(vector)


def minimum_degree(vector):
    return min(map(degree, vector), default=CAP + 1)


def bracket_checks(left, right, space, antisymmetric=False):
    count = 0
    nonzero = 0
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if antisymmetric and j <= i:
                continue
            if minimum_degree(a) + minimum_degree(b) > CAP:
                continue
            value = commutator(a, b)
            assert space.includes(value), (i, j, "Bracket closure failed")
            count += 1
            nonzero += bool(value)
    return {"pairs_checked": count, "nonzero": nonzero}


def lyndon(w):
    return all(w < w[i:] for i in range(1, len(w)))


@lru_cache(None)
def lyndon_bracket(w):
    if len(w) == 1:
        return {encode(w): 1}
    split = next(i for i in range(1, len(w)) if lyndon(w[i:]))
    assert lyndon(w[:split])
    return commutator(lyndon_bracket(w[:split]), lyndon_bracket(w[split:]))


def generated_closure(initial, acting_generators):
    space, queue = Span(), []
    for v in initial:
        if space.insert(v):
            queue.append(v)
    for v in queue:
        for g in acting_generators:
            w = commutator(g, v)
            if space.insert(w):
                queue.append(w)
    return space


def same_space(a, b):
    assert len(a.rows) == len(b.rows)
    assert all(a.includes(v) for v in b.rows.values())


def main():
    start = time.monotonic()
    rows = {key: [convert(v) for v in C[key]] for key in ("R_basis", "ideal_basis", "W_basis")}
    R, I, W = (Span(rows[k]) for k in ("R_basis", "ideal_basis", "W_basis"))
    assert (len(R.rows), len(I.rows), len(W.rows)) == (226, 31, 88)
    assert all(R.includes(v) for v in rows["ideal_basis"] + rows["W_basis"])
    assert all(W.includes(v) for v in rows["ideal_basis"])

    counts = []
    lyndon_rows = []
    for n in range(1, CAP + 1):
        words = ["".join(w) for w in itertools.product("xy", repeat=n) if lyndon("".join(w))]
        counts.append(len(words))
        lyndon_rows.extend(lyndon_bracket(w) for w in words)
    assert counts == [2, 1, 2, 3, 6, 9, 18, 30, 56, 99]
    generated_R = Span(lyndon_rows)
    same_space(R, generated_R)
    print("Independent ambient reconstruction passed.", flush=True)
    checks = {
        "R_Lie_closed": bracket_checks(lyndon_rows, lyndon_rows, R, True),
        "I_is_Lie_ideal": bracket_checks(lyndon_rows, rows["ideal_basis"], I),
        "W_is_Lie_subalgebra": bracket_checks(rows["W_basis"], rows["W_basis"], W, True),
    }

    X, Y = {encode("x"): 1}, {encode("y"): 1}
    s, top = exp(X), exp(Y)
    assert log(s) == X and log(top) == Y
    alpha = [None] * 6
    alpha[5] = top
    for i in range(5, 1, -1):
        alpha[i - 1] = multiply(multiply(inv(alpha[i]), s), alpha[i])
    logs = [log(a) for a in alpha[1:]]
    assert logs == [convert(v) for v in C["alpha_logs"]]
    assert all(R.includes(v) for v in logs)
    assert all(exp(log(a)) == a for a in alpha[1:] + [s])

    rel = log(multiply(multiply(multiply(inv(s), inv(alpha[1])), s), alpha[1]))
    assert rel == convert(C["relator_log"]) and I.includes(rel)
    generated_I = generated_closure([rel], [X, Y])
    same_space(I, generated_I)
    for i in range(2, 6):
        # All recursive Hydra relations hold before the final Lie quotient.
        assert multiply(multiply(inv(alpha[i]), s), alpha[i]) == alpha[i - 1]
    assert not multiply(inv(s), multiply(inv(alpha[1]), multiply(s, alpha[1]))) == UNIT

    L_logs = [logs[0]] + [log(multiply(multiply(a, s), inv(a))) for a in alpha[2:]]
    assert L_logs == [convert(v) for v in C["L_generator_logs"]]
    assert all(W.includes(v) for v in L_logs)
    generated_W = generated_closure(rows["ideal_basis"] + L_logs, rows["ideal_basis"] + L_logs)
    same_space(W, generated_W)
    print("All Lie spaces, relators, and generated closures passed.", flush=True)

    dual_checks = []
    for record in C["dual_separation_certificates"]:
        index = record["alpha_index"]
        assert 2 <= index <= 5
        dual = convert(record["functional"])
        evaluate = lambda v: sum(c * dual.get(w, 0) for w, c in v.items()) % P
        assert all(evaluate(v) == 0 for v in rows["W_basis"])
        value = evaluate(logs[index - 1])
        assert value == record["nonzero_value"] and value != 0
        assert not W.includes(logs[index - 1])
        dual_checks.append({"alpha_index": index, "value": value, "support_size": len(dual)})
    assert sorted(r["alpha_index"] for r in dual_checks) == [2, 3, 4, 5]

    slp_path = INPUT.with_name("rank5_s_membership_slp.json")
    slp_raw = slp_path.read_bytes()
    slp_hash = "d6f43db01906e8f3fd96acebec1ab55a8103712e2a2da010a8c0637e2640a6d4"
    assert hashlib.sha256(slp_raw).hexdigest() == slp_hash
    S = json.loads(slp_raw)
    assert (S["prime"], S["class"]) == (P, CAP)
    values, shapes = [], []
    seed_counts = {}
    for n, instruction in enumerate(S["proof_nodes"]):
        op = instruction["op"]
        if op == "seed":
            kind, j = instruction["kind"], instruction["index"]
            assert type(j) is int and j >= 0
            seed_counts[kind] = seed_counts.get(kind, 0) + 1
            if kind == "s":
                assert j == 0
                value, shape = s, "H_times_s"
            elif kind == "ideal_exponential":
                assert j < len(rows["ideal_basis"])
                value, shape = exp(rows["ideal_basis"][j]), "H"
            elif kind == "L_generator_exponential":
                assert j < len(L_logs)
                value, shape = exp(L_logs[j]), "H"
            else:
                raise AssertionError("Unknown seed")
        elif op == "pow":
            a, exponent = instruction["arg"], instruction["exponent"]
            assert type(a) is int and 0 <= a < n and shapes[a] == "H"
            assert type(exponent) is int and 0 <= exponent < P
            value, shape = power(values[a], exponent), "H"
        elif op == "multiply":
            a, b = instruction["left"], instruction["right"]
            assert type(a) is int and type(b) is int and 0 <= a < n and 0 <= b < n
            assert shapes[a] == "H" and shapes[b] in ("H", "H_times_s")
            value, shape = multiply(values[a], values[b]), shapes[b]
        else:
            raise AssertionError("Unknown SLP instruction")
        values.append(value)
        shapes.append(shape)
    assert S["identity_node"] == len(values) - 1 == 191
    assert seed_counts.get("s") == 1
    assert shapes[-1] == "H_times_s" and values[-1] == UNIT
    print("Independent 192-node group identity passed.", flush=True)

    # Sample group multiplication/normality checks supplement, rather than
    # replace, the Lie-ideal proof and BCH theorem in the accompanying audit.
    samples = [X, Y, combine((7, X), (13, Y))] + logs
    for a in samples:
        for b in samples:
            product = multiply(exp(a), exp(b))
            assert R.includes(log(product)) and exp(log(product)) == product
    normality_checks = 0
    for a in (X, Y):
        ea = exp(a)
        for v in rows["ideal_basis"]:
            conjugate = log(multiply(multiply(inv(ea), exp(v)), ea))
            assert I.includes(conjugate)
            normality_checks += 1

    result = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_EXACT_CERTIFICATE_PARTIAL_SCOPE",
        "certificate_sha256": EXPECTED,
        "membership_slp_sha256": slp_hash,
        "independent_implementation": "Integer word encoding, greatest-pivot elimination, Lyndon reconstruction; imports no author code",
        "dimensions": {"R": 226, "I": 31, "W": 88, "R_over_I": 195, "W_over_I": 57},
        "Lyndon_dimensions_by_degree": counts,
        "closure_checks": checks,
        "ideal_regeneration_from_relator": True,
        "W_regeneration_from_I_and_L": True,
        "dual_separations": dual_checks,
        "group_product_samples": len(samples) ** 2,
        "normality_samples": normality_checks,
        "membership_slp": {"nodes": len(values), "seed_counts": seed_counts, "identity": "h*s=1", "exact_unit_equality": True, "q_s_in_q_L5": True},
        "quotient_group_order": "101^195",
        "full_problem_solved": False,
        "interosculation": "Exact SLP and independent geometric argument prove inter-osculation; this cover is not special",
        "elapsed_seconds": time.monotonic() - start,
    }
    (HERE / "INDEPENDENT_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
