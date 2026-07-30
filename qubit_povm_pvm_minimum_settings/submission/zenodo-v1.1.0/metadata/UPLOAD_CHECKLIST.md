# Zenodo draft and upload checklist

## Before uploading

- [ ] Confirm the two draft records are distinct.
- [ ] Confirm both use version `1.1.0` and publication date `2026-07-29`.
- [ ] Add Alec Kriebel's ORCID only if it is available and validated.
- [ ] Answer **No** to the existing-DOI question in both drafts.
- [ ] Reserve one DOI in each draft.
- [ ] Record both reserved DOIs and do not delete either draft.
- [ ] Replace the DOI placeholders in the two Zenodo descriptions.

## Publication draft

- [ ] Upload exactly the four files in `publication/`, separately.
- [ ] Select the ordinary publication PDF as the default preview.
- [ ] Use Resource type **Publication → Preprint**.
- [ ] Use CC BY 4.0.
- [ ] Mark the work unreviewed / not peer-reviewed where applicable.
- [ ] Add the software DOI with relation **Is supplemented by**.
- [ ] Add the immutable tag URL with relation **Is version of**, or retain it
  in the description.
- [ ] Verify all four uploaded file checksums against the local manifests.

## Software draft

- [ ] Upload exactly the single ZIP in `software/`.
- [ ] Do not add separate README, PDF, checksum, or source files.
- [ ] Use Resource type **Software**.
- [ ] Declare CC BY 4.0 and MIT; note the bundled LPPL-licensed
  `paper/lineno.sty`.
- [ ] Add the publication DOI with relation **Is supplement to**.
- [ ] Add the immutable tag URL with relation **Is version of**.
- [ ] Verify the uploaded ZIP checksum against `SHA256SUMS.txt`.

## Preview and publication

- [ ] Inspect title, creator spelling, affiliation, version, date, language,
  licenses, descriptions, keywords, and relation directions.
- [ ] Confirm the normal PDF is the publication record's default preview.
- [ ] Confirm both files panels are public.
- [ ] Publish the software record first.
- [ ] Publish the publication record immediately afterward.
- [ ] Preserve both records and use Zenodo's **New version** feature for later
  substantive corrections.

No Zenodo draft was created, DOI reserved, or record published during local
preparation of this upload set.

