# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787788800`
(`2026-08-27T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `d1344711d3d85ce5936574ccf54bcfbea1bf4164a0d2b6f5d25d5ecb483991bb` | `a6b91bc5d8864d1ce1a6eb352d00ecdf83712449b41fa4ad041e43a4c06e4858` | 26 | 194,574 |
| reader supplement | `e0fe9e08c923a2946c282a3b19aa66c4c6aaa52e762639977024f538295de455` | `654f9150a2a22be18c651d9bd38864be2a080828dbcdad847d2b344e407ebdb2` | 24 | 160,272 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `70394f0cb0a4b2947fb64c327431185c2fbd57df5f6c10fd1b5eecea221f0d89`.
