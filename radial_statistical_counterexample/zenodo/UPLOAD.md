# Zenodo upload kit

Prepared for manual upload. No record has been created and no DOI is assigned. No GitHub release was created; the repository's release-to-Zenodo integration is not used.

## Upload

1. Extract `zenodo-upload-kit.zip` and open [Zenodo's upload page](https://zenodo.org/uploads/new).
2. Upload the three files inside `files/`: `paper.pdf`, `source-and-verification.zip`, and `SHA256SUMS.txt`. The outer kit includes this guide and metadata for convenience; do not upload the kit in place of the readable PDF.
3. Use the fields below. Select a preprint publication, open access, and CC BY 4.0. The code has a separate MIT license in the source archive.
4. Review the file list, author name, ORCID, title, description, date, version, and references, then use Zenodo's publish action when ready. That publication creates the DOI. If reserving a DOI first, it is optional to add it to a later manuscript revision; this kit contains no placeholder or invented DOI.

The JSON file `metadata.json` uses Zenodo's documented legacy deposit-metadata vocabulary; `metadata-for-api.json` wraps it in a `metadata` object. These are prepared metadata, not a submitted or server-validated deposit. The web form need not offer a JSON-import button: the following fields are directly copyable. Schema reference: [Zenodo developer documentation](https://developers.zenodo.org/#deposit-metadata), checked 22 September 2026.

## Copyable fields

**Resource type:** Publication / Preprint

**Title**

Radial orthogonality does not imply dual 1-conformal flatness

**Creator:** Kriebel, Alec

**Affiliation:** Independent researcher

**ORCID:** 0009-0001-9320-500X

**Publication date:** 2026-09-22 (manuscript date)

**Version:** 1.0.0

**Language:** English

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0); source code separately MIT.

**Keywords:** statistical manifolds; radial distributions; 1-conformal flatness; counterexample; affine differential geometry; AMR-059-0011

**Description**

We give an explicit negative answer to Takashi Kurose's Question 3(e) in Furuhata, Matsuzoe and Urakawa, Open Problems in Affine Differential Geometry and Related Topics (1998), p.126, indexed as AMR-059-0011 / 6000011. On the product S²(1) × R with its product metric and Levi–Civita connection, every radial orthogonal distribution in the question is integrable, but the dual statistical structure is nowhere locally 1-conformally flat. The proof combines the first variation of energy with two incompatible curvature evaluations. A conformal metric and projective connection deformation yields a non-self-dual example with nowhere zero cubic tensor; the product obstruction extends to every dimension at least three.

The deposit contains a four-page manuscript, LaTeX source, a standard-library exact rational verifier, an independently implemented SymPy verifier, source and priority audits, and reproducibility instructions. The computations supplement the analytic proof. A focused search found no earlier explicit resolution, but historical priority and current database status are not certified. Classical ingredients and the known divisible-cubic-form construction are credited.

This is an unrefereed, AI-assisted preprint. The candidate was supplied as AI-generated work. The manuscript, verification materials, and separate adversarial AI audits were prepared with OpenAI Codex. AI reviews are not external human peer review or proof-assistant formalization.

**Related works**

- Cites: DOI `10.4036/iis.1998.125` (original question).
- Cites: DOI `10.2748/tmj/1178225722` (definitions and prior criterion).
- Cites: `https://arxiv.org/abs/2503.10024v2` (known deformation mechanism).
- Is documented by: `https://aleckriebel.github.io/Math/papers/radial-statistical-counterexample/`.
- Is supplemented by: `https://github.com/AlecKriebel/Math/tree/main/radial_statistical_counterexample`.

**Funding:** none claimed; leave grant fields empty unless the author has relevant funding to add.

## Verify the upload files

From the extracted `files/` directory:

```sh
shasum -a 256 -c SHA256SUMS.txt
```

The source archive has an internal `SOURCE_SHA256SUMS.txt`; after extracting it, run the same command against that manifest from its top-level folder. Then follow `README.md` to run the verification scripts. Checksums detect changed bytes, not mathematical correctness.
