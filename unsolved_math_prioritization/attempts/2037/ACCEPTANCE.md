# EP302 bounded acceptance report

## Accepted prior results

1. Cambie's set, consisting of the upper half and the odd integers at most
   N/4, is triple-free for three pairwise distinct positive integers. Its size
   is 5N/8 + O(1), so liminf f(N)/N >= 5/8 and the subsidiary conjecture
   f(N) = (1/2 + o(1))N is false.
2. Khanukov's corrected upper certificate and the audited disjoint-multiplier
   transfer establish limsup f(N)/N <= 140803024/163562355. The 10 October
   2026 audit independently regenerated or checked every required finite
   input exactly. The finite checker was separately authored; no upstream
   program or Lean development was executed. Edition preparation did not
   rerun those mathematical checks.
3. Khanukov's padding implication is correct for the exact structured
   witness stated in MATHEMATICAL_AUDIT.md section 5. The required upstream
   witness has all-distinct avoidance for all tail lengths at least two,
   points only in the specified odd low band or closed top half, and size
   at least (1/2 + rho_L/24)N for fixed parameters and all sufficiently large N.
   Padding gives (5/8 + rho_L/24)N - 1 and thus eventually 5/8 + delta with
   delta = rho_L/48 > 0, conditional on that witness.

These are assessments of credited prior work by Stijn Cambie, Dmitry Khanukov,
Donald Della Pietra, and the earlier authors cited in the full audit. No
novelty, priority, complete solution, exact limiting density, convergence, or
new explicit numerical lower improvement above 5/8 is claimed. This edition
is an AI-assisted, unrefereed audit, not a human referee report or journal
acceptance.

## H-L1/H-L2: unconditional lower acceptance remains on hold

H-L1 concerns independent mathematical closure of the upstream witness. The
complete required analytic estimates and uniform constants have not been
independently verified against a complete primary copy of Tenenbaum's cited
Theorem III.3.5, nor has the separate EP327 finite-sieve, centered-tail and
residual proof chain been audited end to end. The human manuscript and Lean
development use different quantitative routes and parameter values. Their
final existence statements must not be treated as interchangeable proofs.

H-L2 concerns formal reproduction. No local Lean build, full upstream source
rebuild, fresh Lean-kernel replay, or local transitive axiom-report reproduction
was performed. The successful exact-release public CI is author-side evidence.
The reported allowed axioms, propext, Classical.choice and Quot.sound, have
not been independently reproduced by this audit. Cached artifacts, toolchain,
Mathlib fork, OS and hardware remain disclosed trust boundaries. A fresh replay
through Lean's own kernel would not constitute a second kernel implementation.

Static lexical guards, matching interfaces, positive numerical margins,
finite proxy checks and author-side CI do not establish the missing closure.
The hold is not a counterexample and does not assert that the source theorem
itself is stated with an extra assumption. Clearing it requires a pinned full
formal replay with semantic checks and disclosed trust boundaries, or a complete
mathematical audit of an adequate upstream analytic route. Neither is supplied
here. The independent upper acceptance does not depend on clearing this hold.
