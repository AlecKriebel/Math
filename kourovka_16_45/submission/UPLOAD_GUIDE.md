# Zenodo upload guide — version 1.0.0

Prepared for Alec Kriebel to upload manually. No Zenodo record, reserved DOI,
or GitHub release has been created. The archive name is a local delivery name,
not evidence of deposit. This guide follows Zenodo's official
[upload instructions](https://help.zenodo.org/docs/deposit/create-new-upload/).

## Files to upload

Extract the outer kit. Upload the **two files inside `upload/`** to one record:

1. `Kourovka_16_45_Counterexample_v1.0.0.pdf` — the nine-page revised preprint.
2. `Kourovka_16_45_Source_and_Verification_v1.0.0.zip` — LaTeX source, identical
   manuscript PDF, exact group specification, certificates, all verification
   software, independent audit reports, and provenance.

The outer kit itself need not be uploaded. Its remaining files help fill the
deposit form. `SHA256SUMS` covers both upload files and the helper documents;
check it before editing or uploading. On macOS, run `shasum -a 256 -c
SHA256SUMS` from the extracted kit. On Linux use `sha256sum -c SHA256SUMS`.

## Deposit fields

- **Resource type:** Publication / Preprint.
- **Title:** A counterexample to Kourovka Notebook Problem 16.45.
- **Creator:** Alec Kriebel; family name Kriebel, given name Alec.
- **ORCID:** 0009-0001-9320-500X.
- **Affiliation:** leave blank unless the author wants to supply one.
- **Version:** 1.0.0.
- **Publication date:** 2026-09-21 (first website/repository edition; use the
  deposit date instead if preferred by the author).
- **Language:** English.
- **Description:** paste `description.html` using HTML/source mode where
  offered, or `description.txt` as plain text. The same text is in metadata.json.
- **Keywords:** finite groups; permutation bases; independent sets; Kourovka
  Notebook; Problem 16.45; semidirect products; subgroup lattices; exact verification.
- **Access:** public/open.
- **License:** consult `LICENSES.md`. If no license has yet been selected,
  choose it in the form before publishing; the metadata intentionally does
  not grant reuse rights on the author's behalf. A useful option is CC BY 4.0
  for manuscript/data and MIT for source code, with those file-specific terms
  recorded in the package before deposit.

`metadata.json` is a human-readable field map, **not** an API request body or
a promise that Zenodo can import it automatically. AI assistance belongs in
the description, not in the list of human creators. No funding or institutional
affiliation is asserted. No journal or peer-review status should be entered.

## Related works and references

Add the website as **Is documented by**:
https://aleckriebel.github.io/Math/papers/kourovka-16-45/

Add the source repository as **Is supplemented by**:
https://github.com/AlecKriebel/Math/tree/main/kourovka_16_45

The source archive uploaded with this record is the frozen version; the main
branch link may subsequently change. Add Cameron's 2024 article as **References**,
using DOI `10.2140/mt.2024.3.417`. Full bibliography entries are supplied in
metadata.json and the manuscript.

## DOI and final action

Use Zenodo's option to obtain a new DOI for this record. No DOI currently
appears in the manuscript or citation file, so there is no placeholder to
remove. Reserving a DOI in a draft does not itself publish the record.
Review the file preview, author name/ORCID, license, description, and version,
then publish when ready. The PDF and source ZIP should remain paired.

After publication, retain the assigned record URL and version DOI and add
them to the website and citation metadata in a follow-up repository update.
Avoid creating a GitHub release for this task: this repository's integration
can create a separate Zenodo record, which would duplicate the manual upload.

## Verification scope

The structural proof and independently reconstructed finite calculations
support b_f(G)=b(G)=3<4=mu′(G) for the displayed group of order 100920. The
review corrected one product order without changing the theorem. The paper
has not undergone external human peer review or complete formal verification;
the priority search was bounded. Those qualifications are already included
in the copy-ready description.
