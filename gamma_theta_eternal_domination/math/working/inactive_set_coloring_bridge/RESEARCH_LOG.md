# Research log: inactive-set coloring bridge

## 2026-07-28 PDT

- Independently reconstructed vertex-star propagation from two literal
  one-guard attacks.
- Proved the exact component identity
  \(A_C^\kappa=[3]\setminus\kappa(R\cap\operatorname{supp}C)\).
- Used well-coveredness of the equality deletion to prove the global
  identity
  \(\bigcap_C A_C^\kappa=[3]\setminus\kappa(R)\).
- Derived the exact constrained-coloring target and the unconditional
  triangle-free theorem for \(H'[R]\).
- Found an initial eight-vertex static equality graph with inactive
  \(C_5\), but rejected it as the principal control because its prescribed
  active pattern violates ridge covariance.
- SAT-synthesized the sharper 11-vertex deletion control
  `JUZeppVvS^_`.  It has all equality parameters equal to three, an
  inactive induced \(C_5\), a full active root facet, and exact
  componentwise covariance.
- Added target 11 to obtain `KUZeppVvS^_~`.  Every prescribed target
  response is statically legal and dominating, but the eternal
  triple-kernel is empty.  Exact parameters are
  \((3,3,3,4,4)\).
- Wrote and ran the standalone verifier.  `control_result.json` has
  SHA-256
  `1a891b0e65fd8ef363007869ad3797191b8fca96912e11a1b41ab02d82fd2faa`.
- In bounded exploratory searches over at least 70,000 random tripartite
  candidates (with exact equality filters), found no actual proper
  eternal-family full-target control whose inactive set necessarily uses
  all three colors.  No exhaustive claim is made.
- Frozen conclusion: static equality and one-step response data are
  insufficient.  The live proof target is a genuinely multi-step closure
  theorem ruling out covariant inactive odd cycles or otherwise producing
  a deletion coloring with at most two colors on \(R\).
