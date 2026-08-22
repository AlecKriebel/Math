# PDF build and visual-inspection report

Both submission documents were rebuilt from the final sources with Tectonic
0.16.9 on 22 August 2026.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `480581cec37b9a90e5e96eb1528e6fca6a4bbfafaefd43d9d41357f8e67ac999` | `204537cef40f155d1fd418c4b17cd7b8cd5e432773b0de037a829690f8ba77e1` | 26 | 192,757 |
| reader supplement | `1989d763d51004f351e42279ccf82374d3c0afa2b4ea96bcfa3026075e6b3ce8` | `19865ffb832abf5757d5fb5d534e1888d22f3b11ea7ea035e451203359ca275a` | 24 | 158,249 |

All 50 rendered pages were inspected, including the new directed-core and
repair proof, the genericity and reconstruction insertions, and the dense formula, transport,
crosswalk, hash, and replay tables. No clipping or layout defect was found.
The logs contain no overfull boxes, undefined references, undefined citations,
fatal errors, or hyperref PDF-string warnings. `pdffonts` confirms that every
font is embedded. A clean-source build with `compression_tables.tex` omitted
failed at the unconditional input, as required. The machine-readable record is
`PDF_BUILD_REPORT.json`.
