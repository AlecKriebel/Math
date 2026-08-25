# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787529600`
(`2026-08-24T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `983ddc75e568ff9278481c5e43159a9dc566c3dfc9aa1db9c6e31ae6c13c5c3c` | `9934a92091d069c8764cf8c3aba6b496d482e4e0d5d0a526586f5a0d133f0411` | 26 | 194,316 |
| reader supplement | `4c6a463d2ef1e3b3505012836baa8b81c162def0938ae504d3545ea42f6bd216` | `486d4a88ef91e839e170f47f224e634f7ddaac1fa47503aa2a3c7aa1dd7f8f69` | 24 | 158,984 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `aa31370904509bd9e5d85837729e9bed015ec9e579be6d82e742bf8040f205cd`.
