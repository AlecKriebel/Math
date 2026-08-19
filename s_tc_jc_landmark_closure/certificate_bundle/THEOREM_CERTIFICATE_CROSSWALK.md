# Minimal theorem-to-certificate crosswalk

All paths are relative to the extracted certificate-bundle root.

| Article claim | Primary files | Separate replay / exact certificate |
|---|---|---|
| Fixed mixed-graph convention, admissible rootings, primitive cycle/four-theta supports | `primary/certificates/core_universe.json`, `primary/certificates/support_universe.json`, `reviews/root_probe/verify_active_structural.py` | `reviews/final_standard_convention/verify_conventions.py`, root/probe certificates under `reviews/root_probe/` |
| Pointwise cut recovery and full incidence-scaling bridge fibre | `independent/bridge_cut/cut_certificate.json`, `independent/bridge_cut/bridge_certificate.json` | `reviews/global_bridge/exact_audit.py`, `independent/bridge_cut/verify_cut.py`, `verify_bridge.py` |
| Theorem 6.3: complete three-outgoing directed atlas | `primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_{relations,graphs,polynomials}.jsonl.gz`, `primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_signs.json` | `reviews/n3_universe_generator/generate_universe.py`, `reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py` |
| Theorem 6.3: four-outgoing theta gate and fixed-full restoration | `primary/certificates/hard_cover_{n4,graphs_n4,polynomials_n4,root_cases_n4}_schema3_theta2_full.jsonl.gz` | `reviews/theta2_signature_gate/`, `reviews/base_gate_adversarial_referee/`, active certificates under `reviews/final_hard_cover_cleanroom/certificates/` |
| Arbitrary subdivisions, direct residual anchors, and coherent one-/two-port probes | `primary/certificates/compact_probe_*`, `reviews/direct_anchor_probe_closure/certificates/` | `reviews/compact_probe_clean_clone_gate/semantic_gate.py`, clean-room engines under `reviews/compact_probe_format/final_n{3,4}_cleanroom/` |
| Ordinary triangle redirection common germ | `primary/certificates/jc_triangle_redirection_active.json` | `reviews/triangle_redirection_cleanroom/cleanroom_verify.py` and `certificate.json` |
| Triangle-free Omega sharpness family | `omega_audit/frozen_input/historical/jc_omega_move.json` | `omega_audit/independent/verify_omega_release.py`, `verify_omega_rank_readability.py` |
| Triangle-containing Theta sharpness family | `s_tc_jc_sharp_boundary/reproducibility/networks.json` | `s_tc_jc_sharp_boundary/reproducibility/verify_math.py` and `independent/verify_sharpness.py` |

`atlas/ATLAS_INDEX.csv.gz` is the human-navigable per-relation index. Each row
names its base certificate and verifier and, for a restoration root, the
closure certificate and verifier as distinct fields. The complete file-level
role and digest map is `ACTIVE_MANIFEST.json`.
