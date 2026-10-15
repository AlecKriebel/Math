"""Exact controls for source/review wording; no new Brownian target search."""
from pathlib import Path
from itertools import product
import json
import sympy as s

HERE = Path(__file__).resolve().parent


def main():
    original = []
    reflected = []
    for steps in product((-1, 1), repeat=3):
        pos = 0
        stop = 3
        terminal = None
        for t, step in enumerate(steps, 1):
            pos += step
            if pos == -1:
                stop = t
                terminal = pos
                break
        if terminal is None:
            terminal = pos
        original.append((stop, terminal))
        reflected.append((stop, -terminal))
    original_event = sum(t < 3 and b == -1 for t, b in original)
    reflected_event = sum(t < 3 and b == -1 for t, b in reflected)
    assert original_event == 4 and reflected_event == 0
    # A terminal forward +c unit increment becomes a backward -c unit
    # increment. Reflecting the complete backward path restores +c.
    b = [0, 1, 2, 5]
    reverse = [b[3-u] - b[3] for u in range(4)]
    assert b[-1] - b[-2] == 3
    assert reverse[1] - reverse[0] == -3
    assert (-reverse[1]) - (-reverse[0]) == 3
    # A continuous increment curve can begin above a level and remain above it.
    # Hence reaching >=c later need not imply hitting exactly c after time1.
    t = s.symbols("t", real=True)
    y = 2*t
    increment = s.simplify(y - y.subs(t, t-1))
    assert increment == 2 and increment > 1
    # Under the hypothesized Brownian law the omitted initial-level probability
    # vanishes as the source's threshold diverges.
    c = s.symbols("c", positive=True)
    assert s.limit(s.erfc(c/s.sqrt(2))/2, c, s.oo) == 0
    beta = s.symbols("beta", positive=True)
    gap = c*s.sqrt(beta/2) - c*s.sqrt(beta)/2
    coefficient = s.simplify(gap / (c*s.sqrt(beta)))
    assert coefficient == (s.sqrt(2)-1)/2 and coefficient.is_positive
    out = {"passed": True, "sympy_version": s.__version__,
           "asymmetric_stopped_walk_pair_law": {"original_event_count": original_event,
                                                "reflected_event_count": reflected_event,
                                                "total_equally_likely_inputs": 8},
           "terminal_forward_increment": 3, "backward_increment": -3,
           "whole_backward_reflection_increment": 3,
           "continuous_initial_above_level_counterexample": {"increment": 2, "level": 1,
                                                               "equality_hit_after_time_one": False},
           "gaussian_initial_boundary_term_limit": 0,
           "theorem_5_2_gap_coefficient": str(coefficient),
           "scope": "Checks sign and equality-hit boundary reasoning and disambiguates literal TeX radical placement. Finite stopped-walk control illustrates the false old-review joint-law claim; the Brownian counterexample is supplied in the written audit. No new proof attempt on the open target."}
    (HERE / "SOURCE_QUALIFICATION_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
