# Zenodo upload guide -- full paper v1.2.7

This worksheet is for a **paper-first public preprint record**. The manuscript
PDF is the primary object and the exact source/verifier/replay archive is its
supporting material. This supersedes the software-first v1.2.6 worksheet.

The record documents public archival chronology for these exact files. Do not
describe Zenodo as establishing legal priority, certifying validity, or
providing peer review.

## Upload exactly these three files

All three are already collected in:

`~/Documents/Math/k2p_k3p_theta_trinet_collision/submission/zenodo/v1.2.7/upload_files/`

1. `Kriebel_2026_Exact_Tree_Theta_Trinet_Collisions_v1.2.7.pdf`
   - Size: `178692` bytes
   - SHA-256:
     `7f1ecd0e70504736146eb8f2d4ebfb43980fd1feef50cf39bbe7e751ad5afa8f`
   - Select this as Zenodo's default preview.

2. `k2p-k3p-theta-collision-19cf11f65ed4.zip`
   - Size: `443027` bytes
   - SHA-256:
     `7c603e15f6afb7546f618b88bbefdc52ee264b656399f6656fc742aeabb786c7`
   - Contains the byte-identical PDF and TeX source, supporting PDFs, exact
     certificates, standard-library verifiers, replay transcripts, build
     files, licenses, provenance, and integrity manifests.

3. `SHA256SUMS`
   - Size: `232` bytes
   - SHA-256 of the checksum file itself:
     `f0de6a53cd36c66db6d7d66c3dbd86b9cf8a62985e43a7d44da01a6bcc4387c2`
   - Covers both the standalone paper and the canonical ZIP.

Do not upload the v1.2.6 files, the tar.gz duplicate, the monorepo, AI-referee
packets, referee reports, legacy versions, or author-only bioRxiv worksheets.

## Verify immediately before upload

```bash
cd ~/Documents/Math/k2p_k3p_theta_trinet_collision/submission/zenodo/v1.2.7/upload_files
shasum -a 256 -c SHA256SUMS
shasum -a 256 SHA256SUMS
unzip -tq k2p-k3p-theta-collision-19cf11f65ed4.zip
unzip -p k2p-k3p-theta-collision-19cf11f65ed4.zip \
  k2p-k3p-theta-collision-19cf11f65ed4/combined-paper-clarified.pdf \
  | shasum -a 256
```

Expected results:

```text
Kriebel_2026_Exact_Tree_Theta_Trinet_Collisions_v1.2.7.pdf: OK
k2p-k3p-theta-collision-19cf11f65ed4.zip: OK
f0de6a53cd36c66db6d7d66c3dbd86b9cf8a62985e43a7d44da01a6bcc4387c2  SHA256SUMS
No errors detected in compressed data of k2p-k3p-theta-collision-19cf11f65ed4.zip.
7f1ecd0e70504736146eb8f2d4ebfb43980fd1feef50cf39bbe7e751ad5afa8f  -
```

## Zenodo metadata -- copy and paste

### Existing DOI

```text
No
```

The paper does not already have a DOI. Let Zenodo assign the version DOI when
the record is published. Do not enter a future bioRxiv DOI as this record's
existing DOI.

### Resource type

Select:

```text
Publication -> Preprint
```

If the interface displays only the subtype, select `Preprint`. Do not select
`Software`: the paper is now the record's primary object.

### Title

```text
Exact Tree–Theta-Trinet Collisions under the Kimura 2- and 3-Parameter Models
```

### Publication date

```text
2026-08-27
```

### Creator

- Name type: `Person`
- Family name: `Kriebel`
- Given name: `Alec`
- ORCID: `0009-0001-9320-500X`
- Affiliation: `Independent researcher`
- Role: leave blank

Do not add the acknowledged correspondents as creators or contributors.

### Description

Copy all paragraphs below:

```text
We construct exact distributions shared by a phylogenetic tree and a binary semi-directed strict level-two theta network under the Kimura two-parameter (K2P) and three-parameter (K3P) substitution models. The compact three-leaf K2P construction lies in the strict stochastic interior and is an exact counterexample to the formal K2P lemma and the K2P part of the corresponding global corollary removed between Versions 2 and 3 of Brits, Holtgrefe, van Iersel, and Martin. Because K2P is nested in K3P, this collision alone answers both high-level Kimura tree–trinet disjointness questions posed in Version 3 negatively. We additionally give an exact K3P theta realization whose network parameter lies outside every globally character-relabelled K2P specialization, while openly identifying its shared distribution as globally character-relabelled K2P. Full-rank Jacobians show that the fixed theta images are Zariski dense in the effective K2P and K3P Fourier spaces. Locally, the collision loci have dimensions 17 and 23 and project submersively onto the tree models, with 11- and 14-dimensional fixed-output network fibers. Consequently, a relatively open dense set of nearby K3P tree distributions outside every globally character-relabelled K2P submodel also has theta realizations. These conclusions persist in edgewise strictly continuous-time chambers, where generators and rate ratios may vary by edge and no clock or global timing is imposed. Finally, a common-subtree argument replaces any chosen internal vertex of any labelled unrooted binary tree by one theta blob while preserving the full leaf-pattern distribution; hence exact strict-interior collisions occur for every number of leaves. For the compact K2P and quartic K3P witnesses, exact verifiers separately reconstruct the retained-graph Fourier coordinates and perform ordinary-state Markov pruning in every pattern.

Preprint; not peer reviewed by a journal. This record archives version 1.2.7 of the full manuscript together with its exact certificates, standard-library verifiers, replay transcripts, source files, and integrity manifests. The deposited files correspond to Git commit 19cf11f65ed448cf031842b666e4bfc7e02a9ab7 and canonical archive SHA-256 7c603e15f6afb7546f618b88bbefdc52ee264b656399f6656fc742aeabb786c7. Zenodo's record metadata documents when this version was uploaded and made publicly available through the repository. No empirical data set is used. AI-assisted exploratory analysis, code assistance, adversarial checking, and editorial review are disclosed in the manuscript's “Provenance and AI-assisted methods” section.
```

### Additional description -- Technical information

If the interface offers **Add description**, choose `Technical info` and paste:

```text
With Python 3.10 or newer, extract the canonical ZIP and run python3 verify.py from its top-level directory. The complete exact suite uses only the Python standard library and ends with ALL EXACT CHECKS PASSED. The release builder replayed the suite under ordinary and optimized Python, rejected the targeted hostile JSON/schema mutations, rebuilt the PDFs from a clean extraction, and checked the archive manifests. The universal arbitrary-taxon result is proved analytically in the manuscript; the finite four-leaf replay is a regression check. “Edgewise continuous time” permits different generators and rate ratios on different edges and does not assert a common generator, molecular clock, or global node-time model. The grafting theorem inserts one theta blob and does not assert independent multi-blob composition.
```

### Publisher

```text
Zenodo
```

### Version

```text
1.2.7
```

### Language

```text
English
```

## Licenses and rights

The v1.2.7 files retain the existing mixed-rights boundary. Remove Zenodo's
default CC BY entry; no new manuscript reuse license has been authorized.

Add both rights entries below.

### Rights entry 1

```text
MIT License
```

This applies only to executable Python and shell source.

### Rights entry 2 -- custom

- Title:

  ```text
  No reuse license granted for non-code materials
  ```

- Description:

  ```text
  No reuse license is granted for the non-code materials in this deposit. To the extent protected by copyright, copyright © 2026 Alec Kriebel is retained for the manuscript, TeX source, figure, JSON certificates, verification transcripts, and documentation unless a file states otherwise. The MIT License applies only to executable Python and shell source. See LICENSES.md and LICENSE-CODE inside the canonical archive.
  ```

- Link:

  ```text
  https://github.com/AlecKriebel/Math/blob/19cf11f65ed448cf031842b666e4bfc7e02a9ab7/k2p_k3p_theta_trinet_collision/k2p_k3p_theta_clarified/LICENSES.md
  ```

If a Creative Commons license is desired for the paper, stop before publishing:
that is a substantive new rights grant and should be made consistently across
the repository, Zenodo, and bioRxiv.

## Keywords

Add each separately:

```text
phylogenetic networks
identifiability
group-based models
Kimura two-parameter model
Kimura three-parameter model
computer-assisted proof
edgewise continuous-time embeddability
algebraic statistics
observational equivalence
```

## Related works

Add the immutable source/replay snapshot:

- Identifier:

  ```text
  https://github.com/AlecKriebel/Math/tree/19cf11f65ed448cf031842b666e4bfc7e02a9ab7/k2p_k3p_theta_trinet_collision/k2p_k3p_theta_clarified
  ```

- Relation: `Is supplemented by`
- Identifier type/scheme: `URL`
- Resource type, if requested: `Software`

Do not add a placeholder bioRxiv DOI. After bioRxiv posts, use `Is identical
to` only if the posted edition is exactly the same; otherwise select the
accurate version relation.

## Remaining fields

- Access: `Public`
- Embargo: off
- Copyright, if shown: `© 2026 Alec Kriebel`
- Contributors: none
- Funding: none / leave blank
- Communities: leave blank unless deliberately selected
- Alternate identifiers: leave blank
- References: leave blank; they are in the paper
- Locations/dates: leave blank
- Repository URL, if shown:
  `https://github.com/AlecKriebel/Math`

## Final preview gate

- [ ] Exactly the three named files are present.
- [ ] `SHA256SUMS` passes and the ZIP opens without error.
- [ ] The PDF inside the ZIP matches the standalone PDF hash.
- [ ] The manuscript PDF is the selected default preview.
- [ ] Resource type is `Preprint`, not `Software`.
- [ ] Title, creator, ORCID, date, and version match this guide.
- [ ] Existing DOI is `No`; no bioRxiv placeholder appears.
- [ ] Access is public and no embargo is active.
- [ ] Zenodo's default CC BY entry has been removed.
- [ ] Both current rights entries and their scopes are visible.
- [ ] The full-commit GitHub relation is present.
- [ ] No AI-referee packet, report, old release, or tar.gz duplicate is present.
- [ ] The final preview has no truncated text or malformed Unicode.
- [ ] The author has personally reviewed the preview and is ready for the DOI
      and public record to be created.

## Immediately after publishing

Record:

```text
Zenodo record URL:
Version-specific DOI:
Concept/all-versions DOI, if displayed:
Publication timestamp:
```

Then verify the public landing page while logged out, download all three files,
recheck `SHA256SUMS`, and use the version-specific Zenodo DOI in the subsequent
bioRxiv metadata. Do not rewrite the immutable v1.2.7 tag or deposited files.

## Official Zenodo guidance

- [Create a new upload](https://help.zenodo.org/docs/deposit/create-new-upload/)
- [Resource types](https://help.zenodo.org/docs/deposit/describe-records/resource-type/)
- [Manage files and previews](https://help.zenodo.org/docs/deposit/manage-files/)
- [Publication date](https://help.zenodo.org/docs/deposit/describe-records/publication-date/)
- [Digital Object Identifier](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
- [Licenses and rights](https://help.zenodo.org/docs/deposit/describe-records/licenses/)

These pages were checked on 27 August 2026.
