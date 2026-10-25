# Independent analytic review — Zenodo 22178672 v1.0.0

**Disposition: defect found; defer without repair.** The published proof of Proposition 13.1 identifies the displayed rootings as tree-child witnesses. Both displayed rootings violate the paper's own definition. This is a concrete error in a proof assertion. It is **not** a counterexample to weak tree-childness of the underlying semi-directed graphs, and it does **not** establish falsity of the main identifiability or sharpness theorem.

Review stopped on this finding under the assigned defect/defer policy. No alternative rooting was sought or constructed in response, no manuscript was repaired, and no promotion or publication was performed. Some certificate computations launched before the finding completed successfully; their scope is preserved below.

## Identity and publication binding

*Triangle Hypersurfaces and a Sharp Identifiability Boundary for Level-2 K3P Networks*, Alec Kriebel, version 1.0.0. [Zenodo record 22178672](https://zenodo.org/records/22178672).

| Published object | Pages read | SHA-256 |
|---|---:|---|
| `K3P_Level2_Identifiability_Article_v1.0.0.pdf` | All 39 | `590eee94dd352c8d4211fd485572b3c316ce5419d89c4e9c561246f8d12aae32` |
| `K3P_Level2_Identifiability_Reader_Supplement_v1.0.0.pdf` | All 15 | `0a611f7a7d14490c681a2f79b44e5929c53888ba8462a4a7d69ebeee82c2130f` |

Read the full article wrapper, all 17 current section sources, all 1,086 lines of the reader supplement, current bibliography and source-build metadata. Rebuilt both documents using the published source-date epoch and cached Tectonic. **Both rebuilt PDFs were byte-identical to the deposited PDFs**, independently binding the source analysis to all 54 published pages. `source_binding.json` records this check. Rebuilt binary PDFs were then removed, retaining source, compiler logs and hash evidence.

No archived mathematical review, historical audit opinion, or sibling review verdict was consulted before this finding. The article's own descriptions of earlier audits were read as part of the complete paper, not treated as independent evidence. Published verifier programs were inspected and several were executed as specified below.

## Exact defect: the displayed sharpness rootings are not tree-child

**Definition:** Definition 3.1, main PDF p. 5, defines a rooted presentation to be tree-child when every internal vertex has a tree vertex or leaf as a child. The roles and arc directions matter: having only reticulation children fails this condition.

**Input:** Section 13, main PDF p. 30, displays these rooted presentations, where `ab` means the directed arc a→b:

| Network | Complete displayed arc list | Printed reticulations |
|---|---|---|
| W | r→S, r→L₀, S→U, S→V, U→X, V→Z, Z→X, U→V, Z→L₁, X→L₂ | V, X |
| W′ | r→S, r→L₀, S→U, S→X₀, V→X₀, U→X₁, V→X₁, U→V, X₀→L₁, X₁→L₂ | X₀, X₁ |

**Erroneous assertion:** Proposition 13.1's proof on main PDF p. 31 says: “The displayed rooting supplies a tree-child witness”. The surrounding sentence uses that witness to justify weak but not strong tree-childness.

**Contradiction directly from the displayed data:**

- In W, `children(U)={X,V}`. Both X and V are reticulations. Their respective incoming-parent sets are `{U,Z}` and `{S,U}`. U has no tree or leaf child.
- In W′, `children(V)={X₀,X₁}`. Both X₀ and X₁ are reticulations. Their respective incoming-parent sets are `{S,V}` and `{U,V}`. V has no tree or leaf child.

Thus neither displayed rooted presentation is tree-child. This is already determined by four outgoing arcs and the specified roles; it does not depend on numerical parameters, root suppression, interval estimates, or the correctness of a graph-isomorphism package.

Source locations in `sections/13_sharpness.tex`: arc lists and roles at lines 7–10; the witness assertion at lines 44–46. `figures/sharpness_pair.tex` confirms the same mixed graphs and the suppressed root edge L₀S. The exact source hash is recorded in `displayed_rooting_defect.json`.

`check_displayed_rootings.py` is a separate standard-library control. It reads neither the paper's verifier nor any stored verdict. It copies the two published arc lists, independently derives reticulation roles from indegrees, verifies agreement with the printed roles, and checks every internal vertex against the definition. Its output identifies U and V respectively, and confirms that both printed rootings fail tree-childness. It does not enumerate or supply a replacement rooting.

**Impact and exact limit:** The sentence gives the wrong displayed witness for the positive weak-tree-child assertion. The listed rootings instead exhibit failure of tree-childness for those presentations. The proposition also cites an exhaustive census with two tree-child rootings for each mixed graph, so this local proof-text error alone does not invalidate that census or the theorem. No conclusion about the nonexistence of other tree-child rootings is warranted. The disposition is deferral of the published version, not a declaration that its central theorem is false.

## Claim and hypothesis map checked before the stop

The main relation is source-relative regular analytic containment: a source-open neighborhood of parameters of maximal rank admits a real-analytic **physical** target section. The target need not be regular or parameter-open. This is stronger than sharing one tensor and distinct from complex-variety inclusion. The main theorem equates this relation, a common full-dimensional regular physical germ, and labelled topology equivalence modulo ordinary triangle redirection.

The class is binary, standard semi-directed under one-step root suppression, strongly tree-child, level at most two, on a fixed finite labelled leaf set. Rooted graphs are acyclic, simple and binary; the root is the lowest stable ancestor. Observable character labels C,G,T are fixed. Each edge is in the principal positive Fourier domain: all three nontrivial eigenvalues in (0,1), with all three nontrivial inverse-Fourier margins positive. Inheritance probabilities are strictly between zero and one. Strict continuous time further requires c>gt, g>ct and t>cg.

The intended generic conclusion excludes a proper Zariski-closed exceptional set for each topology. It does not assert topology identifiability at every physical point, equality of complete triangle-orientation images, or identifiable numerical edge parameters. In particular, the bridge incidence gauges give continuous parameter fibers: there is no claimed finite-fiber theorem for the full numerical parameterization. Exact reconstruction uses an exact-real oracle with sign decisions and real-closed-field quantifier elimination; it is not a finite-data or efficient numerical algorithm.

The sharpness theorem is existential: for every n≥3, a pair in the weak but not strong class shares a full-dimensional strict continuous-time germ of dimension 6n−3. It does not classify all weakly tree-child networks. The outer tree–double-theta example lies outside even the weak class and is explicitly separate from this boundary statement.

## Analytic reconstruction completed

The inverse-Fourier formulas, c/g/t continuous-time inequalities, isotropic near-identity subdivision and triple-product marginal map reconstruct directly. Multiplicative edge products preserve strict stochasticity; the product Jacobian has three independent nonzero diagonal directions. Convex mixtures of effective two-boundary K3P path matrices remain in the principal domain; no unjustified assertion that such mixtures remain continuous-time is needed for the cut-transfer necessity argument.

For a true bridge, each of four conservation-character flattening blocks is positive rank one, giving pointwise rank at most four. A wrong quartet displayed-tree boundary specialization gives the determinant `p₀p₁p₂p₃(1−u²)>0`, so the indicated noncut minor is generically nonzero. The easy directed inclusion is `Cut(target)⊆Cut(source)` because a nonzero source polynomial cannot vanish on the source-open neighborhood. Reverse inclusion deliberately uses a crossing-split dichotomy and pointwise finite one-active obstructions; it does not assume target regularity or a universal pointwise noncut criterion. The 204-direction finite argument remains load-bearing and was not freshly completed before deferral.

The triangle quartic is linear in q₀CC. Its coefficient is a primitive disjoint-support binomial, and the stated specialization kills that coefficient while leaving remainder −1. This makes the Gauss-lemma irreducibility argument coherent. At the common strict point, a nonzero rank-14 minor and nonzero quartic gradient would produce physical local sections into the smooth 14-dimensional hypersurface. The conclusion is a relative germ, not an ambient-open 15-dimensional triangle image. The six-circuit tree–sunlet proof uses strict factors and excludes simultaneous vanishing through f_s²=1 or the incompatible product relation p=p² with 0<p<1. No independent symbolic expansion of every displayed identity was completed before the stop.

Positive bridge rank-one factorization yields three labelled incidence scales. The degree-at-least-three exponent block has determinant −2 per sector; the positive square-root normalizer removes the real positive ambiguity. Physical small-neighborhood splitting and the capped bridge gluing inequalities preserve strictness. The semialgebraic localization argument correctly asks for a stratum projecting with full **source-parameter** rank and then supplies an analytic physical target section; it does not replace the physical incidence correspondence with complex inclusion.

The genericity argument is structurally coherent: source rank-drop images have dimension below d after stratification; a full-dimensional physical intersection would yield the prohibited source-open containment through a local section; finitely many topologies follow from the tree-child reticulation bound; lower-dimensional semialgebraic intersections have proper algebraic closures. This depends on the global classification, whose complete machine obligations remained unfinished in this track.

The sharpness interval argument has the right implication: strict Krawczyk self-mapping plus a norm bound below one supplies an equality-slice root and uniqueness in that slice. Separate uniform rank-15 minors provide ambient-open images. This is not global parameter uniqueness. The six-dimensional cherry inverse uses observable ratios u_h/v_h and products u_hv_h, with positive square-root inversion; its determinant is nonzero and supports the stated per-cherry dimension increment.

## Completed and incomplete certificate work

All work ran in the isolated review directory; deposited sources were untouched.

| Check | Outcome and limit |
|---|---|
| Source rebuild | Both deposited PDFs reproduced byte for byte, all 54 pages |
| Compact classification binding gate | Passed all 86 bindings with `--artifact-only`; explicitly **zero fresh proof replays** |
| Exact Krawczyk replay | Passed; inspected the interval arithmetic, graph-derived Fourier construction, equality system, exact inverse, inclusion/uniqueness and rank/physicality checks before execution |
| Topology/all-n replay | Launched before the defect and completed successfully; retained output, but did not search its results for replacement witnesses or use it to repair the sentence |
| Direct 204-cut replay | Did not run to completion: compact archive omits `CUT_MINOR_SIGN_SEARCH.json`; this is an archive-scope limitation, not evidence of false mathematics |
| Full four-port replay | Initial invocation stopped because networkx was absent; networkx 3.5 was installed into isolated review dependencies, but the replay was not resumed after the defect |
| Full finite graph/probe/restoration coverage | Not freshly completed; no full classification pass is claimed |

The compact gate's binding success cannot replace semantic verification of the finite enumeration. The Krawczyk replay independently rebuilds maps from the printed primitive graphs, consumes rational center/pivot/box data rather than final Booleans, recomputes interval Jacobians and both local rank minors, and checks all strict edge/inheritance margins. Its generated evidence and exact provenance are summarized and hash-bound in `replay_results.json`; source archives remain the canonical reproducible inputs.

## Primary-source checks completed

[Holtgrefe et al., *Characterizing semi-directed phylogenetic networks and their multi-rootable variants*](https://link.springer.com/article/10.1007/s12064-025-00453-8), Theorem 5 and its proof, confirm the no-omnian characterization in their convention. Their definitions distinguish an existing tree-child rooting from all rootings being tree-child. The paper under review explicitly fixes its narrower binary one-step convention; the detected witness failure is visible within that convention itself.

[Brits et al., version 3](https://arxiv.org/html/2607.12919v3), §2.3, Example 2.4 and Lemma 4.2, support the displayed-tree Fourier formula and earlier tree–sunlet separation. Their cleanup convention is exhaustive, whereas this paper explicitly uses one-step suppression. The principal strict domain used here sits inside the positive stochastic setting relevant to that comparison. Their level-one conclusion does not establish this paper's level-two classification.

[Gross–Krone–Martin](https://link.springer.com/article/10.1007/s11538-024-01314-z), discussion and deficiency table, already identify the special K3P three-sunlet deficiency. Accordingly rank 14 alone should not be advertised as wholly new; the paper correctly distinguishes its explicit hypersurface/common physical germ and global level-two theorem.

The [author-maintained Englander et al. listing](https://www.nielsholtgrefe.nl/publications/) confirms the earlier triangle-free, strongly tree-child, level-two **JC** scope. The full bioRxiv page was unavailable through the browsing tool, so no claim of fully checking its proof is made. Direct fetches of Coste's primary semialgebraic notes also failed; exact Bochnak–Coste–Roy proposition-number verification remained unfinished when the defect stopped review. No exhaustive novelty or priority verdict was reached.

## Strongest verified result and exact remaining gap

The strongest decisive result of this review is the independently checkable contradiction between the two printed arc lists and the claimed displayed tree-child witnesses, bound to byte-identical published PDFs. Useful positive evidence includes the exact rational sharpness replay and the reconstructed analytic interfaces described above.

The unresolved validation scope is the complete global finite classification: semantic replay of all cut, bounded-atlas, restoration and probe obligations, plus remaining imported-source checks. No final analytic approval of Theorems 2.1–2.5 is issued. The observed defect does not prove these theorems false. Under the requested workflow the published version is deferred, the finding is recorded, and no repair or replacement witness is supplied.
