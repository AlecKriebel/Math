# Release notes — version 1.0.0

**Release date:** 29 July 2026

**Title:** *Tensor-Local Constraints in the Exceptional Unitary Hecke
Yang--Baxter Class*

## Main results

1. Every exceptional matrix-class solution is automatically standard,
   with both spectral-projection partial traces equal to
   \((d/2)I_d\).
2. Its tensor representation is faithful after passage to the
   \(H_n(3,6)\) Jones--Wenzl trace quotient.
3. Every simple tensor-space multiplicity is
   \[
   m_{\lambda,n}=D_\lambda(d/2)^n.
   \]
   Consequently simple-multiplicity, central-rank, Markov-weight, and
   branching arithmetic alone permits every even local dimension.
4. Exceptional reflections of operator-Schmidt rank at most three exist
   exactly when \(4\mid d\).
5. At operator-Schmidt rank four, injectivity of either intrinsic
   joint-sandwich map forces \(4\mid d\). Thus every unresolved
   rank-four \(d\equiv2\pmod4\) candidate has nonzero Hermitian traceless
   sandwich annihilators on both legs.
6. Every hypothetical \(d=6\) solution is nonrestrictable, has no
   two-dimensional square-invariant local subspace, and satisfies
   \[
   \mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6.
   \]
   It is outside the primitive-Weyl Bell-diagonal and four-product
   Clifford-frame classes.

## Deliberate nonclaims

- The complete dimension spectrum is not settled.
- No exact \(d=6\) witness was found.
- A four-dimensional one-sided square-invariant subspace at \(d=6\)
  remains possible.
- Neither individual leg commutant is proved scalar.
- The simultaneous-singularity branch at operator-Schmidt rank four
  remains open.
- Negative numerical searches are not nonexistence evidence.

## Verification

The central exact suite runs 10 deterministic programs and passes 10/10.
The PDF was built reproducibly with Tectonic 0.16.9, rendered with
Poppler, and visually inspected page by page. A separate hostile audit
found no false central theorem or circular dependency after the repairs
recorded in
[`reviews/manuscript_final_hostile_audit.md`](reviews/manuscript_final_hostile_audit.md).
