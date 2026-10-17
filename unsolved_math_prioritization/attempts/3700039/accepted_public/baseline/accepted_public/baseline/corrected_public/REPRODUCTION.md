# Exact mathematical reproduction

## Scope and normalization

The proofs establish partial results; finite checks confirm the indicated identities and certificates. No symbolic calculation, finite sample, or successful integrity check establishes the unrestricted conjecture. The reader contains three documented shared substantive passes, with lifetime prior count unknown. Audits and reproduction do not add passes.

All angular integrals and L1 norms use dtheta. The cyclic median sector integrals in the [new reconstruction certificate](certificates/third_reader_exact.json) are unnormalized; the cyclic theorem explicitly divides by 2pi when using angular means. The prior mixed-sign example remains normalized as M(s)/(2pi).

## Frozen mathematical baselines

The included [two-pass manifest](baseline/two_pass/MANIFEST.json) has SHA-256 a0d04d609ebf1bc146a23a36e67d14142e226a18a309fee47eb80e03b5dea4b7. Its 24 payload entries, the manifest itself, original navigation, full proofs, four audits, and finite certificates are unchanged.

The included [independent supplement manifest](baseline/review/REVIEW_MANIFEST.json) has SHA-256 a5ad5937638e26e6746342532568638d87ab95aacf3ce69d11dcee44c844c0a9. Its [full acceptance](baseline/review/reader_edition_acceptance.md) and [fresh exact certificate](baseline/review/independent_reader_checks.json) are unchanged. The supplement's independent mathematical reconstruction and corrected self-contained reproduction are the accepted baseline for this edition. The earlier historical mathematical claims have not been silently strengthened.

The [prior reproduction guide](baseline/two_pass/REPRODUCTION.md) explains the original exact Fourier arrays and the 600-, 768-, and 1536-node rational enclosures. The supplement reconstructs a distinct 960-node enclosure with independent Laurent expansion, exact inversion, Taylor bounds, outward rational rounding, and invalid controls. These are exact rational enclosures, not floating-point angular quadrature.

## New concentration calculations

The [author concentration certificate](certificates/concentration_author.json) includes the Gaussian curvature norm, BV optimizer and cubed constant, cutoff Laplacian and margin, record comparison, exact negative mass and variations, and threshold optimum. Any displayed decimal is non-authoritative; the exact expressions are the certificate.

The [independent concentration certificate](certificates/concentration_audit.json) reconstructs the norm by endpoint derivatives, verifies all transition inequalities, record and boundary moments, mean-zero half-factors, a constructive negative-BV smoothing scale, global radial correction, and the negative-part noncompactness gap. It tests 9,261 integer median triples and 1,875 rational threshold cases. Invalid controls include the median one-third factor, omission of equal means, defect-free reversal of negative-part smoothing, incorrect doubled critical frequency, and radial differentiability inferred from angular smoothing.

The [complete analytic acceptance](audits/concentration_acceptance.md) separately proves continuity for actual subharmonic circle representatives, construction of positive slice measures, removal of affine integration constants by the zero left limit, ordered compactness limits, all-order smooth flatness, global extension, Fourier uniqueness, and honest maximum normalization. The finite certificate alone does not prove these assertions.

## New cyclic calculations

The [author cyclic certificate](certificates/cyclic_author.json) checks 24 identities. The [independent cyclic certificate](certificates/cyclic_audit.json) checks 40 identities and nine invalid controls. It reconstructs each angular median integral directly from ordering sectors and trigonometric primitives; it does not merely rescale the previously accepted harmonic result.

It also reconstructs the full helical operator before averaging, including amplitude derivatives, its covering-coordinate pullback, the positive reflection, every q interval with nonnegative-coefficient substitution, q=1 and q=4, the envelopes, scalar inverse orientation, and the strict rational gap. Continuous admissible examples disprove both purported Jensen directions. A harmonic zero-median example disproves an unqualified strict-positive claim. Incorrect branch factors, missing sign(b), drift deletion, omitted helical frequency, and a spurious second-harmonic test term are rejected.

The [full analytic acceptance](audits/cyclic_acceptance.md) covers distributional positivity, the positive scalar inverse for continuous amplitudes, every sign and zero case, smooth-test approximation, and continuity of the median integral. Those arguments justify the stated some-phase conclusion; the finite identities do not eliminate its subclass restrictions.

## Independent reader artifact reconstruction

The [third-reader certificate](certificates/third_reader_exact.json) supplies explicit exact mathematical values, not only success labels. A separate calculation reconstructs the heat norm from sign-change boundary derivatives, optimizes the BV loss, computes the cutoff margin, integrates the critical negative part, derives its variations and noncompactness lower bound, integrates all three cyclic ordering sectors, verifies both branch junctions and the envelopes, evaluates all three positive test polynomials, and reconstructs the helical coefficients by complex Fourier multipliers.

The 25 recorded checks include 729 finite median triples. Eight artifact corruptions are rejected: a changed heat factor, changed BV denominator, negated negative mass, changed small-branch coefficient, missing middle branch, omitted helical drift, relabeled angular normalization, and inflated cutoff margin. The mathematical fields are independently recomputed before comparison with the delivered certificate. No imported author or audit verifier is used for that new reconstruction.

This finite verification is reproduced in normal, -O and -OO modes with explicit exceptions. Optimization cannot disable its checks. Full author and independent audit results are reproduced separately; the prior corrected baseline is reconstructed and replayed independently as well.
