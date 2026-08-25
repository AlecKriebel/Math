# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH=1787529600`
(`2026-08-24T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `ca6dd8d750768b0c47121c8bd60c5c9c3223af194139f5f578cb8bbf5fd5c3f1` | `2c4433d53c33c337d4ed028c2843cf0b5631263d7bf4a0a42106727985daa3a8` | 26 | 194,316 |
| reader supplement | `57275e1e5e1058306607a98583ac31e98383952ef2284515fea01f1c47ce95bd` | `9b10797d7503e6940d80a95bc90302b3b32a9ea34cb9f63a54bee3f12f3c06e1` | 24 | 158,872 |

All 50 rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `08967e35951d391f1a3db9e811856d61c263f4b5374944acd52a54f4e213a721`.
