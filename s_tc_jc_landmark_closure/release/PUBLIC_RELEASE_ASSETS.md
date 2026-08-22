# Persistent proof-certificate assets

Status: **PRE-DOI CANDIDATE — HUMAN DEPOSIT REQUIRED**

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

Before publication, the human author must replace `ZENODO_DOI_PENDING` by
running the documented DOI-finalization command, commit that DOI-bearing source
state, reseal the archive from a clean tree, and rerun all three archive-local
commands.  After publishing the Zenodo record, download the archive and run:

```bash
python reproducibility/verify_certificate_zenodo_release.py \
  /path/to/stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz
```

Only that exact DOI-bearing archive and the PDFs rebuilt from the same source
commit should be submitted to bioRxiv or a journal.
