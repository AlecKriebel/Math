# Non-destructive Zenodo new-version instructions

Perform these steps only after final author approval.

1. Open the standard-PDF concept `10.5281/zenodo.21699160` and choose **New
   version**. Do not edit or replace record `10.5281/zenodo.21699161` in place.
2. Repeat **New version** for the line-PDF concept `21699068`, source concept
   `21699180`, integrity-manifest concept `21699204`, and software concept
   `21699223`. Keep all five records as unpublished drafts. Do not delete a
   draft after reserving its DOI.
3. In each draft, use **Get a DOI now** (or the equivalent DOI-reservation
   control) and record all five version-specific DOI values. Do not publish
   any record yet.
4. Complete every post-reservation item in `POST_UPLOAD_REPLACEMENTS.md`, including the
   canonical manuscript/bibliography, root citation metadata, the
   software-archive citation template, PRA files, website draft, email draft,
   and all five Zenodo metadata sheets.
5. Rebuild the canonical and line-numbered PDFs, PRA auxiliary PDFs, source
   archives, software/verifier archives, website copies, and every SHA-256
   manifest. Rerun `./run_all.sh`. The files currently in this directory are
   safe draft-seeding payloads, but they are not the final publishable bytes
   until this DOI-insertion rebuild has occurred.
6. Remove inherited old files from the five Zenodo drafts and upload the
   corresponding final rebuilt version 1.2.0 file to each draft.
7. Apply the matching metadata sheet. Keep each existing resource type:
   Preprint, Preprint, Preprint, Other, and Software respectively.
8. Confirm creator `Kriebel, Alec`, Independent Researcher, ORCID
   `0009-0001-9320-500X`, actual publication date, version `1.2.0`, English,
   and public visibility.
9. Use CC BY 4.0 for the publication/source/manifest records. The software ZIP
   contains MIT-licensed code and CC BY 4.0 paper/data/report material; declare
   both licenses if the interface permits and explain the mixed licensing.
10. Cross-link the new standard PDF and software versions as supplemented-by /
    supplement-to. Add the public ZCW arXiv identifier as a cited related work
    if the interface supports it.
11. Check all manifests against the exact uploaded bytes, then preview every
    record, title, filename, license, version, ORCID, description, DOI, and
    related identifier. Search the publishable source tree once more for every
    replacement token.
12. Publish the software new version first, then the four publication/support
    records in quick succession. Only after all five resolve should the author
    submit to a journal, deploy the website, or send correspondence.

Treat every published file as immutable. Substantive later changes require
another linked new version.
