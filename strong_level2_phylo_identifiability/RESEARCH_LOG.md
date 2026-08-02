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

## 2026-08-01T20:02:08-07:00 — arbitrary theta subdivisions reduced to bounded support decks

- **PROVED:** every strong port expansion of each of the four oriented theta
  cores contains a core-preserving strong support consisting of every
  path-sink port and one ordinary port on each segment of a contained minimal
  tree-child repair.
- **EXACTLY COMPUTED:** the support sizes are `3,4,3,3` for the four cores.
  Exhaustive occupancy masks verify every monotone strong segment pattern and
  every contained minimal repair.
- **PROVED:** relative to a fixed labelled support, a support-plus-one
  restriction identifies the directed core segment of any extra port.  A
  support-plus-two restriction identifies the order of any two extra ports on
  the same segment.  These pairwise comparisons reconstruct every complete
  ordered port chain, up to labelled core isomorphism.
- **PROVED:** the full collection of induced restrictions on at most six
  outgoing ports determines every finite ported strong theta topology.  If
  the distinguished incoming state port is counted, the corresponding tensor
  restrictions have at most seven total ports.
- **UNRESOLVED:** this is a combinatorial bounded-deck theorem, not yet a JC
  observational-completeness theorem.  The remaining finite task is the
  support-augmented stochastic atlas through six outgoing ports and the
  recovery of those local tensors from a global distribution.
- No numerical evidence or literature search is used.

## 2026-08-01T20:59:20-07:00 — fully relatively labelled bounded-support JC atlas closed

- A first exact replay on 496 role-normalized support-plus-two candidates
  passed, but a scope audit caught that fixing the sink/repair/probe label
  roles did not classify arbitrary relative descendant-block labellings.  No
  theorem was published at that weaker scope.
- **EXACTLY COMPUTED:** adding all outgoing-label permutations and the missing
  support-size-four plus one-probe case gives 656 raw role presentations, 520
  canonical role candidates, and 192,000 relative-label presentations.
- **PROVED / EXACTLY COMPUTED:** exact mixed-graph
  individualization-refinement quotients those presentations into 19,500
  labelled structural classes modulo ordinary triangle redirection: 8,520
  with five outgoing ports and 10,980 with six.
- **PROVED:** each quartet marginal is determined by the four displayed-tree
  descendant masks of every edge.  Equal mask signatures occur only through
  products of independent JC edge multipliers, and signed permutations of
  the two parent-choice bits are open-cube automorphisms.  This is an exact
  stochastic reduction, not an inference from equal closures.
- **EXACTLY COMPUTED:** all 7,360 quartet restrictions reduce to 90 tensor
  types.  Exact rational polynomial replay of all 60 root-atlas invariants on
  each type gives 5,400 symbolic pullbacks.  An additional 8,368 bits agree
  with the earlier direct full-network symbolic certificate.
- **PROVED / EXACTLY COMPUTED:** 75 selected identities for five outgoing
  ports and 65 for six give exactly 19,500 zero/nonzero signatures, one for
  each structural class and no non-`T` collision.  Full-dimensional regular
  JC overlap in this atlas is therefore exactly isomorphism plus `T`.
- **PROVED:** together with the exact three- and four-outgoing atlases, every
  strong support-deck member required by the size-six combinatorial theorem is
  classified modulo `T`.
- **UNRESOLVED:** a support chosen in one arbitrary strong blob may induce a
  nonstrong or non-core-preserving restriction in a competing blob.  Those
  cross-support targets, one-sided containments in the new atlas, recovery of
  global local tensors, and the global `L_1` theorem remain open.
- No numerical evidence, external catalogue, specialized network software,
  or literature search is used.

## 2026-08-01T21:26:36-07:00 — arbitrary nonroot theta theorem closed

- **PROVED:** every possibly nonstrong selected restriction induced from a
  full strong theta blob is obtained by assigning selected labels to arbitrary
  directed core segments and a subset of path-sink ports, then supplying
  omitted sink children and missing minimal repairs with unobserved dummy
  leaves.
- **EXACTLY COMPUTED:** the five- and six-outgoing weak-target censuses contain
  1,512 and 2,856 role presentations, reducing to 427 and 1,027 exact base
  tensor decks.  Dummy-repair choice is exactly irrelevant after edge-product
  reduction.
- **EXACTLY COMPUTED:** the weak atlas uses 50 quartet tensor types, 40 new
  beyond the strong-support atlas.  All 2,400 new root-invariant pullbacks are
  replayed as exact rational polynomials.
- **EXACTLY COMPUTED:** arbitrary relative labellings give 16,470 exact weak
  signatures with five outgoing ports and 218,205 with six.  Strength status
  never mixes within one signature.
- **PROVED / EXACTLY COMPUTED:** the intersections with the strong atlas have
  exactly 8,520 and 10,980 signatures.  Every intersecting target restriction
  is itself strong.  Exact canonical graph replay checks all 12,720 and 43,920
  intersecting labelled target presentations and finds zero non-`T` targets.
- **PROVED:** equality of full blob closures implies equality of every selected
  marginal closure because Fourier marginalization is a dominant edge-product
  reparameterization.  The weak-target separation therefore forces each
  bounded support restriction of a competitor to be strong and `T`-equivalent.
- **PROVED:** Milestone 4A's support-plus-two deck then reconstructs every
  complete ordered port word.  Arbitrary finite strongly tree-child nonroot
  theta blobs have full-dimensional regular JC overlap if and only if they are
  related by labelled isomorphism and ordinary triangle redirection `T`.
- **UNRESOLVED:** one-sided weak-atlas containments, cross-generator local
  comparisons, global cut-split/blob-tree recovery, and nonlocal ambiguity
  remain open.
- No numerical evidence, external catalogue, specialized network software,
  or literature search is used.

## 2026-08-01T21:48:01-07:00 — all nonroot level-2 generator types classified under JC

- **PROVED:** every arbitrary strong cycle subdivision has a two-outgoing
  core-preserving support; support-plus-one locates an extra port and
  support-plus-two recovers pairwise side order. Restrictions on at most
  four outgoing ports reconstruct both complete ordered cycle sides modulo
  side swap and ordinary triangle redirection `T`.
- **EXACTLY COMPUTED:** the full strong cycle atlas has 9 structural and exact
  signature classes at three outgoing ports and 48 at four outgoing ports,
  with zero non-`T` collisions. The two-outgoing triangle is one exact `T`
  class.
- **EXACTLY COMPUTED:** all bounded strong and weak cycle marginals use four
  exact descendant-mask tensor types. The verifier replays 240 rational
  polynomial invariant pullbacks. Weak atlases through outgoing sizes
  three, four, five, and six contain 12, 63, 390, and 2,790 exact signatures.
- **PROVED / EXACTLY COMPUTED:** the four-outgoing strong/weak cycle
  intersection consists of all 48 strong signatures, every target retains
  its selected sink, and exact graph replay finds zero non-`T` targets among
  all 96 intersecting labelled presentations. Dominant marginalization and
  ordered-side reconstruction lift this to arbitrary finite nonroot cycle
  blobs.
- **EXACTLY COMPUTED:** strong theta versus weak cycle signature intersections
  are empty at outgoing sizes 3, 4, 5, and 6: respectively `21∩12`,
  `516∩63`, `8520∩390`, and `10980∩2790` have size zero.
- **PROVED:** cycle and theta generators are mutually JC-separated. Combined
  with Milestone 4C and the exhaustive level-2 generator theorem, arbitrary
  finite strongly tree-child nonroot level-2 blobs have full-dimensional
  regular JC overlap exactly under labelled isomorphism and `T`.
- **UNRESOLVED:** one-sided arbitrary-blob containments, global cut-split and
  blob-tree recovery, nonlocal conspiracies, and arbitrary root-blob
  classification remain open.
- No numerical evidence, external catalogue, specialized network software,
  or literature search is used.

## 2026-08-01T22:33:00-07:00 — generic JC cut splits and bridge tree reconstructed

- **PROVED:** every cut-edge pattern flattening factors through one hidden
  four-state variable and therefore has rank at most four identically. Pattern
  and Fourier flattening ranks agree under invertible sidewise transforms.
- **PROVED:** an arbitrary two-colour port word with a split displayed by
  every switching has at most one colour transition per directed segment and
  reduces to one representative per monochromatic run, with a second retained
  only for a globally singleton run. This gives a finite exhaustive
  compression for arbitrarily subdivided blobs.
- **EXACTLY COMPUTED:** the root/nonroot theta censuses test 124,368 and
  251,352 balanced run-compressed colourings plus 2,232 singleton-run cases in
  each position. The root/nonroot cycle censuses test 16 and 54 balanced
  colourings plus 20 and 24 singleton-run cases. No nontrivial port split is
  displayed by every parent-choice switching.
- **PROVED:** contracting blobs gives a tree. Every non-edge leaf split has a
  crossing quartet; a resolved crossing persists through a bridge, while a
  star crossing is resolved against the split by the exact local switching
  lemma. Hence some displayed tree crosses every non-cut split.
- **EXACTLY COMPUTED:** at effective JC multiplier `1/2`, the two crossing
  quartet Fourier flattenings have exact rank 16. Their common upper-left
  `5x5` minor has determinant `3/1024` for true split `13|24` and `-3/4096`
  for true split `14|23` when testing `12|34`.
- **PROVED:** boundary specialization makes a nonzero-minor polynomial
  certificate for every non-cut split. Outside one proper algebraic
  exceptional set, rank at most four characterizes exactly the cut splits.
  The compatible split system reconstructs the unique homeomorphism-reduced
  leaf-labelled bridge tree.
- **PROVED:** two networks with full-dimensional regular JC overlap have the
  same nontrivial cut splits and reduced bridge tree. An unlabelled degree-two
  root factor is not encoded by splits and is explicitly deferred to the
  root-local atlas.
- **UNRESOLVED:** analytic local-tensor extraction, arbitrary incoming-port
  comparisons, arbitrary root-blob classification, and one-sided global
  containment remain open.
- No literature search or numerical evidence is used.

## 2026-08-01T23:30:19-07:00 — two-port root cycle collapses exactly under JC

- **PROVED:** the unique strongly tree-child two-port root cycle has complete
  Fourier tensor `(1,rho,rho,rho)` on zero-sum characters, where
  `rho=p*q*(lambda*t+(1-lambda)*s*u)` lies in `(0,1)`.
- **PROVED:** an ordinary binary root with arm multipliers `c,d` has the same
  tensor with effective parameter `c*d`. The rational map
  `c=(1+rho)/2`, `d=2*rho/(1+rho)` sends every open cycle point to an open
  tree point.
- **PROVED:** every open tree point maps rationally back by setting
  `r=c*d`, `C=(1+r)/2`, `H=4*r/(1+r)^2`,
  `p=q=C`, `t=H`, `s=(1+H)/2`, `u=2*H/(1+H)`, and `lambda=1/2`.
  The factor `(1-r)^2` certifies `H<1`.
- **PROVED:** the two complete open stochastic images are equal and remain
  equal after arbitrary corresponding rooted JC components are substituted
  at both ports. Both local images have dimension one and are regular
  throughout their open domains.
- **EXACTLY COMPUTED:** one common point has effective multiplier `41/180`,
  matching tree arms `221/360,82/221`, and nonzero rank minors `82/225` and
  `82/221`.
- **PROVED:** this is the only possible degree-two nontrivial blob factor in
  the strong level-2 class. Under a multiplicity-retaining semi-directed
  convention it is a new move `C_root`; under a root-zipped convention it is
  already suppressed.
- **UNRESOLVED:** arbitrary degree-at-least-three root blobs and the K2P/K3P
  behavior of this move remain open.
- No literature search or numerical evidence is used.

## 2026-08-01T23:51:00-07:00 — root collapse extended exactly to K2P and K3P

- **PROVED:** every strictly positive group-based probability kernel `R`
  factors as `E*D` within JC, K2P, or K3P.  If `m` is a minimum coordinate,
  set `epsilon=2m`, `E=(1-epsilon)delta_0+epsilon U_G`, and
  `D=(R-epsilon U_G)/(1-epsilon)`.  Both factors are strictly positive.
- **EXACTLY COMPUTED:** all four minimum-coordinate chambers replay sixteen
  probability-convolution identities and twelve Fourier-product identities.
  Uniform subtraction and rescaling preserve the K2P probability equality;
  in JC the two factor multipliers are `(1+x)/2` and `2x/(1+x)`.
- **PROVED:** applying the factorization once maps every open two-port root
  cycle to an ordinary root. Applying it three times maps every open ordinary
  root back to a cycle by arranging the two reticulation routes to have the
  same positive kernel and setting inheritance probability `1/2`.
- **PROVED:** `C_root` therefore preserves the complete open stochastic image
  under JC, K2P, and K3P, including after arbitrary identical components are
  attached at both ports.
- **EXACTLY COMPUTED:** at the common all-character multiplier point, the
  local image dimensions are `1,2,3`; source rank determinants are
  `1/8,1/64,1/512` and tree-side determinants are `1/2,1/4,1/8`.
- **PROVED:** the model hierarchy is not a uniform nesting of move systems:
  K2P/K3P generically separate `Theta`, but both retain `C_root` with complete
  image equality.
- **UNRESOLVED:** arbitrary degree-at-least-three root blobs under JC and the
  remaining K2P/K3P local/global atlases are still open.
- No literature search or numerical evidence is used.

## 2026-08-02T00:15:54-07:00 — complete three-port JC root atlas saturates

- **EXACTLY COMPUTED:** exhaustive core expansion gives one ordinary tree,
  two root cycles, and five root theta blobs with exactly three outgoing
  ports.  These yield `3,9,30` labelled rooted topologies and `1,3,18`
  semi-directed topologies by kind.
- **EXACTLY COMPUTED:** the tree model has exact generic rank three. Every
  reticulate model has rank four, the full three-leaf JC orbit-space
  dimension.
- **PROVED:** in the equal-internal-edge, inheritance-`1/2` subfamily, each
  reticulate model has a scale-free ratio
  `kappa=u^2/(r12*r13*r23)`. Exact Sturm counts isolate one simple solution
  to `kappa=16/25` in `(1/8,7/8)` for all seven unlabelled models.
- **PROVED:** positive algebraic pendant multipliers give every reticulate
  model the same exact target
  `(delta^2,delta^2,delta^2,4*delta^3/5)`, with `delta=2^-30`.  The bound
  `c_ij>=h^7` puts all pendant multipliers strictly below `2^-9`.
- **PROVED:** the logarithmic rank-four determinant is exactly
  `-kappa'(h)/kappa(h)` and is nonzero at every simple isolated root.  Hence
  all 39 reticulate labelled rooted models share one regular
  four-dimensional stochastic neighborhood.
- **PROVED:** move `R3` may replace any reticulate three-port root blob by any
  other. It joins 21 semi-directed topologies and can change the generator
  type and reticulation count. The one-triangle restriction still contains
  33 rooted and 15 semi-directed compatible topologies in `L_1`.
- **UNRESOLVED:** one-sided containment of the ordinary-tree tensor and the
  arbitrary subdivided root atlas from four ports upward remain open.
- No literature search or numerical evidence is used.

## 2026-08-02T00:24:07-07:00 — tree/reticulate three-port separation completed

- **PROVED:** `F=r12*r13*r23-u123^2` vanishes identically on the ordinary
  three-port tree model.
- **EXACTLY COMPUTED:** after dividing positive pendant squares and exact
  open-cube factors `x` and `1-x`, every one of the seven reticulate
  pullbacks has a natural tensor-product Bernstein expansion with no negative
  coefficients and at least one positive coefficient.
- **EXACTLY COMPUTED:** the positive-coefficient counts for the two cycles
  and five thetas are `6,1,1464,1671,3016,266,268`; all remaining
  coefficients are zero and every coefficient lies in `[0,1]`.
- **PROVED:** Bernstein basis functions and all removed factors are strictly
  positive on the open cube, so `F>0` throughout every reticulate model.
- **PROVED:** the ordinary-tree and `R3` classes have disjoint complete open
  stochastic interiors. Neither direction admits one-sided generic
  containment. This completes the full three-port root `bowtie_JC` and
  containment atlas.
- **UNRESOLVED:** complete-image equality among distinct `R3` reticulate
  models is not claimed; arbitrary root blobs from four ports upward remain.
- No literature search or numerical evidence is used.

## 2026-08-02T00:34:05-07:00 — four-port root cycles classified and Psi reduced

- **EXACTLY COMPUTED:** four-port root cycles have two unlabelled rooted
  layouts, 48 labelled rooted presentations, and 12 labelled semi-directed
  topologies. Both parameterizations have exact generic JC dimension seven.
- **EXACTLY COMPUTED:** sixty exact invariant pullbacks partition the cycles
  into twelve classes of four rooted presentations. Their signatures match
  precisely theta components `96,...,107`, the twelve old dimension-seven
  `Psi` components, and no other theta component.
- **EXACTLY COMPUTED:** inserting `C_root` above both sides of every one of
  the 24 balanced labelled cycles produces exactly all 48 `Psi` theta
  presentations, with the expected component membership.
- **PROVED:** equality of a complete two-state port tensor is preserved under
  contraction with any common downstream two-input context, even when the
  continuations reconnect. Therefore every matching cycle/theta pair has
  equality of complete open images under JC, K2P, and K3P.
- **PROVED:** `Psi` is a derived move, generated by contextual `C_root` and
  reversible root placement. Each of the twelve combined classes contains
  eight rooted and five semi-directed topologies. No other four-port
  cycle--theta `bowtie_JC` collision occurs.
- **PROVED:** together with Milestone 3D, this completes the JC `bowtie`
  classification of all nontrivial strong four-port root blobs.
- **UNRESOLVED:** one-sided four-port containments and arbitrary root
  subdivisions with five or more ports remain open.
- No literature search or numerical evidence is used.

## 2026-08-02T01:13:10-07:00 — Omega extends to arbitrary root path chains

- **PROVED:** for every `k>=2`, the root-spanning triangle-free theta with
  labelled port order `P1,...,Pk,Q,X` has a nonisomorphic semi-directed mate
  with order `Pk,...,P1,X,Q`.  The reticulation sets differ under the forced
  underlying reflection, so this is not triangle redirection.
- **PROVED:** one rational map works for every chain length.  Reversing the
  middle edges and pendants reduces every zero-sum Fourier coordinate to five
  character cases; all five symbolic differences vanish identically.
- **EXACTLY COMPUTED:** complete displayed-tree contractions independently
  verify all `64,256,1024` zero-sum coordinates for `k=2,3,4`.
- **PROVED:** the ungauged core tensor depends on only five endpoint
  combinations plus the `k-1` middle multipliers.  One pendant Euler direction
  is already a core direction, giving the upper bound `2k+5`.
- **PROVED:** adjacent four-port marginals recover those effective core
  combinations, every middle multiplier, and all free pendants.  At the
  uniform rational witness the only nontrivial determinant factor clears to
  an odd integer, proving rank `2k+5` for every `k`.
- **EXACTLY COMPUTED:** at `k=3`, all 256 coordinates agree at an open
  rational point and a rank-eleven source minor is
  `-81/755578637259143234191360000000`.
- **PROVED:** the two model closures are equal and the stochastic images share
  a full-dimensional regular neighborhood for every `k`.  An incoming-port
  marginal reduces to the prior strict Omega obstruction, so the move remains
  root-local.
- **UNRESOLVED:** the bounded support-deck census has one contextual `C_root`
  family and this `Omega_chain` family left; converting that census into the
  arbitrary-root completeness theorem is the next step.
- No literature search or numerical evidence is used.
