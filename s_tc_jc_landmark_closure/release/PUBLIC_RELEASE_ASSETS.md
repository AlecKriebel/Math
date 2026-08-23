# Persistent proof-certificate assets

Status: **DOI RESERVED — HUMAN DEPOSIT AND PUBLICATION REQUIRED**

The authoritative external proof object is the curated Zenodo deposit prepared
from `release_artifacts/`.  It replaces the earlier omnibus development
snapshot and contains only the transitive closure of active theorem evidence.
The human author must reserve and publish the DOI; no repository command does
that automatically.

Required Zenodo files:

1. `stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz`
2. `stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz.sha256`
3. `CERTIFICATE_BUNDLE_ENVELOPE.json`
4. `certificate_bundle_logs/verify_quick.log`
5. `certificate_bundle_logs/verify_full.log`
6. `certificate_bundle_logs/verify_regenerate_all.log`
7. the final article PDF
8. the final supplement PDF
9. a plain copy of `certificate_bundle/README_FIRST.md`

The archive contains the complete finite theorem universe, per-record exact
certificates and transports, restoration and probe closure, primitive inputs,
primary implementations, and separately implemented replays.  The three run
logs are source-commit-bound external records; they are not embedded in the
self-authenticating archive.

The reserved DOI is `10.5281/zenodo.22064121`.  The DOI-bearing archive has
been resealed from clean source commit
`fef87ba874b3476ff0383095c67c031ba8c0dc23`; its SHA-256 is
`ffcce5398c8be387d6d808620fc939490f31ac41fb48592e22608cf0e7b05db4`.
All three archive-local commands passed, including two-run complete
regeneration.  The human author must now upload these exact assets and publish
the draft.  After publication, download the archive and run:

```bash
python reproducibility/verify_certificate_zenodo_release.py \
  /path/to/stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz
```

Only that exact DOI-bearing archive and the final DOI-bearing PDFs listed in
the active package manifests should be submitted to bioRxiv or a journal.
The archive's source commit identifies the immutable certificate payload; Git
tag `stc-jc-sharp-boundary-v1.1.7` identifies the later submission/package
commit containing those final PDFs and manifests.
