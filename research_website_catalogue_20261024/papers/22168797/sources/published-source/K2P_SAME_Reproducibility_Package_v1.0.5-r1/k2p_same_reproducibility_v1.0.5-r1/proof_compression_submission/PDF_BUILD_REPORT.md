# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787788800`
(`2026-08-27T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `43278b63cc6d123fc8ec970178e886e9a57d02c879a2ff748887572f29eeb27d` | `e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4` | 26 | 194,542 |
| reader supplement | `d5f79a95a7ec0aff2ce4e8e3f818dcf930435dcde2265ed23dc6bacede1fea33` | `0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d` | 24 | 160,762 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `4608132ef5448b5221edae63e268d6cf6a20ff5a7eb57ca012ecb91087fc5ce4`.
