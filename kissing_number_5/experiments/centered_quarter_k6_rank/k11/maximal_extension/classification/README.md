# Exact classification of the thirteen stored K40 completions

## Result

The thirteen maximum-clique witnesses of total size 40 yield no new
isometry type:

- atoms 6 and 23 complete to \(D_5\);
- atoms 7, 9, 10, 18, 27, 41, 43, 44, 47, 49, and 50 complete to \(L_5\);
- none of the stored completions is \(Q_5\) or \(R_5\).

This classifies the particular cliques stored in
`../maximal_quarter_grid_extensions.json`.  An atom can have other maximum
cliques, so the result does not classify every completion of that atom.  For
example, the underlying K11 atom 23 embeds in both \(D_5\) and \(L_5\), while
the stored clique completes it to \(D_5\).

## Exact pair distributions

The table uses inner products of unit vectors.  Counts are for unordered
distinct pairs.

| Code | \(-1\) | \(-4/5\) | \(-3/4\) | \(-1/2\) | \(-3/10\) | \(-1/4\) | \(0\) | \(1/5\) | \(1/2\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| \(D_5\) | 20 | 0 | 0 | 240 | 0 | 0 | 280 | 0 | 240 |
| \(L_5\) | 12 | 0 | 32 | 192 | 0 | 32 | 272 | 0 | 240 |
| \(Q_5\) | 10 | 30 | 0 | 180 | 60 | 0 | 250 | 10 | 240 |
| \(R_5\) | 6 | 30 | 20 | 144 | 60 | 28 | 242 | 10 | 240 |

These are reconstructed from exact coordinates and agree with Table 1 of
Henry Cohn and Isaac Rajagopal,
[“Variations on Five-Dimensional Sphere Packings”](https://doi.org/10.1007/s00454-026-00841-x).
Because the four distributions are distinct, each distribution excludes the
other three known types.  The classification does not rely on this invariant
alone: the certificate supplies an explicit permutation carrying every one
of the \(40^2\) Gram entries to the claimed known code.

## Exact exported data

`completion_classification.json` contains, for each completion:

- its complete scaled \(40\times40\) Gram matrix, stored by upper triangle;
- an explicit permutation to a fixed exact \(D_5\) or \(L_5\) model;
- all 40 standard Euclidean coordinate rows;
- its exact pair distribution.

A coordinate row \(q\) in the JSON represents \(q/\sqrt2\).  Thus the
coordinate numerators are rational and every normalized Gram entry is
\(\langle q_i,q_j\rangle/2\).  The verifier checks these coordinates against
the reconstructed completion entry by entry.

The fixed models are reconstructed rather than trusted as opaque data:

- \(D_5\) consists of every vector with two nonzero coordinates, each
  independently \(\pm1\);
- \(L_5\) replaces the eight \(D_5\) points
  \((\pm1,0,0,0,1)\), with the first four coordinates permuted, by the eight
  points whose first four coordinates are \(\pm1/2\) with an odd number of
  minus signs and whose fifth coordinate is 1;
- \(Q_5\) and \(R_5\) are independently reconstructed by the exact
  layer-reflection descriptions, to verify the comparison distributions.

All four unnormalized models have squared norm 2.

## Reproduction

```text
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k6_rank/k11/maximal_extension/classification/verify_classification.py
PYTHONPATH=. .venv/bin/python -m unittest -v experiments/centered_quarter_k6_rank/k11/maximal_extension/classification/test_classification.py
```

The classification certificate SHA-256 is

```text
ccabd04602c5481d40fa16d5979a7cbcb04fa3ece357f3c97d39e881f1bef0a0
```

The verifier first reruns the exact maximal-extension verifier, reconstructs
each clique completion from the K11 source, checks all 20,800 Gram entries
and 520 coordinate rows, and verifies the explicit isometry permutations.
It uses rational/integer arithmetic and explicit exceptions and passes under
`python -O`.  Tamper tests alter a Gram entry, a coordinate, a permutation,
and the file hash; each alteration is rejected.
