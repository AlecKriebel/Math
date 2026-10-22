# Five-approach research log

Target: 10300062 / AMR-102-0062, Calegari Question 14.2. Date: 2026-10-04 UTC.

All work was single-worker research. No remote write or external contact was performed. The five families below are different proposed mechanisms, not a count of tool calls. Their numbering organizes the final packet, rather than manufacturing five separate chat responses. The source queue began at 0/5. The parent campaign should record its five-approach accounting consistently with its actual response ledger.

## Readiness checkpoint (18:31–18:39 UTC)

- Live queue lookup found rank 670, status queued, 0/5.
- Read the repository and queue AGENTS instructions, queue README, exact source question and following remarks, and the complete upstream target report.
- The problem website failed through web retrieval and returned HTTP 403 through direct read-only retrieval. Used the stated private corpus fallback, matched in bytes and SHA-256 to the public repository manifest.
- arXiv source PDF was downloaded, text-extracted, and printed page 31 was visually inspected. No hyperbolic hypothesis appears in Question 14.2; formal image convergence is not defined there.
- Repository numeric/code/title searches and target attempt-path read found no actual prior target attempt. Exact normalized-statement scan found only this target; the related-target-group file has no occurrence of its ID/code. Search is bounded and cannot prove the absence of hidden or unindexed work.
- The upstream report mentions Kahn–Markovic and unspecified virtual-fibering/veering results. Kahn–Markovic's primary Theorems 1.1–1.2 were inspected. They prove existence of certain closed essential surfaces in closed hyperbolic 3-manifolds, not coherent completion of an arbitrary prescribed leaf patch.
- Completion estimate at source identification: 10% toward an exact resolution. This is a planning estimate, not a calibrated probability.

## Approach A: central extensions and a suspension counterexample

**Mechanism.** Force all available closed essential surface groups to be virtually abelian, while placing an injective free-group patch inside every leaf.

**Work.** Construct the suspension of Gamma_3 -> Gamma_2 -> Diff^+(S^1), killing one handle and retaining a genus-2 Fuchsian action. Its oriented circle-bundle Euler number is -2. Prove from the central extension and a covering-space H_2 argument that no closed genus>=2 surface group embeds in its fundamental group. Produce a punctured-torus patch in every leaf by trivial holonomy over the collapsed handle. The compact-domain group lemma then gives a complete obstruction to coherent approximation. Nonorientable approximants are handled by their orientable double covers.

**Adversarial check.** Found a finite-cover control in the product 3-torus: images of growing balls can equal a compact leaf exactly, although no coherent approximate section exists. Consequently the free-group obstruction does not automatically apply to image convergence as worded in the source.

**Result.** Theorem 4 is complete for its explicitly stated strengthened/marked interpretation. Exact-source resolution remains blocked by the convergence bridge. This construction is not hyperbolic and makes no claim about a hyperbolic-only version.

**Completion estimate.** During discovery: 75% toward an unrestricted negative result; after the image-convergence countercontrol: 35% toward an exact source resolution, 100% toward the stated coherent-obstruction theorem. No source resolution promoted.

## Approach B: Diophantine approximation of linear foliations

**Mechanism.** Approximate an irrational plane normal by integer normals; the rational planes quotient to incompressible tori.

**Work.** For v=(1,sqrt(2),sqrt(3)), prove all lattice vectors in the approximating planes escape every bounded set. Select expanding radii simultaneously below half their systoles and small relative to inverse angular error. Prove pointed C^1 convergence of the controlled disks. Implement exact integer floor computations using integer square roots and bounded lattice-exclusion checks as controls.

**Result.** Complete affirmative special case in Section 6. The finite controls do not establish the asymptotic statement; the rational-independence proof does. The route relies on linear structure and supplies no local closing theorem for arbitrary foliations with holonomy.

**Exact gap.** Replacing rational slope approximation by a global closed pi_1-injective surface construction without altering prescribed leaf topology.

## Approach C: doubling, followed by compression or finite-cover closing

**Mechanism.** Double a large compact leaf subsurface and remove compressions; alternatively pass to finite covers before closing it.

**Work.** Compute the folded double of a punctured torus. The explicit word a_+ a_-^(-1) is in the kernel but has nonzero homology in the genus-2 double. This independently checks why the easy geometric doubling is not an essential surface. Finite-cover passage cannot fix this by creating higher-genus surface subgroups in the circle-bundle example: every finite-cover group is still a subgroup of the obstructed group. Mere subgroup separability or existence of an unrelated surface group does not supply a closed surface containing the prescribed marked patch group.

**Result.** A concrete kernel certificate and a precise failure of the proposed repair. No compression sequence was proved to preserve the expanding leaf patch.

**Exact gap.** A relative incompressible completion theorem, which is false under coherent interpretation for the constructed example and unproved for the weaker source interpretation.

## Approach D: invariant measures and rational branched-surface weights

**Mechanism.** Solve integral branch matching equations to close approximating sheets.

**Work.** Prove the elementary rational-nullspace approximation statement for a positive real solution of integer branch equations. Then test its starting hypothesis in the suspension. A transverse invariant measure would induce a probability on the circle invariant under a non-elementary Fuchsian action. Hyperbolic elements with disjoint fixed sets give an elementary contradiction. Thus tautness does not provide this measure.

**Result.** Section 7.3 identifies an actual failed hypothesis rather than treating numerical branch weights as a foliation theorem. Integral weights alone would not verify pi_1-injectivity either.

**Exact gap.** A relative branch-closing construction that accommodates nonmeasured holonomy and proves incompressibility; neither step follows from solving a finite homogeneous system.

## Approach E: closed positive forms and current/area obstructions

**Mechanism.** Use a closed 2-form positive on the foliation to obstruct globally tangent approximations.

**Work.** Prove the good-area/bad-area inequality Area(bad)>=(c/C)Area(good) for null-homologous surfaces. Keep its orientation and null-homology hypotheses explicit. Test the inference to pointed approximation: a closing cap outside the controlled ball can have arbitrarily large area, so the inequality is compatible with arbitrarily large good balls.

**Result.** A rigorous global restriction that does not settle the local pointed target. The source's stronger global-angle discussion is not silently substituted for its question.

**Exact gap.** No bound connects area or placement of the uncontrolled closing part to the radius of the prescribed approximating ball.

## Freeze disposition

Five substantive approach families completed. Strongest authored result: the coherent-approximation obstruction, with an explicit exact countercontrol against extending it to bare image convergence. A positive linear-torus case, a folded-double kernel, a transverse-measure obstruction, and an area estimate are also fully written.

**Recommended status: unresolved with scoped partial results, not solved.** No original-question candidate is promoted for publication as a resolution. A fresh independent audit must assess the proofs and especially the convergence distinction before any external publication. Priority remains unestablished. No more proof-search turns are requested by this packet.
