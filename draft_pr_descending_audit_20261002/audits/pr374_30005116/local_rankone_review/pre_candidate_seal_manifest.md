# Pre-candidate seal manifest

Exact clock read after control execution: **2026-10-03 07:45:47 UTC**. This precedes candidate access. Hashes:

- independent_seal.md SHA256 `1bc245006ee8e26a4643ae2294b16e8dc450f590b6d600f48f0cf0346602470e`
- independent_controls.py SHA256 `7392c9bee8f575c8cc7acc512591742256af75d1958e8d022c601f6e6af3562b`
- independent_controls.fullstream.txt SHA256 `2ad5f8e78a398ea17a72aca6524cf558cf65a58b7df3986fe5f93c7895495e2d`

Metadata correction preserved: the seal and initial log used estimated minute labels 07:48, 07:43, 07:48; the final two are inaccurate because the actual clock at completion was 07:45:47. Treat exact observed first clock 07:40:57 and exact completed-seal clock 07:45:47 as authoritative. No mathematical deduction changed. The estimate error is preserved rather than silently rewriting the sealed artifact.
