# Frozen package identity

- Scientific source commit: `25e281a7a77c7020941d0c163c9b18e99165b09d`
- Source archive SHA-256: `7220a09d7eb31fdd81c42b35cbeb680f8c1b257df3b3002d37146b00d81e588e`
- Manuscript PDF SHA-256: `ec8c09fbc4ef5f382272351f69721b6544c69f5d48bee961447e1907de2c0180`
- Internal source-archive members: 73
- Archive members byte-checked against the source commit: 71
- Package format date: 2026-08-23
- Package remediation level: R4 layout/date refresh on the R3 exact-tree hardening

The scientific source commit predates the wrapping commit that may add this
copied referee folder. It is the commit from which the archive and PDF were
built. `PACKAGE_MANIFEST.sha256` checks every other delivered file; the
detached transport-archive digest binds the package as a whole.
