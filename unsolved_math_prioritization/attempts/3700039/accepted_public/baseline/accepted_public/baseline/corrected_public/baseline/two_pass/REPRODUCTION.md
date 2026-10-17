# Exact reproduction conventions

## What this edition contains

This edition contains authored mathematical reports, their complete mathematical audits, exact finite certificate arrays, and a focused proof clarification. The source PDF is cited rather than copied. No program, third-party source text, external dataset, exploratory optimizer output, or private coordination record is part of the reader edition.

The mathematical original of the rotating-separable proof and its corrected copy are both included, together with an exact unified diff. The change replaces distributional slicing shorthand with positive angular mollification; it changes no theorem hypothesis or conclusion. Other reader edits remove operational material, add local document links, and separate exploratory searches from mathematical acceptance.

## Angular and Fourier conventions

1. I and every L1 norm use dtheta on [0,2*pi]. M(s) is an unnormalized angular integral. M(s)/(2*pi) is an angular mean. The normalized conjecture is I/B, not the mean and not a value at one chosen phase.
2. Circular convolution uses (1/(2*pi))*integral. The Fejer kernel has integral 2*pi with respect to dtheta, or normalized integral one. Its multiplier at integer n is 1-|n|/(N+1) for |n|<=N and zero otherwise.
3. Periodic Fourier series use exp(i*(m*s+n*theta)). A stored coefficient pair [a,b] means a+i*b, with each entry an exact rational string. Index keys "m,n" name the two integer frequencies. The operator multiplier is (rho+i*omega*m)^2-n^2.
4. At s=0, sum the two-variable coefficients over m. At s=pi, first multiply each by (-1)^m. Conjugate symmetry gives a real angular slice. From its n=0,1,2 coefficients, the real value is a_0+2*sum_(n=1)^2 [Re(a_n)*cos(n*theta)-Im(a_n)*sin(n*theta)].
5. The three profiles are rotations by 0, 2*pi/3 and 4*pi/3. On an N-point grid with 3 dividing N, these are exact index shifts by 0, N/3 and 2N/3. A median is the middle of the three values, including ties.

## First-pass finite certificate

The [first-pass certificate](certificates/first_pass_exact.json) gives all three exact radius regimes, the two junction values and the zero normalized endpoint limits of the root-of-unity harmonic example. Reproduce the integrals by evaluating the sine primitive at the sector endpoints listed in the [proof](proofs/first_pass_theory.md), rather than by angular sampling.

For the Fejer witness use N=9999, n=10000. The ten-term rational sum of exp(10) is 5719087/567>10000. Thus log(10000)<10 and the relative median error is strictly below 189/20000<1/100. Positivity and unit mass of the kernel give 0<B_N<=1. These statements certify a fixed-radius negative value, while the source's credited harmonic result still gives the normalized supremum assertion.

## Flat-scale finite certificate

The [flat-scale certificate](certificates/flat_scale_exact.json) records K_N=N(N+1)(N+2)/6 and the exact endpoint lower margins 27/16 and 10011/4096 in the two smooth flat examples. These follow by summing the weighted squares or evaluating the displayed lower polynomials in the [proof](proofs/second_pass_flat_scale.md). The analytic positivity and compactness arguments remain essential.

For the noncompact normalized-profile examples, the fixed-N L1 error tends to 4/5 for each component. When all three components are identical, E_N is the sum of three errors and tends to 12/5. Confusing one component with the sum would change a constant but would not make the angular compactness assumption automatic. Their actual median quotient is 8*pi/5 near the flat frontier, so these examples are affirmative.

## Exact mixed-sign certificate

The [Fourier certificate](certificates/log_periodic_exact.json) lists the integer trigonometric forcing P, all coefficients of P^2, and all exact solution coefficients for rho=3/2 and omega=2/25. Its full rational phase enclosures are retained. Reproduction requires no optimizer and no inferred floating-point sign:

1. Expand each cosine and sine into exponentials. Square P by finite coefficient convolution. Divide each forcing coefficient by its nonzero exact complex multiplier. Multiplication back by that multiplier must reproduce every forcing coefficient, with exactly the same support.
2. Reconstruct the phase-0 and phase-pi angular slices and compare every coefficient with the certificate.
3. Prove the given interval for pi from pi=16*atan(1/5)-4*atan(1/239), using alternating rational arctangent bounds. For the original 768-point certificate, 24 terms at 1/5 and 8 terms at 1/239 suffice.
4. Reduce all angular arguments to [-pi,pi]. Use sine and cosine Taylor polynomials through degree 32. With the midpoint of the stated pi interval, a common trigonometric error bound is 4^33/33! plus half the interval width.
5. Evaluate each rotated slice with rational arithmetic, take medians, and average. If D=2*sum_(n=1)^2 n*(|Re(a_n)|+|Im(a_n)|), the slice and its rotated median are D-Lipschitz. The normalized integral differs from its equal-grid average by at most D*pi/(2*N), by integrating distance to the grid point over each centered cell. Add the coefficient-weighted trigonometric error.
6. Compare the exact upper phase-0 endpoint to -1/3 and the exact lower phase-pi endpoint to 1. Display decimals are not acceptance criteria.

The independent reader check uses a different 1536-point grid and degree-26 Taylor polynomials, with sine through degree 25. Each Taylor value is rounded down to a multiple of 10^(-18). Its error is bounded by 4^27/27! plus half the pi interval width plus 10^(-18). The pi bound is independently obtained with 26 and 9 arctangent terms. The same centered-cell argument gives a second pair of rational enclosures, recorded with outward rounding to denominator 10^12 in [independent finite checks](certificates/independent_finite_checks.json). All acceptance comparisons are exact rational comparisons.

The separate [periodic audit certificate](certificates/periodic_audit_exact.json) uses a third, 600-node reconstruction. Its full real cosine/sine algebra, independent pi interval, Taylor remainder, rational complex-modulus bound and seven negative controls are explained in the [periodic audit](audits/second_periodic_acceptance.md). This is independent verification of the same two phases, not an extra research pass.

## Independent artifact checks and negative controls

The reader checks reconstruct the forcing and solution coefficients from the displayed integer polynomial, verify every angular-slice coefficient and derivative bound, and establish both mixed-sign thresholds on the independent grid. They also reconstruct the exponential sum and finite sharpness inequalities, check the Fejer second-derivative identity at six specified integer values, and verify the exact flat-example margins. General identities and analytic conclusions are covered by the full proof audits, rather than inferred from finitely many evaluations.

Five deliberately invalid controls must fail: changing the solution's constant coefficient, omitting a Fourier mode, replacing the pi slice by the zero slice, reversing the negative enclosure, and replacing its strictly negative upper threshold with equality at -1/3. The [finite check record](certificates/independent_finite_checks.json) lists each actual rejection. A separate [public-artifact validator](certificates/public_artifact_checks.json) reloads the delivered exact arrays, reconstructs the polynomial coefficients, checks complete Fourier support and both phase slices, checks normalization and strict bounds, and verifies consistency with the independent grid. Its five additional corruption controls reject a changed delivered coefficient, a missing mode, wrong mean normalization, swapped phases, and equality at the strict negative threshold. Hashes and file inventories alone are not mathematical verification.

## Limits of verification

The positivity of subharmonic Laplacians, removable origins, Fejer approximation, compactness criteria, periodic Green singularity and global scope are analytic claims proved in the reports and reviewed in the linked audits. No finite grid can establish the missing all-phase negative certificate merely from sampled signs. No file-integrity or finite-artifact check establishes the unrestricted conjecture.
