# Zenodo upload guide — K2P/K3P theta collision v1.2.6

> **Superseded:** do not use this software-first worksheet for the current
> upload. The final manuscript changed after v1.2.6, and the paper-first
> v1.2.7 upload is prepared in `../v1.2.7/`.

This is a manual-upload worksheet for the curated reproducibility package.
It does **not** authorize an upload, create a DOI, or replace the author's
final review of the Zenodo preview.

Use a manual Zenodo deposit. Do not enable GitHub–Zenodo automation for the
`Math` monorepo, do not create a repository-wide GitHub Release, and do not
upload the AI-referee packet.

Before selecting **New upload**, open **My uploads**, enable **View all
versions**, and search for this exact title and version, including unpublished
drafts with reserved DOIs. If an existing draft or record represents these
files, stop and continue that draft or use Zenodo's **New version** workflow;
do not create a duplicate standalone record.

## Recommended record scope

- **Record purpose:** reproducibility package supporting the separately posted
  manuscript.
- **Resource type:** `Software`
- **Do not select:** `Preprint` — bioRxiv will be the preprint record.

Zenodo advises choosing the most significant type for a mixed upload. Here the
record's purpose is to archive executable verifiers, exact certificates, and
replay materials; the manuscript PDF is included as documentation and for a
convenient preview. This also matches the package's `CITATION.cff`.

## Upload exactly these three files

Select these files individually:

1. Canonical replay ZIP

   `~/Documents/Math/k2p_k3p_theta_trinet_collision/releases/k2p-k3p-theta-v1.2.6/k2p-k3p-theta-collision-672d96a08be1.zip`

   - Size: `441490` bytes
   - SHA-256:
     `e0200c66b87c373fb718553ea2b9d8bbaa70c98bd78772ad1874cb9ccd47db12`

2. ZIP checksum sidecar

   `~/Documents/Math/k2p_k3p_theta_trinet_collision/releases/k2p-k3p-theta-v1.2.6/k2p-k3p-theta-collision-672d96a08be1.zip.sha256`

   - Size: `107` bytes
   - SHA-256 of the sidecar itself:
     `0d2b7cc8955a2ec1366fbf424386230044770e2ef08f13be9b0212d321aaa89f`

3. Main manuscript PDF, as a separately previewable convenience copy

   `~/Documents/Math/k2p_k3p_theta_trinet_collision/k2p_k3p_theta_clarified/combined-paper-clarified.pdf`

   - Size: `178508` bytes
   - SHA-256:
     `b39a95bd38d72de5ae1c27fea63828dfe9c6bf867562e23bffb2ad3de77441d3`
   - These bytes match the PDF inside the canonical replay ZIP.

After uploading, select `combined-paper-clarified.pdf` in Zenodo's **Preview**
column so that it is the default landing-page preview.

This three-file layout deliberately prioritizes a directly previewable paper
and an independently visible SHA-256 sidecar. Zenodo's optional automatic
Software Heritage path requires a Software record containing exactly one
compressed source archive, so automatic Software Heritage ingestion is **not**
targeted by this deposit. The immutable Git source and Zenodo files remain
available independently.

### Do not upload

- the tar.gz duplicate or its sidecar;
- `SHA256SUMS-672d96a08be1`, because it also names the intentionally omitted
  tar.gz file;
- loose copies of the technical summary, clarification note, certificates,
  source, or transcripts already contained in the canonical ZIP;
- the AI-referee packet or any referee report;
- bioRxiv worksheets, legacy versions, earlier releases, or the entire
  `Math` repository.

## Verify the selected files before upload

Run from a terminal:

```bash
cd ~/Documents/Math/k2p_k3p_theta_trinet_collision/releases/k2p-k3p-theta-v1.2.6
shasum -a 256 -c k2p-k3p-theta-collision-672d96a08be1.zip.sha256
shasum -a 256 k2p-k3p-theta-collision-672d96a08be1.zip.sha256
shasum -a 256 ../../k2p_k3p_theta_clarified/combined-paper-clarified.pdf
```

Expected output includes:

```text
k2p-k3p-theta-collision-672d96a08be1.zip: OK
0d2b7cc8955a2ec1366fbf424386230044770e2ef08f13be9b0212d321aaa89f  k2p-k3p-theta-collision-672d96a08be1.zip.sha256
b39a95bd38d72de5ae1c27fea63828dfe9c6bf867562e23bffb2ad3de77441d3  ../../k2p_k3p_theta_clarified/combined-paper-clarified.pdf
```

## Basic information — copy and paste

### DOI

- **Does this upload already have a DOI?** `No`

The future bioRxiv DOI belongs to a different object and must not be entered as
the existing DOI of this reproducibility package. Zenodo will assign a DOI when
the record is published. Reserving a DOI in the draft is optional; do so only
if the Zenodo DOI is needed for bioRxiv metadata before Zenodo publication.
Do not modify the frozen v1.2.6 files to insert a reserved DOI.

### Resource type

```text
Software
```

### Title

```text
Exact Tree–Theta-Trinet Collisions under the Kimura 2- and 3-Parameter Models: Reproducibility Package
```

### Publication date

```text
2026-08-27
```

This is the date on which the frozen v1.2.6 tag was first made public.

### Creator

- **Name type:** `Person`
- **Family name:** `Kriebel`
- **Given name:** `Alec`
- **ORCID:** `0009-0001-9320-500X`
- **Affiliation:** `Independent researcher`
- **Role:** leave blank

### Description

Copy both paragraphs:

```text
Exact certificates, standard-library verifiers, replay transcripts, and manuscript source supporting exact tree–theta-trinet distribution collisions under the Kimura two-parameter (K2P) and three-parameter (K3P) phylogenetic substitution models. The package covers exact parameter-level K3P symmetry breaking, nearby observably genuine K3P collisions, edgewise continuous-time strengthenings, full-rank and Zariski-density certificates, 11- and 14-dimensional fixed-output fibers, and one-theta grafting on arbitrary binary tree topologies. It includes the manuscript PDF and TeX source, exact JSON certificates, verification and build code, replay transcripts, integrity manifests, and replay instructions. No empirical data set is used.

Version 1.2.6 was built from Git commit 672d96a08be174cd6b67762a6907dfbdcd926b9b. Canonical ZIP SHA-256: e0200c66b87c373fb718553ea2b9d8bbaa70c98bd78772ad1874cb9ccd47db12. Please cite the manuscript for the mathematical results and cite this version-specific archival record when relying on its exact certificates or verifiers.
```

### Additional description — Technical information

If Zenodo offers **Add description**, select `Technical info` and paste:

```text
With Python 3.10 or newer, run python3 verify.py from the extracted package. The complete exact suite uses only the Python standard library and ends with ALL EXACT CHECKS PASSED. The universal arbitrary-taxon result is proved analytically in the manuscript; the finite four-leaf replay is a regression check. “Edgewise continuous time” permits different generators and rate ratios on different edges and does not assert a common generator, molecular clock, or global node-time model. The grafting theorem inserts one theta blob and does not assert independent multi-blob composition.
```

### Publisher

```text
Zenodo
```

### Version

```text
1.2.6
```

Use `1.2.6`, not `v1.2.6`.

### Language

```text
English
```

## Licenses and rights — current v1.2.6-compatible selection

Zenodo requires a rights entry and defaults to CC BY 4.0. **Do not leave that
default in place for v1.2.6.** The frozen package licenses executable Python
and shell code under MIT, while no reuse license is granted for the non-code
materials. Zenodo supports multiple and custom licenses.

Add both of the following rights entries.

### Rights entry 1

Search for and select:

```text
MIT License
```

### Rights entry 2 — custom

- **Title:**

  ```text
  No reuse license granted for non-code materials
  ```

- **Description:**

  ```text
  No reuse license is granted for the non-code materials in this deposit. To the extent protected by copyright, copyright © 2026 Alec Kriebel is retained for the manuscript, TeX source, figure, JSON certificates, verification transcripts, and documentation unless a file states otherwise. The MIT License applies only to executable Python and shell source. See LICENSES.md and LICENSE-CODE inside the canonical archive.
  ```

- **Link:**

  ```text
  https://github.com/AlecKriebel/Math/blob/672d96a08be174cd6b67762a6907dfbdcd926b9b/k2p_k3p_theta_trinet_collision/k2p_k3p_theta_clarified/LICENSES.md
  ```

This preserves the rights already stated inside the frozen package. If the
author instead wants CC BY 4.0 for the manuscript, certificates, transcripts,
and documentation, stop: that is a substantive new rights grant. Update
`LICENSES.md`, create a new internally consistent release/version, and align
the choice with the intended bioRxiv license before depositing it.

## Keywords and subjects

Add each as a separate custom keyword:

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

No controlled-vocabulary subject is required.

## Related works

Add this relation now:

- **Identifier:**

  ```text
  https://github.com/AlecKriebel/Math/tree/672d96a08be174cd6b67762a6907dfbdcd926b9b/k2p_k3p_theta_trinet_collision/k2p_k3p_theta_clarified
  ```

- **Relation:** `Is derived from`
- **Identifier type/scheme:** `URL`
- **Resource type, if requested:** `Software`

Do not enter a placeholder bioRxiv DOI. Once bioRxiv assigns a DOI, edit the
Zenodo metadata and add it as:

- **Relation:** `Is supplement to`
- **Identifier type/scheme:** `DOI`
- **Resource type:** `Preprint` or the closest publication/preprint choice
  offered by the interface

Metadata may be edited after publication; changing the deposited files should
instead use Zenodo's versioning workflow.

## Remaining fields

- **Files visibility/access:** `Public`
- **Embargo:** off
- **Copyright:** `© 2026 Alec Kriebel`, if that optional field is shown
- **Contributors:** none
- **Funding:** none / leave blank
- **Communities:** leave blank unless the author deliberately chooses a
  relevant moderated community
- **Alternate identifiers:** leave blank
- **References:** leave blank; references are contained in the manuscript
- **Locations/dates:** leave blank

### Software-specific fields, if shown

- **Repository URL:**

  ```text
  https://github.com/AlecKriebel/Math
  ```

- **Programming languages:** add `Python` and `Shell`
- **Development status:** leave blank; no maintenance commitment needs to be
  inferred from this frozen research release

## Final preview checklist — do not publish until every item passes

- [ ] Exactly three files are present, with the exact names above.
- [ ] The file sizes and SHA-256 values match this guide.
- [ ] `combined-paper-clarified.pdf` is the default preview.
- [ ] Resource type is `Software`, not `Preprint`.
- [ ] Title, creator, ORCID, publication date, and version match exactly.
- [ ] DOI question is `No`; no bioRxiv placeholder appears anywhere.
- [ ] Files are public and no embargo is active.
- [ ] Zenodo's default CC BY entry has been removed.
- [ ] Both current-rights entries and their scopes are visible.
- [ ] The immutable full-commit GitHub URL is present as `Is derived from`.
- [ ] The description contains the full commit and canonical ZIP SHA-256.
- [ ] The rendered record preview has no truncated title, description, or
  malformed Unicode.
- [ ] Download each uploaded file from the draft/preview if available and
  compare it byte-for-byte with the local source.
- [ ] The author has personally reviewed the final Zenodo preview and is ready
  for the DOI to become public.

Treat **Publish** as the irreversible checkpoint even though Zenodo may permit
limited post-publication corrections. Future substantive file changes should
be released as a new Zenodo version.

## Immediately after publication

Record all of the following before navigating away:

```text
Zenodo record URL:
Version-specific DOI:
Concept/all-versions DOI, if displayed:
Publication timestamp:
```

Then:

1. Verify the public landing page in a logged-out browser.
2. Download all three files and recheck their hashes.
3. Insert the **version-specific Zenodo DOI** into the bioRxiv code/data-
   availability metadata for the frozen v1.2.6 bytes. Use the concept/all-
   versions DOI only when intentionally citing the evolving record. Do not use
   the bioRxiv DOI as this package's DOI.
4. Add the bioRxiv DOI back to Zenodo later as `Is supplement to`.
5. Cite the version-specific Zenodo DOI when exact v1.2.6 bytes matter.

## Current official Zenodo guidance consulted

- [Create a new upload](https://help.zenodo.org/docs/deposit/create-new-upload/)
- [Manage files](https://help.zenodo.org/docs/deposit/manage-files/)
- [Resource types](https://help.zenodo.org/docs/deposit/describe-records/resource-type/)
- [Licenses and rights](https://help.zenodo.org/docs/deposit/describe-records/licenses/)
- [Digital Object Identifier](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
- [Manage versions](https://help.zenodo.org/docs/deposit/manage-versions/)
- [Upload software manually](https://help.zenodo.org/docs/github/archive-software/manual-upload/)

The official documentation was checked on 27 August 2026. Zenodo currently
allows up to 100 files and 50 GB per ordinary upload, recommends ZIP archives
for 20 or more files, supports mixed/custom rights entries, and permits a
specific previewable file to be selected as the record's default preview.
