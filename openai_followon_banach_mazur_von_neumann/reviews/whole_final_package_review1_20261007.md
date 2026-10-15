# First new complete publication-package review — 2026-10-07

Reviewer: `whole_final_package_reviewer1_20261007`. Completed approximately 14:52 UTC. Relevant review completion estimate: **100%**. This is the first new whole-package review of the full arbitrary-predual proof and upload kit. Earlier conditional-checkpoint reviews do not count toward it. The two supporting mechanism reviews below are subreviews of this review, not additional whole-package reviews or human refereeing.

## Verdict and exact remaining conditions

**PASS for the mathematical and publication-package quality of the exact frozen `final_candidate_v1` bytes: no required mathematical, attribution, reproducibility, or payload-consistency repair was found.** The proof preserves the original goal for every complex von Neumann algebra, arbitrary preduals and centers, and all infinite type-I cardinal dimensions. Its result is an algebra-dependent ordinary complex Banach–Mazur threshold with a Jordan *-isomorphism conclusion and the same threshold for canonical preduals.

This is **not actual publication clearance**. The frozen license is explicitly proposed, not accepted by the human. The original brief also requires the separate second new complete review and a fresh review of the latest exact package after any material changes. Production deposit staging/readback/publication/DOI verification and subsequent tracker readback have not happened and were not performed by this reviewer. This report clears no such action or factual claim. Its quality pass is conditional on the explicit human license decision and faithful reconciliation of the final licensed files; any changed upload payload must receive the required final exact-package inspection/review.

No unresolved mathematical gap was found under the openly stated classical inputs and the independently audited pinned upstream mathematical proof. This is mathematical source review, not a Lean kernel certification or proof of priority. Conventional human peer review remains absent and is accurately disclosed.

## Exact reviewed version and authentication

Project: `/Users/alec/Documents/Math/openai_followon_banach_mazur_von_neumann`. Frozen root: `reviews/versions/final_candidate_v1`.

| Artifact | Bytes / scope | SHA-256 |
| --- | --- | --- |
| `review_manifest.json` | exact frozen manifest | `999be65a839b19f972aa5fd802b766888d8038f2496c7fddb1d0321dc3cca43a` |
| `manuscript/main.tex` | 22,215 bytes, complete standalone source | `46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4` |
| `output/pdf/paper.pdf` | 83,877 bytes, all seven pages | `64ef84935aa6b3d327e30d26719927ce603aa75116a6aefa70589342bafe1c0b` |
| `publication/upload-kit/source-and-verification.zip` | 617,635 bytes, 41 members | `4dc0129f59789e279318bc2e1ba53a1c3e414fda8a7ba32c8dd1d7f221aee9fc` |
| `zenodo-deposit.json` | 2,573 bytes, exact two upload files | `6ba70c83463b4128180fca31aa475b0524825f23c48f9d0ec612b17cfbb36b95` |
| original `research/PROJECT_BRIEF.txt` | 18,577 bytes, read in full | `496e4cf36100a785f53ea8015835231063cb73ec3c53dcda0d4b149f8fa81ca2` |
| actual `/Users/alec/Downloads/roydor2020.pdf` | 431,430 bytes, complete 26-page primary version | `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4` |

All **12** files in the frozen review manifest were independently size/hash authenticated. The ZIP passed CRC readback. All **40** `SOURCE_MANIFEST.json` entries matched their exact archive bytes; the forty-first member is the source manifest itself, deliberately excluded from its own digest list. All member paths are relative, lack parent traversal, and are regular files rather than symlinks. Archive TeX and deposit metadata exactly equal their frozen external counterparts. The two metadata upload paths resolve to the actual reviewed PDF and ZIP. At the end of review, the current manuscript, PDF, ZIP and metadata still matched the frozen bytes exactly; subsequent administrative research-log/state updates are outside the archive.

Every redistributed upstream original file was independently byte-compared to its pinned Git object at `adc7f1241b42e322a6451854ab7e4b4c146bf78a` in the read-only upstream checkout. The five complete proof sections total 2,023 source lines. The archived upstream PDF has 28 pages, correct OpenAI metadata, no encryption, forms or JavaScript, and its pinned SHA is `56ec913df9fbe4a2daf371eec1cb06ddc5b544cf9defc838aab540f33171f753`.

Detailed repeatable authentication is saved in `reviews/whole_final_package_review1_20261007/authentication.json`, SHA `0d561b32d3c6050a82858699f9f9ef9d4bafb340c53e284c571b48e11894805a`.

## Actual coverage and independence

I read the original full brief, applicable AGENTS instructions, the entire 449-line candidate, all seven candidate PDF pages visually, and every text member of the curated supplement: theorem/dependency/approach ledgers; validation scope; licenses; source versions and manifest; upstream attribution, full Apache license, README, Lean scope, build source, figure, typography mappings and both bibliography files; all five upstream mathematical sections (the included upstream PDF was byte-authenticated, with its complete mathematical content read in the pinned TeX rather than a separate visual inspection of all 28 PDF pages); the bundled mathematical audits; the full new October 7 priority audit and its source-bound final-candidate addendum; the three finite scripts and stored results; and both build scripts plus publication/reproducibility instructions. I also read the frozen preparation/build/export/clean-reproduction/local-check receipts, program state and full research log.

For Roydor I read the complete 26-page primary text, including every proof and concluding section, and independently inspected the actual printed physical pages 2, 15 and 20. The supporting geometric reviewer separately read all 26 pages and visually inspected every cited quantitative prerequisite, including pages 6–7 and 10–13. This uses the human-supplied full publisher-formatted December 2020 reading version with the article DOI; it does not pretend that its bytes were compared to a separately retrieved final 2022 issue PDF.

I independently reconstructed the new argument and the upstream five-section mathematical chain. Existing bundled audits were checked for package consistency and additional attacks, not substituted for the proof. I assigned two fresh, distinct supporting reviews from primary inputs rather than giving them a favorable prior mathematical verdict. Their full reports were then read and checked:

- `reviews/whole_final_package_review1_20261007/geometric_independent.md`, SHA `09f6fa1defbde8505b82040f144bd661890a752dd8a5a7b96fb7451f71c8392e`: PASS for Roydor geometry, nonseparable carrier/rank reconstruction and all quantifiers.
- `reviews/whole_final_package_review1_20261007/upstream_independent.md`, SHA `96446dd95deebfa20ddce4fb1da8afa6d1d033cb24ccda6d358d466c1ba33e0a`: PASS for every upstream section, ordinary bounded actual-image cohomology, arbitrary-algebra assembly and use on fixed P,E.

Neither supporting report counts as the second new whole-package reviewer. Neither claimed a kernel build, human peer review, or publication clearance.

## Mathematical falsification results

### Ordinary cohomology and the complete upstream proof

The candidate uses ordinary bounded complex multilinear cochains with values in the algebra itself and the literal image of the standard differential. The displayed differential has every adjacent merger, right-action sign `(-1)^(k+1)`, and degree-zero commutator. It agrees with family 295. The Roydor reading-version differential on physical page 20 really has the reported omitted merger/sign typo; the candidate does not adopt it. Degree-three vanishing makes the actual image equal the closed kernel, so closed range is supplied without passing to reduced cohomology.

I checked the upstream rare-level walk, martingale Liouville argument, first-letter rigidity, and primitive construction rather than assuming the target theorem. The finite free requirements use Popa's factor-ultraproduct case (a), not its different centralizer case. Distinguished path labels, reduced-word trace tests and later finite probability choices are compatible. The martingale endpoints are obtained through finite-trace compactness; prefix approximations, rather than the limiting endpoints themselves, provide the required independence. Concatenation uses distinct unsigned block indices. Two ultrapowers pass the bounded-ball 2-continuity conditions needed for the exact identities.

The rigidity section applies the Haagerup estimate to the exact free family, controls repeated surviving labels, and uses ordered block products. Catalan moments give a positive operator with zero kernel; finiteness makes its polar isometry unitary. Polynomial regularization and bounded-ball 2-continuity justify polar limits. The spectral-arc trace estimate does not assume the multipliers commute with the polar unitary or lose a growing number-of-arcs factor.

The averaging primitive argument is ordinary bounded; it does **not** claim that averaging commutes with the differential or yields cb cochains. Product ultraweak compactness preserves the multilinear bound and last-slice 2-continuity. The cocycle signs give the actual bounded primitive. Uniform normal-cocycle primitive bounds are obtained before finite-input compactness removes separability. The separable subalgebras contain every finite matrix system, excluding hidden finite type-I central pieces. For arbitrary centers, tracial central-state-support pieces are assembled with the explicit central homotopy; restricted primitives alone would fail on mixed central inputs. Uniform bounds make the uncountable central direct product bounded. The classical complementary-summand result and normal reduction then give an actual ordinary primitive on every von Neumann algebra.

Fresh supporting primary checks authenticated the exact scope of [JKR's original normal-reduction theorem](https://www.numdam.org/article/BSMF_1972__100__73_0.pdf), [Popa's Theorem 0.1(a)](https://arxiv.org/pdf/1308.3982v3), [CPSS's ordinary-cohomology statement on p. 636](https://annals.math.princeton.edu/wp-content/uploads/annals-v158-n2-p07.pdf), and Blackadar's relevant structure results. In particular cb methods in the cited complementary result do not replace the upstream new ordinary type-II argument. These are exact-primary-input checks, not a new foundational proof of every classical citation. The supporting report records that boundary candidly.

### Involution-preserving deformation with fixed constants

Candidate lines 130–184 give a valid complete local correction. Both quotient inverse bounds are available on Banach spaces because actual-image H²,H³ vanish. Strictly enlarged K,L accommodate nonattained quotient infima; no bounded linear splitting is assumed. The signed reverse-adjoint involutions are conjugate-linear on cochains but preserve complex multilinearity. Direct reversal of each differential face gives `d S_n = S_(n+1) d`, so real averaging of cocycle and primitive preserves all bounds and the required star symmetry.

Associativity gives the displayed quadratic `d Delta` exactly. I expanded the transported product using `g=I+h`, `b=g^-1`: its defect is precisely `(Delta-dh)+h Delta-m(h.,h.)` evaluated on b inputs. The bounds give `D=8K+8L+16L²`, and the chosen positive fixed delta gives geometric decay and a summable correction norm. Ordered products `g_(n-1)...g_0` converge in norm within one-half of I and are invertible. The intertwining limit is exact. Intermediate products need not have the original unit; the final onto algebra isomorphism between products having unit 1 automatically fixes 1. Constants belong to the entire fixed algebra throughout.

This mechanism is correctly attributed to the classical deformation literature and [Ricard–Roydor Proposition 3.2](https://arxiv.org/pdf/1108.1970v2), whose primary full text I independently read. It is not represented as an invented involutive mechanism or a universal numerical ordinary-cochain bound.

### Halving, orientation and ordinary norm control

Roydor's actual Theorem 1.2 on printed page 2 requires separable predual. The candidate correctly rejects its direct use for the full target. The separately cited Corollary 2.4, Lemma 2.5, Proposition 2.13, Lemma 3.1 and Theorem 3.2 have no hidden separability assumption in their finite matrix/norm proofs. Theorem 3.2's even finite type-I hypothesis is used only when the source unit halves.

Lemma 3.1's maps are symmetrically unitalized, onto, self-adjoint and complex linear; this justifies the claimed unital F, including zero-block omission. Central target product twisting is associative and C* with the unchanged norm/star/unit and Jordan product. Its pulled-back product is on the **entire fixed V**, with the displayed ordinary bilinear bound tending to zero. Thus moving central orientation projections never enter a choice of deformation threshold. The exact homomorphism is `F Phi^-1`, with the correct transport direction.

The source's Claim 4 heading really has an off-diagonal transpose typo; the preceding computation and subsequent claim use the correct `h_ji`. A further supporting source check sharpened the compressed inverse estimate: the source's last coarse bound by itself does not prove its displayed inverse constant over the whole stated interval, but its earlier estimate proves

`||(T_p^q)^-1|| <= (1+t)^2 / [1-742(1+t)sqrt(t)] <= 1+988sqrt(t)`

for `sqrt(t)<=10^-4`; the cleared polynomial is positive. Moreover the candidate needs only much smaller sufficiently small parameters. Consequently this is a verified source-calculation abbreviation, **not a candidate defect**, and requires no source/PDF repair. The full derivation is preserved in the new geometric report.

### Full carriers, odd finite ranks, arbitrary centers and cardinalities

I checked the carrier inequality by applying approximate order to the unital self-adjoint inverse, followed by both center/projection error terms. Compressing by the complement of the source central projection yields a projection bounded above by a scalar strictly below one, forcing zero. The complement argument uses unitality and introduces no normality or countability assumption on the near map.

For odd O, the rank-(n-1) projection is chosen **once** in the bounded central product. E=eOe is a single fixed algebra that halves; both e and its abelian complement are full. Both rounded target projections remain full. The complementary corner is abelian, forcing type I. The exact Jordan map from E identifies full-corner centers. Positive order isomorphisms preserve all existing increasing-net suprema, so central joins survive without measurable-fiber or separability assumptions.

On each corresponding finite degree piece, the Jordan map preserves the degree n-1 of the large corner. Its n-1 equivalent abelian projections and the full abelian complement have the same target carrier, so all n are equivalent. This establishes degree n without an infinite-cardinal cancellation. Exact matrix-over-center *-isomorphisms have norm one and assemble into the bounded product even when odd finite degrees are unbounded. The supporting primary check uses [Anantharaman–Popa's author-hosted book](https://www.math.ucla.edu/~popa/Books/IIun.pdf), including full-corner centers, equivalence of equal-support abelian projections, type-I characterization and halving.

The final decomposition has only fixed A,P,O and at most two nonzero deformation sources P,E. Every infinite type-I cardinal dimension belongs to P and halves; II and III parts also halve. All later smallness inequalities are finite compositions of error functions tending to zero. One positive threshold therefore precedes every comparison N and every target/orientation projection. The proof does not take an unsupported infimum over moving corners or degrees. Universal upstream vanishing is explicitly applied to noncentral E, rather than incorrectly deriving it from a central restriction of M.

### Preduals and boundary cases

The adjoint of an actual predual isomorphism has exactly the two original norms and inverse equal to the inverse adjoint. Symmetry of ordinary distance therefore proves `d(M,N)<=d(M_*,N_*)` and transfers the same epsilon. Exact Jordan order isomorphisms are normal and isometric and give isometric canonical preadjoints. The converse is consistent with Kadison and the unrestricted p=1 endpoint of [Sherman's Theorem 1.1](https://arxiv.org/pdf/math/0309365v2), which I checked in the primary paper.

The zero algebra is handled with the literal norm-product distance convention; nonzero/zero comparisons have no isomorphism and infinite distance. Absent central blocks are omitted. Strict distance bounds supply actual maps without attainment. Opposite orientations explain why Jordan structure is the correct conclusion. No passage from ordinary to cb distance, no arbitrary Banach comparison target, universal epsilon, or unproved associative-isomorphism conclusion is used.

## Priority and publishable-contribution audit

I read the complete newly dated October 7 primary-source priority audit, including its final-candidate addendum bound to source SHA `46a02c0...`. The supplement audit SHA is `20547284b6f72c892b12cfc13fa0092cfd2a0bfe1e76af9e0afb1337221503f1`. It checks original and equivalent formulations, prior deformation/predual/type-I results, relevant older primary literature and companion upstream material. I independently checked Roydor's complete primary version, the complete Ricard–Roydor comparator and Sherman, and made fresh literature-discovery searches with ordinary-distance, nonseparable, predual and cohomology formulations. No explicit duplicate of the complete arbitrary-algebra consequence **and proof** was identified in these bounded checks. An additional GitHub API read failed; that failure was treated as inconclusive, not evidence that no newer version exists. The package pin is exact and the archived fresh upstream check is separately documented.

The contribution is modest but intelligible: a complete fixed-source proof arrangement extending the inspected published argument to arbitrary preduals and applying the newly public cohomology theorem. The general conditional statement was already announced by Roydor, involutive deformation and orientation twisting are inherited, full-carrier/type-I structure is classical, and predual duality and older ordinary subcases are inherited. PDF, source, metadata and ledgers consistently say this. They do not claim firstness or an independent new cohomology solution. The fresh priority evidence supports considering this a checkable follow-on preprint, not a certified novelty or historical-priority conclusion. No external person was contacted or outreach prepared.

## Reproduction, rendering and package/security checks

I ran the three included exact finite scripts in a fresh extracted archive. The original semantic JSON results reproduced: 5,461 scalar central-homotopy equations, 16 Catalan-count cases and seven block cases; 260,416 noncommutative scalar equations on M₂(C) direct sum C; and 1,022 symbolic central patterns in degrees 1–9. These checks are finite mechanism evidence, not a computational proof of the full theorem, and the kit correctly labels them.

I ran the included standalone builder from that extracted tree in its fresh temporary build directory with Tectonic 0.16.9. It completed successfully with no overfull boxes. The rebuilt PDF is seven pages and 83,877 bytes. Its SHA `b546960950925ded1e6f8d1b6efda48fe4f6088aa5808645b4cda16071e2d272` differs from the export because of its new creation timestamp, not source or rendering. The complete layout text matched the frozen PDF exactly, and **all seven independently rendered 105-dpi page PNGs matched byte-for-byte**. Separately, I visually inspected every frozen page at 1500-pixel scale. No clipping, missing equations, unreadable layout or PDF/source discrepancy was found. The sole underfull warning produces expanded but legible spacing in the Sherman bibliography entry; no repair is required.

I then ran the archive builder in the extracted tree. It recreated the **exact same 617,635-byte ZIP**, SHA `4dc0129...`, including all 41 members. No unbundled manuscript support file is needed. The build script checks the immutable source and writes only owned output/scratch; the archive builder curates explicit files and preserves upstream bytes. Neither finite checks nor archive building performs deposit, tracker operations, external messaging, or secret access. No credentials, local acquired Roydor/comparator PDFs or their full extracted text, unrelated work, or large formal dependencies are bundled. References to repository-only research records are disclosed as such and are not needed to rebuild the standalone paper.

The independent replay and seven-page pixel evidence are saved in `reviews/whole_final_package_review1_20261007/independent_replay.json`, SHA `2a511a8d0705fbeb4dd447f01f3ad79e886c904e9158902f4a416e2ae7d1738e`.

## Metadata, redistribution and protocol consistency

The reviewed manifest uploads exactly `paper.pdf` and `source-and-verification.zip`, presents a preprint dated October 7, 2026, and uses Alec Kriebel's supplied ORCID without invented affiliation or coauthors. The PDF and metadata identify the same result, fixed pin and attribution limits. Extensive AI use and absence of conventional human review are explicit; static formal-source checks are never called a reproduced kernel build. Historical frozen logs accurately mark earlier blocked/conditional stages and zero final-package reviews before this version; those dated records are not claims about the later completed review.

The unchanged Apache-2.0 upstream license and attribution are preserved. No upstream NOTICE exists at the inspected pin, and no third-party reading-copy license is inferred. The proposed original-material Creative Commons license does not purport to relicense the upstream exception. **The original-material license choice is still pending**, as stated in LICENSES, preparation receipts and review manifest. A syntactically valid metadata license field does not satisfy that human-choice requirement.

I checked the described separate check→stage→inspect→publish→inspect-with-DOI workflow and the required exact-ID/tracker readback against the original brief. This reviewer has performed no production deposit, DOI creation, tracker append, Git mutation, GitHub release, or external-person communication. Those concrete actions remain with the coordinator after every user-required gate is fulfilled.

## Findings and disposition

| Severity | Finding | Required disposition |
| --- | --- | --- |
| Mathematical / package blocker | None found in the exact reviewed proof and provisional kit. | No manuscript or payload repair requested. |
| Explicit publication gate | Human license decision is unresolved; frozen metadata has the proposed cc-by-4.0 value. | Obtain the already-requested human answer and reconcile final license documents/metadata/archive; no elapsed-time inference of consent. |
| Explicit review/protocol gate | This is only the first new whole-package review. Actual deposit/DOI/tracker protocol remains unperformed. | Complete the other required new review and latest exact-package fresh pass as specified, then the separately authorized publication/readback protocol. Supporting reviews do not fulfill this gate. |
| Evidence limitation | Bounded priority search and mathematical source audits; no fresh Lean kernel experiment or human refereeing. | Preserve the existing candid disclosure; no stronger certification or firstness claim. |
| Optional cosmetic observation | Legible underfull Sherman bibliography spacing. | No repair required; avoid an unnecessary source/PDF change merely to remove the warning. |

Strongest verified result: the complete ordinary arbitrary-von-Neumann/Jordan/predual theorem follows by the stated, independently checked proof chain, and the actual standalone artifact and curated verification kit reproduce consistently. Exact remaining gap to publication is procedural/license completion, not an identified unresolved mathematical step. The whole-package review is complete; actual publication clearance and completion of the user's entire project are not claimed.
