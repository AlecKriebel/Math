#!/usr/bin/env python3
"""Own stdout-only arithmetic diagnostics; no native code or file access."""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json


def add(z, w):
    return (z[0] + w[0], z[1] + w[1])


def mul(z, w):
    return (z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0])


def inv(z):
    norm = z[0]*z[0] + z[1]*z[1]
    assert norm > 0
    return (z[0]/norm, -z[1]/norm)


def field(z, center, radius_squared):
    delta = (z[0]-center[0], z[1]-center[1])
    reciprocal_squared = mul(inv(delta), inv(delta))
    return tuple(radius_squared*x for x in reciprocal_squared)


def pair(z):
    return [str(x) for x in z]


def main():
    qzero = (Q(0), Q(0))
    centers = [(Q(-2), Q(0)), (Q(2), Q(0))]
    points = [(Q(0), Q(0)), (Q(0), Q(1)), (Q(3), Q(0))]
    expected = [(Q(1, 4), Q(0)), (Q(3, 25), Q(0)), (Q(13, 25), Q(0))]
    fields = []
    for z, want in zip(points, expected):
        for c in centers:
            assert (z[0]-c[0])**2 + (z[1]-c[1])**2 > Q(1, 2)
        g = qzero
        for c in centers:
            g = add(g, field(z, c, Q(1, 2)))
        assert g == want
        transform = tuple(-x for x in g)
        assert add(g, transform) == qzero
        fields.append({"z": pair(z), "g": pair(g), "T_union": pair(transform)})

    hole_z = (Q(1, 2), Q(0))
    hole_actual = qzero
    hole_wrong = tuple(-x for x in field(hole_z, qzero, Q(1)))
    assert hole_actual != hole_wrong == (Q(-4), Q(0))
    exterior_z = (Q(2), Q(0))
    annulus_exterior = add(tuple(-x for x in field(exterior_z, qzero, Q(2))),
                           field(exterior_z, qzero, Q(1)))
    assert annulus_exterior == (Q(-1, 4), Q(0))
    assert Q(1, 2) + Q(1, 2) == 1
    assert Q(1, 2) != 1  # coincident naive union has wrong normalized area

    ratios = []
    for r2 in [Q(1), Q(9, 4), Q(100)]:
        for factor in [Q(2), Q(5, 2), Q(3), Q(10)]:
            rho2 = factor*r2
            ratio = rho2/(rho2-r2)
            assert 1 < ratio <= 2
            ratios.append({"R_squared": str(r2), "rho_squared": str(rho2), "ratio": str(ratio)})

    scalar = []
    with localcontext() as ctx:
        ctx.prec = 70
        one = Decimal(1)
        critical = (-one).exp()
        log_two = Decimal(2).ln()
        for R in [Decimal("1.0001"), Decimal("1.5"), Decimal(2), Decimal(10)]:
            for t in [Decimal(0), Decimal("0.01"), critical, Decimal("0.5"), one]:
                entropy = Decimal(0) if not t else -t*t.ln()
                split = 2*t*R.ln() + log_two + entropy
                target = 2*R.ln() + log_two + critical
                assert split <= target
                scalar.append({"R": str(R), "a_over_pi": str(t), "entropy": str(entropy), "target_minus_split": str(target-split)})

    print(json.dumps({"kind": "own arithmetic diagnostics, universal proofs in accompanying text",
                      "native_executions": 0, "exact_two_disk_fields": fields,
                      "hole_wrong_alternative": {"z": pair(hole_z), "actual_T_annulus": pair(hole_actual), "wrong_exterior_continuation": pair(hole_wrong), "outside_T_annulus": pair(annulus_exterior)},
                      "exact_kernel_ratios": ratios, "decimal_scalar_diagnostics": scalar,
                      "all_assertions_passed": True}, indent=2))


if __name__ == "__main__":
    main()
