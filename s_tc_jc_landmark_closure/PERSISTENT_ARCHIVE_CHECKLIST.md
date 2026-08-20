# Zenodo certificate-deposit checklist

Status: **CURATED PROOF OBJECT VERIFIED — DOI PENDING**

Current pre-DOI candidate (the hash will change when the reserved DOI is
inserted and the archive is resealed):

- source commit: `8f28b6238b815bd531b621ea3ad629d173708712`
- archive SHA-256: `b165b6e65615c144c0a8b60e4381e453c20a6bb02602134384aa037f80cd26f7`
- record-level evidence commitment:
  `09adbe4c639246b8a966d183984f1e1883246b92bd8927e2552a3cc5a25b505b`
- finite universe: 10,466 three-outgoing relations and 192 four-outgoing
  survivors

## Record metadata

- Recommended title: **Computer-assisted proof certificates and reproducibility package for “Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for Level-2 Jukes–Cantor Networks”**
- Creator: Alec Kriebel
- ORCID: 0009-0001-9320-500X
- Affiliation: Independent Researcher
- Version: v1.1.5
- Primary resource type: Dataset (computer-assisted proof certificates)
- Description: Curated primitive graph inputs, complete finite directed-relation atlases, exact per-relation polynomial/sign/rank certificates, raw-to-canonical transports, restoration and probe records, and primary plus separately implemented verifiers supporting the associated preprint. The record also contains a secondary full reproducibility snapshot and the article/supplement PDFs.
- Suggested keywords: phylogenetic networks; identifiability; Jukes–Cantor; level-2 networks; strongly tree-child; algebraic statistics; exact symbolic verification
- License: human selection required. The archive contains separate code and manuscript license notices; do not infer the Zenodo record license automatically.

## Files to upload

Required proof object:

1. `stc_jc_sharp_boundary_atlas_certificates_v1.1.5.tar.gz`
2. `stc_jc_sharp_boundary_atlas_certificates_v1.1.5.tar.gz.sha256`
3. `CERTIFICATE_BUNDLE_ENVELOPE.json`
4. `certificate_bundle_logs/verify_quick.log`
5. `certificate_bundle_logs/verify_full.log`
6. `certificate_bundle_logs/verify_regenerate_all.log`

Recommended secondary files:

7. `stc_jc_sharp_boundary_reproducibility.tar.gz`
8. `stc_jc_sharp_boundary_reproducibility.tar.gz.sha256`
9. final article PDF
10. final supplement PDF
11. a plain copy of `certificate_bundle/README_FIRST.md`

The curated archive is the canonical proof object cited by Theorem 6.3. The
broader snapshot is secondary provenance and should be labelled accordingly.
Legacy `RELEASE_ENVELOPE.json`, `RELEASE_ASSET_SHA256SUMS`, and older
clean-clone transcripts are not part of this v1.1.5 deposit unless they are
regenerated after DOI finalization.  The authoritative envelope for the
curated object is `CERTIFICATE_BUNDLE_ENVELOPE.json`.

## DOI handoff

Reserve the DOI in the Zenodo draft, then run the following sequence from the
project root.  The certificate archive itself must be rebuilt after the DOI is
inserted; changing only the manuscript or release envelope is insufficient.

```bash
python reproducibility/finalize_zenodo_doi.py --doi 10.5281/zenodo.<issued-number>
python reproducibility/test_finalize_zenodo_doi.py
git diff --check
# Review the DOI-only diff, then commit it before sealing so the archive's
# source_commit identifies the DOI-bearing source state.
git add source certificate_bundle biorxiv_submission journal_submission \
        release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json
git commit -m "Insert reserved Zenodo certificate DOI"

python reproducibility/build_certificate_bundle.py prepare
python reproducibility/build_certificate_bundle.py seal
bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.5/verify.sh quick
bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.5/verify.sh full
bash release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.5/verify.sh regenerate-all

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
