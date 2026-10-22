# Source ledger for affine incidence matching

Problem 30000391, priority rank 1223. Audit performed 2026-10-10 UTC.

## Original problem

- Author and contribution: Anders Björner, *Matching points to hyperplanes*.
- Venue: *Combinatorics*, Oberwolfach Report 1/2006, DOI 10.4171/owr/2006/01, report pages 5-72.
- Relevant location: printed pages 51-52; one-based PDF pages 47-48.
- Publisher record: https://ems.press/journals/owr/articles/1183
- DOI: https://doi.org/10.4171/owr/2006/01
- Retrieved PDF: https://ems.press/content/serial-article-files/46029?nt=1
- Retrieval: 2026-10-10T00:45:45.460856+00:00, HTTP 200.
- Size: 616085 bytes.
- SHA256: 3f3b74e79efb6ec1b79269483d7c8f8d4698f3859947fd57c43de5f0dcaa90f5.
- Inspection: the full relevant contribution, including inherited full-span assumption, conjecture, known cases, CH observation and bibliography, was read in extracted text; both relevant pages were visually inspected against the PDF.
- Scope finding: affine spanning is explicit; the injection preserves incidence. The source does not explicitly state d>=1. The zero-dimensional exception is therefore disclosed in the acceptance report.

## Published closing theorem

- Author: Jonathan David Farley.
- Title: *A question of Björner from 1981: Infinite geometric lattices of finite rank have matchings*.
- Venue: Australasian Journal of Combinatorics 82(3) (2022), 228-236.
- Publisher issue record: https://ajc.maths.uq.edu.au/?page=get_volumes&volume=82
- Official PDF: https://ajc.maths.uq.edu.au/pdf/82/ajc_v82_p228.pdf
- Retrieval: 2026-10-10T00:47:17.166222+00:00, HTTP 200.
- Size: 129860 bytes.
- SHA256: f896a28f690f4875bdefadf1b68ef695ee2c43575887111d78a9a7b26ba7bae4.
- Inspection: all nine pages read in extracted text. Printed pages 229-235, including the definitions, imported hypotheses, restriction lemma, singular-cardinal proposition and full final proof, were visually inspected. The journal issue record was checked on 2026-10-10.
- Locators: geometric-lattice definition on 229; incidence matching definition and rank-two convention on 230; restriction Lemma 9 on 231-232; singular-cardinality Proposition 10 on 232; final Theorem 11 on 233, proof continuing through 235.
- Status: published journal article. A focused title/author search for corrections or gaps on 2026-10-10 did not locate an applicable correction or retraction. This is bounded negative search evidence, not a guarantee that none exists. One search response reported a robots restriction for the journal domain; the audit did not retry that blocked resource. The official PDF and issue content had already been successfully retrieved.

## Directly checked dependency statements

- Authors: R. Aharoni, C. St J. A. Nash-Williams and S. Shelah.
- Title: *A General Criterion for the Existence of Transversals*.
- Venue: Proceedings of the London Mathematical Society (3) 47 (1983), 43-68.
- DOI: https://doi.org/10.1112/plms/s3-47.1.43
- Author archive PDF: https://shelah.logic.at/files/95295/194.pdf
- Retrieval: 2026-10-10T00:54:15.046572+00:00, HTTP 200.
- Size: 656520 bytes.
- SHA256: e9f5f5c0dbfcf765aebd5d60772ad6d3f0d33a5204dff24177124629f6926055.
- Relevant locations: definitions on printed pages 44-45 and 48; Lemma 4.2 on 49; Lemma 4.3 on 50; Corollary 4.9a and Theorem 5.1 on 54.
- Inspection: relevant definitions and statements checked in extracted text; printed pages 48, 49 and 54 visually inspected. The full original proof of the transversal criterion was not independently audited.
- Use: verifies that Farley's obstruction parameters, saturation, deletion deficiency, and no-obstruction criterion are compatible with the original theorem.

## Dependencies not independently re-proved

The audit reads Greene's finite matching theorem, Björner's rank-three and regular-cardinality results and cardinal-counting lemma, and the Milner-Shelah/Tverberg criterion in their cited formulations in Farley. The original proofs of all of these were not retrieved and re-proved. Standard finite-rank geometric-lattice facts are also accepted inputs for the internal proof audit. The affine application itself is checked directly using homogenized vectors and does not require an uninspected representation theorem.

## Provenance of this edition

The companion JSON ledger records the same public scholarly-source URLs, PDF identities, retrieval dates and inspection scope. The retrieval and reading statements describe the originating audit of 2026-10-10. Preparing this edition did not add a fresh source reading or extend the recursive-dependency audit.
