# Source and prior-work audit

Checked 5–6 October 2026 UTC. No full resolution located in this bounded search.

## Exact target

- John M. Sullivan, Problem 5 in *Open Problems in Discrete Differential Geometry*, collected by Günter Rote, in Oberwolfach Report 12/2006, printed p. 693, PDF page index 40. DOI https://doi.org/10.4171/owr/2006/12 . Official PDF: https://ems.press/content/serial-article-files/46044 . The actual page was text-inspected and visually inspected. It presents both the weak 5/6 and stronger TCP questions; the latter restricts degree-six edges. The text does not explicitly settle the category qualifiers discussed in the note.
- Target website: https://www.unsolvedmath.com/problems/30000433 . A direct web open failed. Identity and full-record review were instead checked against the supplied dataset and the official primary report. This access limit is retained.
- The complete [record, reports.get(problem_number,{})] pair was read and serialized by Python json.dumps(..., sort_keys=True), with default spacing and escaping. It is 3,552 UTF-8 bytes, SHA-256 48336d46884d5c1b7cb087f2ca3c3a5f5c2426fd761e15572df88dc93e303f94, agreeing with the catalog review hash. The report is absent and was represented by {}, not null. No corpus or original record text is included in this package.

## Directly relevant published or primary material

1. N. Brady, J. McCammond, J. Meier, *Bounding edge degrees in triangulated 3-manifolds*, Proc. Amer. Math. Soc. 132 (2004), 291–298. DOI https://doi.org/10.1090/S0002-9939-03-06981-8 . Author PDF https://math.ou.edu/~nbrady/papers/edgedegrees.pdf . Inspected Theorem 1.2, Definition 1.1, and Sections 2–5. The actual theorem has closed orientable hypotheses and allows 4,5,6; it does not remove degree four. Quotient constructions must not silently be treated as strict simplicial certificates.
2. M. Elder, J. McCammond, J. Meier, *Combinatorial conditions that imply word-hyperbolicity for 3-manifolds*, Topology 42 (2003), 1241–1259. DOI https://doi.org/10.1016/S0040-9383(02)00100-3 . Author PDF https://web.math.ucsb.edu/~mccammon/papers/thurston.pdf . Definition 1.1 and Theorem 1.2 inspected. The extra condition is at most one degree-five edge per triangle, so this is a distinct conditional theorem, not a solution of Sullivan's existence question.
3. F. H. Lutz, with T. Sulanke and J. M. Sullivan, *Periodic foams and simplicial manifolds with small valence*, OWR 4/2007, pp. 228–230. Official PDF https://ems.press/content/serial-article-files/46090 . Printed p. 229 inspected. It explicitly treats closed TCP triangulations, reiterates the universal question, and records examples including products of surfaces with S1 and certain spherical manifolds. Its p. 230 reference identifies the original 2006 Problem 5.
4. F. Frick, *Combinatorial restrictions on cell complexes*, 2015 dissertation, https://d-nb.info/1076082246/34 . Sections 3.6–3.7 inspected through the public PDF. Theorems 3.25 and 3.32–3.36 supply nearby bounded-valence and geometric results, not universal 5/6 or TCP existence. No proof of the entire dissertation is claimed here.
5. K. Huszár, C. Maria, *On Sparse Representations of 3-Manifolds*, SoCG2026, DOI https://doi.org/10.4230/LIPIcs.SoCG.2026.58 . Full official HTML https://drops.dagstuhl.de/storage/00lipics/lipics-vol367-socg2026/html/LIPIcs.SoCG.2026.58/LIPIcs.SoCG.2026.58.html . Introduction, Theorem 2 and Section 2.2 inspected. The new algorithm attains a maximum-valence-nine bound while controlling treewidth, and uses generalized tetrahedron face pairings. It does not supply the present target.
6. John M. Sullivan's primary project page, *Restricting valence for polyhedral surfaces and manifolds*, https://www3.math.tu-berlin.de/geometrie/ps/s.shtml , explicitly identifies 5/6 sufficiency as a research question. This older project page is contextual evidence only, not an authoritative assertion of current openness.

Additional discovery searches covered the exact problem title, “TCP triangulations,” “5/6-triangulation,” the universal 3-manifold wording, and date-qualified 2024–2026 TCP/Sullivan queries. Search-engine crawl dates were not confused with publication dates. No search hit was substituted for inspection of the primary statements used above.

## Prior user/repository work

Read-only AlecKriebel/Math searches for exact ID 30000433 and problem number OWR-1194-002 in code, PRs and issues, and the exact ID in commits, returned no direct records. Broader “triangulations” PR and “edge degree” code searches revealed no target-specific substantive attempt. The catalog itself records desk review and zero approaches. This is sufficient to proceed, not proof that no inaccessible or unindexed prior work exists. No remote state was changed.

## Attribution and publication status

The note's elementary lemmas and finite certificates were independently authored here, but their novelty is unestablished. The 600-cell and the admitted manifold types are classical. The source package contains only authored mathematical analysis, code, results, and public verification metadata. It does not contain copied source PDFs, source-page screenshots, extracted source text, dataset records, or private coordination material.
