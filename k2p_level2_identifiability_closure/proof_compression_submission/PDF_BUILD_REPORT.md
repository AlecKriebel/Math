# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787788800`
(`2026-08-27T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `20387611077cf1bfb128456e523b34f46c5a98537c6bbf6ddb5436911f8c9dec` | `186522a14070fc872e67e75736804fa14621104803225f73615d7f76d09f9a11` | 26 | 194,515 |
| reader supplement | `e96888fc17c1f7084c951ba8efbabd61cf6f9b8a2d60c91e256508a3189177a2` | `c402b463a8bc89728cd95dac671fbb166acb2e2c415ace3c267253d4a9bc5296` | 24 | 160,292 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `4f0d4a04018dab323b2b03fa280ced7149efba0bff2bdcffa415fb18a667feae`.
