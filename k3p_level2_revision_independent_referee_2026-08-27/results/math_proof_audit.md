# Independent adversarial audit of the current mathematical proof

Date: 2026-08-27
Auditor: independent Codex proof-review subagent
Package audited: `/Users/alec/Documents/Math/k3p_level2_identifiability_final/release/dist/K3P_Level2_Independent_Referee_Package`

## Scope, version, and evidentiary rule

I read the current rendered article and reader supplement in full and compared the proof against the current TeX sources in `proof_package/manuscript/sections/01_*.tex` through `17_*.tex`. I also read the portion of the bundled JC source on which generic noncut recovery depends. The current rendered files were:

- `paper/K3P_Level2_Identifiability_Article.pdf`, SHA-256 `97c14b1eb234f6dd71110c1afd5bf39ac3f7313359684a71a914d94f4c0657d1`;
- `paper/K3P_Level2_Identifiability_Reader_Supplement.pdf`, SHA-256 `b0d6d1e2aea371e9cab6f416452e496e0c9dfd80921d04d199bcd06b93083fcb`.

The two most revision-sensitive sources had SHA-256 hashes
`9106bce3df575f2c3fe0268d879db0fcbeee69861c0b40762230409ebf2c218f`
for `proof_package/manuscript/sections/04_physical_topology.tex` and
`7b9472d3ccb465f66d7647d65fab842e5a9cf246f4b34887952b4efdc8131d97`
for `proof_package/manuscript/sections/10_global_classification.tex`.

I did **not** execute any package program, verifier, mutation suite, or reproduction command. I did **not** infer truth from a stored `PASS`, status field, count, checksum, or claimed clean-room agreement. Read-only inspection of text and frozen record structure was used only to understand the mathematical interfaces. Accordingly, “verified” below means verified as a handwritten implication, sometimes conditional on an explicitly identified finite or exact-arithmetic premise; it does not mean that the machine premise itself was rerun or independently reconstructed.

Line references below are exact current source references relative to the package root. Within a paragraph, a bare `:line-range` continues the last fully named file; a section filename such as `04_physical_topology.tex` abbreviates `proof_package/manuscript/sections/04_physical_topology.tex`.

## Executive verdict

**No fatal counterexample, circularity, or direction/quantifier reversal was found in the revised non-computational chain.** The two previously vulnerable handwritten transitions are materially repaired:

1. The cut-transfer theorem now concludes only equality of the labelled **abstract, undecorated** bridge-incidence tree and expressly postpones trivalent decoration (`proof_package/manuscript/sections/04_physical_topology.tex:216-228`, `:289-298`).
2. The new trivalent-decoration lemma separates an ordinary branching component from a three-boundary cycle by six cubic circuits that remain zero/nonzero under the full positive labelled incidence gauge (`proof_package/manuscript/sections/10_global_classification.tex:5-34`).
3. The revised localization proposition no longer silently selects a fixed target type from a pointwise finite union. It constructs a semialgebraic incidence correspondence, uses finite-cover dimension, and then obtains an analytic fixed-type section from a full-rank incidence stratum (`proof_package/manuscript/sections/07_marginal_localization.tex:68-127`).

The strongest result independently supported by this no-execution audit is therefore:

> **Conditional mathematical result.** If the companion JC pointwise cut theorem cited in Proposition 4.3 (including its corrected topology/palette regeneration), the finite graph/algebra statements asserted in Lemmas 4.6 and 4.7, Theorem 8.2, Propositions 9.1 and 9.2, the exact \(H_{14}\) rank calculations, and the sharpness interval certificate are correct, then the displayed non-computational arguments carry them to the principal-domain classification, generic reconstruction, continuous-time restriction, and all-\(n\) sharpness statements without the old bridge-decoration gap or the old fixed-target-type section gap.

This is not an unconditional verification of the paper. The proof has an openly declared, very large finite machine dependency (`proof_package/manuscript/sections/17_reproducibility.tex:3-66`). Under the requested rule not to execute code or accept stored success, the zero-survivor palette, the 204 K3P obstructions, the 405,216-presentation exhaustiveness, restoration/probe exhaustiveness, exact \(H_{14}\) minors, and Krawczyk inequalities remain **unverified premises**. They are proof obligations, not handwritten logical contradictions.

My confidence is approximately **0.89** that the highlighted revised handwritten transitions are logically sound, **0.84** that there is no fatal gap elsewhere in the non-computational chain reviewed here, and only **0.45** in an unconditional end-to-end theorem certification under this deliberately no-code audit. The last number reflects untested evidence, not a discovered mathematical counterexample.

## Findings by severity

### No blocking handwritten defect found

I found no surviving analogue of the old claim that split equality itself decorates a degree-three component, no use of the local cycle/theta theorem before that decoration is supplied, no assumption of a common bridge tree in the proof that the bridge trees agree, and no invalid inference from a varying finite target type to a single analytic target section.

### U1 — decisive finite premises remain outside this audit

This is the exact remaining verification gap. Lemma 4.6 invokes the claim that the compressed direct-or-singleton-doubled palette has zero all-switching survivors (`04_physical_topology.tex:144-173`). Lemma 4.7 then invokes 204 exact strict K3P obstructions (`04_physical_topology.tex:176-213`). The local theorem invokes the complete primitive enumeration and its algebraic eliminations (`08_primitive_bounded.tex:196-281`) plus restoration and probe ledgers (`09_restoration_words.tex:17-55`, `:65-128`). The sharpness base invokes exact interval and Jacobian computations (`13_sharpness.tex:66-121`). None of those conclusions follows merely from the printed census.

The bundled JC source makes the same boundary explicit: the handwritten compression is at `proof_package/input_frozen/referenced_chat_manuscripts/jc_level2_source.tex:637-700`, while the zero-survivor and 204-minor steps are computational premises at `:807-868`. The current K3P generic-noncut proposition cites that JC cut theorem (`04_physical_topology.tex:78-95`), and the resulting generic-noncut statement is load-bearing for the easy directed cut inclusion (`:97-112`), hence for the main classification as well as generic reconstruction. A precise theorem in a companion manuscript is formally acceptable as a cited premise, even when same-author, and I found no circular dependency back to the K3P result. Its unreviewed status and unexecuted bundled evidence nevertheless mean that an independent end-to-end verdict must be explicitly conditional on validating it.

This is **not** evidence that the finite claims are false. It is the reason a no-execution referee cannot issue an unconditional pass.

### E1 — simultaneous contextual \(H_{14}\) use is compressed exposition

Lemma 5.3 is stated and proved for replacing one triangle in a fixed context (`05_three_leaf_geometry.tex:189-211`), whereas sufficiency speaks of using the relative germ for “each redirected triangle” and choosing the generic rank in one joint contextual contraction (`10_global_classification.tex:107-118`). The missing displayed sentence is the finite-product version: take the product of the common relative germs for all redirected triangle factors and apply the same constant-rank argument to their joint multilinear contraction. Because ordinary triangle factors are separate complete components in the recovered tree and only finitely many occur, this is a straightforward extension; I classify it as exposition, not a substantive gap. Confidence: **0.91**.

### E2 — two proofs are terse at their parameter-transport interface

Root movement says that, when the old root meets a reticulation-parent edge, the reversible edge products and “where necessary” the inheritance coordinate are transported (`04_physical_topology.tex:38-55`). The switching-by-switching reason is plausible and strict subdivision supplies the required local sections, but an explicit parameter formula would make the claim easier to audit.

Similarly, the bridge-fibre proof gets completeness by sectorwise rank-one peeling and freeness by marked one-character and unmarked pair anchors (`06_bridge_fibre.tex:20-85`). The argument is sound on the stated positive conservation-supported locus, but the transition from the peeled aggregate side tensors to all component factors is compressed to one sentence (`:41-49`). I found no extra gauge or holonomy counterexample on a tree. These are low-risk auditability issues, not demonstrated gaps.

### E3 — reconstruction step R3 is ordered before explicit bridge normalization

R3 says to use the six-circuit sum of squares before R4 factors and normalizes bridge blocks (`11_genericity_reconstruction.tex:121-131`). This is executable as written by taking a three-leaf marginal through one chosen leaf in each incident branch: every intervening two-boundary component becomes a positive K3P arm multiplier, and the circuits are incidence semi-invariants. That mechanism is proved across `04_physical_topology.tex:264-287` and `10_global_classification.tex:12-27`, but is not repeated in R3. This is expository ordering, not an algorithmic impossibility.

## Detailed transition audit

### 1. Fixed convention and strong tree-child combinatorics

The model fixes one-step root suppression and does not allow later cleanup to alter admissible rootings (`03_conventions_model.tex:16-38`). The no-omnian criterion argues both directions under that convention (`:47-65`). In the forward contrapositive, an ordinary tail with two retained reticulation edges can be rooted at its sole ordinary incidence, producing two reticulation children; in the reverse direction the incidence condition supplies an ordinary child at every ordinary tail and at every reticulation. I found no use of a restriction cleanup to enlarge the original rooting set.

The reduced-tree language is potentially dangerous because a degree-two nontrivial component would not be reconstructible from a set of edge splits. The later primitive bounds exclude that danger in this class: a strong cycle needs its incoming, path-sink child, and a repair port; a theta needs at least four physical boundaries (`08_primitive_bounded.tex:77-120`), and the bridge-fibre proof separately identifies the only candidate unmarked degree-two theta as the non-tree-child \(K_4-e\) factor (`06_bridge_fibre.tex:51-81`). Thus the only unresolved decoration after split recovery is genuinely the degree-three ordinary-vertex versus three-cycle ambiguity addressed by Lemma 10.1.

### 2. Strict subdivision, root movement, and true/generic cuts

The subdivision bounds are correct. For a residual spectrum ((c/r,g/r,t/r)), the six displayed lower bounds on (r) are exactly the three upper-coordinate and three inverse-Fourier positivity inequalities; the continuous-time additions are (r>gt/c,ct/g,cg/t) (`04_physical_topology.tex:8-36`). These choices can be made locally analytically because all bounds are strict.

True-cut rank is pointwise: conditioning on the cut character produces four rank-one blocks (`:62-76`). Generic noncut recovery is intentionally weaker and uses one nonzero minor on the strict isotropic JC slice to show that its full K3P pullback is not the zero polynomial (`:78-95`). The easy directed inclusion then correctly uses the fact that a nonzero polynomial cannot vanish on a source-open containment neighborhood (`:97-112`). There is no illicit promotion of generic noncut detection to a universal K3P pointwise converse; the paper reiterates that boundary at `:300-304`.

The only unresolved issue here is the external JC finite premise discussed under U1, not the polynomial-continuation implication.

### 3. Revised Lemma 4.6: balanced noncut compression

The handwritten part of the compression is coherent (`04_physical_topology.tex:117-174`):

- the rigid support uses at most four compulsory ports (`:129-140`);
- at most four actual color labels are added, leaving at most eight ports (`:134-142`);
- retaining the primitive blob and two labels of each color prevents a core or pendant edge from realizing the color split (`:140-142`);
- if a segment contains (c,d,c), the middle (d)-attachment lies on the path between the outer (c)-attachments in every switching, and a pendant edge can isolate only that one (d), while another (d) remains (`:144-150`);
- otherwise leaf restriction reduces each segment to one of five two-run words, with a doubled singleton if required (`:152-159`);
- once one switching fails the balanced split, the ordinary tree split criterion supplies a (2+2) quartet witness (`:162-167`).

The direction of the leaf-restriction implication is correct: a split displayed by every switching before restriction remains displayed after deleting leaves, so zero survivors in the reduced palette rules out an all-switching survivor before reduction.

The decisive sentence “the independent finite switching replay has zero survivors” (`:160-162`) is not proved by the surrounding prose. The printed counts at `:169-173` are checksums, not a substitute. Read-only inspection shows that the raw 216-direction table contains 12 displayed-by-all directions, including nonzero-reticulation records. That observation is **not** a counterexample: a raw flag concerns only its four active labels, while the Lemma 4.6 palette also carries the colors and compulsory roles inherited from the complete balanced restriction. A quartet can be displayed by all switchings even though an additional retained colored role prevents the complete color split from being displayed. It does, however, confirm why palette exhaustiveness and role semantics are load-bearing and cannot be inferred from the number 204 alone.

Verdict: handwritten reduction sound; finite zero-survivor premise unverified here.

### 4. Lemma 4.7 and Theorem 4.8: cut equality without a hidden common tree

The algebraic inference in Lemma 4.7 is correct conditional on its exact certificates. Strict positivity gives each of four character blocks rank at least one; total rank at most four would force every block to have rank one and hence all selected (2\times2) minors to vanish, contradicting the applicable signed/cyclic certificate (`04_physical_topology.tex:176-213`). What remains unverified is the asserted exhaustive partition (204=180+12+10+1+1), not this rank inference.

Theorem 4.8 now avoids the former circularity (`:216-298`). Assume a source bridge split (S=A\mid B) is absent from the target and form the two color hulls in the **target** reduced tree (`:230-238`).

- If their intersection contains an edge, that target bridge has both colors on both sides, hence crosses (S). The already proved easy inclusion makes it a source bridge, contradicting compatibility of two source-tree edge splits (`:240-245`). No common tree has been assumed.
- If the intersection is one component (v), every incident branch is monochromatic and each color occupies at least two branches. Hence (v) has at least four relevant branches and cannot be a binary ordinary vertex (`:247-256`). Lemma 4.6 supplies a wrong quartet in that one active blob (`:258-262`).
- Every intervening two-boundary target component marginalizes to a convex mixture of strict K3P path matrices; inverse-Fourier positivity is convex, its nontrivial eigenvalues stay in ((0,1)), and convolution preserves strictness (`:264-287`).
- The same four-leaf marginal retains two source leaves on each side of (S), so source rank is at most four while the target one-active obstruction gives rank greater than four (`:289-294`).

The conclusion is deliberately only the compatible split system and abstract bridge-incidence tree (`:295-297`). This is the correct conclusion. A tree and a three-sunlet at a trivalent component do indeed have the same three incident bridge splits, so any stronger conclusion at this point would be false.

### 5. Tree–sunlet circuits and contextual \(H_{14}\)

For a three-leaf tree, every circuit has equal portwise character multisets in its two monomials and therefore vanishes (`05_three_leaf_geometry.tex:17-44`, `:53-66`). For the displayed sunlet map, the six factorizations reduce simultaneous vanishing to one of two impossibilities: a nonzero composition margin forces a strict eigenvalue square to be (1), while vanishing of all three margins gives (p=p^2) with (p\in(0,1)) (`:65-99`). I checked the logical case split and the circuit multidegrees. I did not machine-expand all six displayed pullback identities.

The ordinary-triangle theorem correctly works relative to the irreducible hypersurface \(H_{14}\), not an ambient 15-dimensional model (`:122-181`). Conditional on the printed substitutions, nonzero 14-minors, and nonzero gradient, each orientation submerses onto a relative neighborhood of the same smooth hypersurface (`:134-163`). The irreducibility argument is valid: treating the polynomial as linear in \(q_{0CC}\), its coefficient is an irreducible primitive disjoint-support binomial, the displayed specialization proves it does not divide the remainder, and Gauss's lemma applies (`:165-179`). The exact determinant/substitution arithmetic was not independently recomputed in this no-code audit.

The contextual lemma has the right rank inequalities (`:189-211`). Writing each contextual map as \(F_i=\Psi\circ(\phi_i,\mathrm{id})\), a physical section of \(\phi_i\) gives \(\operatorname{rank}\Psi\le\operatorname{rank}F_i\), while factorization gives the reverse. A constant-rank section of \(\Psi\), followed by the orientation section, produces the same relative full-dimensional output germ. No tensor-product independence of the terminals is needed. The finite simultaneous extension is the expository item E1.

### 6. Bridge fibre and physical product chart

The contraction formula and incidence action are correctly matched (`06_bridge_fibre.tex:3-38`). For each fixed cut character, positivity turns the bridge flattening block into a nonzero rank-one matrix, whose factorization is unique up to one positive scalar. Peeling a tree yields one scalar for every incidence and sector, direct cancellation gives the converse, and there is no graph cycle to support holonomy (`:40-49`).

Freeness is also correctly handled. A marked component has one-character anchors. For an unmarked component of degree (d\ge3), the pair-anchor exponent matrix generated by
\((1,2),(1,3),(2,3),(1,4),\ldots,(1,d)\)
has full rank; the first (3\times3) determinant is (-2), and the displayed positive square-root normalizer is its inverse (`:51-84`). Three state sectors give block-diagonal rank (3d). Fixed observable state labels prevent treating a sector permutation as an unobservable gauge.

Strict subdivision supplies independent endpoint gauge coordinates and a residual strict edge on every bridge, so finite intersection gives a simultaneous physical local product chart in both domains (`:87-103`). I found no extra positive gauge, discrete compensator, or remote-factor cancellation on the tree.

### 7. Revised Proposition 7.4: fixed target type and no compensation

This revision closes the former quantifier gap (`07_marginal_localization.tex:68-127`). The argument now has the required order:

1. Work in a source product box where the focal map has maximal rank (`:77-91`).
2. For every one of finitely many target incoming/completion types, form the physical semialgebraic incidence set (Z_\tau\) (`:93-100`).
3. Use the original global analytic target section only to show that the finitely many projections cover the source box (`:101-104`).
4. Finite semialgebraic-cover dimension fixes one type whose projection contains an open source subgerm (`:104-106`; the supporting finite-cover lemma is at `:55-66`).
5. Stratify (Z_\tau\) analytically and semialgebraically. Lower-rank projection strata have lower-dimensional images, so one stratum projects with full source-parameter rank (`:108-114`).
6. The constant-rank theorem gives the desired physical analytic fixed-type section (`:114-124`).

This remains valid even when the source focal parametrization has redundant parameters: the incidence projection is to the source parameter box, and a full-rank stratum supplies a section as a function of those parameters. Intrinsic bridge extraction makes the projective focal orbit a function of the global tensor, so varying remote target parameters cannot alter a polynomial or rank obstruction on that orbit (`:124-126`). I found neither circular use of the local classification nor an exchange of “for every point there exists a type” with “there exists a type for every point.”

The marginal descriptor itself factors retained restrictions into independent triple-product maps, projections, permutations, and inheritance complements (`:3-53`). Its analytic submersion logic is sound; the assertion that the enumerated descriptors cover every used restriction remains tied to the finite graph records.

Fixed-full restoration also has the right direction: start with one actual full relation, marginalize it, and use a local physical section of the source marginal map. It does not invert an arbitrary target deletion or lift an unrelated small relation (`:129-144`).

### 8. Primitive cores, bounded residue, restoration, and arbitrary words

The non-computational primitive-core reduction is plausible and internally consistent (`08_primitive_bounded.tex:11-70`). Degree counting gives
\(\sum(\deg_B-2)=2(r-1)\). For (r=1) the blob is a cycle; for (r=2) biconnectedness and binary degree force a theta. The subsequent cases distinguish whether a pole is reticulate and whether the local source shares a path with an internal sink. I did not find an omitted acyclic source/sink placement or a mixed-core counterexample.

The minimum-repair table and completion formula (`:77-120`) are not derived in full prose. They are another finite grammar interface. In particular, the lower bound used later in Lemma 10.1 can be checked directly from the table: every theta has one incoming boundary, at least one path-sink child (two for \(\theta_2,\theta_3\)), and a nonempty minimum repair, so at least four physical boundaries.

The vector-field rank-upper mechanism in the bounded proof is mathematically valid (`:217-271`). If (A) encodes polynomial identities (J_fV=0), then
\(\dim E(\ker A)=\operatorname{rank}[A;E]-\operatorname{rank}A\).
A nonzero evaluation minor makes those kernel fields generically independent, giving a genuine global generic-rank upper; a polynomial map cannot have a special Jacobian rank above its generic maximum. Likewise a nonzero source minor cannot vanish throughout a source-open containment witness. The issue left to computation is whether all 405,216 presentations, maps, fields, transports, and certificates were actually generated and checked as asserted (`:217-280`).

The restoration and probe prose does not assemble unrelated marginal survivors. Proposition 9.2 fixes an actual anchor/full relation; every one- and two-port marginal then comes from the same finite target word, so the resulting pair orders are transitive (`09_restoration_words.tex:84-102`). This answers the natural coherence objection. The claimed exhaustive ledgers and zero unresolved rows remain machine premises (`:17-55`, `:65-82`). Conditional on them, the local theorem's transition at `:107-128` has the right source-to-target direction and leaves only labelled isomorphism or coherent ordinary-triangle redirection.

### 9. Lemma 10.1: the old bridge-decoration gap is repaired

This is the most important revised transition (`10_global_classification.tex:5-34`). Equality of cut sets provides corresponding positions in an **abstract** tree, and the bridge product chart makes the corresponding projective component tensor orbit intrinsic (`:12-17`). Under the most general positive labelled incidence change,
\[
q_{xyz}\mapsto A_xB_yC_zq_{xyz},
\]
the two monomials of every (I_j) contain exactly the same multiset of characters at each port. Hence each circuit is multiplied by one common positive monomial and its zero/nonzero status is unchanged (`:17-24`). A source ordinary vertex has all six circuits zero, while a strict three-sunlet has at least one nonzero (`:25-27`). This works pointwise, in either source/target direction, and does not require choosing a canonical incidence gauge.

The possible third case is also excluded: the primitive repair table forces every strong theta to have at least four physical boundaries, so a nontrivial three-boundary component is precisely an ordinary cycle (`:29-33`; supporting table `08_primitive_bounded.tex:77-120`). Therefore the necessity proof applies the local cycle/theta theorem only **after** all trivalent components are decorated (`10_global_classification.tex:36-50`).

Adversarial check: an ordinary trivalent tree and a three-sunlet really do have identical incident bridge splits, so the criticism of the old stronger split-reconstruction sentence was genuine. It is false as a criticism of this revision, because the revision states the limitation and supplies a separator invariant under exactly the contextual scaling introduced by bridge factorization. Confidence in this repair: **0.96**, conditional only on the explicit tree–sunlet factorization.

### 10. Simultaneous bridge gluing, including continuous time

The gluing estimates are correct (`10_global_classification.tex:56-105`). On compact local germs take (0<L\le A_h\le U), set
\(\varepsilon=\min\{1/4,L^2/(8U)\}\), (z_h=\varepsilon), and (x_h=\varepsilon/A_h\). Then

- (0<x_h\le\varepsilon/L\le1/8);
- every principal inverse-Fourier margin is at least (1-2\varepsilon/L\ge3/4);
- cyclically,
  \[
  x_C-x_Gx_T\ge \varepsilon/U-\varepsilon^2/L^2
  \ge 7\varepsilon/(8U)>0;
  \]
- the common effective isotropic spectrum satisfies the continuous-time margins \(\varepsilon-\varepsilon^2>0\).

The same effective (z) can be used on both networks even when their incidence products (A_h) differ, because the actual physical bridge is chosen separately as (x_h=z_h/A_h). Strict uniform inequalities persist in a three-dimensional neighborhood of each bridge coordinate, providing all independent bridge directions. The physical product chart is a local inverse, so component ranks plus bridge ranks add. I found no hidden assumption that the two networks have the same incidence representatives, and no loss of the CT inequalities under contextual scaling.

### 11. Genericity and exact reconstruction

The equality (d_N=\dim\mathcal V_N) is correctly proved from complex generic rank and the fact that a nonzero real polynomial minor cannot vanish on the Euclidean-open physical domain (`11_genericity_reconstruction.tex:3-15`). Finiteness for fixed (n) follows from the (r+1) vertex-disjoint terminal tree paths in a tree-child rooting and the binary degree count (`:17-28`).

The generic-intersection argument now contains the target-section step it needs (`:30-110`). The image of the total source rank-drop locus has dimension at most (d_N-1) (`:40-60`). If an intersection with a non-equivalent competitor had dimension (d_N), a full-dimensional regular source-image stratum would occur in it; a compatible incidence stratum then projects with rank (d_N), giving a physical analytic target right inverse (`:62-82`). Composing that section with a regular source neighborhood is exactly the directed relation, contradicting the main classification. This is not an inference from Zariski closure alone.

The passage from real semialgebraic dimension to proper complex Zariski-closed exceptional sets is valid (`:85-109`), and finite union does not fill the irreducible image variety. No target competitor with only a rank-deficient source realization can create a full-dimensional physical intersection, because that image was separately removed.

The reconstruction procedure is finite under its exact-real oracle (`:117-155`). Even if an early structural test were used only as pruning, R8's finite real-closed-field membership test guarantees that outside the competitor-intersection closures exactly one triangle class is feasible. The output is a topology class, not numerical bridge parameters. The R3 ordering issue is only E3 above.

### 12. Strict continuous-time restriction

From (c>gt,g>ct,t>cg), the definitions
\(u=\sqrt{gt/c},v=\sqrt{ct/g},w=\sqrt{cg/t}\)
give (u,v,w\in(0,1)) and ((c,g,t)=(vw,uw,uv)). The displayed inequality
\(1+vw-u(v+w)>(1-v)(1-w)>0\)
and its cyclic versions prove \(\mathcal D_{CT}\subset\mathcal D_+\) (`12_continuous_time.tex:3-18`). Since the CT domain is a nonempty Euclidean-open subset of the principal domain, a CT source-open containment witness is also a principal-domain witness (`:20-25`), and nonzero generic minors remain nonzero on a dense CT subset. The common triangle point and the bridge-gluing margins remain strict CT (`:27-40`). No boundary equality is admitted (`:43-44`).

### 13. Sharpness and the all-\(n\) cherry step

The base topology census and Krawczyk conclusions are computational premises (`13_sharpness.tex:16-50`, `:66-121`). Conditional on a common physical point at which both normalized maps have rank 15, the submersion theorem really does give an ambient-open common 15-dimensional germ (`:108-116`). Uniqueness is claimed only in the selected equality slice (`:119-121`), so there is no overstatement of global parameter identifiability.

The all-\(n\) cherry transition is independently checkable (`:123-190`). For each nonzero sector,
\(R_h=u_h/v_h\) and (P_h=u_hv_h\); strict positivity of the old Fourier coordinate makes the ratio legitimate (`:125-146`). The (2\times2) Jacobian determinant per sector is (2u_h/v_h), so the product is
\(8u_Cu_Gu_T/(v_Cv_Gv_T)\ne0\), and the positive inverse is
\(u_h=\sqrt{R_hP_h},v_h=\sqrt{P_h/R_h}\) (`:148-178`). Retained cherry coordinates then recover the entire old tensor after division by nonzero pendant factors. Hence exactly six observable dimensions are added to the common germ.

Topologically, extending the same labelled leaf by the same labelled cherry preserves a tree-child rooting, preserves the old non-tree-child rooting/omnian, adds only bridges, and leaves blobs and level unchanged (`:181-190`). Label preservation makes the newest cherry contractible under any alleged enlarged isomorphism or triangle equivalence, so such an equivalence would descend to the base pair. I found no zero-denominator, dimension, or descent counterexample.

## Explicit counterexample and circularity search log

The following plausible attacks were checked and did not invalidate the revision:

1. **Same split tree, different trivalent decoration.** This is a real counterexample to the *old* inference from splits to decorated components. The current theorem explicitly stops before decoration and Lemma 10.1 repairs it.
2. **Incidence scaling destroys the tree–sunlet test.** It does not: both monomials of each circuit have the same character multiset at every port, so arbitrary positive (A_xB_yC_z) scaling is a common monomial factor.
3. **The 12 displayed-by-all one-active entries contradict zero palette survivors.** They do not by themselves. The zero-survivor assertion is restricted to complete balanced noncut compressed colorings with all compulsory colored roles; a raw record flags only its active quartet. The machine exhaustiveness tying those semantics together remains unverified.
4. **Theorem 4.8 assumes the common tree it proves.** It does not. A target hull-intersection edge is first converted to a source bridge via the already established easy inclusion, and compatibility is then invoked only inside the source tree.
5. **A varying finite target type is silently fixed.** The revised semialgebraic incidence/stratification argument in Proposition 7.4 fixes a type and supplies a section.
6. **A target has a special rank above its certified generic upper.** Impossible for a polynomial Jacobian: generic rank is the global maximum. The vector-field identities therefore give a pointwise upper once their exact independence certificate is correct.
7. **Contextual bridge gauges can push the actual edge out of CT.** The explicit uniform (L,U,\varepsilon) estimates prevent this and leave an open three-sector neighborhood.
8. **Cherry ratios divide by zero or add fewer than six dimensions.** Strict positive Fourier parameters make the denominator positive, and the explicit six-coordinate inverse recovers both new edge spectra and the old tensor.

I found no circular dependency of Lemma 10.1 on the local classification it enables, no use of the fourteen-orbit theorem in the cut-tree proof, and no use of proper-intersection genericity to prove the containment classification on which that genericity relies.

## Exact remaining gaps and recommended disposition

1. **To certify the main classification unconditionally, independently validate the cited companion JC pointwise cut theorem—including its corrected topology/palette regeneration—and rerun or reconstruct the current zero-survivor palette and all 204 K3P one-active certificates.** The JC dependency enters at `04_physical_topology.tex:78-112` and is proved in the bundled source across `proof_package/input_frozen/referenced_chat_manuscripts/jc_level2_source.tex:637-868`. The current K3P interface is `04_physical_topology.tex:117-213`.
2. **Independently validate the finite local universe and its direction-sensitive certificates.** Exact interface: `08_primitive_bounded.tex:196-281`, followed by `09_restoration_words.tex:17-128`. Counts alone are insufficient.
3. **Independently recompute the \(H_{14}\) substitution, three rank-14 minors, and gradient.** The surrounding differential/irreducibility reasoning is sound, but those exact arithmetic inputs occur at `05_three_leaf_geometry.tex:134-163`.
4. **Independently rerun the Krawczyk and local rank enclosures for sharpness.** Exact interface: `13_sharpness.tex:66-117`.
5. **For publication clarity, add a one-sentence finite-product version of contextual \(H_{14}\), an explicit root-movement parameter formula near a reticulation-parent edge, and a sentence explaining how R3 obtains its scaled three-port marginal before R4.** These are exposition improvements, not conditions for mathematical correctness as presently understood.

Subject to successful independent validation of items 1–4, my mathematical recommendation on the revised non-computational proof would be **accept / no major proof revision required**. Under the present no-code mandate alone, the proper status is **conditional pass on handwritten logic; machine-dependent theorem not independently certified**.

## Addendum — exact audit of the cited JC dependency (2026-08-27)

### Bottom-line classification

The active 53-command route is not merely checking a stored `PASS`: its first command constructs a fresh graph-derived JC topology/polynomial certificate without reading `corrected_jc_cut_certificate.json`, its second command requires exact byte equality between that fresh object and the frozen object consumed downstream, and its third command applies three binding mutations. This is enough, if executed successfully and combined with the handwritten reductions in the companion manuscript, to regenerate the **finite computational ingredients** of the JC pointwise cut theorem used in `04_physical_topology.tex:78-112`. It is not by itself a proof of the full theorem: core exhaustion, arbitrary-word reduction, the crossing-quartet argument, and the final two-endpoint inequality remain handwritten.

I found **no concrete mathematical or implementation error** in the producer by static inspection. I did find two evidence-scope limitations:

1. the comparison verifier imports substantial graph semantics from the producer and does not independently recompute the endpoint polynomials or the 204 stored JC strict-minor/sign objects; and
2. the supplied active route does not contain the separately claimed enumeration of all 808,642 four-through-eight-port word distributions. It exhausts the already reduced five-word palette instead.

The second limitation is a reproducibility/documentation discrepancy, not a gap in the theorem, because the arbitrary-word-to-palette reduction is proved in prose and the companion source expressly says the large count is a checksum rather than a premise (`proof_package/input_frozen/referenced_chat_manuscripts/jc_level2_source.tex:829-867`). The appropriate final referee verdict is therefore: **the JC citation is formally usable as a cited premise, and the bundle gives a serious active replay of its finite core, but an unconditional end-to-end endorsement remains conditional on accepting or independently validating the companion theorem.** Confidence: **0.91** that there is no static mathematical/code defect in the supplied reduced-palette producer; **0.98** that the 53-command plan contains the required fresh-generation/byte-binding commands; **0.76** that the package, without executing it or obtaining the omitted independent JC replay, provides genuinely independent validation of every companion claim.

### Exact theorem-to-replay map

The K3P article uses the dependency only to show that a fixed K3P noncut minor is not the zero polynomial: it restricts to the isotropic slice, invokes a strict JC point, and then returns to the full K3P polynomial (`proof_package/manuscript/sections/04_physical_topology.tex:78-95`). The easy directed cut inclusion is then the elementary open-set consequence at `04_physical_topology.tex:97-112`. Thus the cited theorem needed here is exactly the companion pointwise statement at `proof_package/input_frozen/referenced_chat_manuscripts/jc_level2_source.tex:702-805`, not a claim of openness of the JC slice in the full K3P domain.

The companion proof decomposes into the following interfaces.

- The reduced bridge-tree argument produces either one active factor or a bridge between two active endpoints (`jc_level2_source.tex:637-665`). This is handwritten and does not depend on the JSON.
- Arbitrary one-factor noncuts are restricted to at most eight ports while preserving the primitive core, a minimum repair, all path-sink children, and two actual labels of each color (`jc_level2_source.tex:667-700`). This also is handwritten.
- In the one-active case, a non-all-switching displayed split is handed to a four-port strict minor (`jc_level2_source.tex:716-723`, `:829-865`). The producer supplies the finite palette obstruction and all four-port tensor/minor records.
- In the two-active case, the proof uses the endpoint dichotomy Δ>0 or Δ=0, Γ≥0 and four explicit minors/identities (`jc_level2_source.tex:725-794`). The producer supplies every bounded endpoint dichotomy certificate and independently regenerates membership of the four minors and the three symbolic identity remainders; the last strict inequality is the transparent handwritten step.
- Marginalization and the four-block rank count finish the pointwise theorem (`jc_level2_source.tex:796-805`). No computation is hidden there.

### What the fresh producer actually derives

`generate_cut_topology.py` states and implements a no-historical-input construction (`proof_package/cut_recovery/strong_crossbridge/topology_regeneration/generate_cut_topology.py:1-16`). It imports only standard-library modules and SymPy (`:18-31`), and rejects optimized Python (`:34-35`). The five core templates and the five compressed segment words are explicit inputs at `:38-40` and `:59-92`; they are mathematical grammar, not recovered from the frozen JSON.

Within that grammar the producer performs the following fresh work.

- It enumerates orientations on representative cycle and theta graphs and checks that their reduced isomorphism classes equal the five templates (`generate_cut_topology.py:156-248`). This verifies orientation enumeration **inside** the assumed cycle/theta core shapes; it does not replace the handwritten theorem that those shapes exhaust the class.
- It checks binary rooted DAG structure, reachability, the lowest-stable-ancestor condition, and a tree-child presentation (`:287-327`), suppresses the root (`:336-355`), and applies the stated rooting-independent standard-strong criterion (`:358-392`). Completeness of that criterion is a cited/handwritten structural result, not established by the program.
- It builds every bounded root/incoming/outgoing completion described by its grammar, including selected sink roles and dummy repairs on empty segments, and filters by those validity predicates (`:395-467`). It then recomputes switching descendant masks and collapses serial edges with identical switching signatures to one effective product (`:470-537`). This collapse loses no open parameter values: a finite product of numbers in (0,1) ranges over (0,1), and the tensor depends on such edges only through that product.
- It exhausts all five-word compressed palettes and the singleton-doubled variants for each of five cores and each root/nonroot role, directly tests display by every switching, and fails if any survivor remains (`:545-703`). The frozen result records ten families and zero survivors (`proof_package/cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json:60415-60501`).
- It canonically identifies tensors up to leaf permutations and switching-choice actions (`generate_cut_topology.py:706-761`), then constructs the exact JC Fourier mixture from XOR characters, inheritance weights, and one nonzero-character eigenvalue per effective edge class (`:768-793`). The formula is the standard group-based JC Fourier formula and is algebraically consistent with the chosen signatures.
- Its Bernstein conversion is exact over ℚ (`:796-820`). Nonnegative Bernstein coefficients with at least one positive coefficient give strict positivity on the open cube because every Bernstein basis function is positive there. The factor and partial-inheritance routines preserve that logic (`:823-956`): even powers are nonnegative; odd factors are required to be strictly positive; and a positive inheritance Bernstein basis combination is strict when at least one coefficient polynomial is uniformly strict. I found no sign or boundary error in this mechanism.
- Endpoint generation removes the unique complete central singleton-signature edge product, computes Δ and Γ, and certifies the dichotomy (`:959-1038`, `:1149-1196`). The fresh result is required to have 77 tensors; the frozen object exposes the expected partition (67+2+7+1) and no failures (`corrected_jc_cut_certificate.json:60502-60509`, `:104219-104220`).
- Four-port generation considers all three balanced splits of every canonical tensor, skips only those displayed by every switching, constructs exact flattening minors, and searches for a strict sign on the complete open cube (`generate_cut_topology.py:1041-1090`, `:1199-1251`). The bound frozen interface is 72 tensors, 12 displayed directions, and 204 strict wrong-split certificates (`corrected_jc_cut_certificate.json:2-4`, `:60250-60252`).
- The two-active routine constructs the four required block minors as literal matrix minors and verifies the three symbolic identities with zero remainders (`generate_cut_topology.py:1254-1311`). The frozen record exposes all four membership flags and all-zero remainders (`corrected_jc_cut_certificate.json:104222-104236`). The routine records, but need not machine-prove, the final implication from the endpoint inequalities and (0<z<1); that implication is correct.
- The active invocation does not pass `--skip-one-active`; it runs the endpoint, full one-active, two-active, and switching-compression routines and exits nonzero unless every generated section is exact (`generate_cut_topology.py:1318-1356`).

### Binding to the active 53-command route

The active plan declares 54 original commands, excludes only the nonmathematical live-checkout release-engineering mutation, and fixes 53 mathematical commands (`referee_tools/ACTIVE_VERIFIER_PLAN.json:46-55`). Its first three named commands are `cut_topology_graph_regeneration`, `cut_topology_graph_compare`, and `cut_topology_graph_mutations` (`:56-60`). The source command list shows that the first writes a fresh ephemeral candidate and the second passes that candidate to the comparison verifier (`proof_package/reproducibility/run_release_suite.py:116-134`). The referee runner imports this plan from the copied proof workspace and rejects count or order drift (`referee_tools/run_active_verifiers.py:220-263`); it executes inside a copied workspace and checks post-run drift (`:366-442`). An integrated replay later invokes the three-part topology wrapper again (`proof_package/reproducibility/verify_k3p_same_classification.py:1254-1284`).

Downstream programs read `upstream_frozen/corrected_jc_cut_certificate.json`, not the ephemeral candidate. That does not introduce a logical mismatch if the compare command succeeds: `verify_cut_topology_regeneration.py:236-254` requires literal byte equality between candidate and reference, in particular at `:246-248`. Provenance also labels this JSON an auxiliary frozen copy with active graph-derived regeneration (`proof_package/cut_recovery/UPSTREAM_PROVENANCE.json:23-31`). The historical withdrawn `pointwise_cut_certificate.json` is a different object (`UPSTREAM_PROVENANCE.json:14-21`) and should not be treated as the active corrected proof input.

Accordingly, the first two active commands are enough to bind fresh finite JC output to the bytes later K3P commands consume. The remaining active commands validate K3P-specific transfer, restoration, local geometry, and sharpness. They add useful downstream checks but are not what proves the companion manuscript's handwritten crossing-quartet or word-compression lemmas.

### What is not clean-room or freshly regenerated

The comparison program is fail-closed as a binding gate, but it is not an independent algebra verifier. It imports `generate_cut_topology` at `proof_package/cut_recovery/strong_crossbridge/topology_regeneration/verify_cut_topology_regeneration.py:14`, and uses producer data structures/functions to rebuild witness graphs, masks, and tensor hashes (`:53-75`). It independently fixes the core/orientation census and checks endpoint and four-port record counts, graph witnesses, split flags, and the zero-survivor status (`:78-170`). For a wrong split, however, it only requires that `strict_minor` be a dictionary (`:143-156`); it does not reconstruct that minor, its polynomial hash, or its Bernstein/factor sign. Likewise, endpoint rows are accepted from their top-level exact status/no-failures plus graph binding without recomputation of their stored Δ/Γ sign certificates (`:92-117`). The mathematical work for those signs therefore lives in the fresh producer itself.

The mutation suite imports both that producer and verifier (`test_cut_topology_regeneration_mutations.py:14-15`). Its three cases reverse a primitive arc, coherently change the ordinary-tree masks/hash/flags, and insert a coherent serial subdivision (`:45-101`). These are useful topology/byte-binding tests, but they do not mutate a strict-minor polynomial or sign certificate, an endpoint dichotomy certificate, the palette enumerator, or the core/completion grammar. Indeed the ordinary-tree mutation deliberately substitutes an arbitrary dictionary as `strict_minor` (`:68-82`), demonstrating the comparison verifier's intended limited semantic boundary.

There is later, genuinely separate K3P algebraic checking: `proof_package/cut_recovery/strong_crossbridge/final_certificate/verify_final_certificate.py:1-8` recompiles K3P Fourier polynomials from the frozen switching masks without importing the producer, constructs the 204-direction universe (`:121-215`), and replays the 180 single-minor Bernstein certificates while binding the remaining child families (`:340-418`, `:600-619`). This materially reduces the risk of a shared tensor-compiler error for the downstream K3P theorem. It is not, however, a clean-room reconstruction of the **JC producer's own** endpoint Δ/Γ records or its 204 `strict_minor` fields. The companion manuscript's stronger wording that a second implementation reconstructs all graph-to-polynomial assignments and agrees on all normalized records/minors (`jc_level2_source.tex:817-827`) is therefore not directly substantiated by the specific topology comparison files audited here.

The remaining trusted inputs are consequently:

- the handwritten structural lemmas and their match to the hard-coded five cores/completion grammar;
- the handwritten arbitrary-word reduction to `(), (0), (1), (0,1), (1,0)` and singleton doubling;
- the correctness of the one fresh Python/SymPy implementation for the JC endpoint and minor signs, plus Python and the pinned SymPy 1.14 dependency (`proof_package/reproducibility/requirements.txt:1-4`);
- successful execution of the active route, which this no-code audit did not perform.

### The 808,642 discrepancy

The companion source says that a standalone combinatorial implementation exhausts all 808,642 balanced four-through-eight-port binary word distributions and checks the reduction partition (`jc_level2_source.tex:851-855`). A source search found no such enumerator or numeric count in the supplied active code. The only Python occurrence of the descriptive phrase is a manuscript-snippet binding check at `proof_package/cut_recovery/strong_crossbridge/global_transfer/adversarial/verify_global_transfer_adversarial.py:635-651`, which checks that the words occur in the manuscript; it does not enumerate the distributions. The topology producer instead iterates `COMPRESSED_WORDS` directly (`generate_cut_topology.py:38-40`, `:660-703`).

This does not defeat the pointwise theorem. The proof at `jc_level2_source.tex:829-850` gives a complete dichotomy: a three-run c,d,c word is already an all-switching obstruction; otherwise each segment has at most two runs and restricts to the five-word palette, with singleton doubling when needed. The subsequent quartet step is handwritten at `:857-865`, and the source explicitly says at `:865-867` that the finite counts are checksums, not premises. Thus the absent 808,642-case replay is best classified as an **unreproduced auxiliary assertion / evidence-packaging overclaim**, not as a mathematical gap. If the authors want the package literally to support every sentence of the companion certificate lemma, they should include that independent enumerator or weaken `:851-855` to describe only the reduced-palette replay actually shipped.

### Final dependency verdict

For the narrow K3P inference at `04_physical_topology.tex:78-112`, I would not issue a new major-gap objection. The bundled current route is capable of regenerating the necessary finite JC topology, palette, endpoint, one-active, and two-active data and binding it exactly to the K3P input; the handwritten JC theorem transitions are coherent; and static inspection found no counterexample or code defect. Nevertheless, because the cited work is same-author and unreviewed, because no program was executed under this mandate, and because the JC algebra comparison is not clean-room, the final overall verdict should remain **explicitly conditional on independent validation (or accepted status) of the companion JC pointwise theorem**. The corrected topology regeneration materially narrows that condition; it does not eliminate it.
