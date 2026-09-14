# Section 3 attribution and exposition audit

Checkpoint: 2026-09-13 (America/Los_Angeles). Bounded attribution/exposition audit: 100% complete; this is not an independent certification of the entire equality proof.

## Primary artifacts inspected

- Zenodo review PDF, record [21699069](https://zenodo.org/records/21699069), `kriebel-2026-minimum-bell-setting-complexity-review-v1.1.0.pdf`; extracted PDF text inspected directly with binary-safe search.
- Zenodo clean PDF, record [21699161](https://zenodo.org/records/21699161), corresponding v1.1.0 file.
- Source downloaded from Zenodo record [21699181](https://zenodo.org/records/21699181), `main.tex` lines 106–225, 408–704, and `appendices.tex` Appendix A.
- Vértesi–Bene, [arXiv:1007.2578](https://arxiv.org/pdf/1007.2578), especially Eqs. (2)–(4), Sections IV–V, Eq. (26), and Section V.D.

No claim here relies on the author's current website. The relevant passages agree between the review and clean Zenodo PDFs and the downloaded source.

## Prior result and actual incremental content

Vértesi–Bene already established qubit POVM advantage with the same heterogeneous setting/outcome architecture. Their construction couples a dominant CH/CHSH term to a ternary measurement optimization. They analytically optimize projective measurements on the maximally entangled state and report matching numerical lower/NPA upper projective bounds over all two-qubit states at their chosen parameter. They do not establish the universal two-input convex-hull equality. These statements summarize their primary paper, not a judgment about priority of every later refinement.

The published Zenodo abstract already begins by crediting their 3-by-2 example. The introduction explicitly credits the existence result; Table 1 compares architectures and proof styles. Therefore a claim that the published manuscript contains no attribution would be incorrect.

Section 3 supplies a different rational functional,

\[
10S+\tfrac35p(0,0|2,0)+\tfrac35p(1,1|2,0)+\tfrac45p(2,0|2,1),
\]

an explicit rational ternary POVM on the maximally entangled state, and an analytic bound over all two-qubit PVM strategies. The certified strict gap is

\[
(20\sqrt2+16/25)-\left(20\sqrt2+3/5+(4+3\sqrt2)/250\right)
=3(2-\sqrt2)/250>0.
\]

The proof controls the auxiliary score through the CHSH deficit and explicitly covers the six ternary PVM supports. Appendix A gives its nonnegative polynomial certificate. These are concrete incremental certificate/exposition features; they are not a new discovery of the existence phenomenon. Neither the broad construction mechanism nor the setting architecture should be presented as new. This bounded comparison does not establish worldwide novelty of the specific rational refinement or inequivalence under every possible Bell-functional transformation.

## Concrete v2 changes

1. Open Section 3 with explicit credit for the known existence result and construction mechanism. Explain that this section gives a self-contained exact rational witness for the upper-setting direction of the classification.
2. Lead the contributions list with the two-input equality, its reductions, and the resulting setting classification. Put the witness afterward as a supporting exact certificate.
3. Shorten Section 3 in the main text to its functional, theorem, attained strategy, and a concise global-bound argument. Move longer support calculations and the optional strengthened strategy to appendices or the verification package. Preserve the proof, sign conditions, and degenerate cases.
4. Correct Table 1's ambiguous row `Global optimum claimed / No / No`. The earlier paper does supply projective optima (an analytic fixed-state result and numerical global results). Replace the row with `Exact overall POVM optimum supplied` or remove it. Do not suggest that earlier work lacked a global PVM comparison.
5. Avoid claims that the new proof gives a better numerical gap: no normalized comparison has been performed here.

The appropriate response to attribution concerns is to acknowledge the known result and make the section's narrower role more prominent. It is unnecessary to retract the entire section or to assert that the work was copied; this comparison supplies evidence for neither claim.

## Lemma 4.1: shorter checkable proof

The published proof's argument is legitimate and can be expressed more compactly. Preserve the distinction between a sign-compatible support-minimal relation and an arbitrary linear dependence.

Let the distinct rays in a reduced nontrivial relation be columns of a matrix \(R\), with signed coefficient vector \(c\), and let \(N=|\operatorname{supp}c|\). If a proper subset were linearly dependent, perturb \(c\) along that dependence until one coefficient first vanishes. The perturbation preserves weak signs and yields a smaller positive relation, contrary to minimality. Thus these columns form a linear circuit and

\[
N-1=\operatorname{rank}R\le\dim K\le3.
\]

Pointedness forces both signs to occur; extremality of each ray excludes exactly one ray on either side. Consequently

\[
4\le N\le4,\qquad |\operatorname{supp}c_+|=|\operatorname{supp}c_-|=2,
\qquad\dim K=3.
\]

Absorb the four positive magnitudes into the ray representatives to obtain \(r_0+r_1=s_0+s_1\).

For clarity, the lemma statement should say that common-ray cancellations are handled first, and the remaining **nontrivial** relation is two-versus-two. The existing wording says both “after canceling” and “either ... one-versus-one cancellation,” which is an avoidable presentational inconsistency rather than a failure of the argument.

The same editorial principle should apply throughout v2: show the mathematical intermediate step and its hypotheses, then give only the prose needed to identify why it holds. Concision alone does not resolve an unsupported step, and the principal theorem still requires the broader proof-to-Lean audit.
