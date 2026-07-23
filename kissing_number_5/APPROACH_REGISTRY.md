# Approach Registry

Last updated: 2026-07-23T18:39:53Z

Statuses are `active`, `blocked`, `falsified`, `subsumed`, or `certified`.

## A. Exact constructions and unrestricted optimization

- **Route:** Optimize \(N=41,42,43,44\) unit vectors directly, using nonsmooth
  max-inner-product objectives, soft-max/energy continuation, manifold
  optimization, random asymmetric starts, and surgery on all four known
  40-point configurations.
- **Proved lemmas:** The exact \(D_5\) construction gives \(N=40\).
- **Unresolved:** Whether any \(N\geq41\) feasible code exists; whether persistent
  near misses have a common exact obstruction.
- **Artifacts:** `certificates/d5_roots.json`; search artifacts pending.
- **Counterexamples:** Non-uniqueness and non-antipodality of 40-point codes
  invalidate symmetry-only search assumptions.
- **Restrictions:** The main search must be unrestricted; structured searches
  are discovery subroutines only.
- **Status:** active.

## B. Two-point harmonic/linear programming

- **Route:** Search auxiliary Gegenbauer polynomials and strengthened
  piecewise-polynomial inequalities, possibly coupled to exact local cap data.
- **Proved lemmas:** Standard Delsarte positivity applies to every spherical
  code when coefficients in the normalized Gegenbauer basis are nonnegative
  and the auxiliary polynomial is nonpositive on the allowed off-diagonal
  interval.
- **Unresolved:** Produce a valid objective below 41, or prove the ordinary
  two-point cone cannot do so and identify the minimal strengthening required.
- **Artifacts:** none yet.
- **Known counterexamples:** None recorded yet; ordinary LP is historically too
  weak in this dimension.
- **Restrictions:** No symmetry assumption; two-point information only.
- **Status:** active.

## C. Three-point and higher-order SDP/SOS

- **Route:** Implement the Bachoc--Vallentin three-point bound with explicit
  polynomial normalizations, then explore higher degree and k-point/Lasserre
  strengthenings.  Recover exact rational/algebraic duals from high-precision
  discovery runs and certify PSD/nonnegativity independently.
- **Proved lemmas:** Published three-point computations imply the imported upper
  bound 44.
- **Unresolved:** An exact dual objective strictly below 41; exactification of
  every PSD and domain-nonnegativity condition.
- **Artifacts:** none yet.
- **Known counterexamples:** Solver status or near-PSD matrices are not
  certificates.
- **Restrictions:** Universal if the full three-point domain and all boundary
  cases are retained.
- **Status:** active.

## D. Rank-aware Gram matrices and nullspace/stress

- **Route:** Use \(G\succeq0\), `diag(G)=1`, \(G_{ij}\leq1/2\), and
  `rank(G)<=5` simultaneously through principal minors, stresses, spectral
  moments, Gale duality, low-rank completion, or sign/rank inequalities.
- **Proved lemmas:** A code exists iff such a Gram matrix exists; a hypothetical
  41-point matrix has nullity at least 36.
- **Unresolved:** Convert the large nullspace plus entry inequalities into a
  contradiction without assuming a contact pattern.
- **Artifacts:** none yet.
- **Known counterexamples:** Dropping rank admits irrelevant correlation
  matrices and cannot establish the geometric claim.
- **Restrictions:** None intended.
- **Status:** active.

## E. Contact graphs and rigidity

- **Route:** Derive universal consequences of first-order optimality only after
  proving the required maximality/rigidity hypotheses, and combine local
  contact links with stress identities.
- **Proved lemmas:** none beyond definitions.
- **Unresolved:** A contact lower bound or stress certificate valid for every
  maximum 41-point code, including flexible and degenerate cases.
- **Artifacts:** none yet.
- **Known counterexamples:** Maximum need not imply a prescribed graph;
  locally jammed does not imply globally maximum; known 40-point codes are
  nonunique.
- **Restrictions:** Potentially severe; every use must be audited.
- **Status:** active.

## F. Local cap, projection, and overlapping-link geometry

- **Route:** Condition on points, contacts, or small simplices; project to
  orthogonal complements; derive exact cap/link occupancy bounds and
  compatibility constraints between overlapping neighborhoods.
- **Proved lemmas:** elementary projection identities pending formal write-up.
- **Unresolved:** A global averaging or compatibility inequality that excludes
  total size 41.
- **Artifacts:** none yet.
- **Known counterexamples:** Averaging a weak isolated cap bound is insufficient.
- **Restrictions:** Case assumptions must cover boundary contacts exactly.
- **Status:** active.

## G. Semialgebraic exhaustive proof

- **Route:** Fix orthogonal gauge safely, describe a compact coordinate/Gram
  domain, and use exact rational interval branch-and-bound, Bernstein
  enclosures, CAD, or Positivstellensatz certificates.
- **Proved lemmas:** Compactness of \((S^4)^{41}\) ensures feasibility is attained
  when nonempty.
- **Unresolved:** A tractable complete branching scheme and independently
  checkable tree covering the continuous domain.
- **Artifacts:** none yet.
- **Known counterexamples:** Finite guessed combinatorial types or solver
  “infeasible” statuses are incomplete.
- **Restrictions:** Symmetry breaking must be proved safe.
- **Status:** active.

## H. Certified spherical-cell discretization

- **Route:** Partition \(S^4\) into cells with rigorous pairwise angle
  enclosures, map every continuous code to a graph/hypergraph object, and prove
  a clique/independence bound with boundary-safe coverage.
- **Proved lemmas:** none yet.
- **Unresolved:** Cell system fine enough to separate 40 from 41 while retaining
  a provable continuous-to-discrete implication.
- **Artifacts:** none yet.
- **Known counterexamples:** A heuristic mesh cannot rule out boundary or
  between-grid configurations.
- **Restrictions:** None if coverage is rigorous.
- **Status:** active.

## I. Classification-free universal inequalities

- **Route:** Seek moment forcing, rank-versus-sparsity, average-degree, or
  global consistency inequalities applying to every 41-point code.
- **Proved lemmas:** none yet.
- **Unresolved:** The separating inequality.
- **Artifacts:** none yet.
- **Known counterexamples:** All proposed statements must be tested against the
  four known 40-point configurations and randomized smaller codes.
- **Restrictions:** None intended.
- **Status:** active.

## J. Hybrid finite-list plus exact elimination

- **Route:** Use SDP/optimization to discover finitely many candidate local
  patterns, prove a completeness theorem with interval margins, then eliminate
  each candidate by exact algebra or a small certificate.
- **Proved lemmas:** none yet.
- **Unresolved:** A noncircular completeness mechanism.
- **Artifacts:** none yet.
- **Known counterexamples:** Enumerating guessed contact graphs is not complete.
- **Restrictions:** Depends on the eventual completeness theorem.
- **Status:** active.
