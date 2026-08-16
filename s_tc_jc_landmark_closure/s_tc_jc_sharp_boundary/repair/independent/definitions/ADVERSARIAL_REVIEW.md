# Independent adversarial review of the definitions gate

Date: 2026-08-09  
Mode: separate ephemeral Codex process, read-only sandbox, no browsing  
Inputs: `DEFINITIONS_GATE_REVIEW.md`, the independent validator, the candidate
closure note, and the local primary-source texts

## Findings

### P0 — the closure note narrows “2-sub-blob” without proving equivalence

Brits defines a 2-sub-blob by connectedness, absence of globally cut internal
edges, and exactly two vertices of `W` adjacent outside.  It does not require
exactly two external incident edges.  Closure-note §3 instead proves the
stronger operational claim with exactly two external attachment edges.

The independent reviewer reproduced the 4-sunlet witness: `W={v0,v1}` has two
boundary vertices but four external edges, while the ambient topology is
binary, simple, level one, and strongly tree-child.  Contraction gives degree
four.  This is a source-definition inconsistency, not a JC model
counterexample.

### P0 — broad reduction and “all preimages” `S_TC` are incompatible

Brits' reduction exhaustively removes root-created parallel and degree-two
artifacts.  Englander's local strongly-tree-child criterion is tied to the
narrower reticulation-preserving reduction with no parallel semi-directed
network admitted.  The validator's LSA-valid non-tree-child level-2 rooted DAG
reduces broadly to a plain two-leaf edge, confirming that arbitrary broad
preimages cannot be used to define `S_TC` while retaining the local criterion.

### P1 — the `K4-e` conclusion survives; the prose contains an unnecessary
external-root subcase

The reviewer independently accepted the exact-two-edge cyclomatic argument:
the proper case forces a forbidden parallel pair, and the whole rank-two case
is uniquely `K4` minus the boundary edge.  The 25 LSA-valid rooting records all
fail tree-childness.  Nonadjacent attachment reticulations occur only in the
five internal-root records; the external-root discussion in the closure note
is therefore not the clean surviving case split.

### P1 — the proposed class is a real scope restriction

Separating narrow `sd_0` rootings from broad cleanup and defining an
operational two-edge suppression class is a defensible repair.  It must be
presented as a narrowed theorem scope, not as equivalent to the literal
prior-work definition.

## Surviving conclusions

- No exact-two-external-edge operational suppressible gadget occurs in the
  simple binary narrow-standard `S_TC` level-2 class.
- The 4-sunlet refutes “two boundary vertices implies two external edges,”
  but does not itself refute a JC model theorem.
- The complete `K4-e` rooting census has 25 LSA-valid presentations and zero
  tree-child presentations.

The independent reviewer found no additional mathematical defect in the
cyclomatic proof or finite rooting interpretation beyond the convention and
scope defects already recorded in the gate report.

