# Source-first checkpoint (sealed before candidate access)

Date: 2026-10-15 04:15 UTC. Reviewer: oracle01. PR 570, target 30006605. Estimated completion of assigned oracle/source audit: 35%.

No candidate proof, author controls, prior candidate audit, or sibling audit has been read at this checkpoint. Only the primary sources below, exact target catalog metadata, AGENTS.md, snapshot filenames/hashes, and related-target group metadata have been read. This checkpoint records an independent reconstruction, not a certificate of the candidate.

## Exact source target and boundaries

The selected record identifies Ducoffe, *Radius functions in median graphs*, OWR 8/2026, pp. 504-507, DOI 10.4171/OWR/2026/8, Open Problem 1 on p. 505. The question asks for an almost linear algorithm for multiplicatively vertex-weighted centers in bounded cube dimension. With the definitions on p. 504, the objective is

r_pi(v) = max_{u in supp(pi)} pi(u) d_G(u,v),   pi: V -> R_{>=0},

and the answer is a vertex minimizing r_pi. The opening definition allows infinite graphs with finitely supported profiles. The computational question immediately follows n-vertex time bounds; finite n-vertex adjacency input is its operative algorithmic interpretation. Infinite graphs need an input representation and are not resolved by an n-vertex algorithm. Cube dimension means the largest induced hypercube dimension, not tree dimension or a supplied product-of-trees embedding. The target does not promise integral, positive, bounded-ratio, or few distinct profile values. Zero values and empty support require conventions/handling. Edges have unit length. The separate edge-weight question on p. 506 is outside this target.

Success requires an exact minimizer for every finite connected median graph with nonnegative profile values under an explicit arithmetic/input model and an almost linear n dependence for fixed dimension. Real weights require exact comparisons or a rational bit-cost statement; arbitrary unrepresented reals cannot be finite binary input. A result for all finite median graphs would strengthen the dimension restriction. An additive-weight center is a different objective.

## Imported primary theorem and exact interface

Berge-Ducoffe-Habib, *Quasilinear-time eccentricities computation, and more, on median graphs*, arXiv:2410.10235v1 (2024-10-14), Theorem 1 (pp. 3 and 23), provides a combinatorial O(n log^4 n) algorithm with input a finite connected simple undirected median graph and vertex map omega:V -> N, N explicitly including zero. It returns, for EVERY x,

E_omega(x) = max_{y in V} [d_G(x,y) + omega(y)].

Thus the weight belongs to the arrival vertex and is additive; it is not an edge weight, a multiplicative profile, or a two-sided additive metric. No nonnegativity violation, arbitrary signed offset, fractional offset, or induced nonmedian subgraph is allowed merely from the theorem statement. No dimension bound or embedding is an input promise. Theorem 2 is a distinct distance oracle and is not needed to compute these labels.

The paper's graph model is stated in section 2.1, pp. 4-6. It does not state a word size/weight-bit parameter in Theorem 1. Arbitrarily long integer inputs/outputs cannot have literal O(n log^4 n) binary bit cost independent of their lengths. A reduction using omega in [0,O(n)] would eliminate that ambiguity for the imported calls. The graph must be supplied explicitly (ordinary adjacency access suffices); all-pairs distances as an extra input would destroy the desired end-to-end time claim.

## Read primary proof dependency map

Read the introduction and full sections 2-4 (pp. 1-24), including the full Theorem 1 proof and Algorithm 1. These are the complete proof-bearing sections for the weighted-eccentricity import; section 5 proves the separate distance-oracle result. The explicit structural imports are convex=gated for median graphs, gated fibers/intersections, linear-time Theta classes and halfspace sizes/median set, signature/path characterization, pairwise orthogonal families and ladder sets. These are relied-on classical/cited theorems; their original historical proofs have not been rederived or formalized here.

The algorithm recurses on gated halfspaces for a balanced Theta cut, merging using the identity

E_G(x) = max(E_H(x), d(x,g_{H'}(x)) + E_{H'}(g_{H'}(x))).

This is checkable from gatedness and additive arrival weights. In the no-balanced-cut case, an unweighted median vertex v0 is used. A weighted farthest vertex u_max determines a ladder of pairwise orthogonal cuts. Vertices whose ladder misses this ladder have eccentricity d(x,v0)+E(v0), by a shortest-path separation lemma. The remaining vertices split into gated slices. Each slice gets two recursive calls, original weights and fiber-maximum arrival weights; max-plus gate identities assemble the outputs. Thus weight-dependent operations are comparison, maximum and addition of unweighted distances; the graph's structural operations are independent of weights. A dominance case u_max=v0 avoids slicing.

The correct transfer question is whether multiplicative radius feasibility can be converted into one or a few such additive calls with nonnegative integer omega and bounded magnitude, and whether exact optimization avoids n^2 materialized products or a weight-dependent number of searches. Calling this import directly on pi without a reduction would be invalid.

## Independent issue in the imported v1 presentation

The paper defines bare log as natural logarithm (p. 4). It correctly states d <= log_2 n (p. 7), but its p. 18 cardinality discussion and p. 24 recursive-volume estimate use ell <= log n with f(n)=2 log n. That intermediate inequality is false with the stated convention. This is a source proof-presentation issue, not yet a counterexample to Theorem 1. A local constant/base repair appears available: choose the balance threshold f(n)=2 log_2 n throughout sections 3-4, equivalently (2/ln 2) ln n. Then 2 sum |S_i| <= n, while the depth bound remains O(log^2 n) using Lemma 16 with lambda=2/ln 2. All gating and weight identities are threshold-independent. This repair needs to be stated explicitly if the source's complete proof is promoted as independently verified; it should not be silently treated as the literal v1 algorithm.

## Primary provenance and review extent

- Official OWR landing: https://publications.mfo.de/handle/mfo/4442 ; report https://publications.mfo.de/bitstream/handle/mfo/4442/OWR_2026_08.pdf?isAllowed=y&sequence=1 . Full Ducoffe contribution read including references; PDF pages 18-21 visually inspected, printed pp. 504-507. PDF SHA256: 92d33ad86e2ba37d8df828c147e73b40e32206e7090cc6d74c34e5eba47f7c51.
- BDH v1 original: https://arxiv.org/pdf/2410.10235v1 ; PDF SHA256: af1ea4ea9e338c466892289c99bda9048458e41a490b1bbc915da273b31f60c38. Full relevant proof sections read as above; pp. 23-24 visually checked to confirm the log issue is present in the original, not extraction damage.
- Source PDF/OCR/render copies are private local cache only, excluded from public authored seal.
- review_v2/related_target_groups.json has no group containing 30006605. No other target was investigated. No communication with outside individuals, repository mutations, branch/index operations, or source publication occurred.

Next: hash the candidate original, read the entire candidate proof, and adversarially match every oracle call and optimization claim to this reconstructed interface.
