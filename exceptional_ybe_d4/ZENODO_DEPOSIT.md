# Manual Zenodo deposit record

This package is ready to start a **new manual upload**. Do not create a GitHub
release and do not select **New version** on any existing record. Reserve the
new record's version DOI and complete the gate below before publishing it.

## Mandatory repository safeguard

Before any future GitHub release, the human owner should disable the Zenodo
GitHub integration toggle for `AlecKriebel/Math`. That integration has placed
seven unrelated releases under concept DOI `10.5281/zenodo.21753404` and
archives the whole monorepo. This paper must not use or cite that DOI family.

Create a fresh record with Zenodo **New upload**. No draft, DOI reservation,
deposit, or integration change was made while preparing this package.

## Exact metadata for the new record

- Resource type: Publication / Preprint
- Title: *An exceptional four-dimensional unitary Hecke Yang–Baxter operator*
- Creator: Kriebel, Alec
- ORCID: `0009-0001-9320-500X`
- Affiliation: Independent researcher
- Version: `1.1.3`
- Publication date: `2026-08-16`
- Publisher: Zenodo
- Access: Open
- Languages: English
- Licenses: Creative Commons Attribution 4.0 International for the paper and
  documentation; MIT for the verifier and runner code
- Related identifier: the GitHub package URL, relation **Is supplemented by**
- Keywords: Yang–Baxter operator; Hecke algebra; braid group representation;
  unitary localization; fusion category

Description:

> We construct an explicit 16 by 16 unitary Yang–Baxter operator in the
> exceptional Hecke class [exp(i pi/3), 1/2, 4]. Its spectral projection has
> both unnormalized partial traces equal to twice the identity, so the
> tensor-space representation induces the Markov trace and faithfully
> localizes the C(sl_3,6) Jones–Wenzl sequence. The paper proves that four is
> the minimum local dimension. This record includes the manuscript,
> compilable TeX source, three exact verification routes, negative tests,
> frozen output, checksums, provenance, and submission metadata.

## Reserved-DOI completion gate

In the fresh **New upload** draft, use Zenodo's **Reserve DOI** control before
uploading or publishing. Record the newly reserved **version DOI** (not a
concept DOI), but do not publish the record yet.

Insert that DOI in all of the following places:

- the manuscript's data/code/source availability statement and formal
  bibliography;
- `README.md` and the current package-status language in `MANIFEST.md`;
- `CITATION.cff`;
- the project page's structured metadata and suggested citation; and
- the bracketed template in `ARXIV_METADATA.md`.

Run a package-wide DOI/status sweep before rebuilding. Historical logs and
prior-version release notes may retain clearly dated pre-reservation facts,
but no file describing version 1.1.3 as current may say that its archive is
still only planned.

Then run the complete final rebuild and checksum workflow: rebuild both PDF
mirrors, refresh and verify the package-local `SHA256SUMS`, rerun all supported
verifiers and negative tests, run `package_submission.py`, verify both outer
checksum files, and compile the regenerated arXiv ZIP. Commit and push that
DOI-bearing source, page, and PDF without creating a GitHub release. Wait for
GitHub Pages to deploy, then confirm that the live project page and live PDF
show the same DOI-bearing edition before publishing the Zenodo draft.

This reserve-before-publication sequence gives the Zenodo, repository, arXiv,
and journal copies the same DOI-bearing manuscript content and provenance. If
the reserved DOI is not yet available, stop; do not publish first and retrofit
a self-citation afterward.

Official DOI-reservation instructions:

- <https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/>

## Upload exactly these files after the gate

From `submission/`:

- `exceptional-ybe-d4-v1.1.3.pdf`;
- `exceptional-ybe-d4-v1.1.3-source.zip`;
- `SHA256SUMS`.

Set the PDF as the default preview. Upload the final DOI-bearing versions of
exactly those three files to the same draft. Before publishing, download all
three, check their names and sizes, and verify the downloaded `SHA256SUMS` in a
directory containing the downloaded PDF and source ZIP. Preview the record,
confirm that the reserved DOI is the one printed in the files and metadata,
and only then publish. The arXiv archive and its separate
`ARXIV_SHA256SUMS` are not part of the Zenodo record.

After Zenodo publication, submit the already checked DOI-bearing arXiv ZIP.
Put the supporting-record DOI in arXiv's Comments field, not its DOI field.
Use the same DOI-bearing manuscript for the journal, adding only the separate
journal title-page address described in `SUBMISSION_CHECKLIST.md`.

Official instructions:

- <https://help.zenodo.org/docs/deposit/create-new-upload/>
- <https://help.zenodo.org/docs/github/enable-repository/>
