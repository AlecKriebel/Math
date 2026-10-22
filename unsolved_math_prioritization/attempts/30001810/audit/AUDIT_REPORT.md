# Independent audit of immersive simplicial volume partial results

Problem 30001810, OWR-5158-010, rank 980. Audit date: 2026-10-07 UTC.

## Verdict

**ACCEPT AFTER THE SUPPLIED LOCAL CLARIFICATIONS. PARTIAL PROGRESS ONLY.** All six numbered propositions and both numbered corollaries have valid arguments under the stated smooth closed connected oriented manifold conventions, with Proposition 2's face parametrizations made explicit. The five approaches remain unsuccessful at resolving the arbitrary-aspherical comparison. Neither a general equality proof nor an aspherical strict-inequality example has been established.

The correction is narrow. It specifies compatible standard face parametrizations in the auxiliary pseudomanifold formulation and separates mixed-factor from same-factor interior deletions in the shuffle boundary explanation. It changes no asserted norm, example, quantitative bound, or mathematical-turn count. The original Proposition 2 already required its displayed sum to represent a homology class, implicitly ruling out a noncycle; the correction removes an unjustified shortcut in its converse explanation and makes its source category unambiguous.

The entire frozen mathematical report, approach ledger, source/status record, metadata, tests, recorded output, README, and manifest were read. The original manifest hash and all eight listed file hashes/sizes match. The original test program reproduces the saved JSON byte for byte. No original file was edited. The audit includes an actual unified correction patch, its full corrected report, independent reproducible tests, acceptance metadata, and an audit manifest. No copied source document, source extraction, dataset content, or private coordination material is included in this audit's public directory.

## Scope and definition verification

Bucher's contribution defines the two quantities using ordinary real fundamental classes of closed oriented manifolds. The immersion condition includes an open neighborhood of the whole simplex. The smooth setting is explicit in the neighboring theorem; Question 4 asks for equality for aspherical targets and gives no dimension restriction. The frozen formulation faithfully fixes this setting and does not replace it with interior-only regularity, integral coefficients, locally finite chains, relative homology, or pseudomanifold targets. [Official Oberwolfach report, printed pp. 1673–1675](https://ems.press/content/serial-article-files/46346)

Throughout this audit, C_k means the free vector space of finite ordinary singular k-chains, with its ordinary singular boundary and coefficient ℓ¹ norm. Distinct parametrized singular maps are distinct basis elements. The subspace I of C_n is spanned by the immersive maps. A chain in I need not be a cycle, and an ordinary boundary in I need not bound through immersive chains. In equal dimensions, full rank means local diffeomorphism near each domain point, not global injectivity. A point has norm one; statements using positive-degree self-covers concern positive dimension.

### Existence of an admissible integral fundamental cycle

The required external foundational input is a smooth nondegenerate triangulation of the smooth manifold, not an arbitrary topological triangulation or a triangulation smooth only in open simplex interiors. For a compact smooth manifold it can be finite. Choose one global order on the vertices of its genuine simplicial complex. Parametrize each closed simplex according to that order and give every top simplex the sign comparing its parametrization with the manifold orientation. Shared faces then have the same parametrized map with opposite signed coefficients. This produces an integral singular fundamental cycle.

The simplex maps of a smooth nondegenerate triangulation are smooth up to each closed face and have injective differential at every point. A smooth extension near a closed simplex has full rank on an open neighborhood after shrinking, because full rank is an open condition. If smoothness is formulated by local extensions, these combine to a single extension: embed the target smoothly in Euclidean space, glue local extensions there with a partition of unity, and retract from a tubular neighborhood. On the simplex the extension equals the original map; derivatives on its full-dimensional closed domain agree by continuity from its interior. Shrink to the full-rank locus. Global injectivity of the extension is not needed.

This verifies the implication from the foundational triangulation theorem to exactly the admissibility convention used here. The theorem itself is an accepted external input, not a theorem proved by the finite tests. Lurie's author-hosted Lecture 3 states smooth simplexwise injective differentials, and Lecture 4 proves existence for compact smooth manifolds from that framework. [Whitehead triangulations](https://www.math.ias.edu/~lurie/937notes/937Lecture3.pdf), [existence proof](https://www.math.ias.edu/~lurie/937notes/937Lecture4.pdf)

## Proposition 1 and the rational reduction

The finite-system argument is sound, including the integral conclusion. Let t be the integral immersive fundamental cycle just described, and let z have finite immersive support S. Equality of the ordinary real classes supplies a finite ordinary (n+1)-chain w with z−t=∂w. Use the union of all n-simplex maps occurring in S, t, and ∂w as the row basis. The unknowns are the coefficients on S and on the fixed finite support of w; the coefficients of t are fixed integers. The resulting system A x=b has integer data.

Rational row reduction gives a rational particular solution and rational nullspace basis whenever the system has a real solution. Thus every real solution is approximable within the same affine solution set by rational solutions. Importantly, this approximation changes coefficients rather than singular maps, so it preserves immersion. Continuity of a finite-dimensional ℓ¹ norm supplies arbitrarily small norm error, including when coefficients approach or cross zero.

Clear denominators of both the cycle and its ordinary bounding witness. The resulting identity c−d t=∂u is an identity of integral chains, so it proves [c]=d[M] in integral homology, not merely after tensoring with the reals. No torsion shortcut is involved. Conversely, c/d is immediately a real immersive fundamental cycle. Neither a rational optimum nor attainment of the original infimum is claimed.

The independent tests include an affine family z=(1+2b,1+2b,−b), t=(1,1,0), and boundary vector (2,2,−1). Five rational choices, including the exact optimizing choice b=−1/2, are checked after denominator clearing. Genuine exact ℓ¹ optimization, rather than only inspection of these candidates, is described below.

**Disposition: accepted without change.**

## Proposition 2 and the parametrized pseudomanifold issue

The forward construction is correct. Expand a reduced integral chain into signed top-simplex occurrences. Each face occurrence has a coefficient sign, and the vanishing of the ordinary singular boundary says that the positive and negative occurrences of each exact parametrized face map have equal multiplicity. Pair those occurrences and glue through their standard face parametrizations. The induced oriented boundary signs are opposite. Maps on the paired faces are literally equal, so they descend to a continuous map on the quotient. Singular links, multiple components, and face identifications within a top-simplex occurrence cause no difficulty. The number of top occurrences is exactly the integral ℓ¹ norm.

The converse is correct for this parameter-compatible class. Each paired contribution cancels in the free ordinary singular-chain group. The top chain has norm at most N, and division by the positive integer degree gives an admissible fundamental cycle of cost at most N/d. Taking both infima proves the claimed normalized formula. The same construction works without immersion.

Orientation-reversing geometric gluing by itself is insufficient to justify this raw-chain cancellation. Here is a negative control with an aspherical target and positive topological degree. Present T² as the unit square modulo opposite sides, and use the oriented affine triangles

- A: (0,0), (1,0), (1,1)
- B: (0,0), (1,1), (0,1)

Both displayed parametrizations preserve the geometric orientation and extend immersively to the plane. Together their geometrically glued source is the torus, mapped to itself with degree one. Write h(t)=(t,0), h_rev(t)=(1−t,0), v(t)=(0,t), and d(t)=(t,t), always modulo Z². Direct singular-boundary calculation gives

    ∂A=v−d+h,       ∂B=h_rev−v+d,
    ∂(A+B)=h+h_rev ≠ 0.

The final inequality holds in the raw chain group: a path and its reverse are different singular simplices, not formal negatives. Give the upper triangle the parametrization B': (0,0), (0,1), (1,1), with coefficient −1. Now ∂B'=h−d+v and A−B' is a genuine singular fundamental cycle of norm two. This does not require a norm-increasing subdivision.

The original statement's requirement that the sum represent d[M] implicitly excludes A+B, so the example does not refute its stated infimum. It does expose why the converse cannot follow from orientation-reversing gluing alone. The supplied patch explicitly uses the standard compatible parametrizations already present in the forward construction. No quotient by reparametrizations, alternation operator, hidden subdivision, or extra norm estimate is invoked.

**Disposition: accepted with the explicit parametrization clarification.**

## Proposition 3 and finite covers

Both inequalities and all normalizations are correct. A smooth d-sheeted covering is understood to be a local diffeomorphism. Postcomposition preserves the full-neighborhood immersion condition, is a chain map, and can only reduce the coefficient norm through coincidences. If z_N represents [N], then p_*z_N/d represents [M], giving d μ(M)≤μ(N).

For the reverse direction, every singular simplex has d lifts, since the simplex is simply connected. Restricting all lifts to any standard face gives exactly all lifts of that face; uniqueness at a point proves the bijection. Hence transfer commutes with the boundary, including all face signs. If σ extends on U, compactness and convexity of Δ give ε>0 with V=Δ+B_ε contained in U. This V is open and convex. The extension lifts to V from any chosen point over a simplex point. Its differential is full rank because the covering has locally invertible differential. The lift agrees with the chosen simplex lift and is admissible at all boundary points.

Transfer has norm at most d. The identity p_*T=d id and the degree identity p_*[N]=d[M], together with one-dimensional top real homology, give T[M]=[N]. Thus μ(N)≤d μ(M). The same proof without the smooth-rank restriction gives the ordinary formula. Equality of the two volumes passes in both directions across connected finite covers.

Finiteness of μ is necessary in the self-cover deduction and was already established. For d>1, μ=d μ implies μ=0. The explicit circle self-covers on N×S¹ justify that family; products with a zero-μ factor also follow from Proposition 4. Merely taking a tower with growing degrees proves no vanishing: the normalized costs can remain a fixed positive constant. A smooth map of nonzero degree need not preserve immersion. For instance, the degree-one circle map induced by t↦t−sin(2πt)/(2π) has derivative zero at every integer; postcomposing a regular simplex through such a point loses rank.

Independent finite tests verify all lift-endpoint permutations and total signed winding for 408 pairs of cover degree 2 through 13 and nonzero winding from −17 through 17. These are controls, not a replacement for the covering-space proof.

**Disposition: Proposition 3 and Corollary 3.1 accepted without change.**

## Proposition 4 and the shuffle product

A staircase simplex has p+q successive edge increments. In the first factor these increments are e₁, e₂−e₁, …, e_p−e_(p−1), a basis with determinant one; the second factor contributes the analogous independent basis. Interleaving the bases changes only the determinant sign. Passing from successive increments to vertex-difference columns is a unipotent triangular change, so the affine map A has full rank. This is a statement about the full affine span, including its boundary, not only the interior of its image.

If the factors extend on U and V, the product map is immersive on U×V, and composition with the full-rank affine A extends on A⁻¹(U×V). This is an open neighborhood of the entire standard product simplex. No degeneracy is introduced by the staircase triangulation.

For the signed boundary identity, an interior vertex whose two adjacent steps are in different factors can be removed from either order of those steps. The two shuffle signs differ by −1 and the deletion index agrees, so those identical parametrized faces cancel. If the two adjacent steps are in the same factor, removing the vertex instead omits a vertex of that factor; these faces do not cancel internally. Endpoint deletions also belong to factor boundaries. The remaining sign is (−1)^i for a first-factor face i and (−1)^(p+j) for a second-factor face j, after its lower-dimensional shuffle sign. This yields the usual chain identity in the literal singular-chain basis.

The frozen proof's phrase about deleting an interior vertex was overbroad: it omitted the same-factor case. The patch repairs that explanation. Its displayed formula and the original test implementation were already correct.

There are exactly binomial(p+q,p) shuffles per pair of simplices, each carrying the product coefficient up to sign. Summing absolute values gives the upper norm bound even when chain terms coincide or cancel. The cross product has the product fundamental class by the local orientation normalization. Letting both input cycle norms approach their finite infima yields the claimed product inequality, including zero factors and dimension-zero point factors. It yields neither a sharp product formula nor comparison equality for arbitrary positive-volume factors.

Independent exact reconstruction uses recursive binary words and fraction-free Bareiss determinants, rather than importing the original implementation. It checks 64 dimension pairs 0≤p,q≤7 and 12,869 simplices, along with full signed boundaries. The test sees 67,212 same-factor interior deletions, making the wording distinction substantive. Flipping a shuffle sign or dropping a shuffle is correctly detected.

**Disposition: accepted with the local boundary-explanation clarification.**

## Proposition 5 and the fold obstruction

The triangle has the stated inequalities: at x=−2 the two bounds meet at y=0, and at x=1 they give y=1 and y=3. Its displayed vertex order has positive determinant six. Along the three oriented edge paths the y-velocities are 1, 2, and −3. Thus for f(x,y)=(x²,y), each edge derivative has a nonzero second coordinate everywhere, including endpoints; extending those linear edge paths to open intervals preserves this property.

For a=(1/4,3/5), the only algebraic candidate x-coordinates are −1/2 and 1/2. The negative candidate is interior and the positive candidate is outside. For b=(1/4,2), the roles are reversed. Neither point is a boundary image. The full differential determinant equals 2x, yielding degrees −1 and +1. The test also checks a point with both preimages and degree zero, a point with no preimages and degree zero, and an interior critical point.

The quotient target R²/(10Z)² is a smooth closed oriented aspherical torus. Any proposed immersive filling g with the same three parametrized faces agrees on the entire connected boundary. Since D is simply connected, lift g to G. One deck translation makes G agree with f at one boundary point, and uniqueness of lifts on the connected boundary makes it agree everywhere there. A convex neighborhood of D inside the extension domain is simply connected, so the immersion extension itself lifts. Consequently det DG is nonzero on D and has a constant sign by connectedness.

For a target outside G(∂D), preimages in D are compact and stay away from the boundary. They are isolated by the inverse function theorem, hence finite. All contribute the same orientation sign to degree. A point without preimages has degree zero. Thus every nonzero degree has the same sign. The straight-line homotopy from G to f fixes the boundary; at a and b it is an admissible degree homotopy because those points never occur on the fixed boundary image. Therefore its degrees would have to be −1 and +1, a contradiction.

This proof is complete. It does not assume the filling stays in a single torus chart; the global lift supplies the planar comparison. It does not require injectivity of an immersion, a global inverse, or the Euler-characteristic estimate. It refutes the stated boundary-fixed repair strategy, not equality for the torus. Its source torus actually has μ=ν=0 by the accepted self-cover argument.

**Disposition: accepted without change.**

## Proposition 6 and the exact comparison criterion

Let Z=I∩ker ∂ and let deg:Z→R be ordinary homology evaluation relative to [M]. For every z of nonzero degree, z/deg(z) is an admissible fundamental cycle, regardless of the sign of deg(z). Thus μ|deg(z)|≤||z||₁. The same inequality is immediate at degree zero. Since μ is finite, L(z)=μ deg(z) is a bounded linear functional on Z with norm at most one.

Real Hahn–Banach extends L to a norm-at-most-one functional E on I. Neither I nor Z must be complete or closed for the normed-space version. Every element of I∩B_n is a degree-zero element of Z, so E vanishes there. Therefore F(i+b)=E(i) is well-defined on I+B_n: any two decompositions differ by an element of I∩B_n. It is linear and kills B_n. An algebraic extension to C_n continues to kill B_n and is an ordinary n-cocycle. Its bound is retained on I only. On an immersive fundamental cycle t it evaluates to μ, so it attains the proposed dual value.

Conversely, any ordinary cocycle bounded by one on the immersive basis has absolute evaluation at most ||z||₁ on every immersive fundamental cycle z. Taking infima gives the reverse inequality. Repeating the proof with I=C_n supplies the ordinary bounded maximizing cocycle. At μ=0, the zero cocycle handles attainment; attainment of this dual supremum does not imply that a nonzero fundamental cycle attains a zero primal infimum.

For Corollary 6.1, a normalized immersive-bounded cocycle has absolute evaluation at most μ. Under equality and ν>0, scale an ordinary maximizing cocycle by a/ν, where a is the given evaluation. The factor has absolute value at most one. Equality of evaluations means equality of ordinary real cohomology classes because evaluation identifies H^n(M;R) with R. If ν=0, equality forces a=0 and the class is zero. Conversely, a bounded replacement of an immersive maximizer evaluates to μ, so ordinary duality gives μ≤ν. Together with the immediate reverse inequality, this proves the exact equivalence.

There is no circular inference that every algebraic extension is norm-controlled, that ordinary boundaries are immersive boundaries, or that asphericity supplies a bounded replacement. The report identifies precisely that missing step.

**Disposition: Proposition 6 and Corollary 6.1 accepted without change.**

## Exact optimization controls

The audit's optimization is an actual exhaustive rational linear program. For A x=b, it splits each signed variable into positive and negative parts, enumerates all supports of sizes up to the number of independent constraints, solves each candidate system exactly, and compares all feasible basic solutions. It separately enumerates dual vertices satisfying |Aᵀy|≤1 and requires exact equality of primal and dual objective values. Compactness of an objective sublevel and the standard basic-feasible-solution argument justify this finite search for the small full-row-rank systems used here. No floating point or guessed optimizer is used.

A useful negative abstract model has C_n=R⁴, boundary row (1,−1,0,0), degree row (1,0,2,3), and ordinary boundary vectors (2,2,−1,0) and (3,3,0,−1). They are independent, lie in both row kernels, and span the degree-zero cycle space. Let I be the first three coordinate directions. The genuine minima for boundary zero and degree one are

    μ_model=1/2, attained at e₃/2;
    ν_model=1/3, attained at e₄/3.

The cocycle degree/2 is bounded by one on I but takes value 3/2 on e₄. Since e₄ is a cycle, adding a coboundary cannot repair that value. This verifies why homological surjectivity plus an algebraic cocycle extension does not force an isometric comparison. It is only an abstract finite chain model, not the singular chains of a claimed manifold. In particular, it is not an aspherical counterexample. A matched model with final degree coordinate two verifies the equal-norm positive control.

On the genuine circle, the restricted library of immersive straight loops with windings 1 through K has exact optimum 1/K, by the degree constraint and its matching dual certificate. The tests optimize this for K=1,2,3,5,8,13. The unrestricted sequence tends to zero and explicitly illustrates self-cover dilution without asserting primal attainment.

The nonzero vector (2,2,−1,0) also checks the distinction between a truncated top-cycle group and its image in ordinary homology. A purported cocycle evaluating nonzero on it is rejected. Additional negative controls reject unbalanced face multisets, boundary-only differential rank loss, a wrong shuffle sign, and an omitted shuffle. Appended, truncated, and single-byte-mutated variants of every frozen file are rejected by the size/hash validator.

## Source dependence and status limits

The primary report's supporting Euler-characteristic manuscript is described there as a preprint in preparation in 2011. The author's public list and a fresh exact-phrase search did not locate a separate copy. This records the search outcome, not nonexistence or a theorem about the present literature. The announced Euler estimate and its announced locally symmetric equality cases are not dependencies of any accepted proof. [Author's publications](https://www.unige.ch/~bucherka/Publications.html)

Cerf's precise Section 5.1 theorem, printed p. 1156, was inspected in the complete publisher PDF. In the relevant category it distinguishes isomorphism below the specified dimension from surjectivity at that dimension. It does not provide the required ℓ¹ isometry. None is inferred here. [Official article](https://aif.centre-mersenne.org/articles/10.5802/aif.1652/)

The complete Löh–Moraschini–Raptis author PDF was hash-verified; its introduction and bounded-cohomology discussion are context for the Euler/simplicial-volume questions, not a proof of this comparison. [Author PDF](https://loeh.app.uni-regensburg.de/preprints/euler.pdf)

Kim–Wan's versioned arXiv record and the local v4 PDF agree on a 19-page manuscript addressing ordinary simplicial volume of nonpositively curved four-manifolds. Theorem 1.4 states a lower bound with factor 1/11. This neither identifies immersive volume nor covers arbitrary aspherical manifolds. Its proof was not independently audited and is unused here. The record gives 17 July 2026 for v4, while the PDF carries its own 20 July manuscript date; no inferred chronology is needed. [Versioned record](https://arxiv.org/abs/2506.09524v4)

The original packet's public-corpus and repository-search provenance remains attributed to the original investigation. This audit verifies those metadata files' frozen integrity but does not claim to have independently re-downloaded the large datasets or exhaustively repeated repository screening. All four accepted original PDF sizes, hashes, and page counts were independently matched. Supplemental triangulation PDFs were retrieved from the author's IAS page after the older MIT endpoint returned 404. No failed or partial retrieval was accepted as a source.

## Accepted partial results and remaining gap

Accepted after the supplied clarifications:

1. Equality of the real, rational, and normalized integral immersive infima.
2. Exact normalized parameter-compatible pseudomanifold reformulation.
3. Finite-cover multiplicativity, two-way equality inheritance, and self-cover vanishing.
4. The binomial shuffle-product upper bound and propagation of zero immersive volume.
5. An explicit torus boundary with regular edges that has no immersive face-fixed filling.
6. Attained duality and the exact ordinary bounded-cocycle replacement criterion, including zero norms.

Still missing is either a general norm-controlled conversion of almost-efficient ordinary cycles into immersive ones, or the equivalent ordinary bounded replacement of every normalized immersive-bounded top cocycle, for an arbitrary smooth closed oriented aspherical target. A cover tower, mere smoothing, mere homological representability, fixed-boundary local filling, or uncontrolled algebraic extension does not supply that step. No accepted partial result closes it.

The corrected packet must therefore remain **PARTIAL-PROGRESS**, with **five mathematical approaches and all five general-resolution attempts unresolved**. This audit makes no novelty claim and no stronger literature-openness claim. No remote write, publication, commit, push, or external helper was used.
