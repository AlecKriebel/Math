# Probability and primary-source family: final scoped report

Completed UTC: 2026-10-02T23:30:16.785962+00:00. Completion estimate for **this independent family audit**: 100%. This is not a claim that the whole PR publication audit has finished.

## Verdict and strongest verified result

The precise status correction to `already_solved` is justified. Johnston, Kabluchko and Prochno's Theorem A states the literal one-dimensional random-probability-measure LDP, and Proposition 3.1 plus the candidate's explicit coefficient construction gives the complete Prohorov limit set. The candidate credits the prior authors and makes no new discovery claim. Independent falsification found no mathematical counterexample to either target and no need to change the candidate's final mathematical formulas, topology or boundary treatment.

This family independently supplied a complete checkable probability derivation in `INDEPENDENT_DERIVATION.md`: corrected finite-coordinate sphere density; local upper bound with ordered coordinate assignments; local lower bound including ties, zero coordinates and residual maximum control; direct finite-cover promotion to a full LDP; compactness and characteristic-function continuity; canonical injectivity; contraction to all of P(R); and attainment of every closed-ball limit. It is an audit derivation of an existing theorem, with no novelty or priority claim.

## Independence and coverage

1. Before any candidate or sibling content, read only the immutable `source_record.json`, applicable AGENTS and the original OWR publisher report's relevant pp. 411–413. `INITIAL_SEAL.md` was sealed at 2026-10-02T23:17:03.932302Z (SHA-256 `1ad9af79dbce7b0554ec980beacd447b257c3c68181797c2159ad128ecb3cadc`). Its compactness, uniform sinc-tail and real-zero injectivity route was reconstructed independently.
2. Independently searched primary literature, downloaded versioned primary files, read the entire 12-page arXiv v2 proof and sealed `SOURCE_VERDICT_SEAL.md` at 2026-10-02T23:22:16.251146Z (SHA-256 `763a8de24d4c1b04276198cc1e51b0517f01a5f06deb2caf94064d24ff5dc578`). Only then read candidate materials.
3. Read all 16 original candidate files in full, including all three helper copies, both author result copies, independent result, review and metadata, immutable source record and the empty turn ledger. No candidate helper was imported, executed or compiled. Read every line of the complete 957-line, 17-path original diff, including the queue mutation, and the snapshot manifest. Original head: `86be0f85c7a37a5cad8d24abd16a32d8d1f27e62`; original diff SHA-256: `7a246eef4c351e42b054ac60afec30d016387b797eb0b8883cfc70f1855211fe`.
4. After both independent seals, read ROOT's separate actual-reproduction `RESULT.json` and `ACTUAL_RUNS.json`. This later exposure does not supply the earlier mathematical/source mechanism and is explicitly distinguished from this family's own executions.

## Exact source and topology match

For independent U_i uniform on [-1,1] and independent standard normal Z,

    κ_a = law(Σ a_i U_i + sqrt((1−||a||₂²)/3) Z), ||a||₂≤1.

The series is L² and almost surely convergent. Every such law has variance 1/3. The random object is ν_N=μ_{Θ^(N)} as a point in P(R), where the direction is uniform on S^(N−1); the random measure's distribution obeys the LDP at speed N. It has finite rate −½log(1−||a||₂²) for norm below one and infinite rate otherwise. The only zero is N(0,1/3). The original report explicitly names Prohorov for its intermediate lemma; the main conjecture paragraph does not separately specify the topology, while the later theorem explicitly uses weak topology. Weak convergence and Prohorov convergence agree on P(R).

The canonical domain is W={a₁≥a₂≥…≥0, Σa_i²≤1} with coordinatewise topology. Its image K is compact in weak topology. The canonical characteristic-function zeros establish injectivity, so signs/permutations cause no ambiguous rate. The complete limit set is K; the finite-rate domain excludes norm-one coefficients. K's compactness is compactness of a set of measures, not a claim that every scalar law has bounded support. Some norm-one ℓ² coefficients are not ℓ¹ and produce unbounded scalar support.

A quenched scalar LDP concerns a sample conditional on a direction, and an averaged/annealed scalar LDP concerns the direction-averaged sample. A direction law LDP concerns the direction itself. Those objects do not replace the required random-law theorem without a proved continuous map. Theorem A is a **full** LDP in **weak topology**, not merely a weak LDP. Fixed projection dimension one is the exact target; a fixed-k generalization is not a theorem for arbitrary growing k(N).

## Primary publication, version and access distinctions

| Primary source | Independently verified facts | Reading/access limit |
| --- | --- | --- |
| [OWR publisher](https://ems.press/journals/owr/articles/17469), DOI 10.4171/OWR/2020/6 | Workshop 2–8 February 2020; volume 17 (2020), no. 1, pp. 377–416; target pp. 411–413 | Original report PDF downloaded; relevant target and p. 412 rendered display read. Publisher visible date is 10 February 2021; machine citation date is 2021/02/09 and timestamp is 2021-02-09T23:45:03.000Z. Preserve that display/UTC metadata distinction. |
| [JKP arXiv](https://arxiv.org/abs/2103.16430) | v1 submitted 30 March 2021 15:25:18 UTC; v2 revised 19 September 2021 19:52:59 UTC | v1 theorem statement inspected; whole v2 proof read. Both PDFs preserved individually. |
| [JKP publisher](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/264/1/114493/projections-of-the-uniform-distribution-on-the-cube-a-large-deviation-perspective), DOI 10.4064/sm210413-16-9 | Authors/title, Studia Mathematica 264 (2022), 103–119; online 17 December 2021; exact theorem's formula in publisher abstract | Public journal PDF endpoint returned HTML. Proof verification is arXiv v2 plus independent derivation; no journal-proof reading or byte identity is claimed. |
| [Kabluchko–Prochno arXiv](https://arxiv.org/abs/2110.12977) | v1 25 October 2021; v2 28 October 2021; v3 3 November 2022. Fixed-k matrix and product-measure theorem statements generalize the target | v3 main-result statements inspected, not the whole 41-page proof. DOI 10.1214/22-AIHP1340 access returned an anti-bot response. It is corroboration; no journal proof or precise journal publication date is certified here. |
| [Kabluchko–Prochno–Thäle arXiv](https://arxiv.org/abs/1910.02676) | v1, 7 October 2019, Theorem 1.3 is an almost-sure scalar-law LDP after n^(−1/2) projection scaling | Relevant v1 definitions and theorem inspected. v2/v3 PDF requests returned 406. Its scalar rate cannot substitute for the target measure-valued rate. |

Independently fetched candidate source URLs reproduce both frozen source hashes exactly: MFO report 490099 bytes, SHA-256 `908283ff96b6ee7d710e14f817f263f62d50d467114b2723cb50f4de86fbc3e0`; JKP v2 160880 bytes, SHA-256 `895649b83af8609a638d77f18baa00890952196b429c3304cba7721815e310cd`. A separate EMS publisher report capture has a different file hash/size; these are separate primary representations, not a silent replacement of the candidate's frozen MFO bytes.

## Adversarial source-proof findings

The source identification is valid, but the accessible primary texts contain defects that should not be blindly transferred into a proof certificate:

- OWR p. 412 prints density exponent (N−k−1)/2 rather than (N−k−2)/2, and its normalized log-density display omits the logarithm and uses an incorrect outside sign. The final conjectured rate is correct. This was visually checked.
- JKP v2 p. 4 says variance one in prose after its defining equation; its equation, theorem and publisher abstract give variance 1/3. The candidate already records and corrects this.
- JKP v2 Lemma 3.3 p. 7 divides by the full limiting characteristic function, which can be zero. Uniformly control the nonzero tail and multiply by the finite prefix instead. The independent derivation includes this repair.
- JKP v2 p. 10's factor 2^m binom(N,m) misses m! for ordered assignments. Use 2^m(N)_m. The omitted fixed-m factor changes a finite-N bound but has zero logarithmic cost at speed N. The independent derivation includes it.
- Zero final prefix coordinates need positive perturbations tending back to the target; ties need a strict ordered wedge of positive volume. The independent derivation explicitly treats both.
- ROOT later independently flagged Proposition 2.2's unrestricted converse from full LDP to exponential tightness as overbroad. A constant full-support Gaussian sequence at speed N has a full LDP with zero rate on R but is not exponentially tight. This is a checkable counterexample. The target proof uses compact W, and the direct finite-cover proof here bypasses that converse entirely. This later corroborating finding was not in either earlier seal.

These findings do not invalidate the candidate's status correction. Its old review explicitly declined a reconstruction of every source proof estimate; a publication statement must retain that limit instead of interpreting old PASS as a formal proof certificate.

## Execution and provenance disposition

This family's only candidate-related execution was its own **read-only source/byte predicate** process. Initial child PID 23183 exited 0, with 43 of 44 predicates true; the failed predicate was this family's wrong ISO spelling for the OWR visible date. Its complete streams remain preserved. Corrected child PID 24098 exited 0 with all 44 finite predicates true, including all original file identities, all added diff bodies, source hashes and accessible-source text predicates. Those predicates do not prove an LDP or a historical execution. The first source program was later reconstructed by reversing the family's own edit; its SHA-256 exactly matches the genuine first-run prelaunch hash and its reconstruction is explicitly labeled after-execution, not falsely represented as a prelaunch save.

ROOT's later actual unchanged reproductions ran the current author helper (PID 17872), historical author helper (PID 17873) and old independent helper (PID 17877), each exit 0. The historical 527-assertion receipt and independent 664-assertion receipt are byte-exact; the current author's entire output differs only in `source_status_sha256`. ROOT's actual Git retrieval of the historical source (PID 17871) confirms frozen hash `98918841ab30dd1e41d51dbc7ec8515a66f1f1c82f01ff08ccc5462b758a2727`; the final `90402aea80b79b7713d740863b6058b43c64050c3499701b2bf8490c90b210e3` differs by exactly one review-status sentence. This resolves the receipt version difference. It verifies reproducibility now, not the claimed 30 September execution timeline, model configuration or historical native permissions.

Mandatory provenance/workflow repairs before promotion of a current package:

1. Qualify/correct SOURCE_AUDIT's claim that shared queue/state files were not edited: the original 17-path diff changes QUEUE.md. Keep the immutable old snapshot and archived old review intact.
2. Treat pending/completed review sentences, model/reasoning/deadline values and old PASS as historical fields. Do not transfer them to a fresh review of an expanded artifact or current publication state.
3. Describe saved diagnostics as results for the frozen historical source hash, and current reproduction as the separate actual run above. A current author run is not byte-identical to the old receipt because its bound source hash changes.
4. Correct the claimed null research-results lookup. ROOT's actual whole importer check reports the raw OWR-17469-011 key absent and SQL `{}` as fallback; neither certifies a retrieved null. This family read ROOT's scoped result after its independent seals and did not itself execute the importer.

## Remaining gap and closure boundary

No mathematical gap remains for the exact theorem/limit-set source match under the stated assumptions. Remaining publication work belongs to ROOT: apply the provenance precision changes, reconcile all other families and perform the current whole-scope review. This report does not certify future files, native state, remote publication, a new research budget, a paper or a DOI.

All family files stay in this dedicated directory. `SELF_MANIFEST.json` lists only this family's artifacts, bounds each by its own hash and labels every foreign file separately. Foreign PDFs, extraction text, screenshots, HTML pages and access responses are retained primary evidence and excluded from authored-science and novelty claims. Candidate snapshots and ROOT execution artifacts are referenced as outside-family evidence; they are not silently copied into this family's authored artifact set. No Git/native/remote write, candidate helper execution or communication with an outside individual was performed by this family.
