# Algebra and topology overlap findings

Snapshot: OpenAI `adc7f1241b42e322a6451854ab7e4b4c146bf78a` (2026-10-06T21:58:50Z), 372 families / 722 manuscripts. Our open/draft inventory is `sources/open_prs.json`. This is a relationship review, not a validity audit of the OpenAI proofs. Source browsing and downloaded manuscript LaTeX were read-only. No researcher was contacted. Report checkpoint 2026-10-06: comparison task approximately 95% complete in this approach family; the remaining proof-validation work is deliberately outside this comparison's scope.

## 1. Highest-priority finding: conditional negative answer to our wreath-Hopfian target

**OpenAI:** [197: A torsion-free group algebra that is not directly finite.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/direct-finiteness.pdf) (prime-field, torsion-free manuscript).

**Ours:** [#389 2531: reviewed Hopfian wreath-product partials (unsolved, 5/5)](https://github.com/AlecKriebel/Math/pull/389) (draft: True, head `fcb661d172c182d0437a07c3714ad4e113278d3b`). The immutable `FINAL_RESULT.md` says the original question is the standard restricted regular wreath product of two finitely generated Hopfian groups, and remains unresolved after five author turns. It expressly identifies abelian group-ring stable finiteness as a residual obstruction.

**Relation: conditional subsumption of the original existence question.** OpenAI's manuscript main theorem asserts finitely presented torsion-free G and a,b,c in F₂[G] with ab=1, ac=0, c≠0, hence ba≠1. This would negate Kaplansky direct finiteness. Bradford–Fournier-Facio's published [Theorem 1.3 / 4.11](https://d-nb.info/1355447615/34) identifies that conjecture with the assertion that every finitely generated abelian A and every finitely generated Hopfian Γ has Hopfian A wr Γ. Its contrapositive therefore supplies finitely generated Hopfian factors with a non-Hopfian regular wreath product. This is a deduction from the external claimed result and the published bridge, not an assertion that our packet already proves it.

**Exact hypotheses / constructive strengthening:** The specific OpenAI G is not asserted Hopfian. Directly setting Γ=G would leave a real hypothesis gap. However, BFF Theorem 4.11's proof explicitly imports the theorem that every finitely generated group embeds in a finitely generated Hopfian group (reference [39]); this resolves that gap without asking G itself to be Hopfian. Since F₂[G] embeds into F₂[Γ], the one-sided inverse defect persists. BFF Theorem 1.5 then implies C₂ wr Γ is non-Hopfian (the relevant matrix size is 1). C₂ is finite, finitely generated, and Hopfian. No explicit finite presentation for Γ is needed by the original target. This does not answer the separate nonabelian-free-base question.

**Correction history:** The initial comparison identified the missing Hopfian hypothesis for OpenAI’s particular G and tentatively classified the relation as neighboring. Retrieval of the published BFF theorem and its proof showed that the imported finitely generated Hopfian embedding removes that hypothesis gap. The final relation above supersedes the tentative classification. Root reports a separate adversarial check of the bridge and explicit right-multiplication wreath epimorphism; this remains conditional on the unadjudicated OpenAI theorem.

**Verification:** Full OpenAI LaTeX source was retrieved under the pinned commit; its introduction/main theorem was checked. The BFF published PDF was browsed, especially printed p.3 Theorem 1.5 and printed p.22 Theorem 4.11/proof. [Cambridge published-version record](https://www.repository.cam.ac.uk/handle/1810/376427), [journal DOI](https://doi.org/10.1007/s00209-024-03589-3). The OpenAI construction/probability/topology argument was not independently audited. Consequently the full target should not be reclassified as solved on this comparison alone.

## 2. Nagata and the irrational-Seshadri project

**OpenAI:** [039: Nagata’s conjecture and maximal Seshadri constants.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Nagatas-Conjecture-for-Plane-Curves-September-23-2026/main.pdf).

**Ours:** [#712 30003978: credit recent Seshadri preprints for all r >= 9](https://github.com/AlecKriebel/Math/pull/712) (draft: True, head `b33bc36a06b904d6746cedeb437bd46a98ac0d7f`).

**Relation: same conjectural premise and stronger multipoint statement; not direct duplication of our credited single-point constructions.** OpenAI asserts the full strict Nagata inequality for all r≥10 very general complex points and arbitrary multiplicities. Our question concerns irrational **single-point** Seshadri constants of **integral ample polarizations on plane blowups** at r≥9 very general centers, formerly conditional on Nagata. Our draft credits Laface–Ugaglia for r=9 and Malara–Merta–Szpond–Zieliński for every r≥10. If OpenAI's theorem is valid, the original Nagata premise becomes available for r≥10; the current credited prior-preprint resolution remains separate.

**Boundary:** OpenAI's equality ε(O(1);p₁,…,pᵣ)=1/√r is multipoint on P² and is irrational only at nonsquare r. It is not the same assertion as an irrational single-point constant on the r-point blowup with an ample integral polarization. Nine points are excluded from OpenAI's strict Nagata theorem because a cubic passes through nine points. Our prior-preprint result includes r=9. No conclusion for arbitrary/special centers or every evaluation point follows.

**Verification:** OpenAI introduction and consequences were read; our complete PR body and cited scope were inspected. Geometric validity of OpenAI's degeneration/interpolation proof was not audited.

## 3. CM reduction / Tate classes: compatible neighboring results, not a contradiction

**OpenAI:** [001: Milne’s rationality conjecture and algebraic specialization.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Milnes-rationality-conjecture-for-abelian-varieties-September-23-2026/paper.pdf) and [032: Hodge and Kuga–Satake results for all projective K3 surfaces.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-September-30-2026/paper.pdf) (the latter CM-abelian manuscript also states the consequence: Tate conjecture for all abelian varieties over finite fields).

**Ours:** [#799 CM reduction: eightfold candidate and literal converse, two AI audits](https://github.com/AlecKriebel/Math/pull/799) (draft: True, head `cc45ec9dc93515593c3b2a228def86c3a562e13f`).

**Relation: exact shared CM-specialization setting, complementary questions.** Our candidate gives a simple CM eightfold all of whose powers have divisor-generated (Lefschetz) Hodge classes, with a geometrically simple characteristic-5 reduction having codimension-two Tate dimension 32 versus divisor-product dimension 28. OpenAI asserts algebraicity of all rational CM Hodge classes and, through Milne's implication, all Tate classes on abelian varieties over finite fields. These statements are compatible: non-Lefschetz is not nonalgebraic. If the OpenAI result is valid, the four extra Tate dimensions in our candidate are represented by algebraic cycles beyond divisor products.

**Boundary:** Family 001 controls specialized Hodge classes and cohomology-independent rational pairings. It does not say every new Tate class of a reduction came from a Hodge class on the original lift. The codimension-two Hodge space on our A has dimension 28; the new four Tate dimensions therefore do not contradict the family-001 specialization assertion. Our eightfold is neither ordinary nor supersingular; Newton slopes are 0^6, (1/2)^4, 1^6. No Hodge/Tate-conjecture disproof is claimed in our draft.

**Verification:** Complete corrected proof from our immutable PR head was retrieved/read. Pinned OpenAI introductions and consequences were retrieved, and the broad theorem statements checked. Neither complete OpenAI CM proof nor every imported Milne theorem was reaudited.

## 4. Keller/Jacobian: nearby affine geometry, no direct claimed resolution found

**OpenAI:** [047: Zariski cancellation and affine fibrations over the complex numbers.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026/paper.pdf) and [049: A stable-coordinate counterexample in four variables.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-stable-coordinate-that-is-not-a-coordinate-in-four-variables-October-5-2026/stable-coordinate-four-variables.pdf).

**Ours:** local `dimension_three_keller_degree/README.md` and [#236 30000661: reviewed five-turn partial; generalized tameness unresolved](https://github.com/AlecKriebel/Math/pull/236) (draft: True, head `3cf1565194a867ce4ab3ad7cb72416f22366f955`).

**Relation: background/neighboring affine algebraic geometry.** Family 047 claims a complex affine fourfold X≄A⁴ with X×A¹≅A⁵ and nontrivial A³-fibrations. Family 049 claims a noncoordinate polynomial in four variables becoming a coordinate after one variable is added. Our main Keller program asks whether degree-four Keller maps of C³ are excluded; its README retains universal floor 4 and only scoped structural-row exclusions. PR236 asks exact finite-word membership in polynomial locally-nilpotent-derivation exponentials for a three-variable automorphism, with localized factors and stable tameness insufficient for descent.

**Boundary:** Cancellation, stable coordinate, tameness and the Jacobian conjecture are distinct statements. Affine-space fibers do not on their own produce a constant-Jacobian nonautomorphism in C³. No Jacobian/Keller claim or manuscript was found in the 372-family catalogue. Neither family 047 nor 049 currently subsumes the degree-four frontier or PR236's exact LND-word question.

## 5. Affine-fibration comparison across characteristic

**OpenAI:** [047: Zariski cancellation and affine fibrations over the complex numbers.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026/paper.pdf).

**Ours:** [#354 30000660: credit Russell-form obstruction to the literal 2007 étale claim](https://github.com/AlecKriebel/Math/pull/354) (draft: True, head `ab0a7dd122a3d9d74d8308e056e1709ad0e97685`).

**Relation: substantive neighboring counterexamples to local triviality of affine-space fibers.** Our credited Russell-form family yᵖ=x+t xᵖ has smooth geometric A¹ fibers in characteristic p but no dominant étale base change trivialization; a purely inseparable degree-p base change does trivialize it. OpenAI's family 047 asserts non-Zariski-locally-trivial smooth A³-fibrations over C.

**Boundary:** Different fields, dimensions, and allowed base changes. Our draft explicitly leaves the Qbar case and later finite-degree question untouched. OpenAI's non-Zariski-triviality alone does not imply failure of trivialization after a finite/étale cover. Thus this is not automatic resolution of those remaining questions.

## 6. Disk embedding and good-group boundary

**OpenAI:** [305: Four-dimensional disk embedding and Wall's conjecture.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-boundary-only-obstruction-to-four-dimensional-disk-embedding-September-24-2026/paper.pdf).

**Ours:** [#868 KP-4.52 (2928): audited stable-normal-invariant partials, unsolved 3/5](https://github.com/AlecKriebel/Math/pull/868) (draft: True, head `2dd6bb1f11c85d5380cee32b9ffa5d54e6171543`).

**Relation: directly relevant hypothesis boundary, not solution of our stable-normal-invariant question.** The OpenAI disk manuscript asserts F₂ is not good in the Freedman–Quinn sense, and every group containing F₂ is likewise not good. Our accepted orbit/classification reductions keep a good-group hypothesis and Whitehead-group assumptions. If the OpenAI claim is valid, its nongoodness conclusion prevents extending those good-group arguments to free-group-containing examples merely by appealing to unrestricted disk embedding.

**Boundary:** The good-group-scoped deductions in our draft remain logically compatible. OpenAI does not by itself provide the unstabilized simple-self-equivalence realization/cancellation needed in our residual gap.

**Verification:** Full pinned disk manuscript intro/main theorem/nongoodness corollary were read, including its explicit use of subgroup and quotient closure of good groups. The representation-deformation obstruction proof was not audited.

## 7. Four-manifold homotopy rigidity

**OpenAI:** [320: Nonhomeomorphic closed aspherical four-manifolds.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Nonhomeomorphic-closed-aspherical-four-manifolds-with-the-same-homotopy-type-October-4-2026/paper.pdf).

**Ours:** [#865 Audit KP-4.18 prior part (a) implication; retain unsolved (1/5)](https://github.com/AlecKriebel/Math/pull/865) (draft: True, head `51e041675eee6170964a5512771b1266e5d33bd5`).

**Relation: substantial neighboring nonrigidity results, not exact target equivalence.** OpenAI asserts homotopy-equivalent but nonhomeomorphic closed **aspherical topological** four-manifolds with a common word-hyperbolic group, defeating Borel rigidity. Our draft credits recent preprints for **smooth closed** four-manifolds homotopy equivalent but without a simple homotopy equivalence even after S²×S² stabilization, with group G*G; the separate part (b) remains unresolved.

**Boundary:** Homeomorphism versus simple homotopy equivalence, aspherical versus unrestricted, topological versus smooth, and unstabilized versus stabilized comparisons are different. Neither result immediately implies the other. Our credited part-(a) finding and OpenAI's Borel counterexample can coexist.

## 8. Artin asphericity and F₄/H₄ commensurability

**OpenAI:** [254: Classifying spaces and geometric obstructions for Artin groups.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Harmonic-heights-and-the-Artin-K-pi-1-conjecture-September-23-2026/paper.pdf).

**Ours:** [#440 KOU-21.128: audited F4/H4 commensurability partial results (unsolved 5/5)](https://github.com/AlecKriebel/Math/pull/440) (draft: True, head `53601d32c7f206bae6a93bc2b11d4071a6c34d31`).

**Relation: relevant common infrastructure.** OpenAI claims Salvetti asphericity for every finite-rank Artin group. Our F₄/H₄ spherical-type Artin commensurability packet already uses Deligne's asphericity and finite-CW input, and leaves an unproved commensurator premise. The new general asphericity claim would extend infrastructure to other types; it does not settle our F₄/H₄ commensurability problem.

**Boundary:** Both of our types lie in the classical finite-type asphericity regime, so the broad OpenAI theorem provides no missing asphericity hypothesis in this packet. The additional CAT(0)-nonexistence and parabolic-intersection results are distinct.

## 9. Artin primitive roots and the diagonal quartic prime question

**OpenAI:** [029: Primitive roots for every admissible integer base.](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Primitive-roots-for-every-admissible-integer-base-October-4-2026/primitive-roots-all-integer-bases.pdf).

**Ours:** [#299 3356: reviewed five-turn partial results; original primitive-root conjecture unsolved](https://github.com/AlecKriebel/Math/pull/299) (draft: True, head `f67abd7ab51a47d29efecf5b40ae2b01090e9820`).

**Relation: same base a=3, stronger generic-prime supply, different prime subsequence.** OpenAI claims infinitely many primes with primitive root a for every admissible integer a, giving lower bounds in dyadic intervals. Our target asks whether 3 is a primitive root for primes p=16q⁴+1 with prime q, and our draft verifies all q through 10⁸ while retaining a q-primary obstruction.

**Boundary:** An infinite set of primes for which 3 is primitive does not select p=16q⁴+1, and does not establish the universal assertion on that sparse diagonal. Even full Artin infinitude cannot eliminate that remaining gap. This is neighboring number theory, not subsumption.

## False matches actively excluded

- OpenAI 205 Saxl tensor-square conjecture versus our #403 generalized **Saxl graph** common-neighbor counterexample: representation-theoretic tensor coverage and permutation-base graphs are different questions; shared surname is insufficient.
- OpenAI 251 strong unitary Ulam stability versus our #346 flexible **permutation** stability: different approximation norms, stability definitions, and allowable changes of dimension. No resolution transfers without a new bridge.
- OpenAI 248 nonamenability of Thompson F versus our #437 virtual finiteness spectrum {0,1} for F: amenability is not the missing F_n-kernel premise, so no direct resolution.
- OpenAI 247 finitely presented residually finite infinite 2-group versus our #723 shortest laws in **finite iterated binary wreath groups**: no uniform law or exact shortest-law consequence follows.

## Local source records

The selected OpenAI main sources and full section sets were fetched from pinned commit URLs, retained under this folder, and are identifiable by corresponding `openai_*_directory.json` / `openai_*_sections_directory.json`. The attempted full recursive GitHub tree was truncated (`truncated=true`) and was **not** treated as an exhaustive file inventory; selected direct directory APIs supplied the actual manuscripts. The catalogue snapshot is the exhaustive family-level basis of the negative direct-Keller statement.

The failed fetch `our_712_PROOF.md` was an incorrect path (404); no such source was used. PR712 scope was taken from its exact captured PR body. Our #389 and #799 proof files were fetched from the immutable heads above. Proof validity and mathematical novelty remain unadjudicated unless expressly described as a short checked conditional deduction.
