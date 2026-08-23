# Journal of Mathematical Biology submission checklist

> **DRAFT — NOT SUBMITTED.** The official instructions were checked on
> 2026-08-20. Recheck the live page immediately before submission:
> <https://link.springer.com/journal/285/submission-guidelines>.

## Manuscript identity and format

- [ ] Select the journal's original-research article type.
- [ ] Confirm the title is concise enough for the portal and identical in the
      PDF, editable source, cover letter, and metadata.
- [ ] Confirm the abstract is 150--250 words and contains no undefined
      abbreviation or unspecified reference.
- [ ] Supply the manuscript's six final keywords consistently in the portal.
- [ ] Retain the MSC codes 92D15, 60J10, and 05C81.
- [ ] Upload the compiled PDF and every editable LaTeX source, included file,
      and figure source needed to build it.
- [ ] Check whether the journal asks for the exact-verifier archive as
      Supplementary Information or prefers its persistent repository link.
- [ ] If submitted as Supplementary Information, give the archive a journal-
      compliant caption and reference it in the manuscript.

## Journal style checks

- [x] Use author--year citations in the manuscript.
- [x] Alphabetize the reference list by first-author surname and include DOI
      links where available.
- [ ] Check heading levels, abbreviations at first use, table captions, and
      figure accessibility against the live instructions.
- [ ] Decide whether to migrate to the current Springer Nature LaTeX template;
      the journal recommends it but the mathematical source must remain
      semantically unchanged.
- [ ] Verify the title page includes name, affiliation/location, active
      corresponding email, and ORCID.

## Declarations and author approval

- [ ] Confirm `me@aleckriebel.com` and replace `[[POSTAL_ADDRESS]]`.
- [ ] Insert or portal-enter the unified statements in `DECLARATIONS.md`.
- [ ] Confirm no external funding and no financial or non-financial competing
      interests.
- [ ] Confirm the ethics, consent, and data statements are not applicable for
      this proof-and-software study.
- [ ] Confirm the substantive AI disclosure is placed in the manuscript's
      appropriate methods or declarations section, as required by the live
      Springer policy.
- [ ] Confirm the sole-author contribution and accountability statement.
- [ ] Read and accept the live publication, copyright, and open-access terms.

## Originality and public-version disclosure

- [ ] Confirm the manuscript is not under simultaneous journal consideration.
- [ ] Disclose the superseded software archive DOI
      `10.5281/zenodo.21753405` and explain neutrally which earlier results
      are incorporated and which fitness-two results are added here.
- [ ] Disclose the companion-workstream software archives
      `10.5281/zenodo.21850042` and `10.5281/zenodo.21852072` if the portal asks
      for related manuscripts or public records.
- [ ] Add the assigned bioRxiv DOI if the preprint is posted before journal
      submission.
- [ ] Confirm no text, figure, or table permission is required.

## Reproducibility and final gate

- [ ] Generate the deterministic archive with `../release_bundle.sh`.
- [ ] Build the enclosing reproducibility package and run its sole certified
      `run_all_referee_checks.sh`; plain manifest checking or a direct internal
      bootstrap is not equivalent.
- [ ] Rebuild and visually audit the final PDF after all style changes.
- [ ] Compare every theorem and scope statement across abstract, cover letter,
      manuscript, certificate notes, and portal fields.
- [ ] Human author approves all files and performs the portal submission.
