# Acceptance record and controlling conventions

Date: 7 October 2026. Target: 30005481 / OWR-12697711-017 (rank 951).
Disposition: **accepted scoped partial results; original conjecture unresolved;
five of five substantive approaches used**.

The independent audit accepts the full submitted partial-result package subject
to one theorem-preserving wording correction. The original manifest is pinned at
`a59097544b285a4d5452cad2b8dac7d80d4f437098b123f71e04ad06242d9fa7`.
The independent audit manifest is pinned at
`5f2be175c5830e1d41f901e287c57c6d56c5d0084255519c83c3aa972624ebf1`.
The corrected proof reading copy is pinned at
`f2e0e866b9ae517ea1cdb3181546ab67f6afccd9dd604d537c64c3960984c65f`.
All original bytes, audit bytes, the exact patch and its correction metadata are
preserved. The wording correction is exactly “scalar multiple” to “nonzero
scalar multiple” in the sentence identified by `CORRECTION.json`; there are no
other changes in the corrected reading copy.

## Explicit source convention

“Diagonal” is degree-shifted: for input degree bound n and output degree bound d,

    T(t^(n-i)) = gamma_i t^(d-i) for i <= d,
    T(t^(n-i)) = 0 for i > d.

The centered domain omits i=1; an extension supplies that coefficient and acts
on the entire degree-bounded input space. The source uses this convention in
Definition 1.7 and Section 4.1, and the inverse-symbol argument uses it in Section
5.2. The present arguments take 1 <= d <= n and nonzero symbol leading
coefficients. They make no claim for omitted degenerate conventions or d>n.

The associated operator is defined using p(r-t e), not p(r+t e). The exact base
quintic identity is T_p((t-1)^4(t+4)) = -750(t-1)^2(t-2)^2(t+6).
Multiplication by the nonzero scalar -1/750 preserves extendability; multiplication
by zero does not preserve the equivalence of extendability statuses.

Weak SOS-hyperbolicity requires an SOS Wronskian for every pair of directions in
the closed hyperbolicity cone. Checking the all-ones pair or two SOS slices cannot
establish it. In the quintic deformation the sharp extension boundary is accepted,
including equality, but the weak-SOS boundary is still unknown. The published
nonextendable quintic is not a counterexample to the original equivalence.

## Verification and scholarly limits

The full prose audit, 206 author exact assertions, and 46 independently coded
checks support the accepted partials. Their scope is stated in `AUDIT.md` and the
proofs. Neither verifier is a formal proof assistant. The base quintic's published
hyperbolicity theorem is a cited mathematical input. The source reports a
computational full-space non-SOS result; no independent rational dual certificate
for that result is provided here. The two local rational Gram certificates prove
only the stated slice identities and positive semidefiniteness.

The primary source is G. Blekherman, J. Lindberg and K. Shu, *Symmetric Hyperbolic
Polynomials*, Journal of Pure and Applied Algebra 229(2), 107869 (2025),
https://doi.org/10.1016/j.jpaa.2025.107869 . Its published Section 2 retains
Conjecture 2.3. The preceding statement is OWR 15/2023, Conjecture 3, printed p.868,
https://doi.org/10.4171/owr/2023/15 . Publication metadata was rechecked before this
packet was prepared. The frozen author and auditor records separately disclose
their source-access and inspection histories, including a failed direct publisher
request during the audit and the limits of search-indexed text.

No historical novelty, exhaustive literature coverage, worldwide current-openness,
human referee acceptance, or complete solution is claimed. The original target
remains unresolved after the five documented routes. This acceptance record does
not authorize extrapolating the partial results to the full conjecture.
