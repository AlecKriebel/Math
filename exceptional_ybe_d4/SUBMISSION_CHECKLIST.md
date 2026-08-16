# Submission checklist

## Sequence

1. Start the fresh manual Zenodo **New upload** described in
   `ZENODO_DEPOSIT.md`, reserve its new version DOI, and do not publish yet.
2. Insert that reserved DOI in the manuscript and bibliography,
   `CITATION.cff`, project-page metadata and citation, and
   `ARXIV_METADATA.md`; complete the final rebuild, checksum, verifier,
   packaging, and commit/push cycle without a GitHub release.
3. Upload the final DOI-bearing PDF, source ZIP, and checksum file to that
   Zenodo draft; download, verify, preview, and then publish it.
4. Upload the already checked DOI-bearing arXiv source ZIP with `math.QA`
   primary and `math.RT` cross-list; attempt `quant-ph` only if permitted.
5. Submit to **Journal of Algebra** as a regular research article.
6. Submit to the **Journal of Pure and Applied Algebra** only after a rejection
   or completed withdrawal from Journal of Algebra. Never submit concurrently.

## Package-visible gates

- [x] Author, affiliation, corresponding email, and ORCID
- [x] Abstract under 250 words and arXiv's 1,920-character limit
- [x] Five keywords and MSC 2020 classification
- [x] Complete, verified, alphabetized numbered references with DOI links
- [x] Fixed manuscript date
- [x] Funding, CRediT, competing-interest, and AI declarations
- [x] Exact verifier environment, locked dependencies, negative tests, and
      portable checksums
- [x] Separate CC BY 4.0 manuscript and MIT code licenses
- [x] Journal of Algebra highlights (five lines, each at most 85 characters)
- [x] Self-contained Zenodo and arXiv archives
- [ ] Fresh reserved Zenodo version DOI inserted before publication

## Journal of Algebra portal items

- Select a regular research article, not the Computational Algebra section.
- Before journal submission, make a journal-only title-page copy that gives a
  real full postal address for the independent-researcher affiliation,
  including country. A legitimate mailing, post-office-box, or business
  correspondence address may be used if appropriate; do not invent one or
  publish a private home address unintentionally. JPAA uses the same title-page
  convention.
- Upload `main.tex` and the complete editable source; a PDF alone is not an
  acceptable source submission.
- Upload `HIGHLIGHTS.txt` as a separate editable Highlights file.
- Enter the fresh Zenodo DOI in the research-data linking field.
- Complete Elsevier's declarations tool, choose “nothing to declare” if still
  accurate, and upload its generated `.doc` or `.docx` file.
- Enter that same full postal address and the corresponding author's phone in
  the portal. These were intentionally not invented or published here.
- Confirm the work is not under consideration elsewhere and preview every
  generated submission file.

Journal of Algebra applies Elsevier research-data Option C: the verifier/code
record must be deposited, cited, and linked, or unavailability explained.
JPAA currently treats deposit as encouraged, but using the same Zenodo record
is preferable.

No paper, deposit, endorsement request, declaration form, or journal message
was submitted or sent during package preparation.
