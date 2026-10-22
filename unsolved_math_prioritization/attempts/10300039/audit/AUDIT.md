# Independent audit: asymptotic separation, problem 10300039

Date: 8 October 2026. Catalog rank 1007; problem code AMR-102-0039.

## Decision

**Accept the corrected v2 author packet as five scoped, valid partial approaches with disposition unsolved, 5/5.** All five authored proofs were independently checked, including their countercontrols and missing hypotheses. No mathematical correction to v2 is required. The initial freeze is superseded and is not part of this acceptance.

This is an independent AI mathematical and artifact audit, not human refereeing, proof-assistant verification, a novelty finding, or a solution of Calegari's question. Acceptance is conditional on the explicitly cited classical theorems in the usual mathematical sense. It is not a claim that every original proof in the dependency chain has been re-proved or even retrieved. Two 1998 original articles remain unavailable in full, as detailed below. In particular, neither the Anosov subclass nor worldwide present-day openness is certified.

The accepted author packet is exactly 45,884 bytes, with 21 files and SHA-256 df03afb408c6eb41c56a3a4a94faed0c6a90a08d890d9fd58ce568456de23b7b. Its externally supplied manifest has SHA-256 4ddc7651c1da6facd2692d5b2cfa1291ad64dbf8765bfb69079372aa9c46684f. The bootstrap pin is fa007f533eedc28a8d62b0197777c5d6d8cc7c6323a02bf9c3ec0534cf9e1665. These were checked independently before executing the authenticated author verifier.

## Target and source scope

The actual target page was freshly rendered from the pinned primary PDF and visually inspected. Question 10.1 asks for existence of one lifted leaf having an open hyperbolic halfspace in each complementary component, assuming tautness and two-sided branching. The printed question does not explicitly insert closedness. The author correctly restricts uses of cocompactness and the global limit-set alternative to closed manifolds. No conclusion for a broader noncompact interpretation follows from those applications. [Calegari, Problems in foliations and laminations of 3-manifolds, p.22](https://arxiv.org/abs/math/0209081v1).

The relevant statements and surrounding proof of §2.5 of Calegari's other article were independently inspected. Theorem 2.5.5 excludes empty-interior leaf limit sets in the non-separated, two-sided case. Theorem 2.5.6, explicitly credited to Fenley, requires a closed hyperbolic manifold and Reeblessness, and converts a proper leaf limit set plus branching in both directions into a dimension bound below two. Corollary 2.5.8 gives the resulting dichotomy. Tautness supplies the Reebless hypothesis in the intended closed setting; transverse orientation can be arranged in a finite cover without changing the universal lifted foliation. The author uses a weaker existential conclusion than the corollary's separated-leaf conclusion and does not overstate it. [Calegari, The Gromov norm and foliations, §2.5](https://arxiv.org/abs/math/0007120v2).

## Route 1: side domains and the horosphere control

**Pass.** A compactification neighborhood, rather than an escaping ray or a finite-radius empty ball, is the right certificate. In the Klein model, caps cut out by x·p > a, with a tending upward to one, shrink to the ideal point p. Hence a side-domain point supplies a contained geodesic halfspace. Conversely an interior point of a halfspace's ideal cap has the required neighborhood. This proves the equivalence and openness.

For the partition of the ideal complement, choose a sufficiently small connected ball-cap disjoint from the closed compactified leaf. Its interior is connected and avoids the separating plane, so lies on exactly one side. This yields the disjoint union of the two side domains; it does not imply that both domains are nonempty.

The z=1 horosphere is a decisive negative control. It is a proper plane with singleton ideal limit set. The lower side contains sufficiently small hemisphere halfspaces. Every side of every vertical geodesic plane, and both the inside and outside of every orthogonal hemisphere, contains points of arbitrarily small positive height. Thus none is contained in z>1. This invalidates the shortcut from a proper limit set to two halfspaces for an arbitrary plane. It does not satisfy the global foliation hypotheses and is not a counterexample to Question 10.1.

The finite exact controls vary hemisphere centers and radii and test both vertical sides. The universal classification argument above, not those samples, establishes the negative conclusion. The missing global step remains obtaining the required domains, or a proper leaf limit set, from arbitrary two-sided branching.

## Route 2: compact leaves and stabilizers

**Pass for v2.** The corrected lemma uses the leaf's stabilizer H, not invariance under the whole ambient group. Given a compact set K with HK=L, the bound R=max d(k,x) gives L contained in the R-neighborhood of Hx, while Hx is contained in L. If d(y,z)≤R, the triangle inequality gives (y|z)_o≥d(o,y)−R. This proves equality of the visual limit sets of bounded-Hausdorff-distance subsets. No ambient cocompact action or invariance under all of Gamma is needed for this lemma.

A compact incompressible leaf has a lift with cocompact action by its actual leaf subgroup. The application is therefore legitimate. A quasifuchsian stabilizer has a Jordan-curve limit set, which is proper; the cited closed, taut, two-sided dichotomy then supplies asymptotic separation. The more general proper-stabilizer-limit-set consequence follows identically.

This reasoning must not be applied to a noncompact leaf solely because it has a stabilizer. Cocompactness on that leaf is the required bridge. Nor does an unrelated quasifuchsian subgroup or an ambient virtual fibration identify a suitable leaf of the specified foliation. These exclusions are correctly stated. The author supplies no universal existence theorem for the required compact leaf, so this route does not solve the problem.

The v1 overstatement has already been corrected in the accepted frozen bytes. This audit creates no further patch and does not revive the initial freeze.

## Route 3: Hölder boundary maps

**Pass.** For n equal arcs, the squared-diameter sum is bounded by C²(2π)^(2α)n^(1−2α), and the maximal diameter tends to zero. For α>1/2 this proves zero two-dimensional Hausdorff measure and hence a proper image. More generally the same cover establishes dimension at most 1/α. No numerical approximation is used to determine the threshold.

The equality between the boundary image and the ambient leaf limit set requires the stated continuous extension to a compact closed intrinsic disk, together with a proper inclusion. An intrinsic-boundary sequence cannot have an ambient interior limit: properness would give a convergent subsequence in the intrinsic interior. Conversely an ambient-boundary sequence has a convergent subsequence in the intrinsic closed disk; continuity excludes an intrinsic interior limit. These facts justify the equality used by the author. The statement is conditional on having that disk compactification and extension, not an assertion that every target leaf already has them.

At α=1/2 this covering estimate is constant; below the threshold it grows. The conclusion cannot be extended by the calculation. Continuous sphere-filling maps independently refute an inference from continuity alone. Changing the circle metric arbitrarily would change the quantitative hypothesis and is not a proof of the required estimate. No Hölder estimate of the stated strength is deduced from branching.

## Route 4: uniform quasigeodesics and endpoint properness

**Pass under all stated hypotheses.** Uniform constants are essential. The Morse stability theorem gives one Hausdorff-distance bound for every orbit and its complete endpoint geodesic, in both directions. Merely orbit-dependent quasigeodesicity would not justify the compactness argument.

For an escaping sequence x_n in the plane, choose nearby points on geodesics (p,q_n) and pass to a convergent subsequence of q_n. If its limit differs from p, the upper-halfspace chart with p at infinity makes the geodesics vertical above bounded, convergent basepoints. A boundary-escaping sequence on them can limit only to p or that finite endpoint. If q_n tends to p, use a chart in which p is finite: the corresponding orthogonal hemispheres shrink to p. This proves the asserted upper containment of the limit set. Following the two ends of each orbit and then taking closure proves the reverse containment.

For compact A in the punctured sphere, the geodesics (p,q), q in A, meet a fixed compact set, represented by points (q,1) after putting p at infinity. The reverse direction of Morse stability places a point of each relevant orbit in a common closed ambient ball. Proper embeddedness makes its intersection with L compact. Its image under the continuous quotient projection is compact and contains q^−1(A); continuity makes that inverse image closed. Thus q is proper when Q is homeomorphic to R. Even without that quotient hypothesis, choosing orbit points in this compact intersection proves that the endpoint image E is closed away from p.

It follows that full-sphere limit set is equivalent to E filling the punctured sphere in this model. It does not follow that this is impossible. The author's proper Peano-surjection control is valid: each closed annulus admits a continuous interval surjection with prescribed endpoints, because a Peano square can be continuously mapped onto the annulus and endpoint-joining paths can be added inside it. Begin with the disk, concatenate consecutive annuli with compatible endpoints, and compose with absolute value to get a surjection R→R². Its radius grows at least like floor(|t|)−1, so it is proper. This is an abstract-map control, not an embedded flow or a counterexample foliation.

No step supplies the additional geometric restrictions that would exclude this abstract behavior. The result remains an endpoint reduction, not a solution for the Anosov subclass.

## Route 5: covers, isotopies, and product blow-ups

**Pass with the stated construction boundary.** Pulling the specified foliation back to a finite cover does not change its universal lifted foliation or metric. An ambient homeomorphism induces a homeomorphism of leaf spaces, preserving the R-covered property. For the identity-starting lift of an isotopy on a compact manifold, deck equivariance and a compact fundamental set times the compact isotopy interval give uniform displacement. The bounded-distance argument then preserves each ideal limit set. The compactness and choice of lift are correctly retained.

For the interval-insertion model, strict monotonicity follows because a positive base-coordinate difference remains after accounting for all inserted weights. Summability controls the total omitted tail uniformly. Therefore the weighted cumulative function has no jumps except at the designated sites; the inserted intervals fill exactly those jumps. Its values tend to both infinities because the total weight is bounded. This proves surjectivity, so the increasing map is an order-homeomorphism onto R. Dense countable insertion sets cause no additional gaps.

The coordinates can be chosen summably for a countable collection because the weights have no invariant geometric significance. The conclusion applies only to product blow-ups with exactly this ordered interval leaf-space effect. It does not rule out more general surgery. Within the stated family, R-coveredness is preserved, so the required two-sided branching cannot be manufactured. No general nonexistence theorem for counterexamples is claimed.

## Dependency inspection and unresolved originals

All five pinned PDFs were independently hashed. Fresh pdftotext extraction from each PDF matched the text inspected in this audit exactly; extraction output and screenshots are not distributed. The question page and Fenley's p.85 were also freshly rendered and visually checked.

- Fenley's 2005 arXiv manuscript, Theorem 7.3, assumes a closed atoroidal manifold and an almost-transverse **quasigeodesic singular pseudo-Anosov** flow, with transversality to the associated almost pseudo-Anosov flow. It is not an unrestricted extension theorem for arbitrary taut foliations. Section 8 distinguishes extension, branching, and proper limit-set questions. The author makes no broader application. Manuscript pagination is retained separately from the 2009 journal article. [Geometry of foliations and flows I](https://arxiv.org/abs/math/0502330v2).
- The 27 February 2026 arXiv revision has the closed-hyperbolic, non-R-covered topological Anosov hypothesis in its main theorem. Its p.85, item E, still raises the relevant full-sphere question, including Anosov leaves. The arXiv version date was independently checked. This is dated evidence only. [Non R-covered Anosov flows in hyperbolic 3-manifolds are quasigeodesic](https://arxiv.org/abs/2210.09238v2). The publisher independently confirms 23 March 2026 publication, volume 36, pages 412–508; its subscription PDF was not used or equated to the manuscript. [Publisher record](https://link.springer.com/article/10.1007/s00039-026-00733-5).
- Buckminster's Theorem A concerns the leftmost **global universal circle** of a non-R-covered Anosov foliation on a closed hyperbolic manifold. Section 3 separately constructs leafwise extension maps; its working orientation and coorientation assumptions are explicit. A surjective global circle map does not imply a proper or a surjective boundary image for any particular leaf. This source remains identified as a preprint. [Cannon–Thurston maps for Anosov foliations](https://arxiv.org/abs/2604.21201v1).
- The AMS indexed abstract for the 1998 local/global article appears to make a stronger assertion about quasigeodesic Anosov leaf limit sets. The original full text remains inaccessible; the direct publisher page returned 403, and no access restriction was bypassed. The indexed abstract was not substituted for a source-complete theorem application. Reconciliation with the 2026 item E remains an exact blocker to claiming the Anosov subcase resolved. [AMS article record](https://www.ams.org/tran/1998-350-10/S0002-9947-98-01973-4/).
- The 1998 Topology original underlying Calegari's Theorem 2.5.6 was not available for a full-original proof audit. The accepted applications rely on the precisely stated theorem in the inspected Calegari primary article. This boundary must remain explicit. [Limit sets of foliations in hyperbolic 3-manifolds](https://doi.org/10.1016/S0040-9383(97)00062-1).

Morse stability, the quasifuchsian Jordan-curve characterization, and classical Peano parameterization are standard mathematical dependencies. Their exact uses and hypotheses were checked above; finite diagnostics are not evidence for their truth. A dependency-complete re-verification of their original proofs is not claimed.

## Artifact and execution audit

The outer packet, outer manifest, expanded final directory, nested author archive, and bootstrap all matched their authenticated pins. The entire 21-file boundary was checked, not merely the 12 author files. The packet contains authored mathematics and verification metadata only. No source PDF, source extraction, screenshot, dataset record, dataset contents, or private coordination material is included in this audit or its acceptance bundle.

The actual final directory was tested as uid 1000 with nonwritable files and directories. Attempts to create a file there or open the bootstrap for writing were denied. Its bytes were unchanged afterward. Read-only relocated copies passed too.

The independent harness itself was run in normal, -O, and -OO modes. Each run exercised the author bootstrap in all three corresponding interpreter modes with both full corpora and all five PDF identities. Independent code separately rehashed both corpora, checked their record counts, selected the unique target, reproduced all target serialization hashes, and checked the five PDF hashes. Those receipts contain identities and match results only.

Per independent harness run, 60 adverse executions were rejected, including missing files, extra files and directories, archive edits and duplicate ZIP entries, malformed or wrong-target manifests, symlinks, a malicious-code sentinel, wrong object types, unauthenticated author edits, unknown options, incomplete or malformed external corpus inputs, and absent source files. Ten additional direct guard controls exercise malformed identity schemas, duplicate JSON keys, nonfinite constants, and invalid JSON after loading the independently authenticated bootstrap. A whole-outer-directory control catches an extra file outside the inner bundle.

Most malformed distribution tests are expected to fail at the outer hash or exact-inventory gate before reaching parser details. They do not by themselves prove parser robustness; the separate direct guard controls address that distinction. The included author harness was also replayed independently: six positive and 51 negative controls passed.

There are 2,773 independent exact-rational mathematical diagnostics per harness run. They test hemisphere/vertical-side controls, bounded-distance inequalities, the strict Hölder threshold including its endpoint, upper-halfspace geodesic endpoint limits, and interval insertions at accumulating sites. None proves an infinite topological or geometric assertion. The proof review above is separate.

Trust remains bounded by the authenticated external bootstrap pin, the trusted interpreter and standard library, the operating system, and a quiescent filesystem. No claim is made against concurrent file races, runtime compromise, or a malicious replacement of the externally trusted pin. No remote write was performed.

The historical repository duplicate-search account in the author's SOURCE_AUDIT.md was not re-enacted by this mathematical audit. This acceptance does not independently certify an exhaustive repository-history search or current queue state. The full corpus identities and the intended mathematical target were independently verified.

## Remaining mathematical obligation

For the closed interpretation, the missing universal step is to exclude all lifted leaves having the full visual sphere as their limit set under tautness and two-sided branching. None of the five routes establishes that step without additional assumptions. For a broader noncompact interpretation, even the invoked global dichotomy has not been supplied. The correct queue disposition remains **unsolved, 5/5**. This acceptance records genuine partial reasoning and construction obstructions, without promoting them to a solution.
