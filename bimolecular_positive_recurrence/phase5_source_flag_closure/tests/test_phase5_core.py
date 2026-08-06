from fractions import Fraction
from math import log

from src.generator import Reaction
from phase5_source_flag_closure.src.complete_credit_elimination import (
    envelope_step,
    path_envelope,
    verify_concave_supremum,
)
from phase5_source_flag_closure.src.episode_library import (
    enumerate_episode_outcomes,
    expected_template_drift,
    shortest_designated_path,
)
from phase5_source_flag_closure.src.source_rate_flag import (
    top_availability_or_conservation,
)
from phase5_source_flag_closure.src.target_source_residual import (
    entropy_identity_terms,
    increment_ratio,
)


def stress_network():
    return (
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    )


def test_residual_identity_and_entropy_bound():
    rs = stress_network()
    x = (51, 1)
    t = (1, 1)
    assert increment_ratio(x, t, t) == 1
    terms = entropy_identity_terms(x, t, rs)
    assert abs(terms["direct"] - terms["rewritten"]) < 1e-12
    assert terms["direct"] <= terms["upper_bound"] + 1e-12


def test_episode_recursion_equals_branch_enumeration():
    rs = stress_network()
    path = shortest_designated_path(rs, (0, 0), (0, 1))
    drift, _ = expected_template_drift(rs, (100, 0), path)
    branches = enumerate_episode_outcomes(rs, (100, 0), path)
    expected = sum(float(p) * reward for p, reward in branches)
    assert abs(drift - expected) < 1e-12
    assert drift < -4


def test_scalar_elimination_formula():
    assert verify_concave_supremum(-500, 3.0, 0.2, 5000)
    cert = envelope_step(-500, 3.0, 0.2)
    assert cert.branch == "interior"
    b1, _ = path_envelope(1e-20, 2.0, (0.2, 0.3, 0.4))
    b2, _ = path_envelope(1e-200, 2.0, (0.2, 0.3, 0.4))
    assert b2 < b1


def test_top_pair_and_token_conservation():
    C = ((0, 0), (1, 1), (0, 1))
    cert = top_availability_or_conservation(C, {0}, (Fraction(1), Fraction(0)))
    assert cert.kind == "service_available"
    C2 = ((0, 0), (1, 1))
    cert2 = top_availability_or_conservation(C2, {0}, (Fraction(1), Fraction(0)))
    assert cert2.kind == "service_token_conservation"
    assert cert2.conservation == (Fraction(1), Fraction(-1))
