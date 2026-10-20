# Acceptance report: bounded partial results, not a full solution

Date: 2026-10-20 UTC. Problem ID 30002547.

**Disposition: ACCEPTED for the explicitly bounded mathematical claims below. NOT ACCEPTED as a full proof or disproof of Albert–Bousquet-Mélou Conjecture 11. Full-target status remains UNSOLVED after five attempts.**

The two open parameter intervals (-1,-1/2) and (-1/2,0) remain unsettled by these arguments. The source/status review is bounded and does not certify their global literature status. The a=-1 case was already known. No novelty, priority, or exhaustive-search claim is accepted.

## 1. Nonnegative parameters

Accepted from ATTEMPT_1.md, with AUDIT_NONNEGATIVE.md:

- The exact half-length radius (2+sqrt(2+2a))^(-2) for each fixed real a>=0.
- The ordinary coefficient root limit, including the endpoint a=0.
- The zero-drift finite-state construction, sublinear confinement bound, endpoint grouping, reverse-negation symmetry, exact seam weights, padding and injectivity.

The argument cannot be transferred to negative a by retaining a positive subfamily: the full coefficients are signed sums. The finite checks confirm the construction but are not the asymptotic proof.

## 2. Signed quadratic-pencil bound

Accepted from ATTEMPT_2.md, with AUDIT_SIGNED_PENCIL.md:

- The exact quadrant identity Q(a,t^2)=<delta,(I-tA+(1-a)t^2 B)^(-1)delta>.
- Holomorphy throughout the full complex disk required to prove rho_Q(a)>=rho_*(a) for -1<=a<0, not merely real-axis invertibility.
- The explicit coefficient estimate |Q_n(a)|<=e^2(n+1)^2 rho_*(a)^(-n).
- Operator noninvertibility at the proposed endpoint and a finite one-sided Abel value there.

Here rho_*(a) is the conjectured piecewise radius. Bulk operator noninvertibility alone is not an accepted proof that the corner scalar function is singular. A finite Abel value alone proves neither ordinary boundary convergence nor holomorphic continuation.

## 3. Exact counterexample to the refined assertion (P2)

Accepted from ATTEMPT_3.md, with AUDIT_REFINED_P2.md:

- For vertical projection N^13 S^13 and horizontal half-length 2, including both horizontal Dyck projections EWEW and EEWW, the complete polynomial is

      G(a)=13769+27300a+13741a^2
          =210-182(a+1)+13741(a+1)^2.

- The coefficient -182 disproves precisely (P2) in ABM Section 6.3.1.
- The full family formulas, negative signed fixed-shuffle classes, negative fixed-vertical slices over the stated parameter ranges, and marked-corner convolution are proved.

All 54,810 words in the explicit example were checked with exact integer enumeration. This is not a counterexample to the unrefined positivity Conjecture 10, not a counterexample to the radius Conjecture 11, and not exponential-growth evidence: the family with fixed horizontal half-length has polynomial size in the vertical length.

## 4. Scope of the local blocking obstruction

Accepted from ATTEMPT_4.md, with AUDIT_LOCAL_BLOCKING.md:

- For incoming direction N, block length L and displacement (-1,L-1), the exact signed block weight is La for every L>=1.
- Consequently no exact nonnegative fixed-length blocking representation retaining incoming state and displacement can represent this model for a<0, even after adding nonnegative hidden states whose sum must recover that coefficient.
- The unrefined M^2 positivity and arbitrary-endpoint cancellation formulas do not repair this obstruction.

This excludes only the stated local strategy. It does not exclude all global regrouping, all sign-reversing constructions, or a proof of the original radius conjecture.

## 5. Transition point and lower-branch projection formula

Accepted from ATTEMPT_5.md, with AUDIT_TRANSITION.md:

- At a=-1/2, rho_Q=1/9, the one-sided Abel value is 3/2, and the derivative in u tends to positive infinity.
- The exact lower-branch formula q_*=c||P_M delta||^2, where c=1-a, M is the closure of the range of U+V-alpha_* I, and alpha_*=sqrt(2/(c-1)).
- For 3/2<c<=2, the strict bound 0<q_*<c; at c=3/2 the range is dense and q_*=3/2.
- The range obstruction at the transition gives divergence of ||K(t)^(-1)delta|| and hence divergence of the scalar derivative. This genuinely detects the corner threshold.
- The stated upper-branch quadratic-form comparison is valid, but it does not justify comparison of higher inverse powers of noncommuting operators.

No ordinary or absolute convergence of the signed coefficient series at its boundary, no full coefficient asymptotic, and no radius equality on either remaining open negative interval are accepted as consequences of this proof.

## 6. Reproducibility and source verification

Four exact checker programs were independently replayed in a fresh isolated directory. All exited successfully with no stderr. REPLAY_VERIFICATION.json records their full stdout and source hashes. Additional controls cover all 85,208 mirror pairs through length 6, rational sparse-vector pencil factorizations and derivative rearrangements, and exact formal transition recurrence coefficients. No floating-point or numerical-only evidence is used to accept an infinite mathematical claim.

The four source-PDF hashes and byte counts in SOURCE_VERIFICATION.json were rechecked against the inspected files during package preparation. Only that public metadata, citations and authored analysis are included, not the source PDFs or extracted text.

The final inventory and all package file hashes appear in MANIFEST.json. Mathematical source files with hashes cited by audit reports must match those references; the manifest then pins the audited package versions.
