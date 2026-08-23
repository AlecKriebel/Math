# Frozen package identity

- Scientific source commit: `b9a415f763e82d9cc45c83de96c895b109e158a4`
- Source archive SHA-256: `12a8c89b77aa898e9c16a1efdf93e77f35ea3cee3eed93ad34c7f497eaad3eb0`
- Manuscript PDF SHA-256: `5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd`
- Internal source-archive members: 73
- Archive members byte-checked against the source commit: 71
- Package format date: 2026-08-22
- Package remediation level: R3 exact-tree and interpreter-path hardening

The scientific source commit predates the wrapping commit that may add this
copied referee folder. It is the commit from which the archive and PDF were
built. `PACKAGE_MANIFEST.sha256` checks every other delivered file; the
detached transport-archive digest binds the package as a whole.
