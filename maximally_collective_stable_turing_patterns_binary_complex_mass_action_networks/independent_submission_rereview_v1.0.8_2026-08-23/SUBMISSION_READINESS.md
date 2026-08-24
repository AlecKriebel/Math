# Submission readiness decision

## Decision

**HOLD the present v1.0.8 upload.** The mathematics is suitable for submission
after minor corrections, but the current release and journal bundle are not
upload-ready.

## Required before submission

1. Publish a new immutable version after fixing the contaminated top-level
   manifest, the two unenforced TeX lock rows, the missing third supplement
   pass, and the cosmetic `Delta_m` subscript.
2. Generate the release manifest from the final tracked/allowlisted tree and
   verify it against a fresh archive before any replay mutates files.
3. Rebuild the supplement until its auxiliary files stabilize; confirm the TOC
   and extracted text, not merely a zero LaTeX exit.
4. Use SIAM's current review format, or otherwise satisfy its alternative
   layout limit. Add continuous line numbering, visible keywords and current
   MSC codes.
5. Add the required Supplementary Materials index with a description and
   justification for every submitted item.
6. Approve and convert the final cover letter to PDF.
7. Obtain the author's final approval of funding, competing-interest,
   authorship, availability, and AI-assistance declarations. Under the current
   SIAM AI policy, use the responsibility sentence “The author assumes
   responsibility for all content.”
8. Cite the exact DOI of the corrected immutable version throughout. The exact
   v1.0.8 DOI is `10.5281/zenodo.22074358`, but a corrected v1.0.9 should use its
   own new version DOI.
9. From a clean archive, rerun the current full portable and minimal replays,
   all 39 entrypoints normally and under optimized Python, all 25 tests, and
   every manuscript/stale/PDF/package audit.
10. Inspect the PDFs produced by the journal portal before final confirmation.

Current official references:

- SIADS author instructions:
  <https://epubs.siam.org/journal/siads/instructions-for-authors>
- SIAM artificial-intelligence policy:
  <https://epubs.siam.org/artificial-intelligence>
- v1.0.8 immutable release:
  <https://github.com/AlecKriebel/Math/releases/tag/maximally-collective-stable-turing-v1.0.8>
- v1.0.8 exact DOI: <https://doi.org/10.5281/zenodo.22074358>

## Acceptance gate after correction

The package is ready for upload only if all of the following are true:

- the fresh top-level and inner manifests pass from the immutable archive;
- both release and portable replay routes reach their advertised completion
  markers, or any unavailable lineage-only stage is explicitly removed from
  the submission claim;
- the submitted PDFs and source ZIP are synchronized after journal formatting;
- the supplement TOC matches the final pagination;
- all required human declarations and portal fields are approved; and
- no pending DOI placeholder remains.
