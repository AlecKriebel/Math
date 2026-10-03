#!/usr/bin/env python3
"""Small exact algebra checks for REPORT.md, not a proof of the gap theorem.

Only rational arithmetic is used. Symbols standing for cosh, sinh, and
displacement bounds are supplied as positive rationals. Analytic inputs and
geometric covering assertions are outside this script's scope.
"""
from fractions import Fraction as Q
import json


def run():
    checks = {"ball_area_rearrangement": 0,
              "finite_subgroup_threshold": 0,
              "class_count_rearrangement": 0,
              "tube_count_rearrangement": 0,
              "cover_ratio_rearrangement": 0}
    for g in range(2, 52):
        # Area / (2*pi): cosh(ell/2)-1 <= 2(g-1).
        boundary_cosh = Q(2*g-1)
        assert boundary_cosh - 1 == 2*(g-1)
        checks["ball_area_rearrangement"] += 1
        # N=84(g-1) forces cosh(D0(K^2)) >= 43/42.
        assert 84*(g-1)*(Q(43,42)-1) == 2*(g-1)
        checks["finite_subgroup_threshold"] += 1
        for t in (Q(101,100), Q(3,2), Q(2), Q(5)):
            # Exact cosh(log(t)) and sinh(log(t)).
            b = (t + 1/t)/2 - 1
            s = (t - 1/t)/2
            assert b > 0 and s > 0
            n = 2*(g-1)/b
            assert n*b == 2*(g-1)
            checks["class_count_rearrangement"] += 1
            for k in (Q(101,100), Q(6,5), Q(2)):
                ell = Q(7,3)
                # m/pi = 2(g-1)/(K*ell*sinh(C)).
                m_over_pi = 2*(g-1)/(k*ell*s)
                assert m_over_pi*k*ell*s == 2*(g-1)
                checks["tube_count_rearrangement"] += 1
    for ell in (Q(1), Q(3), Q(10), Q(100), Q(1000)):
        for diameter in (Q(1), Q(7,3), Q(10)):
            upper_d = ell + 2*diameter
            assert upper_d/ell - 1 == 2*diameter/ell
            assert upper_d >= ell
            checks["cover_ratio_rearrangement"] += 1
    return {"result": "passed", "arithmetic": "exact fractions",
            "checks": checks, "total_checks": sum(checks.values()),
            "scope": "algebraic rearrangements only; no analytic theorem or universal gap verified"}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
