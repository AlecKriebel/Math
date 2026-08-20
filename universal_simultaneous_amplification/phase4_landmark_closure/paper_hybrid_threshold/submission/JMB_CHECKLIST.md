# Journal of Mathematical Biology submission checklist

> **DRAFT — NOT SUBMITTED.** The official instructions were checked on
> 2026-08-20.  Recheck the live page immediately before submission:
> <https://link.springer.com/journal/285/submission-guidelines>.

## Manuscript identity and files

- [ ] Select the journal's original-research article type.
- [ ] Confirm the title is identical in the PDF, editable source, cover
      letter, and portal metadata.
- [ ] Confirm the abstract is 150--250 words, self-contained, and free of
      undefined abbreviations or unspecified references.
- [ ] Supply the manuscript's six final keywords consistently.
- [ ] Retain MSC codes 92D15, 60J10, and 05C81.
- [ ] Upload the compiled PDF and every editable LaTeX or figure source needed
      to build it.
- [ ] Check whether the exact source-and-certificate archive should be
      Supplementary Information or linked through its new persistent record.
- [ ] If uploaded as Supplementary Information, give it a compliant caption
      and cite it in the manuscript.

## Journal style

- [x] Use author--year citations.
- [x] Alphabetize references by first-author surname and include DOI links.
- [ ] Recheck heading levels, abbreviations, equation numbering, diagram
      accessibility, and title-page requirements against the live guide.
- [ ] Decide whether to migrate to the current Springer Nature LaTeX template
      without changing the mathematical content.
- [ ] Confirm the title page includes author name, affiliation/location,
      active corresponding email, and ORCID.

## Declarations and approval

- [ ] Confirm `me@aleckriebel.com` and replace `[[POSTAL_ADDRESS]]` in the
      private cover-letter copy.
- [ ] Insert or portal-enter the unified statements in `DECLARATIONS.md`.
- [ ] Confirm no external funding and no financial or non-financial competing
      interests.
- [ ] Confirm ethics, consent, and empirical-data statements are not
      applicable for this mathematical study.
- [ ] Approve the substantive AI disclosure and its placement against the
      current Springer Nature policy.
- [ ] Confirm sole-author contribution and accountability.
- [ ] Read and accept live publication, copyright, and open-access terms.

## Prior public versions and related work

- [ ] Disclose `10.5281/zenodo.21852072` as the v1 **source/software archive**
      containing an earlier manuscript version and explain the superseding
      revision.
- [ ] Disclose `10.5281/zenodo.21850042` as the superseded
      **source/software archive** for the earlier `R_sim>=3/2` construction.
- [ ] Disclose companion Paper I wherever the portal requests closely related
      manuscripts.
- [ ] Add the assigned bioRxiv DOI if the preprint is posted before journal
      submission.
- [ ] Confirm no text, figure, or table permission is required.
- [ ] Confirm the manuscript is not under simultaneous journal consideration.

## Reproducibility and final gate

- [ ] Generate the deterministic archive with `../release_bundle.sh`.
- [ ] Verify its internal SHA-256 manifest and complete a fresh-extraction
      pinned replay.
- [ ] Rebuild and visually audit the final PDF after all style changes.
- [ ] Compare every theorem and scope statement across abstract, cover letter,
      manuscript, certificate notes, and portal fields.
- [ ] Human author approves all files and performs the portal submission.
