# Exact prior implication and attempted repair

Audit of frozen PR #672, problem 6700060, head `13d9b2d944ce8ec121381a4bc21e48d2bb19846e`. This is an independent dependency/priority audit, not a replacement for the separate analytic audit. The source theorem is treated as a mathematical theorem after the prior proof gates; its lack of verified journal acceptance neither supplies novelty nor by itself refutes it.

## 1. The precise assertions

Let C be the category actually claimed by the native README: compact full-dimensional convex Euclidean reference polytope P, a Euclidean domain P', and a face-preserving bijection F:P→P' whose map and inverse extend smoothly locally to the ambient n-manifolds with nonsingular derivatives through every stratum. The competitor has nonnegative outward-normal face mean curvature, interior ridge angles θ'≤θ(P) everywhere, and at least one strict angle inequality at one point of one closed ridge. No distance contraction, face isometry, volume, or length comparison occurs.

Gromov's 2017 Question 64 on printed p.60 asks whether convex extremality implies mean-convex extremality. The exact definition immediately preceding it has the pointwise weak angle comparisons and an existential strict comparison just specified. The source does not explicitly spell out every convention for diffeomorphisms there. Gromov's earlier 2013 manuscript, §1 printed pp.2–3, models corner structures by ambient extensions and uses the ambient tangent bundle. That supports category C. It does not prove that every conceivable weaker reading of the 2017 wording is category C. The native README already preserves this limit.

Bi's v1 (6 August 2026) fixes a compact full-dimensional convex polytope P represented by its irredundant affine facet inequalities u_a≤0, normalizes their Euclidean gradients N_a, and assumes a smooth positive-definite metric g on a neighborhood of P. For n≥3, Theorem 1.1 assumes R_g≥0, H^g_a≥0, and exterior angles α^g_ab≥α_ab on each codimension-two face. In addition to flatness and totally geodesic facets it explicitly concludes

    <ν_a,ν_b>_g = <N_a,N_b> on F_a∩F_b

for every distinct pair with nonempty intersection. This last conclusion is an actual part of the earlier theorem, not an equality the present PR must newly obtain from flatness. The theorem applies to arbitrary such P, with no simplicity, acute-angle, upper-dimensional, or additional spin hypothesis in the statement.

## 2. Every bridge, including the neighborhood condition

1. **Reference object.** P in category C is exactly a reference object in Bi's setup. The finitely many facet inequalities may be chosen irredundant and their nonzero gradients normalized; this does not alter P, its face lattice, or any angle.

2. **Positive pullback.** Define g=F*e on P. For each nonzero v, g(v,v)=|dF(v)|²>0 by nonsingularity. In coordinates its matrix is JᵀJ. Its restriction to the interior is an ordinary smooth Euclidean pullback metric.

3. **Smooth extension.** At each point of P choose a local smooth ambient extension of F. Its derivative is nonsingular at that point and on a smaller open neighborhood, so its Euclidean pullback is a local positive-definite metric. A finite cover exists by compactness. On overlaps along P these tensors agree with the same g. Their full jets along P agree as well: the restrictions agree on the full-dimensional interior, all derivatives there agree, and continuity gives equality of their derivatives at its boundary. A smooth partition of unity on a neighborhood of P produces a positive-definite tensor because positive-definite matrices form a convex cone. The resulting tensor has precisely the pullback jets along P. There is no curvature hypothesis outside P in Bi's theorem. Thus partitioning the extensions does not introduce an omitted curvature condition or change the geometry needed on P. This is the usual extension/gluing argument for a smooth metric on a compact domain.

4. **Scalar curvature.** On P° the map F is a local isometry from g to e, so R_g=0. Since the extension is smooth, scalar curvature is continuous through ∂P; density of P° gives R_g=0 on P. No positive scalar curvature assertion is made.

5. **Outward side and face curvature.** F maps the interior side of each labeled facet to the interior side of the corresponding facet. The derivative maps outward unit normals to outward unit normals. This statement does not require F to preserve ambient orientation. Pullback functoriality of the Levi-Civita connection gives equality of the second fundamental forms under F, and hence H^g_a=H^{e}_{a'}∘F. Therefore H^g_a≥0. If nonnegative curvature is initially formulated only on the facet relative interior, smoothness and continuity give it at its lower-dimensional boundary as well.

6. **Angles and sign.** At x on a ridge and y=F(x), dF is a linear isometry between the tangent inner-product spaces, sending both oriented face normals to their counterparts. With outward normals, θ=π−α, so θ'(y)≤θ(P) is precisely α^g(x)≥α(P). Equivalently the normal inner product for g is at most its reference value, since cosine decreases on [0,π]. A strict interior inequality becomes a strict exterior inequality at the same corresponding point. No requirement that every point or every ridge have a strict inequality is added.

7. **Quantifiers.** Face preservation bijects each closed ridge and all of its strata with its counterpart. Thus “all ridges, every point” transfers to exactly the source hypothesis. The strictly smaller point has one inverse image. Source equality at all nonempty facet intersections includes this point and contradicts strictness there. Even a theorem stated first on relative interiors would extend this equality to a closed ridge by continuity, but Bi's theorem already states the stronger closed-intersection conclusion.

8. **Nonsimple corners.** Bi uses arbitrary irredundant facet descriptions. For a nonsimple vertex more than n facets may be incident; this does not make J noninvertible or require those facet normals to be independent. The same invertible J acts on all of them. A pair of facets meeting only in higher codimension receives no new angle hypothesis in the application; the source nevertheless concludes its normal-product equality. No resolution of an extra corner obstruction remains in the PR's implication.

9. **Dimension.** The theorem already includes every n≥3. Its proof explicitly treats even n by P×[−1,1] with g+dt². Thus the PR's even-dimensional statement is not a new extension. In n=2 the separate standard total-turning argument below applies. In n=1 there is no ridge carrying the required strict angle, so the specified nonexistence is vacuous.

Applying Theorem 1.1 now proves every relevant angle equal. The assumption that P was convex-extremal is unused: the same specialization proves mean-convex extremality for every P within category C. That apparent strengthening is inherited from the source's arbitrary-P quantifier; it is not a new stronger theorem supplied by the PR.

## 3. The classical planar addition

A planar competitor is a disk with piecewise smooth Jordan boundary by the face-preserving diffeomorphism. Traverse its boundary with the disk to the left. With the convention that a circle has positive curvature, total turning gives

    Σ_i (π−θ'_i) + ∫ k ds = 2π.

For the convex reference polygon Σ_i(π−θ_i)=2π. Set d_i=θ_i−θ'_i≥0 and K=∫k ds≥0. Subtracting gives Σ_i d_i+K=0. Every term is nonnegative; every d_i is zero. One strictly positive d_i is already impossible. The statement follows directly from the classical turning theorem/Gauss–Bonnet, without any new extremality or rigidity argument. The native proof is correct and useful for complete dimension bookkeeping, but does not supply an unresolved planar mechanism.

## 4. Challenge the implication in both directions

**Forward direction.** The nine bridges above show that every prohibited C-competitor produces a metric satisfying every source assumption and violating its explicitly stated equality conclusion. There is no remaining scalar curvature, regularity, corner, dimension, or “strict only somewhere” mismatch. The cited theorem is strictly stronger in its geometric input and in its additional conclusions.

**Reverse direction.** A solution of Question 64 for Euclidean competitors does not by itself prove Bi's theorem for arbitrary smooth R_g≥0 metrics: such a metric is not assumed flat or globally realizable as the Euclidean pullback of an embedded domain, and proving flatness is a substantial conclusion of Bi. Nor does the PR prove every combinatorial equivalence of nonsimple polytopes can be represented by the ambient-smooth diffeomorphism required here. These reversals are unnecessary for the prior implication and must not be asserted. This audit establishes a sufficient earlier theorem, not equivalence of the two problems or resolution of every regularity interpretation.

**Strictness at exceptional points.** The source equality is pointwise, not merely almost everywhere or integrated. A single strict vertex point on a closed ridge cannot escape it. The proof's limiting spinor relation is extended to closed facets before recovering angle equality; the earlier theorem itself has already done this work.

## 5. Was an unacknowledged substantial proof step added?

Reading the complete Bi manuscript establishes the following mechanism concordance with the native proof-verification note. This is more specific than saying that a paper has a similar title:

| Native section | Earlier mechanism in Bi v1 | What the PR adds |
| --- | --- | --- |
| A, normal-cone distance and noncancellation | Lemmas 2.1–2.2, pp.2–4 | Explanation of the same estimates |
| B, ridge interpolation and angle ratio | Lemmas 2.3–2.5, pp.5–9 | Verification and endpoint clarification |
| C, radial degree, hemisphere, logarithmic cutoff | Lemmas 2.6–2.9, pp.10–11 | Review of the same construction |
| D, sliced logarithmic trace term | Lemma 3.4 and its proof, pp.14–16 | Expanded explanation of the source estimate |
| E, boundary energy and index input | Propositions 3.1 and 3.5, pp.12–13,16 | Verification against the cited foundation |
| E, normalized nonzero limit and closed-facet boundary relation | Proposition 3.6, pp.16–17 | Explicit elementary L¹ bookkeeping |
| E, invertibility, corner Gram equality, parity | Proof of Theorem 1.1, pp.17–18 | Review and omission of unneeded stronger conclusions |

The extra L¹ estimate makes the source's normalization passage transparent: strong L² convergence gives strong L¹ convergence of the squared norms, while the shrinking boundary layer has vanishing integral. It is not a repair of a false inference identified in the source, and does not add an assumption or new conclusion. Similarly, the metric-neighborhood extension makes a routine differential-geometric application explicit. No native passage identifies a source gap requiring a novel repair. Finite code controls reproduce conventions and packaging; they are not a substitute independent proof of the PDE/index theorem. The native README and application note already candidly say that no new discovery or theorem is claimed.

## 6. Reasonable repair routes and exact gaps

| Route | Mechanism and evidence | Status and exact remaining gap |
| --- | --- | --- |
| Correctly credited smooth-category corollary | The exact pullback implication above; every source assumption matches | Mathematically valid, fully covered by the earlier theorem; no new central solution survives |
| More explicit smooth extension or planar proof | Standard partition of unity and turning identity | Complete expository clarification; cannot create mathematical priority for the original claim |
| More thorough independent audit of Bi | Check the existing smoothing, trace, index, limit, and equality proof | Valuable validation record; does not move the theorem's author or priority; no repaired source defect has been found |
| Exploit that the reference is convex-extremal | Use a hypothesis not needed by Bi | Restricting an earlier theorem yields a weaker corollary; no new outcome |
| Include non-acute or nonsimple P | Would need an extension if the source excluded them | Source already permits them; no additional theorem here |
| Broaden to singular-corner or facewise/interior maps | Would require a way around degenerate pullback metrics, or a new nonsmooth rigidity theorem | Unverified and explicitly excluded. F(x,y)=(x³,y) demonstrates how an interior diffeomorphism may have degenerate boundary pullback; this is a failure of the method, not a counterexample to the desired extension. Simply declaring an extension transfers the central problem to an unsupported stronger claim; route blocked pending a materially new mechanism |
| Obtain a genuinely independent Euclidean proof without Bi | Could conceivably be new if a new rigidity mechanism were proved | No such argument is present. Removing the citation while retaining its hard analytic mechanism is not a repair |
| Publish an exposition or source-verification note | Preserve attribution and label the purpose accurately | A possible different artifact, but not a newly solved-open-problem research note and not a repair of its priority claim |

No reasonable local repair preserving the present central research claim was found. This does not assert that further research on corner regularity is impossible. It says the current result is already implied in precisely its own asserted category, and the only prospective extension identified is both out of scope and unsupported.

## 7. Checkable evidence and limits

The independently written controls test exact normal pushforwards and all pair Gram products under two rational nonorthogonal linear maps (one orientation reversing), including a square-pyramid nonsimple vertex; the interior/exterior sign; degeneration of an excluded corner map; and finite exact nonnegative planar defect patterns. All 89 pass under ordinary and optimized Python with identical output. They are useful convention falsifiers, not a numerical or formal proof of the source theorem.

The strongest verified conclusion is therefore: **the present ambient-smooth result is a mathematically valid direct application of Bi v1 Theorem 1.1 plus the classical planar turning theorem; the packet contains no verified new central resolution.** This is an exact prior-implication finding, not a sweeping claim about every version of Gromov's question, exhaustive prior literature, community consensus, or source journal acceptance.

Primary sources independently retrieved and hash-bound in SOURCE_RETRIEVAL.json: [Gromov 2017](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf), [Bi v1](https://arxiv.org/abs/2608.06320v1), and [Gromov 2013](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/Plateauhedra_modified_apr23.pdf). Complete original question/theorem/convention pages were visually inspected. All 18 pages of Bi were read as extracted text to identify the proof mechanisms; this audit does not claim a fresh full PDE/index validation independent of the previously accepted analytic family.
