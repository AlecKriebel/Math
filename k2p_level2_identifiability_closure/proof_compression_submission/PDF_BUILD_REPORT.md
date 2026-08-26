# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787702400`
(`2026-08-26T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `d64574e30ef3dac38c91613938a6ce29f7b07688ea791013c56a45e9af0e75c3` | `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9` | 26 | 194,327 |
| reader supplement | `947380b08543c285cf4866c4864855cea2d020e072853b53ae67e53e4b6e9f25` | `0ef0bc101af3c2edaa19c03dac1a78fcade37509f157cd65e548c70b279aa405` | 24 | 160,132 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `06045710af643a1c2615d8a11a10a889ce9c518a7b626c7558bd1980e0b4109e`.
