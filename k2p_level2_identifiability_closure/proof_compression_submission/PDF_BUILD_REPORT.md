# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787788800`
(`2026-08-27T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `20387611077cf1bfb128456e523b34f46c5a98537c6bbf6ddb5436911f8c9dec` | `186522a14070fc872e67e75736804fa14621104803225f73615d7f76d09f9a11` | 26 | 194,515 |
| reader supplement | `adccd175bfff5707d0d4d938287040636e40bd4071e64716292a5c03b003b631` | `5ea090740046fbafa0c10b9397e610be8584d49dbf8cd560d190e24420e344f2` | 24 | 160,293 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `a3c6b81b053be86811d56bb763a8a139c4d5e03cdf78a06da36887b2aa982d46`.
