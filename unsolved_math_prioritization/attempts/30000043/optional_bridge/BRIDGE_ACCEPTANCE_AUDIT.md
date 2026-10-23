# Independent audit of the universal dual-to-tight bridge

Date: 2026-10-14 UTC.

## Reviewed artifact

Title: *A rigorous dual-to-tight bridge using complex perturbations*.

SHA-256: `aeedf3442b91df6d1f9316fccb8f60d99f422cd3a94f457086cef14867728c35`.

Byte count: `7808`.

## Verdict

**Accepted as an optional, independent existence proof for the stated complex-Hilbert-space, fixed-index contract.** The original explicit real Haar counterexample does not depend on this lemma. Neither proof implies an impossibility under arbitrary reindexing or a changed lattice.

The proof correctly distinguishes a universal closure property over all complete frame generators from the corresponding property of one fixed generator. It never asserts that canonical-dual failure at a generator implies canonical-tight failure at that same generator.

## Checked mathematical steps

1. Under canonical-tight preservation for `x`, its canonical Parseval atoms have the required orbit form `y_i=U_i y`. With `A=F^(1/2)`, the new single-generator orbits for `x±it y` are exactly `(A±itI)y_i`.
2. The Parseval synthesis identity gives their exact frame operators `(A±itI)(A∓itI)=F+t²I`. The complex scalar and self-adjointness of `A` make the cross terms cancel. No global commutation with the orbit operators is needed.
3. Subtracting the two canonical-tight covariance identities at a common nonzero `t` gives local covariance of `(F+t²I)^(-1/2)` at `y`. Operator-norm convergence as `t→0` yields canonical-dual covariance at `x`. This proves universal canonical-tight closure implies universal canonical-dual closure.
4. The quantitative estimate `||(F+t²I)^(-1/2)−F^(-1/2)||≤t²/(2a^(3/2))` follows from the scalar derivative bound on `[a,∞)`. Because `||y_i||=||y||`, the stated error bound for the dual-defect vector and the maximum-of-two-signs lower bound follow with the printed constants.
5. The optional converse uses well-defined positive scalar functions of `A`. Universal dual covariance validates every recursive generator. The change of variable `(u−1)/(u+1)` squares at each Newton step, uniformly on the compact spectral interval after the first iteration, so the claimed norm limit is justified.
6. The classical application keeps exactly one generator in `L²(R;C)`, the physical dyadic dilation, integer translation lattice, and original pair of indices. It introduces no abstract-representation substitution.

## Source and scope checks

Bownik–Lemvig, *The canonical and alternate duals of a wavelet frame*, ACHA 23 (2007), 263–272, supplies the canonical-dual counterexample used in the application. Theorem 1 gives a single-generator dyadic frame; the indexed canonical-dual covariance convention is stated on p.265. The source is https://pages.uoregon.edu/mbownik/papers/29.pdf . The audited application correctly relies on the corrected 2007 argument, rather than its flawed 2002 predecessor.

The complex perturbations do not, by themselves, prove an assertion restricted to real-valued generators. The optional converse has no such restriction. The proof makes no claim of mathematical novelty, source-text reproduction, or historical priority.
