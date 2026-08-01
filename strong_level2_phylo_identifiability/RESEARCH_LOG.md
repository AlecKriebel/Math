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

## 2026-08-01T14:28:10-07:00 — reduced generator atlas completed

- **PROVED:** every nontrivial level-2 blob has cyclomatic number equal to its
  number of reticulations and reduces to either a cycle or a theta core.
- **EXACTLY COMPUTED:** enumerated 24 valid rooted theta event orientations
  before symmetry and four after quotienting by branch reversal and path
  permutation.  Together with the unique cycle orientation, this gives five
  complete orientation-core templates.
- **PROVED:** parameterized every full ported blob by ordered chains of
  ordinary tree port vertices on directed core segments.  This also explains
  why fully port-labelled blobs are infinite even though the core atlas is
  finite.
- **EXACTLY COMPUTED:** obtained template automorphism orders and all minimum
  segment-subdivision repairs enforcing strong tree-childness and the
  no-reticulation-child clause.
- No external generator catalogue or specialized phylogenetic software was
  used.

## 2026-08-01T15:10:38-07:00 — first exact JC atlas class completed

- **EXACTLY COMPUTED:** the root-spanning simple four-leaf theta census has
  112 raw port distributions, 27 unlabelled rooted networks, and 612
  leaf-labelled rooted isomorphism classes.
- **EXACTLY COMPUTED:** isolated census entries `0,4,13,22` with the stated
  leaf assignments and proved that all six inherited JC equations vanish
  identically on every complete parameterization.
- **PROVED:** exact rank-eight minors and irreducibility of the positive
  invariant locus imply that all four Zariski closures equal the inherited
  eight-dimensional closure.
- **EXACTLY COMPUTED / INTERVAL CERTIFIED:** extended the inherited quadratic
  common point through one exact triangle redirection and two root
  relocations.  All 64 zero-sum Fourier coordinates agree, every parameter is
  strictly in `(0,1)`, and all four rank-eight minors are nonzero at that same
  point.
- **PROVED:** the inverse-function argument gives one common regular relative
  open stochastic region of full dimension for all four models.
- **EXACTLY COMPUTED:** the four rooted topologies form exactly two
  semi-directed isomorphism classes, `{0,4}` and `{13,22}`.  The classes are
  the inherited `Theta` pair after triangle redirection; each class's two
  rooted representatives differ only by reversible root placement.
- **PROVED:** JC root relocation preserves the complete stochastic image,
  since a root-split edge enters the Fourier model only through the product of
  its two multipliers and every effective multiplier has a rational open
  split.
- A pure-standard-library verifier independently checks the common quadratic
  point and all four exact Jacobian determinants.  No literature search was
  conducted.
