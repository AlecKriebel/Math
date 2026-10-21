# Source gate: adjoint-free nonsymmetric low-rank approximation

Checked: 2026-10-21 UTC. Queue identity: row 1855, ID 30006081, OWR-14298796-001. This is a source/status audit, not a new mathematical result or proof claim.

## Gate decision

Do not start a purported unrestricted low-query recovery breakthrough from the curated wording. The source is a research-talk summary explaining already-established barriers and positive results under structure. A directly relevant 2026 preprint explicitly supplies a randomized/adaptive lower bound for best-rank approximation. The remaining structured questions must be selected precisely; the broad curation is not one fully specified open theorem.

## Original source and provenance

Nicolas Boullé, joint with Diana Halikias, Samuel Otto and Alex Townsend, “Operator learning without the adjoint,” in Deep Learning for PDE-based Inverse Problems, Oberwolfach Report 48/2024, pp. 2820–2822 (whole report pp. 2805–2900). Workshop: 27 October–1 November 2024. DOI: https://doi.org/10.4171/OWR/2024/48 . The recovered publication PDF contains the talk on printed pages 2820–2822, not merely a search snippet.

The introductory question motivates results discussed immediately afterward. Its finite model is square complex rank-k F, forward products FX only, and candidate matrices with AX=FX. Spectral-norm diameter of the candidate set measures uncertainty. A near-symmetry prior compares left/right singular subspaces, not entrywise symmetry. The report also describes Fourier-projection recovery for structured compact operators. Its explicitly stated conjectural direction is continuation of linear error-bound growth to large lower-order perturbations of elliptic PDEs. That is distinct from unrestricted finite-matrix recovery.

Public PDF mirror inspected: https://oa.tib.eu/renate/server/api/core/bitstreams/4c8ce439-c8a5-4ba7-b682-11acfd488415/content .

## Foundational full paper

Boullé–Halikias–Otto–Townsend, JMLR 25(364):1–54 (2024): https://www.jmlr.org/papers/v25/24-0162.html .

Section 3 uses F in C^(n×n), exact rank k, and X in C^(n×s), k≤s≤n, full column rank, rank(FX)=k. Gaussian tests satisfy the rank condition almost surely; the geometric theorems condition on X, rather than providing a general randomized minimax theorem. Theorems 4–5 bound spectral-norm candidate diameter under a singular-subspace prior. Remark 7 identifies nonmatching asymmetric-case bounds as a remaining direction. Do not equate that prior with normality or a bound on ||F−F*||.

Theorem 9 gives ||A−AP_n|| ≤ ||LA*||/|λ_(n+1)|, assuming a known self-adjoint prior L with compact resolvent and Range(A*) contained in D(L). Forward evaluations on its first n eigenfunctions construct AP_n. This needs prior regularity information, not an adjoint oracle; it is an operator-norm, structure-dependent guarantee, not uniform relative-to-best-rank error for arbitrary matrices. Numerical neural-network results are not substitutes for this theorem. No polynomial-time or bit-complexity claim should be inferred from these oracle counts.

## Decisive 2026 status update

Halikias–Hochstenbach–Townsend, “Transpose-free linear algebra,” arXiv:2606.01335v1, submitted 31 May 2026; currently a preprint on the inspected author/arXiv pages: https://arxiv.org/abs/2606.01335 .

Theorem 5.1: A in R^(m×n), n≥m, 1≤k≤m, γ>1 (possibly dimension/rank dependent). Any randomized adaptive algorithm returning rank-at-most-k Atilde with ||A−Atilde||_F≤γ||A−A_k||_F, probability at least 2/3 for every A, requires n forward matvecs in the bounded/worst-case query model, not n in expectation. Model: arbitrary Ax queries, internal randomness/adaptivity allowed, no transpose or direct entry access, unrestricted internal computation. The hard distribution is rank one, so best-rank residual is zero and success requires exact recovery. Full PDF and proof inspected, not independently peer-reviewed here.

This is stronger than fixed-transcript non-identifiability alone: the paper explicitly distinguishes the two. Avoid deriving randomized lower bounds merely by choosing an unseen direction after observing random queries. The theorem's stated norm is Frobenius; do not silently relabel it spectral. Source: https://arxiv.org/html/2606.01335v1#S5.SS1 .

## Forward-only methods are not contradictions

Smith–Do–Chen, “Adaptive, Matrix-Free Low-Rank Approximation,” arXiv:2607.06758v1 (July 2026): https://arxiv.org/html/2607.06758v1 . Sections 3.3 and 4.3 explicitly return a range basis Q, not B=Q^T A. The conceptual error is ||A−QQ^T A||, but storing Q alone does not supply a stand-alone evaluator without another A call. Its Frobenius variant claims high-probability fixed-tolerance control; the spectral variant expressly offers only same-order tolerance rather than the exact prescribed bound. Thus its adjoint-free label does not overturn full-matrix recovery lower bounds. The paper also identifies earlier forward-only range finders, including Halko–Martinsson–Tropp.

## Model checks and elementary interpretation

These are scope checks, not proposed new results:

- A rectangular m×n matrix is recovered exactly by n coordinate queries Ae_j. “Impossible without the adjoint” must mean insufficient queries or lack of uniform efficient guarantees, not absolute impossibility.
- Each column of a block sketch counts as one vector query. Calling AX one API call does not make it one information sample.
- Forward coordinate queries reveal columns and their entries, but an independent row/entry oracle is additional information, excluded from the 2026 model.
- Knowing a range basis does not determine the matrix's row coefficients. Exact rank and approximate rank must not be conflated.
- Relative-to-best-rank residual differs from additive tolerance or error relative to ||A||. The zero-tail lower-bound argument does not by itself settle every noisy/additive model or restricted family excluding exact low rank.
- Nonnormality can defeat eigenvalue/Krylov intuition: singular values, not eigenvalues, govern low-rank error. No spectral gap, normality, known row space, PDE regularity, or bounded nonnormality may be assumed unless specified.
- Numerical training loss is not a uniform operator-norm certificate.

## Current-status conclusion and limits

See theorem_scope_audit.md for an independent proof-quantifier check, output representation, expected-query countercheck, and field/dimension limits.

The broad finite-dimensional low-query, relative-best-rank task has an existing negative result, including randomization/adaptivity. Structured operator learning already has positive results. Sharpening near-symmetric candidate-set geometry or resolving the large-perturbation PDE conjecture are separate potential research tasks; neither was verified solved in the targeted search through 2026-10-21. Absence of a search hit is not proof of openness. The curated “partially solved” category may remain reasonable for the broad umbrella, but its unrestricted-status sentence must not be treated as an exact current open-problem certificate.

No copied sources or corpus excerpts are included in this package.
