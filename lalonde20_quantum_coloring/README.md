# Lalonde 20-vertex quantum coloring

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

The argument allows zero projectors, arbitrary original rank profiles,
noncommuting apex/join projectors, reducible representations, and all finite
dimensions. It does not use a numerical search result.

The proof has four exact steps:

1. color symmetrization converts any putative $n$-coloring to common rank
   $r$ in dimension $nr$;
2. an exact rational SOS rigidifies vertices $1,\ldots,13$ for each fixed
   color;
3. every higher-rank tail, including non-transverse branches, is classified
   by a $J$-invariant $r$-plane in $K\oplus K$;
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
the human proof.

To rebuild the paper with Tectonic:

```sh
tectonic --outdir publication/build publication/paper.tex
```

See [RESEARCH_LOG.md](RESEARCH_LOG.md) for timestamped checkpoints and audit
history.
