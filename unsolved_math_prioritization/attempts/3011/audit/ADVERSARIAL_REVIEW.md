# Adversarial mathematical review

Review date: 2026-10-08. Reviewed `candidate/REPORT.md` and `independent/alexander_parametric_extension_audit.md`; the former was being updated during the review. This is a mathematical audit of the stated partial results, not a compact-manifold ANR resolution, novelty assessment, or independent certification of all literature-status claims.

## Verdict

**The priority proofs survive the audit.** No false step was found in the noncommutative product formula, radial-twist amplification, bounded-dimensional metric-parameter extension, Hilbert-cube/Baire obstruction, or noncompact homology-twist construction. One literal parameter-range error and one omitted subgroup-topology qualification were identified and corrected during review. The corrections were verified in REPORT.md at 16:36 UTC; neither changes the substantive conclusions.

### Corrections and qualifications

1. **Actual statement error, readily repaired:** REPORT §3 initially defines Alexander shrinking “for t>0.” It must say **0<t≤1**, with t=0 defined separately. For t>1 the formula need not give a disk self-map: take an increasing interval homeomorphism with h(1/2)=3/4; then A_2(h)(1)=3/2. The independent note already restricts the parameter correctly. All audited uses are in [0,1].
2. **Hypothesis clarification:** REPORT §4 should explicitly give H_i their subspace topologies, or at least require their inclusions into G to be continuous. The proof needs continuity of multiplication from the product of these spaces into G. The independent note already states the subspace-topology hypothesis. This is a wording omission under the usual intended interpretation, not a failure of the conditional lemma.
3. **Normalization:** REPORT initially defines D as a sum of forward and inverse distances, while the independent note defines D as their maximum. Both are valid equivalent complete metrics here, but their numerical constants must not be silently interchanged. The π/(2N) radial bound holds for each distance separately and for the maximum metric. For the sum convention the displayed upper bound becomes π/N. The updated report's wording “forward-and-inverse distances ... at most π/(2N)” is correct when referring separately to the two distances.
4. **Conditional gaps remain conditional:** Continuous finite fragmentation, its boundary-adapted version, and the ANR property of higher-dimensional disk factors are not supplied by the conditional lemma. The texts correctly identify those limitations. Likewise, the proposed alternative uniformly controlled interpolation is a sufficient condition, not a construction or an asserted necessary characterization.

## Priority proof checks

### 1. Ordered factor formula: accepted

With hk=h composed with k, α_s a homomorphism, and α_sα_t=α_st, the recursive interpolation expands to

    I_m = E_m ... E_0,
    E_j = α_{S_{j+1}}(h_j)^{-1} α_{S_j}(h_j).

For example the noncommutative m=2 expansion is

    α_{S_2}(h_2) α_{S_2}(h_1)^{-1} α_{S_1}(h_1)
    α_{S_1}(h_0)^{-1} h_0.

It agrees exactly with E_2 E_1 E_0. At the induction step, applying α_{S_1} to the normalized tail replaces every tail scale S_j/S_1 by S_j without changing factor order, after which the final E_0 is appended on the right. No unjustified commuting is used. Both expressions are continuous on the closed simplex, so the identity extends from positive tails to every face. Zero-coordinate deletion and the uniform 2(1-p_0) estimate resolve the apparent normalized-coordinate singularity.

### 2. Radial-twist amplification: accepted

The scales S_j=1-j/(2N) lie in [1/2,1]. Consequently r/S_j and r/S_{j+1}, for r=1/4 and j<N, are distinct interior points, so the stated piecewise-linear angle functions exist with sup norm at most a_N=π/(2N). Radius preservation proves both invertibility and the displacement bound, including inverse displacement.

Every E_j preserves radius. On radius r, its angle is exactly

    φ_j(r/S_j) − φ_j(r/S_{j+1}) = 2a_N.

The last factor is the identity because h_N=e. The ordered product therefore rotates r e_1 through 2Na_N=π and displaces that point by 1/2. This works in every n≥2; the extra coordinates do not change the computation. Thus the lower bound A_m≥m/π and upper bound A_m≤2m+1 are justified for m≥1. “Order-sharp” means linear growth, not equality of optimal constants.

The compact parameter-space example also checks out: each simplex has diameter at most 1/N, its distance from the added point is 1/N, the triangle inequalities hold, the resulting space is compact, and its vertex subset together with the added point is closed. The boundary data tend uniformly to e whereas the canonical interior values do not. This disproves continuity of this extension rule, not existence of some other extension.

### 3. Finite-dimensional metric-parameter extension: accepted

The distance estimates are correct. For an active coordinate, membership in B(x_i,r_i/4) gives dist(y,A)>3r_i/4 and ρ(a_i,y)<9r_i/4<3dist(y,A), hence ρ(a_i,a)<4ρ(y,a). All active source points therefore approach a uniformly. Local finiteness gives continuity off A by using one finite index set in a neighborhood and allowing zero coordinates. The uniform multiplicity bound gives the fixed constant 2m+1 at A.

The covering-dimension corollary uses the standard bounded-order refinement theorem for metrizable spaces, applied to the open subspace X\A. This is an external dimension-theory dependency, expressly identified in the note; the core lemma is independent of that corollary because it states the needed cover hypothesis. No completeness of the forward metric and no compactness or separability of the parameter space is smuggled into the construction. Locally finite does not mean globally bounded multiplicity, so the failure to extend this argument unchanged to arbitrary metrizable parameter spaces is genuine.

### 4. Hilbert cube and Baire obstruction: accepted

The cube-fiber derivative is 1−(t/2)b(x')x_1≥1/2, all boundary faces are fixed, and the center detects t. On disjoint shrinking cubes, both forward and inverse maps have tail displacement bounded by the largest tail diameter. This proves continuity at the accumulation point and uniform parameter continuity without assuming equicontinuity of an uncontrolled family. Compactness of Q then upgrades the injective continuous map to an embedding.

For any putative countable covering by finite-dimensional compact K_i, Q∩K_i is closed in Q. If it had nonempty relative interior, it would contain a closed copy of [0,1]^m for arbitrarily large m: use unrestricted coordinates in a basic product-open set. This contradicts finite covering dimension. Baire therefore applies. No common dimension bound on the K_i is needed. The result obstructs this finite-dimensional-compact exhaustion criterion, not ANR itself.

The separate stabilization/slice counterexample also works: the small tapered rotation exchanges one base coordinate with one Q-coordinate on the chosen slice and collapses an interval after projection. Shrinking its finite-coordinate support makes both it and its inverse uniformly small. Closed subgroup inclusion alone does not supply a retraction.

### 5. Escaping noncompact twists: accepted within the stated scope

The locally finite handle construction gives a connected orientable noncompact surface. Compact curves a_j,b_j of intersection one certify [a_j]≠0 in ordinary integral H_1; the local Dehn-twist calculation changes [b_j] by ±[a_j]. A sign convention selects the displayed plus sign, and either sign gives nontriviality. Thus each twist is not homotopic to the identity.

Escaping supports imply convergence to the identity in the compact-open topology. Local compactness of the surface makes a path of maps into a jointly continuous homotopy, so no twist is in the identity path component. An open path-connected identity neighborhood would contain all sufficiently late twists, a contradiction. For S×S^{n−2}, inclusion of S at a fixed sphere point is split by projection on H_1, preserving the obstruction; compact-set projection proves escaping support. The counterexamples therefore cover all n≥2. They do not address compact manifolds, the Whitney topology, or ANR status of the identity component by itself.

## Other checks and remaining dependencies

The inverse-pair closed model, one-dimensional convex extension, midpoint-collapse example, local-section-to-ANE argument, and disk/boundary topological product decomposition are consistent. The last decomposition is a homeomorphism of spaces; no direct-product group assertion is needed.

Standard retract-theory closure properties, ANR/ANE equivalence, contractible ANR implying AR, and the local-to-global theorem are external foundational dependencies. The independent note explicitly matches its Hanner reference to the separable metrizable setting; compact-manifold homeomorphism groups satisfy that category restriction. Current publication status, the exact external fragmentation theorem, and complete proofs of cited historical results remain subjects of the separate source audit, not conclusions certified by these direct calculations.

**Acceptance:** accept as rigorously delimited partial mathematical work. The parameter-range correction and topology clarification have been verified. Retain the explicit statement that no compact-manifold ANR proof or counterexample has been obtained.
