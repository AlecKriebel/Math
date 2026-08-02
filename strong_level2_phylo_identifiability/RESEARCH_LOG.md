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

## 2026-08-01T16:15:54-07:00 — root-collapsed Psi orbit and lifting classified

- **EXACTLY COMPUTED:** found four pairwise distinct root-suppressed
  semi-directed topologies, `A,A_reflected,B,B_reflected`, sharing one
  seven-dimensional regular JC region.  Exact rational gauge maps preserve
  all 64 zero-sum four-leaf Fourier coordinates.
- **EXACTLY COMPUTED:** restored an incoming cut edge and outgroup leaf.  Each
  augmented network is binary, strongly tree-child, and level 2, with one
  blob having cycle lengths `3,6,7` and two reticulations.
- **PROVED:** the augmented orbit splits into the two ordinary
  triangle-redirection pairs `{A,B_reflected}` and `{A_reflected,B}`.  The
  unique underlying labelled-graph isomorphism swaps the triangle vertices
  `U,V`, preserves every reticulation direction outside the triangle, and
  changes only its local reticulation designation.
- **EXACTLY COMPUTED:** derived the rational full-tensor map
  `b0=4*a0*a1*a3/d`, `b1=a1`, `b2=4*a1*a2*a3/d`,
  `b3=d/(4*a1)`, with `d=a0*a1+a2`, together with the path and pendant
  permutations.  Both pairings agree on all 256 zero-sum five-leaf Fourier
  coordinates.
- **PROVED:** rational endpoint bounds place the map in the complete open JC
  cube on a nonempty box.  Exact polynomial rank gives model dimension ten;
  nonzero rational rank-ten minors and a factored common-gauge determinant
  prove full-dimensional regular stochastic overlap.
- **PROVED:** on ordered quartet `(5,1,2,3)`, `I=J-K-M+N` vanishes on
  `{A,B_reflected}` and is strictly positive throughout the complete open
  parameter spaces of `{A_reflected,B}`.  The two nonroot classes therefore
  have disjoint stochastic interiors.
- **PROVED:** this `Psi` collision is a genuine extra move only at the global
  root, where suppression destroys its supporting triangle.  Its surviving
  nonroot lift is standard `T`, so it does not yield independent stackable
  non-triangle ambiguity bits.
- A pure-standard-library sparse rational-function implementation
  independently verifies both symbolic 256-coordinate identities, the exact
  common point, and both rank-ten determinants.  No literature search was
  conducted.

## 2026-08-01T17:02:26-07:00 — triangle-free root path-reversal Omega certified

- **EXACTLY COMPUTED:** found four rooted models in census entries `16,26`
  forming exactly two semi-directed classes and sharing one exact rational
  four-leaf Fourier tensor.  The two classes are triangle-free and not
  semi-directed isomorphic.
- **EXACTLY COMPUTED:** derived the nine-variable rational `Omega` map and
  verified all 64 zero-sum Fourier coordinates symbolically.  An explicit
  rational source point maps strictly inside the target stochastic cube.
- **PROVED:** exact core rank six, a displayed Euler tangent dependence, and
  four nonzero rank-nine minors establish model dimension nine and regularity
  on all four sheets.  The inverse-function theorem gives a common
  full-dimensional relatively open stochastic region and equality of the
  irreducible closures.
- **PROVED:** census entries `16` and `26` are reversible root placements with
  equal complete stochastic images; the exact root-splitting map was checked
  on all 64 coordinates for both labellings.
- **EXACTLY COMPUTED:** exposed the incoming port with an outgroup leaf.  Both
  lifts remain binary, strongly tree-child, triangle-free level-2 networks
  with cycle lengths `4,5,7`.
- **PROVED:** on ordered quartet `(1,2,5,3)`, `I=J-K-M+N` is identically zero
  on the lifted source and strictly positive throughout the complete open JC
  cube of the lifted target.  Their stochastic interiors are disjoint, so
  this `Omega` gadget is root-local and cannot stack naturally.
- A pure-standard-library verifier independently checks all 64 common
  coordinates and all four exact rank-nine determinants.  No literature
  search was conducted.

## 2026-08-01T18:08:37-07:00 — root-spanning four-leaf JC atlas closed

- **EXACTLY COMPUTED:** regenerated all 27 unlabelled and 612 leaf-labelled
  rooted networks in the root-spanning simple four-port slice.  They reduce
  to 216 semi-directed topologies and 108 components generated by reversible
  root placement, triangle redirection `T`, `Theta`, `Psi`, and `Omega`.
- **EXACTLY COMPUTED:** exact fraction-free polynomial Jacobian elimination
  gives dimensions 7 for two census networks, 8 for thirteen, and 9 for
  twelve.  This is a symbolic generic-rank computation, not a sampled rank.
- **EXACTLY COMPUTED:** six integer invariant templates of degrees 2 through
  5 have 60 distinct leaf-relabelling images.  Exact pullback into every one
  of the 612 complete parameterizations gives a constant signature on each
  proposed component and 108 different signatures.  All 2,898 pairs of
  different equal-dimensional components are separated.
- **PROVED:** within-component stochastic overlap follows from the existing
  exact `T`, `Theta`, `Psi`, and `Omega` maps and uniform-reversible root
  relocation.  Distinct equal-dimensional signatures force distinct
  irreducible closures.  Models of unequal dimension cannot satisfy
  `bowtie_JC` by definition.  Hence the proposed move system is an exact
  if-and-only-if classification for this finite slice.
- **EXACTLY COMPUTED:** the 108 labelled components form eight classes modulo
  simultaneous leaf relabelling.  Their ambiguity sources are one
  `Theta+T` class, one `T` class, four root-relocation-only classes, one
  `Omega` class, and one `Psi` class.
- **EXACTLY COMPUTED:** of 2,880 possible lower-to-higher directed
  containments, the six signature templates refute 2,304 and one additional
  degree-five orbit refutes 108.  The remaining 468 directions are explicitly
  marked **UNRESOLVED**; no containment is inferred from their survival.
- The deterministic machine certificate contains all network encodings,
  component memberships, dimensions, signatures, and unresolved directions.
  No literature search was conducted.

## 2026-08-01T18:36:35-07:00 — incoming-port JC atlas closed

- **EXACTLY COMPUTED:** exposed the incoming state port of every one of the
  612 root-spanning labelled networks with a new root and outgroup leaf 5.
  All 612 rooted and all 612 semi-directed lifted topologies are pairwise
  distinct.
- **EXACTLY COMPUTED:** exhaustive graph comparison finds exactly 96 ordinary
  triangle-redirection pairs and 420 singleton classes, giving 516 candidate
  nonroot observational components.
- **EXACTLY COMPUTED:** exact fraction-free symbolic Jacobian ranks are 10
  for eight unlabelled parameterizations and 11 for nineteen.  At component
  level this gives 96 dimension-10 and 420 dimension-11 classes.
- **EXACTLY COMPUTED:** two symmetry-reduced invariant templates, one cubic
  and one quartic, evaluated on only the four quartets containing incoming
  leaf 5 produce 60 exact polynomial zero/nonzero tests per model.  Their
  signatures are constant on each `T` pair and different on all 516
  components, separating all 92,550 distinct equal-dimensional pairs.
- **PROVED:** `N bowtie_JC N'` in this finite incoming-port atlas if and only
  if the two networks are isomorphic or differ by ordinary triangle
  redirection.  This exhaustively eliminates `Theta`, `Psi`, and `Omega` as
  nonroot moves in the reduced five-port slice and proves a quartet witness
  bound there.
- **EXACTLY COMPUTED:** the same quartet templates refute 39,168 of 40,320
  possible dimension-10-to-11 containments.  The remaining 1,152 directions
  are marked **UNRESOLVED** and do not affect the symmetric classification.
- No intrinsically five-leaf invariant, numerical rank, external catalogue,
  or literature search was used in the theorem.

## 2026-08-01T19:11:40-07:00 — same-root directed containments resolved

- **EXACTLY COMPUTED:** the 168 dimension-10-to-11 directions surviving the
  compact incoming-port signatures and having equal four-leaf root marginal
  form seven orbits of size 24 under simultaneous relabelling of the four
  outgoing ports.
- **PROVED:** one incoming-quartet invariant vanishes identically on the
  smaller model in each orbit and factors into a strictly nonzero expression
  throughout the larger model's complete open stochastic cube.  Six orbits
  use one cubic relabelling; the seventh uses one quartic relabelling.  Hence
  all 168 same-root directions have disjoint open stochastic images.
- **EXACTLY COMPUTED:** two of the seven orbit representatives admit explicit
  rational parameter maps into a target sheet with one Fourier edge
  multiplier equal to one.  Substitution proves equality of all 51 five-leaf
  JC orbit coordinates.
- **PROVED:** nonzero exact rank-ten source-gauge minors prove both maps are
  dominant onto the smaller closures.  Therefore 48 directed pairs are
  proper algebraic boundary containments even though their open stochastic
  images are disjoint.
- **EXACTLY COMPUTED:** combining the compact incoming signatures, root
  marginal certificates, and the new strict factors rejects 39,720 of the
  40,320 possible dimension-10-to-11 stochastic containments.  The remaining
  600 directions all cross distinct unresolved root-marginal components and
  are explicitly retained as **UNRESOLVED**.
- No numerical evidence or literature search is used in this milestone.

## 2026-08-01T19:39:40-07:00 — incoming-port stochastic containment atlas closed

- **EXACTLY COMPUTED:** the 600 cross-root dimension-10-to-dimension-11
  directions left by Milestone 3F form 25 free outgoing-label orbits and
  depend on exactly ten directed root-marginal orbits.
- **EXACTLY COMPUTED:** for every root-marginal orbit, selected one existing
  root-atlas invariant whose smaller-model pullback is identically zero and
  whose larger-model pullback has an explicit complete factorization.
- **PROVED:** nine factorizations contain only positive monomials and factors
  of the forms `x-1`, `x+1`, and `xy-1`.  The tenth contains in addition a
  strictly positive convex combination.  Every target pullback is therefore
  nonzero throughout its complete open JC parameter cube.
- **PROVED:** marginalization transports the strict separation to all 600
  lifted pairs.  Combining this with the preceding 39,720 certificates proves
  that all 40,320 unequal-dimensional incoming-port pairs have disjoint open
  stochastic images; there are no one-sided stochastic containments.
- **PROVED:** together with the equal-dimensional Milestone 3E theorem, the
  finite 612-network incoming-port atlas is now completely classified for
  full-dimensional regular overlap and one-sided stochastic containment:
  labelled isomorphism and ordinary triangle redirection `T` are the only
  generic observational equivalences.
- This does not classify every possible lower-dimensional intersection or the
  algebraic boundary-containment status of every pair.  No numerical evidence
  or literature search is used in the theorem.

## 2026-08-01T19:52:47-07:00 — minimal three-outgoing-port nonroot atlas closed

- **PROVED:** every strongly tree-child nonroot theta blob with exactly three
  outgoing ports arises from the four-core expansion rule with the ordinary
  port count fixed by its number of path-sink reticulations.
- **EXACTLY COMPUTED:** 42 raw core subdivisions reduce to 30 labelled rooted
  and 30 labelled semi-directed candidates.  They use core types `0,2,3`;
  the separated `TT` core requires at least four outgoing ports and is absent.
- **EXACTLY COMPUTED:** reversible root relocation identifies every candidate
  with a unique semi-directed topology in the certified four-leaf root atlas.
  The 30 candidates partition into 21 JC observational components: nine
  size-two ordinary triangle-redirection classes and twelve singletons.
- **PROVED:** the assigned root-atlas dimensions give nine dimension-eight
  components and twelve dimension-nine components.  Eighteen `S_3` orbits of
  exact strict invariants separate all 108 dimension-eight-to-nine pairs over
  their complete open parameter cubes.
- **PROVED:** full-dimensional regular JC overlap in this complete minimal
  nonroot atlas occurs exactly under labelled isomorphism or `T`, and there
  are no one-sided stochastic containments.  In particular, no non-triangle
  ambiguity becomes stackable merely because a fourth outgoing witness port
  is absent.
- No numerical evidence, external catalogue, or literature search is used.
