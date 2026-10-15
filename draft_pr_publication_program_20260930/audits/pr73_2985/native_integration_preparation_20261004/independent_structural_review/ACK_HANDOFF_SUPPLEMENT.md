# ACK handoff supplementary independent review

Closed at 2026-10-04T19:33:39.319164+00:00; preparation-only result. The exact old defect witness and 24-case corrected witness are pinned by FINAL_V2_REVIEW.json. Both use in-memory files/index/Git-output fixtures, never shared repository actions. The only cross-phase body-equality exception is the exact ACK_REL control path, with prior and fresh actual ACK authentication and preserved mode/index/flags. It does not extend to another filename, unrelated foreign body, or within-phase ACK drift.

The fresh Window remains fully captured and checked. Predecessor receipt authentication verifies prior retained ACK bytes/pin against the recorded controller/phase/gate/plan/execution/nonce/freeze/time interval and actual first retained HEAD command. Fresh ACK capture remains pinned to current actual bytes and the fresh controller. Restoration skips ACK after the full pre-restoration drift guard; it does not stage, restore or overwrite ACK.

Check cases:
- authenticated_ACK_only_body_handoff: accepted as intended
- ACK_mode_between_phases: rejected as intended
- ACK_index_between_phases: rejected as intended
- ACK_flags_nonordinary: rejected as intended
- unrelated_body_between_phases: rejected as intended
- prior_retained_ACK_body_tampering: rejected as intended
- lookalike_ACK_path_not_excepted: rejected as intended
- prior_false_pause: rejected as intended
- prior_nonempty_index_declaration: rejected as intended
- prior_wrong_phase: rejected as intended
- prior_wrong_gate: rejected as intended
- prior_wrong_plan: rejected as intended
- prior_wrong_execution: rejected as intended
- prior_ack_after_controller: rejected as intended
- prior_unobserved_head: rejected as intended
- fresh_reused_nonce: rejected as intended
- fresh_stale_time: rejected as intended
- fresh_false_freeze: rejected as intended
- fresh_wrong_phase: rejected as intended
- fresh_wrong_gate: rejected as intended
- within_phase_ACK_body: rejected as intended
- within_phase_ACK_mode: rejected as intended
- within_phase_ACK_index: rejected as intended
- ACK_never_restored_or_overwritten: accepted as intended
