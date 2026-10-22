# Independent audit of K3 Problem 2 21 partial results

## Verdict and exact scope

Accept the exact six-file author freeze as a mathematically sound, source-qualified partial audit. The decision is PASS PARTIAL ONLY, with no required repair. This is not acceptance of a general solution, a new minimum, a novel theorem, exhaustive literature coverage, or a machine proof of mapping-class equality. The problem remains partial and stalled after five approaches out of five.

This review independently checked the complete frozen artifact, its six member pins, all three full corpus inputs, the exact-ID record and inherited report, all seven pinned source PDFs, the cited hypotheses, the five written mathematical arguments, and both the reported and independent arithmetic checks. The review date is 6 October 2026 UTC. The original freeze is preserved byte for byte; its historical independent-audit-pending fields are not silently edited. The separate exact acceptance records the review now completed.

The accepted author archive is POSITIVE_FACTORIZATION_2769_AUTHOR_SAFE_FREEZE.zip, 10,667 bytes, SHA-256 eedb7ba67020556df9d58af261cef3bb7d42ca6d9687a262cf0dc1958b0f75ac. Its external manifest is 1,357 bytes, SHA-256 a5ba4e6136eb6948565fe486c8037fd08df4f3a6bd2508bfd7fd16494d7ddec4. All six member hashes and byte counts agree with that manifest and the extracted working copies. Exact member pins are in ARTIFACT_VERIFICATION.json and EXACT_ACCEPTANCE.json.

## Original problem and admissible objects

K3 Problem 2.21 asks for a minimum length and realizing factorizations of the boundary multitwist in the boundary-pointwise mapping class group. The source excludes curves homotopic to a point or one boundary component; essential separating curves remain allowed. The author's admissible class correctly follows this convention. This reading was checked against the full book at printed pages 101–103, including independent visual inspection of pages 102–103. [K3]

Three scope distinctions are necessary and are retained in the accepted text.

1. With no boundary, the product on the right is the identity. The author's nonempty-word convention specifies the intended nontrivial-fibration problem. If empty words are allowed literally, the closed-case minimum is zero. The value m_2,0=7 is accepted only under the explicitly stated nonempty convention.
2. A separating essential curve need not have nonzero homology. Conversely, on a surface with several boundary components, a separating homologically essential curve may cap to a null-homotopic curve. Essentiality on the original surface, nonseparation, homological essentiality there, and essentiality after capping must remain distinct.
3. BMVHM's principal length function is a supremum over nonseparating factorizations. Its auxiliary function admits homologically essential separating curves. Neither convention may silently replace the full curve class or turn a maximum theorem into the requested minimum theorem. Its definition and Proposition 1 were checked directly. [BMVHM]

The source's existence-range and all-low-genus discussion is correctly presented as contextual literature reporting. The author has not supplied a new proof of the complete existence classification or an independent formula for every genus-one or genus-two boundary count. The acceptance does not add either claim.

## Mathematical review of the five approaches

### One-boundary torus abelianization

Proposition 1 is correct. Cutting a separating curve in a genus-one surface with one boundary yields a genus-zero side with either one boundary circle, hence a disk, or two, hence an annulus. Such a curve is respectively null-homotopic or boundary-parallel. Therefore every permissible factor is nonseparating.

The homomorphism to the integer abelianization assigns value one to every positive nonseparating twist and value twelve to the boundary twist. Applying it to any admissible factorization forces length twelve. The two-chain relation (T_a T_d)^6=T_boundary supplies twelve admissible positive factors, so both the lower bound and its realization are present. The specified abelianization values occur in BMVHM Proposition 1, genus-one part, printed page 1532. [BMVHM]

This is the familiar value m_1,1=12. The argument is not a general genus argument: it uses a special integer-valued abelianization and the fact that all admissible curves in this particular surface are nonseparating. The author expressly stops at this known subcase.

### Genus-two lower bound and realization

Proposition 2 is correct under its stated hypotheses. The external input is Baykur–Korkmaz Lemma 5, with the paper's conventions: a nontrivial, relatively minimal, genus-two Lefschetz fibration over S^2, with distinct critical values after perturbation. A pair (n,s) counts nonseparating and essential separating vanishing cycles. It is not a statement requiring a simply connected total space or a minimal total space. Relative minimality concerns exceptional spheres contained in fibers; it is weaker than minimality of the four-manifold. Sections 2.1–2.2, Lemma 5 and Theorem 7 were inspected. [BK]

For an independent algebraic check, write l=n+s with n,s nonnegative integers. If 1<=l<=6, then l<=n+2s<=2l<=12. The congruence n+2s=0 mod 10 forces n+2s=10. Therefore s=10-l and n=2l-10. Substitution into 2n-s>=3 gives 5l-30>=3, impossible. The zero pair is excluded, in particular by n+7s>=20. At l=7 the same congruence yields (n,s)=(4,3), which satisfies all three inequalities. This proves the lower bound and equality type; the inequalities alone do not prove realization.

The realization is the separate, explicit seven-factor one-boundary relation in BK Theorem 7, with four nonseparating and three separating factors. It is a boundary-twist relation before capping, not a word merely assumed to lift from the closed group. The audit accepts that published theorem as an external mathematical input; it does not claim a formal independent certification of every geometric move in its construction. [BK]

Capping the sole boundary preserves admissibility here: a curve that capped to a disk boundary would originally bound either a disk without the capped disk or an annulus containing it. Both are prohibited. Thus every admissible one-boundary factorization gives a relatively minimal capped fibration, allowing the lower bound to apply. Capping the published seven-factor relation gives a closed identity factorization. Hence m_2,1=7 and the nonempty m_2,0=7 are correctly recovered.

The one-boundary argument must not be generalized to an arbitrary number of boundaries without checking capped curves. A planar component enclosing multiple original boundaries can cap to a disk. No such invalid generalization is made in the accepted proof.

### Euler characteristic and Betti numbers

Proposition 3 is correct. Let b denote the number of pencil base points or boundary circles, and write beta_i for the Betti numbers in this audit to keep that integer distinct from beta_2. For the blown-up fibration Y over S^2, each positive nodal critical point adds one to the smooth-bundle Euler characteristic, so

    e(Y)=4-4g+l.

Blowing up b distinct base points gives e(Y)=e(X)+b, beta_1(Y)=beta_1(X), and beta_2(Y)=beta_2(X)+b. For a closed connected oriented four-manifold, Poincare duality gives e(X)=2-2 beta_1(X)+beta_2(X). Consequently

    l=e(X)+4g-4+b
     =beta_2(X)-2 beta_1(X)+4g-2+b,
    beta_2(Y)=l-4g+2+2 beta_1(Y).

All signs and constants agree with the author text. The symbol b_2 in that text is the second Betti number, not a square of the boundary count. The four-manifold assumptions are essential for the displayed Poincare-duality formula. Coincident critical values may be separated by perturbation; length counts critical points/nodes, with multiplicity, rather than unqualified distinct singular fibers.

For fixed g and b, minimizing length is exactly minimizing beta_2(X)-2 beta_1(X), or e(X). It coincides formally with minimizing beta_2 only after fixing beta_1, or after an additional theorem that controls the optimizing family. The note correctly makes an objective-function qualification without asserting that two realized minima differ. It supplies neither a sharp geography bound nor a corresponding construction for the remaining cases.

### Homology false positive and mapping-class kernel

Proposition 4 is correct for every g>=2 and b>=0. Embed a one-holed torus with boundary gamma so that the complementary surface has genus g-1. Both sides have positive genus, making gamma essential and nonperipheral. Choose curves a,d meeting once within that torus. They are nonseparating in the full surface because cutting either does not disconnect the torus, which remains attached to its connected complement.

The two-chain relation gives W=(T_a T_d)^6=T_gamma. This is a positive word of twelve permissible twists. In the displayed homology basis,

    A B = [[0,1],[-1,1]],
    (A B)^3=-I,
    (A B)^6=I.

The complementary homology summand is fixed. Equivalently, the separating twist has trivial action on closed-surface integral homology. Boundary twists also have trivial action there. Thus the homological images of W and Delta agree.

Equality of mapping classes fails. A closed essential curve x can be formed by joining suitable arcs on the two positive-genus sides, in minimal position with gamma. Its geometric intersection with gamma is positive. A single twist satisfies i(T_gamma(x),x)=i(gamma,x)^2>0, whereas every boundary twist fixes every closed-curve isotopy class. Hence W(x) differs from Delta(x). This argument also proves W is nontrivial when b=0. The actual word is an interior separating twist; it is not the desired boundary multitwist.

This distinguishes three tests. Equality in the original boundary mapping class group implies equality after capping, which implies equality of symplectic matrices. In general neither implication is reversible. In genus at least two, the separating twist lies in the kernel of the closed homology representation, but is nontrivial in the capped mapping class group. When b>0, a boundary twist is nontrivial before capping and becomes trivial afterward, separately demonstrating a capping kernel. Lifting a closed identity to the prescribed single boundary twists therefore requires actual lift data and the correct boundary exponents. A matrix certificate supplies none of them.

A finite search using bounded curve coordinates cannot exclude all shorter words unless a completeness theorem covers every such factorization, possibly after specified equivalences. Hurwitz moves and simultaneous conjugation preserve length and organize words, but do not by themselves prove that a chosen bounded search contains every relevant class. No exhaustive search or completeness theorem is claimed here.

### Restricted monodromy and direction of inequalities

The set-theoretic deduction is correct. If H is a restricted collection of admissible words and H is contained in F, then min length(F)<=min length(H) whenever both minima exist. A construction in H gives an upper bound for F. A lower bound valid only in H does not constrain all of F in the needed direction. If H is empty, its nonexistence cannot imply that F is empty.

Altunoz's introduction separates all hyperelliptic fibrations from those on complex surfaces, and records N_3=12 for the nontrivial genus-three hyperelliptic sphere-base family. The author uses it only at that restricted scope. It does not settle the unrestricted genus-three minimum or produce a one-boundary lift. The relevant definitions and introductory statements were checked in the published article. [Alt]

Restrictions involving hyperellipticity, holomorphicity, simple connectivity, fixed Betti numbers, or extension over one handlebody change the set being minimized. A general reduction theorem would be needed to transfer restricted minimality to the unrestricted problem. The fifth approach supplies no such theorem, and the author explicitly identifies this gap.

## Recent manuscripts and literature limits

The 5 October 2026 version of Huang's arXiv:2602.20451 identifies three already known genus-two type-(4,3) factorizations up to the corresponding fibration isomorphism. The introduction and Theorem 1.1 were inspected. This does not classify all such factorizations, establish uniqueness of every minimal fibration, or solve higher-genus minimum lengths. The arXiv version date and scope were independently confirmed on its current public record. [Huang]

Baykur–Hirose arXiv:2610.05537v1, dated 4 October 2026, imposes monodromy extending over a fixed handlebody. Its Theorem 1 allows positive critical-point count precisely when the fiber genus is at least three and the base genus is at least two. Thus its one-critical-point existence statement is outside the sphere-base problem. Its exclusion within the handlebody class does not exclude ordinary sphere-base fibrations. The abstract, introduction and theorem were inspected, and the current arXiv date and scope confirmed. [BH]

Both are manuscript claims at the stated versions. This review does not certify their complete proofs. Stipsicz's older Theorem 1.1 provides a non-sharp lower bound on nonseparating vanishing cycles for nontrivial relatively minimal sphere-base fibrations, in the paper's genus-at-least-two setting. It is context only and is not used to assert a new optimum. [Sti]

The literature pass was bounded. No comprehensive negative theorem about all later or unindexed research is claimed. The justified conclusion is that the supplied note does not solve the general problem and that the checked new manuscripts do not change that result.

## Exact corpus and inherited-work verification

All bytes of catalog.json, problems.json and research_results.json were read and their SHA-256 hashes independently recomputed. Their byte counts are 21,735,099, 68,931,837 and 80,334,822 respectively. All match the author pins. The exact catalog ID is the string "2769"; the exact problem ID is the integer 2769. Each has one match, and the catalog identifies rank 909 and problem number KP-2.21.

The full 17-field problem record, including its complete background, was used. The statement is 272 UTF-8 bytes and hashes to 8bed6f86416cac76b1793dbbe1c9a6eb0f5e714b24f9136b0c894b5ccc27bac3. There is no KP-2.21 key in the reports map. Applying the specified reports.get(problem_number,{}) gives the empty inherited report object; this is not a substantive proof omitted by a truncation.

The exact mandated encoding json.dumps([complete_record, reports.get(problem_number,{})], sort_keys=True), with the Python defaults for separators and ensure_ascii, has 11,010 bytes and SHA-256 698a4d641cee060382eeaddd34a2d776e06f1d9232bc3a0f9cea2969b0a09c1e. This matches both the expected pair hash and the catalog review hash. The author's stored pretty-printed pair is a different byte representation, 11,220 bytes, SHA-256 1ec3203695d96d212e37e4842d6751ea99e339e9a4b03743264afb5f31578d27, and parses to exactly the same complete pair. The two byte pins must not be conflated.

The full inherited background was inspected. It contains source exposition, references and dated literature triage, but no inherited substantive mathematical proof or computation to continue. The prior-work gate passes at that scope. These records are not included in the audit package; only public verification metadata is included.

## Source artifact and retrieval verification

All seven local source PDFs have the exact claimed byte counts and hashes. Independent PDF text extraction was performed from the pinned bytes rather than relying exclusively on the author's text files. Poppler emitted font/graphics warnings on some inputs, but completed extraction; the relevant book pages were independently rendered and visually inspected. No source PDF, extracted source text or rendered source image is included in any safe output.

Fresh direct retrieval on 6 October 2026 reproduced the identical bytes of K3, BMVHM, BK, Altunoz, Huang and Baykur–Hirose. The Stipsicz DOI resolved to the publisher's HTML landing page, not directly to a PDF. A publisher PDF found through public search was readable through the web tool, and its theorem statement was checked; direct byte retrieval of that URL returned HTTP 403. Therefore the seventh local source pin is verified, and its public content is corroborated, but a new matching PDF download is not claimed. SOURCE_VERIFICATION.json preserves this distinction.

The numeric UnsolvedMath page remained inaccessible through the web tool. Its public problem-number route returned HTTP 403 when opened, though a search result supplied corroborating indexed context. The exact identity rests on full pinned corpus reconstruction plus the actual K3 book, not on an assumed successful page download. Earlier timeout or browser-screenshot failures recorded by the author are historical reports, not actions independently witnessed by this reviewer.

A fresh read-only GitHub replay used the exact documented bounded searches: default-branch code query 2769 with topn 10, and all-state PR/commit queries for the ID, KP-2.21 and the positive-factorization phrase with topn 20. All returned zero matches without a tool error. This verifies the scoped negative result, not every branch, every unindexed object, or mathematical novelty.

## Arithmetic execution and what it establishes

The private author validation program was inspected before execution, then replayed under ordinary Python, -O and -OO. All three runs exited zero and exactly reproduced the three claimed structured results. Its explicit exception-based checks remain active under optimization. The delivery itself contains no executable, so these runs do not establish an executable-deliverable guarantee.

A separately written arithmetic program independently computed the matrix product and powers, enumerated all nonnegative genus-two pairs through length seven, and checked 37,128 integer substitutions in the Euler/Betti identities. It also passed under ordinary Python, -O and -OO. The finite substitutions are algebraic diagnostics, not assertions that every tested tuple is realized by a four-manifold. The formula was reviewed analytically above.

No execution decides mapping-class equality, classifies curve systems, verifies the full external literature, proves a new minimum, or supplies a formal proof certificate. The analytic arguments and correctly scoped cited theorems carry the mathematical conclusions.

## Artifact safety and release boundary

Every archive member was tested for its exact bytes, unique name, regular-file mode, relative path, UTF-8 text and non-executable status. The author archive contains exactly the six expected Markdown/JSON files and passes ZIP integrity testing. Full content inspection found authored exposition and public verification metadata only. There are no copied third-party documents, dataset contents, source PDFs, private sources, private personal data, credentials, private coordination files, or executable payloads in the safe outputs.

No repair is required and no replacement author freeze was created. The audit archive carries the unchanged six originals under original/ and the new authored review files under audit/. A smaller, separate exact-acceptance archive pins the same original target. Each archive has an external manifest, was independently extracted into a fresh replay directory, and is made read-only after final verification. Read-only filesystem mode and SHA-256 pins support immutability checking; they are not claimed to be cryptographic write-once storage.

No repository publication, commit, push, pull request, or external document sharing was performed by this review.

## Final acceptance boundary

The accepted result is a five-approach partial/stalled mathematical and source audit. The known values and elementary validation arguments are sound at their declared scopes. To resolve the original general problem, one still needs admissible realizing words in the exact boundary mapping class groups and matching lower bounds against every permitted shorter word for every remaining admitting pair. None of the five approaches discharges those obligations.

## Public references

- [K3] R. Inanc Baykur, Robion C. Kirby and Daniel Ruberman, K3 A New Problem List in Low-Dimensional Topology, author's preliminary version, Problem 2.21, printed pages 102–103. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [BMVHM] R. Inanc Baykur, Naoyuki Monden and Jeremy Van Horn-Morris, Positive factorizations of mapping classes, Algebraic and Geometric Topology 17 (2017), 1527–1555; definitions, Theorem A and Proposition 1. https://msp.org/agt/2017/17-3/agt-v17-n3-p06-p.pdf
- [BK] R. Inanc Baykur and Mustafa Korkmaz, Small Lefschetz fibrations and exotic 4-manifolds, Mathematische Annalen 367 (2017), 1333–1361; author manuscript Sections 2.1–2.2, Lemma 5, Section 3.2 and Theorem 7. https://arxiv.org/abs/1510.00089
- [Alt] Tulin Altunoz, The number of singular fibers in hyperelliptic Lefschetz fibrations, Journal of the Mathematical Society of Japan 72 (2020), 1309–1325; introduction and principal theorem statements. https://www.jstage.jst.go.jp/article/jmath/72/4/72_1309/_pdf
- [Huang] Evan Huang, Equivalent genus-2 factorizations of type (4, 3), arXiv:2602.20451v2, 5 October 2026; introduction and Theorem 1.1. https://arxiv.org/abs/2602.20451v2
- [BH] R. Inanc Baykur and Susumu Hirose, Lefschetz fibrations with handlebody monodromy, arXiv:2610.05537v1, 4 October 2026; abstract, introduction and Theorem 1. https://arxiv.org/abs/2610.05537v1
- [Sti] Andras I. Stipsicz, On the number of vanishing cycles in Lefschetz fibrations, Mathematical Research Letters 6 (1999), 449–456; Theorem 1.1 and genus convention in Section 2. https://doi.org/10.4310/MRL.1999.v6.n4.a7
