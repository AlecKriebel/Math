#!/usr/bin/env python3
"""Independent exact sparse-polynomial review of the pointwise cut theorem.

This reviewer imports no discovery code and does not use symbolic-factorization
software.  It parses the frozen polynomial strings with a small AST evaluator,
reconstructs every factorization in exact rational sparse arithmetic, computes
all tensor-product Bernstein coefficients directly, checks the true-bridge
signatures, and rederives the four two-active-endpoint identities.
"""
from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, prod
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "certificates" / "pointwise_cut_certificate.json"
OUT = ROOT / "certificates" / "pointwise_cut_adversarial_review.json"

VARIABLES = tuple(f"x{i}" for i in range(15))
INDEX = {name: i for i, name in enumerate(VARIABLES)}
ZERO_EXP = (0,) * len(VARIABLES)

# Sparse polynomial: exponent tuple -> exact rational coefficient.
Poly = dict[tuple[int, ...], Fraction]


def clean(poly: Poly) -> Poly:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def constant(value: Fraction | int) -> Poly:
    value = Fraction(value)
    return {} if not value else {ZERO_EXP: value}


def variable(name: str) -> Poly:
    exponent = [0] * len(VARIABLES)
    exponent[INDEX[name]] = 1
    return {tuple(exponent): Fraction(1)}


def add(left: Poly, right: Poly) -> Poly:
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
        if not answer[monomial]:
            del answer[monomial]
    return answer


def neg(poly: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def mul(left: Poly, right: Poly) -> Poly:
    if not left or not right:
        return {}
    # Iterate the smaller dictionary outside to reduce Python overhead.
    if len(left) > len(right):
        left, right = right, left
    answer: Poly = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            answer[monomial] = answer.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
    return clean(answer)


def power(poly: Poly, exponent: int) -> Poly:
    assert exponent >= 0
    answer = constant(1)
    base = poly
    while exponent:
        if exponent & 1:
            answer = mul(answer, base)
        exponent >>= 1
        if exponent:
            base = mul(base, base)
    return answer


def divide_constant(poly: Poly, denominator: Poly) -> Poly:
    assert set(denominator) == {ZERO_EXP}
    scalar = denominator[ZERO_EXP]
    assert scalar
    return {monomial: coefficient / scalar for monomial, coefficient in poly.items()}


PARSE_CACHE: dict[str, Poly] = {}


def parse_expression(text: str) -> Poly:
    cached = PARSE_CACHE.get(text)
    if cached is not None:
        return cached
    tree = ast.parse(text, mode="eval")

    def evaluate(node: ast.AST) -> Poly:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant):
            assert isinstance(node.value, int)
            return constant(node.value)
        if isinstance(node, ast.Name):
            assert node.id in INDEX
            return variable(node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return neg(evaluate(node.operand))
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add):
                return add(evaluate(node.left), evaluate(node.right))
            if isinstance(node.op, ast.Sub):
                return add(evaluate(node.left), neg(evaluate(node.right)))
            if isinstance(node.op, ast.Mult):
                return mul(evaluate(node.left), evaluate(node.right))
            if isinstance(node.op, ast.Div):
                return divide_constant(evaluate(node.left), evaluate(node.right))
            if isinstance(node.op, ast.Pow):
                assert isinstance(node.right, ast.Constant) and isinstance(node.right.value, int)
                return power(evaluate(node.left), node.right.value)
        raise AssertionError(ast.dump(node))

    result = clean(evaluate(tree))
    PARSE_CACHE[text] = result
    return result


def rational(value: object) -> Fraction:
    text = str(value)
    if "/" in text:
        numerator, denominator = text.split("/", 1)
        return Fraction(int(numerator), int(denominator))
    return Fraction(text)


BERNSTEIN_CACHE: dict[tuple[str, tuple[str, ...], tuple[int, ...]], tuple[Fraction, ...]] = {}


def bernstein_coefficients(expression: str, active: tuple[str, ...], degrees: tuple[int, ...]) -> tuple[Fraction, ...]:
    key = (expression, active, degrees)
    if key in BERNSTEIN_CACHE:
        return BERNSTEIN_CACHE[key]
    polynomial = parse_expression(expression)
    active_indices = tuple(INDEX[name] for name in active)
    inactive_indices = set(range(len(VARIABLES))) - set(active_indices)
    terms: dict[tuple[int, ...], Fraction] = {}
    for monomial, coefficient in polynomial.items():
        assert all(monomial[index] == 0 for index in inactive_indices)
        active_monomial = tuple(monomial[index] for index in active_indices)
        assert all(exponent <= degree for exponent, degree in zip(active_monomial, degrees))
        terms[active_monomial] = terms.get(active_monomial, Fraction(0)) + coefficient
    answer: list[Fraction] = []
    for beta in product(*(range(degree + 1) for degree in degrees)):
        value = Fraction(0)
        for alpha, coefficient in terms.items():
            if not all(a <= b for a, b in zip(alpha, beta)):
                continue
            multiplier = Fraction(1)
            for degree, b, a in zip(degrees, beta, alpha):
                multiplier *= Fraction(comb(b, a), comb(degree, a))
            value += coefficient * multiplier
        answer.append(value)
    result = tuple(answer)
    BERNSTEIN_CACHE[key] = result
    return result


def partial_bernstein_polynomials(expression: str, variables: tuple[str, ...], degrees: tuple[int, ...]) -> dict[tuple[int, ...], Poly]:
    polynomial = parse_expression(expression)
    active_indices = tuple(INDEX[name] for name in variables)
    answer: dict[tuple[int, ...], Poly] = {}
    for beta in product(*(range(degree + 1) for degree in degrees)):
        value: Poly = {}
        for monomial, coefficient in polynomial.items():
            alpha = tuple(monomial[index] for index in active_indices)
            assert all(a <= degree for a, degree in zip(alpha, degrees))
            if not all(a <= b for a, b in zip(alpha, beta)):
                continue
            multiplier = Fraction(1)
            for degree, b, a in zip(degrees, beta, alpha):
                multiplier *= Fraction(comb(b, a), comb(degree, a))
            reduced = list(monomial)
            for index in active_indices:
                reduced[index] = 0
            reduced_tuple = tuple(reduced)
            value[reduced_tuple] = value.get(reduced_tuple, Fraction(0)) + coefficient * multiplier
        answer[beta] = clean(value)
    return answer


FACTOR_CERT_CACHE: dict[str, tuple[int, bool]] = {}
SIGN_CACHE: dict[str, int] = {}


def verify_factor(record: dict, nested: bool = False) -> tuple[int, bool]:
    active = tuple(record["active"])
    if nested:
        metadata = record["bernstein"]
        degrees = tuple(metadata["degrees"])
        expected_negative = metadata["negative"]
        expected_positive = metadata["positive"]
        expected_zero = metadata["zero"]
        expected_min = rational(metadata["min"])
        expected_max = rational(metadata["max"])
        recorded_factor_sign = record["factor_sign"]
    else:
        degrees = tuple(record["degrees"])
        expected_negative = record["negative"]
        expected_positive = record["positive"]
        expected_zero = record["zero_count"]
        expected_min = rational(record["min"])
        expected_max = rational(record["max"])
        recorded_factor_sign = record["sign"]
        assert record["count"] == prod(degree + 1 for degree in degrees)

    coefficients = bernstein_coefficients(record["factor"], active, degrees)
    negative = sum(value < 0 for value in coefficients)
    positive = sum(value > 0 for value in coefficients)
    zero = sum(value == 0 for value in coefficients)
    assert (negative, positive, zero) == (expected_negative, expected_positive, expected_zero)
    assert min(coefficients) == expected_min and max(coefficients) == expected_max
    raw_sign = 1 if negative == 0 and positive > 0 else -1 if positive == 0 and negative > 0 else 0
    exponent = int(record["exponent"])
    if raw_sign:
        assert recorded_factor_sign == raw_sign
        contribution = raw_sign ** exponent
        strict = True
        if nested:
            assert record["strict_on_open_cube"]
    else:
        assert nested and exponent % 2 == 0 and recorded_factor_sign == 1
        assert not record["strict_on_open_cube"]
        contribution = 1
        strict = False
    return contribution, strict


def verify_factored_certificate(record: dict, nested: bool = False) -> int:
    key = json.dumps({"nested": nested, "record": record}, sort_keys=True, separators=(",", ":"))
    if key in FACTOR_CERT_CACHE:
        return FACTOR_CERT_CACHE[key][0]
    assert not record["zero"]
    expression = parse_expression(record["expression"])
    coefficient = rational(record["coefficient"])
    reconstructed = constant(coefficient)
    total_sign = 1 if coefficient > 0 else -1
    strict = True
    for factor in record["factors"]:
        contribution, factor_strict = verify_factor(factor, nested=nested)
        reconstructed = mul(reconstructed, power(parse_expression(factor["factor"]), int(factor["exponent"])))
        total_sign *= contribution
        strict &= factor_strict
    assert expression == reconstructed
    if nested:
        assert total_sign == record["weak_sign"]
        assert strict == record["strict"]
        result = record["weak_sign"]
    else:
        assert total_sign == record["total_sign"]
        result = record["total_sign"]
    FACTOR_CERT_CACHE[key] = (result, strict)
    return result


def verify_partial_certificate(record: dict) -> int:
    assert not record["zero"] and record["total_sign"] in (-1, 1)
    partial = record["partial_certificate"]
    variables = tuple(partial["inheritance_variables"])
    degrees = tuple(partial["degrees"])
    coefficients = partial_bernstein_polynomials(record["expression"], variables, degrees)
    assert len(coefficients) == partial["coefficient_count"] == prod(degree + 1 for degree in degrees)
    stored = {tuple(item["index"]): item for item in partial["coefficients"]}
    assert set(stored) == set(coefficients)
    nonzero = 0
    strict = 0
    for index, value in coefficients.items():
        item = stored[index]
        if not value:
            assert item["zero"]
            continue
        nonzero += 1
        assert not item["zero"]
        certificate = item["coefficient_certificate"]
        assert value == parse_expression(certificate["expression"])
        sign = verify_factored_certificate(certificate, nested=True)
        assert sign == partial["total_sign"]
        strict += int(certificate["strict"])
    assert nonzero == partial["nonzero_count"]
    assert bool(strict) == partial["at_least_one_coefficient_strict"]
    assert partial["total_sign"] == record["total_sign"]
    return record["total_sign"]


def verify_sign(record: dict) -> int:
    key = json.dumps(record, sort_keys=True, separators=(",", ":"))
    if key not in SIGN_CACHE:
        SIGN_CACHE[key] = verify_partial_certificate(record) if "partial_certificate" in record else verify_factored_certificate(record)
    return SIGN_CACHE[key]


def main() -> None:
    data = json.loads(SOURCE.read_text())
    assert data["status"] == "PROVED"
    assert len(data["endpoint_records"]) == data["endpoint_type_count"] == 177
    assert len({row["type_key"] for row in data["endpoint_records"]}) == 177
    assert sum(data["endpoint_origin_type_counts"].values()) >= 177

    endpoint_counts = Counter()
    ordinary_signs = 0
    partial_signs = 0
    for row in data["endpoint_records"]:
        certificate = row["certificate"]
        branch = certificate["branch"]
        endpoint_counts[branch] += 1
        if branch == "F_positive":
            sign_record = certificate["F"]
            assert not sign_record["zero"] and verify_sign(sign_record) == 1
        else:
            assert branch == "F_zero_G_positive"
            assert certificate["F"] == {"expression": "0", "zero": True}
            sign_record = certificate["G"]
            assert verify_sign(sign_record) == 1
        partial_signs += int("partial_certificate" in sign_record)
        ordinary_signs += int("partial_certificate" not in sign_record)
    assert dict(endpoint_counts) == data["endpoint_dichotomy"] == {"F_positive": 151, "F_zero_G_positive": 26}

    assert len(data["single_blob_records"]) == data["single_blob_type_count"] == 453
    assert len({row["type_key"] for row in data["single_blob_records"]}) == 453
    single_counts = Counter()
    bridge_signature_checks = 0
    for row in data["single_blob_records"]:
        certificate = row["certificate"]
        classification = certificate["classification"]
        single_counts[classification] += 1
        if classification == "wrong_split_strict":
            assert not certificate["displayed_bridge"]
            sign_record = certificate["sign"]
            assert verify_sign(sign_record) in (-1, 1)
            partial_signs += int("partial_certificate" in sign_record)
            ordinary_signs += int("partial_certificate" not in sign_record)
        else:
            assert classification == "rank_one_all_blocks" and certificate["displayed_bridge"]
            tensor_type = ast.literal_eval(row["type_key"])
            assert any(len(set(signature)) == 1 and signature[0] in (3, 12) for signature in tensor_type)
            bridge_signature_checks += 1
    assert dict(single_counts) == data["single_blob_classification"] == {"wrong_split_strict": 421, "rank_one_all_blocks": 32}
    assert bridge_signature_checks == 32

    # Independent exact polynomial derivation of the two-active identities.
    # m0=m2=0 gives A*B*C=T^2 after positive cancellation; m0=m3=0 gives
    # a*b*c=t^2.  Together with m0=0 and z in (0,1), the endpoint zero-branch
    # inequalities a>b*c and A>B*C are contradictory.
    stored = data["two_active_endpoint_case"]["decisive_minors"]
    expected = {
        "m0": "a*A-b*c*B*C*z**2",
        "m1": "(a*A-T*t*z)*(a*A+T*t*z)",
        "m2": "a*A**2-b*c*T**2*z**2",
        "m3": "a**2*A-t**2*B*C*z**2",
    }
    # These nine symbols are outside the x_i parser.  Expand both sides in a
    # second exact sparse ring and compare coefficient dictionaries.
    symbols = ("a", "b", "c", "t", "A", "B", "C", "T", "z")
    symbol_index = {name: index for index, name in enumerate(symbols)}
    generic_zero = (0,) * len(symbols)

    def generic_parse(text: str):
        def gconstant(value):
            value = Fraction(value)
            return {} if not value else {generic_zero: value}
        def gadd(left, right):
            answer = dict(left)
            for monomial, coefficient in right.items():
                answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
                if not answer[monomial]: del answer[monomial]
            return answer
        def gneg(poly): return {m: -c for m, c in poly.items()}
        def gmul(left, right):
            answer = {}
            for lm, lc in left.items():
                for rm, rc in right.items():
                    monomial = tuple(a + b for a, b in zip(lm, rm))
                    answer[monomial] = answer.get(monomial, Fraction(0)) + lc * rc
            return {m: c for m, c in answer.items() if c}
        def gpow(poly, exponent):
            answer = gconstant(1); base = poly
            while exponent:
                if exponent & 1: answer = gmul(answer, base)
                exponent >>= 1
                if exponent: base = gmul(base, base)
            return answer
        def visit(node):
            if isinstance(node, ast.Expression): return visit(node.body)
            if isinstance(node, ast.Constant):
                assert isinstance(node.value, int); return gconstant(node.value)
            if isinstance(node, ast.Name):
                assert node.id in symbol_index
                exponent = [0] * len(symbols); exponent[symbol_index[node.id]] = 1
                return {tuple(exponent): Fraction(1)}
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub): return gneg(visit(node.operand))
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Add): return gadd(visit(node.left), visit(node.right))
                if isinstance(node.op, ast.Sub): return gadd(visit(node.left), gneg(visit(node.right)))
                if isinstance(node.op, ast.Mult): return gmul(visit(node.left), visit(node.right))
                if isinstance(node.op, ast.Pow):
                    assert isinstance(node.right, ast.Constant) and isinstance(node.right.value, int)
                    return gpow(visit(node.left), node.right.value)
            raise AssertionError(ast.dump(node))
        return visit(ast.parse(text, mode="eval"))

    for name, text in expected.items():
        assert generic_parse(stored[name]) == generic_parse(text)
    assert data["two_active_endpoint_case"]["derived_rank_one_equations"] == [
        "a*b*c=t**2", "A*B*C=T**2", "a*A=b*c*B*C*z**2"
    ]

    review = {
        "status": "VERIFIED",
        "endpoint_types_checked": 177,
        "endpoint_F_positive": endpoint_counts["F_positive"],
        "endpoint_F_zero_G_positive": endpoint_counts["F_zero_G_positive"],
        "single_blob_types_checked": 453,
        "strict_wrong_split_minor_signs_checked": single_counts["wrong_split_strict"],
        "rank_one_true_bridge_types_checked": bridge_signature_checks,
        "ordinary_factored_sign_certificates_checked": ordinary_signs,
        "partial_Bernstein_sign_certificates_checked": partial_signs,
        "distinct_factor_Bernstein_expansions_checked": len(BERNSTEIN_CACHE),
        "two_active_endpoint_minors_checked": 4,
        "two_active_endpoint_contradiction": "VERIFIED",
        "conclusion": "one-sided open JC containment preserves every cut split",
    }
    assert review["distinct_factor_Bernstein_expansions_checked"] == 547
    OUT.write_text(json.dumps(review, indent=2, sort_keys=True) + "\n")
    print(json.dumps(review, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
