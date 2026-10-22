# Source gate: maximizing initial odd ears

Checked 20 October 2026. Assigned queue row 1828; ID 30002726; OWR-13353-012.

## Verdict

**Source recovered; partially solved, with the general complexity question unresolved in the verified literature found.** No general polynomial-time algorithm or NP-hardness result for the exact target was located. This is a bounded literature finding, not proof that no later resolution exists.

This record describes the literature assessment before the authored proof in
NP_COMPLETENESS_PROOF.md. Its unresolved status concerns the verified prior
literature, not the separately audited result in this package.

## Source identity

András Sebő, “Problems about uniform covers, with tours and detours,” pp. 2912–2915, in *Combinatorial Optimization*, Oberwolfach Reports 11 (2014), no. 4, pp. 2873–2932, DOI 10.4171/OWR/2014/51. Question 4 appears on printed p. 2914, in the discussion of joint work with Yohann Benchetrit. It asks for the computational complexity of β, the maximum number of starting odd ears. Reference [3] names their then-in-preparation work on matching-polytope complexity. The report does not give a complete standalone ear convention; the subsequent joint paper supplies it. [Original report, p. 2914](https://ems.press/content/serial-article-files/46541).

The report volume is dated 2014, while EMS gives publication on 29 October 2015. These dates do not conflict. [EMS record](https://ems.press/journals/owr/articles/13353).

## Exact target and conventions

The target input is a finite undirected, **2-vertex-connected** graph with at least three vertices. The subsequent paper permits parallel edges but excludes loops; a restriction to simple graphs must be labeled as such. [Benchetrit–Sebő, introduction and §1.1](https://arxiv.org/html/1509.05586v1).

Use an **open** ear-decomposition D=(P₀,P₁,…,Pᵣ): P₀ is a circuit, and every later Pᵢ is a new path whose two distinct endpoints lie in the preceding union, with all internal vertices new. The ears partition the edge set. The initial circuit counts as an ear; a one-edge path also counts. Oddness means an odd number of edges. Closed ears attached at a single vertex are not allowed. [Benchetrit’s author exposition, definitions and Theorem 2](https://matroidunion.org/?p=1769).

In explicit notation, set b(D)=max{t : P₀,…,Pₜ₋₁ all have odd length}, permitting t=0. Then β(G)=max_D b(D). The objective stops at the first even ear; later odd ears do not contribute.

Equivalently, β(G) is the largest value |E(H)|−|V(H)|+1 over 2-connected factor-critical subgraphs H of G. Here factor-critical means that deleting any one vertex leaves a perfect matching. H is not required to be spanning or induced. If no such H exists, β(G)=0; this is precisely the bipartite case. [Benchetrit’s author exposition, Definition 3](https://matroidunion.org/?p=1769).

## Verified partial results and remaining question

Benchetrit–Sebő’s 2015 preprint gives elementary polynomial-time recognition of β≤1. Its Theorem 1.8 states fixed-parameter tractability for graph β; the threshold k is the parameter, not an unrestricted input silently treated as constant. Section 3.1, Question 3.3 still asks whether β can be computed in polynomial time; the threshold problem β(G)≥k lies in NP. The inspected arXiv record lists only v1, submitted 18 September 2015. These are established prior claims, not results of this gate. [Paper, Theorem 1.8 and §3.1](https://arxiv.org/html/1509.05586v1), [version record](https://arxiv.org/abs/1509.05586).

The FPT statement concerns graphs. Do not transfer it to arbitrary binary-matroid inputs merely because the same paper extends the β≤1 method to binary matroids.

## Variant controls

- **All odd ears is a different objective.** Section 3.2 distinguishes β from the maximum total number of odd ears, which is polynomially computable via Frank’s results. Proposition 3.4 supplies graphs with β=2 and unbounded total optimum. [Benchetrit–Sebő, §3.2](https://arxiv.org/html/1509.05586v1).
- **Length restrictions and closed ears are different problems.** Havet–Nisse’s 2019 paper permits a cycle attached at one vertex and works with 2-edge-connected graphs. Its NP-completeness results for prescribed/forbidden ear lengths or all-even ears do not resolve the present open-prefix question. [Constrained ear decompositions, §1.1 and §5](https://dmtcs.episciences.org/articles/5626).
- **Recent matroid hardness is not β hardness.** Bai–Bérczi–Nalam’s August 2026 preprint studies maximum joins and minimum total even lobes. Its cographic-matroid NP-hardness theorem addresses the join objective, not the maximum initial odd-ear prefix in a graph. Its introduction, relevant definitions, and conclusion were checked. [2026 preprint](https://arxiv.org/html/2608.01059v1).

## Verification boundaries

Exactly one matching problem record and no matching research-result record were found in the recovered local corpus. Both datasets were freshly hashed, not freshly fetched upstream. Their dated partial-solution assessment agrees with the independently inspected sources. Public hashes and byte counts are recorded separately in CORPUS_VERIFICATION.json; source retrieval and inspection metadata are in SOURCE_METADATA.json. Raw extracts, PDFs, extracted text, and rendered pages remain private.

The original question page and the later paper’s definition/status pages were visually inspected. Searches covered the exact title, starting/initial odd ears, β, factor-critical subgraphs, polynomial complexity, NP-hardness, and later work. The checked author webpage dates its last update to January 2019, so it is not evidence of a comprehensive current publication list. No verified journal publication or newer exact-target resolution was found. [Author page](https://pagesperso.g-scop.grenoble-inp.fr/~seboa/).

**Scope control:** the source question is the 2-vertex-connected, open-ear,
initial-prefix objective, with the initial circuit counted. Total-parity
optimization, fixed-k tractability, matroid-join hardness, and closed-ear
theorems do not resolve this question. The original literature status above
is preserved separately from the authored Set Cover reduction and its audit.
