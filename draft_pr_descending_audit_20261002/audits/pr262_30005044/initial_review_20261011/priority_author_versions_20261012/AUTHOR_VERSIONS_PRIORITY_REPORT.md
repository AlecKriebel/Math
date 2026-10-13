# Independent original-author and version priority audit

PR #262 · problem30005044 · OWR-9790363-003

Audit authored 2026-10-12 UTC. Owner: `priority_author_versions_20261012`. The relevant discovery goal remains at the parent's starting estimate of 35%; this bounded audit family is complete. Percentages describe progress, not confidence in novelty.

## Decision

**GO for a credited, self-contained quantitative note that answers the historical existential explosion question, subject to incorporating the later original-author reference. HOLD any claim of first discovery, current openness, or a newly discovered qualitative explosion mechanism.** The qualitative route was explicitly anticipated by the original authors in a paper submitted in June 2024, and the existing BKV estimates already support the qualitative common-time conclusion after elementary but essential time and recovery bookkeeping. This audit supplies that bookkeeping in `BKV_ESTIMATES_BRIDGE.md`; it does not pretend that the resulting statement was printed as a BKV theorem.

All four actual arXiv versions of Cardona–Tobón and Ortgiese's original fitness paper, and its distinct actual 37-page Cambridge publisher PDF, were read completely in manageable full-page text chunks. Each retains a finite offspring-mean standing assumption and an explicit finite-mean nonexplosion theorem. Those theorems neither refute nor directly contain the accepted infinite-mean candidate. Their survival and phase-transition results cannot be used as a substitute for the candidate's common-time assertion.

The decisive author-related material is Cardona–Tobón, Ortgiese, Seiler and Sturm, *The contact process on dynamical random trees with degree dependence*, [arXiv:2406.12689v1](https://arxiv.org/pdf/2406.12689v1), pp. 15–16 (submitted 18 June 2024), retained in [v2](https://arxiv.org/pdf/2406.12689v2), p. 16 (10 March 2026). The authors discuss finite-time explosion of the classical contact process for offspring mass exponent b in (1,2), point to BKV Proposition 6.2, and suggest removing the penalisation by taking its exponent zero. Their language is qualified discussion, not a theorem with an explicit deterministic time and probability bound. The candidate has mass probabilities asymptotic to (1/4)n^(-5/4), hence lies squarely within that discussed regime.

This audit did not find a printed original-author theorem with the exact time 1/(2λ), probability bound (7/30)exp(−3/(2λ)), and the candidate's all-rates quenched formulation. That is a bounded observation about actually read bodies, not a certification that these refinements are new anywhere in the literature.

## Exact accepted claim and audit boundary

The mathematical and source-model acceptance is an input from `ROOT_SCOPED_MATH_SOURCE_ACCEPTANCE.json`, SHA256 `542f4233d8d696fe9804a42120b1c2e3e9cd164ed85c785d349544edd105bf13`. The exact candidate manifest is SHA256 `3bad9b517356b93a5339c776ebfde1825492b21c171d881f06c67946897fcea8`. Those receipts accept the scoped theorem, not priority, novelty, publication or a merge. Their byte sizes, paths and hashes, together with candidate PROOF/TARGET/SOURCE_GATE/source_manifest and the dated historical proof/gate/review, are in `INPUT_MANIFEST.json`.

The candidate's offspring variable ξ is a finite positive integer almost surely, with P(ξ≥m)=m^(-1/4). Thus the random tree is locally finite, has no extinction, and has infinite mean offspring. Initially only the root is infected. There are independent rate-λ directed infection arrows in both directions and rate-one recoveries. Fitness is F≡1, or any almost surely finite fitness values at least one under the stated comparison. The process is the minimal extension witnessed by finite root-originating graphical paths, equivalently the increasing union of finite-ball processes.

For every λ>0, the accepted theorem has the annealed assertion

\[
\mathbb P(|X_{1/(2\lambda)}|=\infty)
\ge \frac{7}{30}\exp\!\left(-\frac{3}{2\lambda}\right)>0.
\]

For almost every tree, every λ>0 has positive quenched probability of an infinite configuration at some finite time. This is not a universal criterion for every infinite-mean distribution; it is not a uniform quenched lower bound or deadline; it is not explosion with dynamics probability one; and it does not settle post-explosion uniqueness. Novelty and current openness are not part of the accepted theorem.

The assigned family's job was to check original authors, versions, chronology, theorem bodies, later author-related discussion and the exact historical question. It did not independently re-prove every lemma in the original survival papers or certify the entire literature. No individual was contacted. No email, account/provider write, Git write, PR edit, Google Workspace change, paper publication or DOI release was performed.

## Provenance and actual reading

The actual repository AGENTS.md was read. Early independence was preserved: other priority-family reports were neither read nor discussed before `PRIMARY_COMPARISON_FROZEN.json` was created. Source-fidelity primary files were used only as byte locators, copied after independent size and SHA256 verification. The root acceptance receipt fixed the target claim. Earlier statements that someone had fully read a source were treated as dated historical claims; this report does not certify those old visits.

`PRIMARY_MANIFEST.json` records source URLs, byte counts, hashes, PDF page counts, metadata, copied-file provenance and direct-retrieval response headers. In particular the missing v2/v3 actual PDFs were successfully downloaded from their exact official arXiv version URLs and independently pinned. Extraction alone was not treated as reading. `READ_VISITS.jsonl` records every actual displayed page chunk, UTC visit time, inclusive bounds, character count and full-page extracted-text hashes. `READ_COVERAGE.json` contains the reader's confirmation and scope limitations. `FULL_BODY_LOCATORS.json` pins complete actual page bodies at theorem/model/argument locations, not just citation strings.

| Actual manuscript | PDF pages | Actual complete text-read chunks |
|---|---:|---|
| 2110.14537v1 | 42 | 1–7; 8–14; 15–21; 22–28; 29–35; 36–42 |
| 2110.14537v2 | 42 | 1–7; 8–14; 15–21; 22–28; 29–35; 36–42 |
| 2110.14537v3 | 38 | 1–7; 8–14; 15–21; 22–28; 29–38 |
| 2110.14537v4 | 41 | 1–7; 8–14; 15–21; 22–28; 29–35; 36–41 |
| Cambridge 10.1017/apr.2026.10066 | 37 | 1–7; 8–14; 15–21; 22–28; 29–35; 36–37 |
| 2406.12689v2, accepted author version | 55 | 1–8, with truncated 7–8 separately re-read fully; 9–18; 19–26; 27–34; 35–42; 43–49; 50–55 |

Bounded additional reads: official OWR PDF p. 1 and pp. 42–44 (printed 618–620); 2406.12689v1 pp. 1–30 and 55–56; BKV publisher pp. 1–11, 16–18, 46–48; 2312.06251v1 pp. 1–7. The rest of those manuscripts was not certified as read. The newer 2406 manuscript was read completely; the v1 read includes its full model, main theorems, explosion discussion, finite-path construction, relevant nonexplosion/comparison proofs and references, but not its entire star-survival section.

Twenty-five exact critical page renders were actually viewed. These include all original-version finite-mean/nonexplosion locators, the actual publisher counterparts, all three original OWR contribution pages, both later author's explosion discussions and the complete three-page BKV ray proof. `VISUAL_MANIFEST.json` records their image hashes and confirmed visits. Full-manuscript visual review is not claimed. Mathematical extraction can damage fraction placement, ceilings, fonts and rotated diagram labels; the critical formula locations were confirmed against pixels.

Main original-source byte pins:

| Source | Bytes | SHA256 |
|---|---:|---|
| OWR report | 950818 | 49a8f5051471ba04972b8d9cdd87e6e5d049ebcea93de93d2d4d10957febc98d |
| v1 | 427547 | 1ae3416d890db13c8bf4ba760c3f0bd20848d5b1908423a9cf72f8b7606ba28e |
| v2 | 432904 | af3342d45b4b2f08c16cd27d7537f066caa69c7f2c21eaf9b15999c2a38cc5fc |
| v3 | 394748 | 33c8b5c7c8ca01b4adb1375fc04ae634c65de35d2bdc989219eb60c0660d0864 |
| v4 | 463643 | 4614ee8c8aeb8a9374649d4e5ae95c99ab030cf27350c6f2a90a81fbbb39f0a9 |
| Publisher | 432817 | 9622cc6e8e9dfbfc404fb5fe7d5f97a431e7e4848420baa8f59ccf27c05f5d3d |

## Chronology and version changes

Official chronology is pinned by the [original arXiv history](https://arxiv.org/abs/2110.14537), [later arXiv history](https://arxiv.org/abs/2406.12689), [EMS report metadata](https://ems.press/journals/owr/articles/9790363), the actual publisher first page and [Cambridge publication metadata](https://www.cambridge.org/core/journals/advances-in-applied-probability/article/contact-process-with-fitness-on-random-trees/609C26838775B2CBB0A8B5D222E10D27). PDF generation dates can differ from submission dates; they are recorded as metadata, not confused with the first public timestamp.

| Date/time UTC where available | Primary event | Priority significance |
|---|---|---|
| 27 October 2021 15:48:41 | 2110.14537v1 submitted | Original finite-mean fitness model and nonexplosion theorem predate the OWR question. |
| 6–12 March 2022 | OWR workshop, report p. 1 | Historical source of the talk/question, not the report's publication date. |
| 11 March 2023 | EMS publication of OWR 19(2022), no. 1, pp. 577–656 | Actual report publication metadata. Question is printed p. 619. |
| 21 November 2023 14:46:42 | 2110.14537v2 submitted | Mixed-moment criteria broadened; joint offspring/fitness and positive fitness allowed. Finite mean retained. BKV preprint cited. |
| 11 December 2023 09:48:44 | 2312.06251v1 submitted | Ortgiese's adaptive Erdős–Rényi paper concerns finite graphs and cumulative epidemic size. |
| 24 May 2024 | Cardona–Tobón–Pardo CSBP explosion article published | Different continuous-state mass process, not contact-process cardinality. |
| 18 June 2024 15:04:09 | 2406.12689v1 submitted | Explicit classical infinite-mean explosion discussion and BKV-route suggestion already present, pp. 15–16. |
| 15 October 2024 22:19:15 | 2110.14537v3 submitted | Extinction proof shortened; main fitness paper remains finite mean. |
| 26 October 2024 | Date received by original fitness publisher, actual PDF p. 1 | Publisher processing date, not first public appearance of the result. |
| 10 March 2026 15:44:24 | 2406.12689v2 submitted | Accepted author version retains explosion discussion, p. 16. |
| 16 April 2026 | Fitness publisher acceptance, actual PDF p. 1 | No removal of finite-mean scope in actual published text. |
| 13 July 2026 | Cambridge original fitness paper online | Distinct 37-page publisher text, DOI 10.1017/apr.2026.10066. |
| 14 July 2026 15:55:15 | 2110.14537v4 submitted | Latest 41-page author PDF; not the same pagination/file as publisher. |
| 12 October 2026 | This audit | Prior-result comparison as of this bounded search. |

Version comparison, using full bodies rather than abstract-only extrapolation:

* **v1:** Definition 2.1, p. 4, takes independent identically distributed fitness F≥1; F≡1 is explicitly included on p. 5. The global finite-mean assumption is on p. 5. Theorem 3.2 and its complete proof are p. 12. Theorem 2.2, p. 5, uses an exponential moment of ξF for small-rate extinction. Theorem 2.4, p. 6, assumes both offspring and fitness unbounded and gives sufficient heavy-tail conditions for strong survival at every rate. These are survival claims within the standing finite-mean domain.
* **v2:** The model, pp. 3–4, samples joint iid offspring/fitness pairs and allows dependence and F>0. The standing finite-mean sentence moves to p. 4; Theorem 3.2 is p. 11. Main Theorem 2.2 uses E[F(1+cF)^ξ]<∞ for some c>0. Theorem 2.3 uses divergence of all indicated mixed moments above an offspring/fitness cutoff, with cutoff ξ≥3. Lemma 5.1, pp. 20–21, explicitly concerns infection reaching a vertex by time 2r, a cumulative event. BKV's 2023 preprint appears in the bibliography.
* **v3:** The same scope and main cutoff ξ≥3 remain on pp. 3–5; finite mean is p. 4 and Theorem 3.2 p. 11. The shortened extinction argument and smaller manuscript do not produce an infinite-mean explosion theorem. The path lemma is pp. 16–17. Full final strong-survival proof and references were read, pp. 35–38.
* **v4:** Model pp. 3–4 explicitly allows zero offspring, still joint iid with positive fitness. Finite mean is p. 5 and nonexplosion Theorem 3.2 p. 11. The strong-survival cutoff is now ξ≥7. The proof uses reverse Fatou for root returns at arbitrarily large times (pp. 38–39), not a finite accumulation horizon. BKV's 2026 publisher article and Valesin's 2024 lecture notes appear in the references, pp. 40–41.
* **Publisher:** Definition 1, pp. 3–4; global finite mean, p. 4; extinction Theorem 1, p. 4; strong-survival Theorem 2, p. 5; nonexplosion Theorem 3 and complete proof, p. 10. The last main proof, pp. 35–36, aims at positive liminf of root infection probabilities as t→∞ and then strong survival. It additionally explicitly uses finite E[ξ_ϑ] when choosing star distances. These bodies confirm the publisher's finite-mean domain.

The original v1 graphical representation describes directed arrows. Later v4/publisher text describes Poisson processes on undirected edges. This audit does not silently attribute independently directed arrows to that later wording. The accepted candidate convention is independently fixed by the root receipt, and the downward-arrow construction has the required downward clock law. The original v1 and BKV (19) are the appropriate explicit directed-path references.

## Prior-result/candidate implication matrix

The matrix distinguishes a printed theorem, an author's qualified discussion, and a deduction supplied by this audit. A reference string or survival title is insufficient to assert an implication.

| Prior item, actual body locator | Hypotheses relevant to candidate | Exact kind of conclusion | Candidate implication / exact gap |
|---|---|---|---|
| v1 Theorem 3.2, p. 12 | Finite Eξ and finite initial set | Every time has finite infected configuration almost surely | Candidate has Eξ=∞, so outside domain. No converse asserted. |
| v2/v3 Theorem 3.2, p. 11 | Same finite-mean restriction | Same nonexplosion | Same exclusion. Lemma 3.1's domination uses E|C₂|≤(Eξ)^2<∞, which fails for candidate. |
| v4 Theorem 3.2, p. 11; publisher Theorem 3, p. 10 | Same global finite mean | Same nonexplosion | No contradiction or competing infinite-mean theorem. Exact statement and proof checked. |
| v1 Theorem 2.2, p. 5 | Exponential moment of ξF; global finite mean | Extinction for small λ | Candidate F=1 has no positive exponential offspring moment; criterion fails. |
| v2/v3/v4 Theorem 2.2, p. 5; publisher Theorem 1, p. 4 | E[F(1+cF)^ξ]<∞ for some c; global finite mean | Extinction for small λ | Criterion fails for candidate, but failure alone never implies explosion. |
| v1 Theorem 2.4, p. 6 | Unbounded fitness and offspring, prescribed tails, global finite mean | Strong survival at all λ | F=1 and infinite mean violate hypotheses. Strong survival is not common-time explosion. |
| v2/v3 Theorem 2.3, p. 5; v4 p. 5; publisher Theorem 2, p. 5 | Mixed-moment divergence, cutoffs3/7; global finite mean | Strong survival at every λ | Candidate meets divergence/cutoff but violates the global finite-mean domain. Applying a displayed condition without its standing assumptions is invalid. |
| v1 Lemma 5.1, pp. 23–25 | Finite path, fitness assumptions | v1 prints infection at 2r; the successful-transmission event in proof controls arrival by 2r | No bounded common horizon as r→∞; no infinite population conclusion. Later versions use cumulative formulation. |
| v2 path Lemma 5.1, pp. 20–21; v3/v4 pp. 16–17; publisher Lemma 3, pp. 14–16 | Finite path | Vertex belongs to union of infection sets up to 2r | Reaching-by event, not necessarily present at deadline. r-dependent deadlines diverge. |
| Original full star/return proofs: v1 pp. 23–40; v2 pp. 19–41; v3 pp. 15–37; v4 pp. 15–39; publisher pp. 14–36 | Finite-mean tree; fixed large stars | Persistent infection and repeated returns at arbitrarily large times | Long-time persistence does not supply summable travel times plus a common-time recovery guard. |
| 2406.12689 v1 Theorem 3.1, p. 6; v2 p. 6; exact proof v1/v2 pp. 27–28 | Degree penalisation/update weighted bounds | Nonexplosion at every rate; small-rate extinction | Its nonexplosion corollary regimes require substantial degree suppression. Classical p≡1 does not satisfy the displayed α≥1 or ασ≥1/2 conditions. It does not refute candidate. |
| 2406 v1/v2 Theorem 3.4, pp. 7–8; v2 proof pp. 45–54 | Infinite mean explicitly permitted, p/v tail constraints | Strong survival or finite survival threshold | Classical specialization can give survival, but the theorem body still has no common-time infinite configuration conclusion. |
| 2406 v1 pp. 15–16; v2 p. 16, “Explosion” discussion | Classical offspring mass exponent b∈(1,2) | Qualified expectation and specified BKV-ray proof route to finite-time explosion | Candidate b=5/4 fits. Explicit prior anticipation of regime/mechanism. Not a printed exact quantitative theorem. Must cite. |
| BKV Definition 1.7, p. 6; Proposition 6.2 and complete proof pp. 46–48 | Positive offspring, weak power-law tail α, α+μ<1 | Printed global survival of a downward degree-penalised infection ray | Candidate α=1/4, μ=0 meets algebra. Printed survival statement alone is insufficient. Existing estimates support the audit's explicit bridge below. |
| BKV (19), p. 17; Corollary 3.2, p. 17 | Locally finite graph, independent directed clocks, finite-path witnesses | Minimal graphical process including possible explosion; monotone coupling | Direct model/convention credit, not a new construction to attribute to candidate. |
| `BKV_ESTIMATES_BRIDGE.md`, audit derivation | Existing BKV offspring-pool estimates and α+μ<1 | Positive annealed probability of infinitely many vertices at one finite deterministic time for every λ | Qualitative candidate conclusion follows after supplied time/recovery bookkeeping. Not exact τ,7/30,or all-rates quenched candidate refinement; not a falsely cited printed prior theorem. |
| Fernley–Mörters–Ortgiese 2312.06251v1, Definitions 2.1–2.3 pp. 4–5, Theorems 2.4–2.5 p. 6 | Finite N adaptive/nonadaptive Erdős–Rényi graphs | Cumulative epidemic set grows to a positive fraction of N or stays tight | Different model/limit and observable. Does not give infinitely many simultaneous infections at finite time on fixed infinite-mean tree. |
| Cardona–Tobón–Pardo 2024 Springer article, actual Introduction/SDE and Theorem 1.1 | Continuous-state branching mass driven by Lévy environment | Conservativeness and nonexplosion probabilities of [0,∞]-valued mass | Infinite “mass” is a different event/model. No contact-process reduction theorem was identified or asserted. |

## Why the later author discussion matters

There are two common priority errors in opposite directions. The first is to declare the problem already solved merely because the earlier theorem says survival at every rate. Ordinary supercritical contact processes on bounded-degree trees survive strongly while finite-mean nonexplosion holds, so that implication is false. The second is to declare the mechanism new because BKV's proposition is labeled survival rather than explosion. The original authors explicitly identify that very proposition as an explosion route in 2024, and its proof has rapidly growing degrees and rapidly decreasing failure probabilities.

The complete BKV proof was checked at the level needed for the bridge: an infected vertex of offspring L has, with probability at least 1−exp(−L^a/48), a pool of order L^a children with offspring between L^{s₁} and L^{s₂}; infection rates into that pool yield a growing-degree ray when δ=a−μs₂>0. BKV's printed race-with-recovery argument proves a positive probability for such a ray. It does not print a summable deterministic deadline or the candidate's simultaneous recovery window event. See [the actual publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0C2D174326F5BB7EFDC7DADE9E768D56/S2050509425101448a.pdf/degreepenalized_contact_processes.pdf), pp. 46–48.

The audit bridge preserves the earlier degree-pool estimates but chooses the ray using the tree and arrows before inspecting recoveries. With L_m≥K^{s₁^m}, it uses deterministic intervals ℓ_m=K^{−(δ/2)s₁^m}. The sum of stage failure probabilities becomes small for large K, and both ∑ℓ_m and ∑(m+2)ℓ_m are finite. Keeping the root and every ray vertex recovery-free through the common τ=∑ℓ_m costs exp(−∑(m+2)ℓ_m)>0. Every infected vertex at τ has a finite path witness. This is a complete qualitative common-time deduction from the prior estimates, with degree+1 and integer-pool constants handled explicitly.

For the candidate α=1/4, μ=0, the admissible choices s₁=3/2, s₂=2 and ε=1/64 give a=δ=77/128. They satisfy the tail-separation condition ε<α(s₂−s₁)/(s₂+s₁)=1/28 preceding (100), as well as (106). Root's independent check identified an earlier audit choice ε=1/16 that violated the first condition; the authored bridge and this report were corrected while the earlier primary comparison freeze remains a dated record. Thus the older argument's quantitative estimates already encode the qualitative answer in exactly the candidate's regime. The candidate remains a clean, explicit quantitative construction with a useful fixed deadline and numerical lower bound; this report does not certify originality or research significance of those refinements.

The quenched all-rates claim has additional quantifiers. An annealed positive-probability statement does not automatically become a positive quenched statement on almost every tree for every real λ. The candidate's hereditary subtree argument and countable rational-rate intersection supply that step. Related authors' Lemma 5.2, 2406v2 pp. 20–22, uses the familiar branching/self-similarity mechanism for survival thresholds. That is appropriate prior conceptual credit; the lemma's printed survival observable is not an automatic theorem about explosion deadlines. No uniform quenched τ or probability should be attributed to it or to the candidate.

## Exact OWR question and neighboring questions

The official full contribution occupies printed pp. 618–620, corresponding to PDF pp. 42–44. The separate next contribution starts on p. 620 after the original authors' references. A bibliography page that lists 618–621 is not a correction to these observed boundaries.

The question on p. 619 is: “Can we get an explosion if E[ξ] = ∞?” Its immediate context contrasts the authors' standing finite-mean assumption, which guarantees finite infection sets at every time. A construction of an infinite-mean offspring law with positive probability of an infinite configuration at one finite time therefore gives a truthful affirmative example for that historical question, under the accepted graphical extension. The words do not require a universal infinite-mean criterion. They do not require F to be nonconstant; F≡1 is explicitly included in the source model. See [the official report](https://ems.press/content/serial-article-files/46949), printed pp. 618–620.

The neighboring questions must remain separate:

| OWR location | Question | Relationship to this candidate |
|---|---|---|
| p. 619 | Close gap between phase-transition criteria | Candidate is not a complete mixed-moment survival criterion. |
| p. 619 | Weaken lower fitness bound one | Later author models already allow F>0 and dependence; candidate's F≥1 comparison does not resolve the general weaker-fitness problem. |
| p. 619 | Infinite-mean explosion | Candidate supplies a precise affirmative example. The later 2024 discussion and BKV estimates preclude unqualified firstness framing. |
| pp. 619–620 | Bounded offspring, sufficiently heavy fitness, no phase transition | Separate survival question. Later v4/publisher Theorem2 allows bounded offspring≥7 and a fitness law with every positive moment infinite, which yields examples within its finite-mean scope. Candidate has unbounded offspring and constant fitness, so is not such an answer. |
| p. 620 | Extend results to finite random graphs with general degrees | Candidate is an infinite-tree theorem. Specific later adaptive finite-graph results do not turn it into that general extension. |

Two visible textual cautions were verified, but do not drive the explosion conclusion. The exponential-moment inequalities in the background summary on OWR p. 618 are reversed relative to their stated tail descriptions and the main source bodies. The main criterion text on p. 619 is distinct. Also v4 Remark2.5/publisher Remark2 use survival language for the exponential-moment classical case although their extinction theorem immediately states the opposite. Neither typo licenses a new explosion or novelty inference. The correct exact theorem bodies govern this comparison.

The v1 path lemma prints a probability at time 2r, while its displayed successful-transmission event only assures a visit by 2r; later versions explicitly use the cumulative union. This is important evidence against sliding from “infected by a deadline” to “still infected at that deadline.” It is recorded as a local formulation difference, not used to dismiss the later survival paper.

## Search bounds and remaining priority gaps

The seven actual query strings, visited primary URLs and read scopes are in `SEARCH_RETRIEVAL_LOG.json`. The search followed exact author/title/arXiv/DOI questions, original references and the authors' public research pages. Cardona–Tobón's public bibliography identifies the original paper, 2406.12689 and a separate CSBP explosion paper. The Bath portal identifies Ortgiese's related adaptive finite-graph paper and the correct personal homepage. An obsolete/guessed Bath research path resolved to a generic university homepage; this is preserved as a failed bibliography locator, not treated as evidence of no publications.

The direct DOI web-open initially failed. This is not an essential source gap: the actual publisher page and actual publisher PDF were available, the latter independently hashed and completely read. Both intermediate original versions were available and completely read. No original essential version is missing.

The Bath portal's 2406 accepted-manuscript entry gives 41 pages and an inaccessible/embargoed institutional file; the official public arXiv accepted v2 has 55 pages. Those files were not assumed equal. No distinct final publisher file for 2406 was obtained. This remains a bounded gap if someone wants to attribute a final publisher statement to that article; it does not erase the verified 2024 v1 discussion or the completely read public accepted version.

The entire citation graph of the original papers, every earlier contact-process textbook/paper, all arXiv revisions of BKV, and all author theses/seminar materials were not exhaustively read in this family. These are explicit limits. An absent search hit, unvisited bibliography entry, inaccessible file or unchanged abstract cannot establish firstness or current openness. The BKV-specific priority/version family and other independent families remain responsible for their own bodies and conclusions; their reports were not borrowed to manufacture a fuller reading claim here.

The exact remaining priority gap is whether the candidate's particular deadline, simple constants and simultaneous finite-time/quenched presentation already occur elsewhere or are a sufficiently substantive original refinement to merit research promotion. This family supplies no clearance for that claim. The documented prior author anticipation and the existing-estimates bridge are affirmative reasons to retain HOLD on broad novelty, rather than merely a failure to find evidence.

## Reviewable framing and deliverables

A truthful concise note can present the result as an explicit quantitative construction in the classical special case of the OWR model, credit the historical question to Cardona–Tobón and Ortgiese, credit the graphical extension and growing-degree ray to BKV, and credit the later Cardona–Tobón–Ortgiese–Seiler–Sturm discussion for already identifying this regime and route. Its added presentation consists of an explicit offspring law, deterministic time, numerical probability bound, recovery persistence at a common time and the precise accepted quenched quantifiers. It should avoid a first-solution title and avoid describing the question as still open today. The immutable-source promotion decision remains HOLD unless a separate priority/significance gate is satisfied.

Checkable deliverables in this owned folder:

* `AUTHOR_VERSIONS_PRIORITY_REPORT.md`: this authored comparison.
* `BKV_ESTIMATES_BRIDGE.md`: complete audit deduction of the qualitative common-time implication with adversarial checks.
* `PRIOR_RESULT_CANDIDATE_MATRIX.json` and `CHRONOLOGY.json`: structured comparison and dated events.
* `INPUT_MANIFEST.json`, `PRIMARY_MANIFEST.json`, `OUTPUT_MANIFEST.json`: exact input, actual source and output receipts.
* `READ_VISITS.jsonl`, `READ_COVERAGE.json`, `VISUAL_MANIFEST.json`, `FULL_BODY_LOCATORS.json`: actual visits and complete-body pins.
* `SEARCH_RETRIEVAL_LOG.json`: reproducible search/retrieval boundaries and failed/limited leads.
* `PRIMARY_COMPARISON_FROZEN.json`: pre-sharing independent comparison, SHA256 `586f0b647b984ea7b4816a6989902b9e58a181a8f1c90a3c31cc8ab2f5b79ad0`.
* `tools/verify_locators.py` and `LOCATOR_CHECK_RESULTS.json`: reproducible byte, complete read-coverage and exact body-locator checks. They verify provenance and locations, not mathematical novelty by automation.

The root was notified after the independent primary freeze about the later author discussion, then about the separately authored bridge. The bridge requires adversarial review during integration as a new audit derivation. No external outreach is proposed or prepared; any possible benefit from outside expert input is only a research-note fact and can be pursued solely by the human user.
