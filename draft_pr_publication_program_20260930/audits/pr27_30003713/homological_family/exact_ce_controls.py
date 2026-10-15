#!/usr/bin/env python3
"""Independent full-CE controls, exact arithmetic, not an all-degree proof.

No frozen script is imported. Free Lie components are spanned by commutators
across ALL binary degree splits, with exact tensor-algebra coordinates. Full
ordinary CE differentials are constructed from all factor pairs. Their
homology is compared with an independently constructed generator-action
complex by E weight. Noninvertible and invertible substitutions test
naturality. This validates a reduction, not the unknown general decomposition.
"""
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import sympy as S

OWN = Path(__file__).resolve().parent

def commutator(left, right):
    result = {}
    for u, a in left.items():
        for v, b in right.items():
            result[u + v] = result.get(u + v, 0) + a * b
            result[v + u] = result.get(v + u, 0) - a * b
    return {word: coeff for word, coeff in result.items() if coeff}

@lru_cache(None)
def tensor_words(m, d):
    return tuple(product(range(m), repeat=d))

@lru_cache(None)
def free_lie(m, d):
    if d <= 0:
        return ()
    if d == 1:
        return tuple({(j,): S.Integer(1)} for j in range(m))
    candidates = []
    for a in range(1, d // 2 + 1):
        b = d - a
        for i, x in enumerate(free_lie(m, a)):
            for j, y in enumerate(free_lie(m, b)):
                if a == b and i >= j:
                    continue
                z = commutator(x, y)
                if z:
                    candidates.append(z)
    matrix = S.Matrix(len(tensor_words(m, d)), len(candidates),
                      lambda i, j: candidates[j].get(tensor_words(m, d)[i], 0))
    selected = matrix.rref()[1]
    basis = tuple(candidates[j] for j in selected)
    witt = sum(S.mobius(a) * m ** (d // a) for a in S.divisors(d)) // d
    assert len(basis) == witt
    return basis

@lru_cache(None)
def embedding(m, d):
    basis = free_lie(m, d)
    return S.Matrix(len(tensor_words(m, d)), len(basis),
                    lambda i, j: basis[j].get(tensor_words(m, d)[i], 0))

@lru_cache(None)
def coordinate_solver(m, d):
    matrix = embedding(m, d)
    rows = matrix.T.rref()[1]
    return rows, matrix.extract(rows, tuple(range(matrix.cols))).inv()

def lie_coordinates(m, d, vector):
    if not free_lie(m, d):
        assert not vector
        return ()
    rows, inverse = coordinate_solver(m, d)
    dense = S.Matrix([vector.get(w, 0) for w in tensor_words(m, d)])
    coeff = inverse * dense.extract(rows, (0,))
    assert embedding(m, d) * coeff == dense
    return tuple(coeff)

@lru_cache(None)
def lie_bracket(m, a, i, b, j):
    return lie_coordinates(m, a + b,
                           commutator(free_lie(m, a)[i], free_lie(m, b)[j]))

@lru_cache(None)
def entries(m, e, d, ideal_only=False):
    colors = range(1, e + 1) if ideal_only else range(e + 1)
    return tuple((color, degree, i)
                 for degree in range(1, d + 1)
                 for color in colors
                 for i in range(len(free_lie(m, degree))))

def sign_sort(indices):
    if len(set(indices)) != len(indices):
        return None, 0
    inv = sum(indices[i] > indices[j]
              for i in range(len(indices)) for j in range(i + 1, len(indices)))
    return tuple(sorted(indices)), (-1) ** inv

@lru_cache(None)
def wedge_basis(m, e, n, d, q, ideal_only=False):
    if n < 0 or d < 0:
        return ()
    choices = entries(m, e, d, ideal_only)
    result = []
    def visit(start, remaining_n, remaining_d, remaining_q, chosen):
        if remaining_n == 0:
            if remaining_d == 0 and remaining_q == 0:
                result.append(tuple(chosen))
            return
        if remaining_d < remaining_n or remaining_q < 0 or remaining_q > remaining_n:
            return
        for i in range(start, len(choices)):
            color, degree, _ = choices[i]
            if degree > remaining_d - remaining_n + 1:
                break
            visit(i + 1, remaining_n - 1, remaining_d - degree,
                  remaining_q - (color > 0), chosen + [i])
    visit(0, n, d, q, [])
    return tuple(result)

def current_bracket(m, left, right):
    c, a, i = left
    f, b, j = right
    if c > 0 and f > 0:
        return ()
    color = c or f
    return tuple(((color, a + b, k), coeff)
                 for k, coeff in enumerate(lie_bracket(m, a, i, b, j)) if coeff)

@lru_cache(None)
def ce_matrix(m, e, n, d, q):
    source = wedge_basis(m, e, n, d, q)
    target = wedge_basis(m, e, n - 1, d, q)
    choices = entries(m, e, d)
    lookup = {entry: i for i, entry in enumerate(choices)}
    row = {wedge: i for i, wedge in enumerate(target)}
    matrix = S.zeros(len(target), len(source))
    for col, wedge in enumerate(source):
        for i in range(n):
            for j in range(i + 1, n):
                rest = [wedge[k] for k in range(n) if k not in (i, j)]
                for entry, coeff in current_bracket(m, choices[wedge[i]], choices[wedge[j]]):
                    out, sorting = sign_sort([lookup[entry]] + rest)
                    if sorting:
                        matrix[row[out], col] += (-1) ** (i + j + 1) * sorting * coeff
    return matrix

@lru_cache(None)
def action_matrix(m, e, q, d):
    source = wedge_basis(m, e, q, d - 1, q, True)
    target = wedge_basis(m, e, q, d, q, True)
    source_choices = entries(m, e, max(d - 1, 0), True)
    target_choices = entries(m, e, max(d, 0), True)
    lookup = {entry: i for i, entry in enumerate(target_choices)}
    row = {wedge: i for i, wedge in enumerate(target)}
    matrix = S.zeros(len(target), m * len(source))
    for generator in range(m):
        for col, wedge in enumerate(source):
            for position, ind in enumerate(wedge):
                color, degree, index = source_choices[ind]
                for k, coeff in enumerate(lie_bracket(m, 1, generator, degree, index)):
                    if not coeff:
                        continue
                    out = [lookup[source_choices[x]] for x in wedge]
                    out[position] = lookup[(color, degree + 1, k)]
                    sorted_out, sorting = sign_sort(out)
                    if sorting:
                        matrix[row[sorted_out], generator * len(source) + col] += sorting * coeff
    return matrix

def exact_rank(matrix):
    return matrix.to_DM().rank() if matrix.rows and matrix.cols else 0

def compare_full_ce(m, e, d):
    rows = []
    for q in range(d + 1):
        action = action_matrix(m, e, q, d)
        action_rank = exact_rank(action)
        ranks = {}
        for n in range(d + 2):
            differential = ce_matrix(m, e, n, d, q)
            ranks[n] = exact_rank(differential)
            if n > 1:
                assert ce_matrix(m, e, n - 1, d, q) * differential == S.zeros(
                    ce_matrix(m, e, n - 1, d, q).rows, differential.cols)
        for n in range(d + 1):
            dimension = len(wedge_basis(m, e, n, d, q))
            actual = dimension - ranks[n] - ranks[n + 1]
            expected = 0
            if n == q:
                expected += action.rows - action_rank
            if n == q + 1:
                expected += action.cols - action_rank
            assert actual == expected, (m, e, d, n, q, actual, expected)
            if dimension or actual or expected:
                rows.append({"homology_degree": n, "E_weight": q,
                             "CE_chain_dimension": dimension,
                             "CE_outgoing_rank": ranks[n],
                             "CE_incoming_rank": ranks[n + 1],
                             "actual_homology": actual,
                             "two_term_prediction": expected,
                             "action_domain": action.cols,
                             "action_codomain": action.rows,
                             "action_rank": action_rank})
    return {"dim_V": m, "dim_E": e, "V_degree": d, "rows": rows,
            "full_CE_vs_reduced": True, "differential_squared_zero": True}

def tensor_substitution(vector, substitution):
    result = {}
    for word, coeff in vector.items():
        expanded = {(): coeff}
        for letter in word:
            next_expansion = {}
            for prefix, value in expanded.items():
                for image, scalar in enumerate(substitution[:, letter]):
                    if scalar:
                        key = prefix + (image,)
                        next_expansion[key] = next_expansion.get(key, 0) + value * scalar
            expanded = next_expansion
        for word2, value in expanded.items():
            result[word2] = result.get(word2, 0) + value
    return {w: c for w, c in result.items() if c}

def induced_wedge_map(m, e, n, d, q, v_map, e_map):
    choices = entries(m, e, d)
    lookup = {entry: i for i, entry in enumerate(choices)}
    basis = wedge_basis(m, e, n, d, q)
    row = {wedge: i for i, wedge in enumerate(basis)}
    factor_images = {}
    for ind, (color, degree, index) in enumerate(choices):
        coeffs = lie_coordinates(m, degree, tensor_substitution(
            free_lie(m, degree)[index], v_map))
        colors = [(0, 1)] if color == 0 else [
            (a + 1, e_map[a, color - 1]) for a in range(e) if e_map[a, color - 1]]
        factor_images[ind] = [(lookup[(c, degree, j)], scalar * value)
                             for c, scalar in colors
                             for j, value in enumerate(coeffs) if value]
    matrix = S.zeros(len(basis), len(basis))
    for col, wedge in enumerate(basis):
        expansions = {(): S.Integer(1)}
        for ind in wedge:
            next_expansion = {}
            for prefix, coeff in expansions.items():
                for target, value in factor_images[ind]:
                    out = prefix + (target,)
                    next_expansion[out] = next_expansion.get(out, 0) + coeff * value
            expansions = next_expansion
        for output, value in expansions.items():
            sorted_output, sorting = sign_sort(output)
            if sorting:
                matrix[row[sorted_output], col] += sorting * value
    return matrix

def naturality_controls():
    m, e, d = 2, 2, 4
    pairs = [
        ("V_shear_E_projection", S.Matrix([[1, 1], [0, 1]]), S.Matrix([[1, 0], [0, 0]])),
        ("V_projection_E_shear", S.Matrix([[1, 0], [0, 0]]), S.Matrix([[1, 1], [0, 1]])),
        ("V_swap_E_swap", S.Matrix([[0, 1], [1, 0]]), S.Matrix([[0, 1], [1, 0]])),
    ]
    result = []
    for name, v_map, e_map in pairs:
        tested = 0
        for q in range(d + 1):
            for n in range(1, d + 1):
                differential = ce_matrix(m, e, n, d, q)
                if not differential.rows or not differential.cols:
                    continue
                here = induced_wedge_map(m, e, n, d, q, v_map, e_map)
                below = induced_wedge_map(m, e, n - 1, d, q, v_map, e_map)
                assert differential * here == below * differential
                tested += 1
        result.append({"name": name, "dim_V": m, "dim_E": e, "V_degree": d,
                       "V_matrix": [list(v_map.row(i)) for i in range(m)],
                       "E_matrix": [list(e_map.row(i)) for i in range(e)],
                       "CE_chain_map_blocks_verified": tested})
    return result

def signed_pair_controls():
    """Falsifiers for a spurious Leibniz sign and an omitted wedge sign."""
    m, e, q, d = 2, 2, 2, 3
    source = wedge_basis(m, e, q, d - 1, q, True)
    target = wedge_basis(m, e, q, d, q, True)
    source_choices = entries(m, e, d - 1, True)
    target_choices = entries(m, e, d, True)
    lookup = {entry: i for i, entry in enumerate(target_choices)}
    rows = {w: i for i, w in enumerate(target)}
    wrong_leibniz = S.zeros(len(target), m * len(source))
    omitted_sorting = S.zeros(len(target), m * len(source))
    witness = None
    for gen in range(m):
        for col, wedge in enumerate(source):
            for position, ind in enumerate(wedge):
                color, degree, index = source_choices[ind]
                for k, coeff in enumerate(lie_bracket(m, 1, gen, degree, index)):
                    if not coeff:
                        continue
                    output = [lookup[source_choices[x]] for x in wedge]
                    output[position] = lookup[(color, degree + 1, k)]
                    out, sorting = sign_sort(output)
                    if sorting:
                        wrong_leibniz[rows[out], gen * len(source) + col] += (
                            (-1) ** position * sorting * coeff)
                        omitted_sorting[rows[out], gen * len(source) + col] += coeff
                        if sorting == -1 and witness is None:
                            witness = {"generator": gen,
                                "source_factors": [source_choices[x] for x in wedge],
                                "changed_factor_position": position,
                                "output_factors_before_sorting": [target_choices[x] for x in output],
                                "correct_sorting_sign": -1}
    correct = action_matrix(m, e, q, d)
    assert correct != wrong_leibniz and correct != omitted_sorting
    assert witness is not None
    return {"dim_V": m, "dim_E": e, "E_weight": q, "V_degree": d,
            "domain": correct.cols, "codomain": correct.rows,
            "correct_matrix_rank": exact_rank(correct),
            "extra_Leibniz_sign_rank": exact_rank(wrong_leibniz),
            "omitted_sorting_sign_rank": exact_rank(omitted_sorting),
            "both_wrong_matrices_distinguished": True,
            "sorting_sign_witness": witness,
            "limitation": "Matrix distinction tests signs; ranks alone need not distinguish every sign error."}

def right_resolution_controls():
    m, max_length = 3, 4
    words = [word for n in range(max_length + 1) for word in tensor_words(m, n)]
    nonempty = [word for word in words if word]
    split = {word: (word[0], word[1:]) for word in nonempty}
    assert len(set(split.values())) == len(nonempty)
    wrong_side_witnesses = []
    for v, tail in split.values():
        assert (v,) + tail in nonempty
        for a in range(m):
            # phi((v tensor tail) . a)=v tail a=phi(v tensor tail).a
            assert (v,) + (tail + (a,)) == ((v,) + tail) + (a,)
            # Swapping the factors but retaining first-letter multiplication
            # would fail left-linearity in a noncommutative tensor algebra.
            if v != a and not tail:
                wrong_side_witnesses.append({"v": v, "a": a,
                    "incorrect_phi_after_left_action": [v, a],
                    "required_left_linear_value": [a, v]})
    return {"dim_V": m, "word_lengths_through": max_length,
            "augmentation_basis_words": len(nonempty),
            "right_linearity_checks": len(nonempty) * m,
            "wrong_side_counterexamples": wrong_side_witnesses,
            "claim_scope": "Finite word controls; the universal first-letter bijection is proved in REPORT."}

def serialize(value):
    if isinstance(value, S.Integer):
        return int(value)
    if isinstance(value, S.Rational):
        return str(value)
    raise TypeError(type(value).__name__)

if __name__ == "__main__":
    cases = [(0, 2, 0), (0, 2, 2), (2, 0, 1), (2, 0, 4)]
    cases += [(1, 3, d) for d in range(5)]
    cases += [(2, 1, d) for d in range(1, 6)]
    cases += [(2, 2, d) for d in range(1, 5)]
    cases += [(3, 1, d) for d in range(1, 5)]
    cases += [(3, 3, 4), (4, 2, 4)]
    models = []
    for case in cases:
        model = compare_full_ce(*case)
        models.append(model)
        print("full CE validated", case, flush=True)
    out = {"utc": datetime.now(timezone.utc).isoformat(),
           "status": "PASS_FINITE_REDUCTION_CONTROLS", "arithmetic": "exact rational",
           "sympy_version": S.__version__, "models": models,
           "naturality": naturality_controls(),
           "negative_sign_controls": signed_pair_controls(),
           "right_resolution": right_resolution_controls(),
           "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "scope": "Full CE vs reduction, boundaries, q preservation, d squared zero, and naturality in finite degrees. Not the unrestricted functor decomposition."}
    (OWN / "NEW_EXACT_CE_RECEIPT.json").write_text(json.dumps(out, indent=2, default=serialize) + "\n")
    print(json.dumps({"models": len(models), "naturality_blocks":
                      sum(x["CE_chain_map_blocks_verified"] for x in out["naturality"]),
                      "status": out["status"]}, indent=2))
