# Independent adversarial validation: caret metric and ℓ¹ in cones of F

Validator scope: only this file; no Git operations, outside contacts, or edits to other agents' files. The candidate statements were treated as hypotheses. This audit makes no novelty claim.

## Research log and completion estimate

- 2026-10-17 20:51:53 UTC: audit begun. Checked possible failure of the triangle inequality and possible cancellation of carets inside grafted blocks. Validation completion estimate: 10%.
- 2026-10-17 20:53:55 UTC: core arguments and the continuum-index extension verified; exact word-metric constants checked against a primary paper. Validation completion estimate: 100%. This estimate concerns the lemma audit, not discovery or novelty of the surrounding research program.
- 2026-10-17 20:54:23 UTC: supplementary coarse-shift lemma and finite-center obstruction verified, with the necessary product-metric and uniform-closeness hypotheses made explicit. Validation completion estimate: 100%.
- 2026-10-17 20:56:02 UTC: canonical two-block cone-product image identified with the stabilizer cone and proved proper by a normalized logarithmic displacement. Validation completion estimate: 100%.
- 2026-10-17 20:56:26 UTC: optional strengthening to the full real measure Banach space M(C) verified using regularity and refining cylinder partitions. Validation completion estimate: 100%.

## Strongest verified conclusion

Let F be standard binary Thompson F. Let N(g) be the number of carets in either tree of its reduced tree pair, allowing the trivial one-leaf tree for the identity, so N(1)=0. Then d_N(g,h)=N(g⁻¹h) is a left-invariant metric. For every nonprincipal ultrafilter ω on ℕ and every positive real scale sequence r_i→∞, Cone_ω(F,d_N,(r_i)) contains an isometric copy of ℓ¹(I), where I={0,1}^ℕ has cardinality continuum. In particular it contains an isometric ℓ¹(ℕ).

The same representatives give an embedding into every asymptotic cone for the standard word metric |·|_{x₀,x₁}, satisfying

    ||a−b||₁ ≤ d_word(Φ(a),Φ(b)) ≤ 4||a−b||₁.

For any other fixed finite generating set, this gives uniform bilipschitz constants depending only on that generating set, independently of ω and the scale sequence. The conclusion also holds with arbitrary basepoint sequences by coordinatewise left translation.

No counterexample was found. The exact proofs below resolve the proposed elementary mechanism; novelty and comparison with prior infinite-dimensional embeddings remain outside this audit.

## 1. The caret count really defines a metric

Encode a binary tree by its finite, prefix-closed set of internal vertices in {0,1}*. The common refinement of two trees is obtained by taking the union of those sets. Consequently its number of carets is at most the sum of their caret counts.

To multiply reduced tree pairs for g and h, expand their middle trees to this common refinement. Both outer trees then have as many carets as that refinement, because an expansion adds one caret to each member of its pair. Subsequent reductions only decrease the count. Therefore

    N(gh) ≤ N(g)+N(h).

Inversion exchanges the two trees, so N(g⁻¹)=N(g). The only reduced zero-caret pair is the identity. These facts prove definiteness, symmetry, and the triangle inequality for d_N. Left invariance follows directly from (ag)⁻¹(ah)=g⁻¹h. No conjugation invariance is used or claimed.

Boundary case: the identity must be given N(1)=0. If one follows a convention retaining a root caret for the identity and uses its unmodified caret count, d(1,1) would be 1 and would fail to be a metric. This is a convention issue already fixed in the candidate statement.

## 2. Grafting reduced blocks cannot cancel block-internal carets

Fix a full binary scaffold T with n leaves. Graft the reduced pair for f_j into leaf j in each copy of T. The resulting pair represents a homomorphism

    B_T : Fⁿ → F,

because it acts separately on the n dyadic intervals indexed by T. Its unreduced caret count is

    (n−1)+Σ_j N(f_j).

Here is the reduction invariant needed for the lower bound. Corresponding blocks have equal numbers of leaves in the two trees, so their boundaries have the same leaf indices. An exposed caret strictly inside block j can pair only with a caret strictly inside the corresponding block j: its two leaves lie between those common boundaries. Such a pairing would contradict the reducedness of f_j. A scaffold caret can become exposed only after every block underneath it has collapsed to a leaf. Initially this occurs precisely for subscaffolds consisting of identity blocks. Cancelling a matching exposed scaffold caret preserves the invariant and does not alter any nonidentity block.

Thus every cancellation removes a scaffold caret in both trees; no caret originally internal to any reduced f_j is removed. This proves

    Σ_j N(f_j) ≤ N(B_T(f₁,…,f_n)) ≤ Σ_j N(f_j)+(n−1).

More exactly, if S={j:f_j≠1}, then the retained scaffold carets are precisely the internal vertices of T having a descendant leaf in S. Hence

    N(B_T(f₁,…,f_n)) = Σ_j N(f_j)+κ_T(S),

where 0≤κ_T(S)≤n−1. For S=∅ all scaffold carets cancel, producing the identity. This also checks the all-identity boundary case.

## 3. Powers and the finite-block estimate

For either conventional orientation of x₀, and every nonzero integer k,

    N(x₀^k)=|k|+1.

For k>0, one can display x₀^k using the left comb and right comb with k+1 carets, exchanging the pair if the generator convention is reversed. Their only exposed carets occupy the first two and last two leaves respectively, so for k≥1 they have no matching exposed caret. The diagram is reduced. Negative k follows by inversion; k=0 must be treated separately and has N=0.

If s is the number of nonzero k_j, the exact count from §2 is

    N(B_T(x₀^{k₁},…,x₀^{k_n})) = Σ_j |k_j|+s+κ_T({j:k_j≠0}).

In particular,

    Σ_j |k_j| ≤ N(B_T(x₀^{k₁},…,x₀^{k_n})) ≤ Σ_j |k_j|+2n−1.

The n=1 case and all-zero tuple satisfy these inequalities. No geometric bound on the depth of T is needed.

## 4. Countably indexed ℓ¹ embedding: quantifiers and errors

Choose integers n_i→∞ with n_i/r_i→0, and any n_i-leaf scaffold T_i. For a∈ℓ¹(ℕ), define

    g_i(a)=B_{T_i}(x₀^{⌊r_i a₁⌋},…,x₀^{⌊r_i a_{n_i}⌋}).

The homomorphism property of B_{T_i} means that g_i(a)⁻¹g_i(b) is exactly the blocksum with exponents

    k_{i,j}=⌊r_i b_j⌋−⌊r_i a_j⌋.

For real u,v, |⌊u⌋−⌊v⌋−(u−v)|<1, including negative inputs. Therefore, writing

    L_i(a,b)=Σ_{j≤n_i}|a_j−b_j|,

the finite-block estimate gives

    L_i(a,b)−n_i/r_i ≤ N(g_i(a)⁻¹g_i(b))/r_i
                         ≤ L_i(a,b)+(3n_i−1)/r_i.

The two error terms are uniform in a,b. Since L_i(a,b)→||a−b||₁, the normalized distances converge ordinarily to ||a−b||₁. This is stronger than merely having the desired ω-limit. Taking b=0 shows that g_i(a) is an admissible cone representative; a uniform bound follows from the displayed estimate and the boundedness of n_i/r_i after finitely many initial terms.

Consequently a↦[g_i(a)]_ω is defined simultaneously for every a, is injective, and is isometric. No diagonal subsequence depending on a,b or on ω is taken. The result works for every nonprincipal ω with the originally supplied r_i.

The candidate's total error should be recorded as O(n_i/r_i), or with the explicit bounds above. Rounding alone costs at most n_i/r_i for a difference of floors. Power-diagram overhead and scaffold overhead contribute at most another (2n_i−1)/r_i. Any smaller claimed universal total bound needs separate justification; the limiting conclusion is unaffected.

## 5. Continuum-index extension

Let I={0,1}^ℕ and ℓ¹(I) denote all real families with summable absolute values. Such a family has countable support. For a finite binary word w of length m, set

    A_m(a)_w=Σ_{x∈I, x|m=w}a_x.

The sums are absolutely convergent and ||A_m(a)||₁≤||a||₁. Moreover

    ||A_m(a)||₁ → ||a||₁ as m→∞.

Proof: choose a finite support subset E carrying all but ε of the absolute mass. Sufficiently long prefixes separate all members of E. For these m, aggregation is isometric on a|E. The aggregated tail has norm at most ε. Thus

    ||A_m(a)||₁ ≥ ||a|E||₁−ε ≥ ||a||₁−2ε.

The upper bound is contractivity. This proves the asserted convergence. Refinement also shows that these finite-partition norms are monotone increasing. In particular the same argument applies to c=a−b.

Choose m_i→∞ such that n_i=2^{m_i}=o(r_i), use the complete depth-m_i binary scaffold, and let the exponent in leaf w be ⌊r_i A_{m_i}(a)_w⌋. Such a choice always exists; for example, eventually take m_i=⌊(log₂r_i)/2⌋. The same floor estimate yields

    ||A_{m_i}(a−b)||₁−n_i/r_i ≤ N(g_i(a)⁻¹g_i(b))/r_i
                                  ≤ ||A_{m_i}(a−b)||₁+(3n_i−1)/r_i.

Taking ordinary limits proves the isometric ℓ¹(I) embedding claimed above. No fixed enumeration of I or of its supports is needed, and no simultaneous separation of all points of I at a finite stage is claimed. Every fixed finite subset is eventually separated, which is exactly what summability requires.

Cardinality check: |I|=c; countable supports and real coefficient sequences give |ℓ¹(I)|=c^{ℵ₀}=c. An asymptotic cone of the countable group F has cardinality at most |F^ℕ|=c, so this does not violate cardinality. The unit vectors form a c-sized 2-separated set in the source; this correctly predicts nonseparability of the target cones.

## 6. Word-metric passage and exact source

The elementary arguments above are independent of word-length formulae. For the word-metric conclusion I checked the primary source [Cleary and Taback, *Combinatorial properties of Thompson's group F*, Theorem 3.1, PDF p.10](https://arxiv.org/pdf/math/0208117). For a nonidentity reduced pair with N carets it states

    N−2 ≤ |g|_{x₀,x₁} ≤ 4N−4.

With our identity convention the globally safe inequalities are

    N(g)−2 ≤ |g|_{x₀,x₁} ≤ 4N(g).

They show quasi-isometry directly and ensure that the same g_i(a) are word-cone admissible. Dividing by r_i and taking ω-limits gives

    ||a−b||₁ ≤ d_word([g_i(a)]_ω,[g_i(b)]_ω) ≤ 4||a−b||₁.

The identity normalization affects no asymptotic conclusion. Arbitrary finite generating sets are bilipschitz equivalent word metrics with constants depending only on the two sets. Arbitrary cone basepoints p_i are handled by replacing g_i(a) with p_i g_i(a), using left invariance of either metric.

## Audit boundaries and remaining gap

Verified mechanisms: common refinement/subadditivity; symmetry and normalization; graft reduction invariant; all-zero and one-block cases; powers of either sign; negative-input rounding; cone admissibility; ordinary rather than only ultrafilter convergence; arbitrary scale/ultrafilter quantifiers; prefix aggregation with cancellation; continuum cardinality; word-cone constants.

There is no unsupported equivalent claim to mark as a blocked route in this construction. The remaining research gap is historical: this audit does not establish that the infinite-dimensional or continuum-density conclusion is new. Fixed finite-dimensional block embeddings alone should not be presented as a novelty argument, and the continuum-index proof should be stated explicitly if that stronger conclusion is promoted.

## Supplemental audit: coarse shifts and the finite-center obstruction

The second submitted lemma is also valid, under an explicit metric hypothesis. Equip Y=X×ℤ with a standard product metric for which T_n(x,k)=(x,k+n) is an isometry and d_Y(T_n y,y)=|n|; both the sum and maximum product metrics qualify. Let q:Y→X be an (L,A)-quasi-isometry, let p:X→Y be a quasiinverse, and choose D,E satisfying

    sup_x d_X(qp(x),x) ≤ D,
    sup_y d_Y(pq(y),y) ≤ E.

Define τ_n=qT_np. Since q and p have fixed quasi-isometry constants and T_n is an isometry, the τ_n are quasi-isometries with constants independent of n. Coarse surjectivity is uniform: the E-density of p(X) in Y gives a (LE+A+D)-density bound for qT_np(X) in X. The displacement bounds are

    L⁻¹|n|−A−D ≤ d_X(τ_n(x),x) ≤ L|n|+A+D

for every x,n, by comparing qT_np(x) with qp(x). The composition defect obeys

    sup_x d_X(τ_mτ_n(x),τ_{m+n}(x)) ≤ LE+A,

because pq is E-close to id_Y and translation T_m preserves distances. Also τ_0 is D-close to id_X. These estimates do not assert that the maps form an exact action.

Now take X to be a finitely generated group G with a left-invariant word metric, and suppose its center is finite. If there were g_n∈G and a single D₀ such that

    sup_{n,x} d_G(τ_n(x),xg_n) ≤ D₀,

then for every generator s and n, the uniform quasi-isometry upper bound for τ_n would give

    |g_n⁻¹sg_n| = d_G(xg_n,xsg_n) ≤ K+C+2D₀.

There are finitely many elements of this bounded word ball, so there are only finitely many possible tuples (g_n⁻¹sg_n) indexed by the fixed finite generating set. An inner automorphism is determined by such a tuple; its kernel as a function of the conjugating element is precisely Z(G). Thus the g_n lie in finitely many center cosets. Since Z(G) is finite, {g_n} itself is finite and has bounded word length. It follows that

    d_G(τ_n(x),x) ≤ D₀+sup_n|g_n|

uniformly in x,n, contradicting the lower displacement estimate as |n|→∞.

The composition-defect estimate is not needed for this contradiction. The decisive assumptions are a uniform quasi-isometry upper bound, one closeness constant D₀ for every n and x, finite generation, and finite center. Allowing the closeness bound to depend on n destroys this argument. The result excludes only such approximations by right translations; it does not rule out nonlinear coarse shifts, and therefore does not by itself solve a product-splitting or quasi-isometry problem for G.

## Supplemental audit: the canonical cone product has proper image

Fix ω and r_i→∞, and write C_N=Cone_ω(F,d_N,(r_i)). Let p=1/2 and let B:F×F→F be the two-leaf blocksum, acting by rescaled copies of its two arguments on [0,p] and [p,1]. Use ordinary functional composition, so gu=g∘u. Set H=Stab_F(p).

For arbitrary f₁,f₂,g₁,g₂∈F, the two-block count gives

    N(f₁⁻¹g₁)+N(f₂⁻¹g₂)
       ≤ d_N(B(f₁,f₂),B(g₁,g₂))
       ≤ N(f₁⁻¹g₁)+N(f₂⁻¹g₂)+1.

Dividing by r_i proves that B induces a well-defined isometric embedding

    β : C_N ×₁ C_N → C_N,

where the product metric is the sum of the two cone distances. Every h∈H preserves the two halves. Rescaling its restrictions to the halves gives two elements of F, so B(F×F)=H exactly. Conversely, the lower caret inequality shows that if a sequence in H is cone-admissible, then both of its component sequences are admissible. Thus the image of β is precisely the embedded cone of H equipped with the metric restricted from d_N. This assertion concerns the restricted metric; an intrinsic word metric on H is unnecessary.

Define

    λ(g)=log₂(g⁻¹(p)/p).

A binary tree with N carets has every leaf at depth at most N. A linear piece represented by a leaf pair has slope 2^{d_source−d_target}, so every slope of u∈F lies in [2^{-N(u)},2^{N(u)}]. The same holds for u⁻¹. Since these maps fix 0, integrating the slope bounds gives

    2^{-N(u)} ≤ u⁻¹(t)/t ≤ 2^{N(u)}    (0<t≤1).

If h=gu and t=g⁻¹(p), then h⁻¹(p)=u⁻¹(t). Hence

    |λ(h)−λ(g)| = |log₂(u⁻¹(t)/t)| ≤ N(u)=d_N(g,h).

Therefore λ is 1-Lipschitz for d_N and λ(h)=0 for every h∈H.

For the standard generator orientation with x₀(t)=t/2 on the whole interval [0,1/2], one has x₀^n(p)=2^{-n}p, and therefore

    λ(x₀^{-n})=−n    (n≥0).

This proves, for n≥1,

    n ≤ d_N(x₀^{-n},H) ≤ N(x₀^{-n})=n+1.

The exact formula needs x₀(t)=t/2 on [0,p], not merely on an unspecified neighborhood of 0. Under only the latter hypothesis, the orbit is eventually in that neighborhood and the equality becomes −n+O(1); the cone conclusion below still follows.

Take n_i=⌊r_i⌋ and z=[x₀^{-n_i}]_ω∈C_N. For every point y=[h_i]_ω in the embedded cone of H, choose its representative h_i∈H. The 1-Lipschitz inequality gives

    d_N(x₀^{-n_i},h_i)/r_i ≥ n_i/r_i → 1,

so d_{C_N}(z,y)≥1. The identity sequence belongs to the image, and

    d_{C_N}(z,[1])=lim_ω N(x₀^{-n_i})/r_i=1.

Thus z has distance exactly 1 from im(β), proving that this canonical isometric product embedding has proper image. This argument bounds every representative sequence directly and does not exchange an infimum with an ultralimit. It does not imply that C_N admits no different surjective product representation, and does not establish arbitrary cone product irreducibility.

## Optional verified strengthening: the full real measure space M(C)

Let C={0,1}^ℕ, and let M(C) be the real Banach space of finite signed regular Borel measures, with total variation norm. For a length-m word w, let C_w be its clopen cylinder, and put

    V_m(μ)=Σ_{|w|=m}|μ(C_w)|.

The finite partitions refine one another, so V_m is increasing, and V_m(μ)≤||μ||_{TV}. In fact V_m(μ)→||μ||_{TV}. To prove this directly, write μ=μ⁺−μ⁻ and choose disjoint compact sets K⁺,K⁻ in the positive and negative Hahn parts whose omitted total variation is less than ε. Regularity permits this choice. For all sufficiently large m, no cylinder C_w meets both compact sets. Assign f_m the value +1 on cylinders meeting K⁺, −1 on those meeting K⁻, and 0 on other cylinders. Then ||f_m||∞≤1 and

    V_m(μ) ≥ ∫ f_m dμ ≥ ||μ||_{TV}−2ε.

The second inequality follows because f_m has the correct sign on K⁺∪K⁻, while the remaining mass can change the integral by at most its total variation. This proves convergence without assuming any atomicity. Equivalently, continuous functions on C are uniformly approximated by cylinder step functions, and regular-measure duality identifies total variation with the supremum of their integrals.

Choose m_i→∞ with n_i=2^{m_i}=o(r_i), and define g_i(μ) using the complete depth-m_i scaffold and exponent ⌊r_i μ(C_w)⌋ in leaf w. For μ,η∈M(C), exactly the previous floor/caret computation gives

    V_{m_i}(μ−η)−n_i/r_i ≤ N(g_i(μ)⁻¹g_i(η))/r_i
                              ≤ V_{m_i}(μ−η)+(3n_i−1)/r_i.

The normalized distances converge ordinarily to ||μ−η||_{TV}. Taking η=0 verifies admissibility. Therefore every caret cone contains an isometric M(C), and every standard word cone contains its image with distances between ||μ−η||_{TV} and 4||μ−η||_{TV}.

The atomic map a↦Σ_{x∈C}a_x δ_x is isometric from ℓ¹(C) into M(C); the sum has countable support and converges absolutely in total variation. For any finite positive regular Borel measure ν, the map f↦fν embeds real L¹(C,ν) isometrically into M(C), since ||fν||_{TV}=∫|f|dν. In particular the fair Bernoulli probability measure supplies a nonatomic L¹ subspace.

There is no cardinality issue. A finite signed Borel measure is determined by its values on the countable cylinder algebra, so |M(C)|≤c; the Dirac measures give the reverse inequality. This strengthening concerns the real measure space; the construction as written does not encode arbitrary complex coefficients. It is an optional mathematically verified conclusion, with no assertion of historical novelty.
