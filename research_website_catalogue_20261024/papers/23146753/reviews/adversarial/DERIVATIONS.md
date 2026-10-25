# Independent adversarial derivations — record 23146753

These are fresh checks of the deposited argument, not changes to it. The complete initial reconstruction was sealed before foreign bodies or current family opinions. No historical audit conclusion is used as an axiom. Finite diagnostics below do not prove the universal theorem.

## 1. Exact target and necessary distinctions

For every finite simple graph G=(V,E), let F₂(G) consist of normalized nonnegative binary mass functions which satisfy every MTP₂ inequality and have finite nonnegative unary and original-edge factors. Let A(G) be the strictly positive exponential family with arbitrary real fields h_i and nonnegative pair couplings J_ij on precisely E (zero couplings permitted). The literal assertion is F₂(G)=closure A(G) in the entire finite probability simplex. There is no positive-support restriction, bound on parameters, hidden vertex, added edge, chordality assumption, or fixed graph size. The resulting finite-factor assertion does not assert that every globally Markov MTP₂ law factors: the credited four-cycle example excludes that stronger statement.

For n=0 both sides contain the single mass 1. For an edgeless graph and n>0 the unary-factor model consists of all product Bernoulli laws, including deterministic coordinates. That differs from the source's literal edge-only empty product. The source convention is handled in section 5 below.

## 2. Original-edge geometry, contraction, and attractive approximation

Let S={x:p(x)>0}. If x,y∈S, MTP₂ forces x∧y,x∨y∈S. Thus finite meet and join give a unique bottom and top in S. The support is nonempty because p is a probability.

The local support identity is exact, not the generally false inference from arbitrary Markov conditions. If a unary cell or edge cell occurs in S, the corresponding supplied factor entry is strictly positive: a finite nonnegative product producing positive p cannot have a zero entry. If x meets every actual unary and original-edge projection of S, every factor in the product at x is therefore positive. Hence x∈S. The opposite inclusion is immediate. The proof uses finiteness and nonnegativity; signed factors can first be replaced by absolute values because |∏f|=∏|f|=p.

Delete pinned coordinates. The bottom and top now have every active coordinate respectively 0 and 1, so each active-edge projection contains 00 and 11. The only possibilities are the full square, square without 10, square without 01, and {00,11}. They impose respectively no constraint, i⇒j, j⇒i, or both implications. Pinned-edge constraints add no active restriction beyond the already recorded unary and active-edge conditions: every active bit occurs with the fixed pinned bit. Consequently the support is exactly the satisfying assignments of the unary pins and these original-edge implications.

Transitive implications form a preorder. Mutually implying active coordinates have identical values on S; its strongly connected classes are the equality classes. Each class is connected using original edges because a strongly connected directed graph is connected after forgetting orientation, and every directed arc is an original edge. After contraction the quotient relation is antisymmetric. Its valid assignments are exactly the upsets, with neither extra nor missing states. In particular, no new cross-class edge is needed to describe the hard constraints.

On every locally observed cell take the logarithm of its strictly positive factor entry; assign any finite real value on unobserved cells. A two-bit function has a unique multilinear polynomial c+a x_i+b x_j+d x_i x_j. Substituting pinned values and equalities produces a finite quadratic polynomial on quotient variables. If K⇒L, then y_K y_L=y_K on S, so the coefficient of that pair is moved to a unary term; if both endpoints are in K it is also unary. Coefficients on distinct incomparable classes aggregate across all original edges connecting the two classes. No term of degree greater than two appears, and no coefficient between incomparable classes without an original cross edge appears.

For incomparable K,L, let U be the union of their strict successor sets. U is an upset and contains neither K nor L: otherwise comparability would follow. The four upsets U, U∪{K}, U∪{L}, U∪{K,L} are allowed support states. In the mixed log difference

    log p(U)+log p(U∪{K,L})−log p(U∪{K})−log p(U∪{L}),

the constant, unary, and every other quadratic term cancel. What remains is exactly the aggregate B_KL, which is nonnegative by the actual global MTP₂ inequality. This argument applies to aggregate coefficients; requiring each supplied potential to be attractive would be false at zeros.

Place each quotient unary on one representative coordinate, and each B_KL≥0 on one original edge connecting K and L. The resulting finite quadratic L(x) has only nonnegative pair coefficients and agrees with log p−c on S. Let D(x) be the sum of unary pin violations and original directed-edge implication violations x_i(1−x_j); equality uses both directions. D is a nonnegative integer, D=0 exactly on S, and D≥1 outside S. Every −t x_i(1−x_j) contributes the nonnegative coupling +t x_i x_j and a unary −t x_i. Pin penalties are unary. Therefore exp(L−tD), normalized, belongs to A(G) for every finite t≥0 on the unchanged graph.

On S its unnormalized mass is e^(−c)p; its total there is a=e^(−c)>0. Write R_t=∑_{x∉S}exp(L(x)−tD(x)). Then R_t→0 by a finite sum. More explicitly, R_t≤|Ω\S|exp(max_{x∉S}L(x))e^(−t) when the complement is nonempty. The full L¹ error is exactly 2R_t/(a+R_t), because probabilities on S are uniformly rescaled downward and off-support mass is R_t/(a+R_t). Thus convergence is a proof for every fixed finite graph and every allowed p, not an inference from sampled parameters. The bound is body/representation dependent; no uniform parameter rate is claimed by the note. All-pinned and empty-support-complement cases satisfy the same reasoning. Empty V is separate and immediate.

## 3. Residual normalization: real capacities and exact signs

Let E(x)=−∑h_i x_i−∑J_ij x_i x_j. Choose an orientation i→j of each original edge and rewrite −J_ij x_i x_j=J_ij x_i(1−x_j)−J_ij x_i. Let b_i be the collected unary coefficients. The arc i→j has capacity J_ij, i→t has b_i when b_i≥0, and s→i has −b_i otherwise. For U={s}∪{i:x_i=1}, the terminal contribution for b_i<0 is −b_i(1−x_i)=b_i x_i−b_i. Hence

    C(U)=E(x)+κ,  κ=∑_{b_i<0}(−b_i).

Capacities are finite nonnegative reals, not integers. The feasible directed-flow set 0≤f≤c, with conservation at nonterminals, is compact and nonempty, so its continuous value attains a maximum. This does not claim finite termination of arbitrary augmenting paths with irrational data. A maximum flow has no positive-residual s–t path, since any such finite path could be augmented by its minimum positive residual. The residual-reachable set then defines a cut with zero residual capacity, proving max-flow/min-cut directly for finite real capacities.

Take nonnegative directed flow variables, include c_uv=0 for absent arcs, and set r_uv=c_uv−f_uv+f_vu. The capacity inequality gives r_uv≥0. For any cut U, conservation gives

    ∑_{u∈U,v∉U}(f_uv−f_vu)=value(f).

Consequently ∑cut r=C(U)−value(f). At a maximum flow this equals C(U)−min C=E(x)−min E. The reverse-flow term has a plus sign. Omitting it or using a minus sign is not a harmless choice of convention. The target's displayed formula and sign are correct.

Residual internal arcs occur only along original undirected edges. Group their contributions as r_ij x_i(1−x_j)+r_ji x_j(1−x_i). Terminal contributions r_si(1−x_i)+r_it x_i are unary. Arcs i→s and t→i never cross a valid source–sink cut and contribute zero. There is no s→t arc in this construction, nor can reversing an existing arc create one; no extra constant is silently omitted. Exponentiating the negative nonnegative local contributions yields local entries in (0,1], product

    W(x)=exp(−E(x)+min E),  max W=1,
    1≤Z=∑W≤2^n.

This normalizer lower bound is the essential protection against every bounded factor tending to zero. Finite-dimensional compactness gives a subsequence of the full list of factor entries converging in [0,1]. Products and their finite sum converge, while Z_*≥1. Since the original probability sequence already converges to p, this subsequence has the same p=W_*/Z_*. Absorb Z_*^(−1) into any unary factor for nonempty V. Every resulting entry is finite and nonnegative; every pair factor is on an original edge. The MTP₂ inequalities pass to p by continuity. This establishes the reverse inclusion for the entire graph, independent of support changes and diverging original fields/couplings.

## 4. Critical overextensions actually falsified

The own driver uses bit i for manuscript coordinate i+1, and exact fractions throughout.

* Tied repulsive supplied potential: take original edges 12,34,13,24, hard equalities x₁=x₂ and x₃=x₄, and supplied weights 2^(−2x₁x₃)2^(3x₂x₄). On the support the aggregate exponent is +x₁x₃, so the law has masses (1,1,1,2)/5 and is MTP₂. Replacing each equality zero by ε=1/16 gives a strictly positive finite product whose mixed ratio at 1000,0010 is 1/4, so it is not MTP₂. The manuscript does not use that shortcut. Redistributing the +1 aggregate onto edge13 and penalizing the two equalities gives attractive laws with exact L¹ errors 10/9,18/25,66/289,1026/66049 for ε=2^(−k), k=1,2,4,8.
* Wrong residual sign: 520 of the 900 independent rational networks have an internal reverse residual and reject the wrong c−f−f_reverse cut formula. All 13,176 correct cut identities pass. This makes the sign test discriminating.
* Compact factors with collapsing normalizer: a unary factor (2^(−k),2^(−k)) has all entries bounded by one, produces the uniform binary law, and has normalizer tending to zero. Its limiting product is identically zero. The actual max-weight-one residual gauge supplies the missing lower bound.
* Without attraction, finite-factor closure can fail even on a triangle: weights ε² on 000,111 and 1 on the other six states are positive pair-factorizable (proportional to exp(β·cut_size), ε=e^(−β)). Their limit is uniform on the six nonconstant states. Every unary and pair projection is full, so no finite nonnegative unary/pair product can have that support. It is not MTP₂: the positive pair 100,010 has unsupported meet000. This does not contradict the note's MTP₂-restricted theorem.
* The old four-cycle law is globally Markov and MTP₂ but violates the balanced edge quartic. The independently checked products are 1/6561 and2/6561; it cannot be used as a member of F₂ or of its toric closure. The note credits its earlier authors and keeps it outside the closure theorem.

## 5. Literal Lauritzen convention and zero conditional probabilities

The actual 2022 primary page3125 defines M_I by an edge-only product of finite real functions; the probability product is not given a separate scalar. Absolute values preserve any nonnegative mass vector exactly. If E≠∅, every isolated coordinate is absent from every factor, so for fixed nonisolated state all isolate assignments have the same mass. Thus the isolate vector is jointly uniform, independent of the remaining variables, and the nonisolated marginal is itself an edge product after multiplying one edge factor by 2^(number of isolates). This property is closed under limits. The main theorem applies to that nonisolated graph; absorb each resulting unary into a selected incident edge (every such vertex has one), and absorb the uniform-isolate scalar into any edge. This proves exactly the source intersection's closedness.

If E=∅ and V≠∅, the literal empty product is 1 at every configuration and is not a probability; M_I is empty. Under a tacit normalizing scalar it instead contains only the uniform law. Both families are closed. V=∅ has the unique mass1. None of these cases licenses arbitrary nonuniform isolated marginals in the literal edge-only model.

For a general finite nonnegative factorization and a separator assignment c with p(c)>0, fixed-separator factors are positive and every remaining connected component has a positive finite normalizer. Summing all irrelevant components therefore leaves a normalized product on the A and B sides. This proves global Markov, including disconnected graphs and zero cells. For p(c)=0, all nonnegative joint cells over c vanish and every conditional-independence polynomial is 0=0. Hence no division by a zero event is needed. There are finitely many relevant CI polynomials, so global Markov is closed.

## 6. Separate prior-framework lifting check

The published supplement makes an attributed deduction beyond the literal natural-support KS theorem. It is not needed by the main density/residual proof. I checked it as another possible failure route.

In the edge-design toric closure, GMS faciality supplies a finite original-edge energy H≥0 with zero set exactly the nonempty support S. For any Boolean sublattice, pins and all-pair implications describe S: the meet of all support states with a given active coordinate1 lies in S; taking joins of these minimal states and the bottom reconstructs any assignment satisfying the implications. Equality classes therefore yield a poset even without assuming edge feasibility in advance.

To show an equality class C is connected in the original graph, choose two valid order ideals differing precisely in C. If C splits into D,F with no original edge across the split, fixing the common exterior makes H(D1,F0)+H(D0,F1)=H(00)+H(11)=0. Nonnegativity forces both split states into S, contradicting equality. Similarly, for a quotient cover C<D, the common exterior downarrow D minus {C,D} gives allowed patterns00,10,11 and forbidden01. In the absence of any original cross edge, additivity would force H(01)=H(00)+H(11)−H(10)=0, a contradiction. Therefore each cover uses an original edge. Pinned nonisolates are enforced by an incident edge; an isolated coordinate cannot be pinned or tied by an energy independent of it. Each assignment meeting every original-edge projection then respects all pins, all equalities, and all quotient covers, hence belongs to S. This proves original-edge feasibility and allows the stated GMS finite-factor conclusion.

The no-edge case is separate because the pure edge-design matrix has zero columns; the primary toric statements are not applied to that degenerate design. This lifting is a deduction using the prior framework, not an earlier verbatim theorem and not a new-method certificate. It confirms that citing only KS's natural-support theorem without these steps would leave a gap; the deposited supplement supplies the steps and they are valid.
