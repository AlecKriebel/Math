# Research log: positive-rank full-list terminals

## 2026-07-28 PDT

- Reconstructed the accepted C-149 restricted peeling, terminal gates,
  C-154 singleton-terminal exclusion, and C-157 rank-zero corridor lemma.
- Isolated the elementary positive-rank rule: every unbanned dominating
  successor to a deletion-witness attack has strictly smaller restricted
  rank.  Kept unrestricted greatest-family membership separate from
  restricted rank.
- Observed that a positive-rank terminal predecessor must have such an
  alternate to its terminal attack, because it survived the first
  restricted peeling round.  This conclusion is palette-free.
- Proved the corridor dichotomy.  A direct-root secondary response is
  retained and lower-rank; a nonroot secondary response is either
  lower-rank and dominating or nondominating with the C-157 private
  witness.
- Minimized terminal-predecessor rank for a fixed color.  This bypasses
  every nonsingleton direct-root terminal at every rank.  For a nonroot
  corridor, the exact remaining obstruction is a dominating lower-rank
  alternate that is absent from the unrestricted greatest family.
- Treated anchor restoration separately.  At positive rank, the old
  terminal vertex is forced to move to the attacked anchor; the resulting
  state dominates, avoids the ban, and has smaller rank.  This does not
  require the attacked anchor to occur in the terminal root palette.
- Combined the minimum-rank normal form with C-154: among one
  minimum-rank entry per annihilated color, at least one nonsingleton
  entry is nonroot or anchor-restoration, with four exact residual
  subbranches.
- Audited the named equality graph ``Ksv`f\knJVis``.  It has a genuine
  positive-rank anchor restoration whose retained alternate drops from
  rank one to rank zero.
- Scanned the fixed MMV Table 9 catalog as a discovery audit.  The
  MMV-006 graph ``JEhbtj{rvf?`` has a positive-rank nonroot secondary
  alternate that dominates and has lower restricted rank but is absent
  from the unrestricted greatest family.  MMV-007 ``JEhbtj{ruv?`` has an
  anchor-restoration terminal whose attacked anchor is absent from the
  root palette even though the physical move edge exists and the
  alternate is retained.  Both controls have \(\gamma=2\), so they delimit
  rank/fixed-point logic without refuting a future equality-specific
  lemma.
- Built a direct ordinary-bitmask replay that recomputes all four
  parameters, greatest kernels, ranks, palettes, transitions, and ban
  membership for the three named controls.  The strict control replay
  passes.
- No graph nonedge was inferred from a missing family transition.

## Open

- Prove under \(\gamma=3\) that a lower-rank dominating corridor alternate
  is retained, or else forces a dominating pair.
- Eliminate the rank-zero anchor-restoration branch using the equality
  hypothesis.
- Obtain hostile review before promoting any theorem from this directory.
