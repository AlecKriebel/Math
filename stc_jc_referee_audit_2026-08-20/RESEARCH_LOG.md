# Independent referee audit log

## Scope

Adversarial mathematical and reproducibility audit of *Strong Tree-Childness Is the Sharp Identifiability Boundary for Level-2 Jukes-Cantor Networks*, its supplement, source package, and certificate archive v1.1.5.

The target conclusion is treated as a hypothesis. Passing scripts are not accepted as mathematical evidence unless their outputs are traced to primitive inputs and independently regenerated.

## 2026-08-20 20:55 PDT - Checkpoint 1: archive authentication

- Computed SHA-256 of `stc_jc_sharp_boundary_atlas_certificates_v1.1.5.tar.gz`:
  `66f0e324b9cdb1448806eecd9cd9397f9e8c45f4762ff48c5750cd64d2938e6a`.
- The value exactly matches the separate `.sha256` file and `archive_sha256` in `CERTIFICATE_BUNDLE_ENVELOPE.json`.
- Computed byte count is 79,567,059, exactly matching `archive_bytes` in the envelope.
- `gzip -t` succeeded; all tar member names are relative and traversal-free; the archive contains no symbolic-link members.
- Trust boundary: the supplied envelope has no digital signature or independently resolved publication identifier (`zenodo_doi` is `ZENODO_DOI_PENDING`). Authentication therefore proves consistency with the supplied sidecar files, not external provenance or authorship.

Best-guess completion: **4%**.

