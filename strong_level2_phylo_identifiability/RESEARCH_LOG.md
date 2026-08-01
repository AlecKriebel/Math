# Research log

## 2026-08-01T13:45:10-07:00 — program continuation

- Created this dedicated folder for the final-closure program.
- The inherited artifact links in the supplied ChatGPT transcript do not exist
  in the local repository.  The exact graph descriptions and stated inherited
  theorems in the transcript are therefore being treated as the starting data;
  local replay certificates must be rebuilt independently.
- The repository has unrelated dirty work on both the current branch and the
  existing `main` worktree.  Those files will not be touched.  Checkpoint
  publication will use an isolated Git index based directly on `origin/main`.
- Immediate target: derive exact K2P/K3P Fourier parameterizations of the
  inherited four-leaf theta pair and decide persistence or separation.

## 2026-08-01T14:09:49-07:00 — K2P/K3P robustness resolved

- **EXACTLY COMPUTED:** rebuilt the displayed-tree Fourier engine and matched
  all fourteen stated JC orbit coordinates at the inherited rational source
  point.
- **EXACTLY COMPUTED:** replayed equality of all 64 zero-sum Fourier
  coordinates at the inherited target point modulo
  `43337075*beta^2 - 36083110*beta + 7336259`; replayed the rational isolating
  interval and open-parameter inequalities.
- **EXACTLY COMPUTED:** found an eight-term multihomogeneous quartic that
  vanishes identically on the source K2P topology.  Its target pullback is a
  nonzero polynomial and has value
  `-530769561108218123463328187575021 /
  8358844170240000000000000000000000000000000` at a rational interior K2P
  point.  The least transition probability there is `7/50`.
- **EXACTLY COMPUTED:** found the analogous eight-term quartic for K3P.  Its
  target value at a rational interior point is
  `-690050294443971144456773 /
  419904000000000000000000000000000`, and the least transition probability is
  `29/300`.
- **PROVED:** the two topology closures are irreducible and have equal
  dimension because target is the leaf-coordinate transposition `(1 4)` of
  source.  The separating quartics therefore exclude full-dimensional
  stochastic overlap under K2P and K3P.  Since the inherited JC common point
  embeds in both richer stochastic parameter spaces, separation is generic,
  not complete over the open stochastic domains.
- Numerical finite-field discovery showed that all source/target relations
  through degree three coincide; separation first appeared in the searched
  multigraded degree-four space.  No minimal-degree theorem is claimed yet.

