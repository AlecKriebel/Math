# Persistent archive checklist

Status: **PREPARED — DOI NOT YET ISSUED**

## Deposit object

- Archive filename: `stc_jc_sharp_boundary_reproducibility.tar.gz`
- SHA-256: `2ee0dd26322d83bd30bd54c02b5b2e028fc547d60579f1875124a8682a6b10f1`
- Immutable source commit:
  `01fdaa5bd1b9ae9f3cd39ee19226804ed68c0a4c`
- External seal: `release_artifacts/RELEASE_ENVELOPE.json`
- Checksum sidecar:
  `release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256`
- Recommended title: **Reproducibility package for “Strong Tree-Childness Is a Sharp Identifiability Boundary for Level-2 Jukes–Cantor Networks”**
- Author: Alec Kriebel
- ORCID: 0009-0001-9320-500X
- Affiliation: Independent Researcher
- Recommended description: Exact graph encodings, primary and clean-room symbolic implementations, graph-to-polynomial records, sign and Jacobian certificates, mutation tests, sharpness verifiers, release transcripts, and LaTeX sources supporting the associated preprint.
- Suggested keywords: phylogenetic networks; identifiability; Jukes–Cantor; level-2 networks; strongly tree-child; algebraic statistics; exact symbolic verification

## Files to upload

1. `stc_jc_sharp_boundary_reproducibility.tar.gz`
2. `stc_jc_sharp_boundary_reproducibility.tar.gz.sha256`
3. `RELEASE_ENVELOPE.json`
4. `RELEASE_ASSET_SHA256SUMS`
5. `biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf`
6. `biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf`
7. `biorxiv_submission/SHA256SUMS`

The deterministic archive is built from the immutable source commit with:

```bash
python reproducibility/build_biorxiv_release.py archive --commit <source-commit>
```

The archive contains a commit-independent core manifest and
`ARCHIVE_SOURCE_COMMIT.txt`.  Its final hash and the hashes of the appended
clean-clone transcripts live in the external, non-self-referential
`RELEASE_ENVELOPE.json`.  This avoids placing an archive's own digest inside
the bytes being digested.

Verify an isolated extraction with the pinned Python 3.14 environment (the
safe extraction API requires Python 3.12 or newer):

```bash
python reproducibility/verify_extracted_archive.py \
  release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz
```

## Human selections

- Choose the repository license deliberately. Plausible options include CC BY 4.0 for documentation/manuscript material and MIT or BSD-3-Clause for code, but no license is selected by this package.
- Review the generated archive and its manifest before deposit.
- Reserve or publish the deposit only after the final commit is public.
- Insert the repository-issued persistent identifier in the manuscript and metadata only after it exists. Do not invent a DOI.

## Identifier insertion point

After issue, replace the private placeholder in the release metadata field
`persistent_identifier` and, if desired, update the manuscript's Data and
code availability section. Until then the public PDF uses the accurate GitHub
repository URL and makes no DOI claim.
