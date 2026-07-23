# Actionable literature record

Retrieval date: **2026-07-23**. Links below are primary papers, formalization
repositories, or maintained author data/survey pages.

## Current \(R(5,5)\) bounds

- The maintained revision 18 of Radziszowski's
  [Small Ramsey Numbers](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf)
  (2026-04-24) reports lower bound 43 and upper bound 46.
- Exoo's 1989 lower-bound construction is
  [A lower bound for \(R(5,5)\)](https://doi.org/10.1002/jgt.3190130113).
  McKay's established [Ramsey graph data
  page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html) publishes 328
  42-vertex representatives, with their complements giving 656 known graphs.
- Angeltveit and McKay's
  [\(R(5,5)\leq46\)](https://doi.org/10.1002/jgt.70029), also
  [arXiv:2409.15709](https://arxiv.org/abs/2409.15709), is the current upper
  bound. Both authors report independent implementations of every computation.

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** no credible primary-source bound
improvement was found by the retrieval date. A public unreviewed claim of a
43-vertex UNSAT proof was not adopted: the maintained survey still reports
43–46, and its proof package was not checked here.

## Angeltveit–McKay: upper-bound structure

Actionable details:

- \(R(4,5)=25\) gives degree 21–24 in a hypothetical 46-vertex graph.
- For adjacent \(a,b\), overlap pointed neighborhood graphs
  \(G=F_b^+\) and \(H=F_a^+\) over
  \(K=N(a)\cap N(b)\), then solve the missing edges between the two wings and
  selected vertices adjacent to neither endpoint.
- Rather than enumerate the enormous full \(R(4,5,n)\) classes for
  \(n=21,22,23\), enumerate only dense tails:
  \(n=24,e\ge127;\ n=23,e\ge119;\ n=22,e\ge113;\ n=21,e=107\).
- Use the paper's subgraph-count/excess identity as a linear-programming
  covering argument. Dense neighborhood and dual-neighborhood cases are
  discharged by pointed-graph gluing.
- Add enough dual-neighborhood vertices during gluing to reach order 37,
  propagate forbidden \(K_5/I_5\) constraints, and SAT-complete the remaining
  edges. Canonicalize pointed inputs and use automorphisms of the overlap.
- Reported main cost was about 15 CPU-years for dense catalogs plus 15
  CPU-years for gluing; independent replication was also large. This makes
  replay a secondary track on the present laptop.

Implementation warning: the printed definition
`C3=R(4,5,21,e=113)` is inconsistent with the same paper's
\(E(4,5,21)=107\). The census/archive show the intended class is
\(R(4,5,22,e=113)\).

## Reinforced generation working paper

[Nagda–Raghavan–Thakurta,
arXiv:2603.09172](https://arxiv.org/abs/2603.09172) improves other Ramsey
cells, not \(R(5,5)\).

Actionable search ideas:

- Score a valid primary graph and a larger near-feasible prospect separately;
  never confuse near-feasibility with a bound.
- Maintain genuinely different initialization families: random, algebraic or
  Paley, cyclic/Cayley, and hybrid/spectral.
- On cyclic starts, optimize generator offsets using local clique counts, then
  deliberately break symmetry by cloning/perturbing and switch to unrestricted
  edge flips.
- Use exact violation bitsets and cached flip deltas, violation-biased move
  selection, tabu/annealing, elite pools, and strategic kicks.
- For \(R(5,5)\), the paper's local mechanics specialize exactly to triangles
  in common neighborhoods and independent triples in common
  non-neighborhoods.

**CONJECTURE OR HEURISTIC:** cyclic graphs should be treated as bootstraps, not
the main search space; previous cyclic \(R(5,5)\) searches are already heavily
exhausted.

The authors' [code and witness
repository](https://github.com/google-research/google-research/tree/master/ramsey_number_bounds)
does not currently provide an \(R(5,5)\) implementation.

## Formal proof of \(R(4,5)=25\)

[Gauthier–Brown,
arXiv:2404.01761](https://arxiv.org/abs/2404.01761) and its
[HOL4 repository](https://github.com/barakeel/ramsey) provide a formally
kernel-checked proof.

Reusable proof-engineering details:

- Enumerate one-vertex extensions up to isomorphism using generalized graphs
  with red, blue, and gray edges.
- Treat nauty only as an untrusted source of isomorphism witnesses; check every
  permutation inside HOL4.
- Check cover completeness with an internal DPLL-style graph solver.
- Encode each gluing as SAT, unit-propagate fixed colors, and reconstruct the
  MiniSat result through HOL4.
- Rank covers and gluings by short-clause mass, but use the score only for
  ordering, never for sound pruning.

For this project the immediate formal use is the necessary degree bound. For a
vertex \(v\), \(G[N(v)]\) contains neither \(K_4\) nor an independent 5-set, so
\(d(v)\le24\). The anti-neighborhood contains neither \(K_5\) nor an
independent 4-set, so \(n-1-d(v)\le24\), hence \(d(v)\ge n-25\).

## Exact edge-flip identity

Let \(u,v\) be distinct vertices. Toggling \(uv\) can change the status only
of five-sets containing both endpoints, because every other five-set has the
same ten pairs before and after the toggle.

Suppose first that the nonedge \(uv\) is added. A new 5-clique is created
exactly when its other three vertices form a triangle and each is adjacent to
both \(u\) and \(v\). Thus the number created is the number \(t\) of triangles
in \(N(u)\cap N(v)\). An independent 5-set is destroyed exactly when its other
three vertices are pairwise nonadjacent and each is a nonneighbor of both
\(u\) and \(v\). Thus the number destroyed is the number \(q\) of independent
triples in the common non-neighborhood. Adding an edge cannot destroy a
5-clique or create an independent 5-set, so

\[
E(G+uv)-E(G)=t-q.
\]

Deleting an existing edge reverses the same two changes, giving

\[
E(G-uv)-E(G)=q-t.
\]

This proof is independent of the exhaustive order-6 test and the C++ kernel
self-test cited in `CLAIMS.md`.

## Exoo witness reconstruction

[Ge et al.,
arXiv:2212.12630](https://arxiv.org/abs/2212.12630) gives a directly
implementable definition:

1. On \(\mathbb Z_{43}\), color as graph edges the cyclic distances
   \(1,2,7,10,12,13,14,16,18,20,21\).
2. Delete vertex 0.
3. Recolor from edge to nonedge the consecutive pairs starting at
   \(4,5,6,7,13,14,15,16,23,24,30,33,39,40,41\), and the pair \(\{11,32\}\).

`src/construct_exoo42.py` implements this definition. The imported mathematical
description was treated as untrusted; both local verifiers independently
establish the resulting graph's Ramsey property.
