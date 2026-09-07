# Rendered document review of v1.0.10

Target: `953c836a12b9d9d474521feb4a96e218c1155203`. The parent reviewer inspected every page of all seven supplied PDFs on 2026-09-06, using 26 newly rendered contact sheets at 100 dpi and the corresponding source/extracted text for precise mathematics.

| Document | Pages inspected |
|---|---|
| Canonical manuscript | 1–19 |
| Canonical supplement | 1–19 |
| Theorem summary | 1–3 |
| Proof skeleton | 1–6 |
| SIADS manuscript | 1–24 |
| SIADS supplement | 1–24 |
| SIADS cover letter | 1 |

Total: 96 pages. Every contact sheet named in `PDF_INVENTORY.json` was viewed. The rendering script recreates the ignored images.

No new physical overlap, clipping, illegible coefficient, misplaced line number, unresolved reference, or broken equation was found in the initial contact-sheet inspection. This did not establish conformity to the journal's narrower text area: subsequent fresh TeX logs and independent PDF-coordinate measurements identify five overfull boxes, detailed below. The exact-fraction rows remain separated. Canonical supplement pages 14–15 and SIADS supplement pages 17–19 now put the parameter in the numerator, as in `8281A/8100`, removing the prior ambiguity. The certificate referee separately checks the semantic value of all 218 printed table rows and the 50 rational-parameter rewrites.

The missing hypotheses are restored in the rendered generic theorem statements: theorem summary page 1 and proof skeleton page 2. Both explicitly require positive diagonal diffusion, and the skeleton now assumes det J=0 before discarding the constant term. The main theorem remains unchanged and correctly stated.

Title, abstract, figures, exact formulas, data-availability links, bibliography and AI responsibility sentence are legible in the canonical and SIADS formats. However, legibility is not the same as fitting the declared six-inch text width. Journal manuscript pages 17 and 19 have overlong command/table boxes; journal supplement pages 14, 20 and 23 have overlong command, rational-identity and display boxes. Their exact TeX excesses are 33.31522, 22.83739, 59.06581, 48.9858 and 1.66727 points respectively. The last is small; the other four materially exceed the intended text area. `check_journal_margins.py` independently measures those four against the configured right edge at 522 PDF points, excluding line numbers and tiny punctuation protrusions. These are journal-layout issues, not clipped scientific content or defects in the canonical preprint layouts.

The cover letter is dated September 6, 2026, and includes the declarations already confirmed by the user. No renewed declaration request is needed.

The exact predecessor DOI is correctly described as v1.0.9. Independent DataCite registry checks confirm that record, its relationship to the concept DOI, and the newly registered exact v1.0.10 DOI 10.5281/zenodo.22559244. Current manuscript links to the immutable v1.0.10 tag and concept DOI are accurate. The new exact DOI is optional metadata for a later upload, not a reason to revise the frozen release again.

This is a read-only inspection of the supplied documents. Build and adversarial mutation results are reported separately; the newly found conflicting-coefficient-field attack concerns a disposable regenerated table, not these correct released PDFs.
