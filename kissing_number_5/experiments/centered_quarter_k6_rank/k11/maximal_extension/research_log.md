# Research log: K11 maximal quarter-grid extensions

## 2026-07-24T05:48Z

- Fixed the 51 selected K11 atoms as exact rank-five source Gram matrices.
- Chose the first five vertices as a positive-definite basis in every atom.
- Exhaustively enumerated the \(7^5\) possible quarter-grid correlation rows
  for an additional unit point.
- Built the exact candidate compatibility graphs.  Candidate counts ranged
  from 12 to 71.

## 2026-07-24T05:56Z

- Computed exact maximum-clique sizes 7--29, corresponding to exact maximal
  total sizes 18--40.
- Found proper colorings using exactly the same number of colors as the
  displayed clique size for every graph.  This converted the discovery
  computation into simple clique/coloring sandwich certificates.
- Identified the thirteen atoms reaching total size 40:
  6, 7, 9, 10, 18, 23, 27, 41, 43, 44, 47, 49, 50.

## 2026-07-24T06:03Z

- Added an independent verifier using exact integer arithmetic and explicit
  exceptions.  It reconstructs source rank five, enumerates all candidates,
  regenerates every compatibility graph, and checks every clique and coloring
  witness.
- Added tamper tests for colors, cliques, candidate counts, and hashes.
- Verified the checker and tests both normally and under `python -O`.
- Pinned certificate SHA-256
  `c0d75a0d9422a9aef646d90280c0f0d0d984e9981ac77da1bf0063818d7b2465`.

## 2026-07-24T06:14Z

- Reconstructed exact rational coordinate models for \(D_5,L_5,Q_5,R_5\).
- Classified the thirteen stored K40 completions by complete Gram-preserving
  permutations: atoms 6 and 23 give \(D_5\), and the other eleven give
  \(L_5\).
- Exported all exact Gram matrices and rational-over-\(\sqrt2\) coordinates.
- Pinned classification SHA-256
  `ccabd04602c5481d40fa16d5979a7cbcb04fa3ece357f3c97d39e881f1bef0a0`.

## 2026-07-24T06:23Z

- Ran 26 deterministic symmetry-broken N41 construction probes: insertion
  plus unrestricted release and one-to-two replacement plus unrestricted
  release from every exact K40 completion.
- Best recomputed maximum inner product was 0.5213989457472671.  All outcomes
  are labeled numerical evidence only.
- Independently recomputed 78 stored coordinate diagnostics and added tamper
  tests.
- Replayed the portfolio byte-for-byte; results SHA-256
  `2049ff1827e1f30298bf9a289be9773e498dd1f0dc4c5adb24f7a104c1c99465`.

## 2026-07-24T06:26Z

- Replayed the maximal-extension and classification generators
  byte-for-byte.
- Compiled all new Python sources and ran 14 exact/tamper tests under
  `python -O`; all passed.
- Retained the central scope limitation: the exact theorem covers only the
  51 selected K11 atoms and only quarter-grid extensions.  It is not a global
  proof that \(\tau(5)=40\).
