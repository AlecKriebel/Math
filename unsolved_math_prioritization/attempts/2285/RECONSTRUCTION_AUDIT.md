# Independent audit of the partial-bound reconstruction

Date: 2026-10-21 UTC. Audited work: the five-approach mathematical note `research_erdos734_1868_20261021/RESEARCH.md`. Scope: logical verification of its displayed proofs, not a claim of historical novelty, exhaustive literature review, or resolution of Erdős #734.

## Verdict

The fixed-cardinality sampling, covariance-trace, and binomial-unimodality argument correctly proves the historical upper exponent F(n)=O(n^(3/4)) for every sufficiently large integer n, with simultaneous control of every size. It does not prove F(n)=O(sqrt(n)) and does not reproduce the historical outline's high-probability 1−o(1) statement. The existence/positive-probability conclusion is sufficient for this partial bound.

An initial threshold claim n≥8 was incorrect: n=9 produces q=8 and q+1=n. The correction is to require n≥10. For those n, q<sqrt(8n) and sqrt(8n)+1<n, so every restricted line is a proper block. This threshold correction does not change the asymptotic result.

## Checks

1. Exact-cardinality sampling is retained throughout. For m specified coordinates of a uniform n-subset, entropy chain-rule conditioning gives the stated conditional Bernoulli parameter. Its variance comes from the exact hypergeometric variance, yielding D(P||Q)≤m(m−1)/(2(v−1)(v−m+1)). Pinsker then gives TV≤m/v under m≤v/2. No probability penalty for conditioning an iid sample on its total size is introduced.

2. Fourier inversion bounds the largest Bin(r,p) atom by sqrt(π)/(2sqrt(2r p(1−p))). The modulus estimate follows from 1−cos(θ)=2sin²(θ/2), 1−x≤exp(−x), and sin(|θ|/2)≥|θ|/π on [−π,π]. The integral bound has the stated constant. Binomial unimodality gives sum|a_t−a_(t−1)|=2max a_t and therefore sum(a_t−a_(t−1))²≤2(max a_t)².

3. Two plane lines intersect in exactly one point. In the iid model, condition on that point and use the independent q-point remainders. This gives the displayed nonnegative covariance for each size. Its trace is O(1/q), uniformly over the chosen density range. The fixed-n trace differs by at most the union-coordinate TV plus twice the line-coordinate TV. Expressing the two terms as equality-event probabilities justifies those error bounds; no invalid entrywise sum over q sizes occurs.

4. Summing the trace over ordered distinct line pairs and the diagonal gives sum_t Var(X_t)=O(v²/q). Markov controls the squared Euclidean deviation vector with positive probability. Each individual coordinate is bounded by its Euclidean norm, so this one event bounds all multiplicities at once. No union bound or independence between different sizes is needed.

5. The smallest power of two q≥sqrt(2n) exists for every n and satisfies 2n≤q²<8n. Thus the finite projective plane exists and v=Θ(n), q=Θ(sqrt(n)). For n≥10, density lies between 1/10 and 1/2, q≥4, 2q+1≤v/2, and q+1<n. Removing intersections of size zero or one leaves an exact pair cover; distinct retained blocks cannot coincide. The result is valid for every n≥10, not only plane orders.

6. The deterministic dense-subset barrier, the corrected distinct-size upper bounds, independent full-plane block refinement obstruction, unequal-full-transversal weighting obstruction, pair-capacity condition, singleton-pair repair budget, and keep-old-blocks padding obstruction all follow as stated. These are scoped to their explicitly defined construction classes. They do not rule out more general weighted designs, pair reorganization, sparse restrictions, or other repair mechanisms.

## Optional explicit upper constant

The same argument can be quantified without optimization. For q≥4 the exact Pinsker bound gives single-line TV≤1/(2q) and two-line-union TV≤2/q. The iid covariance trace is at most π/(4q), so the exact-n trace is less than 4/q. Since v≤2q², sum_t Var(X_t)≤17q³. The density range gives max_t E X_t≤5q^(3/2). Some selection has squared deviation at most its expectation, hence max_t X_t≤(5+sqrt(17))q^(3/2)<10q^(3/2)<50n^(3/4). This is an existence bound for n≥10, not a sharp constant and not a claimed improvement in the historical exponent.

## Inspected final artifact

The corrected research note was rechecked for the n≥10 threshold. Its SHA-256 is `2f43e21fd8d2f8fcc1027f7bf0615616741990e3f1fb76c876267f5f7c94b56e`. Finite checks reported by its author are supplementary; this audit rests on the proofs above, not those computations.

## Acceptance boundary

Accept this as a complete authored reconstruction of a known partial exponent, with the n≥10 correction now verified. Keep the original sqrt(n) target unresolved. Do not describe the proof as new resolution, a proof of the original stronger probabilistic claim, or a general n^(3/4) lower bound for arbitrary designs.
