# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787788800`
(`2026-08-27T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `20387611077cf1bfb128456e523b34f46c5a98537c6bbf6ddb5436911f8c9dec` | `186522a14070fc872e67e75736804fa14621104803225f73615d7f76d09f9a11` | 26 | 194,515 |
| reader supplement | `c1cbf3f3bc2e7ce2df3972eb5a0a6839eef4eae59aca6735be91db7a0fb7b0b5` | `f317a4a6f14cfebc0f58ff0e8ebeb5ecd9659c5bb3fa2af8e92f8235dace7d44` | 24 | 160,280 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `fd1b49bba0eb3793e528c8b8b169f1953773a005c58d3058bd675ce3e3803438`.
