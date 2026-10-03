"""Exact rational walk controls for hypotheses in the frozen rotation proof.

These controls verify finite algebra and distinguish invalid mechanisms. They
are not simulations, Brownian-law certificates, or attempts at an exact shift.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

checks = {}
details = {}


def check(name, value, detail=None):
    assert value, name
    checks[name] = True
    if detail is not None:
        details[name] = detail


words = tuple(product((-1, 1), repeat=3))


def stop(word, level, cap):
    value = 0
    for j, bit in enumerate(word[:cap], 1):
        value += bit
        if value == level:
            return tuple(word[:j])
    return tuple(word[:cap])


def mark_law(level, cap, active_probability):
    law = defaultdict(Q)
    law[()] += 1 - active_probability
    for word in words:
        law[stop(word, level, cap)] += active_probability / len(words)
    assert sum(law.values()) == 1
    return law


def prefix_law(law1, law2, prefix_length=6, reverse_internal=False):
    result = defaultdict(Q)
    tail_words = tuple(product((-1, 1), repeat=prefix_length))
    for chunk1, probability1 in law1.items():
        for chunk2, probability2 in law2.items():
            chunks = (chunk1, chunk2)
            if reverse_internal:
                chunks = tuple(tuple(reversed(chunk)) for chunk in chunks)
            for tail in tail_words:
                prefix = tuple(-v for chunk in chunks for v in chunk) + tail
                result[prefix[:prefix_length]] += (
                    probability1 * probability2 / len(tail_words)
                )
    return result


law1 = mark_law(-1, 3, Q(1, 3))
law2 = mark_law(1, 2, Q(3, 5))
correct = prefix_law(law1, law2)
check(
    "non_iid_randomized_zero_stop_gluing_exact_six_step_law",
    len(correct) == 64 and set(correct.values()) == {Q(1, 64)},
    {"mark1_active_probability": "1/3", "mark2_active_probability": "3/5",
     "prefix_atoms": len(correct)},
)

# A future-dependent zero duration would not be an F_0 stopping decision.
bad_zero_law = defaultdict(Q)
for word in words:
    bad_zero_law[() if word[-1] == 1 else word] += Q(1, 8)
bad_zero = prefix_law(bad_zero_law, {(): Q(1)})
check(
    "anticipated_time_zero_decision_rejected_by_prefix_law",
    set(bad_zero.values()) != {Q(1, 64)},
    {"terminal_mean_of_bad_mark": str(sum(sum(k) * v for k, v in bad_zero_law.items()))},
)

# Optional sampling checks use a legitimate bounded stopping rule. Terminal
# displacement is not independent of T, which this control also exposes.
sample = []
for word in words:
    chunk = stop(word, -1, 2)
    sample.append((len(chunk), sum(chunk), Q(1, 8)))
mean = sum(value * weight for duration, value, weight in sample)
second = sum(value * value * weight for duration, value, weight in sample)
duration_mean = sum(duration * weight for duration, value, weight in sample)
exponential = sum(Q(2) ** value / Q(5, 4) ** duration * weight
                  for duration, value, weight in sample)
check("bounded_optional_sampling_terminal_mean", mean == 0)
check("bounded_optional_sampling_terminal_square", second == duration_mean == Q(3, 2))
check("bounded_optional_sampling_exponential_martingale", exponential == 1)
check(
    "terminal_duration_dependence_detected",
    {value for duration, value, weight in sample if duration == 1} == {-1},
    {"E_endpoint": str(mean), "E_endpoint_squared": str(second),
     "E_duration": str(duration_mean), "exponential_expectation": str(exponential)},
)
original_pair_law = defaultdict(Q)
reflected_pair_law = defaultdict(Q)
for duration, value, weight in sample:
    original_pair_law[(duration, value)] += weight
    reflected_pair_law[(duration, -value)] += weight
check("sign_change_preserves_admissibility_not_joint_mark_law",
      original_pair_law != reflected_pair_law,
      {"original_probability_T1_endpoint_minus1": str(original_pair_law[(1, -1)]),
       "reflected_probability_T1_endpoint_minus1": str(reflected_pair_law[(1, -1)])})

# An anticipating T=1 or 3 fails the stopped-martingale hypothesis and the
# concatenated fair-prefix law. This is an invalid-input control, not a source
# counterexample.
bad_law = defaultdict(Q)
for word in words:
    chunk = word[:1] if word[-1] == -1 else word
    bad_law[chunk] += Q(1, 8)
bad_mean = sum(sum(chunk) * probability for chunk, probability in bad_law.items())
bad_prefix = prefix_law(bad_law, {(): Q(1)})
check("anticipated_T_rejected_by_optional_sampling", bad_mean == Q(1, 2))
check("anticipated_T_rejected_by_gluing_law", set(bad_prefix.values()) != {Q(1, 64)})

# Reversed stopped paths need not be Brownian. For cap-two first hitting of -1,
# the first reversed reflected increment is +1 with probability 3/4, although
# the correctly ordered reflected first increment has probability 1/2.
forward_first = Q(0)
reversed_first = Q(0)
for word in words:
    chunk = stop(word, -1, 2)
    forward_first += Q(1, 8) * (-chunk[0] == 1)
    reversed_first += Q(1, 8) * (-chunk[-1] == 1)
check("internal_reversal_negative_control", forward_first == Q(1, 2) and reversed_first == Q(3, 4),
      {"correct_first_plus_probability": str(forward_first),
       "reversed_first_plus_probability": str(reversed_first)})

# Deterministic rotations of iid increments preserve their law; rotation at an
# endogenous stopping cut can bias it. This is distinct from the submitted
# 180-degree piece identity, whose W uses the unrotated driving chunks.
cyclic = defaultdict(Q)
deterministic_cyclic = defaultdict(Q)
for word in product((-1, 1), repeat=2):
    duration = len(stop(word, -1, 2))
    cyclic[word[duration:] + word[:duration]] += Q(1, 4)
    deterministic_cyclic[word[1:] + word[:1]] += Q(1, 4)
check("deterministic_circular_exchangeability_control", set(deterministic_cyclic.values()) == {Q(1, 4)})
check("endogenous_cyclic_rotation_negative_control",
      sum(v for k, v in cyclic.items() if k[0] == 1) == Q(3, 4),
      {str(k): str(v) for k, v in cyclic.items()})

# Test complete joint finite laws, stronger than a covariance-only diagnostic.
joint = defaultdict(Q)
for negative_word, np in correct.items():
    for positive_word in product((-1, 1), repeat=3):
        joint[(negative_word[:3], positive_word)] += np / 8
check("disjoint_input_half_independence_joint_law", len(joint) == 64 and set(joint.values()) == {Q(1, 64)})
shared = {(word, word): Q(1, 8) for word in product((-1, 1), repeat=3)}
check("shared_input_half_independence_negative_control", len(shared) == 8 and joint != shared)


def path(increments):
    values = [Q(0)]
    for increment in increments:
        values.append(values[-1] + increment)
    return values


def interpolate(values, time):
    j = time.numerator // time.denominator
    if j == len(values) - 1:
        return values[j]
    return values[j] + (time - j) * (values[j + 1] - values[j])


# Rational non-unit slopes, zero chunks, and quarter-grid cut-through horizons
# were absent from the old tests. Endpoint/index identities must hold even on
# deterministic non-Brownian paths because these are algebraic claims.
algebra_cases = 0
equalities = 0
for lengths in ((0, 2, 1, 0, 3), (1, 0, 2, 0), (0, 0, 1, 3)):
    n = sum(lengths)
    for increments in product((Q(-3, 2), Q(1, 3)), repeat=n):
        chunks = []
        cursor = 0
        for length in lengths:
            chunks.append(increments[cursor:cursor+length])
            cursor += length
        w = path(tuple(v for chunk in chunks for v in chunk))
        r = path(tuple(v for chunk in chunks for v in reversed(chunk)))
        cursor = 0
        for chunk in chunks:
            T = len(chunk)
            for quarter in range(4*T + 1):
                u = Q(quarter, 4)
                assert interpolate(r, cursor + u) == (
                    w[cursor] + w[cursor+T] - interpolate(w, cursor+T-u)
                )
                equalities += 1
            cursor += T
        c = max(lengths)
        for quarter in range(4*n+1):
            H = Q(quarter, 4)
            horizon_grid = tuple(Q(k, 4) for k in range(quarter+1))
            full_grid = tuple(Q(k, 4) for k in range(4*n+1) if Q(k, 4) <= H+c)
            err = max(abs(interpolate(r, t) - interpolate(w, t)) for t in horizon_grid)
            modulus = max(abs(interpolate(w, t) - interpolate(w, u))
                          for t in full_grid for u in full_grid if abs(t-u) <= c)
            assert err <= 2*modulus
        algebra_cases += 1
check("rational_non_unit_slope_rotation_quarter_grid", algebra_cases == 88,
      {"path_configurations": algebra_cases, "quarter_grid_equalities": equalities})

# A common time bound is essential for the domain used in the modulus estimate.
# If the only piece has duration 10 while a false bound c=1 is inserted, a spike
# at time 9 is invisible in [0,H+c]=[0,2] but affects reversal at H=1.
oversized_w = [Q(0)] * 11
oversized_w[9] = 7
R1 = oversized_w[0] + oversized_w[10] - oversized_w[9]
false_modulus = max(abs(a-b) for a in oversized_w[:3] for b in oversized_w[:3])
check("noncommon_bound_horizon_negative_control", abs(R1 - oversized_w[1]) > 2*false_modulus,
      {"piece_duration": 10, "false_c": 1, "horizon": 1, "error": 7, "false_modulus": 0})

# These cover and series constants are checked without external symbolic code.
for m in range(1, 9):
    for quarter in range(4*(2**m+1)+1):
        s = Q(quarter, 4)
        t = min(Q(2**m+1), s+1)
        j = s.numerator // s.denominator
        assert 0 <= j <= 2**m+1 and j <= s <= t <= j+2
check("dyadic_time_cover_including_last_cell", True)
e4_lower = sum(Q(4)**j / __import__('math').factorial(j) for j in range(4))
check("dyadic_tail_rational_majorant", e4_lower > 16 and Q(2, 16) < 1)

out = {
    "passed": True, "named_checks": len(checks), "checks": checks,
    "details": details,
    "source_target_solved": False, "source_research_turns_added": 0,
    "scope": "Exact rational finite laws and algebra, with explicitly invalid-input controls. Brownian gluing and pathwise probability estimates require the independent written proof; no finite random shift has been constructed.",
}
Path(__file__).with_name('falsification_results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
