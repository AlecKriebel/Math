# Response to complete-package review 04

The complete frozen-v4 review required one repair: the title must state the nonnegative restriction already present in every mathematical hypothesis. V4's exact files and custody seal remain preserved in `reviews/candidate_v4/` and `reviews/package_review_04/V4_CUSTODY_SEAL.json`.

V5 changes the title to **Nonnegative binary rational hafnians: an exact reduction and approximation and sampling consequences** in the manuscript, PDF title metadata, actual exported PDF, publication README, project heading, builder metadata and Zenodo manifest. The mathematical TeX body, excluding the title and PDF-title lines, is byte-identical to v4. No algorithm, proof, saved mathematical data or theorem scope changed.

The built-in standalone LaTeX compiler returned success (`receipts/native_compile_v5.json`). Tectonic0.16.9 exported the actual six-page PDF, and root rendered and inspected all six pages. The title's changed height alters geometric text extraction around some formulas; direct source comparison and visual inspection confirm the unchanged mathematical body. This distinction is recorded in `receipts/title_scope_v5_text_check.json`. The exact documented main reproduction command passed all28 payload hashes and all three finite checks in a clean v5 extraction, preserving every original extracted byte (`receipts/documented_reproduction_v5.json`).

V5 identities: paper SHA256 `8c93b0f14bc4fd935dbc3a489c5ecca63a8262ba4560a09822b7f65e1036bee7`; ZIP `e79ba53de7b0d937189271d5941ee77eb8e1f10212fef33aa3bb4c4311c666fa`; README `a272e4bc9b525d60a9adfe3ba3a113e8c46c53f246ccd01f16b77eb8958cc1cd`; manifest `2fe834bdf2e5de74a92f7b9463fdc6917717c7e37ccf7ca58c9670065f3efa7d`. Complete identities and exact bytes are preserved in `reviews/candidate_v5/`.

NEW complete reviewer05 has the original request, primary sources and exact v5 package, without inherited favorable review history. V5 remains frozen pending its complete verdict. No Zenodo draft has been created, and no tracker CLI operation has been attempted.
