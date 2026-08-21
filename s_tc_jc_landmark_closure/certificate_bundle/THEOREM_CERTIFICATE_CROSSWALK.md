# Minimal theorem-to-certificate crosswalk

All paths are relative to the extracted certificate-bundle root.

| Article claim | Minimal exact evidence | Replay |
|---|---|---|
| Fixed mixed-graph convention and primitive supports | `primary/certificates/{core_universe,support_universe}.json`; `reviews/root_probe/*_certificate.json` | `reviews/final_standard_convention/verify_conventions.py`; `reviews/root_probe/verify_active_structural.py` |
| Pointwise cut recovery and full incidence-scaling bridge fibre | `independent/bridge_cut/{palette_reduction,cut,bridge}_certificate.json`; `reviews/global_bridge/palette_cleanroom_certificate.json` | `independent/bridge_cut/verify_palette_reduction.py`; `independent/bridge_cut/verify_{cut,bridge}.py`; `reviews/global_bridge/{verify_palette_cleanroom,exact_audit}.py` |
| Theorem 6.3, including every three-/four-outgoing relation and restoration/probe closure | `atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz` points row-by-row into `atlas/{RESTORATION,DIRECT_ANCHOR}_CLOSURE_BINDINGS.jsonl.gz`; restoration terminals point onward into `atlas/COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz`, whose records bind the exact path, transport, witness, and polynomial streams | `verifiers/evidence_bindings.py`; `reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py`; `reviews/final_hard_cover_cleanroom/audit_candidate_stream.py`; `reviews/compact_probe_clean_clone_gate/semantic_gate.py`; `reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py` |
| Deterministic reconstruction of the complete bounded proof object from primitive inputs | primitive inputs and compilers under `primary/`; frozen streams under `primary/certificates/` | `verifiers/regenerate_load_bearing.py` through `bash verify.sh regenerate-all` |
| Ordinary triangle redirection common germ | `primary/certificates/jc_triangle_redirection_active.json` | `reviews/triangle_redirection_cleanroom/cleanroom_verify.py` |
| Triangle-free Omega and triangle-containing Theta sharpness families | `sharpness/omega/inputs/jc_omega_move.json`; `sharpness/theta/inputs/networks.json` | `sharpness/omega/cleanroom/verify_omega_release.py`; `sharpness/theta/{verify_math.py,cleanroom/verify_sharpness.py}` |

For three outgoing ports the evidence map is indexed by canonical directed
relation.  For four outgoing ports it retains all 192 normalized survivor
presentations and records their further 3-direct/57-nonretaining quotient
digests separately.  `atlas/ATLAS_INDEX.csv.gz` is the human-navigable
projection of that authoritative evidence map.  `ACTIVE_MANIFEST.json`
authenticates included files; `verifiers/evidence_bindings.py` reconstructs
and verifies the row-by-row graph-to-evidence association.

The evidence is transitively closed at record level.  Restoration-root rows
list every reachable hard-cover state and bind each equality terminal to a
compact path row; compact rows bind every packed transport, witness, and
polynomial record.  Direct-anchor rows bind every one- and two-port child
relation, graph, and graph-derived witness.  The mutation suite rejects
deleted and swapped links at each layer.
