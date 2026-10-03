# Attempt 1 of 5: mass differentiation of spectral calculus

3 October 2026. Mechanism: prove nonconstancy by differentiating the defining
operator formula, rather than inferring it from plots. Estimated completion
toward the full two-part target: 10%; no resolution.

Work first in finite dimension, where A(λ)=A₀+λI is strictly positive, χ is an
orthogonal projection, and the one-particle standardness conditions hold.
Write C=A^(1/4)χA^(−1/4), B=C+C*−I, F=arcoth B, E=A^(−1/4), and M=2EFE.
Here λ=m². On an open interval where spec(B) avoids [−1,1], all the following
derivatives exist:

    C′ = (1/4)[A^−1,C],
    (C*)′ = −(1/4)[A^−1,C*],
    B′ = (1/4)[A^−1,C−C*],
    E′ = −(1/4)A^−1E.

For any selfadjoint B with a spectral gap around [−1,1],

    arcoth B = (1/2)∫₀¹ [(B−tI)^−1+(B+tI)^−1] dt.

Differentiating resolvents therefore gives the exact Fréchet derivative

    DF_B(X) = −(1/2)∫₀¹ [(B−t)^−1 X (B−t)^−1
                        +(B+t)^−1 X (B+t)^−1] dt.

Inserting the product rule yields

    M′ = −(1/4)(A^−1M + MA^−1) + 2E DF_B(B′)E.                (1.1)

Thus M′=0 is equivalent in finite dimension to the cancellation equation

    DF_B(B′) = (1/4)(A^−1 F + F A^−1).                        (1.2)

This demonstrates a concrete defect in a tempting argument: B′≠0 does not
imply M′≠0. Both exterior factors also vary. The exactly known massive wedge
is a physical example where total cancellation occurs.

Attempt 4 tests (1.1) in a genuinely standard finite-dimensional model and
finds nonconstancy there. To prove nonconstancy for the double cone using
(1.1), one must justify differentiating the Sobolev cutting projection formula,
control the resolvents as t→1, and find a nonzero continuum matrix element of
the residual. These steps have not been established. In particular, χ is not
being assumed bounded at the critical Sobolev index; the finite formula is not
silently extended to the continuum.

**Outcome:** exact finite-dimensional derivative/cancellation criterion;
continuum proof route blocked at domain and endpoint control.

