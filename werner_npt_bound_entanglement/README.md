# NPT Werner-state distillability

This directory contains a first-principles research program on finite-copy
distillability of the NPT Werner family.  No external literature or prior
research artifacts are used.

## Scope

For \(d\geq 3\), \(-\tfrac12\leq\alpha<-\tfrac1d\), and
\[
X_{\alpha,d}=I+\alpha d P_d,
\]
the target is to decide whether \(X_{\alpha,d}^{\otimes n}\) is
two-block-positive for every finite \(n\), or to give an exact finite-copy
Schmidt-rank-two witness whenever it is not.

## Directory layout

- `RESEARCH_LOG.md`: timestamped checkpoints, decisions, and obstructions.
- `notes/`: exact derivations and proof attempts.
- `discovery/`: exploratory code and outputs; never treated as proof.
- `verification/`: small deterministic exact verifiers for certified claims.

## Current exact reductions

The main proof notes establish the partial-trace formula, the sharp one-copy
theorem, endpoint parameter monotonicity, several all-copy no-go classes, and
an exact amplification theorem showing that orthogonal rank-two projections
suffice for the all-copy existence question.  The project has not yet
established either all-copy undistillability or a finite-copy distillation
witness; every note labels unresolved inequalities explicitly.

At three copies, the endpoint is now proved nonnegative for every
self-adjoint or normal rank-at-most-two coefficient matrix, and more
generally whenever the left and right singular planes coincide.  The
remaining nonnormal problem has exact three- and four-dimensional canonical
forms, recorded in `notes/agent_unrestricted_n3_selfadjoint.md`.  The
intersection-one stratum is equivalent to one explicit three-vector Gram
inequality; the transverse stratum is equivalent to a coupled
pseudo-Hermitian complex-structure inequality.  Neither remaining inequality
is presently claimed proved.
