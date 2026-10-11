# Acceptance: recursive bound for based cyclic fixed subgroups

Decision: PRIOR_RESULT_VERIFIED_SCOPED.

The accepted conclusion is the exact total recursive maximum B(n,L) for based cyclic fixed-subgroup generator lengths, for automorphisms of F_n given by explicit reduced basis images of maximum length at most L. Correctness and termination of the Bogopolski–Maslakova basis algorithm are imported from Theorem 1.1, arXiv:1204.6728v6. The complete 68-page algorithm proof was not independently audited.

## Authored conclusions accepted

1. Every finite image tuple can be recognized as an automorphism or rejected by a terminating labelled-graph folding procedure. The proof covers preservation of based loop labels, the basepoint loop test, graph rank, homotopy equivalence of accepted folds and both directions of recognition.
2. Enumerating all reduced image tuples with fixed n,L, recognizing automorphisms and invoking the imported algorithm only on valid inputs gives a finite terminating computation. The output basis decides trivial, cyclic and noncyclic cases, so taking the maximum returns exactly B(n,L). Rank zero, L=0 and rank one are explicit.
3. The construction is uniform in finite rank. Fixed-rank B_n(L) is distinguished from B(n,L); there is no silent maximum over all ranks at fixed image norm. The total-letter bound C(S)=max_{1<=r<=S} B(r,S), with C(0)=0, is justified by n<=S. Finite-alphabet bit encodings must include rank, delimiters and generator indices.
4. The stated maximum/sum comparisons, recursive inverse-image conversion, conversion from a specified finite Aut(F_n) generating set and marked/based graph length estimates are proved with their hypotheses. No quantitative rate beyond recursiveness follows from those comparisons.
5. For g_k=b^k a b^(-k), the inner automorphism by g_k has Fix(alpha_k)=<g_k> and based generator length 2k+1 while its outer class and cyclically reduced generator length stay constant. The full centralizer argument is preserved. This explains why basing cannot be dropped.

## Imported theorem and source boundary

The source basis algorithm, including its correctness, termination and based output, remains an imported established result. Selected sections and closing reductions were inspected; uninspected train-track, orbit-decision and internal perfect-path dependencies are not certified. The inspected 2014 arXiv v6 and the bibliographically identified 2016 journal paper are not asserted to be byte-for-byte or proof-for-proof equivalent. Feighn–Handel Proposition 9.10 corroborates the algorithmic statement but is unnecessary to the finite-maximum proof; its full dependencies were not independently audited.

No basis-algorithm implementation or general numerical B(n,L) computation is provided. Finite elementary checks supplement, and do not replace, the general written proof. No stronger rate, rank-independent bound in maximum image norm, novelty, priority, worldwide open-status claim or unrestricted resolution of an unspecified quantitative variant is accepted.

## Review and distribution

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance concerns only the recursive-bound consequence of the imported Bogopolski–Maslakova basis algorithm; it is not external human peer review or formal proof-assistant certification. This is a written proof/audit edition, not a computational reproduction package. Source inspection and elementary finite checks were performed during the preceding investigation on 11 October 2026. Edition preparation authenticates retained bytes without a fresh scholarly-source inspection or mathematical-program rerun.

Both PROOF.md and AUDIT.md retain the same complete accepted original mathematical argument, with only edition heading/review context and historical-check wording changed. They do not assert two independent audits. Their full substantive source-inspection/dependency record is preserved. The closed selected input bundle is distinguished from its parent directory. Programs, raw outputs, datasets and copied sources are omitted. Publication packaging verifies identities and editorial retention; it does not re-audit the imported theorem.
