# Verification summary

## Mathematical checks

The proof checks:

1. A rational base field of characteristic two.
2. A purely inseparable extension of degree four and exponent two.
3. A genuine separable quadratic Artin–Schreier extension.
4. An anisotropic two-dimensional bilinear Pfister form that stays anisotropic over the inseparable extension.
5. The exact projective quasilinear function field and all field inclusions.
6. A class in the composite kernel, by two explicit Artin–Schreier differential identities.
7. Nonmembership in the full three-summand sum, by restriction, a cyclic-algebra norm criterion, total ramification, and an impossible square-class descent in the residue field.
8. The original `n=0` case, proved separately to satisfy the equality.

The nonmembership argument is quantified over every possible cyclic-kernel parameter `c∈F*`; it is not a search over finitely many parameters.

## Exact algebra diagnostics

Thirteen diagnostics passed under ordinary Python, Python `-O`, and Python `-OO`. They check characteristic-two rational-function identities by exact polynomial reduction, including:

- The descended coefficient `h²=bz²/(1+bz²)` and `dlog f=h dlog z`.
- Both Artin–Schreier parameter changes.
- The Eisenstein equation for the inverse Artin–Schreier root and its norm.
- An alternative tensor-rank expression of the residue obstruction: over `R`, a product of elements of `R(β²)` and `R(z)` has a rank-one coefficient matrix in the basis `{1,β²,z,β²z}`, whereas `1+β²z` has the identity matrix, of determinant one.
- Adverse controls that remove the obstruction: exponent-one degeneration and the absorbing Pfister slot `z`.
- Rejection of an incorrect power in the proposed descended coefficient.

These diagnostics validate finite exact identities; they are not a formalization of the field-theoretic or cohomological proof. The valuation, cyclic-kernel, norm, and linear-independence arguments were reviewed in the independent internal AI audit in AUDIT_REPORT.md. That mathematical review is separate from these diagnostics.

## Integrity and publication boundary

The accompanying integrity verifier checks an externally supplied manifest hash, exact byte counts and SHA-256 hashes, strict inventory, safe relative paths, and absence of symlinks. Its checks do not use Python assertions, so optimization flags do not disable them. This provides artifact integrity, not mathematical acceptance.

This summary, the authored counterexample, the source audit, the independent audit reports, and the public acceptance and source metadata constitute the authored public edition. Source copies, extracted source text, diagnostic code and raw outputs, and coordination/history materials are separate and are not candidate publication content.

The counterexample has been accepted by the independent internal AI mathematical audit. These authored documents remain unrefereed; this edition does not claim external human peer review, journal acceptance, formal proof-assistant certification, prior publication of these documents, or a new DOI.
