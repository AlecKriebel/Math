# Kourovka 21.145: independent metric-invariant route

Author metadata: Alec Kriebel, ORCID <https://orcid.org/0009-0001-9320-500X>.

Started 2026-10-17 20:49:13 UTC. Scope: standard finitely generated Thompson group F, with a finite-generator word metric, compared separately with F × Z and F × F. All research here is independent; no outreach or Git operations were performed by this route.

## Exact target and success criteria

For each Y in {Z,F}, decide whether there are constants L ≥ 1 and A,R ≥ 0 and a map q:F × Y → F such that

    L⁻¹(d_F(f,f′)+d_Y(y,y′)) − A
      ≤ d_F(q(f,y),q(f′,y′))
      ≤ L(d_F(f,f′)+d_Y(y,y′)) + A,

and every point of F is within R of the image. Either a proof of these inequalities and the last, global coverage condition, or a genuine quasi-isometry invariant with provably different values, would resolve the relevant clause. Embeddings, algebraic non-isomorphism, and noncommensurability do not meet this criterion.

**Current outcome:** neither clause is resolved here. There are independently checked elementary deductions below, including a uniform copy of M(Cantor), and hence of nonseparable ℓ¹(Cantor), in every asymptotic cone. No novelty or priority claim is made for those deductions. They remove several attractive but ineffective invariant approaches; they do not construct a surjective product decomposition.

## 1. Why a large class of metric invariants cannot distinguish these spaces

The existing undistorted support embeddings give quasi-isometric embeddings

    F ↪ F × Z ↪ F,
    F ↪ F × F ↪ F.

The forward arrows can be factor inclusions; the reverse arrows are the established product embeddings. Prior credit: [Burillo, *Quasi-Isometrically Embedded Subgroups of Thompson's Group F*](https://doi.org/10.1006/jabr.1998.7618), and [Cleary–Taback, *Geometric quasi-isometric embeddings into Thompson's group F*](https://nyjm.albany.edu/j/2003/9-11.html). These results explicitly concern embeddings.

**Poset lemma.** If I is an invariant valued in a partially ordered set and X quasi-isometrically embedding in Y implies I(X) ≤ I(Y), then mutual quasi-isometric embeddings force I(X)=I(Y). For growth functions, take the partial order on their usual coarse-equivalence classes. The proof is antisymmetry.

Consequences include asymptotic dimension and other embedding-monotone dimension bounds; non-equivariant coarse-compression spectra into a fixed target class; and separator/Poincaré profiles whenever their standard monotonicity under regular maps applies. A quasi-isometric embedding between bounded-degree Cayley graphs is a regular map: the upper bound is Lipschitz on edges and the lower bound uniformly bounds inverse-image multiplicities. There is no prospect of distinguishing these three groups by computing different values of such an invariant. One must verify monotonicity for the particular proposed invariant rather than assume it.

For the profile statement, a precise primary reference is [Hume–Mackay–Tessera, *Poincaré profiles of groups and spaces*, Theorem 1](https://people.maths.bris.ac.uk/~jm13806/pdf/Poincare-sep.pdf): every Lᵖ-Poincaré profile, 1≤p≤∞, is monotone under regular maps between bounded-degree graphs. The separation profile is the p=1 case up to the established equivalence. Thus their equality here is unconditional, even though their exact common values may be unknown.

This argument **does not** apply automatically to higher filling functions, uniformly finite homology as a graded object, or arbitrary coarse cohomology: embeddings need not induce the required inequalities or isomorphisms. In particular, an undistorted subgroup need not be a coarse retract.

## 2. A stronger cone deduction: a nonseparable ℓ¹ space occurs uniformly

This is a derivation from binary tree pairs with all quantifiers made explicit. It strengthens the weak observation that the cones have unbounded finite-dimensional rank. Its relevance here is negative: a finite-rank obstruction cannot work, even with a distortion bound uniform in the rank.

Let N(g) be the number of carets in either tree of the reduced tree pair for g, with N(1)=0, and set

    d_N(g,h)=N(g⁻¹h).

### Lemma 2.1: d_N is a metric quasi-isometric to a word metric

Symmetry and positive definiteness are immediate from reduced pairs. To multiply pairs for g and h, refine the middle trees to their smallest common binary refinement U. A binary tree is specified by its finite, prefix-closed set of internal vertices, and U is obtained by taking the union of those sets. Thus

    N(U) ≤ N(g)+N(h).

Expand the other two trees in the corresponding positions. Each expanded outer tree has N(U) carets. Reducing the resulting pair cannot increase the count, so N(gh) ≤ N(g)+N(h), proving the triangle inequality.

The comparison with a word metric is standard; see [Burillo–Cleary–Stein, Theorem 3](https://arxiv.org/pdf/math/9809185). The sharper bound used here is [Cleary–Taback, *Combinatorial properties of Thompson's group F*, Theorem 3.1](https://arxiv.org/pdf/math/0208117): for the standard generators and nonidentity g,

    N(g)−2 ≤ |g| ≤ 4N(g)−4.

The globally safe bounds N(g)−2 ≤ |g| ≤ 4N(g) suffice below, including the identity.

### Lemma 2.2: uniform blocksum estimate

Let T have n leaves, and let B_T:Fⁿ → F act by the j-th given element on the dyadic interval represented by the j-th leaf. Graft reduced pairs for f₁,…,f_n onto the common scaffold T. Then

    Σ_j N(f_j) ≤ N(B_T(f₁,…,f_n)) ≤ Σ_j N(f_j)+(n−1).        (1)

The unreduced count is exactly the upper bound. No reduction can remove a caret internal to a grafted nontrivial reduced pair: before the first such reduction, only scaffold carets have been removed, so the two children in the proposed internal reduction would already form a reducible pair within the original block. This contradicts its reducedness. Hence only scaffold carets reduce, proving the lower bound. Identity blocks have no internal carets and cause no difficulty.

Because B_T is a homomorphism, the same estimate applies to pairwise distances, replacing f_j by f_j⁻¹h_j. This uniformity in n matters; separate embeddings with uncontrolled constants would not suffice.

For the standard x₀ one has

    N(x₀^k)=|k|+1 for k≠0,    N(1)=0.

One can read this directly from the two comb trees. Therefore

    Σ_j|k_j| ≤ N(B_T(x₀^{k₁},…,x₀^{k_n}))
                 ≤ Σ_j|k_j|+2n−1.                       (2)

### Theorem 2.3: every cone contains ℓ¹ of continuum density

Let I={0,1}^N, let ω be any nonprincipal ultrafilter, and let r_i→∞ be any scaling sequence. The basepoints may be arbitrary. Then:

1. Cone_ω(F,d_N,r_i) contains an isometric copy of ℓ¹(I).
2. For the standard word metric, Cone_ω(F,d_word,r_i) contains an embedding E with

       ||a−b||₁ ≤ d(E(a),E(b)) ≤ 4||a−b||₁.              (3)

For another finite generating set there is again a uniform bilipschitz bound depending only on that generating set. The statement holds for every ω and every scaling sequence; no uniqueness of the cones is asserted.

**Proof.** Choose m_i→∞ such that n_i=2^{m_i}=o(r_i), for example m_i=floor((log₂ r_i)/2) after discarding finitely many indices. Let T_i be the full depth-m_i binary tree. For a∈ℓ¹(I) and w∈{0,1}^{m_i}, put

    A_w(a)=Σ_{x∈I: x begins with w} a_x,
    k_w(i,a)=floor(r_i A_w(a)),
    g_i(a)=B_{T_i}((x₀^{k_w(i,a)})_w).

The sums are well-defined: an ℓ¹ family has countable support and is absolutely summable. The norm bound from (2), together with n_i/r_i→0, shows that g_i(a) is an admissible cone sequence.

Write c=a−b. Aggregation over a finite-prefix partition is contractive:

    V_m(c):=Σ_{w∈{0,1}^m}|Σ_{x begins w}c_x| ≤ ||c||₁.

Moreover V_m(c)→||c||₁. Given ε>0, choose a finite set J⊂I with Σ_{x∉J}|c_x|<ε. For all sufficiently large m, the distinct points of J have distinct length-m prefixes. Consequently V_m(c)≥Σ_{x∈J}|c_x|−ε>||c||₁−2ε.

For each w, the difference between k_w(i,a)−k_w(i,b) and r_i(A_w(a)−A_w(b)) has absolute value <1. Combining this with (2) gives

    V_{m_i}(c)−n_i/r_i
       ≤ N(g_i(a)⁻¹g_i(b))/r_i
       ≤ V_{m_i}(c)+(3n_i−1)/r_i.

Both outer terms tend, in the ordinary sense, to ||c||₁. Thus a↦[g_i(a)] is isometric in the caret cone. The word/caret estimates imply (3) after rescaling, since their additive errors vanish. For arbitrary basepoints o_i, replace g_i(a) by o_i g_i(a). ∎

The space ℓ¹(I) has density continuum, and ℓ¹(I) × ℓ¹(I) is isometric to ℓ¹(I) with the ℓ¹ product norm. Thus the theorem supplies no difference between a cone and a product of cones. In particular, **it is not a proof that any cone of F itself is a product**, nor that any displayed subspace is coarsely dense or cone-surjective.

### Measure-space strengthening

The same construction embeds the larger Banach space M(I) of all finite signed regular Borel measures on Cantor space I, with the total-variation norm. Replace A_w(a) by μ(C_w), where C_w is the cylinder with prefix w. Finite-partition variation is contractive, and

    Σ_{|w|=m}|μ(C_w)| → ||μ||TV.

For completeness, every continuous function on Cantor space is uniformly approximated by functions constant on sufficiently long cylinders. The identity

    ||μ||TV=sup{|∫f dμ| : f continuous, ||f||∞≤1}

for finite signed regular measures therefore gives the displayed convergence. The same floor-error estimate then gives an isometric embedding of M(I) in every caret cone and the bounds (3) in every standard word cone. Atomic measures recover ℓ¹(I); absolutely continuous measures give nonatomic L¹ subspaces. Cardinality remains continuum, since a measure is determined by its values on the countable cylinder algebra.

This stronger formulation also does not obstruct splitting: decomposing Cantor space into its two clopen halves gives M(I)≅M(I)⊕₁M(I) isometrically. The proof is recorded as a consequence without a novelty claim.

### The canonical self-product embedding has a genuinely proper cone image

For the two-leaf scaffold, (1) induces an **isometric embedding**

    C ×₁ C ↪ C,    C=Cone_ω(F,d_N,r_i),

for the same ω and scales, since the additive scaffold error 1 disappears. Its image is the cone of H=Stab_F(1/2), the usual support product F×F. This particular embedding is not onto.

To see the gap quantitatively, choose the x₀ orientation that contracts [0,1/2] by 1/2 and put

    λ(g)=log₂(g⁻¹(1/2)/(1/2)).

This is 1-Lipschitz for d_N. Indeed every slope of u is between 2^{-N(u)} and 2^{N(u)}, because the depths of leaves in a tree with N(u) carets are at most N(u). Since u fixes 0, the same bounds hold for u(t)/t and for u⁻¹(t)/t. If h=gu, then h⁻¹(1/2)=u⁻¹(g⁻¹(1/2)), proving |λ(g)−λ(h)|≤N(u). The function vanishes on H, whereas λ(x₀^{-n})=−n. Consequently

    n ≤ d_N(x₀^{-n},H) ≤ n+1.

Taking n_i=floor(r_i) gives a point of C at distance exactly 1 from the canonical product image. Thus even after taking cones the familiar product embedding retains a macroscopic coverage failure. This does not rule out a different, nonlinear surjective bilipschitz product map.

### Exact finite verification

[verify_caret_metric.py](verify_caret_metric.py) uses complete binary prefix codes and exact integer combinatorics. [exact_checks.json](exact_checks.json) records a successful run:

- 125 distinct reduced elements represented through four carets;
- 15,625 triangle-inequality checks;
- 41 exact power-count checks;
- 3,405 power-block checks over every scaffold through four leaves;
- 289 two-block checks using general reduced factors through three carets.

These checks support the finite combinatorics. They do not replace the proof of the infinite-dimensional ultralimit statement. A separate adversarial proof audit is in [validation_l1_cone.md](validation_l1_cone.md).

## 3. Product geometry forces a uniform coarse line flow

This gives a concrete necessary condition for clause (a), and rules out a broad elementary form of candidate construction. It does not rule out all candidate quasi-isometries.

Suppose q:X × Z→X is an (L,A)-quasi-isometry, and p is a quasi-inverse with

    d(qp(x),x)≤D,    d(pq(u),u)≤D.

Let T_n(x,k)=(x,k+n) and set τ_n=q T_n p. Then all τ_n are quasi-isometries with constants independent of n, and

    L⁻¹|n|−A−D ≤ d(τ_n(x),x) ≤ L|n|+A+D             (4)

for every x and n. Also

    sup_x d(τ_mτ_n(x),τ_{m+n}(x)) ≤ LD+A.           (5)

The first statement follows by composing fixed quasi-isometries with the isometry T_n; (4) compares τ_n(x) with qp(x), and (5) uses the bound on pq−id between the two translations. Product fibers also give a family of uniformly embedded copies of X and uniformly controlled coarse retractions onto each copy. Their union is uniformly coarsely dense.

The quantifiers “independent of n” and “for every x” are essential. A translation-like action with a bounded step size, or a single undistorted cyclic subgroup, is much weaker.

### Lemma 3.1: finite center rules out uniformly group-like right flows

Let G be finitely generated with finite center. There cannot be a family satisfying (4), with |n|→∞, that is uniformly within a single constant E of right multiplications R_{g_n}:x↦xg_n.

Indeed the R_{g_n} would be quasi-isometries with constants K,C independent of n. Applying their upper bound to the pair (1,s), for each generator s, gives

    |g_n⁻¹ s g_n| ≤ K+C.

Only finitely many tuples of conjugated generators occur. Such a tuple determines the inner automorphism; two elements inducing the same tuple differ by a central element. Thus {g_n} is finite, as the center is finite. The right translations have bounded displacement, contrary to the lower bound in (4).

Thompson F has trivial center, so this applies. It does **not** make the center a quasi-isometry invariant. It says that any hypothetical product quasi-isometry must induce a nonlinear coarse flow that cannot be uniformly approximated in this way.

Left translations do not rescue this particular construction. Every nontrivial element of F has infinitely many conjugates: choose a dyadic interval J with J∩g(J)=∅ and conjugate g by distinct elements supported in J; their restrictions to J are distinct. Therefore sup_x d(gx,x)=∞ for g≠1, while (4) requires finite displacement for every fixed n.

## 4. Other invariant families investigated and their exact gaps

| Family/mechanism | Verified evidence | Status and exact gap |
|---|---|---|
| Divergence; cone cut points | [Golan–Sapir](https://arxiv.org/abs/1709.08144) prove linear divergence for F. Both direct products have linear divergence as products of two unbounded finitely generated groups. | Rejected as a distinguishing invariant. No cut points is far weaker than product irreducibility. |
| Cone simple connectivity | F has [quadratic Dehn function, Guba](https://arxiv.org/abs/math/0211395); [Papasoglu](https://doi.org/10.4310/jdg/1214459409) gives simple connectivity of the cones of a group with a quadratic isoperimetric inequality. Products retain quadratic Dehn function. | Rejected: all three have simply connected cones. Their topology beyond these basic facts is not computed here. |
| Finite asymptotic/cone rank | Support embeddings give every finite rank, and §2 gives uniform ℓ¹(I). | Rejected. Infinite dimension does not give cancellation of a product factor. |
| Coarse/free-coefficient cohomology | [Brown–Geoghegan](https://pi.math.cornell.edu/~kbrown/scan/1984.0077.pdf) prove H*(F;ZF)=0. Tensoring finite-rank free resolutions gives the same vanishing for F×Z and F×F; in each total degree only finitely many bidegrees occur. | Rejected for this untwisted group-ring invariant. This does not settle every possible coarse cohomology theory or coefficient system. |
| Ordinary cohomology, abelianization, center, simple commutator | They distinguish the groups algebraically. | Rejected as unproved QI invariants. A finite-index or QI-rigidity theorem would be needed and is absent. |
| Uniformly finite H₀ / amenability | F, F×Z, and F×F are amenable simultaneously; product and subgroup closure prove both directions. | Rejected regardless of the current amenability status of F. Higher uniformly finite groups were not computed; no product/Künneth conclusion is assumed. |
| Higher homological/homotopical filling | [Weis, 5 October 2026](https://arxiv.org/abs/2610.06276), Theorem B, gives polynomial integral homological filling functions in every degree k≥2 for the Higman–Thompson families, and hence polynomial higher homotopical upper bounds. Sharp Euclidean exponents are not obtained there. | Potentially viable but blocked here: sharp comparable values for F and its products are needed. Polynomiality alone cannot distinguish them. Do not use an unknown coarse retraction to infer filling monotonicity. |
| Coarse product rigidity / irreducible cones | The [AIM Thompson problem list](https://aimath.org/WWN/thompsonsgroup/thompsonproblist.pdf), Q4.11, explicitly asks for failure of a cone product decomposition. | Blocked: asserting cone irreducibility transfers the target difficulty into an unsupported claim. No verified splitting or nonsplitting is obtained. |
| Quasi-retractions onto support products | The [2018 Oberwolfach report](https://ems.press/content/serial-article-files/46748), Question 100, asks whether F×F is a quasi-retract of F; no resolution was located in this route's bounded search. | Blocked: treating the standard support embedding as retract would assume an unsupported claim already formulated as a separate problem. |
| Scaling/measure-scaling groups | [Genevois–Tessera](https://arxiv.org/abs/2105.04883) distinguish measure-scaling quasi-isometries from arbitrary quasi-isometries. | Rejected in its naive form: an arbitrary QI need not be measure-scaling, so no scaling-group obstruction follows without an extra theorem. |

The tensor-resolution claim in the cohomology row can be checked directly: F admits a free resolution of Z with finite rank in every degree. Hom into Z[F×H] of the product resolution identifies degreewise with the total tensor product of the two free-coefficient cochain complexes, for H=F or Z. The F factor is acyclic by Brown–Geoghegan. As complexes of free abelian groups in nonnegative degrees, the Künneth computation has zero cohomology. No infinite sum over a fixed total degree is present.

For future work, a route should be reopened only after finding a new computable feature of cone products, genuinely sharp higher fillings, or a mechanism for controlling an arbitrary uniform coarse flow. Repackaging any one of those as an assumption is not progress.

## 5. Current literature caveats and prior credit

[Golan, 17 August 2026](https://arxiv.org/abs/2608.17193) proves that every subgroup of F isomorphic to F is undistorted. It does not prove that such an image is coarsely dense. This substantially strengthens what is known about homomorphic embeddings while leaving the requested quasi-isometries open.

Bounded current-status searches found no primary solution to either clause. Official-status verification is handled independently by the parent research effort; this note does not infer absence of a solution from search silence.

A third-party search result pointed to a September 2026 public claim about nonamenability of F. It was forwarded for primary-source audit and is not relied on here. In particular, this note deliberately makes no current assertion that amenability remains open or that the new claim is correct. Either amenability outcome gives the same answer for both products, so this uncertainty has no effect on the invariant elimination above.

The finite product embeddings, caret/word comparability, linear divergence, quadratic Dehn function, and free-coefficient vanishing are prior results. The proofs in §§2–3 are independently derived consequences, not claimed new contributions. A bounded search for this precise ℓ¹(Cantor) formulation did not locate it, which is not a priority determination.

## Research log and checkpoints

- **2026-10-17 20:49:13 UTC:** began the metric-invariant route, preserving independence from the constructive and priority routes. Defined QI quantifiers and coverage requirement. Best-guess completion toward resolving both clauses: **3%**.
- **2026-10-17 20:52:14 UTC:** found fresh August and October 2026 primary papers; identified embedding-monotone invariants as automatically equal; rejected a proposed coarse-retraction shortcut because it transfers the difficulty to Question 100. Best-guess completion toward resolving both clauses: **5%**; completion of this route's obstruction census: **55%**.
- **2026-10-17 20:53:30 UTC:** proved the uniform scaffold estimates and the ℓ¹(Cantor) cone construction; separate adversarial verifier found no flaw in these arguments. Exact finite checks passed. The uniform coarse-flow restriction is also derived; a second proof audit is pending. Best-guess completion toward resolving both clauses: **6%**; completion of this route's audit: **85%**.
- **2026-10-17 20:55:27 UTC:** adversarial audit completed for both the ℓ¹ construction and the coarse-shift lemma. Corrected a bibliographic DOI before delivery and sharpened the word-cone embedding bound to distortion at most 4 from the primary theorem. Added a quantitative proof that the canonical product embedding has proper cone image. Best-guess completion toward resolving both clauses: **6%**; completion of this route's audit: **95%**.
- **2026-10-17 20:56:26 UTC:** the proper-image cone proof passed adversarial review. Strengthened the Banach subspace from ℓ¹(Cantor) to the whole space M(Cantor) of finite signed regular measures; the verifier independently checked the total-variation convergence and cardinality. All local required artifacts are complete. Best-guess completion toward resolving both clauses: **6%**; completion of this bounded metric-invariant investigation: **100%**. The target QI decisions remain unresolved, and route completion is not discovery completion.

The percentages estimate research completion, not a probability that either answer is yes. The remaining gap is the actual QI decision for each clause; none of the rejected invariant routes closes it.
