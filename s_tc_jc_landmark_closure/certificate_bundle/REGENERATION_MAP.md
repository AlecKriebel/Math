# Regeneration map

`bash verify.sh regenerate-all` runs the following logical reconstruction
chain twice in isolated copies and requires identical commitments.

| Proof object | Reconstruction / replay program |
|---|---|
| Primitive core, completion, and support universes | `primary/core_universe.py`, `primary/completion_universe.py`, `primary/support_universe.py`, plus the convention/root fixtures |
| 10,826 raw and 10,466 canonical three-outgoing relations | `reviews/n3_universe_generator/generate_universe.py` |
| Complete three-outgoing graph-to-switching-to-mask-to-tensor-to-certificate association | `reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py` |
| Four-outgoing invariant filter and 192 surviving presentations | `reviews/theta2_signature_gate/verify_gate.py` and `canonicalize_relations.py` |
| Exact strict factors and relation transports | `reviews/base_gate_adversarial_referee_n3/referee_n3.py` and `reviews/base_gate_adversarial_referee/referee.py` |
| Three-/four-outgoing restoration forests | `reviews/final_hard_cover_cleanroom/verify_schema3_n4_certificates.py` together with the clean-room bounded replay and semantic probe replay |
| 2,642 one-port and 18,224 two-port direct-anchor relations | `reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py` followed by its verifier and mutations |
| 269,730 compact path-bound probe relations | `reviews/compact_probe_clean_clone_gate/semantic_gate.py` with independent n3/n4 engines and mutation tests |
| Cut/bridge, ordinary triangle, Omega, and Theta component certificates | the primary and separately implemented component programs named in `THEOREM_CERTIFICATE_CROSSWALK.md` |

The large compressed streams are retained as frozen proof records so a
reviewer can inspect the finite universe without first running a long build.
The regeneration gate reconstructs their logical universes, associations,
sign/equality decisions, and normalized commitments from the included
primitive inputs; it does not use byte equality of compressed container
metadata as a mathematical premise.
