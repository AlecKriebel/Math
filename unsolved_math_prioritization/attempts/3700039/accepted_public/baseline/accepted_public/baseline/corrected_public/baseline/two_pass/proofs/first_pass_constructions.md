# First shared substantive pass: exact construction limits

Problem: row 1762 / 3700039 / AMR-036-0039, the normalized circular median inequality for three whole-plane subharmonic functions with u_j(0)=0.

Disposition: **partial results only; the unrestricted target is unresolved in this pass.** No counterexample or general proof is claimed. This is part of the first documented substantive pass, not an additional pass; lifetime prior count is unknown.

## Verified mathematical results

1. [common_spiral.md](common_spiral.md): If all three functions are r^rho h_j(theta-kappa log r) with common rho>0 and common kappa, subharmonicity gives a common weighted half-period inequality. The median inherits it. Hence I(r,median)>=0 at every radius. This excludes common spiral-homogeneous counterexamples and extends the source's credited kappa=0 case, without a novelty claim.

2. [rotating_separable.md](rotating_separable.md): More generally, any common positive C^2 amplitude F(log r)->0 at the origin and common C^2 rotation psi(log r) of three fixed continuous periodic angular profiles has the same nonnegative-integral conclusion. A constant-coefficient angular lemma handles either complex roots by half-period pairing or real roots by positivity of the periodic inverse. Changing angular shapes, unequal amplitudes and unequal drifts remain outside the argument.

3. [compact_potential.md](compact_potential.md): Positive finite compactly supported logarithmic measures of finite absolute log moment, plus polynomial harmonic parts normalized to vanish at 0, satisfy the target. At infinity, either every function is eventually nonnegative or the highest harmonic degree gives a median numerator o(B), so I/B->0. This excludes finite atomic and compact-mass polynomial-potential constructions, even when their finite-radius median integrals are negative.

4. [log_periodic_reduction.md](log_periodic_reduction.md): An exact sufficient route to a genuine counterexample is a continuous doubly periodic triple H_j(s,theta) with ((omega*d_s+rho)^2+d_theta^2)H_j>=0 and strictly negative angular median integral at every s. Positive square-trigonometric forcing and explicit nonresonant Fourier inversion produce admissible entire subharmonic candidates. No uniform negative certificate was found.

All formulae in the proof notes use the source's unnormalized angular integral. B=0 is classified in the [theory report](first_pass_theory.md); the partial conclusions above concern B>0 except where the median integral itself is proved nonnegative.

## Exploratory search does not enter acceptance

Finite-grid searches found no certified uniformly negative periodic candidate. Tiny sampled values near a Fourier resonance can be explained by a large approximately harmonic denominator. Grid maxima need not control the continuum supremum, and a sampled angular maximum underestimates the actual maximum. No exploratory sign, optimizer statistic, or failure to find a candidate is used as a theorem in this edition.

## Remaining obstruction

The genuinely unrestricted task allows angular shape changes at every scale, noncompact or infinite Riesz mass, and nonpolynomial harmonic components. None of the proven construction exclusions controls all of these. A negative median at one radius, a negative sampled phase, or failure of a stronger local statement would not refute the target. Any continued construction search must maintain a strict negative normalized bound across every positive radius, or otherwise explicitly prove that the supremum is negative.
