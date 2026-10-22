#!/usr/bin/env python3
"""Independent scope/nonapplication controls; not a literature-absence test."""
from fractions import Fraction as Q
import json
import math
from pathlib import Path


def run():
    controls = []

    def require(name, condition, detail):
        if not condition:
            raise AssertionError((name, detail))
        controls.append({"name": name, "pass": True, "detail": detail})

    for power in range(1, 9):
        alpha = beta = epsilon = Q(1, power)
        gamma = Q(2, power)
        chi = max(Q(0), Q(2, 3) * epsilon, (beta + epsilon) / 2)
        deficit = gamma - alpha - beta - chi
        require("HZ_size_parameter_power_" + str(power), deficit == -Q(1, power),
                {"gamma_minus_required": str(deficit), "strict_condition_holds": deficit > 0})

    for scale in range(8):
        alpha = beta = Q(1 + scale)
        gamma = Q(2 + scale)
        epsilon = Q(1)
        chi = max(Q(0), Q(2, 3), (beta + epsilon) / 2)
        deficit = gamma - alpha - beta - chi
        require("HZ_capacity_upscale_power_" + str(scale), deficit == -1 - Q(3, 2)*scale,
                {"gamma_minus_required": str(deficit), "strict_condition_holds": deficit > 0})

    # For fixed K, exact E[min((1+(1+delta)X)/2,K)] eventually lies below one.
    delta = 1e-12
    for cap in (1, 2, 3, 4, 8):
        limit = 1 - math.exp(-(2*cap - 1)) / 2
        value = 1 + delta/2 - (1 + delta)/2 * math.exp(-(2*cap-1)/(1+delta))
        require("KMN_fixed_truncation_" + str(cap), value < 1 and limit < 1,
                {"K": cap, "delta": delta, "truncated_mean": value,
                 "limit_mean": limit, "role": "Floating illustration of the analytic strict limit."})

    # Fixed finite capacity and traffic count restrictions, independent of any random replay.
    for height in range(2, 10):
        leaves = 2**(height-1)
        vertices = 2**(height+1)-1
        edges = vertices-1
        require("tree_OD_scaling_height_" + str(height),
                vertices == 4*leaves-1 and edges == 4*leaves-2,
                {"k": leaves, "vertices": vertices, "physical_edges": edges,
                 "OD_streams": leaves**2, "leaf_capacity": 2*leaves,
                 "top_edge_capacity": 2*leaves**2})

    # Exact finite min-cut envelope, k=2, all four positive rates equal two.
    k = 2
    rates = [[Q(2) for _ in range(k)] for _ in range(k)]
    candidates = []
    for A in range(1 << k):
        for B in range(1 << k):
            a = A.bit_count()
            b = B.bit_count()
            pairs = [(i,j) for i in range(k) for j in range(k)
                     if A >> i & 1 and not (B >> j & 1)]
            intercept = Q(2*k*(k-a+b) + len(pairs))
            slope = sum((rates[i][j] for i,j in pairs), Q(0))
            candidates.append((intercept, slope))
    value = min(i for i,s in candidates)
    derivative = min(s for i,s in candidates if i == value)
    actual_slope = sum((x for row in rates for x in row), Q(0))
    require("finite_actual_slope_normalization", value == 4 and derivative/actual_slope == 1,
            {"F_at_t1": str(value), "right_derivative": str(derivative),
             "actual_offered_slope": str(actual_slope), "normalized": str(derivative/actual_slope)})
    require("finite_initial_total_normalization_differs", derivative/(k*k) == 2,
            {"initial_total": k*k, "normalized": str(derivative/(k*k)),
             "role": "Refutes an exact finite r=1 claim using the deterministic initial denominator."})

    variances = [(Q(t)-1)**2 for t in (1,2,3)]
    require("affine_growth_variance_not_linear", variances[2] - 2*variances[1] + variances[0] == 2,
            {"times": [1,2,3], "variances": [str(v) for v in variances]})

    return {"schema": 1, "all_passed": True, "count": len(controls), "controls": controls,
            "scope": "Specific prior-theorem nonapplication and scope restrictions only. No proof of novelty, no full model replay, no empirical tail-asymptotic certification."}


if __name__ == "__main__":
    result = run()
    Path(__file__).with_name("SCOPE_PRIORITY_CONTROLS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"all_passed": result["all_passed"], "count": result["count"]}))
