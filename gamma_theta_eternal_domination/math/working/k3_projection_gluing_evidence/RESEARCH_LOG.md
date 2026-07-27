# Research log: \(k=3\) projection gluing

## 2026-07-26 PDT — initialization

- Read the four prerequisite attack notes and their hostile reviews in full.
- Isolated the candidate exact gluing formalism: one Boolean orientation
  variable per connected component of each missing-color bipartite
  projection, unit constraints at singleton-list vertices, and one binary
  conflict clause for each complement edge whose endpoint lists have no
  common omitted color.
- Began a labelled \(2^{11}\)-graph order-eight extension test of the mixed
  \(P_4\) with its equality-forced middle-pair witness.  The test deletes
  exactly the six forbidden one-swap states and computes the greatest
  remaining eternal triple-family.
- Best-guess completion toward this assigned projection-gluing question:
  **35%**.

## 2026-07-26 PDT — parity reduction and dynamic countermodel

- Proved the exact no-full-list reduction.  After fixing one bipartition
  coordinate on every connected component of every frozen-color projection,
  the only choices are component flips.  Singleton lists give unit parity
  equations.  A complement edge between two distinct two-lists gives the
  single 2-CNF clause forbidding both endpoints from choosing their shared
  color.  These constraints are satisfiable if and only if the three
  bipartitions glue to a global family-response list coloring.
- Identified the two exact obstruction forms: an inconsistent parity path
  inside one projection, or a contradictory implication cycle in the
  cross-projection 2-SAT instance.  The mixed \(P_4\) is the smallest
  two-unit/one-clause certificate.
- Proved that a successful family-compatible coloring transports across a
  ridge by response covariance and keeps the underlying clique partition
  unchanged.  Covariance therefore preserves *existence* of a gluing but
  does not force one to exist.
- Exact named tests:
  `FCZbg` has two gluing solutions; the specified `FCXfO` family and
  `FCpbO` each have one; the specified `FDzro` family has none; the
  greatest `FDzro` family has two full-list vertices invisible to the
  projection formula but eleven direct list colorings.
- Constructed graph6 `HDzruf]`, a nine-vertex exact full-closure extension
  of the mixed \(P_4\) by the dual deficient-pair vertices \(w,y\).  Its
  explicit 46-state family passes all 276 attack obligations and has lists
  \(\{a\},\{a,c\},\{b,c\},\{b\},\{a,b\},\{a,b\}\).  Thus even the
  \(W/Y\) dynamics and every applicable covariance coexist with failed
  gluing.  Its parameters are
  \((\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3)\), so it isolates
  \(\gamma=3\) as the still-essential hypothesis.
- The complete labelled order-eight extension scan found no equality
  realization.  The complete labelled order-nine scan with a designated
  middle-pair witness and one arbitrary extra vertex likewise found none,
  even for proper families via the greatest safe fixed point.  These are
  lightweight observations, not coverage claims.
- Best-guess completion toward this assigned projection-gluing question:
  **78%**.

## 2026-07-26 PDT — final checkpoint

- Wrote `math/working/k3_projection_gluing.md` with the exact 2-SAT theorem,
  implication/parity obstruction certificates, ridge-stability theorem,
  full-list boundary, named stress tests, explicit `HDzruf]` countermodel,
  and a precise equality-sensitive stop gate.
- Replayed the evidence script from a clean invocation.  It verifies all
  named family obligations, the direct list-coloring counts, the 46-state
  countermodel, and the order-eight/order-nine extension counts.
- A separate collaborating lane independently decoded `HDzruf]`,
  reconstructed the same 46-state greatest safe family after the six bans,
  replayed all 276 obligations, recomputed its lists and parameters, and
  found no defect in the edge audit of the 2-SAT theorem or the
  non-automorphism handling in the ridge theorem.
- Hostile review accepted the proofs and exact checks with one qualification:
  the two unsatisfiable countermodels contain no independent-state ridge
  pair, so covariance is vacuous there.  The main note now states this
  explicitly and makes no nonvacuous negative claim about covariance on an
  unsatisfiable gluing instance.
- `git diff --check` passes on every file in this effort.
- No central campaign registry, state, README, manifest, or claim file was
  edited.  No order-14 computation was run.
- Best-guess completion toward this assigned projection-gluing question:
  **100%**.
