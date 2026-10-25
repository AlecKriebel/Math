# Independent adversarial review — Zenodo 22178672, v1.0.0

**Disposition: DEFER — a concrete error in the published proof witness is confirmed. No repair or publication action was taken.**

This review covers *Triangle Hypersurfaces and a Sharp Identifiability Boundary for Level-2 K3P Networks*, all 39 article pages and all 15 reader-supplement pages. It is bound to the published article SHA-256 `590eee94dd352c8d4211fd485572b3c316ce5419d89c4e9c561246f8d12aae32` and reader-supplement SHA-256 `0a611f7a7d14490c681a2f79b44e5929c53888ba8462a4a7d69ebeee82c2130f`. These match both the original local PDFs initially read and the fresh Zenodo copies subsequently acquired.

The review read the full manuscript before evaluating supplied verification outputs. Its independently written polynomial and rooting controls import no project verification module or stored conclusions. After those controls and a fresh Krawczyk replay had completed, the coordinator relayed another reviewer's specific concern about the displayed sharpness rootings. I checked that concern directly against the published definitions, edge lists, PDF images, and TeX. The final conclusion is therefore independent confirmation of that particular defect, not a claim that this reviewer first discovered it. No other review report or verdict was read.

## 1. Confirmed defect and its exact scope

Definition 3.1, article p.5, says that a rooted presentation is tree-child when **each internal vertex has a tree vertex or leaf as a child**. Section 13, article p.30, gives the following rooted presentations:

- `W: rS, rL0, SU, SV, UX, VZ, ZX, UV, ZL1, XL2`, with reticulations `{V,X}`.
- `Wprime: rS, rL0, SU, SX0, VX0, UX1, VX1, UV, X0L1, X1L2`, with reticulations `{X0,X1}`.

In the displayed rooting of `W`, the children of `U` are precisely `X` and `V`. Both are reticulations. In the displayed rooting of `Wprime`, the children of `V` are precisely `X0` and `X1`. Again both are reticulations. Thus **neither displayed rooting is tree-child** under the article's own definition.

Nevertheless, the proof of Proposition 13.1 on p.31 states: “The displayed rooting supplies a tree-child witness”. That assertion is false for both printed presentations. This is visible in the actual PDF and present verbatim in the fresh source archive, `sections/13_sharpness.tex`, lines 44–45; the edge lists are at lines 7–10. PDF page images were inspected to exclude text-extraction confusion.

This finding invalidates the *stated displayed witness*. It does **not**, by itself, invalidate the broader assertion that the underlying mixed graphs are weakly but not strongly tree-child. Indeed, independently written controls completed before the concern was relayed reproduce all admissible-rooting censuses:

| Mixed graph | Admissible | Tree-child | Non-tree-child |
|---|---:|---:|---:|
| W | 5 | 2 | 3 |
| Wprime | 7 | 2 | 5 |

Those pre-existing controls are retained, but no new replacement-rooting search or manuscript repair was undertaken after the defect was confirmed. No substitute witness is proposed here. The user-directed defect policy requires deferral rather than a silent correction.

The exact outstanding publication requirement is to reconcile the published proof's witness statement with its actual graphs and certified rooting evidence in a separately authorized correction, and then reassess the corrected version. The current version has not passed this gate.

## 2. Claims and hypotheses reviewed

The headline result is not unrestricted phylogenetic identifiability. Its stated class consists of binary, standard semi-directed, strongly tree-child networks of level at most two, on a fixed labeled leaf set. It fixes one-step root suppression, retains reticulation arrowheads, uses a uniform root distribution, and uses independent parent selections at reticulations.

The principal edge domain requires positive nontrivial Fourier multipliers less than one and all three strict inverse-Fourier inequalities. It is narrower than all stochastic K3P matrices. The continuous-time domain additionally requires `c>gt`, `g>ct`, and `t>cg`. Inheritance probabilities must be strictly between zero and one. Observable nonzero character labels are fixed.

Directed containment is source-relative and includes a physical real-analytic target section; the target need not be regular. That distinction is retained in the cut-transfer and semialgebraic arguments. The claimed topology result is generic outside a proper algebraic exceptional set, and the reconstruction claim assumes exact-real field, sign, and quantifier-elimination operations. It does not promise finite-sample consistency, conditioning, an efficient practical algorithm, or identification of all edge parameters.

The ordinary triangle assertion is a shared smooth, relative rank-14 germ in the 15-dimensional normalized Fourier chart, not equality of complete stochastic images and not an ambient-open triangle model. The weak-class sharpness assertion is an existence result for examples outside the strong class, not a classification of every weakly tree-child network.

## 3. Written argument assessment completed before deferral

### Physical model, roots, and cuts

The printed strict-subdivision inequalities are correct: choosing an isotropic factor near the identity leaves the compensating residual in the stated open domain. Coordinatewise products preserve the principal domain through convolution; the continuous-time factorization follows either from positive rate splitting or the explicit ratio inequalities. The distinction between these two domains matters when remote blobs are replaced by mixtures: convexity preserves the principal domain, while the reverse-cut proof only needs that broader domain for target positivity.

The true-cut rank bound follows from the four character sectors and their positive rank-one blocks. The boundary displayed-tree argument supplies a generic noncut witness, while continuity moves inheritance parameters into the strict interior. That argument is not a pointwise converse for all K3P networks, and the manuscript explicitly does not assert one.

The reverse cut-transfer proof requires a stronger, finite pointwise obstruction for 204 one-active directions, plus the handwritten balanced-word reduction and crossing-hull argument. The universal conclusion cannot be inferred from generic rank alone because the physical target section might lie in a singular or special locus. I checked that the printed proof respects this issue. However, the 204-direction replay did not complete from the compact archive: it requires discovery inputs in the full archive. This is an explicitly limited reproduction result, not an algebraic failure. No unconditional endorsement of the global cut theorem is made by this review.

The cycle/theta primitive case split, the two pole possibilities, and the role of compulsory path-sink children were read in full. The external quarnet source supports the two underlying semi-directed generator types; it does not by itself prove the finer incoming-port grammar or the statistical K3P classification. Those remain obligations of the paper's written reduction and exact enumeration.

### Triangle geometry

The six displayed cubic pullback factorizations were independently expanded exactly. Each has eight terms; all six vanish identically on the tree map. The printed strict-domain argument is valid: if a paired first factor is nonzero, simultaneous vanishing forces a nontrivial multiplier to have square one; if all three first factors vanish, their product gives `p=p^2` with `0<p<1`. This proves pointwise tree–sunlet separation in the stated positive domain.

The eight-term H14 quartic was independently substituted into all six permutations of the printed triangle map, and all pullbacks vanish exactly. At the stated symmetric strict-CT point, independent rational linear algebra gives rank 14. The printed 14-by-14 determinant is exactly `-1/760840571584512`; the normalized quartic gradient has exactly six nonzero entries, with absolute value `1/6912`. Every port permutation has the same rank and symmetric image point.

The irreducibility argument is mathematically sound as written: the coefficient of `q0CC` is a primitive binomial with disjoint monomial supports; the supplied specialization makes that coefficient zero while the remainder is nonzero, ruling out its divisibility into the remainder. Gauss's lemma then gives irreducibility of the normalized quartic. The rank and gradient facts yield local physical analytic sections onto a shared relative hypersurface germ. They do not yield equality of full stochastic images.

### Bridge gauges, localization, genericity, and reconstruction

The positive component-tensor fiber argument is based on rank-one factorizations on a tree, with nonzero character sectors kept separate. Positive anchor normalizers eliminate the relevant incidence scales; positivity excludes sign ambiguities. The paper treats equality of component tensors separately from equality of their physical parameter realizations. The capped bridge construction has the stated strict CT margin: with `epsilon <= L^2/(8U)`, `epsilon/U - epsilon^2/L^2 >= 7epsilon/(8U)`. Hence the gluing argument does leave an open neighborhood when the preceding component claims hold.

Marginal submersion through visible edge-signature product classes requires that every retained role and switching distinction actually be recorded. The finite-target-type argument uses semialgebraic projection and analytic constant-rank strata to obtain a local physical section; it does not incorrectly assume target regularity. The genericity argument correctly considers the full rank-drop locus, not just one chosen minor's vanishing set. A compatible finite stratification bounds the image of that locus by `dN-1`, and a full-dimensional physical intersection would produce the directed containment forbidden by the classification.

These analytic implications are plausible and correctly scoped conditional on the finite local classification and the intended triangle relation. They are not independently certified merely because a JSON dependency declaration lists them. The final quantifier-elimination step supplies a termination statement only under the exact-input convention.

### Finite classification and a separate unresolved scope concern

I inspected the literal descriptor compiler and the four-port verifier's graph grammar, polynomial/rank classification flow, and exact vector-field upper-rank mechanism. The upper-rank argument `dim E(ker A) = rank([A;E])-rank(A)` is a genuine symbolic mechanism; a sampled Jacobian rank alone would not be an upper bound. The full verifier was started but stopped after the concrete proof defect was confirmed. It had reconstructed thousands of map keys; it had not returned its final classification verdict. The full restoration forest, non-four anchor census, probe ledgers, and all finite mutation suites were not freshly replayed in this review.

Before stopping, I also recorded an unresolved consistency issue that should be checked in a later authorized correction/review. Definition 3.5 describes matching reduced trees of blobs and isomorphism of nontriangle complete factors. Lemma 5.3 expressly permits reconnecting triangle terminals inside a theta factor. The finite `mixed_relation` routine searches every three-clique in the mixed graph and masks the internal triangle arrowheads; it does not restrict this search to a three-cycle blob. Consequently, the code's accepted relation appears broader than a literal reading of “nontriangle complete factors ... isomorphic”. This may be intended terminology, but the review did not settle the interpretation before deferral.

A diagnostic construction and modular controls are retained in `triangle_context_control.py/.json/.log`: two four-leaf theta graphs with an internal triangle redirection are each strongly tree-child in the exhaustive rooting control (7/7 and 9/9 admissible rootings tree-child). Their full-map modular Jacobians have rank at least 26 at sampled points, and the chosen symmetric triangle points agree modulo 1000003. These modular observations are **not** presented as a real physical counterexample or a proof of the generic classification. They identify an explicit case on which the definition and computational relation can be compared later. No repair was attempted, and this secondary concern is not needed for the DEFER verdict.

### Sharpness and outer obstruction

Before the witness error was raised, I independently reconstructed the W/Wprime root-suppressed graphs, enumerated every admissible rooting with degree, acyclicity, reachability, and common-dominator/lowest-stable-ancestor checks, and tested tree-childness. The counts above match the article. Every one of the 120 internal-vertex bijections fails to give an underlying leaf-labeled graph isomorphism. Thus triangle redirection cannot relate the base pair, since it preserves the underlying graph.

The archived independent Krawczyk implementation was freshly executed in an isolated copy of the checksum-bound compact package. It reconstructs the displayed graph maps, exact rational equality system, center-Jacobian inverse, interval Jacobian, inclusion, physical inequalities, and full-rank bounds. It completed and recreated the published 9.9 MB certificate **byte-for-byte**, SHA-256 `8187174b3e0c0b3a0a55fa32595c211811c357dc223ada7a74b3033f7cae3941`. This is substantially stronger than testing a floating-point approximate coincidence.

The interval logic is sound: the preconditioned fixed-point map sends the convex box into itself, and its derivative norm is strictly below one. Existence follows from the fixed-point argument and uniqueness is only in the selected 15-variable equality slice. The two local maps have rank 15 throughout that box; the strict CT inequalities are enclosed separately. Consequently, this completed check supports a real, strict-CT common ambient-open three-leaf germ.

The printed cherry observables give `Rh=uh/vh`, `Ph=uh*vh` with a positive inverse. Independent exact arithmetic reproduces the stated determinant `176/25` at the sample parameters. The all-n dimension increase of six is consistent with recovering the old tensor after dividing by the two pendant spectra. The written topology-persistence argument was read, but the full archived all-n replay was not freshly run here. Section 14's separate outer-class collision was read; its complete imported tangent/collision computation was not freshly reproduced before stopping.

## 4. Reproduction record and limits

Completed artifacts:

- `fresh_controls.py`, `.json`, `.log`: independently written exact sparse-polynomial identities, triangle ranks/determinant/gradient, 200 rational strict-principal separator samples (including 512 non-CT edge triples), an inheritance-boundary negative control, exhaustive base-pair rootings, labeled nonisomorphism, and cherry determinant. Samples are explicitly supplementary to proof.
- `archived_krawczyk.log` and `archived_krawczyk_summary.json`: completed fresh archived rational interval replay, with exact output certificate hash.
- `archived_compact_binding.json/.log`: integrity-only check of 86 artifact bindings; `fresh_replays=0`. This is not treated as a complete proof verification.
- `archived_four_port.log` and run-status metadata: full four-port replay started, then intentionally terminated at the confirmed-defect stop. No successful full-classification conclusion is claimed.
- `archived_cut204.log`: attempted replay from the compact bundle stopped because `CUT_MINOR_SIGN_SEARCH.json` is absent there. Full-archive inputs were still being acquired. This is not asserted to be a defect in the supplied full package.
- `triangle_context_control.py/.json/.log`: retained unresolved diagnostic, not an asserted theorem or counterexample.
- `defect_evidence.json`, `input_identity.json`, `compact_input_identity.json`, `reference_sources.json`, `RESEARCH_LOG.md`, and `verdict.json` preserve provenance, claims, limitations, and timestamps.

The compact ZIP is 38,014,437 bytes, SHA-256 `c9944a49681c00cdb75308d116869a9b1dab523391e58d2deb149396e4925cf0`. Its advertised purpose is an artifact-binding portal bundle; its README does not promise that it contains all regeneration inputs. The full archive was not falsely treated as complete or reviewed when only the compact bundle was available.

The strongest independently checked results are the exact H14 triangle geometry/tree–sunlet separation, the base mixed-graph rooting counts and nonisomorphism, and the fresh rational-interval strict-CT common rank-15 germ. The published proof's specific displayed tree-child witness is false. The entire main generic-identifiability theorem is **not cleared** by this review because the work stopped at that defect and the finite classification/probe obligations were not all freshly discharged.

No source manuscript, website, spreadsheet, Git state, Zenodo record, or external communication was changed. Review-local caches and extracted packages are ignored by a local `.gitignore`.
