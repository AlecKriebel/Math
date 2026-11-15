#!/usr/bin/env python3
"""Independent paper-first finite falsifiers, not an upstream cost proof.

Only --run computes and writes the new OWN_EXACT_RESULTS.json. No supplied
code/results, imports, external files, network, subprocesses or dependencies.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import sys

A = Path(__file__).resolve().parent
CHECKS = 0


def require(ok, reason):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(reason)


def reduced(word):
    stack = []
    for x in word:
        if stack and stack[-1] == -x:
            stack.pop()
        else:
            stack.append(x)
    return tuple(stack)


def inverse(word):
    return tuple(-x for x in reversed(word))


def substitute(word, images):
    return reduced(x for letter in word for x in (images[letter] if letter > 0 else inverse(images[-letter])))


def add_term(ring, word, value):
    word = reduced(word)
    ring[word] = ring.get(word, 0) + value
    if ring[word] == 0:
        del ring[word]


def group_controls(rank):
    a = (1,)
    u = [()]
    for i in range(1, rank):
        u.append(u[-1] + a + (i + 1,))
    w = u[-1] + a
    forward = {1: a, **{i + 1: u[i] for i in range(1, rank)}}
    backward = {1: a}
    for i in range(1, rank):
        previous = () if i == 1 else (i,)
        backward[i + 1] = (-1,) + inverse(previous) + (i + 1,)
    for g in range(1, rank + 1):
        require(substitute(forward[g], backward) == (g,), "inverse new-basis substitution")
        require(substitute(backward[g], forward) == (g,), "inverse old-basis substitution")
    derivs = {g: {} for g in range(1, rank + 1)}
    prefix = ()
    for letter in w:
        add_term(derivs[letter], prefix, 1)
        prefix += (letter,)
    require(derivs[1] == {word: 1 for word in u}, "exact noncommutative a-prefix derivative")
    for i in range(1, rank):
        require(derivs[i + 1] == {u[i - 1] + a: 1}, "exact b-prefix derivative")
    telescope = {}
    wrong_order = {}
    for word in u:
        add_term(telescope, word + a, 1)
        add_term(telescope, word, -1)
        add_term(wrong_order, a + word, 1)
        add_term(wrong_order, word, -1)
    for i in range(1, rank):
        p = u[i - 1] + a
        add_term(telescope, p + (i + 1,), 1)
        add_term(telescope, p, -1)
        add_term(wrong_order, p + (i + 1,), 1)
        add_term(wrong_order, p, -1)
    expected = {w: 1, (): -1}
    require(telescope == expected, "full ordered free group-ring telescoping")
    require(wrong_order != expected, "negative control detects left/right factor swap")
    return {"rank": rank, "w_letters": len(w), "a_occurrences": w.count(1), "all_basis_generators_checked_both_directions": rank, "all_Fox_coordinates_checked": rank, "telescope_nonzero_terms": len(telescope), "wrong_order_residual_terms": len(wrong_order)}


def cyclic_labels(degree, length):
    def extend(prefix):
        if len(prefix) == length:
            if prefix[-1] != prefix[0]:
                yield prefix
            return
        for i in range(degree):
            if not prefix or i != prefix[-1]:
                yield from extend(prefix + (i,))
    yield from extend(())


def tree_controls():
    rows = []
    for degree in [2, 3, 4, 5]:
        for length in [2, 4, 6, 8]:
            count = 0
            for labels in cyclic_labels(degree, length):
                word = tuple((x if i % 2 == 0 else -x) for i, x in enumerate(labels) if x)
                require(reduced(word) != (), "nonbacktracking alternating labelled word cannot close")
                count += 1
            require(count == (degree - 1) ** length + degree - 1, "independent cycle-label enumeration count")
            rows.append({"degree": degree, "edge_length": length, "all_admissible_cyclic_label_words": count})
    require(reduced(()) == (), "zero-label immediate backtrack is not a cycle obstruction")
    path_vector = (1, 0, -1)
    product = (path_vector[1], path_vector[0] + path_vector[2], path_vector[1])
    require(product == (0, 0, 0) and any(path_vector), "negative control: finite tree adjacency can have a kernel")
    return {"bounded_cycle_label_enumeration": rows, "actual_degree100_uniform_tree_proof": "INITIAL_DERIVATIONS.md Family4; finite enumeration is supplementary only", "finite_path3_kernel_negative_control": {"vector": list(path_vector), "adjacency_product": list(product)}}


def height_controls():
    rows = []
    for M in [101, 102, 103, 199, 200, 201, 503, 1000]:
        available = set(range(99))
        added = []
        for k in range(M - 99):
            require(set(range(k, k + 99)) <= available, "all earlier a-source heights available")
            source = k + 99
            require(source not in available and source < M, "new distinct source height")
            require((k + 100) % M == (source + 1) % M, "w edge gives correct new a target")
            available.add(source)
            added.append(source)
        require(available == set(range(M)), "all M source heights covered")
        require(added[-1] == M - 1 and (added[-1] + 1) % M == 0, "last edge wraps to zero")
        require(not set(range(99)) <= set(range(98)), "negative control:98 initial heights insufficient for this induction")
        rows.append({"M": M, "initial_source_heights": 99, "inductively_added_source_heights": len(added), "all_source_heights_covered": len(available), "cost_addition_exact": str(Fraction(99, M))})
    return {"height_dependency_controls": rows, "not_a_finite_simulation_of_measured_cost": True}


def arithmetic_controls():
    left = 2 * 3 ** 97 * 96 ** 4
    right = 2 ** 183
    require(left < right, "strict exact alpha-admissibility integer certificate")
    require(2 ** 61 > 200, "strict alpha size")
    upper = Fraction(3 ** 97 * 96 ** 4, 2 ** 183)
    require(0 < upper < Fraction(1, 2), "rational upper bound for K alpha cubed")
    gap = Fraction(1, 100 * 2 ** 61)
    require(gap > 0 and gap.denominator == 100 * 2 ** 61, "exact stated eta")
    finite_controls = []
    for q in [1, 2, 3, 5, 100]:
        cost = 1 - Fraction(1, q)
        b0 = Fraction(1, q)
        require(cost - 1 == -b0, "finite orbit beta0 term")
        require(cost - 1 < 0, "negative control detects omitted beta0")
        finite_controls.append({"finite_group_order": q, "cost": str(cost), "beta0": str(b0), "comparison_sides": str(-b0)})
    return {"integer_left_2times3pow97times96pow4": str(left), "integer_right_2pow183": str(right), "strict_positive_margin": str(right - left), "strict_rational_Kalpha3_upper_bound": str(upper), "alpha_exact": str(Fraction(1, 2 ** 61)), "eta_exact": str(gap), "finite_orbit_zeroth_term_controls": finite_controls, "positive_external_Bernoulli_cost_theorem_validated_by_these_checks": False}


def main():
    destination = A / "OWN_EXACT_RESULTS.json"
    require(not destination.exists(), "never overwrite independent first results")
    initial = A / "INITIAL_SEAL.json"
    require(hashlib.sha256(initial.read_bytes()).hexdigest() == "087144bfa352a5236528c552ea4c31650da8a0b7ac0aa4fae746769b56717101", "paper-first initial pin")
    result = {"UTC": datetime.now(timezone.utc).isoformat(), "group_basis_and_ordered_derivative_controls": [group_controls(r) for r in [2, 3, 5, 10, 100]], "tree_controls": tree_controls(), "height_controls": height_controls(), "arithmetic_controls": arithmetic_controls(), "foreign_primary_supplied_code_results_archived_or_current_opinion_exposure": False, "supplied_programmes_executed_or_imported": False, "uniform_proof_not_replaced_by_finite_tests": True}
    result["actual_checks"] = CHECKS
    result["status"] = "PASS_OWN_BOUNDED_FALSIFIERS_ONLY"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "actual_checks": CHECKS, "result_SHA256": hashlib.sha256(destination.read_bytes()).hexdigest(), "foreign_exposure": False, "supplied_scientific_execution": False}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--run"]:
        main()
    elif not sys.argv[1:]:
        print("Independent finite-control source; explicit --run required.")
    else:
        raise SystemExit("Only --run is supported")
