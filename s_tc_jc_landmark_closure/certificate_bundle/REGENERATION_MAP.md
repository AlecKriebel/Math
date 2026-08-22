# Regeneration map

`bash verify.sh regenerate-all` invokes
`verifiers/regenerate_load_bearing.py` twice in isolated copies.  Each run
executes the complete chain below from primitive inputs, compares every final
logical stream with the frozen proof records, and emits a normalized
commitment.  The two commitments must agree exactly.

| Proof object | Reconstruction / replay program |
|---|---|
| Primitive core, completion, and support universes | `primary/core_universe.py`, `primary/completion_universe.py`, `primary/support_universe.py`, plus the convention/root fixtures |
| Descriptor invariant-bit table used as a performance cache | `primary/atlas_compiler.py --sizes 3 4 --disable-target-signature-prefilter`; `regenerate_load_bearing.py` first deletes the bundled derived cache, reconstructs it from the regenerated primitive inputs and invariant templates, and requires exact byte equality before downstream use.  The compiler's loaded/expanded-count summary is diagnostic and is not a proof input. |
| 10,826 raw and 10,466 canonical three-outgoing relations | `reviews/n3_universe_generator/generate_universe.py`; all three emitted certificate/stream files are deleted first and compared after rebuilding |
| Complete three-outgoing graph-to-switching-to-mask-to-tensor-to-certificate association | `reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py` |
| Four-outgoing invariant filter and 192 surviving presentations | `reviews/theta2_signature_gate/verify_gate.py` and `canonicalize_relations.py`; all six signature/crosswalk/quotient outputs are deleted first and compared after rebuilding |
| Exact strict factors and relation transports | `reviews/base_gate_adversarial_referee_n3/referee_n3.py` and `reviews/base_gate_adversarial_referee/referee.py` |
| Three-/four-outgoing restoration forests | `primary/hard_cover_compiler.py`, `primary/merge_hard_cover_shards.py`, and the all-record audit `reviews/final_hard_cover_cleanroom/audit_candidate_stream.py` |
| 2,642 one-port and 18,224 two-port direct-anchor relations | `reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py` followed by its verifier and mutations |
| 269,730 compact path-bound probe relations | `primary/compact_probe_extension_compiler.py`, followed by `reviews/compact_probe_clean_clone_gate/semantic_gate.py` and mutation tests |
| Per-relation graph/evidence binding, transitive restoration/compact/direct closure bindings, and human index | `verifiers/evidence_bindings.py` reconstructs all four content-addressed JSONL streams; the verifier requires `atlas/ATLAS_INDEX.csv.gz` to be the exact projection of the theorem-row stream |
| Arbitrary-word cut reduction | `independent/bridge_cut/verify_palette_reduction.py` partitions every balanced four-through-eight-port segment word into a direct three-run obstruction or a short-palette reduction; `reviews/global_bridge/verify_palette_cleanroom.py` independently reconstructs every primitive rooted graph and switching and checks that the reduced palette has no survivor |
| Normalized endpoint dichotomy and crossing minors | `independent/bridge_cut/verify_cut.py` and the separate implementation `reviews/global_bridge/exact_audit.py` identify the complete central singleton-signature class, normalize it, and replay every exact sign/minor certificate |
| Bridge fibre, ordinary triangle, Omega, and Theta component certificates | the primary and separately implemented component programs named in `THEOREM_CERTIFICATE_CROSSWALK.md` |

The large compressed streams are retained as frozen proof records so a
reviewer can inspect the finite universe without first running a long build.
The regeneration gate reconstructs their complete logical universes,
graph-to-certificate associations, sign/equality decisions, restoration
transports, probe records, and normalized commitments from the included
primitive inputs.  It compares decompressed logical streams, not incidental
compressed-container metadata.

Before invoking any producer, the regeneration driver deletes every declared
derived output in its disposable copy.  A no-op, partial, or stale-output
producer therefore fails because a required stream is absent; it cannot pass
by leaving the bundled frozen bytes untouched.  The immutable expected bytes
remain only in the separate extracted bundle against which regenerated
logical streams are compared.
