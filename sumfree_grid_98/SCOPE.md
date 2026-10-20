# Mathematical scope and limitations

## Qualified asymptotic acceptance

For each fixed positive integer d, the audited submitted preprint gives f_d(N)=c*_d N^d+O_d(N^(d−1)), with c*_d the maximum volume of a coordinate-sum slice in [0,1]^d. The audit supplies local repairs to connectivity, numerical certification, and the final weighted-error comparison. It is not a formalized proof or a claim that all imported theorems were independently reproved. The independent checker certifies the stated finite rational inequalities and analytic-tail constants, not the entire manuscript by computation.

The positive-grid and zero-based-grid conventions are compared by boundary inclusion, never by assuming translation preserves sum-freeness. No estimate uniform in growing dimension is claimed. Submitted status is not peer review.

## Exact finite contributions

- Elementary formulas for d=1, N=1, and N=2.
- Twelve independently replayable branching/packing certificates for the small grid values tabulated in attempt 1. Before replay, run `python computation/reconstruct_certificates.py`: one certificate is transported as numbered base64 parts and reconstructed byte-for-byte with size and SHA-256 checks; the other eleven gzip files are shipped directly. This transport does not alter any certificate or mathematical conclusion.
- An exact Boolean-family reduction for N=3, upward-compression proof, and independent upset enumerations through d=6, giving f_6(3)=706.
- A partition-free-family theorem yields the stated N=3 formula for d≡1 modulo 3 with d≥4 and every d≥18. Source hypotheses are retained. Dimensions 8,9,11,12,14,15,17 are not covered by those sources and computations.
- Exact isolated-boundary and two-sided-boundary constructions, an outer-shell profile identity, and boundary-scale improvements that disprove universal exact plain-slice and isolated-completed-slice formulas.

An inclusion-maximal construction is not necessarily maximum-cardinality. A profile identity is not a scalar recurrence or a universal upper bound. Floating-point optimization is useful only for proposing witnesses; no floating-point solver bound supplies an exact upper proof in this package. Computational agreement over a finite list does not settle arbitrary d,N.

The full literal finite maximum problem remains unresolved by these arguments. This is not a claim that every uncovered finite instance is open in the literature. No novelty claim or exhaustive literature-search claim is made.
