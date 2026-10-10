# Independent audit: strong-expansion spectral partial

Problem: 20000886 / AIM-COMBINATORICS-0011, rank 1271.

Date: 2026-10-10 UTC.

## Verdict

**PASS as a scoped partial result. The original existence/converse problem remains unresolved by this work.**

The distributed [mathematical report](MATHEMATICAL_REPORT.md), *Strong expansions: a global spectral exclusion and sharp binary lift boundary*, has 17,759 bytes and SHA-256 `4a932ba8ed7a99b24c6e39d10995bf7498c8b8d3fe675508e8e46086d04195d0`. The complete analytic proofs and source-scope arguments are retained. This AI-assisted, unrefereed audit is not external human peer review, journal acceptance or formal proof-assistant certification.

The report's global regular-marginal spectral-budget theorem, negative-eigenvalue-count corollary, arbitrary-rank L2/dense-host corollary, exact binary extension threshold, tensor closure, principal-restriction nonclosure, and irregular spectral counterexample are correct under their stated hypotheses. No mathematical correction is required. This acceptance does not certify novelty, prove a Sidorenko expansion of any non-Sidorenko core, prove the converse, or justify dropping regularity or the spectral-budget hypothesis.

The audit rederived the assertions. Acceptance rests on the written mathematical arguments; aggregate supporting verification totals are recorded in Section 7.

## 1. Exact target and convention check

The source target asks whether a finite non-Sidorenko uniform core can acquire a Sidorenko strong expansion. Each edge must receive its own new degree-one vertices. That definition matches AIM Problem 3.2 and Spiro Problem 2.1. The report only treats the graph core C4 disjoint-union C5 and only proves its expansion inequality on specified host classes. It repeatedly states the residual gap, so its status is appropriately limited.

The finite density normalization is correct: a single r-edge has `r! e(G)/n^r` homomorphism density in a simple n-vertex host. A finite adjacency step kernel is zero whenever two coordinates belong to the same vertex cell. Its kernel densities exactly equal the finite densities, including the contributions of noninjective source maps.

Conversely, independently sampling vertex labels and conditional edges from a symmetric [0,1]-valued kernel yields finite simple hosts approximating each fixed simple source density. For injective maps, distinct source edges become distinct host edges and their conditional expectations multiply. Noninjective maps contribute at most O(1/n). Pairs of maps with disjoint images are independent; pairs sharing vertices are O(1/n) of all pairs. Therefore the variance goes to zero. A strict kernel violation persists in some finite host. This establishes the needed equivalence without making the false claim that vertex-coordinate kernels represent every hypergraph limit.

Scaling extends the inequality equivalence to bounded nonnegative kernels. Scaling a lift changes its marginal by the same factor; the report correctly does not claim that a nonconstant mean-one marginal has a [0,1]-valued mean-one lift.

For a strong expansion, integrating every private leaf independently gives exactly `t_E^r(F)(W)=t_F(MW)`. This would not be automatic if leaves were shared, but that is excluded here. The nine-edge test core is non-Sidorenko because K2 has edge density 1/2 and no C5 homomorphism.

## 2. Weighted covariance and operator hypotheses

For real f in L2, expand the nonnegative integral of `W(sum_i f(x_i))^2`. Symmetry identifies the r diagonal terms as `r integral d f^2` and the r(r-1) off-diagonal terms as `r(r-1) integral U f f`. Every term is integrable: boundedness of W and the probability-space Cauchy-Schwarz inequality suffice. The weighted inequality in Lemma 1 follows, without regularity.

If `d=p>0`, the normalized kernel K=U/p is symmetric, nonnegative, and has row integral one. Thus T is self-adjoint and Hilbert-Schmidt, hence compact. Pointwise Jensen followed by symmetry gives the L2 contraction. The weighted inequality becomes the quadratic-form bound `T >= -I/(r-1)`. In particular every negative eigenvalue has magnitude at most `c=1/(r-1)`.

The constant unit function is an eigenvector of eigenvalue 1. Its eigenspace need not be one-dimensional. Keeping one distinguished copy and retaining all remaining positive eigenvalues is valid. Zero eigenvalues do not affect any sum. Hilbert-Schmidt summability and bounded spectral radius justify absolute convergence of all fourth- and fifth-power sums, even in infinite rank.

The trace identities have no problematic diagonal trace step. The kernel of T squared is the ordinary integral composition. Its squared Hilbert-Schmidt norm is the C4 integral. The Hilbert-Schmidt inner product of T squared and T cubed is the C5 integral, by Fubini and symmetry. Spectral expansion gives respectively the fourth- and fifth-power eigenvalue sums. T itself need not be trace class, and the report never requires that.

When p=0, nonnegativity gives W=0 almost everywhere, so the claimed inequality holds directly. At constant kernels with p>0, all nondistinguished eigenvalues vanish and equality holds. The formulas also make sense at r=2, where the allowed negative budget is zero; the actual graph-expansion application uses r>=3.

## 3. Spectral budget, finite rank, and density

Let `B=sum_negative |lambda|^4`. Discarding only nonnegative contributions gives normalized C4 density at least `1+B`. The negative contribution to the normalized C5 trace is bounded below by `-cB`, yielding `1-cB`.

The multiplication is legitimate precisely because the permitted range B<=r-2 forces `1-cB>=1/(r-1)>0`. The resulting excess is

`(1+B)(1-B/(r-1))-1 = B(r-2-B)/(r-1) >= 0`.

The negative-eigenvalue-count corollary follows from `B<=N/(r-1)^4`. At r=3, N<=16 suffices. A step kernel on at most 17 positive-measure parts has rank at most 17 and at least one positive eigenvalue, so at most 16 are negative. Unequal part sizes do not affect the rank argument; they only change the finite matrix representation.

For the new arbitrary-rank corollary, each negative term obeys `|lambda|^4<=c^2 |lambda|^2`. Removing the distinguished eigenvalue 1 from the full Hilbert-Schmidt sum therefore gives

`B <= (integral U^2/p^2 - 1)/(r-1)^2`.

No nonnegative eigenvalue has been mistakenly subtracted, and no finite-rank assumption is used. Hence `integral U^2/p^2 <= 1+(r-2)(r-1)^2` suffices. When 0<=U<=L, the inequality U squared <= LU gives the stated L/p condition. For a [0,1]-valued W, its marginal obeys 0<=U<=1, so the density threshold is exactly

`p >= 1/[1+(r-2)(r-1)^2]`.

In particular the r=3 value is 1/5, with the boundary included. This statement still requires pair-marginal regularity.

The cycle generalization is also correct. If `d=2b+1-2a>=1`, replace c by c to the d-th power in the negative-moment comparison. The budget `B_2a<=c^(-d)-1` makes the second factor at least c to the d-th power, and the displayed polynomial excess is nonnegative.

These conditions are sufficient, not necessary. As an independent scope check, take nine equal disjoint copies of the complete tripartite 3-kernel. Its normalized spectrum has nine eigenvalues 1 and eighteen eigenvalues -1/2. Then B4=9/8 exceeds the theorem's budget, while its compensated ratio is `81*135/128>1`. This explicitly confirms that budget failure cannot be interpreted as counterexample evidence and that repeated eigenvalues 1 must be handled as the report does.

## 4. Exact binary lift boundary

The necessity proof applies to all nonnegative integrable lifts, not merely two-cell lifts. Under the probability law with density W, the signs have balanced one-coordinate laws and pair correlation -theta. Therefore `E S^2 = r-r(r-1)theta`. The integer parity of S gives S squared >=0 for even r and >=1 for odd r. These yield exactly the thresholds `1/(r-1)` and `1/r`.

Independently, for a fixed count j of positive signs, the exchangeable pair correlation is `[(2j-r)^2-r]/[r(r-1)]`. Minimizing this finite list recovers the same bound, attained by the middle count or two middle counts. Complementing signs makes the one-coordinate laws balanced.

The endpoint density supported on the minimal-|S| tuples is bounded and permutation-symmetric. Its normalizing mass is the stated binomial probability q_r. Within each sign rectangle the marginal is constant. Complement symmetry, pair exchangeability, and the computed correlation force that marginal to equal `1-c_r f(x)f(y)`. Convex interpolation with the constant lift gives every theta between zero and c_r, including both endpoints. Multiplication by q_r produces a [0,1]-valued lift because its maximum before scaling is at most 1/q_r.

For r=3, q=3/4, theta=1/3, and the nonmonochromatic indicator indeed has marginal values 1/2 and 1 and mean 3/4. The report's product formula is algebraically exact, and `theta<=1/3` makes its excess nonnegative. The generalized even/odd cycle formula is also correct. At theta=1 the complete-bipartite marginal violates the core inequality but is excluded from every r-lift cone with r>=3.

For tensor products, use the product of the two r-lifts on the product probability space. Fubini proves the marginal and density products. A standard atomless product space may be identified with [0,1] modulo null sets, so this introduces no convention gap. The resulting closure only certifies the tensor products actually discussed; no arbitrary-mixture closure of the inequality is inferred.

## 5. Principal restriction, irregularity, and negative controls

For the complete r-partite r-kernel on r equal cells, fixing two coordinates in distinct cells leaves `(r-2)!` admissible arrangements out of `r^(r-2)`. This gives the stated positive cross-cell marginal value h; same-cell marginal values are zero. Restricting to two cells renormalizes their measures to 1/2 while leaving the kernel values unchanged. The restricted marginal is therefore exactly `(h/2)U_1`. A lift for it would scale to a lift for U_1, contradicting the binary threshold. This proves principal-restriction nonclosure for every r>=3, including the r=3 value `(1/6)U_1`.

For the irregular five-cell host, each supported ordered pair has marginal value 1/5. The mean is 12/125, and integration over a cell contributes another factor 1/5. Thus the normalized operator matrix is `(5/12)A`, exactly as claimed. Its degree vector before normalization is `(4,2,2,2,2)/25`. The test vector (-2,1,1,1,1) gives the Rayleigh quotient -5/8. This is below -1/2 and rules out an unweighted extension of the regular spectral bound. The weighted covariance inequality remains true; independently its two sides are -12/125 and -12/125 for this vector.

The theta=2/5 parity control and normalized triangle ratio 26/27 are correct. The outside-budget scalar product at B=17/16 is 495/512; the text properly labels it as a failure of a sufficient lower-bound argument, not a realizable spectrum or host certificate.

## 6. Independent primary-source scope review

- The [AIM source](http://aimpl.org/highdimdiscrete/3/) and [Spiro problem list](https://samspiro.xyz/Research/P2Solve.pdf) match the target and private-leaf convention. Spiro PDF page 3 explicitly proposes compensating a C5 by disjoint Sidorenko components. The report's attribution and low novelty confidence are appropriate. Pages 2-3 were inspected in retained text, and page 3 was visually inspected.
- [Nie and Spiro, arXiv:2309.12873v2](https://arxiv.org/abs/2309.12873v2), dated 20 June 2025, has the claimed clique-containing obstruction, finite-gap hypothesis, and forward-preservation result on PDF page 6. Its later questions retain the converse issue. The statements and formulas were checked in retained primary text and page 6 was visually inspected. No infinite-gap passage is imported.
- [Nie and Spiro, arXiv:2408.03406v2](https://arxiv.org/abs/2408.03406v2), dated 7 December 2024, states after Theorem 2.1 that the existence question is unknown. The report does not misidentify a random-Turan result as solving it.
- [Hyunwoo Lee, arXiv:2509.08680v2](https://arxiv.org/abs/2509.08680v2), dated 1 October 2025, was checked in primary text and visually on PDF page 3. The paper explicitly works with labelled hypergraphs. Its Theorem 1.4 uses actual sub-hypergraphs of one maximum link, not independently relabelled isomorphic copies. In a strong expansion, distinct edges intersect in at most k-1<=r-2 vertices. Two vertex links in the same part cannot share an (r-1)-edge. Containment in the maximum link then forces every other link to be edgeless. All expansion edges contain the maximum-link vertex. If the core is a graph with at least two edges, a private leaf cannot be that common vertex; the original graph is a star with possible isolates. Thus the final structural-scope paragraph is valid. The report appropriately limits this conclusion to direct application to graph expansions.
- [Yuqi Zhao, arXiv:2607.02260v1](https://arxiv.org/abs/2607.02260v1), submitted 2 July 2026, has the stated title and author. Fresh official HTML and visually inspected PDF pages 3 and 5 independently confirm Theorem 1.3 and Definition 2.1. Admissibility requires tensor-power closure and normalized-principal-restriction closure, precisely in the sense used by the report. The new cone example violates the latter condition, so that theorem cannot be applied directly to this class. This checks an applicability boundary; it does not independently audit Zhao's theorem or rule out every other regularization method.
- [Konstantopoulos and Yuan, arXiv:1501.06188v4](https://arxiv.org/abs/1501.06188), last revised 13 December 2016, has the cited authors, title, and finite-extendibility subject. The proof here is elementary and self-contained rather than an unverified application of that paper. The Diaconis-Freedman reference is likewise only general background. Direct access to its DOI/Project Euclid article was blocked during this audit; no mathematical acceptance depends on that reference.

No specialist novelty certification is supplied. The covariance/finite-exchangeability ideas are standard, the compensated-core strategy is expressly prior, and the specific spectral-budget application may be a useful elementary scoped observation without being a solution of the source problem.

## 7. Supporting verification metadata and acceptance limits

The mathematical audit recorded 75 passing independent exact-arithmetic verification groups and 34 passing proposed verification groups. These aggregate totals are supporting audit metadata, not mathematical proof or a completeness certificate. Edition preparation does not claim a fresh execution of those checks.

The analytic arguments in Sections 1–6 supply the infinite-dimensional justification. The audit accepts only the stated hypotheses and conclusions of the exact distributed report identified above. Any substantive mathematical change requires re-review. The original existence/converse problem remains unresolved by this work; novelty remains unconfirmed.
