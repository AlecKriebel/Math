# Scope audit of the 2026 lower bound

This is an independent check of the inference used in the source gate, not an original result or an acceptance report for the entire paper.

## What the theorem actually promises

Theorem 5.1 of arXiv:2606.01335v1 (PDF pp. 16–17) concerns a transcript-determined output matrix, with rank at most k, and Frobenius error relative to the optimal rank-k residual. Its probability quantifier is at least 2/3 for every input. The approximation factor γ>1 can depend on dimensions and target rank. The source specifies real m×n input, n≥m, 1≤k≤m.

The proof fixes q<n queries. The safe reading is a bounded/worst-case query-complexity lower bound. Neither an expected-query lower bound n nor a claim that every random execution makes n queries follows. An immediate check is a mixture: reconstruct with n coordinate queries with probability 2/3, otherwise return zero without querying. This succeeds with probability at least 2/3 on every input, while using only 2n/3 queries in expectation. Thus an expected-n interpretation would be false.

## Independent proof check

Take the source's real Gaussian rank-one family A=e_1 g^T. For every allowed k≥1 its best-rank-k error is zero. Consequently any finite multiplicative guarantee requires the full matrix to be exact, not merely an approximate leading subspace.

Fix the algorithm's random seed. The vector response to x contains only the scalar g^T x. Given earlier scalar measurements, the next adaptive x is already determined; decompose it into the previous query span and its orthogonal complement. A dependent query adds no information. An independent query adds one scalar Gaussian measurement. Gaussian orthogonal residual components remain continuously distributed in the unmeasured subspace. Inductively, after fewer than n independent queries there is at least one continuously distributed degree of freedom. A measurable estimate based on that transcript hits the true residual with probability zero. Averaging over seeds preserves the zero success probability on this hard distribution, contradicting a positive uniform success probability. This validates the advertised obstruction in the bounded-query setting, assuming ordinary measurable algorithms and exact real arithmetic.

This argument is not merely a transcript-dependent adversary chosen after the random seed. It uses one fixed input distribution, which is the crucial randomized-quantifier distinction.

## Representation and boundary checks

- Factors U,V whose product is a fully determined output matrix qualify. A symbolic QQ^T A retaining access to the unknown oracle does not qualify as a matrix reconstructed from the completed transcript. Applying that object to a new vector requires another oracle call.
- Exact rank is not an extra promise in the theorem: the universal input class already includes rank-one matrices. A promise of nonzero tail, noise, additive error, or normalized error relative to ||A|| changes the statement and is not settled by the zero-tail reduction alone.
- n≥m is in the published theorem. The proof mechanism appears not to use it, but this audit does not present the tall-matrix extension as a theorem of the source.
- The source is real. A complex extension would require an explicitly complex oracle/distribution model. Allowing complex query vectors against a real-only input family changes the real-information count; it must not be silently smuggled into the proof.
- The proof is information-theoretic, allowing arbitrary internal computation. It does not establish finite-precision stability, bit complexity, or a separately stated expected-query lower bound.
- n coordinate queries recover the whole matrix; a subsequent truncated SVD supplies an optimal rank-k matrix. Thus the bounded-query endpoint is consistent with the trivial upper bound, not an absolute impossibility claim.

## Relation to the queue row

The source's broad motivating question has known positive and negative regimes. This theorem settles a particularly natural unrestricted relative-best-rank regime negatively. It does not classify all possible structural priors, settle the JMLR asymmetric diameter gap, or resolve its large-perturbation elliptic-PDE conjecture. Do not mark the whole exploratory row already solved solely from this theorem.
