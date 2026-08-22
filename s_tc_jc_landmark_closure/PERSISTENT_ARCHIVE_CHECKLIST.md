# Zenodo certificate-deposit checklist

Status: **CURATED PROOF OBJECT VERIFIED — DOI PENDING**

Current pre-DOI candidate (the hash will change when the reserved DOI is
inserted and the archive is resealed):

- source commit: `6ae493191e2f080d2d902d8580c4819012ff27fd`
- archive SHA-256: `01f8a81ae402893a58d87c80520005d9190f0c672c9e7c839769e5eb06ac4842`
- record-level evidence commitment:
  `38e6f9aa59e799de23711824dd5d1934aad1fd734a57564784119e3348a534c4`
- clean source commit: `6ae493191e2f080d2d902d8580c4819012ff27fd`
- authenticated payload files: `241`
- archive bytes: `94,158,712`
- transcript SHA-256 values:
  - quick: `06309f4baff2d1f580c68a97ecec2058f0397227c6243e5bff71963702291ebf`
  - full: `a91af0e1ed5a2f7bda49790ec64fff0a4c76f5958fe8a4080e5d824e8f3b681b`
  - regenerate-all: `9cf6d8ca814f8a45cf16a0173b087ba7c60ec18cde781be03d7beb96de853a22`
- finite universe: 10,466 three-outgoing relations and 192 four-outgoing
  survivors

## Record metadata

- Recommended title: **Computer-assisted proof certificates and reproducibility package for “Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for Level-2 Jukes–Cantor Networks”**
- Creator: Alec Kriebel
- ORCID: 0009-0001-9320-500X
- Affiliation: Independent Researcher
- Version: v1.1.7
- Primary resource type: Dataset (computer-assisted proof certificates)
- Description: Curated primitive graph inputs, complete finite directed-relation atlases, exact per-relation polynomial/sign/rank certificates, raw-to-canonical transports, restoration and probe records, and primary plus separately implemented verifiers supporting the associated preprint. The record also contains the article and supplement PDFs.
- Suggested keywords: phylogenetic networks; identifiability; Jukes–Cantor; level-2 networks; strongly tree-child; algebraic statistics; exact symbolic verification
- License: human selection required. The archive contains separate code and manuscript license notices; do not infer the Zenodo record license automatically.

## Files to upload

Required proof object:

1. `stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz`
2. `stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz.sha256`
3. `CERTIFICATE_BUNDLE_ENVELOPE.json`
4. `certificate_bundle_logs/verify_quick.log`
5. `certificate_bundle_logs/verify_full.log`
6. `certificate_bundle_logs/verify_regenerate_all.log`

Recommended reader-facing files:

7. final article PDF
8. final supplement PDF
9. a plain copy of `certificate_bundle/README_FIRST.md`

The curated archive is complete and is the canonical proof object cited by
Theorem 6.3. No omnibus development snapshot is required for verification.
Legacy `RELEASE_ENVELOPE.json`, `RELEASE_ASSET_SHA256SUMS`, and older
clean-clone transcripts are not part of this v1.1.7 deposit unless they are
regenerated after DOI finalization.  The authoritative envelope for the
curated object is `CERTIFICATE_BUNDLE_ENVELOPE.json`.

## DOI handoff

Reserve the DOI in the Zenodo draft, then run the following sequence from the
project root.  The certificate archive itself must be rebuilt after the DOI is
inserted; changing only the manuscript or release envelope is insufficient.

```bash
python reproducibility/test_finalize_zenodo_doi.py
python reproducibility/finalize_zenodo_doi.py --doi 10.5281/zenodo.<issued-number>
git diff --check
# Review the DOI-only diff, then commit it before sealing so the archive's
# source_commit identifies the DOI-bearing source state.
git add source certificate_bundle biorxiv_submission journal_submission \
        THEOREM_CERTIFICATE_CROSSWALK.md
git commit -m "Insert reserved Zenodo certificate DOI"

# The entire release_artifacts/ tree is ignored build output, so preparation
# does not dirty the committed source. Seal independently prepares a second
# payload from the same clean commit, byte-compares both stages, and archives
# only the fresh reconstruction.
python -I -S reproducibility/build_certificate_bundle.py prepare
python -I -S reproducibility/build_certificate_bundle.py seal
bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.7/verify.sh quick
bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.7/verify.sh full
bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.7/verify.sh regenerate-all

python reproducibility/build_biorxiv_release.py submission
python reproducibility/build_journal_packages.py
python reproducibility/verify_submission_source_archives.py
```

Capture the three verifier transcripts beside the newly sealed archive and
update this checklist with its final SHA-256. Publish the Zenodo record only
after the DOI-bearing archive, papers, capsule, manifests, and exact logs are
in the draft. Download the published archive and authenticate it with
`reproducibility/verify_certificate_zenodo_release.py` before submitting the
same DOI-bearing PDFs to bioRxiv. Never invent or pre-register a number in the
repository.
