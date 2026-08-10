# Preserved n=4 theta-2 rooted-state identity failure

Status: **EXACT IMPLEMENTATION FAILURE — QUARANTINED**

The completed primary `n=4` theta-2 run was not a valid theorem certificate.
Its canonical restoration state used only semi-directed mixed codes (together
with restoration metadata) as identity.  Distinct rooted realizations can
have the same reduced mixed code.  The run consequently merged presentations
for which a raw coverage record's `target_graph_id` differed from the
canonical state's `target_graph_id`.

That is not harmless deduplication.  The next restoration step and the
terminal `p/q` arc families are functions of the exact rooted source and
target graphs.  Reusing one child set across two such rooted presentations can
omit valid children, add invalid children, or bind a correct polynomial to the
wrong directed relation.

The quarantined bytes must never be consumed by a release verifier.

The independent terminal-extension schema therefore requires state identity
to contain all of:

1. `fixed_full_root_case_id`;
2. exact source rooted-graph content hash;
3. exact target rooted-graph content hash;
4. raw terminal and parent-path identity; and
5. the fixed physical port matching.

It also regenerates the full Cartesian child set separately for every raw
path-bound parent.  The declared `p_child_relation_ids` and
`q_child_relation_ids` must equal that regenerated set exactly.  Canonical
child graph or algebra bodies may be content-addressed, but raw parent-child
bindings may not be merged.

`mutation_tests.py` preserves two regressions:

- `cross_root_case_state_merge`; and
- `borrowed_or_truncated_per_path_child_set`.

Both must be rejected before any final `n=3+n=4` stream can pass this gate.
