# Soccer scores: a decisive-match kernel and a theorem correction

Problem 3000026 / AMR-029-0026. Prose edition dated 2026-10-11.

**PARTIAL. General complete-host 3–1–0 score-vector recognition remains unresolved by this work.**

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. Novelty and priority are unestablished; no exhaustive current-openness claim is made.

## Exact target and results

Each of n teams plays every other team once, receiving (3,0), (0,3), or (1,1) in each match. The target asks for a polynomial-time test of the full integer score vector, with no preassigned matches or arbitrary host graph.

The complete report proves an integral-flow criterion when the draw graph is fixed; an incidence-budget kernel of at most 2m teams, where m is the number of decisive matches; an exact 2^{O(m log(m+1))} recognition algorithm with witness reconstruction; and the deviation patterns for m≤2. It proves holes in the convex hull of labeled feasible score vectors, excluding pure continuous linear feasibility/projection as an exact recognition test. Sorting and other nonlinear preprocessing are outside that obstruction.

The correction concerns only the printed sufficiency direction of Theorem 9 in Pirzada–Samee–Naikoo (2017), pp. 220–221. Its necessary parity implication remains valid. The explicit six-game schedule (3,2,5,5) refutes sufficiency for a prescribed oriented graph. A short contradiction also forces a loss by the 3-point team in every realization of the full vector. The different scalar-existence statement remains true; the paper as a whole is not rejected.

## Complete arguments and supporting records

- PROOF.md combines the entire accepted mathematical report and the entire correction note, including every essential match outcome and the all-realizations proof.
- AUDIT.md contains the full independent internal mathematical audit and its source/computation limits.
- ACCEPTANCE.md and ACCEPTANCE.json state the exact accepted partial scope.
- SOURCES.json preserves source titles, public URLs, version and publication status, byte identities, historical retrieval and inspection scope, and prior credit.
- VERIFICATION.json separates original evidence and historical checks from editorial integrity verification.
- MANIFEST.json lists exactly eight files and hashes the other seven; publication metadata separately pins the manifest.

The creator and independent auditor ran bounded finite checks in normal, -O and -OO Python, including actual semantic and integrity corruptions. The independent audit covered 6,998 sorted inputs through five teams, 10,360 labeled inputs through four teams, 3,194 fixed-host quota cases and sparse six-team cases. Finite checks are supplementary; the partial theorems are proved in prose. The edition preparer did not rerun the mathematical programs or inspect new source bodies.

Prior standard identities and flow arguments are credited, and the (1,1,7,7) draw-pairing obstruction is explicitly credited to Iványi–Schoenfield (2012). The bounded search is no novelty, priority or worldwide-current-status certificate. The unresolved issue is choosing a compatible draw graph efficiently for arbitrary complete-host inputs.

Only authored prose and public verification metadata are distributed. Code, raw scans, datasets, copied scholarly sources, source-page images and private coordination are excluded. The compact six-game counterexample is indispensable mathematical proof, not a dataset distribution.
