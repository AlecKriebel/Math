# Future exact arguments and dependency order

All refs are exact {path,bytes,sha256}; source files/inputs are canonical0444 regular files, descriptor-read without final or ancestor symlink traversal. CLI:
  /opt/homebrew/bin/python3.11 -E -S -B -P capture_logical_packet.py capture|finalize
    --config PATH --config-bytes N --config-sha256 SHA256
    --selection PATH --selection-bytes N --selection-sha256 SHA256
    --source-acceptance PATH --source-acceptance-bytes N --source-acceptance-sha256 SHA256

No command is authorized by this document.

Selection schema pr239-root-positive-public-selection-v1 has exactly:
{schema,PR,operational_authority,files,total_files,total_bytes}.
PR is int239; operational_authority=false. Each row exactly:
{path,origin,bytes,sha256,git_blob,observed_source_mode,role,selection_basis}.
path is repository-relative target, origin an absolute checkout-owned source, observed_source_mode=int292. Byte pins/nativeOID must match full regular UTF8 body. No views/QUEUE row may appear; they are generated. Required24 carry pins and32 archive pins are fixed by the engine.95 includes all32 exact attempt rows.100 disallows science target rows.

Capture config exact:
{schema,PR,phase,output_name,journal,evidence_references,own_row_post,protected_body_paths,deferred_targets,retired_candidates}.
schema=pr239-readonly-factual-capture-config-v1; PR:int239; phase merge95|completion100.
output_name matches private_capture239_[A-Za-z0-9_-]{1,40}, new child of this helper folder.
journal matches ROOT_COMPLETE239_READ_CAPTURE_[A-Za-z0-9_-]{1,35}, new private operational journal under the frozen engine folder. No existing journal is reused.
evidence_references are exact actual precreated Root roles math,custody,priority,whole_package,publication,tracker,ready;100 also merge. No case_ready role is supplied yet. The existing frozen model event contracts govern provider/tracker/ready and actual phase95 merge evidence. Their exact bodies must be positively selected.
own_row_post is an exact raw single-line file reference at95, null at100. Claimed_solved3/5, unique canonical row and every foreign QUEUE byte are enforced.
protected_body_paths is a sorted unique list of at most64 explicit existing own attempt/old-audit regular blob paths. These bodies are fetched and pinned; absent/conflicting paths stop.
deferred_targets is a dictionary of3..40 distinct explicit safe public target paths. Required keys native_identity,case_ready,carry_inventory name the natural future files. Additional keys reserve only individually named future authored files or public canonical raw-commit aliases. No path prefix grants permission. The capture records every target's native preimage, including absence.
retired_candidates is a sorted unique finite<=100 list of native OIDs.

Capture source acceptance schema pr239-root-logical-capture-source-acceptance-v1,
evidence_scope ACTUAL_ROOT_RECEIPT_SOURCE_ONLY,PR239,accepted true,action='capture'.
It binds configuration_reference,selection_reference,capture_source_pin,capture_source_manifest_pin,engine_source_manifest_pin and exact true flags Root_full_source_read,independent_source_review_accepted,only_readonly_capture_or_offline_conditional_staging_authorized. The flag Seed_Runtime_original_lock_actual_five_native_POST_ref_PR_provider_or_intake_authorized must be false. The source reads this acceptance freshly with every guard; the helper does not create it.

After Root separately accepts that source and actual read scope, Root may execute capture. The successful private FACTUAL_CAPTURE_SUMMARY.json names the closed Main before/after and parent raw body, all raw original/base commits, full33 scope,32 body identities/origins, whole queue/row pins, native target preimages, separate local identities and bodies, protected nodes/bodies, initial selected+conditional view bodies, authenticated tree tuples and exact deferred paths. Its scope explicitly denies Root acceptance/candidate/CAS/sync/completion/numeric authority. CAPTURE_STOPPED.json/raw journals alone are not a successful snapshot. A Main movement fails without rebind/retry.

Root then reviews actual facts and authors actual native-identity acceptance, finite carry acceptance and case-ready receipt required by the frozen engine. No optimistic gate is generated here. Root may copy canonical commit bytes to exact reserved public targets; native receipt raw_commit paths may point to those aliases only when every captured raw byte pin and native identity stays identical. Third-party/private raw provider material cannot be exported by this mechanism.

Root's final selection must contain exactly all originally selected targets plus every reserved deferred target. Sources for the original known targets must remain byte-identical; generated views/QUEUE are taken exactly from the successful capture. Every deferred source is newly pinned and subject to the same safe positive selection and add-or-exact-noop checks. A new scope requires a new explicitly accepted capture, not silent expansion.

Finalize config exact:
{schema,PR,snapshot,stage_name,native_identity,case_ready,carry_inventory}.
schema=pr239-offline-logical-finalize-config-v1; snapshot is exact successful factual summary ref.
stage_name matches private_packet239_[A-Za-z0-9_-]{1,40}, new private child under the frozen engine folder.
The three Root acceptance refs must be at their exact reserved natural target paths and selected bodies. Their schemas, exact data bindings, raw original history, carry and ready contracts are checked with the frozen model.100 uses earlier actual merge95 receipt, actual C1 ancestry and original closed merged PR.

A separate source acceptance uses the same source-acceptance schema with action='finalize', but binds the new exact finalize config and final selection refs. It conveys only offline conditional staging authority. Finalize uses only authenticated saved tree tuples and captured native/local preimages; no live API exists in this path. Canonical native hashes and projected own subtree are recomputed. Its output is strict LOGICAL_MANIFEST.json field structure, staged sources and separate local preimages, plus a conditional construction receipt. Full frozen load_inputs cannot run before Root creates the later actual logical-packet acceptance; construction is not that acceptance or independent exact-packet review.

Next Root steps remain full actual logical/source/exact-packet acceptance, fresh native parent admission, candidate/two independent immutable proofs, held external CAS with actual same-live poll, exact-five sync/pointer and separate actual Root terminal. Stale capture facts do not lease Main; modern admission independently rechecks all mutable preimages and PR before effects. No native/PR/provider/tracker/intake action is performed by this helper.

## Revision02 final-target check

Preliminary selection can reserve a finite safe prior-case target, but this is not final carry acceptance. After reading the actual carry acceptance, finalize checks every payload target against the frozen model's exact positive predicate and verifies actual carry/science body pins before any stage directory or packet source is written. Prior-case targets outside accepted carry stop. Because final selection must equal the captured target universe, a wrongly reserved old-case target requires explicit truthful Root carry inclusion or a new reviewed capture; it is never silently dropped or admitted.

Empty own overlays preserve the captured opaque attempt tuple directly. The helper never fetches/replays an intentionally unread own envelope merely to recompute its unchanged OID. An empty/absent state is preserved as None by the pure helper; completion100 capture itself still requires an existing accepted attempt.
