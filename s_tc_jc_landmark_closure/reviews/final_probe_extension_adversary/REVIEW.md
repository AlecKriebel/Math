# Adversarial terminal-extension review

## Status

**EXACT REVIEW IMPLEMENTATION PASSES; FINAL THEOREM STREAM AUDIT PENDING.**

This is intentionally not an Outcome-P promotion.  The final regenerated
`n=3` and `n=4` raw path-bound terminal streams have not yet been supplied to
this reviewer.  The prior completed `n=4` theta-2 run is quarantined because
it merged distinct rooted states under one semi-directed state key.

## What is independently implemented

No module in this directory imports `primary/` or
`reviews/final_hard_cover_cleanroom/`.  The reviewer independently implements:

- rooted binary and tree-child validation;
- LSA filtering and enumeration of all admissible rootings;
- locked standard semi-directed root suppression;
- exact labelled mixed-graph isomorphism and ordinary `T` maps;
- undirected bridge detection and admissible internal blob arcs;
- exact `p`, then `q`, insertion and deletion;
- one record for every raw parent and every source-target arc pair;
- parent-restricted coherent isomorphism/`T` transports;
- displayed-switching enumeration and descendant masks;
- all fifteen four-state JC quartet orbit coordinates as sparse integer
  polynomials;
- exact invariant substitution and pullback hashing;
- source-relative algebraic separators;
- exact modular Jacobian minors together with independently checked structural
  upper bounds; and
- per-path child-set regeneration.

## Exact development certificate

The deterministic fixture is a standard-strong three-port triangle identity
terminal.  The full extension contains:

| object | exact count |
|---|---:|
| raw base terminals | 1 |
| ordered `p` relations | 9 |
| allowed `p` relations | 3 |
| ordered `q` relations | 48 |
| allowed `q` relations | 12 |
| distinct ranked child graphs | 15 |

Every unequal relation has a regenerated target-zero/source-nonzero JC
quartet invariant.  Every allowed relation has a labelled isomorphism or
ordinary-`T` map restricting to its parent map.  Every modular lower rank
equals the exact level-one cycle upper bound.

The fixture certifies the implementation and schema only.  It is not a
substitute for the final hard-cover relation universe.

## Preserved primary failure and stronger identity

The quarantined `n=4` stream demonstrated that semi-directed mixed codes are
not a sufficient restoration-state key.  A canonical state merged raw
records with different rooted `target_graph_id` values.  The independent
schema now requires:

```text
fixed_full_root_case_id
+ exact source rooted graph id
+ exact target rooted graph id
+ raw path id
+ physical port matching.
```

It separately recomputes `p_child_relation_ids` and
`q_child_relation_ids` for every raw parent.  Equal mixed codes authorize no
cross-root or cross-rooted-graph merge.  See
`PRESERVED_PRIMARY_N4_ROOTED_STATE_IDENTITY_FAILURE.md`.

## Mutation results

All eight required or strengthened mutations are rejected:

1. altered physical port correspondence;
2. wrong parent relation;
3. inconsistent child `T`/isomorphism map;
4. dropped admissible insertion arc;
5. duplicated decorated relation;
6. valid graph polynomial attached to the wrong relation;
7. cross-root-case state merge; and
8. borrowed or truncated per-path child set.

## Release gate

The final gate passes only when both regenerated `n=3` and theta-2 `n=4`
seed streams:

1. contain one seed per raw path-bound allowed terminal;
2. use the stronger rooted state identity;
3. produce no unresolved `p` or `q` relation;
4. pass `verify_probe_extension.py` without exclusions;
5. have exact rank upper certificates supported by the final local atlas;
6. survive all mutations; and
7. agree record-for-record with the separately written clean-room producer
   after normalization.

Until then the precise verdict is:

> **The terminal-extension construction is independently implementable and
> mutation-sensitive, but the arbitrary-subdivision gate for the landmark
> theorem remains UNRESOLVED on the actual final relation streams.**
