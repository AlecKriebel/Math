# Research log: paired-repair implication descent

## 2026-07-28 PDT

- Read the accepted minimal-2-CNF, physicalization, virtual-rainbow,
  chirality, boundary-parity, and three-gate witness notes before fixing
  the target.
- Proved the exact oriented replacement formula
  \(|P'|=|P|-d+2\).  This preserves the opposite contradiction path but
  gives strict descent only when the replaced segment has more than two
  arcs.
- Identified the physical-support gap: Boolean endpoint units obtained by
  resolution are not unit clauses, singleton response lists, or the
  common-terminal fan required by C-079.  C-094 cannot repair this because
  C-095/C-098 delimit clause-edge transport.
- First built a four-variable abstract odd-XOR control in which the
  two-clause almost-cap subdivision ties the original core size and leaves
  an inclusion-minimal unit-free bicycle.
- Strengthened the control with direct one-guard synthesis.  Starting from
  the complete three-gate \(012\), length-\((1,1,1)\) odd boundary, forced
  one selected critical pair to have a common complement neighbor while
  omitting the global \(\gamma\geq3\) condition.  A one-spare-vertex model
  exists with all outside response lists exact two-lists.
- Replaced the solver-selected family by the canonical greatest closed
  subfamily subject to the same forbidden direct swaps.  It has 703 states,
  deletion rounds \(51,37,63,29,10\), and exact family hash
  `c116c4a60299fea35d30bf09bda9b1faa31b39533caac8eb265818cd1347874d`.
- Reconstructed the response 2-CNF independently.  Its two almost-cap arm
  clauses resolve to an already essential clause supported by a different
  physical edge.  The unique minimum core has nine clauses; the unique
  minimum inclusion-minimal core containing both arms has ten and is the
  one-clause subdivision of the former.  Both are syntactically unit-free.
- Added `verify.py` and frozen `result.json`.  The clean run checks the
  graph6 record, exact parameters
  \((2,2,3,3,3)\), 11,248 one-guard obligations, response formula, core
  minimality, and marked path lengths.
- **Conclusion:** the proposed paired-repair lemma is not proved and its
  local/shortest-path form is refuted.  A gamma-three proof must use common
  witnesses for additional pairs or a new physical terminal-support
  theorem.  The gamma--theta conjecture remains open.
