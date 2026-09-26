# Final validation of the submission revision

Final manuscript source SHA-256: `ff1f4c7e3a696a2f0c899db6827625f81d386601f22dbd9e065a2de2a5846e05`.

Final manuscript PDF SHA-256: `93618f7cf9de096e6fdaf50c30c3d158a226018a9f472b2748d32844edc056ad`.

Final supplementary manifest SHA-256: `1e92f0f734669a0c233f89a7cd32742e4358133dca0e63a7b884a3bccd246b2c`.

## Proof and source review

Five first-round specialist assignments and independent second-round/final-referee passes covered the local construction and complete circle certificate, universal localization and minimum dimension, braid/link consequences, reproducibility, and novelty. The final referee first derived objections from the revised manuscript before reading earlier reports. Separate primary-source and algebraic approaches are documented in the reports. These are AI-assisted audits, not independent human peer review or whole-paper formal verification.

One material source-fidelity defect was found and repaired: the archived older-GHR comparison changed a prefactor relative to the accessible primary preprint. The revised manuscript removes that comparison; the supplement independently defines and distinguishes the two matrices. No main theorem depends on the removed claim. All other findings have a repair or justified scope disposition in `REVIEW_RESOLUTION.md`. No unresolved substantive defect remained in the reviewed final source.

## Exact computation

| Check | Result |
|---|---|
| Original release | Five routes, 32 negative tests, and 43 package checksums pass; 49 bound original source/manifest/upload files remain byte-identical. |
| Revised supplement | Five routes and 26 stronger scientific negative tests pass in fresh CPython 3.14.6, SymPy 1.14.0, mpmath 1.3.0 with hash-locked dependencies. |
| Independent local algebra | Full symbolic 18-word certificate and exact converse; dense quaternionic/local-unitary and partial-trace checks pass. |
| Independent global checks | 511 exact Pauli-trace/F4 comparisons, 21 finite Garside-generator checks, and Pauli-label independence through n=100 pass. These are finite checks, not universal proof substitutes. |
| Source-mismatch safeguards | Distinct literal-preprint and common-prefactor residuals verified; two additional deliberate safeguard mutations rejected for the intended reason. |

All-n faithfulness, minimality, same-word conjugacy and actual finiteness have written arguments. The new finite-image proof explicitly bounds the scalar kernel. Its cited external representation-theoretic/classification and topology/algorithm inputs are identified in the manuscript and reviews; their entire underlying theories were not re-proved.

## Document and package checks

The saved standalone source passes the built-in LaTeX compiler. Tectonic 0.16.9 with bundle v33 and fixed epoch 1790398800 generates the final 21-page PDF with no compilation warnings, overfull boxes, or undefined references. Extracting the two-member editable source ZIP into a clean directory and recompiling produces a byte-identical PDF. All final manuscript pages and the one-page cover letter were rendered and inspected for legibility, clipping, missing glyphs, table layout, references, headers and page numbering.

The portal abstract matches the source after explicit notation conversion, with 206 whitespace-delimited tokens; all six keywords and author details agree. The separate package audit checks 233 archive, hash, file and metadata conditions. The scientific supplement contains exactly its 15 allowed members, including a manifest for the other 14. The editable source contains only `main.tex` and its README. Private correspondence drafts, editorial strategy and handoff instructions are absent from both journal archives. The full local handoff clearly identifies which files to upload.

The manuscript and package are prepared for the human author's final review and submission. Personal declarations, present submission status, and author accountability remain the author's confirmations. No person was contacted, no journal submission was made, and no new DOI release was created.
