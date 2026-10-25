# Zenodo eligibility and edition reconciliation

Completed 2026-10-24T23:37:02.931535+00:00. Reconciliation subtask completion: **100%** at this snapshot. This is an eligibility and source-identity audit, not mathematical review completion.

## Reconciled scope

- **203 distinct eligible works**: 201 direct-paper works and 2 explicitly named paper releases whose manuscript is inside the Zenodo ZIP.
- The existing spreadsheet has **244 document rows**: 202 eligible canonical rows, 6 edition/presentation aliases, and 36 excluded rows.
- One new published paper is absent from the spreadsheet: **23624706**, “Locally finite p-groups in Golod groups and an AT section”, version 1.0.0, published 24 October 2026. Proposed row 251/index245 leaves all impact and journal-assessment fields empty.
- All **226 owned published records** are accounted for. Three independent unauthenticated author-identity searches have an exact 226-record union: no outside records and no owned published record missing. One unpublished account draft was omitted entirely.
- All **212 local PDF source files** used by eligible canonical queue entries passed fresh size, MD5 and SHA-256 checks. Direct-paper advertised MD5 and sizes were checked against the refreshed account metadata. Archive manuscripts retain the previously verified public member CRC32, size and SHA-256 plus fresh archive metadata comparison; the full large ZIP MD5 was not recomputed.

## Eligibility rule

Include a published record that explicitly releases the paper by title and description, with the manuscript itself as a file or a verified member of that release archive. Do not require a top-level PDF if the intended paper is unambiguous. Exclude a manuscript that happens to be bundled in an unrelated monorepository snapshot. The user explicitly excludes unpublished Keller papers; their incidental appearance in unrelated old ZIP snapshots does not override that instruction. The exclusion record preserves this distinction rather than inaccurately saying those bytes were never on Zenodo.

Repository concept DOI 10.5281/zenodo.21753404 groups unrelated GitHub releases. It is not a scientific work identifier and must not merge all archived papers into a single work. Editions were grouped by paper identity, published title/description, and existing manuscript adjudication. All 226 published records have an explicit disposition in queue.json.

## Necessary spreadsheet corrections

- Row **57**: reversible mass-action continuum is explicitly published in named release **21753997**, version2.0.0, 2026-08-02. Replace the incidental 22625980 archive reference with its real named-release DOI and exact v2 manuscript member. Earlier 21753527 is the v1 release.
- Row **109**: simultaneous amplification below three halves is explicitly published in named release **21850042**, release version simultaneous-amplification-below-three-halves-v1.0.0, 2026-08-08. Replace the incidental 22625980 reference with that release and exact manuscript member.
- Append new paper **23624706** at row251/index245 using spreadsheet-proposals.json. Its existing local publication/paper.pdf exactly matches the published file; no bulk download is needed.
- Pilot **23575190** is existing row **24**, inventory index41. Its page is already live; the root workflow is revalidating that state. No new paper review is claimed by this reconciliation.

Exact proposed cell-range values are in spreadsheet-proposals.json. This agent made no spreadsheet, site, Git, or Zenodo mutations.

## Edition and presentation aliases

| Sheet row | Existing entry | Canonical record | Basis |
|---|---|---|---|
| 34 | An exceptional four-dimensional unitary Hecke Yang–Baxter operator | 22013710 | True older version in concept21971506; later edition adds Pauli–Clifford normal form. |
| 44 | Full-Dimensional Jukes–Cantor Ambiguity in Weakly Tree-Child Level-2 Networks | 22089373 | Earlier ambiguity/sharp-boundary manuscript is a historical edition in the same JC identifiability paper line. |
| 48 | No universal death–birth amplifier on a finite weighted population structure | 22089748 | Paper I fixed-graph strong-selection obstruction is subsumed by the current complete-graph/strong-selection paper; retain its separate historical publication artifact. |
| 52 | Simultaneous amplification beyond fitness three halves | 22089807 | Earlier above-three-halves amplifier manuscript is superseded by the current fitness-independent family paper. |
| 79 | An Exact Full-Dimensional K3P Tree–Theta-Trinet Collision | 22136869 | Earlier K3P-only collision manuscript is incorporated into the later combined K2P/K3P collision paper; preserve as an older edition. |
| 248 | Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation | 21699161 | Line-numbered review presentation of the same qubit Bell-setting paper, distinct Zenodo concepts. |

## Exclusions

These rows remain in the spreadsheet with an exclusion status. They are not silently deleted. A historical attempted extension already recorded as rejected is not reclassified as a new peer-reviewed or published paper.

| Sheet row | Manuscript | Reason |
|---|---|---|
| 13 | Full wreath-product monodromy through the third iterate of an explicit Keller map | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 15 | Positive Recurrence for Bimolecular Weakly Reversible Stochastic Reaction Networks with Three Species and Two Linkage Classes | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 18 | The Quantum Chromatic Number of the G 19 Join Family | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 25 | Global Identifiability in a Three-Taxon Lateral-Gene-Transfer Model | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 32 | A 14-variable unipotent Keller map and every-order image and vanishing obstructions | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 42 | Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell Inequalities | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 51 | Permutation-blind Bell scores and obstructions to maximal global randomness | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 54 | The Complexity of Stationary Diffusion-Driven Instability: Exact Semialgebraic Characterization, NP-Hardness, and Fixed-Species Algorithms | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 71 | Finite Rational Reductions for the Convex-to-Polytope Conjecture in Neural Codes | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 77 | A 14-variable polynomial map with everywhere unipotent Jacobian and a three-point fiber | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 92 | Low-Schmidt rigidity and tensor-local constraints in the exceptional unitary Hecke Yang–Baxter class | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 93 | Maximal violation without maximal global randomness in a cyclic Bell family | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 102 | Relative Polygonalization with Prescribed Traces for Convex Neural Codes | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 120 | The exact quantum value of a cyclic Bell operator | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 134 | An explicit 44-variable vanishing witness from a 22-variable cubic Keller map | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 142 | A Certified Order-Twelve Extension of the \(\gamma\)–\(\theta\) Frontier in One-Guard Eternal Domination | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 145 | A Cube-Component Exit for Three-Dimensional Keller Maps | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 150 | A Reciprocal-Square Obstruction for Equal-Sum–Product Matrices | No published Zenodo record or archived manuscript match; repository-only work. |
| 156 | Exact repair obstructions around a \(64\)-modular Hadamard matrix of order \(668\) | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 157 | Nonexistence in the N=4, R=2 Knights-and-Rooks Problem | No published Zenodo record or archived manuscript match; repository-only work. |
| 158 | Permutation-Cell Auditing | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 161 | Semiregular \(C_{37}\) conference lifts at order \(334\) | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 165 | Eternal domination and the Lovász theta function: an unbounded separation and a smallest counterexample | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 168 | An explicit counterexample to the Special Image Conjecture in dimension 21 | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 178 | A transversal-capacity obstruction for a regular \(R(5,5)\) endpoint | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 179 | Exact shell descent and finite-field norm gates in a prescribed-compression chart for Legendre pairs of length \(333\) | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 180 | Excluding Parameter Three at Order Thirteen in the \(\gamma\)–\(\theta\) Conjecture for One-Guard Eternal Domination | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 181 | Exclusion of the fixed-linear primitive cubic-pencil quartic row | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 182 | Exclusion of the fixed-quadratic primitive-pencil quartic row | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 199 | Excluding the exact-delta=4 stratum | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 222 | Noncommutative Comparative Statics | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 223 | An explicit Hessian-nilpotent quartic in 54 variables witnessing the failure of Zhao's Vanishing Conjecture | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 226 | Full symmetric monodromy throughout Gallagher’s weighted-lift family: An attributed Brink–Gallagher corollary | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 246 | Archival note: symmetric monodromy in a weighted-lift subfamily | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 249 | The generic-degree spectrum of Keller counterexamples in dimension three: An audited, non-novel record | No paper-specific Zenodo publication: manuscript appears only incidentally in a repository archive for other work. |
| 250 | Strong Tree-Childness Is a Sharp Identifiability Boundary for Level-2 Jukes–Cantor Networks: Convention closure by a canonical cleanup quotient | Rejected attempted extension; no eligible published paper-specific Zenodo manuscript. Preserve earlier defect record; do not treat as the published canonical paper. |

## Files and verification limits

- queue.json: 203 review candidates, exact source locations/hashes, dates/versions, scientific grouping, 244 existing-row dispositions, and 226 published-record dispositions.
- zenodo-current-public.json: fresh public scholarly metadata and public identity-query evidence. Credentials and unpublished draft contents were not saved.
- exclusion-evidence.json: frozen reasons, prior manuscript identity evidence, and archive-release titles for every excluded row.
- spreadsheet-proposals.json: precise range corrections, an unassessed new paper row, and excluded/superseded status suggestions.
- refresh_metadata.py and build_queue.py: read-only refresh and deterministic reconciliation scripts. The refresh uses the existing credential helper only in memory.

Prior inventory impact or journal assessments were not used as proof-validation results. Every passing publication still needs the substantive manuscript review required by the active goal. Dates in queue.json identify the selected published edition; earlier related named releases are retained separately and should not be mistaken for a certified worldwide priority claim.

The public API now caps unauthenticated search pages at25. An initial size100 public search returned HTTP400; the bounded refresh was corrected to25 and completed normally. No records were mutated.
