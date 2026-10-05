# Independent audit: consistent conical bicombings

Problem 30004730; source identifier OWR-8415335-002; catalog rank 783.

## Verdict

**PASS for the explicitly scoped partial results and source correction. The original existence question is unresolved in this investigation.** All five approaches remain partial. No mathematical change to the frozen author report is required by this audit. This is an independent mathematical/code review, not formal proof certification, a novelty claim, a publication acceptance, or an exhaustive literature-status certificate.

The audit is bound to the 19,194-byte author ZIP with SHA-256 `4e7599d44d08aa72106fd94b91d12faea77d4b4e2c80dad1c6dbb87277f38334`, and its manifest SHA-256 `327f8e3edf79b1eb762241e6636bdbdfc092f839c9270aaa8605260c7c2d7f6f`. Every frozen member was checked, and the unmodified author verifier passed. The original archive and its seven files have not been edited.

## 1. Source identity, quantifiers, and literature boundary

The source is Basso's contribution in the [Oberwolfach report](https://ems.press/content/serial-article-files/46908), printed pages 1696-1697. Its question concerns every metric space carrying a conical bicombing; no completeness assumption is included. Both pages were visually inspected. Its proper-space result only controls pairs of equal-length selected geodesics. The next page explicitly distinguishes this from conicality. Thus the frozen report correctly rejects the stronger proper-space interpretation in the dataset assessment.

[Basso's 2024 article](https://ems.press/content/serial-article-files/47668), Theorem 1.4, likewise supplies a consistent bicombing with straight geodesics and convex comparison for equal endpoint distances. Its general conicality is not established. Lemma 5.2 and the following direct-iteration paragraph contain the finite-string mechanism; Remark 5.3 identifies convergence of the full mesh sequence as an outstanding step. These attributions were checked in context, including the length-dependent selection used in the proof. They support the report's refusal to claim originality for that mechanism.

[Basso-Krifka-Soultanis](https://link.springer.com/content/pdf/10.1007/s00208-024-02905-w.pdf), Question 7.1, expressly poses the complete-space problem as open in that paper. The following discussion presents their example as a possible test space, not an established counterexample. The definitions and question on printed page 5879 were visually inspected.

[Descombes-Lang](https://arxiv.org/abs/1404.5051), Theorems 1.1-1.2, have the exact qualifications recorded in the report: properness yields a convex bicombing, and finite combinatorial dimension on bounded subsets supplies consistency, reversal and uniqueness of a convex bicombing. Finite topological dimension is not a substitute. [Basso-Miesch](https://arxiv.org/abs/1604.04163), Proposition 1.3, gives reversibility under completeness. Its v4 revision date and same-mathematical-content statement agree with the frozen citation.

The [January 2025 author problem list](https://www.researchgate.net/publication/383463472_Some_questions_from_metric_geometry_and_functional_analysis), Section 1.1, was independently inspected as author-uploaded web text and continues to pose the unrestricted problem. [Danielski's versioned HTML](https://arxiv.org/html/2503.06673v2), Remark III and Remark 2.5, preserves the dimension and equal-length distinctions. Its page simultaneously displays the arXiv v2 header dated 11 May 2025 and an internal manuscript date of 24 August 2026; the safe precise reference is the versioned URL/header, without resolving that discrepancy. Targeted 2025-2026 searches and a check of [Naor's factorization paper](https://arxiv.org/html/2609.07564v2) located no general resolution. These are bounded checks only.

All five principal PDFs were freshly downloaded from their stated public sources and matched the author's copies byte for byte. Their hashes, sizes and actual inspection scope are in `source_audit.json`. The live problem page remained unavailable; its failure is not treated as a successful page inspection.

## 2. Universal proof audit

### 2.1 Definitions and consistency convention

All endpoint, time and subinterval quantifiers in Section 1 are appropriate. Reversibility plus initial-segment compatibility implies terminal compatibility by reversing, and then arbitrary oriented subinterval compatibility by restricting twice. The report proves the stronger reversible convention whenever asserting consistency. Constant paths cover coincident endpoints and degenerate subintervals. Conicality plus oriented consistency gives convexity by applying the endpoint estimate on the two corresponding restricted segments.

### 2.2 Tent bicombing and dyadic obstruction

The domain is the closed upper half-plane with the supremum metric. The formula remains in that domain. Each coordinate is L-Lipschitz in time, where L is the endpoint distance. The endpoint triangle inequality upgrades this to exact constant speed, including the L=0 case. For endpoint perturbations, both the affine height and the tent height change by at most the prescribed conical bound; taking their maximum preserves that bound. Symmetry under exchanging endpoints proves reversal.

The selected quarter points are also the points obtained by recursive midpoint insertion from the outer endpoints. Their intervening newly selected midpoint has height 1/2, while the outer selected midpoint has height 1. All old dyadic values persist under refinement. Completeness gives the dyadic extension but cannot remove the defect. The example therefore refutes an automatic construction, not existence of a consistent bicombing on this space, which has its linear one.

### 2.3 Finite harmonic midpoint strings

Fix arbitrary endpoints and a finite integer n>=2. The product metric with weights i(n-i) is complete because it is equivalent to the ordinary finite maximum product metric. Endpoint differences vanish. The exact weight identity makes the averaging map a contraction with coefficient 1-1/floor(n^2/4). The coefficient is 0 for n=2; the map is then constant. The stated a posteriori error bound follows by summing successive-step distances, with the explicitly supplied convention at k=0.

The finite maximum principle applies to distances from either endpoint and to the distances between strings. The two endpoint bounds must both be equalities because their sum is at least the endpoint distance. Midpoint identities equate consecutive edge lengths; their common value is L/n. The full pairwise distance statement follows by combining the path upper bound and the endpoint-distance lower bound. Concatenation of the original constant-speed interpolants is L-Lipschitz and joins endpoints distance L apart, so it is a geodesic. Interpolating the two adjacent-node conical bounds proves the exact endpoint conical inequality.

Reversal of strings uses symmetric input midpoints, and reversal of interpolants uses the original reversible bicombing. Neither is silently assumed for the nonreversible input case. Every contiguous block satisfies the same fixed-point equations with its own endpoints. Uniqueness identifies it with the smaller-mesh string. This proves the cross-mesh identity, including one-edge blocks via the definition sigma^1=sigma. It does not identify the smaller mesh with the larger mesh on the right-hand side.

The worked model has interior height 2/n. Direct substitution checks the boundary-adjacent equations as well as the interior ones. Its interpolant has the asserted piecewise-linear height. The 2-mesh and 4-mesh have different midpoint heights. Existence and convergence of iterates for each fixed n do not supply convergence as n increases.

### 2.4 Whole-sequence criterion and completeness limits

The condition is pointwise convergence for every fixed endpoint pair and every time, along all integer meshes. No countability or separability hypothesis is needed. Equicontinuity in time controls the moving grid times. If s<t, the restricted mesh size tends to infinity. The conical estimate controls replacement of its moving endpoints by their fixed limits. Whole-sequence convergence then applies along those restricted mesh sizes, proving consistency. For s=t both sides are the same constant path.

Convergence at rational times also suffices: a finite rational time net and the common L-Lipschitz bound make the whole family uniformly Cauchy for a fixed endpoint pair; completeness puts the limit in X. A mere subsequence is not enough for this argument. The contraction coefficients approach 1, and their error estimates concern iteration at fixed mesh only. An O(1/n) increment estimate is not a cross-mesh Cauchy proof.

The Hilbert-product example correctly computes the entire metric midpoint set, and distinct orthonormal basis vectors have separation sqrt(2). This shows failure of compactness of possible midpoints in a complete space, without asserting that the actual mesh sequence wanders through those points or fails to converge. Properness does restore compactness, but not the missing compatible indexing argument.

### 2.5 Medial midpoint sufficient condition

The midpoint assumption includes exact distances to both inputs and consequently idempotence. Balanced iteration of a commutative medial operation gives permutation-invariant means: the interchange law permits a swap across the two halves; permutations within each half move that swap to any desired pair. Duplication invariance follows by rearranging into identical halves and using idempotence.

For dyadic parameters, the average-distance estimate implies the conical bound and the upper distance bound between adjacent parameters. The endpoint triangle inequality makes those upper bounds exact. Completeness supplies the extension. For consistency, choose a common denominator for the two inner parameters, flatten equal-depth balanced means, and count the endpoint leaves. Continuity in endpoints and time extends the resulting identity from dyadic triples to all triples. The explicit tent midpoint violates mediality by 1/4, so this extra condition has not been inferred from the hypotheses of the open problem.

### 2.6 Completion and elementary subclasses

The uniform endpoint conical estimate makes completion-extension independent of Cauchy representatives and jointly continuous in endpoints. All geodesic identities pass to the limit; existing consistency passes after controlling the changing inner endpoints. This extends the given bicombing. It does not imply that a replacement bicombing constructed on the completion preserves the original subset. The uniquely geodesic and linearly convex subclasses are correct, including incomplete convex subsets with their already-defined linear paths.

## 3. Independent computational evidence

The fresh `independent_checks.py` imports no author code. Its conical grid uses scaled integer coordinates rather than the author's Fraction evaluation. It independently reproduces:

- 253,125 conical inequalities, 5,625 geodesic equalities and 1,125 reversal identities;
- the dyadic inconsistency and mediality defects, and failure of mesh-point preservation;
- 4,950 weight/coefficient checks, 12,524 fixed-string distances, 2,015 interpolation values and 19 product contraction tests;
- 247 iteration-error inequalities, including n=2 and k=0;
- 300 exact tent-model meshes with varied endpoints, 9,100 contiguous-block identities and 36,400 cross-mesh interpolation identities, using an independently implemented concave-envelope solver;
- 625 positive-control medial identities in rational affine space.

The varied-endpoint solver is used as finite regression evidence only. All universal conclusions above depend on the written arguments. No finite computation proves completeness of an arbitrary space or whole-sequence convergence.

## 4. Data identity and prior-attempt evidence

Both complete public corpus files were independently hashed and parsed: 15,458 problems and 6,701 research entries. Their sizes and hashes match the freshly retrieved repository manifest. The complete catalog hash and its Git blob identity agree with the freshly read repository directory. Exactly one record has the target ID, and the statement digest matches the catalog.

The review digest was independently reconstructed using the currently retrieved queue implementation's canonical formula. It is `640a06a3fb07d9ffe0e56d4eca4f50420255e54dcd53ab02b926c6880be0883b` and agrees with the catalog. This is a metadata supplement to the frozen report, not a mathematical repair. No research record is keyed by the target code, and no exact ID/code/title matches occur across the research corpus. A broader bicombing search found seven research entries about other questions; these do not establish a prior target attempt.

Fresh read-only repository searches by ID and bicombing terms returned no matching PR, commit, branch, issue or default-branch code result. The root, prioritization, attempts and problems directory listings were read independently; the attempts listing now has 63 entries, compared with the author's earlier 62, with no target entry. A fresh bounded local scan found 223 target matches, all queue-style rows; no authored target attempt was established outside this investigation. The author's truncated recursive tree is not promoted to full coverage. These checks cannot exclude deleted branches, unindexed material, inaccessible private work, or unrelated paths. No prior-attempt skip is justified.

## 5. Reproduction and publication boundary

Run `python independent_checks.py` in the extracted audit folder. It recomputes the finite results and verifies the audit manifest. Run `python provenance_check.py --help` for optional replay against the original author ZIP and externally supplied full public source inputs. The data and PDFs are deliberately not bundled.

The audit package contains only authored audit exposition, authored code, exact results and public verification metadata. It excludes PDFs, screenshots, extracts, raw corpus records/files, downloaded trees and private coordination material. No remote writes were performed. The only accepted conclusion is the scoped PASS above; unresolved status and all convergence/domain limitations must accompany any later use.
