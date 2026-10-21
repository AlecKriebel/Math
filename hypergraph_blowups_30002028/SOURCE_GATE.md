# Source gate: supersaturation blow-ups in uniform hypergraphs

Checked 2026-10-21 UTC. Ordered queue row 1836; catalogue ID 30002028 / OWR-11781-001.

## Verdict

**SOURCE RECOVERED; GENUINE OPEN TARGET; NO RESOLUTION VERIFIED.** The intended problem is the hypergraph extension of Nikiforov's graph blow-up theorem. Domain defects in the catalogue are not counterexamples to this conjecture. Fresh primary evidence from May 2026 explicitly describes the hypergraph extension as open.

## Exact normalized target

Fix integers ell > r > 2 and a real c > 0. Do there exist constants gamma = gamma(c,ell,r) > 0 and n0 = n0(c,ell,r) such that, for every integer n >= n0, every r-uniform hypergraph H with |V(H)| = n and at least c n^ell copies of K_ell^(r) contains K_ell^(r)[t] for an integer t >= gamma (log n)^(1/(r-1))?

Here K_ell^(r)[t] has ell disjoint parts of size t, with every r-set meeting r different parts present. Containment is not induced. Extra host edges are irrelevant. Copy conventions only change fixed constants. The parameter c is fixed before n; gamma is not an absolute constant uniform in c, ell, r. Either logarithm base gives an equivalent existence statement; the 2012 research paper uses base 2. Taking equal parts loses nothing by trimming larger ones.

This is the clique specialization of Rödl–Schacht, Problem 2, which permits any fixed r-graph F on ell vertices and constants depending on F and c. Its research-paper formulation explicitly includes n0. The nontrivial open regime is ell > r > 2; r=2 and ell=r are known affirmative boundary cases.

## Original versus catalogue

The OWR problem-session item is Conjecture 1 on printed p.1156 (PDF page 8) in *Mini-Workshop: Hypergraph Turán Problem*, DOI [10.4171/OWR/2012/19](https://doi.org/10.4171/OWR/2012/19). The workshop ran April 8–14, 2012. Its prose omits explicit positivity/domain restrictions, n=|V(H)|, and the large-n threshold. It also calls the conclusion a graph and writes the graph-style K_{t,...,t}; the hypergraph context and the authors' research paper determine the intended r-uniform blow-up. Visual inspection confirmed these are printed features, not text-extraction errors. OWR reports a weaker known exponent 1/ell.

The catalogue repairs the graph/hypergraph noun but expands the domain to all positive ell,r. At r=1 the exponent is undefined. For ell<r the complete hypergraph has no edges, so the condition/conclusion are a degenerate packing issue, not the intended extremal question. The catalogue still fails to explicitly bind n or include n0. Its `original_statement` is a transformed catalogue sentence, not a verbatim OWR transcription. These are source/statement repairs, not mathematical disproofs. The catalogue's 2013 bibliographic date does not change the report's 2012 workshop/proposal date.

## Current literature and obstruction to an easy solution

- [Rödl–Schacht, *Complete partite subgraphs in dense hypergraphs*](https://www.math.uni-hamburg.de/home/schacht/2012/blowup.pdf), Random Structures & Algorithms 41 (2012), 557–573, DOI [10.1002/rsa.20441](https://doi.org/10.1002/rsa.20441), manuscript pp.1–2: clique-copy auxiliary hypergraphs yield exponent 1/(ell−1), not 1/(r−1). This sharper general benchmark supersedes the weaker rate printed in OWR.
- [Fox–Wigderson–Zhou, *Finding blowups one vertex at a time*](https://arxiv.org/html/2605.23301v1), arXiv:2605.23301v1, 22 May 2026, introduction: explicitly identifies the hypergraph extension as an outstanding open problem. Its new theorem improves graph-case constants; it does not resolve the present hypergraph target. The arXiv landing page inspected on the check date lists only v1. This is a preprint, not a verified journal publication.
- [Espuña, *Finding Partite Hypergraphs Efficiently*](https://arxiv.org/html/2508.10641v2), arXiv:2508.10641v2, 19 February 2026, Theorem 1.2: algorithmically finds a balanced k-partite k-uniform subgraph of a density-d host, with part size floor((log n/log(16/d))^(1/(k−1))). This concerns single-edge blow-ups. Applying it with k=ell to the auxiliary clique hypergraph retains exponent 1/(ell−1). Applying it directly with k=r only finds r parts, not the required ell parts. Neither route solves the conjecture.

The latest targeted searches and these primary sources revealed no claimed resolution. This is bounded literature verification, not proof that no later result exists. No explicit general gamma(c,ell,r) for the target exponent can be supplied without solving the open problem.

## Evidence handling

SOURCE_METADATA.json records public source titles, URLs, byte counts, SHA-256 hashes, retrieval/inspection history, and stated manuscript status. This package contains authored analysis and bibliographic metadata only. No downloaded source documents, rendered pages, extracted source text, or catalogue records are bundled.
