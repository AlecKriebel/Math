# Research log: nonsingleton full-list terminals

## 2026-07-28 13:14 PDT

- Opened the hostile-passed singleton-terminal theorem and review, C-141
  exact response-row structure, C-142 equality control, and C-149 terminal
  descent.
- Exact residual under study: all three color-restricted kernels are
  empty and one selected terminal state \(S-u+r_u\) per color has
  nonsingleton terminal root palette.  Primary subcase: all three entries
  are nonroot corridors.
- The order-12 C-142 control permits no one-color or two-color corridor
  elimination: both empty colors have only nonroot-corridor terminal
  entries, all with two-element palettes.  Any strict contradiction must
  use a genuine three-color interaction.

## 2026-07-28 13:22 PDT

- Corrected a notation collision.  The terminal palette used here is
  \(Q(z)=L_S^{\mathcal F^\star}(z)\).  The C-139/C-141 physical-link
  palette records different triples \(\{x,s_i,z\}\) and cannot be
  substituted for \(Q\).
- **OBSERVED only:** the seven-vertex terminal-cube checker leaves all 26
  singleton/doubleton patterns except the already excluded all-singleton
  pattern locally satisfiable.  A separate local scan also realized every
  choice in which all three own-color palettes have size at least two.
  Hence terminal-state incidence alone cannot settle the residual branch.

## 2026-07-28 13:28 PDT

- **OBSERVED boundary:** MMV-001 (`IEhbtj{ro`) has three empty restricted
  kernels and a cyclic triple of doubleton corridor terminals, but
  \(\gamma=2\).  The secondary alternate in each row is nondominating,
  with the missed witnesses cycling through the other movers.
- Exhausted the 1,024 one-vertex extensions of this named graph and found
  no extension preserving the named full-root incidence together with
  the equality parameters and all three empty kernels.
- A more permissive local repair that only joins a new vertex to the
  isolated physical-link vertex leaves five local eternal models; all
  still have a dominating pair.  Thus the no-isolate consequence of
  \(\gamma=3\) does not by itself close the corridor triple.

## 2026-07-28 13:34 PDT

- Found the exact equality graph
  `OQifur}UO]}iTij]tpo}v`, root \(\{0,1,10\}\), target \(6\).
  It realizes three distinct cyclic doubleton nonroot-corridor rows:
  \(Q(11)=\{0,1\}\), \(Q(7)=\{1,10\}\), and
  \(Q(5)=\{0,10\}\).
- Colors \(0\) and \(10\) have empty restricted kernels and explicit
  rank-one to rank-zero to ban traces.  Color \(1\) has a 150-state
  kernel: its secondary color-\(10\) response is dominating and survives.
  This is an exact sharp control against rank-free/static elimination,
  not an all-three-empty example.

## 2026-07-28 13:46 PDT

- Proved the rank-zero secondary-response lemma.  A direct-root terminal
  at rank zero must have singleton palette.  In a nonroot corridor, every
  secondary palette color gives a legal nonban alternate; at rank zero it
  must be nondominating and therefore has a locally collision-free missed
  witness.
- Audited the C-149 quantifier carefully: a descending trace may enter the
  ban from positive rank.  The lemma and its direct-root exclusion are
  therefore stated only for rank-zero final predecessors.  Positive-rank
  nonsingleton entries remain open.
- Froze the symbolic lemma and equality boundary as a candidate with a
  standalone bit-mask verifier and an explicit collision/occupancy audit.
