# PDF build and visual-inspection report

Both submission documents were rebuilt from the final sources with Tectonic
0.16.9 on 22 August 2026.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `4647e050b148a4fd03eae4242347dee3d5387df19947c64bbd795dc08eb46c02` | `e30ea98ccde1756bb98ad9ce500c83a64c87d5d9985bc06b432f6d9fc79df064` | 24 | 186,039 |
| reader supplement | `1072c5edc677ac2dcec81c1ce57fdfc21c76cccc9fb133d09ab48550b8709d79` | `0a0c55e16b5f7298c9749912a3901d1a0a1323578ab25ef7db13c06e0b912131` | 24 | 158,121 |

All 48 rendered pages were inspected, including the dense formula, transport,
crosswalk, hash, and replay tables. No clipping or layout defect was found.
The logs contain no overfull boxes, undefined references, undefined citations,
fatal errors, or hyperref PDF-string warnings. `pdffonts` confirms that every
font is embedded. The machine-readable record is `PDF_BUILD_REPORT.json`.
