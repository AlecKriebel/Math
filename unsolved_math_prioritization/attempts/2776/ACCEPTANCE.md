# Acceptance and correction reconciliation

## Disposition

Accept as authored partial research for KP-2.28 / catalogue 2776 / queue rank 1043. The general problem remains **unsolved**, with **5/5 substantive mathematical routes**. Publication, correction, audit, and replay work add no proof-search turns. Novelty is not established. No merge, release, external outreach, or universal solution is represented by this draft.

## Immutable originals and separate corrected slice

- Original edition: exactly seven files. `original/EDITION_MANIFEST.json` is 1,198 bytes, SHA-256 `00949c87a3adfa815c55af7b95df7e72da00ca64f382f401c0ca97f3ba0c7f19`.
- Independent audit: exactly sixteen files. `audit/AUDIT_MANIFEST.json` is 3,002 bytes, SHA-256 `a87355863db038d44d826d3e7df039c97e5684a8e319da81731008e2823b6d8f`.
- Required correction: apply the actual `audit/VERIFIER_CORRECTION.patch` to `original/verify_exact.py`. Its result is exactly `corrected/verify_exact.py` and the audit's `verify_exact_corrected.py`: 9,712 bytes, SHA-256 `6b624c31b8a061054ad06720798c04bd62a8e359f2077099db40f23cc855f7ae`.
- Accepted scope clarification: apply the actual `audit/SCOPE_CLARIFICATIONS.patch` to `original/RESEARCH_REPORT.md`. Its result is exactly `corrected/RESEARCH_REPORT.md`. It changes only the Runnels dependency paragraph and Proposition 6.2's ambient finite-index wording. The source's boundary-support convention is retained. Mathematical conclusions are unchanged.
- `corrected/CORRECTED_MANIFEST.json` separately binds both corrected files. The wrapper checks both actual patches with exact line contexts and counts, without fuzzy matching or modification of the originals.

## Mathematical scope

The independent report accepts the written Schottky construction, intrinsic ambient-join/connected-domination criterion, conditional support reduction and local gadget obstruction, cycle-cover diagonal failure, P4 free-target obstruction, and finite-cover/restriction arguments within their stated hypotheses. The free case is proved; general RAAG embeddings remain open in this packet. A failed construction route is not a counterexample to all type-preserving embeddings.

Keep finite generation and admissibility in the cited Koberda–Mangahas–Taylor result. Keep extension-graph/rank-one identifications inside their source hypotheses. Filling must concern the whole ambient surface. Runnels' published 2021 support result is not supplied by the inspected 2020 preprint. Extra boundary-twist annuli can break connectedness. Annular twists are not reclassified as ordinary Nielsen–Thurston pseudo-Anosovs. Finite-index restrictions retain loxodromicity in the original ambient RAAG and obstruct only restriction of the same representation. Covers exclude branching, capping, puncture filling, and forgetting marked points.

## Reproducibility findings

The original code contains 15 asserts and yields 10 optimized false passes over five corrupt specimens in each optimized mode. Its unchanged CLI fails at its mandatory neighbor-file write in genuine UID/EUID-1000 read-only directories under normal, `-O`, and `-OO`. Core-function runs are reported separately and must never be called successful unmodified CLI runs.

The corrected code removes the optimization vulnerability, preserves the finite mathematics/result schema, and supplies stdout or explicitly selected external output. Corrected stdout is exactly the 2,985-byte frozen original result (SHA-256 `bb55320a299063cf85efc4c016e55397645a1f9a5e6a919309b9cfface9d9d5c`). The independent result is exactly 999 bytes (SHA-256 `e913bddd1c6602d46492c548100690aa83d6c4ab66d748f253b7b5ef10120c43`). All 15 corrected mutation/mode combinations are rejected.

Finite results: 1,099 labelled graphs; 32,767 nonempty supports; 616 cycle-cover cases; five minimal C5 triples, ten nonempty cliques and zero clique transversals; 2,308 word states with minimum cyclic length 12 and 20 directed inverse arcs; 3,918 sampled cyclic words with minimum absolute trace 47. The independent conjugator is `bac`. These counts corroborate but do not replace the written unbounded proofs. The finite-cover argument is not computationally certified.

The complete native audit contains 42 verifier runs and three independent runs. The publication wrapper preserves and reproduces that audit with strict stable-field equality while validating the three explicitly documented volatile runtime fields. It additionally checks actual read-only write denial, exact inventories and immutable bytes before and after execution. Publication corruption controls run separately from mathematical mutation controls.

## Source boundary

The six public-source PDF matches and five article extraction matches are historical independently checked evidence. Fresh publication replay has no source bodies and reports source binding/re-extraction `NOT_RUN`. The inaccessible Runnels thesis remains announcement-only and cannot certify a proof. Oh–Park's v2 manuscript was screened, not fully proof-audited. A bounded literature search cannot establish completeness or novelty. Source files, text extracts, page images, datasets, private sources, personal data and coordination material are excluded.
