"""Independent exact geometry and seam-law controls; no research helper imports."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json


def at(values, time):
    if time == len(values) - 1:
        return Q(values[-1])
    left = int(time)
    return Q(values[left]) + (time - left) * (values[left + 1] - values[left])


def integrated(increments):
    values = [0]
    for inc in increments:
        values.append(values[-1] + inc)
    return values


def modulus(values, length, cap):
    # All polygon vertices for a continuous piecewise-linear difference.
    times = {Q(0), length}
    for k in range(len(values)):
        for t in [Q(k), Q(k) - cap, Q(k) + cap]:
            if 0 <= t <= length:
                times.add(t)
    return max(abs(at(values, s) - at(values, t))
               for s in times for t in times if abs(s - t) <= cap)


def main():
    piece_options = [()]
    for size in [1, 2]:
        piece_options.extend(product((-2, 0, 1), repeat=size))
    configurations = identities = horizon_checks = 0
    zero_configurations = endpoint_checks = 0
    for pieces in product(piece_options, repeat=3):
        forward = integrated([d for p in pieces for d in p])
        reverse = integrated([d for p in pieces for d in reversed(p)])
        total = len(forward) - 1
        if not total:
            continue
        configurations += 1
        zero_configurations += any(not p for p in pieces)
        start = 0
        for p in pieces:
            size = len(p)
            for numerator in range(3 * size + 1):
                u = Q(numerator, 3)
                direct = at(reverse, start + u)
                rotated = (at(forward, Q(start)) + at(forward, Q(start + size))
                           - at(forward, Q(start + size) - u))
                assert direct == rotated
                identities += 1
            start += size
            assert reverse[start] == forward[start]
            endpoint_checks += 1
        for numerator in range(1, 2 * total + 1):
            horizon = Q(numerator, 2)
            compare_end = min(Q(total), horizon + 2)
            local_error = max(abs(at(reverse, t) - at(forward, t))
                              for t in [Q(k) for k in range(int(horizon) + 1)] + [horizon])
            assert local_error <= 2 * modulus(forward, compare_end, Q(2))
            horizon_checks += 1

    # A omitted R+c extension is false even for continuous piecewise-linear paths.
    witness = [0, 0, 2]
    t = Q(1, 2)
    rotated = Q(witness[0] + witness[2]) - at(witness, Q(2) - t)
    error = abs(rotated - at(witness, t))
    wrong_short_bound = 2 * modulus(witness, t, Q(2))
    assert error == 1 and wrong_short_bound == 0

    # Independent stopped-walk tree: stop on hitting -1, capped at 2.
    stopped = [((-1,), Q(1, 2)), ((1, -1), Q(1, 4)), ((1, 1), Q(1, 4))]
    forward_plus = sum(prob for path, prob in stopped if -path[0] == 1)
    reverse_plus = sum(prob for path, prob in stopped if -path[-1] == 1)
    assert forward_plus == Q(1, 2)
    assert reverse_plus == Q(3, 4)
    result = {
        "passed": True,
        "independent_path_configurations": configurations,
        "configurations_with_zero_length_piece": zero_configurations,
        "exact_rational_rotation_checks": identities,
        "junction_checks": endpoint_checks,
        "half_integer_horizon_modulus_checks": horizon_checks,
        "omitted_horizon_extension_falsifier": {
            "W_knots": witness, "R": "1/2", "error": str(error),
            "incorrect_short_horizon_bound": str(wrong_short_bound)},
        "stopped_walk_fixed_seam_falsifier": {
            "negative_forward_first_step_plus_probability": str(forward_plus),
            "negative_reversed_first_step_plus_probability": str(reverse_plus)},
        "scope": "Exact finite geometry and a discrete fixed-seam diagnostic. Brownian laws, continuous Brownian support, almost-sure bounds, random-root existence, and novelty are not inferred from these computations."
    }
    path = Path(__file__).parent / "INDEPENDENT_CONTROL_RESULTS.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
