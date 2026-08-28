# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787788800`
(`2026-08-27T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `20387611077cf1bfb128456e523b34f46c5a98537c6bbf6ddb5436911f8c9dec` | `186522a14070fc872e67e75736804fa14621104803225f73615d7f76d09f9a11` | 26 | 194,515 |
| reader supplement | `20a44599a4d1ca0f155c7018b311b3d8e876c7c6560347f5987e8f76cecf580b` | `c31ba938e118089b1148e3f119fc1ac048b381a0c9c75dddadf6388ec7d061b5` | 24 | 160,289 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `51d9054b56578324ff9b904dd237a86ba3bce2998848ca56b83ebbdbacb3e4c4`.
