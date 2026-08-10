# Self-contained probe-extension relation schema

The top-level JSON object has:

- `schema = "stc-jc-probe-extension-review-v1"`;
- `base_relations`: raw path-bound allowed terminals;
- `p_relations`: every ordered source/target internal-arc insertion;
- `q_relations`: the same construction over every allowed `p` parent; and
- `rank_records`: graph-bound exact modular Jacobian records.

Every rooted graph is encoded by `root`, directed `arcs`, and a vertex-to-label
map `labels`.  Vertices are integers and labels are strings.  Reticulations
are inferred from indegree two.

Each base relation records all load-bearing provenance:

- `relation_id`, `raw_terminal_id`, `restoration_root_id`, and
  `parent_path_id`;
- `fixed_full_root_case_id`, exact source and target rooted-graph hashes, and
  a `state_identity_sha256` over this stronger identity;
- `Q_s`, `Q_t`, and the physical `port_matching`;
- source and target rooted graphs;
- `classification` in `{labelled_isomorphism, ordinary_T}`; and
- one explicit standard-mixed-graph `transport`.

Each child additionally records:

- the exact `parent_relation_id`;
- insertion `level` (`p` or `q`), `new_label`, `source_arc`, and `target_arc`;
- the complete child graphs;
- source and target inclusion/deletion maps;
- copied base provenance and transport restriction;
- a classification; and
- for a separated relation, a graph-derived quartet witness.

A witness supplies a quartet, a polynomial in the fifteen JC orbit
coordinates, its claimed exact pullback hashes, and an orientation.  The
reviewer independently enumerates every switching and descendant mask,
substitutes the coordinate polynomial, and checks exact zero/nonzero or a
strict factor certificate.  A polynomial body is never selected by graph id
or topology id.

The verifier treats relation identity as the complete decorated directed
parent/arc/matching/provenance payload.  Duplicate records and coverage by
canonical target hash alone are rejected.

Every base parent declares `p_child_relation_ids`; every `p` parent declares
`q_child_relation_ids`.  These sets are recomputed from the parent's own
rooted arcs.  Reusing a child set from another root case or another rooted
graph is a fatal error even when both parents have the same standard
semi-directed mixed code.
