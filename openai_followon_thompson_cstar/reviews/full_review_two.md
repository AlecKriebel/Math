# Fresh independent complete-package review 2

Review checkpoint: 2026-10-07T05:33:36.673981+00:00. Best-guess completion: 100% of this independent mathematical audit and 100% of this package audit. These percentages do not certify publication or tracker completion.

## Verdict

**PASS: the exact frozen current manuscript, three intended upload payloads, and Zenodo manifest have no substantive unresolved issue found by this review.** They are ready for the authorized publication workflow as an explicitly attributed consequence note. The mathematical resolution is an application of the manually reconstructed OpenAI nonamenability argument and the cited established reductions. This verdict supplies no claim of novelty, first priority, fresh Lean kernel verification, human refereeing, or completed publication.

I independently read the original user request, the original upstream proof and actual theorem declarations, then checked the downstream sources and complete current package. I did not read the other complete-package review's verdict or treat the supporting agents' favorable conclusions as proof. Their audit documents were reviewed as artifacts, with their pivotal assertions checked against sources and deductions below. I did not spawn agents, alter the upstream clone, run Git publication operations, contact individuals, or deposit anything.

One evidence defect was found and resolved during this review: the original receipts/CLEAN_REPRODUCTION.json contained earlier PDF/source hashes 4dfd4523… and d418b694… and therefore did not certify the current frozen files. I notified the lead promptly, performed a fresh clean reproduction of the current archives, and confirmed that the lead replaced the current receipt with those actual results while preserving the initial receipt separately. No manuscript, payload, or manifest bytes changed to accomplish this. There is no remaining required repair.

## Exact reviewed version

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| upload-kit/paper.pdf | 527ac7feb6f2c889998559122296dd8caab2def0cf7aeac00f79c1f8b0c8a978 | 56917 |
| upload-kit/thompson-cstar-source.zip | bee0a8503a8f6706a02e3cad69680c8057a39f361b9b7c622c297fac2217b3aa | 7516 |
| upload-kit/thompson-cstar-verification.zip | ec84a7112daaf322d094a2d8cff44d203fa722e7f431ce868d7b7c497b63157e | 50534 |
| zenodo-deposit.json | f2869998ee98a3cbe54daa3914ba608d2a2acb7b71e261a4bbfc40afaf39fb78 | 2508 |
| main.tex | 5a95378741e1a371056251df4d6a492c16169d349ecc02ddb1b0d3ecd791fe92 | standalone source |

The paper in the project equals the intended upload PDF byte for byte. Every archive member equals its corresponding project file. Both ZIPs pass integrity checks and contain no absolute or parent-traversal paths. The source ZIP has 4 members; the verification ZIP has 15. Their member lists were inspected; they contain project writing, original checker code, bibliography metadata and source/hash references, without upstream papers, Lean sources, dependency caches or credentials. Evidence: reviews/full_review_two/reviewed_hashes.json.

## Independent mathematical reconstruction

The upstream carrier is precisely the standard increasing finite-piece dyadic PL interval group, with composition multiplication. In its finite proof, pair transport is constructed by partitioning the three positive complementary gaps and bisecting until corresponding cell counts match. Slopes remain powers of two, so transport stays inside F. Images of sufficiently fine uniform partitions are basic because each affine intercept is dyadic and a single finite threshold resolves all breakpoints and intercept denominators. Nested basic cells ensure that sufficiently small mesh respects each prescribed interval. Normalized restriction covariance follows from the affine charts, without requiring the transport to preserve the other intervals.

The recursion decreases the finite cell count on every internal parent restriction. All colors lie in the unit ball. Crucially, f,L,delta,D,parents,descendants and the finite transport family S are fixed before the arbitrary nonempty finite A. Only n depends on A, with one level chosen for A union SA. Correlations at that level are globally bounded functions, including zero on inadmissible elements, so finite-average cancellation applies even though n depends on A. No invariant-mean limit or illicit quantifier exchange is used.

Writing c=1-1/D, the parent and sibling norm expansions each have upper bound c(alpha+eta)+1/D. The mixed product has D(D-1) separated terms and D nested exceptions, yielding lower bound c(alpha-eta)-1/D. Therefore the coefficient of alpha cancels exactly, including negative alpha, and the variance bound is 4/D+4c eta. The pointwise identity m=D^{-1} sum_i f(z_i), Jensen's inequality and Lipschitz continuity give delta^2 <= L^2[4/D+4c eta]. Thus every nonempty finite A has maximum S-boundary at least (delta^2/L^2-4/D)/(4c)>0 when D>4L^2/delta^2. Taking the Følner tolerance equal to this fixed positive constant gives the contradiction. No averaging is commuted through nonlinear f, and no probabilistic independence is assumed.

The analytic input is a Lipschitz unit-ball map with positive uniform displacement. Its published existence is the third assertion of [Benyamini–Sternfeld](https://www.jstor.org/stable/2044990). I also reconstructed the explicit upstream appendix: the velocity is bounded and Lipschitz, with speed at least 1/8; sinc decay establishes uniform separation at every fixed parameter gap. The minimizing-sequence argument confines parameters to a compact real interval, so it does not assume compactness of the Hilbert ball. The tangent estimate proves uniqueness of the nearest parameter before selecting it. The rotation formula avoids antipodal singularities. Radial cutoffs glue the correction across the tube boundary; the four residual regions give the nonzero lower bound rho/4. Outside norm 1/2 the correction is identity. Negative normalization then has displacement at least 1/2 and a finite Lipschitz constant. Equality cases at residual rho/4, rho/2, tube boundary rho, and norm 1/2 are covered. No material gap or circular premise was found in the original proof.

## Primary downstream sources and exact group match

I independently inspected the [published Le Boudec–Matte Bon paper](https://www.numdam.org/item/10.24033/asens.2361.pdf) and its [arXiv v3](https://arxiv.org/pdf/1605.01651). Theorem 3.7 requires a countable group of homeomorphisms of a Hausdorff space with nonamenable rigid stabilizers for every nonempty open set. Theorem 4.1 and Corollary 4.2 give the stated standard-circle and F/T results. Theorem 4.3 and Corollary 4.4 give the line and full abstract Aut/Comm results. These are printed established reductions, not a new mechanism. The paper's ambiguous positive-slope ambient description and erroneous left-tail endpoint do not invalidate the conclusion: full faithful Homeo(R) realizations are available and Theorem 3.7 permits reversal.

The full automorphism realization was checked in [Brin, Theorem 1, pp. 8–9](https://www.numdam.org/item/PMIHES_1996__84__5_0.pdf): the normalizer in full Homeo(R) maps isomorphically to Aut(F), with orientation-preserving subgroup of index two. The full commensurator realization was checked in [Burillo–Cleary–Röver, Theorem 3.1 and its proof](https://web.mat.upc.edu/pep.burillo/Papers/comF.pdf): an injective realization in Homeo(R) includes orientation-reversing conjugators. Its orientation-preserving subgroup is explicitly distinguished. This is the abstract commensurator of isomorphisms between finite-index subgroups, not a relative commensurator of an accidentally smaller ambient group.

For the forward mechanism independently of ambient PL notation, each nonempty line or circle open set contains an internal elementary dyadic interval. Affine conjugation of an element of F to that interval, extended by identity, preserves dyadic breakpoints and slopes, gives an injective homomorphism, and lies in its rigid stabilizer. Thus the specified overgroups have nonamenable rigid stabilizers once F is nonamenable. Orientation reversal in the overgroup changes none of these containment facts. A general abstract copy of F in an unrelated action cannot replace the specified local-support copy.

Countability is sound: finite dyadic data count F and T; the dyadic-preservation requirement excludes irrational rotations from T. F has two generators, verified in the [Cannon–Floyd–Parry presentation](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf). Images of two generators count all automorphisms. Permutation actions of a finitely generated group give finitely many subgroups of each finite index; Schreier finite generation then counts all isomorphisms between each ordered pair. Quotienting their countable union counts the full abstract commensurator. There is no unjustified inference from the cardinality of an ambient homeomorphism group.

The actual applicable trace theorem was independently read in [BKKO, Theorem 1.3, Theorem 4.1 and Corollary 4.3](https://www.numdam.org/item/10.1007/s10240-017-0091-2.pdf). For discrete groups, traces on the reduced algebra vanish outside the amenable radical, and uniqueness is equivalent to its triviality. C*-simplicity forces a trivial radical. Applying this separately to each of the four groups gives precisely the canonical trace, by density of the group algebra. This inference is confined to reduced group algebras, with no claim for arbitrary simple C*-algebras.

The [published Haagerup–Olesen discussion after Theorem 5.5 and Remark 5.6](https://www.isibang.ac.in/~soumyashant/misc/collected-works-of-haagerup/2010s/2017_Non-inner_amenability_of_the_Thompson_groups_T_and_V.pdf) explicitly records T's prior unique trace and credits Dudko–Medynets; the remark records the nonamenability/unique-trace equivalence for F. The different arXiv numbering 4.5/4.6 is correctly explained. Their introduction's erroneous “amenable” sentence is not repeated as evidence. T's already unconditional trace assertion is correctly distinguished from its newly available simplicity assertion.

## Falsification attempts and rejected traps

| Attack | Result |
|---|---|
| Swap exists S / for all A | Rejected: S and the positive boundary constant are fixed before A. |
| Require all F to be admissible at one n | Rejected: only the finite A union SA is required; global zero extension supplies bounded test functions. |
| Assume nonlinear f preserves means | Rejected: the proof uses a pointwise recursive identity followed by Jensen/Lipschitz bounds. |
| Impose positivity of alpha | Rejected: signed alpha cancels algebraically. |
| Treat nested child/parent pairs as separated | Rejected: exactly D mixed exceptions are bounded separately. |
| Lose covariance on hA minus A | Rejected: covariance is needed on source A and finite translation cancellation handles the boundary. |
| Assume a bounded Hilbert curve is proper/compact | Rejected: nearest-point attainment uses uniform parameter separation and real compactness. |
| Infer full-group simplicity from an index-two subgroup automatically | Rejected: full faithful actions with the same nonamenable rigid stabilizers are used. |
| Infer subnormality is transitive normality | Not used by the consequence proof; supporting trace notes justify full F' normality through bounded-support preservation. |
| Transfer reduced assertions to full C*(G) | Rejected: augmentation and pulled-back regular traces differ on every nonidentity element; lambda_g-1 gives a nonzero augmentation-kernel element. |
| Confuse C*-simplicity with abstract group simplicity | Rejected: F has proper derived subgroup, while T's abstract simplicity supplies only its prior radical/trace observation. |
| Advertise V/nV as new | Rejected: prior status is explicitly acknowledged. |

## Actual formal-source and computational coverage

Read-only upstream HEAD is adc7f1241b42e322a6451854ab7e4b4c146bf78a. I recomputed all 88 SOURCE_MANIFEST file hashes and compared their bytes with this pinned Git revision: no mismatch. I reconstructed the actual internal import closure from OAI.GroupTheory.Thompson.Main: all 68 internal modules exactly match the Lean manifest hashes, byte counts and line counts. A source scan after removing comments found no sorry, admit, axiom or unsafe declaration in that closure. The ComparatorChallenges statement does contain its intentional sorry; it is not imported into this closure and is not a proof certificate.

I inspected the real Main declarations, StandardF group composition, StandardCharacterization carrier equivalence, InvariantMean semantics and its derived continuity, FiniteBoundary/FiniteCorrelationBoundary quantifiers, MeanApproximation separation bridge, MeanToFolner conclusion and concrete AnalyticConstruction instantiation. There is no hidden displacement or nonamenability certificate left as a hypothesis of Main. This is source/semantic inspection, not Lean kernel verification. No fresh build was performed; available disk was about 336 MiB, consistent with the reported practical limitation. I do not infer kernel acceptance or the complete external dependency trust closure from a marker scan. Evidence: reviews/full_review_two/source_checks.json.

The exact checker was inspected and run from the freshly extracted verification archive under Python 3.14.6. It passes 1969 transports, 31504 covariance-cell identities, 17 recursive identities and the fully enumerated 1024-cell image partition at level 10. Its scalar test map deliberately has a fixed point and is not represented as the analytic displacement witness. These are finite corroborating checks.

I also performed 4480 independent exact-rational vector checks of the variance inequality for D in {2,3,5,7,11}, including 396 trials with negative reference correlation. The symbolic coefficient cancellation was checked directly. No counterexample was found. This finite search does not prove the universal inequality; the expansion above provides the mathematical justification. Evidence: reviews/full_review_two/independent_variance_checks.json.

## Clean final reproduction and PDF verification

The current source archive was extracted into an empty dedicated review directory and compiled successfully with Tectonic 0.16.9. The rebuilt PDF has SHA-256 cdb545609894ff7a72d431e0e7449014e1fc5754b2418ff64f10b47d4ef24d3e. Its binary hash differs from the frozen PDF, so byte-identical PDF reproduction is not asserted. Extracted layout text is exactly identical, and all four rendered page PNGs at 100 dpi are byte-identical to corresponding frozen-paper renders. I visually inspected all four frozen pages: formulas, theorem statements, references, ORCID, title/date and page breaks are readable; no clipping or overlap was found. All fonts are embedded. There are no unresolved-reference markers. The sole TeX diagnostic is an underfull box at line 88, with no substantive layout defect.

The standalone source archive reproduces the PDF. The finite-check command applies to the separately extracted verification archive, which contains the checker. Their common BUILD document accurately distinguishes mathematical/manual checks from finite checks and the unrun formal build. The current exact reproduction receipt is reviews/full_review_two/CLEAN_REPRODUCTION_CURRENT.json; the lead's receipts/CLEAN_REPRODUCTION.json was verified to contain these results.

## Priority, authorship, licenses and metadata

The title, abstract, body, README, ledgers and manifest consistently frame the work as an attributed consequence. OpenAI receives the nonamenability attribution; Le Boudec–Matte Bon the simplicity reductions; BKKO the trace theorem; T's prior trace is acknowledged. No first observation, new criterion, independent amenability solution or new V/nV simplicity claim appears. The original supplied manuscript BibTeX is preserved in the source archive, while the actual paper pins the cited source revision.

My fresh public queries were “OpenAI Thompson C*-simple,” “OpenAI Thompson Aut(F),” “OpenAI Thompson Comm(F),” and “OpenAI Thompson nonamenable correction,” with exact quoted variants saved in priority_refresh.json. No relevant exact post-input duplicate or correction appeared in returned indexed hits. I also scanned upstream TeX/Markdown/BibTeX jointly for Thompson and the named-group/operator terms, inspected the hits and the entire family-248 consequences section; its applications concern other directions. This is bounded corpus/index evidence, not proof of absence or first priority. Current GitHub main independently remains the pinned initial commit, with committer timestamp 2026-10-06T21:58:50Z. The manuscript date September 23 is correctly not treated as proof of earlier public availability. Evidence: priority_refresh.json, bounded_corpus_priority_hits.json, upstream_public_refresh.json under this review directory.

The manifest lists precisely a separately downloadable paper, source ZIP and verification ZIP, with the reviewed title, sole author Alec Kriebel, supplied ORCID, October 6 publication date, open access, preprint type, CC BY 4.0 writing license and primary related identifiers. The README clearly excepts the original exact-check code under MIT and says third-party works retain their own licenses. No third-party source redistribution was found. AI use and absence of conventional human peer review are accurately disclosed, and automated reviews are not represented as human refereeing.

## Readiness boundary

There is no known substantive concern remaining in this exact candidate. A mathematical or material framing change after this review must be reviewed again. This verdict covers the note and reviewed payload/metadata consistency; remote Zenodo identity/file reconciliation, publication, DOI resolution, tracker append/readback and final Git publication are still actions for the lead to verify. The entire new-input conclusion inherits the validity of the upstream theorem; the established conditional reductions and T's unique trace remain intact if that input is later defective. No fresh kernel build or public-priority proof has been claimed or supplied.
