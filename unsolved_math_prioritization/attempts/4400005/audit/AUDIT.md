# Independent adversarial audit: rank 653, ID 4400005

## Verdict

**PASS at the literature-deduction level.** The frozen packet supplies a correct affirmative answer under the standard interpretation of the problem: a nonempty closed Riemannian manifold of dimension at least two with constant strictly negative sectional curvature, with the unit-speed geodesic flow on its unit tangent bundle. No blocking mathematical gap was identified in the passage from the cited specification and universality results to the asserted measure. The stronger variable-negative-curvature conclusion is supported by the same stated specification input.

The appropriate disposition is **already_solved / consequence of established literature**, not a new theorem, priority claim, or proof-by-computation. The direct Quas-Soo corollary covers surfaces. The separate all-dimensional deduction is necessary and is valid. This audit does not assert that an original all-dimensional corollary with precisely the Pingree wording was located.

Three nonblocking source cautions are recorded below: typographical slips in the inspected Burguet manuscript, an upstream Hochman erratum that does not affect the needed theorem, and the distinction between inspecting a dependency/application and re-proving all classical literature from foundations. They do not require changing the mathematical disposition.

## Exact input binding and independence

The audit binds exactly to `AUTHOR_PACKET.zip`, **16,393 bytes**, SHA-256:

`66c2af685b3e86b88f78659db26aa60698415e7cab966bc3fa737d4794879bcf`

All eight ZIP entries agree byte-for-byte with the frozen file manifest and the adjacent packet copies. `input_binding.json` contains the eight individual hashes and sizes. No author file was edited. No remote write, repository mutation, outreach, or additional research helper was used. Newly obtained third-party source files and rendered pages were retained outside this deliverable. The deliverable contains authored analysis, original replay code, and verification metadata only.

`replay_audit.py` accepts a portable path to the frozen ZIP, checks the whole archive and every file against embedded exact constants, then executes the reviewed frozen verifier in a temporary directory. The verifier output must equal both frozen `controls.json` and the controls embedded in frozen `result.json`. The script separately runs additional adversarial controls.

## Target fidelity

The public November 22, 2010 Pingree PDF, printed page 3, was independently retrieved, read, and visually inspected. The ID's pinned statement matches Ledrappier item 1. In particular:

- The question is existence of a probability invariant at time one but not under the entire flow.
- Its geometric wording is a manifold, not merely a surface.
- It imposes no positive-entropy, smooth-density, maximal-entropy, or full-support condition.
- The adjacent explanatory note already identifies realization of an entropy-zero system without a square root as a sufficient strategy.
- Measures belong on the unit tangent bundle. Referring informally to a geodesic flow “on the manifold” does not turn the target into a flow on the base manifold itself.

The packet correctly preserves the specified metric and time unit. Its disconnected-case reduction is valid: choose one connected component and extend the probability by zero. A component is compact; its unit tangent bundle is connected when the base is connected and dimension is at least two. No orientation assumption is necessary.

The exclusions are important conventions rather than additional substantive restrictions: the full geodesic flow on every unit vector presupposes completeness, as supplied by a closed manifold. Dimension one should not be included using a vacuous quantification over sectional curvatures: an irrational-length circle would then furnish a counterexample to the proposed generalization. The packet explicitly excludes this unintended reading.

## Dependency audit

### A. Specification and geometry

Thompson, arXiv:0807.2123v1, Definition 1.5, p. 4, and section 4.3, p. 20, were independently downloaded and visually checked. The bytes match the packet's reported public PDF hash. The definition uses prescribed integer intervals separated by a uniform lower gap and does not require an integer-periodic tracing point. Section 4.3 explicitly treats all compact connected negatively curved Riemannian manifolds and their nonzero sampled geodesic maps. Its underlying citations are Katok-Hasselblatt 17.6.2 and 18.3.6 for Anosov/mixing, and Bowen's flow specification, presented as 18.3.13 in that book.

Tian, section 7.3, pp. 515-516, was checked in the provided published PDF/text. It repeats the time-map statement and the all-dimensional negatively curved case, explicitly distinguishing the nonperiodic version from Bowen's stronger discrete version. This corroboration shares Thompson's dependency; it is not an independent geometric proof.

An additional primary exposition by Hasselblatt, *Shadowing: The Anosov-Bowen approach to hyperbolicity*, April 8, 2022, PDF pp. 16-19, was inspected through the public web PDF. It defines flow tracing at prescribed start times, states strong specification for topologically mixing compact locally maximal hyperbolic sets, and explains the mixing/local-product/closing argument. This rules out confusing this input with gluing that permits uncontrolled accumulated timing changes. Local PDF download returned HTTP 403; no local hash is claimed for this supplementary source.

The application is then direct. Put F = g_1. Integer times are allowed real flow times. A sufficiently large integer lower bound on the transition time converts the flow property into the required discrete property. Alternatively, Thompson states this conversion explicitly. Passing between local orbit origins and absolute-time orbit origins uses F's invertibility. A common integer translation handles negative starting times. A constant positive gap function is sublinear.

Compact negative curvature is essential to the cited geometry. Anosov alone without mixing would not justify this invocation; the packet checks the mixing assertion for geodesic flows. A constant-roof suspension illustrates why one cannot replace this geometric input by a generic suspension claim.

### B. Universality

Burguet, arXiv:1901.00666v1, pp. 1-3 and sections 2-3, was checked. Theorem 1.2 has the required almost-Borel formulation for aperiodic Borel sources; the target is a compact metric homeomorphism of finite entropy. There is no small-boundary or asymptotic-expansiveness assumption. Its proof chain is Proposition 3.1, Lemmas 3.2-3.3, and section 3.4; these use admissible symbolic specifications, Hochman's mixing-SFT embedding, tower markers, and a summable-exception limiting map. In particular the result is an injection on a full set, not merely a factor map.

The internal chain was traced through the relevant definitions and proofs. Its auxiliary classical inputs include the Ornstein-Weiss recurrence formula, a Borel tower lemma, and Weiss's countable-alphabet representation. These remain literature inputs, not computer-certified lemmas. No hypothesis introduced in that chain requires the target geodesic map to be expansive or to have only countably many periodic points.

Hochman's arXiv:1008.3549v2, Theorem 1.5, and the author's 2013 erratum were independently retrieved. The erratum removes a claim about synchronized subshifts in Theorems 1.6-1.7; the mixing-SFT result used here remains unchanged. It therefore does not obstruct Burguet's application.

For additional corroboration, Chandgotia-Meyerovitch, arXiv:1903.05716v2, Theorem 1.5 (p. 3), independently restates and recovers the relevant universality theorem. Chandgotia's 2022 public BIRS note also identifies that alternative proof. These are supplementary checks, not a replacement argument inserted into the frozen packet.

### C. Direct surface corollary

The independently downloaded published Quas-Soo article matches the packet hash. Corollary 4, p. 430, and its proof on pp. 445-446 were checked, together with Theorem 1 and the relevant symbolic-coding discussion. The result concerns compact negatively curved surfaces, including variable curvature. Its proof addresses the coding injectivity issue using recurring marker words; it does not infer that every finite-to-one factor preserves the desired isomorphism. The source's surrounding question mentions the absence of rational-period geodesics, but Corollary 4 itself does not impose that restriction.

This validates the direct surface attribution. It is not used to infer the higher-dimensional result.

## Independent reconstruction of the deduction

### 1. Target entropy and regularity

F is a smooth invertible map of a compact finite-dimensional manifold X = T^1N. A smooth metric makes F globally Lipschitz; choose K >= max(1, Lip(F)). If two points start within epsilon K^{-(n-1)}, their first n iterates remain epsilon-close. The polynomial small-scale covering bound in dimension dim X bounds orbit covering growth by an exponential, so h_top(F) is finite.

Positivity can be obtained without importing a normalization-sensitive entropy formula. Pick x_0 != x_1 with separation delta and use a tracing error smaller than delta/3. At regularly spaced times j q, with q larger than the specification lower gap, prescribe either x_0 or x_1 independently. Different binary words yield separated tracing points. Thus h_top(F) >= log(2)/q > 0. If intervals must have positive length or start at 1, lengthen them and shift the schedule; neither change affects exponential growth. This confirms the strict entropy inequality needed later.

### 2. Odometer source

Let Z_2 be the compact inverse limit of the groups of residues modulo 2^k. Addition by one is an invertible continuous transformation S preserving normalized Haar measure m.

Each finite quotient is one cycle. Any invariant probability assigns equal mass to all its residue cylinders, so uniqueness follows because these cylinders generate the Borel sets. Consequently m is ergodic. Cylinder masses tend to zero, hence m has no atoms. No nonzero integer is divisible by every 2^k, so S has no periodic points. The 2-adic metric is translation-invariant; at fixed accuracy, finitely many residue cylinders control all times simultaneously. Therefore topological entropy and the entropy of m vanish, and the Borel entropy is zero. This source is genuinely aperiodic despite all its finite quotients being periodic.

This also explains why Burguet's topological subshift theorem is not the appropriate direct input: the odometer need not be expansive. The almost-Borel theorem actually invoked has no such restriction on the source.

### 3. Square-root obstruction

Let f be +1 on the even residue cylinder and -1 on the odd cylinder. Then f composed with S equals -f. If a measure-preserving automorphism R satisfies R^2 = S modulo null sets, it commutes with S modulo null sets. Hence h = f composed with R is another real -1 eigenfunction.

For any such h, h/f is S-invariant. Ergodicity makes it constant almost everywhere. Thus f composed with R = a f for a real number a. Preservation of the L^2 norm gives a in {+1,-1}. Applying R twice yields f composed with R^2 = f, whereas R^2 = S demands its value be -f. Since f is nonzero, this is impossible.

All null-set identities can be made simultaneous on a countable invariant intersection. The use of real-valued functions is decisive: a complex linear square root of an eigenvalue is not automatically the Koopman operator of a measurable transformation. Ergodicity is also decisive; two disjoint identical even cycles can possess a square root that exchanges components. The independent controls test both dangers.

There is no claim that S has no roots of any order. Odd integers are invertible in Z_2 and give translation roots. The conclusion specifically needs the absent square root.

### 4. Measurable embedding and the transported probability

All inputs to the embedding theorem now match: compact metric target, invertibility, finite entropy, the correct gap property, an aperiodic standard Borel source, and 0 < h_top(F). It yields an equivariant Borel injection Psi on an S-invariant full set Z_0. In particular m(Z_0)=1.

The Borel injective-image theorem makes A = Psi(Z_0) Borel and the inverse on A Borel. The probability mu = Psi_*m is therefore defined on X, invariant under F, nonatomic, ergodic for F, and of entropy zero. These are isomorphism properties; no factor-only inference is being used.

For a fully explicit treatment of the half-time domain issue, suppose H = g_(1/2) preserves mu and define A' = intersection over n in Z of H^n(A). It is a Borel H-invariant conull subset of A. Its preimage B under Psi is conull and S-invariant. The map R = Psi^{-1} composed with H composed with Psi is an invertible m-preserving transformation of B. Since H^2 = F, equivariance gives R^2 = S on B. This contradicts the preceding obstruction. Thus H_*mu differs from mu, which is stronger than merely failing full-flow invariance.

No continuity of Psi, closedness of A, or H-invariance of the original image A is needed.

## Adversarial alternatives and boundary checks

1. **Rational closed orbits:** the simple atomic construction is correct if a rational length exists, but this premise is not guaranteed for the fixed metric. It is correctly treated as a conditional route, not the proof.
2. **Flow averaging:** averaging an F-invariant probability over one time unit produces a flow-invariant probability. It need not reproduce the original probability. This operation cannot prove the target false.
3. **Finite-to-one coding:** pushforward through a noninjective factor can erase a root obstruction. The successful all-dimensional route avoids that inference.
4. **Periodic versus nonperiodic specification:** F may have no periodic points for an appropriate metric scaling, although the real flow has closed orbits. Requiring a periodic F-tracer would be unjustified. The invoked definition does not do so.
5. **Entropy and support:** no positive-entropy or full-support condition is imposed on the target probability; zero entropy is sufficient and deliberate.
6. **Integer invariance versus flow invariance:** invertibility turns invariance under F into invariance under all integer iterates, but not under all real times. The argument does not confuse these groups.
7. **Noncompact or curvature-zero extensions:** these are not covered. Likewise the neighboring suspension question is not disposed of by this audit.

## Nonblocking manuscript cautions

- On Burguet v1 p. 2, the displayed gap index is reversed relative to the standard almost-weak-specification convention. The intended hypothesis is the gap between successive prescribed intervals. The packet uses that standard meaning, consistent with its cited source's internal specifications and with Quas-Soo's explicit gap definition. It would be misleading to reproduce the misindexed display as a new alternative property.
- On Burguet v1 p. 14, the stated bound P_k/N_k < 2^{-(k+1)} only gives 6 P_k/N_k < 3 times 2^{-k}, not the displayed 2^{-k}. The corrected bound is still summable, which is all the Borel-Cantelli argument needs. Alternatively the chosen ratios can be tightened. This arithmetic slip does not change the theorem application.
- The manuscript's language defining a Borel system contains an evident “invertible”/“measurable” wording slip. The particular source used here is a homeomorphism, satisfying all intended measurability requirements in any case.
- The upstream Hochman erratum should be listed in an expanded bibliography so future readers do not have to rediscover its irrelevance. Its existence does not contradict the packet's narrower statement that no correction negating the used conclusions was located.

These are source-reading cautions, not new unsolved gaps in the authored deduction. No statement of the audit should imply that these manuscript slips were checked against a fully retrieved final publisher PDF; the inspected full Burguet text is arXiv v1, as the packet says.

## Replay and verification limits

The frozen verifier reproduces **754 assertions**, including 46,233 permutation enumerations, with exact equality to both frozen result files. Independent controls pass **1,533 assertions**, enumerate **409,113 permutations** through cycle length 9, test inverse-limit compatibility of odd roots through modulus 262,144, test the nonergodic counterexample, and check **400 rational-circle cases**. Exact rational/integer arithmetic is used.

These checks test algebraic failure modes and integrity, not an infinite-dimensional embedding theorem or an actual numerical geodesic measure. The infinite odometer proof and the measurable-domain argument above are necessary independent of the finite tests.

The essential cited statement/application chain and its relevant proof structure were inspected. This is not a formal proof assistant certificate or a new line-by-line re-proof of every foundational result cited recursively. In particular, the complete original Katok-Hasselblatt chapters and Bowen 1972 article were not independently retrieved in full; their precise role was checked through Thompson, Tian, and Hasselblatt's primary exposition. The DOI/JSTOR access attempts yielded no inspectable Bowen full text. These access limits are recorded rather than hidden.

No unresolved target-level mathematical gap remains **conditional on the established specification and universality theorems**. The packet already presents itself in exactly that literature-dependent form. The result can be accepted as an affirmative literature resolution without a novelty claim.
