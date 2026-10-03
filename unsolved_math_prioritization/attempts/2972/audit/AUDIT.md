# Independent adversarial audit: KP-4.96 / problem 2972

Date: 2026-10-03 UTC. Audited outcome: **unsolved, five documented approach families**.

## Verdict

**PASS for publication as a scoped, unresolved investigation.** No blocking mathematical error, unsupported full-resolution claim, or improper promotion of a relative or higher-dimensional example was found. This is an independent AI-assisted review, not human peer review or certification of foundational gauge/Floer theory. It does not establish that the closed problem has no solution in the literature.

One nonblocking bibliographic improvement is recorded below. No change to the frozen public files is required for this verdict.

## Frozen input and reproducibility

All eight public files were read. The SHA-256 digest of the supplied `SHA256SUMS` is:

    b10de041b5391a59ef3dd32508b5da831978ef681326a20fbfd65d712898fe9a

Every one of its seven payload entries verified before and after the audit. The verifier was executed without modifying the payload; its output is byte-for-byte identical to `verification.json`: 11,393 assertions, all passing. The reproduced output is supplied as `reproduced_verification.json`.

A separate implementation, `independent_verify.py`, imports no code from the audited verifier. It performed 37,120 exact rational/exterior-algebra assertions. These include 21,060 affine-minimum tests, 288 unequal-endpoint boundary tests, 15,625 generic exterior-product torus tests, the half-turn checks, and 144 pullback checks with noncommuting matrices. Deliberately reversing the composition order fails in 132 of the latter examples. These controls strengthen the algebra check but do not prove any statement about all smooth manifolds or all symplectic forms.

`INPUT_MANIFEST.json` identifies all eight audited files by digest. `SHA256SUMS` in this audit directory covers this report and its supporting audit artifacts, and does not replace the payload's manifest.

## 1. Target identification and scope

The primary author-hosted K3 manuscript was checked at Problem 4.96, its adjacent remarks, the section introduction, and the later cross-reference in Problem 4.108. The problem sentence does not explicitly impose closedness. The packet correctly identifies that ambiguity, declares the closed interpretation it investigates, and handles the literal nonclosed reading separately. It does not falsely present an added hypothesis as a quotation. The later closed-manifold cross-reference supports the intended closed research direction. [K3 author manuscript](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

The exact closed target is correctly stated as nontransitivity of the class-preserving diffeomorphism action on the set of symplectic forms in a fixed positive-square class. Pulling a form back by the comparison diffeomorphism preserves both directions of the existence/nonexistence question. A symplectomorphism between two fixed-class forms necessarily preserves that class. On a connected closed manifold, a class-preserving diffeomorphism cannot reverse the symplectic orientation: integration of the class square would change sign despite its positive value. Restricting to orientation-preserving diffeomorphisms therefore loses no candidate equivalence.

The elementary noncompact example is valid. The radial map has radial derivative `(1+r^2)^(-3/2)` and tangential scale `(1+r^2)^(-1/2)`, and its inverse on the ball is `y/sqrt(1-|y|^2)`. Pulling back the standard form gives finite volume `pi^2/2`, whereas standard four-space has infinite volume. Both relevant characteristic/cohomology classes vanish by contractibility. Preservation of symplectic volume excludes every symplectomorphism. This proves only the literal nonclosed version, exactly as stated.

## 2. Canonical classes and Moser reduction

The imported canonical Spin-c statement matches Salamon's Corollary A and its proof. The argument is stronger than merely proving equality of first Chern classes modulo torsion: the positivity equality case forces the difference class itself to vanish. Changing homological orientation changes the sign of a Seiberg–Witten invariant but not nonvanishing; the two `b+ = 1` chambers agree because the symplectic classes agree. Thus the packet has not silently discarded a possible 2-torsion obstruction. The foundational Taubes input is expressly imported rather than claimed as a new proof. [Salamon, §§2.6–2.7 and Corollary A](https://arxiv.org/pdf/1211.2940v5)

Proposition 1 passes. Along a smooth fixed-class path, the derivative is exact and a fixed Hodge-theoretic right inverse supplies smoothly varying primitives. The vector-field equation has the correct sign, and compactness supplies the complete finite-time flow. The converse uses pullbacks by a smooth isotopy and the induced identity on real cohomology. Composition order in the orbit reduction is correct. Smooth path components, rather than arbitrary varying-class deformations, are the relevant objects.

Consequently, detecting multiple fixed-class path components is insufficient: a class-preserving mapping class can permute them. The packet never mistakes this weaker obstruction for distinct orbits under all diffeomorphisms.

## 3. Affine interpolation and local negative control

Proposition 2 passes, including both necessity and sufficiency. The wedge-square polynomial is correctly expanded. If `B > -sqrt(AC)`, its square-plus-positive-term decomposition is positive throughout the segment. If equality holds, the displayed interior time is a genuine zero. If strict failure occurs, the polynomial is negative there and must cross zero between that time and a positive endpoint. It is therefore legitimate to use nonpositivity at that selected time to disprove a wholly nondegenerate segment. The alternative test `B >= 0`, or `B < 0` and `AC > B^2`, is correct.

The common-taming corollary is correct. A kernel vector would contradict positivity on `(v,Jv)`, and convex combinations preserve the taming inequality. Cohomology constancy and closedness, not just pointwise nondegeneracy, are retained before invoking Moser.

Proposition 3 passes. The cutoff vector field is smooth, compactly supported, and preserves the full squared coordinate radius. Hence points in the inner ball remain there, where its time-one flow rotates the two y-coordinates by pi. Its derivative is the indicated diagonal map there; pullback negates both symplectic summands while preserving the four-dimensional orientation. The global flow is an isotopy, so its pullback preserves cohomology and the integral first Chern class. The two endpoints are symplectomorphic by construction but have a zero midpoint on an open set. This is a decisive counterexample to a proposed affine-path argument, not to uniqueness itself.

## 4. Torus family and periodicity

Proposition 4 passes. Translation invariance forces coefficients to depend only on the circle coordinate; the independent three-form coefficients in the closedness equation force each purely spatial coefficient to be constant. The wedge-square sign and all six period coordinates are correct.

For a fixed class, both the spatial vector and the three averages agree. The continuous nonzero function `a(t)·b` has one sign on the circle, determined by its nonzero integral. Thus the two endpoints have the same sign everywhere, and their straight segment remains nondegenerate. This covers negative as well as positive orientation relative to the displayed coordinate volume, because cohomology forces the same choice for both endpoints.

There is no global-periodicity gap: integrating a zero-mean periodic coefficient gives a periodic primitive, so the displayed one-form is globally defined on the torus. No unproved coordinate shear or nonperiodic diffeomorphism is used. Moser supplies the required global diffeomorphism on the compact manifold.

Hajduk–Walczak's Corollary 2.11 applies to forms invariant under a linear free circle action and gives isotopy to a constant-coefficient form. The present translation-invariant family satisfies that hypothesis; its fixed-class uniqueness conclusion is already covered. The packet appropriately makes no novelty claim. Its stronger explicit statement that this particular family is affine-convex has its own valid proof. [Hajduk–Walczak, Corollary 2.11](https://arxiv.org/pdf/math/0312465)

## 5. Pullbacks and restricted literature

Proposition 5 passes. For forms `omega_i = f_i^* omega`, the map `f_j^(-1) o f_i` has the required pullback relation. No homotopy, cohomology, or mapping-class assumption on the `f_i` is needed for this elementary fact.

The pinned Lin–Wu source explicitly constructs forms by powers of a diffeomorphism pulled back from one form. Its Theorem 1.2 proves non-isotopy, and its Remark 1.3 explicitly recalls uniqueness up to diffeomorphism for the fixed class. The packet's exclusion of this construction is sound independently of the difficult Dax-invariant proof. [Lin–Wu, Theorem 1.2 and §3](https://arxiv.org/abs/2507.14636v2)

Ning's Theorem 1.3 lives on a six-manifold obtained by multiplying an exotic four-manifold by a sphere; the base identification is a homeomorphism, whereas the smooth identification is of products. Its compared forms have different first Chern classes. Neither the dimension nor the closed four-dimensional smooth/class constraints can be recovered merely by restricting that product diffeomorphism. The packet correctly declines to infer a desuspension theorem. [Ning, Theorem 1.3 and §4](https://arxiv.org/abs/2505.09550v1)

The other source restrictions are accurately reported: Fine–He–Yao requires an invariant hypersymplectic triple with an effective circle action, while Li–Ning considers Kähler-type or holomorphically tamed subspaces with further manifold hypotheses. Those assumptions are not consequences of merely being cohomologous symplectic forms. [Fine–He–Yao, Theorem 1.2](https://arxiv.org/abs/2503.05272v2), [Li–Ning, Theorems 1.8–1.9](https://arxiv.org/abs/2607.18778v1)

### Nonblocking bibliographic refresh

Wu's current publication page records that the two-author Lin–Wu preprint was incorporated into the four-author paper *Dax invariants, light bulbs, and isotopies of symplectic structures*. Its current version is arXiv:2501.16083v5, dated 1 February 2026. Adding this cross-reference would improve currency; it does not invalidate the pinned source or change the audit verdict. The merged paper's abstract still describes isotopy/homotopy obstructions on irrational ruled surfaces. [Wu's publication page](https://weiweiwu-math.github.io/), [Lin–Wu–Xie–Zhang v5](https://arxiv.org/abs/2501.16083v5)

## 6. Relative Moser, boundary flux, and capping

Proposition 6 passes. Vanishing of the primitive on a collar makes the Moser vector field vanish there, not merely tangent to the boundary. Thus its flow exists on the compact manifold with boundary and extends smoothly by the identity over any compatible common cap. Absolute exactness alone would not provide this support condition, and the packet does not assume otherwise.

The `S^2 x D^2` example correctly exposes that distinction. The disk two-form difference is exact in absolute cohomology but has positive integral over a fiber disk. A primitive vanishing near the boundary would make that integral zero by Stokes. The product-volume difference is exactly the stated positive quantity, excluding every symplectomorphism, including ones that do not fix the boundary. For closed cohomologous forms the top-degree integrals agree, so identical capping cannot preserve both that volume difference and the global cohomology class. This example is not passed off as the Stein result.

Iida's version 2 explicitly distinguishes the closed problem from its normalized relative problem. Theorem 1.8 concerns exact forms on a compact manifold with boundary, a strict boundary contactomorphism, equal first Chern classes, equal volumes, and inequivalence even after reparametrization. The boundary matching is unmarked: it need not be the restriction of the Chern-matching diffeomorphism. Theorem 7.7 uses oriented characteristic circles and a cap-extension argument; Theorem 9.1 additionally uses the Floer input. Remark 10.2 explains the boundary-extension obstruction. The packet accurately treats these as reported results, not as a certified new closed counterexample or as foundations independently proved here. [Iida, §§1, 7, 9–10](https://arxiv.org/abs/2608.09361v2)

A closed construction would still need compatible symplectic gluings, a single smooth identification matching the global classes, and an obstruction that excludes symplectomorphisms moving the chosen cap. The packet correctly lists each missing condition.

## 7. Claim hygiene and limits

The five logged items are distinct mathematical approach families: gauge-theoretic separation, affine interpolation, a symmetric torus family, mapping classes/stabilization, and relative capping. Each records a specific mechanism, substantive calculation or source-based test, an outcome, and a remaining gap. Their count is defensible as five attempts, not as five solutions or a quantitative measure of progress. The percentage estimates are explicitly subjective and play no mathematical role.

The README, proof, log, and machine-readable status consistently say unresolved; none claims novelty, human peer review, or a complete theorem. The original pending-review fields are historical statements in the frozen snapshot; this separate audit records the later result without rewriting that snapshot.

The reported prior repository checks were not repeated in this audit, which did not contact or mutate the repository. They remain bounded provenance claims of the investigation rather than an independently established absence of all prior work. Likewise, the audit checked the stated source uses, not every foundational dependency or every possible later paper. No external source text or source PDF is redistributed in these audit artifacts.

**Final decision:** accept the frozen package as an honest unresolved five-attempt investigation with valid elementary partial results and accurately gated literature. Retain the closed-scope qualifier. Do not mark the underlying problem solved.
