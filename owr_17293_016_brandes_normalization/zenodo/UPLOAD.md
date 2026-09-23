# Zenodo upload: ready-to-copy fields

No deposit or DOI has been created. Extract `zenodo-upload-kit.zip`, then create a [new Zenodo upload](https://zenodo.org/uploads/new).

## Upload these two files

1. `paper.pdf` — the three-page preprint.
2. `source-and-verification.zip` — editable source, exact verifier and certificates, independent proof, audits, and licenses.

`SHA256SUMS.txt` lets you check these files. The outer kit is a convenience download; upload the two files above rather than the outer kit. The JSON files contain metadata, not executable upload commands. Zenodo's web form is filled using the fields below; uploading JSON as an ordinary file does not populate the form.

## Basic information

- Resource type: Publication / Preprint (or Preprint in the current selector).
- Title: **A coefficient normalization for positive definite forms**
- Publication date: **2026-09-23** (the public preprint date, in UTC).
- Version: **1.0**
- Language: **English**
- Creator: family name **Kriebel**, given name **Alec**.
- Affiliation: **Independent researcher**.
- ORCID: **0009-0001-9320-500X**.
- Access: **Open**.
- License: **Creative Commons Attribution 4.0 International (CC BY 4.0)**. The included code is additionally available under MIT, as stated in LICENSES.md.
- DOI: leave any existing-DOI field blank; let Zenodo assign a new DOI. If a DOI is reserved in the draft, that reservation is not publication.

## Description — copy the following three paragraphs

Every positive definite real homogeneous form of positive degree admits an invertible real linear change of variables in which the symmetric ordered coefficients have diagonal entries equal to one and every mixed entry strictly between zero and one. This gives an affirmative answer to Brandes's Problem 11 in the 2019 Oberwolfach report on Analytic Number Theory, including the printed absolute-value inequality.

The three-page proof clusters a basis near a direction minimizing the form on a Euclidean sphere. A polynomial gap has a strictly positive quadratic term for every mixed tuple. The accompanying source package includes an independent proof via positive definite bilinear slices and Cauchy–Schwarz, internal adversarial audits including three fresh preprint-readiness rounds and independently rechecked supplementary controls, a dated priority search, and a standard-library Python verifier with exact rational certificates. The finite checks supplement the analytic proof and are not a formal verification of the universal theorem.

Brandes's 2015 discussion of pseudo-diagonal forms is credited as a direct precursor. A bounded literature audit found no earlier full resolution; first priority is not established. This is an unrefereed preprint developed and checked with generative-AI assistance. Paper and prose: CC BY 4.0. Code: MIT.

## Keywords

positive definite forms; homogeneous polynomials; symmetric polarization; coefficient normalization; pseudo-diagonal forms; Brandes problem; OWR-17293-016

## Related works

| Identifier | Relation from this deposit |
| --- | --- |
| `10.4171/OWR/2019/50` | References |
| `10.1112/jlms/jdv028` | References |
| `https://github.com/AlecKriebel/Math/tree/main/owr_17293_016_brandes_normalization` | Is supplemented by |
| `https://aleckriebel.github.io/Math/papers/brandes-coefficient-normalization/` | Is documented by |

No funding, community, journal acceptance, or external reviewer should be inferred. The internal reviews are AI-assisted checks, not peer review. Preview the record and publish it when ready; after publication, copy the assigned DOI into your citation. A GitHub release is unnecessary for this manual deposit.

## Machine-readable metadata

`metadata.json` and `.zenodo.json` contain the same metadata object in the documented Zenodo deposition/GitHub metadata format. `deposition-payload.json` wraps it in the API's `metadata` key. They include no token, deposit ID, DOI, or publication action. The format was checked against [Zenodo's developer documentation](https://developers.zenodo.org/) on 2026-09-23.
