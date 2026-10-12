# Source and hypothesis ledger

Research date: 12 October 2026 UTC. This is a bounded literature check, not an exhaustive proof of current openness or priority. The mathematical partial proofs are authored in full. Copied third-party source documents are not distributed with this prose edition.

## 1. Intended problem and source conventions

- Open Problem Garden, [List colorings of edge-critical graphs](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs), posted 12 June 2007. The exact maximum-degree criticality and intended nonconstant-list condition were inspected on the live page and downloaded as HTML. The result concerns proper edge coloring of finite simple graphs, not star edge coloring, DP coloring, list-edge-criticality with a different quantifier, or flow-criticality.
- Mohar, [original July 2001 problem](https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html). The homepage's literal “if and only if all lists are equal” is reversed. Constant Δ-lists fail by the source's own criticality definition. The OPG formulation and the later line-graph formulation confirm the intended assertion. This wording error is not a substantive counterexample and is never claimed as one.
- Kaul–Mudrock, [arXiv:1805.02147v2](https://arxiv.org/pdf/1805.02147v2), 7 August 2018, actual 27-page PDF. Definitions and Conjecture 6, printed page 11, were directly inspected. Strong (Δ+1)-chromatic-choosability of the line graph is the relevant list-rigidity condition. Their compressed defining sentence does not separately repeat non-Δ-edge-colorability; our operational hypotheses do so explicitly, avoiding that literal omission.

## 2. Publication identity update

Kaul–Mudrock's paper was published in *Journal of Combinatorics* 12(3) (2021), 479–514, [DOI 10.4310/JOC.2021.v12.n3.a4](https://doi.org/10.4310/JOC.2021.v12.n3.a4). The official publisher PDF's indexed first page directly displays this identity, and its indexed printed page 492 retains the discussion leading to Mohar's conjecture. The DOI/official PDF direct web open returned an internal error, and a direct byte download returned HTTP 403; no complete local capture or full published-version proof inspection is claimed. The proof-source inspection remains the actual arXiv v2 PDF. Search-engine “published six months ago” metadata for the PDF is not used as the publication year.

Official indexed PDF URL: https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1805864015869980674-1805864015869980674-389086e52638ea4b165dd00046cf111e.pdf

## 3. Relevant current development, not a resolution

Bernshteyn–Kaul–Mudrock–Sharma, *On Strongly and Robustly Critical Graphs*, [arXiv:2408.04538v2](https://arxiv.org/pdf/2408.04538v2), 22 January 2025, 15 pages; published [Journal of Graph Theory 112 (2026), 469–483](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70033), first published 16 April 2026, August 2026 issue. The actual arXiv PDF and the publisher's full HTML were available. Definitions, Theorem 1.6 and its proof framework were inspected; a full proof audit is not claimed.

Theorem 1.6 makes a vertex-critical graph strongly chromatic-choosable after joining it to a clique of size at least three times its number of edges. This additional join is essential to the theorem as stated. It does not prove that the original line graph is strongly chromatic-choosable, so it does not resolve the present target. The stronger robust-DP results are likewise not silently transferred back to the original graph.

## 4. Older subcubic theorem, correctly delimited

Juvan–Mohar–Škrekovski, *On list edge-colorings of subcubic graphs*, *Discrete Mathematics* 187 (1998), 137–149, [author-hosted published PDF](https://www.sfu.ca/~mohar/Reprints/1998/BM98_DM187_Juvan_ListEdgeColorings.pdf), [DOI](https://doi.org/10.1016/S0012-365X(97)00230-6). The actual 13-page PDF was inspected for its hypotheses, introductory theorem, and cycle/halfedge reduction statements. Its mixed-list theorem uses lists of size three only on a subgraph of maximum degree at most two and lists of size four on the other edges. It therefore does not settle arbitrary three-element lists on the full subcubic edge-critical graph. No full independent audit of that published proof was done.

## 5. Search boundary and credit

Queries covered the exact problem title; Mohar plus edge-critical/list/nonconstant; strong chromatic-choosability and current 2024–2026 work; amenable critical graphs; subcubic list edge coloring; and near-constant/star-supported exceptions. The search identified the current join theorem and the older mixed-list subcubic theorem above, but no primary full resolution of this precise problem. Search results about strong edge coloring, unrelated list-critical definitions, surface colorings, and critical snarks were not counted as resolutions.

No paper found in this bounded pass is claimed to establish the particular near-constant statements authored here. This absence is not a priority claim. The subdivided-K4 example in FINITE_PALETTE.md is already covered by Kaul–Mudrock Lemma 3. That attribution is not a claim that the structural theorems here are novel.

## 6. Source access and distribution limits

The bounded source review used five successful source captures. Text extracted from a PDF is not a byte-identical substitute for the PDF. Only authored discussion, source titles, public URLs, and the inspection scope described above are included here. Copied third-party HTML, PDFs, and extracted source text are not distributed. No excluded capture filename, file digest, or byte count is supplied.
