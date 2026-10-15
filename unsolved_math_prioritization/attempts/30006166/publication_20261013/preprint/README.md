# Generic Cantor actions of Z wr Z are hyperfinite

Alec Kriebel, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Version 1.0.0, October 13, 2026. AI-assisted, unrefereed preprint.

The note gives an affirmative answer to Question 3 in Iyer's contribution, joint with Shinko, to Oberwolfach Report 2/2025, printed p.115. A dense G_delta in the space of all continuous actions of the restricted wreath product Z wr Z on Cantor space has hyperfinite orbit relation on the entire space. The auxiliary Borel theorem assumes an equivariant profinite shift height and permits stabilizers. The proof includes the entire exceptional integer-height preimage.

The generic-height construction specializes existing principles of Akin–Glasner–Weiss, Doucha, and Doucha–Melleray–Tsankov. The finite-width slab proof uses the exact nonfree and compatible-metric inputs of Conley–Jackson–Marks–Seward–Tucker-Drob. Iyer–Shinko's baseline is credited as a published 2025 paper. The dated, bounded priority review found no exact earlier resolution in the inspected corpus; it does not certify historical firstness or worldwide current openness.

OpenAI tools were used extensively in solving, drafting, diagnostics, and independent adversarial AI reviews. No completed external human peer review or formal proof-assistant certification is claimed. Finite checks support reproducibility and selected constructions; the infinite theorem is established by the mathematical argument relative to its published inputs.

## Contents of the verification archive

- `note.pdf` and editable `note.tex`: the current complete research note.
- `metadata.json`: the exact metadata supplied by the separate repository Zenodo upload manifest.
- `source/`: the unchanged 61-file original publication freeze, including all three original ZIPs and all 51 extracted members. Original pending-review or no-publication labels are historical statements, superseded by the dated current note and fresh audits.
- `audits/category/` and `audits/slab/`: fresh independent proof-family reviews, source checks, and supplemental diagnostics.
- `audits/priority/`: the completed fresh priority audit and two distinct literature families, with exact source locators and quantitative applicability checks.
- `root_evidence/`: the root's independent reconstruction, source/target checks, and reproducibility records. Earlier checkpoint labels retain their original dates; they are evidence of the sequence, not a replacement for the current note.
- `package_index.json` and `verify_package.py`: a closed regular-file inventory and portable verification entry point.

No downloaded source PDF, extract, rendering, raw dataset, credentials, or conversation transcript is distributed. Source retrieval metadata may name ignored local retrieval paths; those paths are provenance notes and are not needed to replay the package. The bibliography and source ledgers give public retrieval URLs. Final package-review receipts are retained separately in the repository so they can bind the frozen archive without a self-referential hash.

## Reproduction

Extract into an otherwise empty directory. Python 3.10 or newer and its standard library suffice; no network or external packages are required. Supply an independently trusted SHA-256 digest of `package_index.json` from the repository package seal:

```text
python3 -I -B verify_package.py TRUSTED_INDEX_SHA256 --full
python3 -I -B -O verify_package.py TRUSTED_INDEX_SHA256 --full
```

The first mode checks all package bytes, the original archive/extracted identities, the three historical diagnostic families, their 68 integrity rejections, and the fresh slab diagnostics. Optimized mode must reproduce the same semantic output. This does not verify the infinite theorem or novelty. A hash computed solely from the same downloaded index checks internal consistency, without independently establishing provenance; manifests are integrity bindings, not signatures.

Compile the editable note with a LaTeX engine supporting the listed standard packages, for example `tectonic note.tex`. Recompilation may change PDF metadata or binary bytes. The supplied PDF is bound to this release by the package index; mathematical reproducibility rests on reading its proof and checking the credited inputs.

The publication uses CC BY 4.0 for the authored note and supporting materials. Cited source documents retain their own terms.
