# Research log

## 2026-07-28 PDT

- Started from accepted C-108, C-132, and the hostile-passed C-139
  anchorless component theorem.
- Observed that every physical-link state \(T_{bc}=\{x,b,c\}\) shares
  \(x\) with every other such state.  Applying C-108 with target \(s_i\)
  makes the \(x\)-response at \(s_i\) global across all link components.
- Applied the accepted family-response Hall theorem at \(T_{bc}\) to the
  outside independent triple \(S\).  Its three response lists must cover
  all three guard positions \(x,b,c\), so the global reverse-color set is
  nonempty.
- Derived the exact response-row identity
  \[
  L_{T_{bc}}(s_i)=
  (\{x\}:i\in R)\cup(\{b\}:i\in P(c))
  \cup(\{c\}:i\in P(b)).
  \]
- Tested the hoped-for coloring implication on the accepted equality
  control `Ksv`f\knJVis`.  At root \(S=\{1,2,3\}\), target \(x=0\), all
  three colors are reverse colors, but only anchor color 2 is feasible
  for \(x\).  This refutes reverse-color sufficiency even with
  \(\gamma=i=\alpha=\gamma^\infty=\theta=3\) and the greatest family.
- Recomputed the natural color-restricted greatest kernels.  False reverse
  colors 0 and 1 have empty restricted kernels after deletion rounds
  \(16,40,56,12\); color 2 leaves 64 states after rounds \(16,32,13\).
  This proves that the missing property is future-stable coinductive
  selection, not another one-step link condition.
- Proved that every feasible target color belongs to the reverse set and
  passes the restricted-kernel gate when the literal greatest family is
  used.  The proof embeds the clique-fiber eternal family supplied by a
  proper coloring.
- Replayed all connected unlabeled graphs through order nine: 273,193
  graphs, 1,538 equality-three graphs, and zero full incidences.  This is
  OBSERVED only and is vacuous for the new reverse-color claim.
- A radius-two labeled toggle probe around the order-12 control tested
  2,212 graphs; 232 retained static and eternal equality, but only the
  base graph retained the specified full incidence.  This is exploratory
  only.
- Froze the human note, deterministic probe, compact control and census
  results, and replay script.  No universal resolution is claimed.
