# A credited negative answer to the bounded-chaining equivalence, with the separation question open

**Target:** 30006170 / OWR-14299082-017, Zomback's Questions 5–6, printed p.122 of Oberwolfach Report 2/2025. **Status:** original bundled target unresolved; proposed `unsolved 2/5`. **Independent review:** pending. This package reconstructs a prior counterexample, records a narrow stochastic-matrix correction, and supplies a bounded-return-set criterion. It does not claim a new resolution of Question 6, priority, or human peer review.

## 1. Exact source and changing terminology

The original context is a Borel action of a countable discrete group on a standard probability space. Measure-class preserving means that every group element and its inverse preserve null sets. Weak mixing means that the diagonal product with every ergodic probability-measure-preserving action is ergodic; it must not be replaced by ergodicity of the action on its own square.

The 2025 report defines its unqualified *chaining* by existence of a single finite bound working for every pair of positive-measure sets. In Tserunyan–Zomback, *Bounded chaining in measurable dynamics*, arXiv:2609.18061v2 (2026), this is called **boundedly chaining**, BC. Their unqualified C instead permits the bound to depend on the two sets. The original question is about BC, not this weaker C.

We use the unambiguous 2026 convention: k-C means that for every positive A,B there are g_1,...,g_k with A intersect g_1 A, consecutive translates, and g_k A intersect B all of positive measure. The report writes g_i for i<=k, separately mentioning g_0 A intersect A, without declaring g_0=1. Read literally with indices 0,...,k, its k corresponds to k+1 here. We preserve this apparent indexing discrepancy. It does not change BC or the negative answer to Question 5. For Question 6 we establish neither a BC-but-not-1-C example in the newer convention nor a BC-but-not-2-C example under the literal older convention.

The new preprint's Proposition 6.13 already constructs an mcp F_2-action that is essentially 1-C, hence metrically ergodic and weakly mixing, but is not BC. Its Question 1.4 still explicitly asks for BC-but-not-1-C nonsingular examples. Thus the first original question has a credited negative answer, while the second part is left open here. Singular-action or essential-chaining separations do not settle the latter.

The downloaded full PDF identifies itself as v2, 17 September 2026, with a printed manuscript date of September 21. These are distinct source metadata, not a verified journal publication. Full sources: [OWR](https://ems.press/content/serial-article-files/51347), pp.121–122; [preprint v2](https://arxiv.org/abs/2609.18061v2), Definitions 2.2, 3.1, 5.4, Question 1.4, and Proposition 6.13.

## 2. Explicit matrix and a local source correction

Write S=(a,A,b,B), where A=a^{-1}, B=b^{-1}. Let

\[
P=\begin{pmatrix}
0&0&1/2&1/2\\
0&0&1/2&1/2\\
1/3&1/3&1/3&0\\
1/3&1/3&0&1/3
\end{pmatrix},\qquad
\pi=(1/5,1/5,3/10,3/10).
\]

Every row sums to one, pi P=pi, inverse transitions vanish, the support is irreducible, and every entry of P^t P is positive. This is a finite stationary Markov chain, so no recurrence theorem for arbitrary countable state spaces is needed. Let mu be its Markov probability on the reduced infinite words X=boundary F_2, and L the set of P-legal words. Then mu(L)=1, and neither aa nor AA occurs in L.

The text of Proposition 6.13 says its transition matrix is symmetric, while drawing this same support with positive loops at b and B and no loops at a or A. A symmetric row-stochastic matrix with that support cannot exist: the total flow from {a,A} to {b,B} is 2, so symmetry forces total reverse flow 2, leaving no row mass for the two positive loops. The displayed P repairs that numerical adjective while retaining exactly the support used in the argument. It is reversible with pi, but is not symmetric. We do not silently describe it as the matrix printed in the source, nor infer that the intended counterexample fails from this repairable point.

Enumerate F_2 as (g_j)_{j>=1}, including the identity, and define
\[
\widetilde\mu=\sum_{j\ge1}2^{-j}(g_j)_*\mu.
\]
This probability is nonsingular: a set has zero measure precisely when all its inverse group translates have mu-measure zero, a condition unchanged by a group translation. Also L is a complete section modulo null sets, because the union of its translates is conull.

**Prefix-replacement fact.** The restrictions of mu and tilde-mu to L are equivalent. Indeed, for a fixed finite reduced g, the partial map x -> gx between points of L splits into finitely many pieces according to the cancellation length and next letter. On each piece it replaces a finite legal prefix by another legal prefix with the same remaining tail. The Markov property and strict positivity of each legal cylinder probability give mutually absolutely continuous conditional measures (a positive constant ratio on each such cylinder piece). Consequently, a mu-null subset of L remains null under every such partial replacement. Apply this to every term of the countable mixture. The reverse absolute continuity follows from the positive identity term. This also justifies all subsequent uses of completed measurable sets.

## 3. One-step chaining on L and weak mixing

We give a direct reconstruction of the mechanism of the cited Lemmas 6.3–6.4 and Theorem 5.7, so the preceding matrix correction is fully accounted for.

Let E,F be positive tilde-mu-measurable subsets of L. By the prefix-replacement fact they have positive mu-measure. Choose states s,t and epsilon>0 with mu_s(E)>epsilon and mu_t(F)>epsilon, where mu_s is mu conditioned on the first letter s. Since P^t P is strictly positive, there is a state c with P(c,s)>0 and P(c,t)>0.

For arbitrarily small delta>0 there exists a legal finite word w c with mu_{wc}(E)>1-delta. Here is the requisite density argument. Cylinder martingale convergence first gives a cylinder on which E has density greater than 1-delta. In a finite irreducible Markov chain the state c is revisited almost surely; partition that cylinder by its first sufficiently late extension ending in c. One of these disjoint subcylinders retains density greater than 1-delta.

Take delta<epsilon min(P(c,s),P(c,t)). The conditional density of E in both cylinders wc s and wc t is greater than 1-epsilon. Prefix removal by g=(wc)^{-1}, together with the Markov property, yields
\[
\mu_s(gE)>1-\epsilon,\qquad \mu_t(gE)>1-\epsilon.
\]
Therefore E intersect gE and F intersect gE have positive mu-measure, hence positive tilde-mu-measure. This proves 1-C on L; it does not prove 1-C on all of X.

Every generator d belongs to the return set of L. Choose a state t with P(d^{-1},t)>0. The positive cylinder [d^{-1}t] is mapped by d into legal words, proving tilde-mu(dL intersect L)>0. Thus returns of L generate F_2.

To see metric ergodicity directly, let phi:X->Z be a measurable equivariant map to a separable metric space with an isometric F_2-action. All equivariance identities hold on a common invariant conull set, since F_2 is countable. If phi is constant z on L, the positive returns just proved imply that every generator fixes z, and completeness of L implies that phi is constant on X. Otherwise the pushforward of the normalized restriction to L is not a point mass. Choose two sufficiently small balls U,V of positive pushforward measure with d(U,V)>diam(U). Set E=L intersect phi^{-1}(U), F=L intersect phi^{-1}(V). One-step chaining on L gives E intersect gE and F intersect gE of positive measure. Equivariance implies that gU intersects both U and V. Its diameter is diam(U), contradicting the separation. Thus phi is essentially constant.

For completeness, this implies the exact weak-mixing property without requiring an identification with double ergodicity. Given any ergodic pmp action on (Y,nu) and an invariant measurable subset D of X times Y, the map x -> 1_{D_x} into the separable Hilbert space L^2(Y,nu) is measurable and equivariant for the Koopman isometries. Metric ergodicity makes this section map essentially constant. The constant indicator is invariant on Y, hence has measure zero or one by ergodicity. Fubini implies that D is null or conull. This proves weak mixing of (X,tilde-mu).

## 4. Failure of every finite chaining bound

This is the support obstruction of the cited Proposition 6.13, with its free-reduction step made explicit.

For x in X other than a^infinity, let h(x) be the length of its initial run of positive a's. Every point in every finite translate of L has finite h. On L, h<=1. For a reduced finite word g let p be the length of its initial run of a's. The following bounds hold for all x in L:
\[
\max(0,p-1)\le h(gx)\le p+1. \tag{1}
\]
If p=0, the upper bound is one: either a non-a initial letter survives or the whole word cancels and the remaining legal tail begins with at most one a. If p>0 and the suffix after a^p does not completely cancel, h(gx)=p. If that suffix cancels, at most one letter of the initial a-run can cancel, since two such cancellations would require consecutive AA in x. At most one new a can be appended from the legal tail. These observations give (1), including the case g=a^p. In particular h has oscillation at most two on every gL.

Starting from L, whose h-values are at most one, any chain of k overlapping translates of L has all h-values in its final translate at most 2k+1. Indeed, select a point in each consecutive overlap and use the oscillation bound to increase the maximum by at most two at each step. This uses mere nonempty intersections, a weaker requirement than positive measure.

The cylinder B_k=[a^{2k+2}] has positive tilde-mu-measure: the translate a^{2k+2} of the positive mu-cylinder [b] lies in B_k, and its mixture coefficient is positive. But L cannot k-chain to B_k, since the final translate would need a point of height at least 2k+2. Thus the action is not k-C for any finite k, and is not BC.

Together with Section 3, this proves the already credited negative answer to original Question 5 with an explicit valid stationary matrix. It is not a BC-but-not-1-C example: the action fails BC itself.

## 5. A precise bounded-return criterion and the remaining gap

For any nonsingular countable-group action and positive A, put
\[
R_A=\{g:\mu(A\cap gA)>0\},\qquad
U_k(A)=\bigcup_{g\in R_A^k}gA,
\]
where R_A^0={1}. Nonsingularity makes R_A symmetric and gives
\[
\mu(gA\cap hA)>0\quad\Longleftrightarrow\quad g^{-1}h\in R_A.
\]
It follows by multiplying consecutive increments that
\[
A\text{ k-chains to }B\quad\Longleftrightarrow\quad
\mu(U_k(A)\cap B)>0. \tag{2}
\]
The reverse implication uses countability to choose a single positive intersection, then factors the corresponding g as a product of k elements of R_A. Thus k-C is exactly the assertion that U_k(A) is conull for every positive A.

This reformulation exposes the unresolved quantifier: Question 6 requires a single finite k for all positive A while some U_1(A) is not conull (or U_2(A) under the older literal indexing). The explicit example above supplies no such uniform k. The 2026 paper's essential-chaining examples only control A inside a particular complete section, and nonsingularization can destroy a global bounded chaining property. Finite cylinder tests cannot certify (2) for all measurable A. Our second approach, through this return-set formulation and the paper's singular examples, supplies no mechanism to close this gap. Original target remains unsolved.

## 6. Verification and attribution boundaries

The accompanying standard-library checker verifies the rational stochastic/stationary data, support and common predecessors, finite legal-word cancellation bounds, and return-set/path equivalence in finite permutation actions. These are exact diagnostic controls, not a substitute for the measurable proofs or an exhaustive test of arbitrary measurable sets.

The negative example and its mechanism are explicitly due to Tserunyan–Zomback, Proposition 6.13; the explanation above is a reconstructed proof with a local numeric correction. The nonsingularization, essential-chaining, and metric-ergodicity framework are their prior work and earlier references they cite. No claim is made that the return-set observation or the correction is novel. The entire recent preprint, particularly its other separation assertions, is not certified by this package. Rank177's topological maximal chains concern a different space/action and are not this target.
