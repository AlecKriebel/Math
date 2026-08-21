# Research log

## 2026-08-21 — Frozen-parent reconstruction and five-port start

- Restricted all new work to `work/restoration_forest/`; the v4 referee
  package is treated as immutable input.
- Reconstructed the 997 canonical `restoration_parent` records from the six
  frozen residual manifests.
- Correlated role-specific attachment rows by the exact tuple
  `(source_index, canonical_class_id, target_index, port_match)`.  This gives
  exactly 2,540 physical member/root presentations and no missing or
  contradictory role attachment.
- Found a load-bearing correction to the provisional census: 568 members have
  one dummy role, 1,260 have two, and 712 have three.  The 712 three-role
  cases are marginalized-incoming completions with a two-edge minimum repair.
  Direct replay of `target_completions(4, ...)` agrees exactly with every
  manifest role union.  Thus a literal one-role-at-a-time forest can reach
  seven selected ports, unless a separate theorem removes the incoming role
  before this forest is invoked.
- The 2,540 roots issue 5,224 role restorations.  Each frozen source has seven
  admissible first insertion edges, hence the complete raw five-port layer has
  36,568 transported child presentations.
- Best-guess completion: **20%** for the restoration-forest computation and
  **0%** for a theorem-level restoration closure from this workspace alone.

## 2026-08-21 — Five-port forest terminates at its first layer

- Generated all 36,568 raw first children with coherent source insertion,
  restored-role-to-label-4 transport, target attachment, port match, and
  remaining-role list.
- Corrected canonicalization uses the exact labelled mixed-graph incidence
  expansion, including endpoint arrowheads.  A Weisfeiler--Lehman digest is
  used only as an acceleration bucket; exact graph isomorphism decides class
  membership.  The layer has 35 source classes, 314 target classes, and 2,240
  directed relation classes.
- Proof-first topology closes 36,404 raw children: 35,758 by a displayed
  quartet mismatch and 646 by the strict K2P tree--sunlet sign theorem.
- Of the 164 equal-deck cases, 148 are separated by exact full five-port
  multihomogeneous quadratics.  The remaining 16 form one
  `theta1 -> theta3` family (source rank 16, target rank 18); twelve still have
  one role and four are fully restored.  Every one is separated by an exact
  lift of the already certified four-port `F_(2,112)` quartic on a selected
  quartet.  Target pullbacks vanish identically, source pullbacks are nonzero
  with 32, 96, or 342 terms, and strict rational `D_+` witnesses are retained.
- Final first-layer status is `separated=36,568`, `isomorphic=0`,
  `triangle=0`, `unresolved=0`.  Because every child is terminal, no depth-2
  or depth-3 state is generated despite the genuine three-dummy roots.
- Full regeneration reproduced the certificate byte for byte.  The saved
  certificate SHA-256 is
  `dc3a3f68c1d8c347ac196de1cd802fd6cd4895a5e007c87c79431a89bd191fb9`;
  its mathematical payload SHA-256 is
  `ff7c7563958c2c73e77d94f6757700819c0513393066ef22e64976a598e25fc3`.
- Five adversarial mutations were rejected after recomputing outer hashes:
  one quadratic coefficient, one quartic coefficient, remaining-role
  transport, Python optimized mode, and a topology-only raw child hash.
- Conditional theorem consequence: once the paired marginal open-image and
  restoration implication are invoked, all 997 four-port restoration parents
  are impossible, since any actual restored role must produce one of the
  exhaustively separated children.
- Remaining theorem-level blocker: this workspace does not itself reprove the
  marginal/restoration implication, the primitive/raw topology universe and
  rank-exclusion ledger, or the global bridge/gluing/genericity arguments.
- Best-guess completion: **100%** for the frozen 997-parent direct-child
  forest and **35%** for promoting it to a globally integrated restoration
  theorem, because the logical upstream and downstream gates remain external.
