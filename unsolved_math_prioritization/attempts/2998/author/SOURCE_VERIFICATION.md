# Source, identity and proof-scope verification

Checked on 2026-10-05. All source PDFs and extracted text were used privately and are excluded from the authored packet.

## Identity and live duplicate checks

- Requested entry: https://www.unsolvedmath.com/problems/2998 . Direct retrieval failed (web access error; direct HTTP 403). This is a disclosed retrieval limit, not an assertion that the page was read.
- The search-index rendering of the catalog's topology/difficulty listing identifies KP-4.122 with the fixed-surface question in S^4: https://www.unsolvedmath.com/problems?category=7&difficulty=3&page=7 . Its cached status is Open. This is indexed corroboration, not a fresh full catalog-page retrieval.
- The live repository queue at `unsolved_math_prioritization/QUEUE.md`, line 706, identifies rank 695 as ID 2998 / KP-4.122, queued, 0/5. The observed Git blob SHA was `5d33a968894980499cb3fbb6d84fe5cca5a47aa4`.
- A pre-existing local copy of the public repository catalog was read without downloading a new corpus. Its computed Git blob hash exactly matches the live connector-reported catalog blob `bd5c23e4e6c7e1901717a7e596477a7f6dc72425`. The selected record matches ID, modern label, title and rank. No catalog text or record is included in this packet.
- Live repository searches returned no PR for `2998`, `"4.122"`, `"universal branching"`, or `"2998" in:body`; no code search match for `2998` or `universal branching`; no branch for `2998` or `4-122`. A fully paginated `kirby` branch search returned other targets, not this one. The expected target README path returned 404. These checks found no previous attempt; they are not a claim of omniscient detection under unrelated names.
- The public dataset manifest was read live. Its original corpus hashes and sizes are reported metadata only. Neither full dataset file was downloaded or rehashed for this task.

## Modern K3 primary

Title: *K3: A New Problem List in Low-Dimensional Topology*, by Baykur, Kirby and Ruberman. Retrieved the April 2026 public author PDF from its UMass-hosted URL. It has 436 pages; its embedded metadata reports creation April 1 and modification April 15, 2026. Computed SHA-256 and byte count are in `SOURCE_METADATA.json`.

The exact item is Problem 4.122 on printed/PDF pages 291–292. Both pages were rendered and visually inspected. They ask for a fixed branch surface in S^4; the companion remarks concern a four-ball ribbon construction and the disconnectedness obstruction. This is modern K3 numbering. The older 1997 numbering must not be substituted.

The book's one-sentence question does not explicitly state smooth/PL conventions. The originating paper and cited representation theorem establish the intended smooth/locally flat PL research setting. The authored results state that setting explicitly and distinguish the topological locally flat extension. They do not exploit an unstated categorical reinterpretation to declare a solution.

The book prohibits reposting its author version. No page image, PDF, or extracted text is in the authored packet.

## Piergallini–Zuddas

The publisher DOI confirms the 2005 paper and its journal pages. The inspected 19-page arXiv version is v1, August 24, 2003; it is not mislabeled as a newly published result. Its introduction specifies a compact orientable total manifold built with handles of index at most two. The map is proper over B^4 and induces a boundary link covering. Its degree and monodromy vary. Its concluding section reduces a displayed five-component surface to a three-component one (annulus and two discs).

Read the introductory definition/theorem, monodromy and local-model conventions, the construction's stated scope, and the concluding questions. The complete diagrammatic construction was not independently reconstructed or certified. It is used as an established source theorem, not as a newly verified universal construction for S^4. The packet's doubling obstruction is independent of its detailed diagram.

## Iori–Piergallini

The inspected nine-page arXiv PDF reproduces Geometry & Topology 6 (2002), 393–401. The theorem on p. 395 gives a simple five-sheeted covering with locally flat PL branch surface; the branch surface depends on the manifold. Read the definitions, theorem, node-elimination construction, and final remarks.

The source's simple-cover Euler/signature expressions are not applied to arbitrary nonsimple covers. The packet derives the general cycle formula separately. The five-sheet theorem is not evidence of one universal fixed surface.

## Viro and the topological extension

Viro's English paper is Mathematical Notes 36 (1984), 772–776. The privately inspected public scan is five PDF pages and includes the beginning of the next article on its final page. Section 2.2 and the displayed formulas (17)–(18) on printed p. 776 were visually inspected. They distinguish upstairs embedded normal Euler numbers, with coefficient (k^2-1)/3, from downstairs immersed normal Euler numbers, with coefficient (k^2-1)/(3k). The original proof is differential-topological and explicitly warns that its proof does not automatically transfer categories.

Geske–Kjuchukova–Shaneson's Theorem 1 supplies the locally flat topological extension for closed compatibly oriented four-manifolds. Inspected arXiv v3, August 29, 2020, and the published journal page. Read Theorem 1 and its proof; visually checked PDF pp. 1 and 7.

Important source-control issue: the final display in that proof writes a 3k denominator against the upstairs self-intersection notation, whereas the theorem statement uses 3. This display-level discrepancy is present in the inspected PDF and journal HTML. The packet uses the theorem statement, independently corroborated in the smooth case by Viro formulas (17)–(18), and explicitly performs the upstairs/downstairs conversion. It does not silently treat the inconsistent display as a second formula. No claim is made that an official erratum was found. The smooth/PL partials do not depend on extending Viro's proof to the topological category on our own.

## Later update checked

Bais–Piergallini–Zuddas, *Branched coverings of simply connected 4-manifolds*, arXiv:2605.26337v2, July 2, 2026, 18 pages. Its actual PDF names all three authors. Read its introduction, Theorem A and associated corollaries and searched for universality language. The theorem characterizes degree-d branched-cover existence over a target N with no 1- and 3-handles by an intersection-lattice embedding, with a variable branch set. It does not state a fixed-surface universality theorem. Its full proof was not independently audited.

Targeted searches through the check date found no primary source resolving the exact universal fixed-locus question. The April book still poses it as a problem. This is a bounded literature check, not proof that no later or unindexed result exists.

## Claims and limitations

The source theorems are cited dependencies. Complete proofs are supplied for the authored deductions from them. The at-least-three-component consequence is not advertised as novel. No proof assistant was used. The exact arithmetic controls support bookkeeping only; they do not prove global monodromy realization or identify smooth structures. The target remains unresolved in this packet.
