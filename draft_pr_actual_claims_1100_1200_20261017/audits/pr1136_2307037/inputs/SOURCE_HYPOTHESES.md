# Source hypotheses and their verified application

Accepted exact result: one compact exceptional set of area pi works for all R>1, with C=pi(log(2)+1/e). The complete argument is PROOF.md; the independent AI-assisted audit is AUDIT.md. This note does not claim historical novelty.

## Imported mathematical inputs

1. Eremenko–Hamilton, Proceedings AMS 123 (1995), pp. 2793–2797, DOI https://doi.org/10.1090/S0002-9939-1995-1283548-8 . Primary PDF: https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf .
   - Exact needed display is on printed p. 2794 / PDF page 2: the integral of |T chi_E| on Delta minus E is at most |E| log(pi/|E|).
   - Kernel normalization there is -1/pi times the principal-value integral with denominator (z-zeta)^2.
   - Ambient Delta may be the closed unit disk, and E is any measurable subset. The proof of this transform estimate ends on printed p. 2797 / PDF page 5.
   - No additive term, pole assumptions, or point-mass approximation is imported from this theorem.

2. Levine–Peres, Journal d'Analyse Mathematique 111 (2010), pp. 151–219, DOI https://doi.org/10.1007/s11854-010-0015-2 . Inspected May 1, 2009 author manuscript: https://lionellevine.github.io/scalinglimit.pdf . Related versioned preprint: https://arxiv.org/abs/0712.3378v2 .
   - Definition (4): smash sum is the union of the input open sets and an obstacle-problem noncoincidence set. Thus it contains the input disks.
   - Proposition 2.12, manuscript/PDF p. 16: for a bounded, compactly supported density continuous almost everywhere, with a gap between densities below one and densities at least one, the enlarged noncoincidence set has null boundary and conserves mass.
   - Corollary 2.13, p. 17: binary smash sums of bounded open sets with null boundary have additive volume.
   - Lemma 2.15, p. 17: the noncoincidence set is bounded for bounded compactly supported nonnegative initial density.
   - Lemma 6.1, p. 54: associativity for bounded open sets with null boundary.
   - Proposition 6.6, p. 58, proof p. 59: arbitrary finitely many positive point masses are represented by the smash sum of the centered balls of corresponding volumes, in the superharmonic quadrature inequality. Applying it to each sign of a real harmonic function gives equality.
   - The application uses masses pi*lambda_j, not lambda_j, and disks of radius sqrt(lambda_j).
   - Finite disk-indicator sums satisfy the density-gap and almost-everywhere continuity assumptions; null boundary and boundedness are preserved at every binary iteration. The sets may be disconnected; overlap and arbitrary locations are allowed.

## Items for adversarial checking

- Combining repeated poles preserves positivity and total mass.
- Closure of the quadrature set has exactly the same area because its boundary is null.
- For each z outside this fixed closure, (w-z)^(-2) is bounded and holomorphic on a neighborhood of it. Both real and imaginary parts are admissible harmonic test functions, even when z lies in a bounded complementary component.
- Quadrature gives integral kernel = pi*g; the Beurling normalization therefore gives T chi_Omega = -g.
- The only radius-dependent objects are auxiliary near/far pieces of Omega, never the exceptional set S.
- The near term uses the scaled sharp estimate on D_(sqrt(2)R).
- The far term uses the exact ordinary integral over D_R of |z-w|^(-2), equal to pi log(|w|^2/(|w|^2-R^2)).
- The final scalar inequality is t log(1/t)<=1/e on [0,1]; R>1 makes replacement of 2a log R by 2pi log R valid.
- The proof never estimates an uncancelled sum of positive inverse-square kernels over a many-pole near field, never differentiates a first-order weak estimate, and never interprets the target integral as a principal value.

## Source identities and inspection scope

Public source URLs, PDF byte counts, SHA-256 identities, retrieval history and inspection coverage are recorded in SOURCE_METADATA.json and SOURCE_DEPENDENCIES.json. The author manuscript and arXiv v2 of Levine–Peres have different PDF bytes; locators above refer to the inspected author manuscript. No complete-version identity is claimed. The entire 74-page article is not claimed to have been fully audited. The Hayman–Lingham update reports the editors’ knowledge at its date and is not a global current-openness certificate.
The mathematical bridge requires both imported inputs and the supplied localization proof; the downstream transform theorem alone does not establish the squared-pole conclusion. The complete deduction has passed the independent internal AI-assisted audit in AUDIT.md. The manuscript and audit are unrefereed.
