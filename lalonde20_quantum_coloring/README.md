# The quantum chromatic number of the G19 join family

This folder is the self-contained research and publication package resolving
the exact dichotomy

\[
\chi_q(G_{19}\vee K_1)\in\{4,5\}.
\]

The base graph has vertex set `1,...,19` and edge set

```text
(1,2)  (1,3)  (1,8)  (1,9)  (1,15)
(2,3)  (2,6)  (2,7)  (2,14)
(3,4)  (3,5)  (3,16)
(4,5)  (4,12) (4,13)
(5,10) (5,11) (5,17)
(6,7)  (6,11) (6,13)
(7,10) (7,12) (7,19)
(8,9)  (8,11) (8,12) (8,18)
(9,10) (9,13)
(14,17) (14,18)
(15,17) (15,19)
(16,18) (16,19)
```

Its graph6 checksum is `RxLAKA@AgYAWDGO?O?@??A?W@@OC@_`.  Vertex 20 is
adjacent to every base vertex.

## Result

The finite-dimensional unrestricted quantum chromatic number is

\[
\boxed{\chi_q(G_{19}\vee K_1)=5}.
\]

In fact, the proof establishes the full joined family

\[
\boxed{\chi_q(G_{19}\vee K_{n-3})=n+1\quad(n\ge3)}.
\]

This confirms the family proposed in Section 4.2 of Lalonde's *Quantum
colorings of spheres* as finite witnesses for the complex-sphere obstruction:

\[
\xi(G_{19}\vee K_{n-3})=n<\chi_q(G_{19}\vee K_{n-3})=n+1.
\]

It also gives an alternative finite-witness proof of Lalonde's sphere bound
\[
\chi_q(S_{\mathbb C}^{n-1})\ge n+1.
\]
The equality at \(n=3\) was already known; the first new unrestricted case is
the one-apex graph at \(n=4\).

Using Lalonde's notation for the restricted parameters, the same conclusion
holds at every fixed local dimension and every fixed projector rank:

\[
\chi_q^{[d]}(G_{19}\vee K_{n-3})
=\chi_q^{(r)}(G_{19}\vee K_{n-3})=n+1
\qquad(d,r\ge1).
\]

The argument allows zero projectors, arbitrary original rank profiles,
noncommuting apex/join projectors, reducible representations, and all finite
dimensions. It does not use a numerical search result.

The proof has four exact steps:

1. color symmetrization converts any putative $n$-coloring to common rank
   $r$ in dimension $nr$;
2. an exact rational SOS rigidifies vertices $1,\ldots,13$ for each fixed
   color;
3. every higher-rank tail, including non-transverse branches that are not
   scalar direct sums, is classified by a $J$-invariant $r$-plane in
   $K\oplus K$;
4. cross-color orthogonality produces two sector packings whose dimension
   inequalities sum to the contradiction $3nr\le2nr$.

## Package

- `publication/paper.tex` and `publication/build/paper.pdf`: self-contained
  theorem and proof.
- `publication/technical_summary.tex` and
  `publication/build/technical_summary.pdf`: two-page technical synopsis.
- `publication/nontechnical_150_words.md`: exactly 150 words.
- `publication/author_handoff.md`: contribution and novelty handoff.
- `publication/assumptions_and_analysis.md`: conventions, equality,
  irreducibility, and minimal-dimension analysis.
- `publication/priority_audit.md`: narrow post-proof literature audit.
- `publication/reviewer_suggestion_audit.md`: itemized disposition of the
  post-proof presentation suggestions.
- `certificate/`: machine-readable exact obstruction certificates.
- `verification/`: independent standard-library exact replay tools.
- `src/graph_data.py`: canonical graph data and checksums.
- `src/search_*.py`: exploratory counterexample searches; these are not used
  by the proof.

## Exact verification

From this folder, run

```sh
python3 verification/verify_graph.py
python3 verification/verify_obstruction_certificate.py
python3 verification/verify_lalonde_uniform_obstruction.py \
  certificate/lalonde_uniform_obstruction.json
```

All verification arithmetic is exact. The two obstruction verifiers use only
the Python standard library. See `verification/README.md` for their precise
coverage and the elementary finite-dimensional semantic bridges retained in
the human proof. The graph checker additionally proves exact
non-three-colorability, checks the published four-coloring, and confirms that
the base graph has no four-clique.

To rebuild the paper with Tectonic:

```sh
tectonic --outdir publication/build publication/paper.tex
```

See [RESEARCH_LOG.md](RESEARCH_LOG.md) for timestamped checkpoints and audit
history.
