# Preprint review cycle: artifact baseline

Checked 2026-09-23 13:31:51 UTC. This read-only baseline precedes the new reviewers' findings.

- All entries in the existing project SOURCE_SHA256SUMS, local Zenodo SHA256SUMS and website SHA256SUMS matched before the new research-log checkpoint was appended.
- Both verification scripts reproduced their saved JSON outputs exactly: 120 coefficient classes and 110 polarization checks in the main script; 500 determinant and 20 tensor/polarization comparisons in the adversarial implementation script.
- Both published ZIP archives passed CRC integrity checks.
- The seven files of the local website matched their repository docs/papers/brandes-coefficient-normalization copies byte for byte.
- A fresh Tectonic compilation of manuscript/paper.tex succeeded and produced three pages. Extracted text exactly matched the existing publication PDF. The only compiler diagnostics were two underfull bibliography lines, not missing references or clipped material.

Reviewed manuscript source SHA-256: `317ab083bdfc4e986921e517b368de8e1501c7f9a24b4faef5b047fe1d504f43`.

Reviewed publication PDF SHA-256: `a84cfe9347d3d0ce05ef0fb22e8648ee64fd77992825729d24991cf0fc1d627d`.

Subsequent review reports and log changes will be incorporated by rebuilding archives and their manifests. These checks support artifact consistency, not universal mathematical validity or publication priority.
