"""PR141 pure final metadata renderer. SOURCE preparation only.
No filesystem, provider, Git, process, publication or installation actions.
The public render entry requires a genuinely supplied complete ROOT native gate.
"""
import copy
import datetime
import hashlib
import json

FILES = ("CURRENT_PROGRESS.json", "CURRENT_PROGRESS.md", "RESEARCH_LOG.md")
ROLES = ("source", "builder_source", "plan", "review", "publish", "install",
         "publication", "tracker", "sheet", "merge", "clean_package",
         "mathematics", "priority", "original_manifest",
         "full_postimage_inventory", "full_local_inventory")
HEAD = "523247e3246a5f44c7b0089074bb304c1f642bd0"
MERGE = "7431d02aed19d00fc8494a564b9048db203320e9"
DOI = "10.5281/zenodo.23224103"
PACKAGE = "05d50f2a24abf580e90bf2bc61e5a0367f03d8edc0fd9fa395a36ceb476372d2"
TEX = "f5a71902a30c386de29a372427d928273ea50e3ff833bd8b6e74ce5f34e9fd9f"
PDF = "acf262d707c9faa466f30a86a8347ae7cbff0ad5a48fbb38893e460c0e3ec2e5"
ZIP = "8835f8ea3be4e25eb25b7663a2da0d56ee4afbc3dbe60843b02436a66dc237ab"
SHEET = "'Math Puzzles'!A56:D56"
SCOPE = ("For every finite number k of independent Brownian walkers on a circle, "
         "the full joint law of first-visit cell lengths is characterized by the explicit "
         "joint Laplace transform and deterministic finite-dimensional integral coefficients "
         "for fixed distinct labeled seeds, equidistant starts and independent uniform starts. "
         "Cumulative physical clocks, absolutely convergent outer series, uniform factorial "
         "remainder and compact-support moment determinacy are proved.")
LIMITS = ("No named density, fast algorithm or certified inner quadrature is claimed. "
          "Exact finite-model and high-precision scalar diagnostics supplement the direct "
          "Brownian proof; they do not prove a Brownian limit or a numerical-error certificate. "
          "The dated bounded priority audit discloses Gomes1996 and Dicker2006 full-text "
          "access and registry-search limitations; it establishes no absolute/exclusive "
          "priority or independent discovery. Extensive AI use and unrefereed status are "
          "disclosed; conventional human peer review is not claimed.")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(body):
    require(type(body) is bytes, "whole bytes input required")
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, "duplicate JSON key")
            out[key] = value
        return out
    return json.loads(body, object_pairs_hook=pairs)


def stamp(value):
    require(type(value) is str, "actual UTC string required")
    dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(dt.tzinfo is not None and dt.utcoffset() == datetime.timedelta(0),
            "actual timezone-qualified UTC required")
    return dt


def oid(value):
    require(type(value) is str and len(value) == 40 and
            all(c in "0123456789abcdef" for c in value), "actual Git OID required")
    return value


def full_pin(pin, bodies):
    require(type(pin) is dict and type(pin.get("path")) is str and
            type(pin.get("bytes")) is int and pin["bytes"] > 0 and
            type(pin.get("mode")) is int and pin["mode"] in (292, 420, 493) and
            type(pin.get("sha256")) is str and len(pin["sha256"]) == 64,
            "typed full body/mode pin required")
    require(pin["path"] in bodies, "missing complete pinned input")
    item = bodies[pin["path"]]
    require(type(item) is dict and type(item.get("body")) is bytes and
            type(item.get("mode")) is int and len(item["body"]) == pin["bytes"] and
            item["mode"] == pin["mode"] and
            hashlib.sha256(item["body"]).hexdigest() == pin["sha256"],
            "whole input bytes or actual mode differ")
    return item["body"]


def gate_header(g):
    require(g.get("schema") == "pr141-root-actual-native-acceptance/v1" and
            g.get("status") == "ACCEPTED_NATIVE_PUBLIC_AND_LOCAL" and
            g.get("fixture_only", False) is False and
            type(g.get("actual_ROOT_PID")) is int and g["actual_ROOT_PID"] > 0,
            "genuine completed ROOT native acceptance required")
    stamp(g["UTC"])
    for key, value in (("PR", 141), ("native_remote_changed_path_count", 18),
                       ("native_local_installed_path_count", 32),
                       ("new_central_proof_search_turns", 0), ("program_case_estimate", 96)):
        require(type(g.get(key)) is int and g[key] == value, "typed native gate field: " + key)
    require(g.get("original_head") == HEAD and g.get("original_merge") == MERGE and
            g.get("native_sole_parent") == MERGE and g.get("original_effort") == "1/5",
            "actual original target/parent/effort identity")
    oid(g["native_commit"])
    for key in ("full_public_body_mode_readback", "full_local_body_mode_readback",
                "whole_parent_tree_preserved_outside_exact_overlay", "real_git_controls_preserved",
                "original_author_turn_ledger_present"):
        require(g.get(key) is True, "native closing guard absent: " + key)
    for key in ("original_native_transition_ledger_present", "program3_changed", "overall_goal_complete"):
        require(g.get(key) is False, "false lineage or premature completion: " + key)


def readback_map(rows):
    require(type(rows) is list, "complete readback inventory required")
    out = {}
    for row in rows:
        require(type(row) is dict and type(row.get("path")) is str and row["path"] not in out,
                "duplicate or malformed inventory path")
        require(type(row.get("bytes")) is int and row["bytes"] > 0 and
                type(row.get("mode")) is int and row["mode"] == 420,
                "typed inventory bytes/mode")
        out[row["path"]] = {k: row[k] for k in ("bytes", "mode", "sha256")}
    return out


def validate_gate(gate_pin, bodies, contract):
    require(gate_pin["path"].endswith("/pr141_30003818/ROOT_ACTUAL_NATIVE_ACCEPTANCE_20261007.json"),
            "fixed actual closing role required")
    g = load(full_pin(gate_pin, bodies)); gate_header(g)
    pins = g["evidence_pins"]
    require(type(pins) is dict and set(pins) == set(ROLES), "exact full closing evidence role table")
    docs = {name: full_pin(pins[name], bodies) for name in ROLES}
    for name, expected in contract["known_role_pins"].items():
        require(pins[name] == expected, "genuine fixed input role changed: " + name)
    pub, ins, plan, review = (load(docs[n]) for n in ("publish", "install", "plan", "review"))
    for receipt, action, status in ((pub, "publish", "published_local_install_pending"),
                                    (ins, "install", "public_and_local_install_verified")):
        require(receipt.get("schema") == "pr141-native-sparse-operation-receipt/v1" and
                receipt.get("transaction") == "native_acceptance" and
                receipt.get("action") == action and receipt.get("status") == status and
                type(receipt.get("actual_PID")) is int and receipt["actual_PID"] > 0 and
                receipt.get("fixture_only") is False and "error_type" not in receipt,
                "actual distinct successful native operation")
        require(receipt.get("source_sha256") == pins["source"]["sha256"] and
                receipt.get("plan_sha256") == pins["plan"]["sha256"] and
                receipt.get("review_sha256") == pins["review"]["sha256"] and
                receipt.get("published_commit") == g["native_commit"] and
                receipt.get("own_operation_lock_released") is True and
                receipt.get("public_full_body_readback") is True and
                receipt.get("public_full_body_mode_readback") is True,
                "native operation/source/plan/review/commit/lock binding")
        children = receipt.get("children")
        require(type(children) is list and children and all(
            type(c) is dict and c.get("child_reaped") is True and
            c.get("process_group_empty") is True for c in children),
            "native unresolved child custody")
    require(pub.get("sole_parent") == MERGE and pub.get("whole_parent_tree_preserved_outside_exact_overlay") is True and
            type(pub.get("remote_changed_path_count")) is int and pub["remote_changed_path_count"] == 18 and
            type(pub.get("local_install_path_count")) is int and pub["local_install_path_count"] == 32 and
            ins.get("local_full_body_mode_readback") is True and
            type(ins.get("local_readback_path_count")) is int and ins["local_readback_path_count"] == 32 and
            ins.get("program3_changed") is False and ins.get("raw_backend_installed") is False and
            ins.get("private_cache_installed") is False, "exact bounded public18/local32 completion")
    require(plan.get("schema") == "pr141-native-sparse-main-overlay/v1" and
            plan.get("transaction") == "native_acceptance" and plan.get("base_commit") == MERGE and
            plan.get("source_sha256") == pins["source"]["sha256"] and
            review.get("schema") == "pr141-native-sparse-operator-source-plan-review/v1" and
            review.get("verdict") == "PASS" and review.get("mandatory_findings") == [] and
            review.get("actual_review") is True and review.get("actual_data_inputs_authenticated") is True and
            review.get("raw_publication_tracker_original_merge_roles_authenticated") is True and
            review.get("source_sha256") == pins["source"]["sha256"] and
            review.get("plan_sha256") == pins["plan"]["sha256"], "actual reviewed native plan identity")
    for name, count, rows in (("remote_members", 18, pub["public_blob_readbacks"]),
                              ("install_members", 32, ins["installed_postimages"])):
        members = plan[name]
        require(type(members) is list and len(members) == count and
                len({m["path"] for m in members}) == count, "exact native inventory selection")
        expected = {m["path"]: m["post"] for m in members}
        actual = readback_map(rows)
        if name == "install_members":
            actual = {next((p for p in expected if path.endswith("/" + p)), path): value
                      for path, value in actual.items()}
        require(actual == expected, "native whole readbacks differ from reviewed postimages")
    publication, tracker, sheet, merge, clean = (load(docs[n]) for n in
                                                ("publication", "tracker", "sheet", "merge", "clean_package"))
    require(publication.get("published") is True and publication.get("DOI") == DOI and
            type(publication.get("record_id")) is int and publication["record_id"] == 23224103 and
            publication.get("public_complete_PDF_ZIP_bytes_equal_local") is True and
            publication.get("metadata_normalizations") == [] and
            publication.get("package_manifest_sha256") == PACKAGE and
            publication.get("whole_package_clean_gate_sha256") == pins["clean_package"]["sha256"],
            "actual exact publication/fullbytes package custody")
    require(tracker.get("DOI") == DOI and tracker.get("range") == SHEET and
            tracker.get("single_append") is True and tracker.get("row_full_readbacks_equal") is True and
            tracker.get("sheet_receipt_sha256") == pins["sheet"]["sha256"] and
            tracker.get("published_record_result_sha256") == pins["publication"]["sha256"] and
            sheet.get("range") == SHEET and type(sheet.get("row_index")) is int and sheet["row_index"] == 56 and
            sheet.get("single_append") is True and sheet.get("both_distinct_actual_full_cell_readbacks_equal") is True,
            "actual single tracker row/full cell readbacks")
    require(merge.get("merged") is True and merge.get("original_head") == HEAD and
            merge.get("merge_commit") == MERGE and merge.get("DOI") == DOI and
            merge.get("actual_tracker_range") == SHEET and
            merge.get("publication_result_sha256") == pins["publication"]["sha256"] and
            merge.get("tracker_result_sha256") == pins["tracker"]["sha256"],
            "actual original-head merge bound to publication/tracker")
    require(clean.get("status") == "APPROVED_EXACT_QUALIFIED_RESOLUTION_PACKAGE" and
            clean.get("package_manifest_sha256") == PACKAGE and
            clean.get("R1_mandatory_findings") == [] and
            clean.get("fresh_new_independent_R2_no_mandatory_findings") is True and
            clean.get("no_package_changes_between_R1_and_R2") is True and
            clean["pdf"]["sha256"] == PDF and clean["zip"]["sha256"] == ZIP and
            clean.get("AI_extensive_unrefereed_no_conventional_human_peer_review_disclosed") is True and
            clean.get("no_absolute_priority_exclusivity_or_independent_discovery_claim") is True,
            "genuine full package review and frozen PDF/ZIP/science limits")
    return g


def transform(preimages, g, gate_pin, goal_record, goal_pin, context, contract):
    """Private pure conservation helper; caller render performs authority checks."""
    require(set(preimages) == set(FILES) and all(type(v) is bytes for v in preimages.values()),
            "exact3 complete preimages")
    before = load(preimages[FILES[0]])
    for key, value in (("current_PR", 140), ("fully_completed_count", 24),
                       ("last_completed_PR", 140), ("dated_eligible_total", 99)):
        require(type(before.get(key)) is int and before[key] == value, "fresh preceding PR140 state")
    require(len(before["published_PRs"]) == 12 and
            len(before["fully_completed_eligible_PRs"]) == 24 and
            141 not in before["published_PRs"] and 141 not in before["fully_completed_eligible_PRs"],
            "current24/12 exactly; no duplicate or premature141 count")
    for name in FILES:
        pin = contract["current_preimages"][name]
        require(len(preimages[name]) == pin["bytes"] and
                hashlib.sha256(preimages[name]).hexdigest() == pin["sha256"], "whole current3 baseline changed")
    require(type(context.get("actual_preparer_PID")) is int and context["actual_preparer_PID"] > 0,
            "actual preparer PID required")
    when = context["UTC"]
    require(stamp(when) >= stamp(g["UTC"]) and stamp(when) >= stamp(goal_record["UTC"]),
            "render time cannot precede actual closing/goal observation")
    goal = goal_record["get_goal_response"]["goal"]
    require(goal.get("threadId") == "01a0f08c-564b-7a51-bc3c-09cc9990d0fd" and
            goal.get("status") in ("active", "blocked") and type(goal.get("updatedAt")) is int,
            "literal unfinished actual ROOT goal response")
    out = copy.deepcopy(before)
    oldcurrent = {k: copy.deepcopy(v) for k, v in before.items() if k.startswith("current_")}
    oldlast = {k: copy.deepcopy(v) for k, v in before.items() if k.startswith("last_completed_")}
    out.setdefault("historical_preparation_snapshots", []).append({
        "UTC": before["updated_UTC"], "status": "COMPLETED_PR140_SUPERSEDED_AS_CURRENT",
        "case_percent": 100, "fields": oldcurrent})
    out.setdefault("historical_completed_case_records", []).append({
        "PR": 140, "fields": oldlast,
        "actual_final_acceptance": contract["previous140_final_acceptance"],
        "note": "Exact previous last-completed family retained; separate genuine final140 receipt supplies the actual metadata commit/readback identities."})
    for key in tuple(out):
        if key.startswith(("current_", "last_completed_")):
            del out[key]
    base = "audits/pr141_30003818/"
    out.update({
        "UTC": when, "updated_UTC": when, "actual_final_metadata_preparer_PID": context["actual_preparer_PID"],
        "current_PR": 141, "current_problem_id": 30003818, "current_code": "OWR-16164-012",
        "current_original_head": HEAD, "current_original_literal_status": "claimed_solved",
        "current_native_status": "claimed_solved", "current_original_budget": "1/5",
        "current_original_author_turn_ledger_present": True,
        "current_original_native_transition_ledger_present": False,
        "current_new_central_proof_search_turns": 0, "current_PR_workflow_percent": 100,
        "current_workflow_estimate_percent": 100, "current_mathematical_clearance": True,
        "current_mathematical_audit_percent": 100, "current_source_authentication_percent": 100,
        "current_mathematical_gate": base + "ROOT_MATHEMATICAL_GATE.json",
        "current_mathematical_gate_sha256": contract["known_role_pins"]["mathematics"]["sha256"],
        "current_mathematical_target": "Finite-k Brownian first-visit cell-length joint law on a circle",
        "current_mathematical_scope": SCOPE, "current_mathematical_scope_limits": LIMITS,
        "current_priority_clearance": True, "current_priority_audit_percent": 100,
        "current_priority_status": "completed_bounded_qualified_support",
        "current_priority_gate": base + "ROOT_BOUNDED_PRIORITY_PREPARATION_GATE_20261007.json",
        "current_priority_gate_sha256": contract["known_role_pins"]["priority"]["sha256"],
        "current_priority_audit_scope": LIMITS, "current_absolute_priority_established": False,
        "current_exclusive_priority_established": False, "current_independent_discovery_established": False,
        "current_novelty_established": False, "current_PR50_exception_used": False,
        "current_copying_or_collaboration_inferred": False,
        "current_supporting_repairs_accepted": ["explicit verifier failures surviving optimization"],
        "current_bounded_priority_support_for_qualified_resolution_note": True,
        "current_DOI": DOI, "current_Zenodo_published": True, "current_tracker_updated": True,
        "current_tracker_range": SHEET, "current_publication_package_manifest_sha256": PACKAGE,
        "current_published_TEX_sha256": TEX, "current_published_PDF_sha256": PDF,
        "current_published_ZIP_sha256": ZIP, "current_publication_package_prepared": True,
        "current_publication_package_review_clearance": True,
        "current_publication_package_review_status": "two_fresh_clean_whole_package_reviews_same_frozen_package",
        "current_publication_package_reviews_required": False, "current_publication_ready": True,
        "current_publication_upload_clearance": True,
        "current_publication_package_candidate_readback": base + "ROOT_CLEAN_PUBLICATION_GATE_20261007.json",
        "current_publication_package_candidate_readback_sha256": contract["known_role_pins"]["clean_package"]["sha256"],
        "current_native_completion_acceptance": base + "ROOT_ACTUAL_NATIVE_ACCEPTANCE_20261007.json",
        "current_native_completion_acceptance_sha256": gate_pin["sha256"],
        "current_native_disposition_checkpoint_commit": g["native_commit"],
        "current_native_export_state": "ACTUALLY_PUBLISHED_INSTALLED_AND_FULLY_ACCEPTED",
        "current_native_public_changed_path_count": 18, "current_native_local_installed_path_count": 32,
        "current_original20_archive_preserved": True,
        "current_original20_preservation_scope": "Frozen original archive preserved; selected canonical verifier guards and metadata intentionally updated by the accepted native transaction.",
        "current_core_disposition_complete": True, "current_closed_without_merging": False,
        "current_closed_without_publication": False, "current_actual_closing_comment_url": None,
        "current_disposition": "published_merged_explicit_joint_transform_resolution_accepted_after_final_metadata_transaction",
        "current_active_checkpoint_pending": False, "current_completion_metadata_checkpoint_pending": False,
        "current_remaining_required_steps": "No PR141 case step remains after exact final metadata acceptance. Persistent program continues.",
        "published_count": 13, "fully_completed_count": 25, "fully_completed_eligible_PRs": before["fully_completed_eligible_PRs"] + [141],
        "fully_completed_fraction_percent": 100 * 25 / 99, "published_PRs": before["published_PRs"] + [141],
        "last_published_PR": 141, "last_published_DOI": DOI,
        "last_completed_PR": 141, "last_completed_PR_workflow_percent": 100,
        "last_completed_DOI": DOI, "last_completed_tracker_range": SHEET,
        "last_completed_merge_commit": MERGE, "last_completed_native_correction_commit": g["native_commit"],
        "last_completed_original_budget": "1/5", "last_completed_new_central_proof_search_turns": 0,
        "last_completed_outcome": "published_complete_finite_k_Brownian_first_visit_joint_transform_characterization",
        "last_completed_source_resolution_scope": SCOPE + " " + LIMITS,
        "last_completed_mathematical_result_valid": True, "last_completed_priority_clearance": True,
        "last_completed_publication_authorization": True,
        "last_completed_record": base + "ROOT_ACTUAL_NATIVE_ACCEPTANCE_20261007.json",
        "last_completed_metadata_checkpoint_commit": None, "last_completed_final_completion_readback": None,
        "last_completed_actual_final_gate": None, "last_completed_actual_writer_release": None,
        "last_completed_transaction_receipt_reference": {
            "native_acceptance": base + "ROOT_ACTUAL_NATIVE_ACCEPTANCE_20261007.json",
            "native_acceptance_sha256": gate_pin["sha256"], "actual_native_commit": g["native_commit"],
            "actual_native_acceptance_UTC": g["UTC"], "metadata_commit": None, "metadata_actual_PID": None,
            "metadata_actual_UTC": None, "final_metadata_readback": None,
            "separate_final_metadata_receipt_role": context["separate_final_metadata_receipt_role"]},
        "active_checkpoint_commit": None, "active_checkpoint_acceptance_receipt": None,
        "active_checkpoint_actual_readback_required": False, "active_checkpoint_source_plan_review_required": False,
        "active_checkpoint_local_installation_performed_by_this_preparation": False,
        "active_checkpoint_publication_performed_by_this_preparation": False,
        "completion_metadata_checkpoint_pending_at_snapshot": False,
        "persistent_goal_complete": False, "persistent_goal_status": goal["status"],
        "persistent_goal_status_at_last_tool_read": goal["status"],
        "persistent_goal_API_updatedAt": goal["updatedAt"],
        "persistent_goal_API_last_observed_UTC": goal_record["UTC"],
        "persistent_goal_status_observation_source": context["goal_reference"],
        "persistent_goal_status_observation_sha256": goal_pin["sha256"],
        "next_numeric_intake_cursor": 142, "next_eligible_PR_after_current_completion": None,
        "next_eligible_order_requires_fresh_status_check": True, "advance_to_next_PR_authorized_now": True,
        "next_step": "Only after this exact final metadata publication, local installation, full readbacks and owned barrier release are accepted, perform fresh ascending literal-original-status intake after PR141; preserve skip8 and leave nonclaimed statuses untouched.",
        "remaining_current_step": "PR141 accepted end state at 100%; later intake requires the separate actual final metadata receipt.",
        "program_snapshot_semantics": "CONDITIONAL_FINAL_ACCEPTANCE_STATE",
        "program_snapshot_authority_condition": "This private proposal becomes authoritative only after the exact final metadata transaction is published, locally installed and fully read back with its owned barrier released. False pending flags describe that accepted end state; rendering performs no such action.",
        "program_snapshot_UTC_semantics": "Actual preparation time after genuine native closure, not a future operation time.",
        "workflow_estimate_percent": 100 * 25 / 99,
        "workflow_estimate_definition": "Twenty-five of the dated 99 eligible cases completed and 13 published only upon exact final metadata acceptance; the overall goal remains unfinished."
    })
    text = ("\n### " + when + " — PR141 conditional final acceptance snapshot\n\n"
            "This private proposal becomes authoritative only after exact final metadata publication, "
            "local installation, full readbacks and owned barrier release are accepted. "
            "The genuine ROOT native gate binds 18 public changes and32 local installations; native commit "
            + g["native_commit"] + ", original-head merge " + MERGE + ", DOI " + DOI +
            " and tracker " + SHEET + " are actual facts. The proposed accepted state is25 completed "
            "of the dated99 cases (25.25%) and13 publications, with PR141 at100%. "
            "The full prior PR140 snapshot and completion record remain history; the frozen original20 "
            "archive remains preserved while accepted canonical guards/metadata intentionally differ. "
            "The imported author effort remains1/5, its author turn ledger was present, the native "
            "transition chain was absent, and zero new central proof-search turns were added. " +
            SCOPE + " " + LIMITS + " The frozen published TEX/PDF/ZIP hashes are retained. "
            "The persistent goal remains " + goal["status"] + " and unfinished. This transaction's "
            "own future commit/PID/UTC/readback are unset; " + context["separate_final_metadata_receipt_role"] +
            " supplies the actual identities after completion. No intake past141 is claimed.\n")
    text = text.replace("and32", "and 32").replace("is25", "is 25").replace("dated99", "dated 99").replace("and13", "and 13").replace("at100%", "at 100%").replace("original20", "original 20").replace("remains1/5", "remains 1/5").replace("past141", "past 141")
    output = {FILES[0]: (json.dumps(out, indent=2, sort_keys=True) + "\n").encode()}
    for name in FILES[1:]:
        preimages[name].decode("utf-8")
        output[name] = preimages[name] + (b"" if preimages[name].endswith(b"\n") else b"\n") + text.encode()
    return output


def render(preimages, gate_pin, goal_pin, bodies, context, contract):
    """Pure renderer of PRIVATE proposals only after authentic late input exists."""
    g = validate_gate(gate_pin, bodies, contract)
    goal_record = load(full_pin(goal_pin, bodies))
    require(goal_record.get("schema") == "ROOT-actual-goal-tool-response-record/v1" and
            goal_record.get("owner") == "ROOT" and
            type(goal_record.get("actual_recorder_PID")) is int and goal_record["actual_recorder_PID"] > 0,
            "genuine fresh full ROOT goal preservation")
    for key in ("goal_reference", "separate_final_metadata_receipt_role"):
        value = context.get(key)
        require(type(value) is str and value.startswith("audits/pr141_30003818/") and
                ".." not in value.split("/"), "bounded future/reference role")
    full_pin(contract["previous140_final_acceptance"], bodies)
    return transform(preimages, g, gate_pin, goal_record, goal_pin, context, contract)
