# Recovery proof turn 4: modulus invariance does not imply onto

2026-10-03. Recovery turn 4/5; historical count unknown. Original unresolved. Completion estimate 20%, subjective coverage. We test the tempting analytic route: Loewner gives positive modulus and QS maps control modulus; can that force all of the ambient space to be covered? The computation identifies the missing premise exactly.

## Complete modulus calculation for rectangles

Let R=∏_{i=1}^n[0,a_i], all a_i>0, n≥2. Let Γ be all rectifiable curves in R connecting the faces x_n=0 and x_n=a_n. For p≥1 define Mod_p Γ using Euclidean arclength and n-dimensional Lebesgue measure on R. Then

  Mod_p Γ = (∏_{i<n}a_i) a_n^(1−p).

For the upper bound use the constant density ρ=1/a_n: every connecting curve has length at least a_n, so ρ is admissible and its p-energy is the stated expression. For the lower bound, every vertical segment γ_z(t)=(z,t), z∈∏_{i<n}[0,a_i], belongs to Γ. Admissibility gives ∫_0^{a_n}ρ(z,t)dt≥1. Holder's inequality (or the identity at p=1) gives ∫_0^{a_n}ρ(z,t)^p dt≥a_n^(1−p). Integrate in z by Tonelli to obtain the matching lower bound. This proves the exact formula, not only a discretized approximation.

For a similarity S(x)=sx+b, s>0, and any curve family Γ in a Euclidean domain Ω,

  Mod_p(SΓ;SΩ) = s^(n−p) Mod_p(Γ;Ω).

Indeed transporting densities by ρ'(Sx)=ρ(x)/s preserves admissibility and scales energy by s^(n−p); apply the inverse similarity for the reverse bound. Infinite values cause no problem since each direction is an inequality. At p=n the modulus is exactly invariant.

## Countermodel to the proposed inference

Take Ω=[0,1]^n and S(x)=x/2. This is a proper similarity embedding. It preserves the critical n-modulus of every family of curves transported into the image, not merely the rectangular test family. All cross-face test moduli equal 1 before and after scaling. Thus even perfect critical modulus preservation, with a QS distortion of t, cannot by itself imply surjectivity.

This is not a counterexample to the source conjecture, because the cube is not asserted to be a group boundary. The calculation isolates why positive-modulus and change-of-variables arguments need an additional global hypothesis.

## Where ambient Loewner estimates fail to close the proof

Suppose f:X→X is a QS embedding and Y=f(X) is proper. The target Loewner inequality can produce many curves between a continuum in Y and a continuum in a missing ball, if those continua are chosen in its domain of applicability. Such curves need not lie in Y. There is no inverse-image curve family through f for the second continuum, so a QS modulus comparison for f:X→Y cannot be applied to that ambient family.

Conversely, for a curve family Γ in X, fΓ lies wholly in Y. In computing its modulus with ambient Hausdorff measure on X one may set an admissible density to zero outside Y: the extra ambient region imposes no constraint for those curves. Consequently no contradiction follows merely from the existence of a missing ambient ball.

A further regularity issue cannot be suppressed: the standard Tyson theorem as stated in Bonk–Kleiner Theorem 2.7 assumes both source and target are Ahlfors Q-regular and the map is a homeomorphism between them. An arbitrary subset Y=f(X) has not been proved Ahlfors Q-regular in the ambient metric. Invoking that theorem with target X would incorrectly assume the desired surjectivity; invoking it with target Y requires verifying its hypotheses. The rectangle example remains a countermodel even when both are regular.

## Conditional closure and exact gap

One sufficient route would be to prove an independent ambient-curve lifting property: every ambient curve connecting appropriate continua in Y is, up to a modulus-zero exceptional family, represented inside Y in a manner forcing the missing regions to have zero capacity. No such property is proved here, and no consequence of QS alone gives it. A QS map controls the curves it transports, not every ambient curve.

The source Loewner condition supplies nondegenerate modulus estimates; the still-missing ingredient is the compatibility of an arbitrary image with the boundary's global group structure. The present turn rejects a circular full proof and saves an exact analytic countermodel for further audits.
