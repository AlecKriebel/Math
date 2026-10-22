# Independent repaired PR239 capture source review

UTC checkpoint: 2026-10-18T03:26:00Z. Source-review completion estimate: 100%.

**Disposition: no mandatory source repairs remain.** Revision02 implements both required revision01 repairs. This report supports Root's consideration of the exact frozen source only. It accepts no actual configuration, finite public selection, captured facts, logical packet, mutable Main state, native candidate, CAS, PR merge, provider/tracker event, local checkpoint, terminal receipt or numeric advance.

The subject is \`logical_capture_preparation_02/capture_logical_packet.py\`, 42,168 bytes / SHA256 \`313a9fdfeb37407f94a5950ab91120e52850b85acb178d1f7a83e5bef8851a3b\`. Its ten-payload source manifest is 1,762 bytes / \`989d582a7fd40b711f46cd3f87cb45dbebcbd7c4d792a0ed9b3e61653bd487dc\`; external seal is 395 bytes / `184f060c59accf8386a13e724d04501e82bbddd752018ad93dae8bd2f2bcceb7`. The ten payloads total101,450 bytes. All ten and all19 accepted-engine payloads were rehashed, canonical and mode0444. The engine source manifest is 3,198 bytes / \`96b0b248f390f67860b435b57cde34b2d2142206b9fc5c8166417f9c98d0db6c\`.

I read the entire helper, CONTRACT.md, README.md and extracted CONFIG_CONTRACT.json. I read the accepted engine contract, the model through the complete strict load_inputs validator, all immediate-tree source, and the relevant descriptor, journal, GET/cache and bounded-transport primitives. Initial source analysis was saved as INITIAL_DERIVATION.md before consulting the earlier adversary report or the producer control source/results. The task and revision documentation already identified F01/F02; this was a fresh independent verification of the repairs, not a claim to rediscover them blindly. Later I read the prior report and the full producer control source, then ran only reviewed pure synthetic controls.

## F01: opaque attempt preservation is repaired

projected_attempt now derives the own overlay and returns the exact authenticated existing tuple immediately if that overlay is empty. No child-envelope rebuild occurs in this case. The absence boundary returns None; capture at completion100 separately requires a positive existing attempt node. A nonempty own overlay retains exact-preimage rebuilding.

The independent reproduction used a fresh authenticated replay containing exactly the ancestors of the attempt and no envelope at all for its sentinel opaque child. A first call with an empty overlay returned the correct tuple after only three ancestor-envelope reads. The own sentinel child and unrelated foreign sentinel remained unread. A repeated call with a wholly unrelated payload changed neither request count, cache contents nor inspected-entry count. Separate controls exercised absent attempts, malformed file-instead-of-tree state, new attempts, existing attempts, correct nonempty projections and wrong preimages. This avoids the populated-cache weakness of the original revision01 producer control.

## F02: final scope now uses actual accepted carry

finalize parses h.carry_inventory, calls final_target_admissibility and completes its Root identity/readiness/tree/preimage/source checks before constructing any stage Output. The new guard uses the same relevant target alternatives as strict load_inputs: views, current-case public targets, exact members of the actual accepted carry map, individually pinned phase95 science, and phase95 QUEUE. Actual carry/science body pins must match. Science and QUEUE are refused at completion100.

I exercised the actual frozen carry_inventory validator on explicitly synthetic in-memory values, including its24 fixed mandatory pins and rejection of an arbitrary foreign target. For each phase, the same safe-looking old-case extra was refused when absent from accepted carry, accepted when explicitly included with the exact body pin, and refused on body mismatch or missing payload. Independent controls also tested private/binary/foreign targets, unlisted science, exact phase95 science, wrong science bodies, duplicate/malformed science and phase100 prohibitions.

The broad preliminary selector still permits a finite safe prior-case target before the actual carry acceptance exists. This is intentional and documented; finalization now closes that preliminary scope against the actual carry map. The final known-plus-reserved target universe cannot silently expand or discard the extra.

## Other examined boundaries

Raw signed commit reconstruction preserves the identity-bearing empty final gpgsig continuation by splitting on the literal LF byte. Exact native SHA1 and metadata tree/ordered-parent association decide acceptance. Independent controls covered one/two parents, no final signature LF, one/two final LFs, CRLF content, Unicode payload, changed signatures, wrong OIDs and reversed parent order. Unsigned recovery was checked at several equal/different timezone offsets and accepts only exact SHA1 reconstruction. Unsupported encodings and zero/three-parent commits fail closed; this is bounded support, not a claim to support every possible Git commit encoding.

The saved-tree replay exposes no transport fallback and authenticates canonical immediate-tree hashes before using tuples. Independent controls rejected missing/corrupt envelopes, inconsistent mode/type and slash-bearing immediate names. Exact overlays preserved unrelated opaque trees and executable mode; preimage and leaf/ancestor conflicts were refused.

Selection checks enforce exact keys/types, int239, false operational authority, readonly mode292, canonical native pins, required24 carry,32 original archives and phase95 original32 attempt targets. Independent metadata controls covered missing/duplicate required rows, malformed pins/origins/modes/types, unsafe/generated/private/binary destinations,595/596-row bounds and8MB aggregate bounds. selected_bodies was separately tested against an explicitly in-memory reader for exact SHA1/SHA256/length, Unicode/empty bodies, NUL and invalid UTF8; those controls do not claim to test real descriptor races. Full source inspection and inherited source/producer AST controls cover the unchanged no-follow descriptor implementation.

WholeQUEUE controls preserved every foreign byte and own-row LF/CRLF/absent finalLF, required claimed3/5, and refused duplicate/indented ambiguous rows, extra foreign payload in the supplied own row and phase100 replacement. In-memory publication/tracker values were passed through the actual event validator before testing proposals. Phase95 retained55/39 and original memberships; conditional100 added only239 to56/40. Both log prefixes and exact95→100 marker order were preserved; duplicate/missing markers, divergent logs and changed/ill-typed counters failed.

Source inspection confirms main obtains the exact Root source/config/selection acceptance before either high-level action. The guard rechecks its own source, both complete finite source closures, exact configuration, exact selection and exact Root acceptance. Output is restricted to a new child under the helper/engine with exclusive, no-follow readonly writes. Capture has bounded GET-only routes, receipt-aware same-invocation immutable reuse, full native body associations, closed Main/PR brackets and no Root acceptance synthesis. Finalize is offline and emits only conditional construction. It does not synthesize a logical acceptance.

I independently compared every top-level symbol against revision01: only projected_attempt and finalize changed and final_target_admissibility was added. No hidden changes occurred in the inherited helper functions. The19-file engine remains frozen.

## Actual checks and explicit limits

The independently authored controls completed **212 checks**, exit0 and empty stderr. The fully read producer controls were also actually rerun: **80 checks**, exit0 and empty stderr; their output bytes exactly match the frozen OFFLINE_CONTROLS.json. Counts include closure and structural checks and describe finite source checks, not mathematical proof coverage.

Neither high-level capture/finalize/source_guard/Output/GET/helpers/main nor any API/Seed/Runtime/lock/native/provider/tracker/PR/current-five/Git operation was executed by the independent controls. In-memory traps forbid all those helper entry points. The producer control rerun invokes helpers only to load pinned inert modules; it performs no high-level helper action or transport. No networking occurred. The only files written by this review are new owned report/control artifacts inside logical_capture_source_adversary_02; control scripts themselves have stdout only.

L01 remains a Root **procedural gate obligation**, not a new mandatory source repair: a safe destination and checkout-owned origin cannot classify the source body's privacy. Root must inspect every exact (origin,target,pin,role,basis) and the intended public body, excluding private/provider/raw exports except deliberately reviewed canonical commit aliases. No private body was read or relabeled by these controls.

Root must also verify the lineage/authenticity of the actual successful capture, exact evidence authorship and acceptance, all native/local preimages and complete target inventory, then perform the distinct strict logical/exact-packet review and later fresh admission. The small final-target subguard is not a standalone full-manifest validator; other load_inputs invariants rely on the actual captured universe and later exact packet gate. Native preimage freshness and actual operational effects cannot follow from this source report.

The scientific publication is outside this source review and unchanged. No goal-completion or intake authority is established.
