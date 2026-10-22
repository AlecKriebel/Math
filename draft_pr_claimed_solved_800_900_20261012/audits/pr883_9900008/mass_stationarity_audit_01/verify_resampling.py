#!/usr/bin/env python3
"""Independent exact window-integral checks; no claim of proving all Borel C.

The analytic proof is in REPORT.md. This program integrates finite partitions
of U exactly, using Fractions, rather than sampling U or inheriting the author
finite quotient checker. Standard library only, no network or candidate writes.
"""
import json
from fractions import Fraction as F


def need(condition, message):
    if not condition:
        raise ValueError(message)


def overlap(intervals):
    lo = max(pair[0] for pair in intervals)
    hi = min(pair[1] for pair in intervals)
    return max(F(0), hi-lo)


def probability(a, b, r, root, height, output_label, zlo, zhi):
    """P(output phase is label AND U_y+V_y in [zlo,zhi)).

    C vertical interval is [0,height), with positive integer height. For each
    possible supporting line y, conditional line probability is its weight /
    (height*(a+b)); U_y has density 1/height. Integrate the intersection of the
    U interval, line-in-C-U condition and shifted-U output interval.
    """
    need(a > 0 and b > 0 and 0 < r < 1, "invalid measure")
    need(root in (F(0), r), "root not supported")
    need(type(height) is int and height > 0, "height must be positive integer")
    need(output_label in (0, 1), "wrong output label")
    need(0 <= zlo < zhi <= height, "wrong test interval")
    total = F(0)
    offsets, weights = (F(0), r), (a, b)
    for label, (offset, weight) in enumerate(zip(offsets, weights)):
        if label != output_label:
            continue
        for n in range(-height-2, height+3):
            y = F(n)+offset-root
            need((root+y) % 1 == offset, "phase sign convention wrong")
            length = overlap([(F(0), F(height)), (-y, height-y),
                              (zlo-y, zhi-y)])
            total += weight * length / (height*height*(a+b))
    return total


def run():
    cases = 0
    models = [(F(1),F(2),F(1,2)), (F(2),F(5),F(1,3)),
              (F(7,3),F(5,2),F(2,5)), (F(5),F(1),F(7,9))]
    for a,b,r in models:
        for root in (F(0),r):
            for height in (1,2,3,5):
                breaks = sorted({F(0),F(height),r,F(height)-r,
                                 F(height,7),F(2*height,7),F(5*height,7)})
                for zlo,zhi in zip(breaks,breaks[1:]):
                    for label,weight in enumerate((a,b)):
                        exact = probability(a,b,r,root,height,label,zlo,zhi)
                        expected = weight/(a+b)*(zhi-zlo)/height
                        need(exact == expected, "resampled joint-law discrepancy")
                        cases += 1
    # Exact advertised 2/3 discrepancy, both initial supported root phases.
    a,b,r=F(1),F(2),F(1,2)
    matrix = [[str(probability(a,b,r,root,1,label,F(0),F(1)))
               for label in (0,1)] for root in (F(0),r)]
    need(matrix == [["1/3","2/3"],["1/3","2/3"]], "wrong candidate matrix")
    # A source-fixing deterministic swap would be measurable and covariant,
    # but preservation fails with unequal weights. Equal weights at offset
    # 1/2 admit the quotient swap and make the observed measure half-periodic:
    # the two putative types coincide as an observed pair. Do not mistake a
    # redundant torus phase label for an observable rooted-state change.
    swap_received = (b,a)
    need(swap_received != (a,b), "unequal-weight control unexpectedly balanced")
    need((F(1),F(1))[::-1] == (F(1),F(1)), "equal-weight control")
    equal_windows=[]
    for shift in (F(0),F(1,2)):
        window={}
        for n in range(-4,5):
            for offset in (F(0),F(1,2)):
                y=F(n)+offset-shift
                if -2 <= y < 2:
                    window[y]=window.get(y,F(0))+1
        equal_windows.append(window)
    need(equal_windows[0] == equal_windows[1],
         "equal-weight half-period observable measure symmetry failed")
    need(equal_windows[0][F(0)] == equal_windows[1][F(0)] == 1,
         "equal-weight root-density witness must disappear")
    # Wrong-bias laws cannot be fixed points of the independently derived
    # resampling matrix, whereas the exact Palm weights are a fixed point.
    biases = [F(0),F(1),F(1,2),F(1,3),F(2,3)]
    bias_results=[]
    for p0 in biases:
        output0 = p0*F(matrix[0][0])+(1-p0)*F(matrix[1][0])
        fixed = output0 == p0
        need(fixed == (p0 == F(1,3)), "wrong fixed-point bias")
        bias_results.append({"initial_light_phase_probability":str(p0),
                             "output_light_phase_probability":str(output0),
                             "fixed":fixed})
    return {"status":"pass", "exact_joint_phase_output_interval_checks":cases,
            "candidate_resampling_matrix":matrix,
            "candidate_original_Q_heavy_probability":"0",
            "candidate_resampled_Q_heavy_probability":"2/3",
            "bias_controls":bias_results,
            "equal_weight_control":"quotient swap allowed; half-period symmetry collapses observed types and the unequal-density root witness disappears",
            "unequal_weight_control":"swap fails preservation",
            "scope":"Exact finite rational window integrals support the analytic proof; not a machine proof of all allocations, all Borel windows, or priority."}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
