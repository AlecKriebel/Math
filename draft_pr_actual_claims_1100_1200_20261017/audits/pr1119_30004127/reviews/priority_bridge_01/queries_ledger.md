# Actual fresh-web query and retrieval ledger

Session date: 2026-10-17 UTC. Queries below are the actual strings sent to `web.run`, in chronological batches. Search output was used for discovery; mathematical conclusions rely on the primary documents identified in REPORT.md. No search count is treated as a proof of priority or absence. There were 24 search strings in six batches; this was a focused follow-through review, not an exhaustive coverage claim.

## Search batch 1

1. `"Alon" "Shapira" "triangle-freeness" "two-sided" 2004`
2. `"Alon" "Kaufman" "Krivelevich" "Ron" "2008" triangle testing`
3. `"Testing Graphs in Vertex-Distribution-Free Models" Goldreich`
4. `"2603.22702"`

Result use: identified Goldreich author page/R3 and AKKR08 primary author manuscript; Fei arXiv identification.

## Search batch 2

5. `Alon Shapira 2004 "two-sided" triangle testing`
6. `Alon Shapira "Testing subgraphs" 2004 lower bound two sided`
7. `"vertex-distribution" "polynomial" complexity Gishboliner Shapira`
8. `"Testing Properties of Edge Distributions" Fei`

Result use: identified Alon–Shapira JCSS paper, Fei arXiv, and AKKR source referring to AS04's dense two-sided result.

## Search batch 3

9. `"Testing subgraphs in directed graphs" pdf Alon Shapira`
10. `"almost" "colorability" "easily testable" graphs`
11. `"hereditary" "easily testable" "intersection" graph property`
12. `"vertex-distribution-free" "complexity" separation`

Result use: retrieved AS04 author manuscript `testdig5.pdf`; identified Gishboliner–Shapira polynomial-removal manuscript `easy.pdf` as background. No bridge or prior full separation identified from these returned sources.

## Search batch 4

13. `graph property testing "vertex deletion" "polynomial" hereditary`
14. `"testing" "apex" "3-colorable" distribution graph`
15. `"testing" "hereditary" "quantitative" "closure" graph 2025 2026`
16. `"Testing Graphs against an Unknown Distribution" separation complexity`

Result use: primary GS author PDF and ECCC/OWR records. Vertex-deletion complexity results returned were computational recognition/parameterization results, not the needed dense/VDF testing bridge.

## Search batch 5

17. `"testdig5" "Theorem 2"`
18. `"Testing Subgraphs in Directed Graphs" "5.2"`
19. `"Testing Subgraphs in Directed Graphs" "two sided"`
20. `"hereditary testing" "closure" polynomial quantitative`

Result use: AS04 primary PDF and older conference version for navigation; identified recent quantitative-container paper for direct hypothesis check.

## Search batch 6

21. `"A quantitative container characterization of one-sided testability"`
22. `"A quantitative container characterization" arxiv`
23. `"quantitative closure" "partition properties" testability`
24. `"hereditary" "vertex-distribution-free" "polynomial" 2026`

Result use: identified and retrieved arXiv:2608.01523v1. Subsequent work focused on its direct hypotheses and the AS04/Gol19/AKKR08/Fei models; no further broad search was attempted.

## Fresh web opens and finds

Opened the primary Fei v2 HTML, GS v5 abstract page, Alon's publication list, and AKKR author PDF. Attempted finds in these pages for theorem/citation navigation; the web parser returned some internal errors for PDFs. The local primary PDFs were then read directly. Opened the AS04 author PDF through the browser tool; parser failed, so the privately retrieved PDF was rendered and OCRed, with critical pages visually inspected. Opened AS04 ScienceDirect publisher page: direct open returned HTTP 403, although its indexed publisher abstract was available in search. Opened the container v1 arXiv abstract and GS Springer journal page. The latter exposed a subscription preview and bibliographic metadata, not the full body.

Specific find terms used: `Testing subgraphs in directed`, `Theorem 1`, `parity`, `Proposition 7.1`, `two-sided`, `queries`. These were navigation requests, not additional independent searches.

## Local primary-source retrievals

Exact retrieval URLs, timestamps, response types, byte counts, and SHA256 hashes are in `source_versions.json`. Full source files and derived text/OCR live only in ignored `sources/private/` or `tmp/`.

- GS arXiv v5 PDF: `https://arxiv.org/pdf/1905.09903v5`
- Goldreich R3 PDF: `https://www.wisdom.weizmann.ac.il/~oded/R3/vdf.pdf`
- AKKR author PDF: `https://www.math.tau.ac.il/~krivelev/testtria.pdf`
- Fei v2 PDF: `https://arxiv.org/pdf/2603.22702v2`
- AS04 author PDF: `https://www.cs.tau.ac.il/~nogaa/PDFS/testdig5.pdf`
- Alon 2002 author PDF: `https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/AlonTestGraphs.pdf`
- Original OWR PDF: `https://ems.press/content/serial-article-files/46798`
- GS journal landing page: `https://link.springer.com/article/10.1007/s11856-021-2228-8`
- GS journal PDF attempt: `https://link.springer.com/content/pdf/10.1007/s11856-021-2228-8.pdf` — response was HTML preview, not PDF.
- GS polynomial-removal author manuscript: `https://www.math.tau.ac.il/~asafico/easy.pdf`
- Container v1 PDF: `https://arxiv.org/pdf/2608.01523v1`

Local reading concentrated on AS04 definitions p.2, Theorem 4(ii) p.4, and §7 pp.23–26; Goldreich Propositions 2.2, 2.11 and Theorem 2.3; AKKR §6 Theorem 3; GS v5 §5.2–5.3; Fei v2 §1 and §7.1/§8; and container v1 §§5–6. The old Alon 2002 and GS `easy.pdf` were contextual rather than necessary black boxes in the final deduction.
