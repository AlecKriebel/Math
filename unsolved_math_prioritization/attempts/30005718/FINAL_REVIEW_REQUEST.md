# Full five turn independent review request 30005718

Proposed disposition: original unresolved/exhausted 5/5. Please audit every scoped proof, particularly the eventual full-row theorem and the universal meaning of the finite Newton certificates. No sixth author search is permitted. Preserve frozen bytes and use additive corrections if needed.

## Source gate

The exact source is official EMS OWR 58/2023, Problem 6, printed pp.3308–3309, https://ems.press/content/serial-article-files/48169. Use the matrix, starting row and original degree normalization given there. The imported record contains unrelated preceding Pluecker/M-convex background; SOURCE_GATE.md records that mismatch and the harmless index/constant typos. The 2025 Poullot and 2026 Juhnke–Poullot primary papers in the source binding must not be claimed as solved by results about unrelated polytopes. The full original asks all n plus tools for more general recursions.

## Proof audit priorities

- TURN_1: exact three-to-two-state reduction; original degrees and zero conventions; first/last ULC polynomials; unipotent truncation and reversal parity; limits of generic preservation shortcuts
- TURN_2: the exact positive inverse-variance gap, analytic amplitudes, strict weighted row-sum aperiodicity, the relative O(m^(-3/2)) expansion and why adjacent logarithmic differences keep a positive 1/m margin
- TURN_3: noncommutative marking counts; overlap for eventual unimodality; fixed-index polynomial degrees; the maximal J/R words and factorial constants at both upper parities
- TURN_4: uniform small-saddle expansion through two correction orders with analytic coefficient functions at alpha=0; exponential suppression of the lower secondary branch; the original +3 monomial shift and the positive 3/j^2 normalized margin; exact upper coefficient identity (10); step-two curvature, parity and uniform joining to the bulk band. The theorem is existential and supplies no effective N
- TURN_5: exact polynomial degree bounds before interpolation; Newton coefficient positivity certifying all r≥0 in only the stated finite index bands; first-nonzero thresholds for strictness; independent regeneration of the certificate; rational Sturm signs. Do not promote the sampled infinite-family conjecture to a proved all-index result

## Reproducibility

Run `python checks/verify_turn1.py` through `python checks/verify_turn5.py`; each stdout must equal its frozen `turnN_output.json` byte-for-byte. The exact assertion total is 1,508,018. No numerical diagnostic is included in that count. `checks/diagnose_bulk.py` has a separate non-interval receipt.

`python checks/verify_turn5.py --dump certificate.json` produces all 200 exact Newton coefficient vectors. Their compact canonical JSON, excluding the final newline, has SHA-256 `63f530185b41356c61167ba5cd16b5a3d1d70bb837cd4d8b86c9bb4b00e29e2b`. This finite certificate uses known polynomial degree bounds to prove an infinite-r statement; it is not just evaluation of a polynomial at finitely many sample points. The full optional file is regenerable and need not be published as a large duplicate.

Source PDFs, extracted text and rendered primary pages are available in the sibling local source directory, with hashes in SOURCE_BINDING.json and SOURCE_ADDITION_2.json. They are not part of the public packet. The complete five-turn remote backup and final author manifest bind the proof version. Please provide a portable independent report, exact binding hashes and separate controls; report any defect promptly. A scoped PASS cannot change the original disposition without a proof of the missing all-size part.
