# Version 2 manuscript

This directory contains the Version 2 manuscript source integrating the
frozen v1 theorem with the exact fixed-support rate family, its positive cone,
generic geometric coprimality, the clean integer optimum, and transverse
stability of the frozen ellipse.

From the repository root, verify every computational claim with

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/manuscript_v2_draft/verify_v2_claims.py
```

Build the PDF locally with

```sh
sh weakly_reversible_continuum_no_common_factor/manuscript_v2_draft/build_pdf.sh
```

The build writes only to `manuscript_v2_draft/output/pdf/` and does not
publish, release, upload, or contact any external service.
