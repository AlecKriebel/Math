# Source, scope, and prior-attempt audit

Checked 2026-10-05 UTC. This is a bounded source audit, not a priority certificate.

## Identification

The catalog, complete cached problems dataset, and complete cached research-results dataset were reread and hashed. Exactly one catalog row and one problems row match ID 30005902 and code OWR-14298370-002. The statement hash and full-record review hash both recompute exactly. There is no exact research-results key for this code; the empty-object default reproduces the review hash. These facts identify the target; the catalog's “open” triage does not prove mathematical status. See `DATASET_IDENTITY.json`.

The requested unsolvedmath entry was tried first. The web reader reported it inaccessible, and direct HTTP retrieval returned 403. Its live contents were not inspected. The independently retrieved publisher report supplies the primary mathematical context.

## Primary report and exact scope

Witherspoon's contribution occupies printed pp. 1114–1117 of OWR 20/2024. Its cohomology is self-Ext of the monoidal unit; for H-Mod this means Ext_H(k,k). The bracket lowers total cohomological degree by one. The question appears on p. 1116. The general Hopf-algebra setup is over a field without an explicit characteristic or finite-dimension restriction. The text mentions finite-dimensional restrictions as optional for restricting modules. The bijective-antipode hypothesis enters the subsequent comparison with Hochschild cohomology. Printed p. 1116 was visually checked after local rendering, as well as read in the extracted text.

The quasitriangular/braided vanishing assertion and the known Taft/quantum-elementary-abelian examples do not imply vanishing for every non-quasitriangular Hopf algebra. The paper's separate Gerstenhaber–Schack contribution is not the object of this problem.

## Bracket comparison and conventions

Karadağ–Witherspoon §2 assumes a bijective antipode, not a characteristic-zero field or finite dimension. Theorem 4.1 identifies the induced Hochschild bracket with the homotopy-lifting bracket. Its author-PDF page 8 was visually checked. Karadağ §5 gives the explicit induced bar comparison used to fix the right-translation convention in `PROOF.md`.

Farinati–Solotar's older preprint gives a left-translation embedding. The two degree-one conventions reverse the convolution commutator. Both give nonvanishing for a nonabelian translation Lie algebra, but the packet uses the orientation of the comparison specified in the OWR report rather than conflating them.

## Literature and novelty limitation

The publisher report, the two Karadağ papers, Farinati–Solotar's preprint, and the current author publication pages were checked. Searches included the problem's topic with 2025 and 2026, “nonzero bracket,” coordinate algebras, and nonquasitriangularity. No direct published resolution of a specifically finite-dimensional characteristic-zero formulation was established by these checks.

A 2019 answer by Marco Farinati explicitly relates degree-one Hopf cohomology, invariant derivations, and the Lie algebra of a coordinate group. This is prior public explanation of the underlying obstruction and further rules out claiming that this packet discovered the general mechanism. The source is recorded for historical attribution, not substituted for the proof or the published comparison theorem: https://mathoverflow.net/questions/310314/lie-algebra-of-a-compact-lie-group-and-derivations-of-the-hopf-algebra-of-repres .

The author's conclusion is therefore a scope-qualified counterexample to the literal wording, not an assertion of a new solution to every intended restricted version. Editorial intent cannot be established from this packet.

## Actual repository checks

Exact-ID PR, branch, commit and default-branch code searches returned no matching prior artifact. Broader Hopf PR and branch searches returned unrelated problems, including 30004831, which concerns monoidal invariance of cohomological dimension rather than this bracket. The Hopf branch search was paginated to its empty final page. Default-branch code and commit topic searches did not locate a matching artifact. A direct read of the target attempts path returned 404. Additional pinned tree evidence is recorded in `REPOSITORY_CHECKS.json`.

These are actual artifact searches, not a decision based on the queue's unattempted status. They do not exclude deleted work, unindexed content, inaccessible repositories, or differently named attempts. The complete cached research-results dataset also lacks this exact problem key.

## Research budget and stopping point

The source and duplication gate was followed by one substantive approach: calculate augmentation-derivation brackets through the published bar embedding and realize a nonabelian bracket in a finite truncated coordinate Hopf algebra. The displayed counterexample and nonboundary certificate closed the unrestricted question, so proof search stopped. No additional approach was charged or represented as attempted. Independent review remains pending.

## Source-byte custody

`SOURCES.json` lists public URLs, titles, byte counts, hashes and inspection limits. Scholarly PDFs, extracted text, page images, raw connector responses, dataset records and full corpora are not included in this packet. A paper's preprint or author PDF is not represented as an inspected final journal PDF. The source report itself was read from the publisher PDF.
