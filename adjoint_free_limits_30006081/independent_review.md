# Independent review: expected forward-query bound

## Verdict

The proposed minimax identity is valid in the stated exact, noiseless, same-field forward-query model, provided the approximation factor is at least one (as usual) and all algorithms, stopping decisions, and outputs are jointly measurable. For fixed integers m,n >= 1 and k >= 1, success probability p in [0,1], and either Frobenius or operator norm,

    inf_alg sup_A E_R[T(A,R)] = p n.

Here the infimum ranges over algorithms satisfying the approximation guarantee with probability at least p for every input A, and stopping after a finite integer number of oracle calls almost surely for every A. The expectation may otherwise be extended-valued. Randomness is independent of A. The output is a rank-at-most-k matrix determined by the algorithm's random seed and finite transcript. A fixed finite approximation factor C >= 1 suffices; the lower bound only needs success to imply exact recovery whenever the best rank-k error vanishes.

This does not assert E_R T(A,R) >= pn for every individual A. The lower bound is on a Gaussian-prior average, and hence on the supremum over inputs.

## Lower bound, including adaptive stopping

Draw g as a nondegenerate standard Gaussian in F^n and set A=e_1 g*, where F is R or C. In the complex case use a circular complex Gaussian, complex queries, and Hermitian orthogonal projections throughout. Every such A has rank at most one. Since k >= 1, success under either relative-error criterion requires the output to equal A exactly.

Let R contain all random bits, including randomness used to decide when to stop or to form the final output. For each finite t, let H_t contain R, all queries through call t, and their responses. Let S_t be the span of those queries, and let r_t be its dimension. The standard adaptive Gaussian conditioning induction gives

    g | H_t  ~  Gaussian(mu_t, P_(S_t perpendicular)),

with the usual interpretation as a Gaussian measure on an affine subspace. The initial seed is independent of g. Conditional on H_(t-1), the next query is fixed. A query in S_(t-1) supplies no new information. A query outside this span supplies one scalar Gaussian observation and removes precisely its normalized residual direction from the conditional covariance. In the complex case, conjugate the scalar response g* x to obtain the linear observation x* g and use the circular-Gaussian conditioning identity. The covariance normalization is immaterial to non-atomicity.

This induction is valid for arbitrary measurable adaptive choices; continuity or smoothness of the query rule is unnecessary. In a formal treatment, take standard Borel seed/transcript/output spaces, or explicitly posit the conditional-distribution framework. Measurable Gram-Schmidt or Moore-Penrose constructions provide the posterior kernel even at rank-changing transcripts.

For every fixed finite t, on the event r_t<n the conditional distribution of g is non-atomic. Any H_t-measurable candidate g-hat therefore equals g with conditional probability zero there. If the algorithm stops at t, extract g-hat from the first row of its output (taking conjugates). The event {T=t} is H_t-measurable: observing that the algorithm stopped supplies no information beyond the seed and transcript. Consequently

    P(success, T=t, r_t<n)=0.

Summing over all nonnegative integers t, and using finite stopping almost surely under the product prior/seed law, yields

    P(success, r_T<n)=0.

One can extend the process after stopping by zero queries to make every finite-time transcript defined. The result covers dependent queries and T>=n as well as the simpler T<n event.

Thus, almost surely under the hard distribution, success implies r_T=n and hence T>=n. Tonelli's theorem and the uniform success guarantee give

    E_g E_R T(A,R) >= n P_(g,R)(success) >= np,

and therefore sup_A E_R T(A,R) >= np. If finite stopping was assumed separately for every A, its product-law version follows by Tonelli/Fubini; joint measurability is needed here as elsewhere.

## Matching upper bound

Flip a Bernoulli(p) coin independently of A. On heads, query the n standard coordinate vectors, reconstruct every column of A, and output a best rank-at-most-k approximation obtained from a measurably selected truncated SVD. On tails, make no query and output zero. Success probability is at least p on every A and expected query count is exactly pn on every A. If k exceeds min(m,n), the heads branch simply returns A. The construction includes p=0 and p=1 and n=1 without exception.

## Limits and presentation cautions

- State the expectation objective explicitly. A worst-case deterministic call budget or an almost-sure call cap is a different model; the Bernoulli construction does not yield a cap pn.
- The conclusion is worst-case over the full matrix class. Restrictions excluding rank-one inputs can invalidate this particular argument.
- Exact arithmetic/noiseless oracle access and exact relative-error guarantees on zero-tail inputs are essential to this proof. Additive slack, promises of nonzero tail, finite precision, or observation noise require separate analysis.
- The lower bound actually applies to any genuine matrix norm and any success criterion forcing exact recovery on rank-one inputs.
- Do not transfer the complex argument to real unknowns queried with complex vectors. One complex query can encode two real directional measurements, so field consistency matters.
- Do not claim positive conditional variance in a fixed coordinate: the residual subspace is adaptive. Nonzero covariance rank, hence non-atomicity on the residual affine subspace, is the correct invariant.
- Approximation factors below one are not the usual model and can make the uniform guarantee impossible when k<min(m,n). State C>=1 rather than merely 'finite factor' unless these exceptional regimes are separately addressed.
- No novelty conclusion was independently source-verified in this review. The result should be presented as an elementary expected-cost corollary/refinement of an applicable existing rank-one exact-recovery obstruction, not as a novel theorem, pending comparison with the cited theorem 5.1 of arXiv:2606.01335.

This review concerns only the stated mathematical claims.
