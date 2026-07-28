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
