# Zenodo upload fields — version 1.0.1

This is a prepared upload kit, not an existing Zenodo record. No DOI is reserved or published.

## Files to upload

Unzip `zenodo-upload-kit.zip`. Upload `files/paper.pdf`, `files/source-and-verification.zip`, and optionally `files/SHA256SUMS.txt`. Uploading the ZIP itself as the only file would hide the paper from direct preview, so prefer the separate files.

## Copy these fields

**Resource type:** Publication / Preprint

**Title:** Nonattainment in the Harrell–Stubbe Dirichlet gap inequality

**Author:** Alec Kriebel (family name: Kriebel; given name: Alec)

**ORCID:** 0009-0001-9320-500X

**Affiliation:** Independent researcher

**Version:** 1.0.1

**Publication date:** 2026-09-23 (UTC; adjust if the first public deposit date differs)

**Language:** English

**Access:** Open

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0). The included code additionally carries the MIT license; see LICENSES.md.

**Keywords:** Dirichlet Laplacian, Yang inequality, Harrell–Stubbe inequality, spectral gap, equality cases, OWR-3389-016

### Description

We prove that the universal Harrell–Stubbe gap bound for Dirichlet eigenvalues is never attained on a nonempty bounded open subset of Euclidean space at any finite index. More strongly, Yang’s first inequality is strict at every real threshold above the lowest eigenvalue. The proof uses the classical spectral remainder and a self-adjointness obstruction to finite spectral support of a coordinate times an eigenfunction. No boundary regularity or connectedness is required.

This answers the corrected saturation question recorded in the 2009 Oberwolfach report and listed as OWR-3389-016; the original report’s missing square is explicitly documented. The package includes the paper, LaTeX source, independent AI-assisted proof audits, a scoped priority audit, and a dependency-free verifier with 7,016 exact checks. The computation checks algebra and box spectra, not the general analytic theorem. No earlier explicit nonattainment proof was located in the literature checked; this is not an exhaustive priority certification. Research and writing were AI-assisted.

### Additional notes

Original manuscript and documentation: CC BY 4.0. Verification and build code: MIT (see LICENSES.md). No external peer-review or proof-assistant certification is claimed.

### Related identifiers

- References: DOI 10.4171/OWR/2009/06 (original question).
- References: DOI 10.1090/S0002-9947-97-01846-1 (classical bound).
- References: DOI 10.1007/BF02829638 (earlier strictness discussion).
- Is supplemented by: https://github.com/AlecKriebel/Math/tree/main/owr_3389_016_strict_gap
- Is supplemented by: https://aleckriebel.github.io/Math/papers/strict-dirichlet-gap/

## DOI and final review

Create a new upload in Zenodo and use its DOI reservation option if desired. Do not enter an invented DOI. Review the preview and publish when ready; record the assigned DOI in CITATION.cff and the paper/site metadata afterward. There is no need to create a GitHub release for this manual deposit.

`metadata.json` contains the metadata object; `metadata-for-api.json` wraps it under `metadata` for the documented deposition API. These were checked locally against the documented field structure, not submitted for server validation. The UI is a straightforward way to use the copyable fields above.

Official instructions checked 2026-09-23: [Describe records](https://help.zenodo.org/docs/deposit/describe-records/) and [Zenodo deposition API](https://developers.zenodo.org/).
