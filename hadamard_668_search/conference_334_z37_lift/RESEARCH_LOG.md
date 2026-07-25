# Research log

## 2026-07-25 PDT

- Started a genuinely new post-gate construction route: a normalized
  symmetric conference matrix of order 334 with a semiregular \(C_{37}\)
  action on its 333-vertex core.
- Excluded the obvious mixed product of normalized conference cores of
  sizes 9 and 37.  The natural zero-filling tensor correction leaves the
  nonzero defect
  `28*(I9 tensor J37-J9 tensor I37)`, so it works only when the two core
  sizes agree.  More elaborate product constructions are not excluded.
- Derived the exact nine-orbit zero-frequency equation
  `T*1=0`, `T^2=333I-37J`, with even diagonal and odd off-diagonal block
  sums.
- A direct quadratic CP-SAT model did not decide the quotient in 120
  seconds.  An algebraic construction using the Sylvester `H8` basis then
  produced an exact integral solution immediately.
- Verified the corresponding nonnegative adjacency orbit matrix, row sum
  166, and exact conference-graph quotient equation
  `B^2+B=83I+83*37J`.
- Proved that the simplest zero/quadratic-residue/nonresidue block family is
  impossible from the trivial-character row norm alone.
- Decomposed the natural `S4`-uniform lift into standard and trivial
  representation sectors.  The standard sector requires Parseval energy
  333, while binary difference sequences have maximum energy 293.
- Broadened from `S4` to blocks translated by either regular group of order
  four.  The nonprincipal pair characters force a common pair sum; the
  odd-dimensional trivial-sector trace then forces a quadratic-character
  word whose total sum contradicts the quotient margins.
- Derived a trace law that applies to the fully general 45-block lift.
  Cyclotomic Galois conjugacy and Fourier inversion leave diagonal
  incidence pairs `(0,9)` or `(3,6)` on the two quadratic classes.  The
  certified diagonal degrees exclude `(0,9)`, so, up to swapping the
  classes, every candidate must use each residue in exactly six diagonal
  blocks and each nonresidue in exactly three.
- Counted the complete fixed-margin ambient lift space.  The quotient alone
  leaves between `2^1340` and `2^1341` assignments.  The trace law removes
  between 42 and 43 binary exponents, but the remaining space is still
  between `2^1297` and `2^1298`; unrestricted enumeration is not viable.
- Found a signed/permuted `1+4+4` normal form of the same quotient.  Its
  diagonal `-16` row has the uniquely forced shell `1^4,3^4`, and its
  completion is unique inside the diagonal-S4 block algebra.  This is a
  cleaner derivation, not a second quotient equivalence class.
- Strengthened the lift obstruction: the general trace law already
  excludes the full `S4` lift, and a standard-sector Parseval deficit
  excludes invariance under even one paired-label transposition or one
  paired-label three-cycle.
- Introduced a nonsemisimple characteristic-37 filtration with `x=1+y`.
  The full SRG equation becomes `N(y)^2=9*y^36*J`, with square-zero
  constant matrix of rank four.  Its first coefficient gives a rank-16
  linear system on the 36 skew off-block first moments.
- Proved that this modular layer reduces the exact fixed-margin census by
  precisely `37^16`, because fixed-size subset moments are uniform under
  translation.  Together with the trace law, the ambient exponent falls
  from about 1297.8 to about 1214.5.  Higher `y`-adic coefficients remain
  to be lifted.
- Built an actual trace-law-compatible membership witness whose first three
  binomial moment matrices vanish.  It passes the `y^0` through `y^3`
  equations exactly and first fails at `y^4` in 79 of 81 entries.  This
  meets the multi-layer lift test but also shows that low moment layers are
  not, by themselves, evidence of convergence.
- Constructed an explicit full formal characteristic-37 completion for
  every admissible first moment.  Each first moment is a commutator
  `[N0,A]` with `A` symmetric, and the trace-corrected conjugation formula
  with terminal term `z^18*J+19*y^36*J` solves the full equation through
  degree 36.  This is not a classification of all formal solutions; exact
  binary support realizability remains open.
- Excluded every constant diagonal and symmetric rank-one generator in that
  exponential family.  Diagonal generators leave nonzero-lag coefficients
  `13/25`.  In the nonisotropic rank-one case, six realized quadratic-
  character lag patterns force local values `a=+/-3`, `b=0`, while the
  projector identities force `a=1`.  In the isotropic square-zero case,
  five zero-lag diagonal coefficients remain nonbinary.  A viable constant
  generator in this family must therefore be genuinely nondiagonal and
  have rank at least two; higher-`y` conjugators are not excluded.
- Derived the conditional group-ring characteristic identity
  `det(YI-D)=(Y^2+Y-83)^4*(Y-(4+tr(D)))`, including explicit second-minor
  and determinant convolution identities for future pruning.
- Audited the closest literature.  Orbit-matrix and semiregular cyclic-block
  methods are standard.  Mathon's `p*q^2+1` theorem is a deceptive
  near-match but requires `p=q+2`, so it does not cover `37*3^2+1=334`.
  The 22 July 2026 multiplier paper concerns common-multiplier Legendre
  pairs and does not subsume this conference route.  No occurrence of the
  particular quotient or its trace/moment/formal results was located, but
  the audit is not exhaustive and priority remains provisional.
- The general semiregular `C37` lift is still open.  Any successful lift of
  this quotient must break the regular symmetry of the four paired fibers.
- No external communication was made.
