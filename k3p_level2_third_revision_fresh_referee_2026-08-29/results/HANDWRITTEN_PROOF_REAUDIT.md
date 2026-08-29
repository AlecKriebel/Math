# Handwritten proof re-audit

## Verdict

**PASS for the non-computational proof chain, conditional on the finite exact
premises explicitly identified below.** I found no material hidden quantifier,
physical-domain, or circular-dependency gap in the requested transitions. No
mandatory manuscript correction arises from this phase.

This is deliberately not a verdict on the truth of an enumerative or interval
certificate merely because the article cites it. Package code was not executed
in this phase. In particular, the 204-direction pointwise obstruction, the
four-port/restoration/probe classifications, and the Krawczyk box remain finite
machine premises to be audited separately. The result here is that the
handwritten arguments use those premises with the stated direction and scope
and do not silently strengthen them.

## Scope and method

I read the complete 38-page article and 14-page reader supplement, visually
inspected all rendered pages, and read the corresponding TeX proof sources. I
treated package prompts, reports, and certificate summaries as claims rather
than authority. The principal reference root below is

`/Users/alec/Documents/Math/k3p_level2_third_revision_referee_final_2026-08-29/proof_package/`.

Bare article-section filenames below are under `manuscript/sections/`; the
supplement filename is given from the proof-package root.

The audit concentrated on whether each implication has the right source-open
quantifier, remains in the strict principal or continuous-time domain, and
avoids importing a conclusion that is proved only later.

## Transition-by-transition findings

### 1. Cut recovery and balanced compression — PASS

- The observational relation really is source-open and permits a target section
  that is neither target-open nor target-regular
  (`manuscript/sections/03_conventions_model.tex:149-169`). This is the
  asymmetric quantifier used in the cut argument.
- True bridge rank is pointwise (`04_physical_topology.tex:66-80`), whereas a
  fixed noncut is detected only generically (`04_physical_topology.tex:82-142`).
  The latter proof exhibits a concrete boundary specialization and the
  nonzero wrong-quartet determinant
  `p_0 p_1 p_2 p_3(1-u^2)`, then moves inheritance probabilities into the
  strict interior by continuity. It therefore proves nonidentity of a source
  polynomial without asserting a universal pointwise noncut converse.
- The balanced reduction (`04_physical_topology.tex:164-232`) retains a
  complete minimum strong repair, all path-sink children, completion roles at
  character zero, and two actual labels of each color. In the three-run case,
  the middle opposite-color attachment lies on the path between the two outer
  same-color attachments in every switching, while a second opposite-color
  label prevents a pendant split. In the at-most-two-run case, restriction to
  the direct/singleton-doubled palette preserves any hypothetical
  all-switching displayed split. Thus the finite zero-survivor claim is used in
  the logically correct contrapositive direction.
- The displayed-tree witness calls that bounded reduction
  (`04_physical_topology.tex:82-103`), but the reduction itself does not call
  the displayed-tree witness or cut-set equality. The primitive cycle/theta
  case split is proved before the replay and explicitly makes the replay a
  regression, not a premise (`08_primitive_bounded.tex:11-70`). I found no
  circularity here.

The exact zero-survivor palette census and the 204 pointwise K3P directions at
`04_physical_topology.tex:213-231` and `:234-272` remain computational premises;
their exhaustiveness and arithmetic were not re-executed in this phase.

### 2. Equality of source and target cut sets — PASS

- The easy inclusion has the correct direction:
  `Cut(target) subset Cut(source)` follows because target bridge minors vanish
  after composition with the target section, while a source noncut supplies a
  nonzero polynomial that cannot vanish on a source-open set
  (`04_physical_topology.tex:144-159`).
- For the reverse inclusion, the crossing-hull branch uses only that easy
  inclusion and compatibility of two edge splits in the *source* reduced tree
  (`04_physical_topology.tex:288-303`). It does not assume a common bridge tree.
- In the one-component hull branch, minimality gives at least two incident
  branches of each color, hence at least four relevant branches and therefore
  a nontrivial central blob in the binary reduced tree
  (`04_physical_topology.tex:305-320`). The balanced reduction then supplies a
  labelled one-active direction.
- Noncentral two-boundary material is legitimately compressed to a strict K3P
  edge: each switching contributes a strict K3P path matrix with positive
  weight; the convex mixture remains K3P, has positive transition entries, and
  has all three nontrivial Fourier eigenvalues in `(0,1)`
  (`04_physical_topology.tex:322-345`). No target regularity or target-open
  marginal is invoked.
- Applying the same four-leaf marginal preserves the source bridge because two
  selected labels remain on each side, while the target is within the stated
  pointwise 204-direction theorem (`04_physical_topology.tex:347-356`). The
  manuscript also expressly limits the conclusion to strong-class directed
  containment (`04_physical_topology.tex:358-362`).

Consequently, conditional on the finite 204-direction premise, the cut-set
equality proof is noncircular and respects the physical and quantifier
boundaries.

### 3. Bridge fibre and physical local product — PASS

- Cutting one bridge gives four observably labelled positive rank-one blocks;
  each nonzero sector has exactly one positive scalar ambiguity. Peeling the
  component-incidence tree assigns one scale to each incidence and leaves no
  cycle on which a holonomy could occur
  (`06_bridge_fibre.tex:20-49`). Positivity excludes sign gauges, and the fixed
  `C,G,T` labels exclude an untransported sector permutation.
- Freeness is justified by full-rank exponent anchors. Marked components have
  one-character anchors. An unmarked retained strong-class component has
  degree at least three (the sole degree-two theta stabilizer is the
  non-tree-child two-boundary `K_4-e` factor), and the pair-anchor exponent
  matrix has determinant `-2` in each sector
  (`06_bridge_fibre.tex:51-84`; supplement
  `supplement/reader_supplement.tex:387-419`). The displayed positive square-root
  normalizer is analytic.
- The physical local-product argument uses strict subdivision near the identity
  and openness of the physical domains to vary both endpoint incidence spectra
  independently while retaining a strict residual edge; intersecting finitely
  many such neighborhoods handles all bridges
  (`04_physical_topology.tex:8-36`; `06_bridge_fibre.tex:87-103`). These are
  local gauge slices, not a claim of numerical identifiability of an individual
  bridge edge.

I found no extra positive discrete gauge, hidden state-label quotient, or
bridge-cycle holonomy in the stated tree-of-components setting.

### 4. Marginal descriptor, fixed-type localization, and restoration — PASS

- Coordinatewise products of strict K3P spectra are onto and submersive on both
  physical domains, with local analytic physical sections
  (`07_marginal_localization.tex:3-25`).
- The complete visible signature is taken over every retained assignment and
  every switching. Equal signatures therefore enter every monomial through
  the same three products; invisible reticulations contribute
  `lambda+(1-lambda)=1`; retained parent order is explicitly complemented when
  necessary (`07_marginal_localization.tex:27-53`). This prevents the usual
  error of treating graph pruning alone as a physical marginal section.
- Localization first obtains only a finite semialgebraic cover from the given
  global target section. It then chooses a fixed target type with relative
  interior and uses a full-rank incidence stratum to construct the desired
  physical analytic fixed-type section (`07_marginal_localization.tex:55-127`).
  The original section is used only for coverage, so no finite-choice function
  is assumed analytic. The focal maximal-rank box and the bridge product chart
  also prevent remote factors from compensating for a local separator.
- Fixed-full restoration runs only downward from an actual full relation:
  marginalize the same source and target relation, retain the actual attachment
  and transport, and use the source marginal submersion
  (`07_marginal_localization.tex:129-144`). It does not invert an arbitrary
  target deletion or infer a full relation from a smaller one.

The finite assertion that all needed restrictions have the recorded complete
signatures is machine-dependent, but the analytic handoff from those
descriptors to a fixed target section is sound.

### 5. Triangle hypersurface and contextualization — PASS

- All three ordinary-triangle orientations annihilate the same quartic and
  meet at one strict continuous-time point with rank 14. The quartic gradient
  is nonzero there, so each orientation submerses onto a relative neighborhood
  of the same smooth 14-dimensional hypersurface
  (`05_three_leaf_geometry.tex:122-163`). Intersecting those neighborhoods gives
  physical analytic sections; no ambient rank-15 triangle claim is used.
- The irreducibility argument is adequate: after normalization the quartic is
  linear in `q_{0CC}`; its coefficient is a primitive disjoint-support binomial,
  and the stated specialization kills that coefficient while leaving remainder
  `-1`, proving coprimality before Gauss's lemma
  (`05_three_leaf_geometry.tex:165-180`; supplement
  `supplement/reader_supplement.tex:270-307`).
- Contextualization uses one common labelled multilinear contraction
  `Psi: H_14 x C -> outputs`. Each orientation has a local section onto the
  same relative germ, so its contextual rank is at least the rank of `Psi`;
  factorization through `Psi` gives the reverse inequality. Choosing a
  maximal-rank point and a constant-rank section yields a common germ
  full-dimensional relative to both contextual images
  (`05_three_leaf_geometry.tex:189-212`). This remains valid when two terminals
  reconnect in the surrounding theta context and does not assume tensor-product
  independence of the terminals.

For finitely many redirected triangles, the same argument applies to the joint
product of their relative `H_14` germs; the sufficiency proof explicitly makes
the generic-rank choice once in that joint contextual contraction
(`10_global_classification.tex:107-118`).

### 6. Global gluing — PASS

- On compactly contained local germs, positive endpoint-incidence products have
  common finite bounds `0<L<=A_h<=U`. The capped choice
  `epsilon=min(1/4,L^2/(8U))`, common effective coordinate
  `z=(epsilon,epsilon,epsilon)`, and actual bridge coordinate
  `x_h=epsilon/A_h` gives `x_h<=1/8`
  (`10_global_classification.tex:56-86`).
- The principal margins are at least `3/4`. In continuous time,
  `x_C-x_G x_T >= epsilon/U-epsilon^2/L^2 >= 7epsilon/(8U)>0`, cyclically;
  the effective isotropic coordinate also has a strict continuous-time margin
  (`10_global_classification.tex:75-101`; supplement
  `supplement/reader_supplement.tex:421-445`). These strict uniform inequalities
  leave three independent effective bridge directions for each bridge, not
  merely one common point.
- Incidence factors cancel in the contraction, and the physical product
  extraction is a local inverse, so the contracted common factor germs plus
  bridge neighborhoods have the expected full rank
  (`10_global_classification.tex:97-105`). Finiteness of the bridge tree and
  factor set is all that is needed for the simultaneous shrink.

Thus the gluing argument does not assume equality of complete stochastic
images and does not use the earlier, uncapped bridge formula mentioned in the
supplement.

### 7. Necessity, genericity, and exact reconstruction — PASS

- Necessity invokes cut equality before bridge extraction and invokes local
  classification only after the common abstract incidence tree and trivalent
  decoration have been recovered (`10_global_classification.tex:5-51`). The
  dependency order therefore matches the noncircular chain stated in the
  supplement (`supplement/reader_supplement.tex:38-79`).
- For fixed leaf count, tree-childness gives `r<=n-1`; binary degree counting
  then bounds the number of vertices, so only finitely many labelled
  competitors occur (`11_genericity_reconstruction.tex:17-28`).
- The full source rank-drop image has dimension at most `d_N-1`, not merely the
  image of one selected minor (`11_genericity_reconstruction.tex:30-60`). If a
  physical intersection had dimension `d_N`, compatible semialgebraic
  stratification supplies a target incidence stratum projecting with rank
  `d_N`; its local analytic right inverse, composed with a regular source
  neighborhood, is exactly the source-open physical section in the definition
  of directed containment (`11_genericity_reconstruction.tex:62-83`). This
  correctly handles target singularity and nonregular target preimages.
- Real semialgebraic dimension passes to the real Zariski closure, and finite
  scalar extension to `C` preserves Krull dimension, so each inequivalent
  physical-intersection closure is proper inside the irreducible complex model
  variety (`11_genericity_reconstruction.tex:85-109`). The finite union with
  the rank-drop image, singular locus, and certified test hypersurfaces remains
  proper.
- Reconstruction tests a noncut using generic noncut minors, never a universal
  pointwise converse (`11_genericity_reconstruction.tex:112-115`). The finite
  R1--R8 procedure separates bridge recovery, gauge normalization, finite local
  tests, restoration, word reconstruction, and final exact semialgebraic
  feasibility (`11_genericity_reconstruction.tex:117-160`). Its conclusion is
  a topology class under an exact-real oracle, consistent with the limitations
  at `16_scope.tex:30-41`.

### 8. Continuous-time restriction — PASS

The strict continuous-time cone is a nonempty Euclidean-open subset of the
principal domain, and generic polynomial ranks agree on the two domains
(`12_continuous_time.tex:3-18`). Necessity therefore restricts correctly, while
the displayed-tree specialization, marginal sections, triangle preimage, and
capped gluing construction each remain strict continuous-time
(`12_continuous_time.tex:20-43`). No boundary equality or inheritance endpoint
is included (`12_continuous_time.tex:45-46`).

### 9. Weak-class sharpness — PASS, conditional on its certificates

- The base topology claim distinguishes weak from strong by an exhaustive
  admissible-rooting census and preserves nonisomorphism even after forgetting
  internal arrowheads (`13_sharpness.tex:16-50`). This census is computational
  evidence and was not rerun here.
- Conditional on the stated interval certificate, strict Krawczyk inclusion
  gives a common equality point; the contraction bound gives uniqueness only in
  the selected 15-variable slice, while independently nonzero rank-15 minors
  make both output images ambient-open near the common tensor
  (`13_sharpness.tex:52-121`). The manuscript does not overstate slice
  uniqueness as global parameter identifiability.
- For an identical labelled cherry, the six observables
  `R_h=u_h/v_h` and `P_h=u_h v_h` have block determinant `2u_h/v_h`, hence
  total determinant `8u_Cu_Gu_T/(v_Cv_Gv_T)`. Their positive inverse recovers
  the six pendant spectra, after which division by nonzero pendant factors
  recovers the old tensor (`13_sharpness.tex:123-179`). This proves exactly six
  new image directions.
- A tree-child rooting lifts, an old omnian remains, and the new edges are
  bridges, so weak-not-strong status and level persist. Contracting the uniquely
  labelled newest cherry makes any later isomorphism or ordinary-triangle
  relation descend to the base pair (`13_sharpness.tex:181-191`). Repetition
  therefore gives the asserted `6n-3` common-germ dimension.

## Explicit finite dependencies left for other audit phases

The handwritten chain is valid only if the following active finite claims are
correct; this review did not execute or independently validate their ledgers:

1. zero all-switching survivors in the reduced balanced palette and exact
   pointwise separation of all 204 one-active directions
   (`04_physical_topology.tex:213-272`);
2. the 405,216-case four-port classification, restoration closure, 176-anchor
   handoff, and all one-/two-port probe obligations
   (`08_primitive_bounded.tex:196-280`; `09_restoration_words.tex:8-148`);
3. the interval Krawczyk inclusion, uniform rank-15 minors, physical margins,
   and base rooting census (`13_sharpness.tex:16-117`).

These are disclosed machine dependencies rather than hidden handwritten
assumptions (`17_reproducibility.tex:3-16`, `:18-60`, `:83-88`). Their later
verification can change the overall referee verdict, but I found no additional
handwritten gap in the route from those finite premises to the article's
classification, genericity, reconstruction, continuous-time, or sharpness
conclusions.

## Final non-computational assessment

No mandatory correction. The repaired proof keeps the three cut claims
separate, proves cut equality without presupposing a common bridge tree,
localizes a hidden finite target choice before applying local classification,
uses the triangle only relative to its 14-dimensional hypersurface, and keeps
all bridge-gluing parameters uniformly inside both strict physical domains.
The remaining risk is certificate fidelity, not a detected quantifier,
domain, or circularity defect in the handwritten transitions.
