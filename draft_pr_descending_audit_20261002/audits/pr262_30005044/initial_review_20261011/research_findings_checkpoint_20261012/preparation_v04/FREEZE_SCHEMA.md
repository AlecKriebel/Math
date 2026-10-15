# V04 freeze and approval interface — source proposal only

Root creates root_final_freeze_v04/SELECTION.json after actual corrected author/
metadata acceptance and final peer handback. Sorted indented JSON with terminal
newline uses checkpoint_common.dump. Full file pins have exactly normalized
absolute path, bytes, sha256 and octal filesystem_mode. Every current full source
must equal Root's literal frozen body, separate Git mode100644/100755. No cache,
source symlink or mutable glob discovery. Launch python3 -I -B, no optimization.

Required final selection fields:

- schema=pr262-main-findings-final-freeze-v4;source_version=preparation_v04;
  root_explicit_final_freeze=true.
- current_baseline_certificate full file pin and identical
  current_baseline_certificate_sha256. See BASELINE_CERTIFICATE_SCHEMA.md.
  baseline_commit/baseline_tree match the exact certificate; sole_parent is its
  current_commit. No executable literal current HEAD, root or count binds data.
- baseline_counts={leaves,directories,all_entries,peer_delta_paths,
  foreign_delta_leaf_paths,foreign_delta_all_entries,protected_leaf_paths}.
  First three match the full current census; peer_delta_paths=76; delta counts
  match complete ADC-to-current derivation; protected_leaf_paths is the exact
  UNION count, permitting overlap and current modifications/deletions.
- Sorted peer_delta_literal_paths,foreign_delta_literal_paths and
  foreign_delta_all_entry_paths, with complete ledger SHA256 fields
  peer_delta_record_sha256 and foreign_delta_record_sha256.
- actor={name:Alec Kriebel,email:me@aleckriebel.com};actor_verified_source_commit
  =adc6d1441ea42af49a9fe296e52358257c087993. Root chooses commit_unix_seconds,
  matching commit_date_utc and literal newline-terminated commit_message.
- Actual corrected_author_head and corrected_PR_metadata={title,body_sha256}
  matching the separate accepted actual corrected author/title/body receipt.
  qualitative_assessment=already_solved;native_PR_merge=false;
  paper_DOI_GWS=false;added_author_attempt_turns=0.
- source_dependencies: exact canonical V04 full pins common,builder,executor,
  owned_reader. Actual build source is preparation_v04/private_builder.py;
  execute source is preparation_v04/provider_executor.py. All role/path/body/
  size/mode aliases fail. Owned reader is20648 bytes SHA256
  e8ce82f5e444095be08fe771963ff24b2c4ce9fa0285f52d4da88d9cd218cd1e.
- tools: absolute full executable pins git and gh; no implicit PATH selection.
  Direct Reader Popen and run_capture freshly validate full pins at dispatch.
  The interval from pin verification to OS spawn remains a host assumption.
- inputs: exact seven CLOSED_HISTORICAL_INPUT_PINS embedded in the complete
  helper, plus actual_author_correction. Historical ADC raw commit/root/full
  census,1de raw commit/full census,peer76 ledger and NI config pins remain
  fixed. Certificate supplies exactly six separate current roles. All consumed
  nested raw/ancestry/provider/body/collector/provenance pins are fully read.
- required_claim_roles: exact helper set, all represented by selected bodies.
  actual_corrected_draft_acceptance occurs exactly once and its current source
  pin equals the closed actual_author_correction input.
- complete_C3_target_files: exact38 accepted target rows, dump SHA256
  844922cb8d940fff1980835b80740a909292c53f0cbbb1dd7b90de42361ee55b.
  complete_C3_target_files_sha256 equals that digest; C3_manifest_sha256 is
  e3ab9c075ad00a7d97651b9218d2c4a83acc366cec847d0783d1eed2a63c3353.
- files: explicit repository_path,git_mode,git_blob,claim_roles,current_full_source
  full pin and frozen_body full pin under root_final_freeze_v04. selected_count
  and complete_selected_list_sha256 bind the whole list. Core38 stay at exact
  checkpoint core_C3 path, filesystem0444. Protected historical/current-delta
  leaf paths and absences cannot be selected or structurally aliased. Selection
  cannot hide foreign descendants. Rewritten common directory ancestors retain
  every unselected child through complete raw-tree/census verification.

Actual corrected acceptance schema is
pr262-root-actual-corrected-draft-acceptance-v4, checkpoint_source_version
preparation_v04, actual_corrected_author_commit equals corrected_author_head,
full_provider_readback_accepted=true,actual_ref_verified=true,
full_metadata_readback_accepted=true,fresh_author_stage_main_guard_accepted=true,
PR_OPEN_DRAFT_unmerged_unclosed=true,accepted_PR_title and accepted_PR_body_sha256
match corrected_PR_metadata. actual_provider_acceptance_support is a nonempty
distinct explicit full-pin list, all read fully. Earlier author-stage MAIN may
be recorded as dated provenance; it is NOT required to equal later certified
findings MAIN. A planned b033 or objects-only upload is not actual acceptance.

ROOT_BUILD_APPROVAL_V04.json binds exact selection_sha256,
root_authorized_stage=build,new_independent_review_required_completed=true and
complete source_review. Decision status=GO_NEW_MAIN_FINDINGS_SOURCE_V04_ONLY,
blocking_findings=[],whole_fresh_review_complete=true, exact selection/source
version/certificateSHA/baseline commit/tree/counts and builder/executor SHA.

ROOT_EXECUTION_PROMOTION_V04.json uses the same exact selection/source review,
root_authorized_stage=execute and complete fresh candidate_review. Artifact
pins cover exactly proof,raw_commit,trees,blobs,tree_payload,commit_payload,
full_rows,validation,completion in private_candidate_v04. Proof schema
pr262-new-main-findings-private-proof-v4/source_version=preparation_v04 binds
exact certificate/selection/census and complete per-path raw-tree closure.
Candidate decision status=GO_NEW_MAIN_FINDINGS_EXACT_CANDIDATE_V04_ONLY binds
selection/proofSHA,candidate commit/tree/sole current parent/count,
complete_all_current_baseline_leaves_and_directories_checked=true,
all_protected_leaf_paths_and_current_foreign_entries_checked=true,
source version,baseline_certificate_sha256 and full derived baseline_counts.
exact_MAIN_CAS_payload_sha256 pins one expected-old current-commit, forcefalse
GraphQL refs/heads/main update to the reviewed candidate.

Each changed directory has a unique per-path before/after/raw-body record.
Repeated raw OID is permitted only for identical valid full bodies, with every
path independently checked against its complete direct census children.
rewritten_ancestor_count is per-path; distinct_rewritten_tree_object_count is
per raw OID. The accepted253-byte33935aba930fe702cfdeb19ab1c5c8968ce2e12c
C3 tree occurs at two paths. Missing/duplicate paths, wrong per-path binding,
nonidentical repeated bodies or inconsistent raw bodies fail.

Before CAS Root supplies actual_readback_acceptance full pin at
ROOT_PRECAS_ACTUAL_READBACK_ACCEPTANCE_V04.json, schema
pr262-root-full-actual-readback-acceptance-v4/source_version=preparation_v04,
root_full_actual_readback_read_and_fresh_rehash=true,no_unknown_outcomes=true,
exact candidate commit/tree/proof/certificate SHA and files covering EVERY
readback_outputs() capture in actual_execution_v04/readback. Full selected blob
and nonrecursive ancestor GETs plus EMPTY independent raw commit/census proof
must precede the one exact-old,forcefalse MAIN CAS. Every stage reserves its
whole future output set before ANY provider/Git dispatch; occupied roots cannot
be retried. Exact REST/CAS request construction is fully supplied by executor.

Each review has core full pins decision,report,inputs,authored_manifest and
root_complete_read_and_fresh_rehash=true. Manifest schema
pr262-explicit-authored-review-closure-v1 requires complete explicit files,
complete_authored_output_list=true,manifest_self_excluded=true, including report,
decision and input manifest. Root reads/rehashes the entire declared closure.
A manifest is not an authentication signature. Prior sealed V01/V02/V03 reviews,
dated baseline data and controls confer no new GO. Changed source/data/selection
requires new whole review. Actual receipt,final selection/promotions,candidate
and provider execution remain absent in this preparation.

Actual object acceptance schema is pr262-main-findings-created-objects-v4;
readback acceptance schema is pr262-main-findings-full-readback-v4; final MAIN
acceptance schema is pr262-root-actual-main-findings-acceptance-v4. Each carries
source_version=preparation_v04,selection_sha256 and baseline_certificate_sha256.
Object/readback revalidation rejects mismatched source,selection or certificate
bindings before later stages. These actual receipts are not created by source
preparation. Eight inert controls cover exact and mismatched stage bindings.
