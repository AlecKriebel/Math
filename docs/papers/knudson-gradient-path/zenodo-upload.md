# Manual Zenodo upload — version 1.0.0

This kit is ready for a **new preprint record**. It has not been uploaded,
published, or assigned a DOI. The PDF deliberately contains no invented DOI.

1. Extract `zenodo-upload-kit.zip`.
2. Open [Zenodo uploads](https://zenodo.org/uploads/new) and create a new record.
3. Upload the **three files inside `upload/`**: `paper.pdf`,
   `source-and-verification.zip`, and `SHA256SUMS`.
4. Copy the metadata below into the record. Preview the PDF and file list.
5. Use Zenodo's DOI reservation/assignment controls, then publish when ready.
   If you reserve a DOI and want it printed in the manuscript before publishing,
   update the paper, rebuild the PDF and kit, and upload the updated files first.

The outer kit is a convenience container; upload its `upload/` contents so the
paper is visible separately. Metadata JSON is supplied for reuse; manually
uploading a JSON file does not automatically populate the form.
`deposition.json` is the documented REST API wrapper, not an upload script.
No tokens or account credentials are needed to unpack or verify the kit.

## Copy-and-paste fields

**Resource type:** Publication → Preprint

**Title:**

A four-vertex counterexample to Knudson's persistence-gradient conjecture

**Creator:** Kriebel, Alec

**ORCID:** 0009-0001-9320-500X

**Affiliation:** Independent researcher

**Publication date:** 2026-09-23

**Version:** 1.0.0

**Language:** English

**Access:** Open access

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

The code inside the companion archive is separately MIT licensed.

**Description:**

Knudson conjectured that every nonincident persistence pair is joined by
exactly one gradient path in the discrete vector field obtained by retaining
the incident persistence pairs. This note gives a simplex-wise filtration of
a triangulated interval with four vertices and three edges for which one such
pair has no gradient path. It disproves Conjecture 2 in Knudson's contribution
to Oberwolfach Report 29/2008, p. 1629. The proof consists of three boundary
reductions and an inspection of the matching, and the same example works over
any field.

The deposit includes a three-page manuscript, LaTeX source, two exact
standard-library Python verifiers, original inputs, and mathematical and
priority audit notes. A bounded literature search located no earlier explicit
refutation, without guaranteeing historical novelty. This is an unrefereed,
AI-assisted preprint; the audits are not external human peer review. Text is
CC BY 4.0; code is MIT.

**Keywords:**

persistent homology; discrete Morse theory; persistence pairing; gradient
paths; counterexample; Knudson conjecture

**Related identifiers:**

- References (DOI): 10.4171/OWR/2008/29
- Is supplemented by (URL): https://github.com/AlecKriebel/Math/tree/main/knudson_gradient_path_counterexample

**Additional notes:**

Prepared with OpenAI Codex and independent AI audit agents from a candidate
supplied by the author from prior AI-assisted work. Mathematical verification
passes; priority is a bounded search with explicit limitations. No minimality
claim is made.

## Checksums and source

On macOS or Linux, from `upload/`:

```sh
shasum -a 256 -c SHA256SUMS
```

Extract `source-and-verification.zip`, enter its top-level project folder, and
run the two commands in its README. All calculations are exact and offline.

[Zenodo's developer documentation](https://developers.zenodo.org/) was checked
for the supplied metadata fields on 2026-09-23. Set the actual deposit date if
you publish a revised version later. A DOI must come from Zenodo, not this kit.
