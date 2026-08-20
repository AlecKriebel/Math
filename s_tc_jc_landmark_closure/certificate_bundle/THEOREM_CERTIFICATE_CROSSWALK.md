# Minimal theorem-to-certificate crosswalk

All paths are relative to the extracted certificate-bundle root.

| Article claim | Minimal exact evidence | Replay |
|---|---|---|
| Fixed mixed-graph convention and primitive supports | `primary/certificates/{core_universe,support_universe}.json`; `reviews/root_probe/*_certificate.json` | `reviews/final_standard_convention/verify_conventions.py`; `reviews/root_probe/verify_active_structural.py` |
| Pointwise cut recovery and full incidence-scaling bridge fibre | `independent/bridge_cut/{cut,bridge}_certificate.json` | `independent/bridge_cut/verify_{cut,bridge}.py`; `reviews/global_bridge/exact_audit.py` |
| Theorem 6.3, including every three-/four-outgoing relation and restoration/probe closure | `atlas/ATLAS_EVIDENCE_BINDINGS.jsonl.gz` binds each row to its base evidence and closure verifier; compact streams are `primary/certificates/compact_probe_{paths,polynomials,transports,witnesses}_*.jsonl.gz`, with direct anchors under `reviews/direct_anchor_probe_closure/certificates/` | `verifiers/evidence_bindings.py`; `reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py`; `reviews/final_hard_cover_cleanroom/audit_candidate_stream.py`; `reviews/compact_probe_clean_clone_gate/semantic_gate.py` |
| Deterministic reconstruction of the complete bounded proof object from primitive inputs | primitive inputs and compilers under `primary/`; frozen streams under `primary/certificates/` | `verifiers/regenerate_load_bearing.py` through `bash verify.sh regenerate-all` |
| Ordinary triangle redirection common germ | `primary/certificates/jc_triangle_redirection_active.json` | `reviews/triangle_redirection_cleanroom/cleanroom_verify.py` |
| Triangle-free Omega and triangle-containing Theta sharpness families | `omega_audit/frozen_input/historical/jc_omega_move.json`; `s_tc_jc_sharp_boundary/reproducibility/networks.json` | `omega_audit/independent/verify_omega_release.py`; `s_tc_jc_sharp_boundary/reproducibility/{verify_math.py,independent/verify_sharpness.py}` |

`atlas/ATLAS_INDEX.csv.gz` is the human-navigable projection of the
authoritative evidence map.  `ACTIVE_MANIFEST.json` authenticates included
files; `verifiers/evidence_bindings.py` reconstructs and verifies the
row-by-row graph-to-evidence association.
