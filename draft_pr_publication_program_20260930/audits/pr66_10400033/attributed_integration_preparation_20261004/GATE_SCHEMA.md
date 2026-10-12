# Final ROOT gate contract — prepared, not authorized

These prepared sources do not authorize integration. ROOT must personally
inspect their exact current bytes and the final scientific reviews, then create
`../ROOT_FINAL_PRIOR_DISPOSITION_20261004.json`. This document is a contract,
not a substitute gate. Never reuse a PR65 acknowledgement or gate.

Every pin is exactly `{"path": "repository-relative/path", "bytes": integer,
"sha256": "64 lowercase hex characters"}`. Pin comparisons require all three
fields, actual regular files and paths confined to the repository.

Required identity and outcome fields:

| Field | Required value |
|---|---|
| `PR` | `66` |
| `expected_original_head` | `78f4a7fadac0fd24e147a617956cb409eb6a579e` |
| `UTC` | Actual final ROOT adjudication UTC with timezone |
| `minimum_writer_ack_utc` | A fresh lower bound, at or after `UTC` |
| `audited_outcome` | `already_solved` |
| `accepted_as` | `attributed_partial_prior_result` |
| `mathematics_percent` | Integer `100` |
| `bounded_priority_percent` | Integer `100` |
| `original_proof_turns` | `1/5` |
| `new_original_proof_turns` | Integer `0` |
| `goal_objective_sha256` | `1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04` |

The following must be literal JSON `true`: 
`ROOT_authorizes_guarded_attributed_prior_result_acceptance`,
`fresh_final_adversary_clean`, `ROOT_personally_read_all_required_reports`,
`candidate_mathematics_verified`,
`prior_resolution_of_exact_original_problem_verified`,
`ROOT_reviewed_exact_operational_byte_plan`,
`initial_literal_claimed_solved_gate_only`,
`initially_nonclaim_targets_untouched`, `even_prior_ingredient_verified`.

The following must be literal JSON `false`:
`new_solution_priority_clearance`, `publication_authorized`, `new_paper`,
`tracker_append`, `PR50_exception_extended`, `exact2000printedbody_read`,
`stronger_prior_p8_extremality_certified`,
`exact_even_formula_earlier_explicitly_printed`. The latter means “not located
or certified”; it does not assert that no earlier printing exists. `new_DOI`
must be JSON `null`.

Required evidence fields:

- `prospective_packet_directory`: repository-relative directory inside the
  PR66 audit. The final selected v2 value is
  `draft_pr_publication_program_20260930/audits/pr66_10400033/attributed_prior_result_preparation_v2_20261004`.
- `prospective_manifest`: exact pin for that directory's `MANIFEST.json`.
- `bound_prospective_inputs`: exactly four pins matching that manifest's
  `CURRENT_RESULT.md`, `CURRENT_PRIORITY_SPECIALIZATION.md`, `PR_BODY.md`,
  `DISPOSITION_PROPOSAL.json`. They are retained immutable prospective inputs.
- `bound_current_evidence`: exact pins for the actual fresh independent reviews,
  root reproductions, source readbacks and final priority adjudication read by
  ROOT. A label such as “fresh” does not substitute for a real report.
- `bound_original_evidence`: exact pins including the authenticated original
  `CANDIDATE.md`, `source_record.json`, `status.json`, and `turns.jsonl` under
  `original_source_authentication_20261004/original/`. ROOT should also bind the
  authentication report, original blob manifest and original queue authority.
- `operational_byte_plan`: exact pin for the selected plan inside this
  preparation folder. The v2 path ends in `OPERATIONAL_BYTE_PLAN_V2.json`.
- `bound_operational_preparation`: exact pins including the selected byte plan,
  `ROOT_integrate_attributed_prior_result_20261004.py` and
  `ROOT_readback_attributed_acceptance_20261004.py`. Include final planned
  document files for direct reviewability; the pinned plan also binds their
  exact final bytes and all literal transformations.

The gate deliberately permits a separately preserved v2 packet and v2 byte
plan. They must meet the same four-input and exact-transformation contract.
The selected plan's `scientific_changes:false` means its transformation from
its selected reviewed source documents changes operational stage wording only.
Any new scientific or historical statement belongs in a newly reviewed source
packet, followed by a new immutable plan. Never overwrite the v1 packet or v1
planned final documents to fit a later finding.

The manifest parser accepts either the v1 filename key `path` or v2 `name`,
strictly one per row. Each row must have exactly that key plus `bytes` and
`sha256`; there must be exactly four unique filenames. Gate pins always use
repository-relative `path`, not `name`.

Here is a complete **documentation-only field sample**. ROOT must compute every
pin from the actual current bytes and use actual UTC/review values. Angle-bracket
values are placeholders; this block is not a usable or authored approval file.

```json
{
  "PR": 66,
  "expected_original_head": "78f4a7fadac0fd24e147a617956cb409eb6a579e",
  "UTC": "<actual final ROOT UTC>",
  "minimum_writer_ack_utc": "<fresh UTC at or after final ROOT UTC>",
  "audited_outcome": "already_solved",
  "accepted_as": "attributed_partial_prior_result",
  "mathematics_percent": 100,
  "bounded_priority_percent": 100,
  "original_proof_turns": "1/5",
  "new_original_proof_turns": 0,
  "goal_objective_sha256": "1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04",
  "ROOT_authorizes_guarded_attributed_prior_result_acceptance": true,
  "fresh_final_adversary_clean": true,
  "ROOT_personally_read_all_required_reports": true,
  "candidate_mathematics_verified": true,
  "prior_resolution_of_exact_original_problem_verified": true,
  "ROOT_reviewed_exact_operational_byte_plan": true,
  "initial_literal_claimed_solved_gate_only": true,
  "initially_nonclaim_targets_untouched": true,
  "even_prior_ingredient_verified": true,
  "new_solution_priority_clearance": false,
  "publication_authorized": false,
  "new_paper": false,
  "tracker_append": false,
  "PR50_exception_extended": false,
  "exact2000printedbody_read": false,
  "stronger_prior_p8_extremality_certified": false,
  "exact_even_formula_earlier_explicitly_printed": false,
  "new_DOI": null,
  "prospective_packet_directory": "draft_pr_publication_program_20260930/audits/pr66_10400033/attributed_prior_result_preparation_v2_20261004",
  "prospective_manifest": {"path":"<v2 MANIFEST path>","bytes":"<integer>","sha256":"<actual digest>"},
  "bound_prospective_inputs": ["<exact four normalized path/bytes/sha256 pins>"],
  "bound_current_evidence": ["<all actual required current review/source/reproduction pins>"],
  "bound_original_evidence": ["<original CANDIDATE/source_record/status/turns pins and authentication authorities>"],
  "operational_byte_plan": {"path":"draft_pr_publication_program_20260930/audits/pr66_10400033/attributed_integration_preparation_20261004/OPERATIONAL_BYTE_PLAN_V2.json","bytes":"<integer>","sha256":"<actual digest>"},
  "bound_operational_preparation": ["<operator/readback/selected plan/final-byte-file pins>"]
}
```

The other writer owns
`draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json`. Its **actual
complete body** must freeze across both phases and readbacks. Required fields:

- `shared_git_writes_paused:true`;
- `paused_for:"PR66 attributed prior-result integration 20261004"`;
- `dirty_tracked_bodies_modes_frozen_after_acknowledgement:true`;
- integer `all_staged_path_count:0` and `owned_staged_paths:[]`;
- `local_main_at_pause == remote_main_at_pause`, matching the fresh native
  baseline before merge; the mirror accepts that same baseline from the actual
  merge receipt;
- actual `utc` (or `UTC`) at or after the gate's `minimum_writer_ack_utc`.

ROOT must obtain the other writer's real acknowledgement. These sources never
create, edit, guess or repair it. At preparation inspection, the status was
`shared_git_writes_paused:false`; it was not integration permission.

No final gate has been created by this preparation task. No integration phase,
metadata mutation, acceptance ledger, paper, DOI, tracker action or human
contact has occurred here.
