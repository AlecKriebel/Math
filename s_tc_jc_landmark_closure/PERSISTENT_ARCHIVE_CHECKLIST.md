# Persistent archive checklist

Status: **PREPARED — DOI NOT YET ISSUED**

## Deposit object

- Archive filename: `stc_jc_sharp_boundary_reproducibility.tar.gz`
- SHA-256: recorded after the revised immutable source commit is replayed, in
  `release_artifacts/RELEASE_ENVELOPE.json` and the checksum sidecar
  `release_artifacts/stc_jc_sharp_boundary_reproducibility.tar.gz.sha256`.
- Recommended title: **Reproducibility package for “Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for Level-2 Jukes–Cantor Networks”**
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
5. `FINAL_RELEASE_ENGINEERING_REPORT.md`
6. `clean_clone_transcripts/verify_quick.log`
7. `clean_clone_transcripts/verify_full.log`
8. `clean_clone_transcripts/verify_regenerate_all.log`
9. `biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf`
10. `biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf`
11. `biorxiv_submission/SHA256SUMS`

The first eight files are the intended exact public replay assets at
`https://github.com/AlecKriebel/Math/releases/tag/stc-jc-sharp-boundary-v1.1.4`.
They become current public evidence only after all eight are uploaded and
`verify_public_release.py` returns `PUBLIC_RELEASE_VERIFIED`. Before manuscript
submission, download `RELEASE_ENVELOPE.json` and `RELEASE_ASSET_SHA256SUMS`
from that page and compare them with the local release. The tracked records
under `history/superseded_release_evidence/` certify an older 18-page
manuscript and are not current evidence.

The public manifest is deliberately flat and covers the other seven assets by
basename, including `RELEASE_ENVELOPE.json`; it does not and cannot hash
itself.  Treat the downloaded manifest as the trust anchor and run
`reproducibility/verify_public_release.py` for the complete tag, archive,
envelope, and transcript check.

The deterministic archive is built from the immutable source commit with:

```bash
python s_tc_jc_landmark_closure/reproducibility/build_biorxiv_release.py archive --commit <source-commit>
```

The archive contains a commit-independent core manifest and
`ARCHIVE_SOURCE_COMMIT.txt`.  Its final hash and the hashes of the appended
clean-clone transcripts live in the external, non-self-referential
`RELEASE_ENVELOPE.json`.  This avoids placing an archive's own digest inside
the bytes being digested.

The immutable source commit is also marked by the annotated tag
`stc-jc-sharp-boundary-v1.1.4`.  In a source-only clone the active verifier
requires that exact tag to peel to a clean checkout.  In a deposited release
bundle it instead verifies the external envelope and every accompanying
asset.  The large archive and its outer envelope are intentionally release
assets rather than Git objects. Exact publication commands and the required
eight-asset list are recorded in `release/UPLOAD_RELEASE_ASSETS.md` and
`release/PUBLIC_RELEASE_ASSETS.md`.

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
