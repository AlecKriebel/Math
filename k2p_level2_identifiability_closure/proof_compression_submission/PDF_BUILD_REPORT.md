# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787529600`
(`2026-08-24T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `983ddc75e568ff9278481c5e43159a9dc566c3dfc9aa1db9c6e31ae6c13c5c3c` | `9934a92091d069c8764cf8c3aba6b496d482e4e0d5d0a526586f5a0d133f0411` | 26 | 194,316 |
| reader supplement | `4166832734f84cd0752f283be6a094249f969e863d084bd11957031f256b8140` | `66161998ec9b30355ac3f6f6467462e8be32230ee52ebf4fbfcaff77fe663866` | 24 | 158,988 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `556ba6792d8dd1e27a3e35d52e306d74d835c1f8d35a49f698039127964dc94d`.
