# Strong expansions: a global spectral exclusion and sharp binary lift boundary

Problem: AIM-COMBINATORICS-0011 / 20000886. Accepted scoped partial, substantive attempt 1 of 5.
Status: **proved scoped partial results; the original existence/converse question remains unresolved by this work**.
Date: 2026-10-10 UTC. This is an AI-assisted, unrefereed proof-only edition.

## 1. Target, conventions, and exact scope

For a finite simple k-uniform hypergraph F and r>k, E^r(F) adds r-k distinct private vertices to each edge. All new vertices have degree one. An r-graph J is Sidorenko if

  hom(J,G)/n^{v(J)} >= (r! e(G)/n^r)^{e(J)}

for every finite simple r-graph G on n vertices. Homomorphisms need not be injective, but each source edge must map bijectively onto a target edge. Isolated vertices are immaterial.

We use a probability space X=[0,1] with Lebesgue measure and symmetric bounded nonnegative kernels W:X^r -> [0,infinity). Set

  t_J(W) = integral product_{e in E(J)} W(x_e),   p(W)=integral W.

It suffices to use [0,1]-valued kernels: multiplying W by a positive constant multiplies both sides of the Sidorenko inequality by that constant to the power e(J). Thus nonnegative bounded lifts can be rescaled before use as ordinary dense kernels. The distinction is important: a nonconstant kernel of mean 1 cannot itself have a [0,1]-valued lift of mean 1.

These kernel and finite-hypergraph definitions are equivalent. A finite host gives its adjacency step kernel, with a value zero on cell tuples with repeated vertex indices. Conversely, for a bounded [0,1]-kernel sample n iid vertex labels and then independent r-edges, with the appropriate W-value as their conditional probabilities. For any fixed simple J, injective source maps have the expected integral t_J(W), while noninjective maps constitute O_J(1/n) of all maps. The variance of the normalized homomorphism count tends to zero: terms from disjoint sets of sampled host vertices are independent, and pairs sharing a vertex constitute O_J(1/n) of the total. The same holds for edge density. Hence a strict kernel violation yields a finite violation with positive probability for sufficiently large n. This argument does not require J to be linear and does not assume that every general hypergraph limit has only vertex coordinates.

Write U=M_{r->k}W for the k-coordinate marginal. Fubini and the private-leaf condition give exactly

  t_{E^r(F)}(W)=t_F(U),   integral U=integral W.

This identity is standard. It is the only expansion reduction needed below. We neither infer global nonnegative surjectivity from an ANOVA right inverse nor rely on its novelty.

Our main test core is F=C4 disjoint-union C5. It is genuinely non-Sidorenko: the host K2 has positive edge density 1/2 but no C5 homomorphism, so t_F(K2)=0. It has nine edges. For every strong expansion,

  t_{E^r(F)}(W)=t_C4(U)t_C5(U),   U=M_{r->2}W.

The compensated disconnected-core strategy is prior art: Spiro's live problem list, PDF page 3, Question 2.2, proposes C5 together with many Sidorenko components. We claim no novelty for that strategy.

## 2. Exchangeability gives an operator inequality

**Lemma 1 (weighted form).** Let r>=2, W>=0 be bounded and symmetric, U=M_{r->2}W, and d(x)=integral U(x,y)dy. For every real f in L2(X),

  integral U(x,y)f(x)f(y) dxdy >= -1/(r-1) integral d(x)f(x)^2 dx.       (1)

**Proof.** Integrate the nonnegative function W(x_1,...,x_r)(sum_i f(x_i))^2. The r diagonal terms give r integral d f^2 and the r(r-1) ordered off-diagonal terms give r(r-1) integral U f f. Boundedness of W makes every term integrable. Rearrangement proves (1). The proof is the elementary finite-exchangeability covariance bound; it is not claimed as a new probability result. □

Assume now that d(x)=p almost everywhere and p>0. Define the integral operator

  Tf(x)=integral [U(x,y)/p] f(y)dy.

It is compact and self-adjoint because U/p is bounded and symmetric, and it is a Markov contraction on L2: T1=1 and Jensen gives ||Tf||_2^2 <= integral T(f^2)=||f||_2^2. Thus every eigenvalue lies in [-1,1], and (1) sharpens the lower endpoint to

  lambda >= -1/(r-1).                                             (2)

The constant function provides one distinguished eigenvalue 1; any further eigenvalues equal to 1 are retained among the other nonnegative eigenvalues. The spectrum may be infinite, with multiplicity, but is square summable. Consequently all sums of fourth and fifth powers below converge absolutely. The trace identities are

  t_C4(U)/p^4=Tr(T^4)=sum lambda^4,
  t_C5(U)/p^5=Tr(T^5)=sum lambda^5.                               (3)

For completeness, the kernel of T^2 is the integral composition of two bounded kernels. T^2 is Hilbert-Schmidt, and Tr(T^4)=||T^2||_HS^2 is exactly the C4 integral by Fubini. Likewise Tr(T^5)=<T^2,T^3>_HS is the C5 integral. The Hilbert-Schmidt spectral expansion proves the sums in (3), without any unverified diagonal trace formula for T itself.

## 3. A global negative-spectrum budget theorem

**Theorem 2.** Under the preceding assumptions, let

  B = sum_{lambda<0} |lambda|^4.

If B<=r-2, then

  t_{E^r(C4 disjoint-union C5)}(W) >= p^9.                        (4)

This is a global statement on a specified class of hosts. W need not be close to a constant in any norm.

**Proof.** Write c=1/(r-1). Separating the distinguished eigenvalue 1 and ignoring all other nonnegative contributions yields

  t_C4(U)/p^4 >= 1+B,
  t_C5(U)/p^5 >= 1-c B.

The second inequality uses |lambda|^5<=c|lambda|^4 on the negative spectrum. Since B<=r-2, its right side is at least 1/(r-1)>0. Multiplying the two lower bounds is therefore valid. Their product is

  (1+B)(1-B/(r-1))
    = 1+B(r-2-B)/(r-1) >= 1.

Apply the exact marginal identity. If p=0, W=0 almost everywhere and (4) holds directly, so the degenerate case needs no spectral normalization. □

**Corollary 3 (finite-rank exclusion).** Every constant-degree r-marginal having at most (r-2)(r-1)^4 strictly negative eigenvalues satisfies (4). In particular, no regular 3-marginal with at most 16 negative eigenvalues can disprove (4). Any step kernel on at most 17 positive-measure parts has operator rank at most 17 and includes the positive eigenvalue 1 after normalization; hence any such *regular* 3-marginal satisfies (4), regardless of its step values or the part sizes.

**Proof.** Each negative eigenvalue contributes at most (r-1)^(-4) to B. □

**Corollary 3a (arbitrary-rank L2 and density exclusions).** Theorem 2 also applies whenever

  integral U(x,y)^2 dxdy / p^2 <= 1+(r-2)(r-1)^2.                 (4a)

Indeed, by (2),

  B <= (r-1)^(-2) sum_{lambda<0}|lambda|^2
    <= (r-1)^(-2) (||T||_HS^2-1)
     = (r-1)^(-2) (integral U^2/p^2-1).

This covers infinite-rank kernels as well. If 0<=U<=L, then integral U^2<=Lp, so it suffices that L/p<=1+(r-2)(r-1)^2. In particular, for a [0,1]-valued W whose pair marginal is regular, mean p>=1/[1+(r-2)(r-1)^2] guarantees (4). For r=3 this threshold is p>=1/5. This is a global dense-host statement; it imposes no small perturbation or rank assumption. It still requires constant pair degree.

**Generalization.** Let a>=2 and b>=a, d=2b+1-2a, c=1/(r-1), and B_{2a}=sum_{lambda<0}|lambda|^{2a}. The same proof gives

  t_C(2a)(U)t_C(2b+1)(U) >= p^{2a+2b+1}

whenever B_{2a}<=c^(-d)-1. Indeed the two normalized traces are at least 1+B_{2a} and 1-c^d B_{2a}; their product minus 1 is B_{2a}(1-c^d-c^d B_{2a}). The allowed budget ensures both factors are nonnegative.

The bound is a sufficient exclusion criterion, not a sharp characterization of feasible marginal spectra. Its failure is not evidence that a counterexample exists.

## 4. Sharp global lift boundary for a binary counterexample direction

Partition X into two sets of measure 1/2 and let f equal +1 and -1 on them. For 0<=theta<=1 set

  U_theta(x,y)=1-theta f(x)f(y).

This is nonnegative, symmetric, of mean 1 and constant degree 1. Its two nonzero operator eigenvalues are 1 and -theta (at theta=0 only 1 remains).

**Theorem 4 (exact bounded-nonnegative extension threshold).** U_theta is the two-coordinate marginal of some symmetric bounded nonnegative r-kernel if and only if

  theta <= c_r,
  c_r = 1/(r-1) when r is even, and c_r=1/r when r is odd.          (5)

**Necessity.** If W is a lift, integral W=1. Under the probability law with density W on X^r, put S=sum_i f(x_i). Every off-diagonal correlation is -theta, so

  E[S^2]=r-r(r-1)theta.

For even r, S^2>=0; for odd r, S is an odd integer and S^2>=1. These inequalities give precisely (5). This argument allows *every* bounded symmetric lift, including lifts depending on more than the signs of the coordinates. Therefore a richer lift cannot evade the obstruction. It also applies to any integrable nonnegative lift.

**Sufficiency, including endpoints.** Let epsilon_r=0 for even r and 1 for odd r. Let A_r consist of the sign tuples with |S|=epsilon_r. Its product-measure probability is

  q_r=2^(-r) binom(r,r/2),                         r even;
  q_r=2^(1-r) binom(r,(r-1)/2),                    r odd.

Define W_*=1_{A_r}/q_r. This is bounded, symmetric, nonnegative and has mean 1. Sign complementation shows its one-coordinate sign mean is zero. Coordinate symmetry and S^2=epsilon_r imply its pair correlation equals -c_r. For two balanced signs, complement symmetry and this correlation determine the four cell probabilities uniquely. Because W_* depends only on the signs, its pair marginal is exactly 1-c_r f(x)f(y), pointwise on each of the four rectangles, up to null boundaries. For 0<=theta<=c_r the convex mixture

  W_theta=(1-theta/c_r) * 1 +(theta/c_r) W_*

has marginal U_theta. This proves sufficiency. To obtain a [0,1]-kernel multiply W_theta and U_theta by q_r; the bound W_theta<=1/q_r gives 0<=q_r W_theta<=1. □

For r=3, q_r=3/4, c_r=1/3, and the endpoint [0,1]-lift is simply the indicator that a triple is not monochromatic. Its pair marginal is 1/2 on equal-sign cells and 1 on unequal-sign cells, with mean 3/4.

**Corollary 5 (the whole liftable binary ray is safe for this candidate).** For every r>=3 and theta satisfying (5),

  t_C4(U_theta)t_C5(U_theta)
    =(1+theta^4)(1-theta^5)
    =1+theta^4(1-theta-theta^5) >=1.                              (6)

Indeed c_r<=1/3 for r>=3, and 1-theta-theta^5>=1-1/3-1/243>0. At theta=1, in contrast, U_1 is the normalized complete bipartite kernel and the product is zero. Thus a genuine global core witness is explicitly separated from the entire nonnegative marginal cone along this ray. This proves that global nonnegative marginal surjectivity is false, even with no upper bound on W. It does **not** prove that the expansion is Sidorenko: other directions remain.

The same ray obeys the corresponding inequality for C_(2a) disjoint-union C_(2b+1) with b>=a, by the expression theta^(2a)[1-theta^d-theta^(2b+1)] and theta<=1/3.

Products are no escape along this tested family. If U and V have bounded nonnegative symmetric r-lifts, then U tensor V has the product lift on (X times X)^r. Homomorphism and edge densities multiply. Therefore finite tensor products of these certified binary kernels also satisfy the compensated inequality. This is a scoped closure statement, not a closure assertion under arbitrary mixtures.

## 4a. Why tensor regularization is not automatic

Let C_r denote the cone of bounded nonnegative pair kernels with bounded symmetric nonnegative r-lifts. It is tensor-closed by the product construction above. For every r>=3 it is **not** closed under normalized principal restrictions.

To prove this, partition X into r equal cells and let W be the indicator that its r coordinates occupy all r cells exactly once. Its pair marginal is zero on each same-cell rectangle and equals h=(r-2)!/r^(r-2)>0 on each different-cell rectangle. Restrict the underlying probability space to the union of two cells, with its conditional probability measure. The two retained cells each have measure 1/2, so the restricted kernel is (h/2)U_1. If it had a bounded nonnegative r-lift, scaling that lift by 2/h would give a lift of U_1, contradicting Theorem 4. In particular, for r=3 we have h=1/3 and restriction gives (1/6)U_1.

This failure is a concrete obstacle to importing a regularization theorem for the ambient class of graphons into the marginal class. For example, Zhao's arXiv:2607.02260v1, Definition 2.1 and Theorem 1.3, assumes closure under both tensor powers and normalized principal restrictions. C_r fails the latter hypothesis. We do not conclude that every possible regularization method fails, only that this stated hypothesis is genuinely unavailable.

## 5. Negative controls and limitations

1. **Regularity is essential to (2).** Take the 3-graph on five equal cells with edges {0,1,2} and {0,3,4}. Its pair marginal operator, divided by its mean, is (5/12)A, where A is the adjacency matrix of two triangles sharing their center. For z=(-2,1,1,1,1), z^T A z=-12 and z^T z=8, so the normalized Rayleigh quotient is -5/8<-1/2. This is a genuine nonnegative symmetric 3-kernel. It refutes an extension of the *constant-degree normalized spectral bound* to arbitrary marginals. It does not refute the weighted inequality (1) or the target Sidorenko inequality.
2. **The binary parity refinement matters.** For r=3 the generic covariance bound only says theta<=1/2, but the exact threshold is 1/3. For example theta=2/5 obeys the generic bound and still has no nonnegative 3-lift, since its required E[S^2]=3/5 is below the pointwise lower bound 1.
3. **Triangle expansions remain non-Sidorenko.** The endpoint binary 3-lift has normalized C3 density 1-(1/3)^3=26/27<1. Thus the verification does not accidentally claim every marginal is Sidorenko, nor does it replace the odd-cycle obstruction with positivity.
4. **The cutoff is an argument limit.** The two numerical lower bounds at r=3 and B=17/16 have product 495/512<1. This merely shows that this multiplication proof does not extend beyond B=1 without further information. It is not a feasible-marginal certificate or a counterexample.

The original question remains unresolved. We have not proved the compensated inequality for irregular marginals, nor for all regular marginals with larger negative-spectrum budget; we have not exhibited a Sidorenko expansion of a non-Sidorenko core; and we have not proved the universal converse. The new-looking contribution is the explicit global spectral-budget exclusion applied to an established candidate. The probability and spectral ingredients are elementary and standard; novelty confidence is low pending specialist review.

## 6. Current literature and provenance

- AIM, High-dimensional phenomena in discrete analysis, Section 3, Problem 3.2: http://aimpl.org/highdimdiscrete/3/ . The private-leaf wording fixes strong expansion.
- Sam Spiro, *Problems that I would like Somebody to Solve*: https://samspiro.xyz/Research/P2Solve.pdf . PDF page 2 Problem 2.1 is the target; PDF page 3 Question 2.2 is the prior disconnected-compensation idea. The live PDF identity is recorded in SOURCE_METADATA.json, without assigning a date from crawl metadata.
- Jiaxi Nie and Sam Spiro, *Sidorenko Hypergraphs and Random Turán Numbers*, arXiv:2309.12873v2, 20 June 2025: https://arxiv.org/abs/2309.12873v2 . Theorem 1.9 excludes cores containing K_(k+1)^k. Corollary 1.12 gives the known forward direction. Theorem 1.11 requires a finite gap. Nothing here applies it to an infinite gap.
- Nie and Spiro, *Random Turán Problems for Hypergraph Expansions*, arXiv:2408.03406v2, 7 December 2024: https://arxiv.org/abs/2408.03406v2 . The retained PDF records the converse as unknown.
- Hyunwoo Lee, *On Sidorenko exponents of hypergraphs*, arXiv:2509.08680v2, 1 October 2025: https://arxiv.org/abs/2509.08680v2 . Primary PDF page 3 was visually inspected during this attempt. Theorem 1.4 is a nested-link Sidorenko criterion, while Theorem 1.6 bounds an exponent. Lee's exponent is e(F) plus Nie–Spiro's gap. These are not expansion-converse theorems.
- Yuqi Zhao, *Tensor Amplification and Spectral Transfer for Sidorenko-Type Inequalities*, arXiv:2607.02260v1, 2 July 2026: https://arxiv.org/abs/2607.02260v1 . Definition 2.1 requires principal-restriction closure as well as tensor closure. Theorem 1.3 is therefore not applied here; Section 4a proves its class hypothesis fails.
- P. Diaconis and D. Freedman, *Finite Exchangeable Sequences*, Annals of Probability 8(4) (1980), 745–764, https://doi.org/10.1214/aop/1176994663 . This is background for finite exchangeability and sampling without replacement; the bounds used here are proved directly, not asserted as a newly discovered probability theorem.
- Takis Konstantopoulos and Linglong Yuan, *On the extendibility of finitely exchangeable probability measures*, arXiv:1501.06188v4, 13 December 2016: https://arxiv.org/abs/1501.06188v4 . General finite extendibility is an established subject. We do not claim novelty for restating marginal extension as that problem or for a finite-dimensional convex-dual description.

A structural scope check on Lee's criterion is useful. Distinct edges in E^r(H) intersect in at most k-1<=r-2. Thus links of different vertices in the same part cannot share an edge. Under Lee's hypothesis that all these links are subgraphs of one maximum link, only one link can be nonempty. All expansion edges therefore meet that one vertex. For graph cores with at least two edges, it must be an original core vertex, so the graph is a star (plus isolates), which is already Sidorenko. Consequently Theorem 1.4 does not directly certify a non-Sidorenko *graph* expansion. We make no analogous unrestricted claim for higher-uniformity cores or for combinations with other constructions.
