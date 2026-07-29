"""Exact checks for the covariant endpoint-compression no-go theorem.

Only standard-library rational arithmetic is used.  The checker verifies
the invariant equations, the required endpoint ratio, the compression
lower bound, and the strict obstruction for a representative range of
integer dimensions.  The symbolic difference printed in the note is also
checked directly.
"""

from fractions import Fraction as F


def required_ratio(dimension: int) -> F:
    return -F(dimension - 2, 2 * dimension - 1)


def compression_lower_ratio(output_dimension: int) -> F:
    return -F(output_dimension - 2, 2 * output_dimension - 1)


def scalar_to_traceless_ratio(ambient_dimension: int, h_over_tau: F) -> F:
    d = F(ambient_dimension)
    return h_over_tau * (d * d - 1) / (d - h_over_tau)


for d in range(3, 20):
    for k in range(2, d):
        tau = F(k) * (F(k) - F(1, 2))
        minimum_h = -F(k * (k - 2), 2)
        assert minimum_h / tau == compression_lower_ratio(k)
        assert compression_lower_ratio(k) > required_ratio(d)

        # Cross-multiplication of the two positive denominators gives
        # exactly 3(d-k), the strict gap used in the proof.
        gap_numerator = (
            (d - 2) * (2 * k - 1)
            - (k - 2) * (2 * d - 1)
        )
        assert gap_numerator == 3 * (d - k)

        # The corresponding identity-to-traceless eigenvalue ratio is
        # strictly larger than the endpoint ratio.  This is the scalar
        # obstruction which survives arbitrary correlated tensor mixtures.
        endpoint_scalar_ratio = F(1) - F(d, 2)
        assert scalar_to_traceless_ratio(
            d, required_ratio(d)
        ) == endpoint_scalar_ratio
        assert scalar_to_traceless_ratio(
            d, compression_lower_ratio(k)
        ) > endpoint_scalar_ratio


# Audit the invariant linear equations and their endpoint solution.
for d in range(3, 12):
    for k in range(2, d + 1):
        tau = F(k) * (F(k) - F(1, 2))
        c = tau / (F(d) * (F(d) - F(1, 2)))
        e = -c / 2
        h = c * F(d) * (F(1) - F(d, 2))

        assert c * d * d + e * d == tau
        assert c + e * d == h / d
        assert h / tau == required_ratio(d)

        c_from_invariants = (tau - h / d) / (d * d - 1)
        assert c_from_invariants == c
        assert (h / d) / c == F(1) - F(d, 2)

        if k < d:
            assert h < -F(k * (k - 2), 2)
        else:
            # The only non-obstructed case in this loop is k=d.
            assert k == d
            assert h == -F(k * (k - 2), 2)


print("endpoint covariant compression no-go: exact checks passed")
