# Primary source and reading-location ledger

Every downloaded whole text, extracted text, HTML response and raw discovery payload is in ignored `private/`. SOURCE_PROVENANCE.json contains retrieval timestamps, exact source URLs, SHA-256 digests and paths. Its metadata can be shared; the downloaded bodies should not be staged or published. Page numbers below are one-based PDF pages unless explicitly printed pages. Line numbers refer to the corresponding private `.txt` file using Python `splitlines()`.

| ID / primary source | Retrieved artifact | Reading location and scope |
|---|---|---|
| OWR 09/2013, DOI 10.4171/OWR/2013/09; https://ems.press/content/serial-article-files/46440 | `private/owr2013.pdf` | Whole Podolskij contribution, printed 491–493 = PDF 9–11; text 250–390. Target and display at printed 492/PDF 10, text 323–344. |
| Podolskij survey, arXiv 1405.1531v1, 7 May 2014 | `private/survey_arxiv_v1.pdf` | Section 4.2, especially Theorem 4.8(i), PDF 30, text 1666–1680; reference [17] PDF 34, text 1908–1909. Earlier theorem announcement, not a first-priority certification. |
| Podolskij survey, Thiele 2014 report | `private/survey2014.pdf` | Section 4.2, text 1551–1760, especially Theorem 4.7, PDF 31–32; reference [17] text 1837–1838. Numbering differs from arXiv v1. |
| Basse-O'Connor–Lachièze-Rey–Podolskij, arXiv 1506.06679v1 | `private/aop_arxiv_v1.pdf` | Introduction/model, Assumption(A), Theorem 1.1(i), text 61–201, PDF 2–4. Full PDF obtained. Identical hash for unversioned URL at retrieval. |
| Basse-O'Connor–Heinrich–Podolskij, arXiv 1604.02307v1 | `private/bernoulli_arxiv_v1.pdf` | Model and assumptions, PDF 2–5; Theorem 1.2(i) text 262–273, PDF 5; obsolete J1 definition text 245–250. Full PDF obtained. |
| Same, arXiv 1604.02307v2 | `private/bernoulli_arxiv_v2.pdf` | Model text 71–86/PDF 2; (A) text 131–142/PDF 3; (B1) text 224–236/PDF 5; Theorem 1.2 text 261–294/PDF 5–6; Remark 1.4 text 300–305/PDF 6; finite-dimensional proof/stability discussion text 740–866. Full controlling PDF obtained. |
| Same DOI 10.3150/17-BEJ956 and AOP DOI 10.1214/16-AOP1170 | `private/*_crossref.json`; `private/*_abs.html` | Primary submission histories and publisher-deposited dates/pages checked. IMS indexed snippets corroborate pagination. Final-journal direct PDFs not obtained:403 or HTML; no substantive final-only comparison asserted. |
| Ljungdahl–Podolskij2018, DOI 10.15559/18-VMSTA111 | `private/singularities2018.pdf` | Journal model text 53–68/PDF 2; Theorem 2.2 text 277–307/PDF 6. Primary journal PDF obtained. |
| Basse-O'Connor–Heinrich–Podolskij2019, arXiv 1806.10352 | `private/functionals2019.pdf` | Model/introduction and (A), text 40–195; Theorem 2.1 text 235–275/PDF 5–6. Full PDF obtained; model/theorem coverage inspected. |
| Basse-O'Connor–Pilipauskaitė–Podolskij2021, arXiv 2008.01412 | `private/random_fields2021.pdf` | Section 2.2 text 129–168/PDF 3, Theorem 3.1 text 318–334/PDF 6, Theorem 3.2 text 369–385/PDF 7. Full PDF obtained; driving-measure and theorem restrictions inspected. |
| Mies–Podolskij2023, arXiv 2208.07453 | `private/mixed2023.pdf` | Equation(1), text 55–70/PDF 1–2; Section 2 multiscale setup text 212 onward/PDF 5; Theorem 2.2 PDF 7. Full PDF obtained; model and main-theorem sections inspected. |
| Benth–Veraart, arXiv 2410.00566v2; DOI 10.3150/25-BEJ1902 | `private/survey2026_current.pdf`; primary abs/Crossref metadata | Section 2.3 text 497–516/PDF 10; bibliography text 1237–1242. Full current preprint obtained; primary metadata confirms Bernoulli 32(1),24–48, Feb2026. |
| Barndorff-Nielsen–Benth–Veraart2018, DOI 10.1007/978-3-319-94129-5_3 | Publisher chapter landing page; failed downloaded PDF stored as HTML | Only abstract, references, first-online date2Nov2018 and pp 99–114 read. Full chapter unavailable; no theorem-coverage assertion. |

Safe source-specific paraphrases are in REPORT.md and kept concise; mathematical reductions there are explicitly labelled as this audit's deductions. No copied whole text or long quote is in an authored report. No individual was contacted.
