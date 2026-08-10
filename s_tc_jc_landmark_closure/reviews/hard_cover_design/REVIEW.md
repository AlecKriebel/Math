# Hard Cover Design Review

Status: **FINAL, SCOPE-LIMITED DESIGN AUDIT**

Date: 2026-08-10

Write scope: `reviews/hard_cover_design/` only.  No primary file was edited.
No compiler census output was used as mathematical evidence.

## Executive Verdict

The sequential dummy-restoration design is **VERIFIED only in the fixed-full
relation sense**:

Given one already fixed full labelled source-target relation, every omitted
target dummy role is a real unselected boundary of that same full relation.
The source support already contains all source sink roles, so each such
unselected source boundary must lie on an ordinary directed source segment.
The recursion in `primary/hard_cover_compiler.py` inserts each restored label
in every source segment position and carries the resulting words forward.
Thus the actual fixed relation determines one coherent root-to-leaf path in
the restoration tree.

The stronger interpretation is **FALSE**:

Selected marginal containment does not by itself lift to containment after
restoring a hidden target boundary and choosing a source placement.  The exact
counterexample is
`counterexamples/unconditional_lift_failure.json`.  Therefore the hard cover
must be promoted only after finite-union logic has selected one target
presentation on a source-open subgerm of one fixed full relation.

## Status Ledger

| Claim | Status | Conclusion |
|---|---|---|
| Fixed-full sequential restoration is exhaustive | **VERIFIED** | Conditional on one fixed full labelled source-target relation and enough actual unselected source labels, the actual relation appears as one restoration path. |
| Unconditional selected-marginal lift | **FALSE** | Selected equality after projection can coexist with restored full separation. |
| Degree mismatch when source lacks enough extras | **VERIFIED** | It is vacuous for fixed-full comparison: the two full factors do not have the same boundary set. It must not be counted as a separated branch. |
| Every omitted target role type | **VERIFIED** | The grammar has `D_REPAIR`, `D_SINK`, and marginalized `INCOMING`; no other core-restoring dummy role is present. |
| Source extras cannot be sinks | **VERIFIED** | Source support generation selects every source path sink as `Q_SINK`; later extras are segment subdivisions only. |
| Submersion of each prefix probe | **VERIFIED** | For a fixed prefix, physical edges map onto descriptor edge classes by disjoint products with full-rank differential on the open cube. |
| Deterministic dummy-restoration order | **VERIFIED** | Sorting by `natural` and using `remaining[0]` fixes an order; all later labels are inserted in all relative positions. |
| Finite-union logic as emitted artifact | **UNRESOLVED** | The defensible statement is source-open subgerm containment in one finite member. The artifacts do not bind a whole focal germ to one member. |
| Generic polynomial separation direction | **VERIFIED** | `source_signature & ~target_signature` is a target identity with nonzero source pullback, excluding full-dimensional source containment. |
| Strict-sign separation direction | **VERIFIED** | `target_signature & ~source_signature` is used only when the source pullback is zero and the target pullback is strictly signed on the open cube. |
| Same-sign quick sign is complete | **UNRESOLVED** | It is sound but only sufficient; terminal mixed-sign survivors need the factor/Bernstein pass or remain unresolved. |
| Terminal `T` quotient suffices for topology conclusion | **VERIFIED** | At full restored terminal states, equal labelled `t_quotient` codes prove isomorphism modulo ordinary triangle redirection. |
| Terminal `T` quotient proves stochastic equality | **FALSE** | The locked definition treats ordinary `T` as a topological quotient, not an equality theorem for complete JC images. |
| All probe paths are artifact-bound to one full relation | **UNRESOLVED** | The recursion is coherent along each path, but canonical deduplication does not emit an explicit full-relation or parent-prefix binding. |

## Detailed Audit

### 1. Fixed-Full Exhaustiveness

The restoration recursion chooses

```text
role = remaining[0]
label = L_{current_p}
```

then restores that target role and inserts the same label into every source
segment position.  The next recursive call receives the extended source word,
so a root-to-leaf path is a single coherent word tuple, not independent
one-label probes.

For a fixed full labelled relation, let `D` be the target dummy roles omitted
from the selected target probe.  Each element of `D` is an actual boundary
label of the full target.  Since the source and target full factors are being
compared on the same labelled boundary set, the same physical label occurs in
the source full factor.  The rigid source support contains every source sink,
so an unselected physical label cannot be a source sink.  It lies on some
source segment with a definite order relative to the selected source labels.
The recursion enumerates that position at the corresponding prefix.

If the source full factor has fewer unselected labels than `|D|`, there is no
fixed full relation with the same boundary set.  A compiler may still generate
formal source extensions, but those are over-approximating branches and cannot
serve as evidence against a smaller selected marginal.

### 2. Target Dummy Roles

The completion grammar creates exactly the omitted roles needed to make a full
standard-strong target witness:

- `D_REPAIR_*`: one dummy on a chosen minimum-repair segment that has no
  selected ordinary label.
- `D_SINK_*`: one dummy for each omitted reticulation sink child.
- `INCOMING`: the structural incoming boundary when it is marginalized.

Additional omitted ordinary ports on an already occupied segment are not
dummy roles.  They have the same complete switching-mask row as adjacent
serial edges and are absorbed into a path product at the selected tensor
level.  They must still be handled by the separate arbitrary-word/probe
coherence argument.

### 3. Source Extras

The source support generator labels every core path sink as `Q_SINK` before
adding any extras.  Extras are generated only by choosing segment indices and
inserting `P_i` into segment word lists.  Consequently, in the hard-cover
restoration stage a restored target dummy can be inserted only as a source
ordinary subdivision.  That is correct for fixed-full relations because source
sinks are already in the selected source support.

### 4. Submersion

For every prefix probe, the selected descriptor has one effective edge
coordinate for each complete displayed-switching mask-row class.  The map from
physical edge multipliers in a class `C` is

```text
y_C = product_{e in C} x_e.
```

The `C`-row differential is supported only on variables in `C` and has
strictly positive entries on `(0,1)^E`; distinct classes are disjoint.  Thus
the product map has full row rank and is onto the effective open cube.
Reticulation choice flips are permutations or `lambda -> 1-lambda`.  This
verifies submersion for fixed prefix probes without relying on hard-cover
census output.

### 5. Finite-Union Logic

The valid finite-union statement is:

If a regular source germ is contained in a finite union of target
semialgebraic members, at least one member contains a relatively open
full-dimensional source subgerm.

The invalid statement is:

The entire focal source germ lies in one fixed member, or selected marginal
containment automatically lifts to a restored full-boundary containment.

The exact counterexample in
`counterexamples/unconditional_lift_failure.json` shows why the lift is false:
`S0 = T0 = (0,1)` after projection, while restored sets
`S1: a+b-1=0` and `T1: b-a=0` meet only at `(1/2,1/2)`.

### 6. Separation Directions

The generic polynomial direction is correct.  If a bit lies in
`source_signature & ~target_signature`, then the target pullback is the zero
polynomial and the source pullback is not.  A source-open full-dimensional
germ cannot lie inside that target identity.

The strict-sign direction is also correct.  If a bit lies in
`target_signature & ~source_signature`, the source satisfies the invariant
identically.  It separates only when the target pullback is certified strictly
positive or strictly negative on the entire target open cube.  The current
`quick_power_sign` certificate is sound for same-sign sparse power
coefficients, but incomplete.  Any terminal mixed-sign target-only survivor
requires the existing factor/Bernstein method or must stay unresolved.

### 7. Terminal Topology

At a terminal state, all target dummies for that completion have been restored.
If the source and target labelled `t_quotient(sd0(...))` canonical codes agree,
then the restored topologies are isomorphic modulo ordinary triangle
redirection.  That is sufficient for the stated topological conclusion.

It is not a stochastic equality certificate.  The locked definitions explicitly
do not claim ordinary `T` preserves complete stochastic JC images.  Hard-cover
promotion should phrase this endpoint only as "allowed topology modulo `T`."

### 8. Probe-Path Coherence

The recursion itself is coherent along one path because each child receives
the parent's extended source word and restored target-role map.  However, the
emitted state identity is canonicalized by source code, target code, remaining
roles, and port matching.  It intentionally merges multiple raw coverages.

That deduplication is fine for classifying a canonical state, but the artifact
does not by itself prove that all prefix states and separate support-plus-one
or support-plus-two probes used in an arbitrary-word promotion refer to the
same full source-target relation.  A promotion-grade certificate should carry
an explicit `full_relation_id`, `parent_state_id`, sorted dummy order, restored
role-to-label map, and source full word tuple for every emitted state.

## Required Corrections Before Promotion

1. State the hard-cover theorem with the fixed-full relation precondition.
   Do not phrase restoration as a lift of selected marginal containment.
2. Treat "source lacks enough extras" as a vacuous boundary-set mismatch for
   fixed-full comparison, not as algebraic separation evidence.
3. In the finite-union step, use "one source-open full-dimensional subgerm in
   one member"; do not claim a whole focal germ lies in one member.
4. Add artifact-level binding fields for full relation and parent prefix
   coherence before using the records in arbitrary-word promotion.
5. Run a factor/Bernstein sign pass on any terminal target-only mixed-sign
   candidates; otherwise leave them `UNRESOLVED`.
6. Phrase terminal equality as isomorphism modulo ordinary `T`, not as complete
   JC image equality.

## Auxiliary Artifacts

- `claims.json`: machine-readable status ledger.
- `counterexamples/unconditional_lift_failure.json`: exact algebraic failure
  of unconditional selected-marginal lifting.
- `source_hashes.json`: audited source byte hashes.
- `structural_audit.py`: independent verifier; imports no primary module.
- `make_manifest.py`: deterministic manifest generator/checker.
- `verify_all.sh`: one-command verifier for this review.
