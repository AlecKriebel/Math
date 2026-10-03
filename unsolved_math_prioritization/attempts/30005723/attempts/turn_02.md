# Attempt 2 of 5: a global quadratic multiplier produces a Yukawa tail

3 October 2026. Mechanism: use complex linearity and localization to test an
explicit mass-independent ansatz. Estimated full-target completion: 25%; the
global ansatz is obstructed under explicit domains, but the full target remains
unresolved.

Let n≥1, m>0, q(x)=1−|x|², ω=(−Δ+m²)^(1/2). Use a Fourier convention in which
∂_x corresponds to ip and x to i∂_p. For u in Schwartz space,

    Fourier[ωqωu] = ω(p)(1+Δ_p)(ω(p)û(p)),
    ω(p)=sqrt(|p|²+m²).

The elementary derivatives are

    ∂_jω=p_j/ω,
    ωΔ_pω=n−|p|²/(|p|²+m²)=n−1+m²/(|p|²+m²).

Consequently

    Fourier[ωqωu]
      = (|p|²+m²)(1+Δ_p)û + 2p·∇_pû
        +(n−1+m²/(|p|²+m²))û.

On the other hand, a direct Fourier calculation gives

    Fourier[(−∇·q∇+m²q)u]
      = (|p|²+m²)(1+Δ_p)û+2p·∇_pû.

Subtracting proves (2.1) in the report. This calculation keeps the nonlocal
m²A^−1 term; dropping it would reproduce precisely the sort of invalid local
candidate that a massless extrapolation risks.

For 0≤h∈C_c^∞(D), h≠0, the heat-kernel representation of A^−1 implies

    (A^−1h)(x)>0  for every x outside closure(D).

Indeed the integrand in (2.2) is strictly positive, and the integral against h
has positive measure of strictly positive contributions. At positive distance
from supp(h) all such integrals converge. The differential part of (2.1) is
supported in supp(h). Therefore ωqωh has a nonzero exterior tail for every
m>0. In dimension 3 this tail is explicitly

    m²∫_D exp(−m|x−y|)/(4π|x−y|) h(y) dy.

At m=0 the displayed residual disappears at the symbol level, in agreement
with the conformal formula in dimensions where the massless scalar realization
is available. We do not use a massless scalar vacuum in one spatial dimension.

## Modular implication, and its exact scope

If M_− is globally multiplication by cq (c≠0) on its natural domain and the
canonical identity M_+=ωM_−ω holds on C_c^∞(D), then M_+h has this exterior
tail. If (h,0) is in the modular generator domain, invariance of the closed
standard subspace under Δ_D^(it) forces the generator's value at (h,0) to be
supported in closure(D). Contradiction. These domain hypotheses are part of
the stated obstruction theorem. It is safe to apply it to a fully specified
global ansatz satisfying them, not to assume them for a merely formal kernel.

There is a useful conditional extension to quadratic global multipliers.
Rotation covariance would force a degree-at-most-two polynomial multiplier
to have the form a+b|x|² (reflection gives this in dimension 1). Entropy
positivity inside D and for the complementary standard subspace gives
f≥0 on D and f≤0 outside. Continuity at |x|=1 implies a+b=0, hence
f=a(1−|x|²), a≥0. The case a>0 is excluded by the tail. If a=0, both blocks
vanish under the conjugation relation, so Δ=I; a nonzero factorial standard
subspace cannot have Δ=I, since its Tomita involution is then a conjugation,
making its symplectic complement equal to itself. Thus no such quadratic
global ansatz satisfying the canonical domain/support conditions works.

**Limits.** A multiplier specified only inside the ball does not specify
ωM_−ωh, because ωh already has exterior support. An arbitrary radial multiplier
need not be a polynomial. Mass independence for m>0 does not automatically
identify the block with m=0 using strong-resolvent convergence. None of these
gaps is claimed closed by this calculation.

