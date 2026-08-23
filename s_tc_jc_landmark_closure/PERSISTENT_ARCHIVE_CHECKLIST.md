# Zenodo certificate-deposit checklist

Status: **DOI-BEARING CURATED PROOF OBJECT SEALED AND VERIFIED**

Reserved Zenodo DOI: `10.5281/zenodo.22064121`

Final upload candidate:

- source commit: `fef87ba874b3476ff0383095c67c031ba8c0dc23`
- final submission/package tag: `stc-jc-sharp-boundary-v1.1.7`
- archive SHA-256: `ffcce5398c8be387d6d808620fc939490f31ac41fb48592e22608cf0e7b05db4`
- prepared-payload SHA-256:
  `f6139234c859d22d87f532589e120988268b0cf122ae2db0c34214fbb1c01382`
- record-level evidence commitment:
  `38e6f9aa59e799de23711824dd5d1934aad1fd734a57564784119e3348a534c4`
- clean source commit: `fef87ba874b3476ff0383095c67c031ba8c0dc23`
- authenticated payload files: `241`
- archive bytes: `94,158,772`
- transcript SHA-256 values:
  - quick: `43d5b5d4dcdfede81b043cbc51d6badf05bd12ae3a9bd6977e0b8ad5c3b5fb43`
  - full: `ba190497dd20e5eace25ffcf8a21cb547b120e238e7e535e44a57db454010f14`
  - regenerate-all: `3727528cc886b68d111214a8170f12cae31edf42d274d57292474e3cb3d6c54f`
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

## Publication handoff

Upload the files listed above to the existing Zenodo draft, verify their names
and checksums, and publish the record.  The DOI will not resolve publicly until
that human publication step is complete.  After publication, download the
archive from Zenodo and authenticate the downloaded bytes with:

```bash
python reproducibility/verify_certificate_zenodo_release.py \
  /path/to/stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz
```

Submit only the final DOI-bearing PDFs and capsule listed in the active package
manifests.  No further DOI insertion or archive resealing is required unless a
curated-payload file or delivered artifact is changed.

The certificate source commit above identifies the immutable graph-to-algebra
proof payload.  The final submission tag identifies the later packaging commit
that contains the DOI-visible PDFs, source archives, and portal manifests; the
two identifiers intentionally serve different roles.
