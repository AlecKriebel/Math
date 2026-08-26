# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787702400`
(`2026-08-26T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `d64574e30ef3dac38c91613938a6ce29f7b07688ea791013c56a45e9af0e75c3` | `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9` | 26 | 194,327 |
| reader supplement | `7b28e0ff620b24256f4eebe61fc233dc21df8ffd7b4b552b51eb579712358bc4` | `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621` | 24 | 160,133 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `d3b3095fb009e0b10870cd8afd04e7948a16c0d2c225c1ecd0989f61beceadaf`.
