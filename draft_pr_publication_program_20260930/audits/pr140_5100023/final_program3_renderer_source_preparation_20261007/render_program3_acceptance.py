"""Pure PR140 final program-three rendering; no filesystem/provider/Git actions.

The caller must authenticate the input custody independently and validate the
genuine native completion with the accepted native operator before adoption.
This function additionally binds complete supplied bodies, validates completed
receipt semantics, and preserves unrelated JSON/history and MD/log prefixes.
It is source preparation, not permission to publish or adopt its postimages.
"""
import copy
import datetime
import hashlib
import json

FILES = ("CURRENT_PROGRESS.json", "CURRENT_PROGRESS.md", "RESEARCH_LOG.md")
NATIVE_COMMIT = "0d5ae675f8a51e0eaead04d0bf20cdce3f182c8d"
MERGE_COMMIT = "3eb0c843cf29502142370e066e8a23ef294c148d"
ORIGINAL_HEAD = "9e908ae58b5ceee6a0825bbebd8acf565db55340"
FINAL_PACKAGE = "1793d4fe2cace232cd316c43e9719c7acdc738f195a1f964a673e0f2a976ff8d"
R1_PACKAGE = "0d4f2a1fe22d06a787712b60821d477b54880c63c3f5716307a7a2eb0cf4b00f"
DOI = "10.5281/zenodo.23220043"
SHEET_RANGE = "'Math Puzzles'!A55:D55"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(body):
    require(type(body) is bytes, "complete input body must be bytes")
    def unique_pairs(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, "duplicate JSON key")
            value[key] = item
        return value
    return json.loads(body, object_pairs_hook=unique_pairs)


def utc(value):
    require(type(value) is str, "actual UTC string required")
    parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None and parsed.utcoffset() == datetime.timedelta(0),
            "actual UTC must be timezone-qualified UTC")
    return parsed


def body_pin(pin, inputs):
    require(type(pin) is dict and type(pin.get("path")) is str,
            "complete role pin required")
    require(type(pin.get("bytes")) is int and pin["bytes"] > 0 and
            type(pin.get("mode")) is int and pin["mode"] in (292, 420, 493),
            "typed size/mode pin required")
    require(type(pin.get("sha256")) is str and len(pin["sha256"]) == 64,
            "whole-body SHA256 pin required")
    require(pin["path"] in inputs, "missing complete body: " + pin["path"])
    value = inputs[pin["path"]]
    require(type(value) is dict and type(value.get("body")) is bytes and
            type(value.get("mode")) is int, "body and actual mode required")
    body = value["body"]
    require(len(body) == pin["bytes"] and value["mode"] == pin["mode"] and
            hashlib.sha256(body).hexdigest() == pin["sha256"],
            "full body/mode pin mismatch: " + pin["path"])
    return body


def completed_native(native_pin, inputs):
    require(native_pin["path"].endswith(
        "/pr140_5100023/ROOT_NATIVE_PUBLICATION_INSTALLATION_ACCEPTANCE_20261007.json"),
        "fixed genuine native completion role")
    r = read_json(body_pin(native_pin, inputs))
    require(r.get("schema") == "pr140-root-native-installation-acceptance/v1" and
            r.get("owner") == "ROOT" and r.get("fixture_only") is False and
            type(r.get("actual_ROOT_PID")) is int and r["actual_ROOT_PID"] > 0,
            "genuine ROOT native completion identity")
    utc(r["UTC"])
    for name in ("public_native_full_readback", "local_native_full_readback",
                 "original17_archive_preserved", "private_cache_and_backend_absences_preserved"):
        require(r.get(name) is True, "completed native readback missing: " + name)
    for name in ("source", "plan", "publish", "install", "root_readback",
                 "actual_acceptance_inputs"):
        body_pin(r[name], inputs)
    pub = read_json(body_pin(r["publish"], inputs))
    ins = read_json(body_pin(r["install"], inputs))
    plan = read_json(body_pin(r["plan"], inputs))
    for receipt, action in ((pub, "publish"), (ins, "install")):
        require(receipt.get("schema") == "pr140-native-publication-operation-receipt/v1" and
                receipt.get("transaction") == "native_acceptance" and
                receipt.get("action") == action and type(receipt.get("actual_PID")) is int and
                receipt["actual_PID"] > 0 and "error_type" not in receipt,
                "completed distinct native operation role")
        require(receipt.get("source_sha256") == r["source"]["sha256"] and
                receipt.get("plan_sha256") == r["plan"]["sha256"] and
                receipt.get("published_commit") == r["published_commit"] and
                receipt.get("own_operation_lock_released") is True,
                "actual source/plan/commit and released operation binding")
        children = receipt.get("children")
        require(type(children) is list and all(
            type(child) is dict and child.get("child_reaped") is True and
            child.get("process_group_empty") is True for child in children),
            "unresolved native child custody")
    require(pub.get("status") == "published_local_install_pending" and
            pub.get("public_full_body_readback") is True and
            pub.get("whole_parent_tree_preserved_outside_exact_overlay") is True and
            ins.get("status") == "public_and_local_install_verified" and
            ins.get("local_full_body_mode_readback") is True,
            "completed public and separate local native acceptance")
    require(r["published_commit"] == NATIVE_COMMIT and
            plan.get("schema") == "pr140-native-publication-overlay/v1" and
            plan.get("transaction") == "native_acceptance" and
            plan.get("source_sha256") == r["source"]["sha256"] and
            plan.get("actual_acceptance_inputs") == r["actual_acceptance_inputs"],
            "exact completed native transaction")
    expected = {}
    for member in plan["members"]:
        if member.get("install") is True:
            path = member["path"]
            require(path not in expected, "duplicate completed install member")
            expected[path] = member["post"]
    require(len(expected) == 23, "exact native14 and repair9 completed inventory")
    pins = r["installed_postimages"]
    require(type(pins) is list and len(pins) == 23, "complete actual23 installation pins")
    seen = set()
    for pin in pins:
        suffix = next((path for path in expected if pin["path"].endswith("/" + path)), None)
        require(suffix is not None and suffix not in seen,
                "unique exact installed native/repair selection")
        seen.add(suffix)
        require({key: pin[key] for key in ("bytes", "mode", "sha256")} ==
                {key: expected[suffix][key] for key in ("bytes", "mode", "sha256")},
                "installed actual postimage differs from completed plan")
        body_pin(pin, inputs)
    require(seen == set(expected), "no installed native/repair omission")
    a = read_json(body_pin(r["actual_acceptance_inputs"], inputs))
    require(a.get("schema") == "pr140-actual-native-publication-inputs/v1" and
            a.get("owner") == "ROOT" and a.get("fixture_only") is False and
            a.get("original_head") == ORIGINAL_HEAD and
            a.get("original_effort") == "2/5" and
            type(a.get("new_central_proof_search_turns")) is int and
            a["new_central_proof_search_turns"] == 0,
            "actual original target/source import identity")
    require(a.get("DOI") == DOI and a["PR140_merge"]["commit"] == MERGE_COMMIT and
            a["sheet"]["range"] == SHEET_RANGE and
            a["package_manifest_pin"]["sha256"] == FINAL_PACKAGE and
            a["R1_reviewed_manifest_sha256"] == R1_PACKAGE and
            a["R2_final_reviewed_manifest_sha256"] == FINAL_PACKAGE,
            "actual DOI/tracker/merge and truthful R1-to-final custody")
    for name in ("package_finally_reviewed_and_published", "actual_tracker_row_verified",
                 "actual_original_head_merge_verified"):
        require(a.get(name) is True, "actual completed publication prerequisite")
    return r


def append_body(body, text):
    require(type(body) is bytes, "whole preimage bytes required")
    body.decode("utf-8")
    return body + (b"" if body.endswith(b"\n") else b"\n") + text.encode("utf-8")


def render(preimages, template_body, native_pin, goal_pin, inputs, context):
    """Return three proposed final acceptance postimages; performs no I/O.

    inputs maps complete pinned paths to {body: bytes, mode: actual int}.
    context holds actual rendering UTC/PID and program-relative native/goal/next
    final receipt roles. The final receipt role has no prospective body or ID.
    """
    require(type(preimages) is dict and set(preimages) == set(FILES),
            "exact3 whole preimages required")
    before = read_json(preimages[FILES[0]])
    require(before.get("current_PR") == 140 and before.get("fully_completed_count") == 23 and
            type(before["fully_completed_count"]) is int and
            before.get("dated_eligible_total") == 99 and
            before.get("last_completed_PR") == 134 and
            len(before["published_PRs"]) == 11 and 140 not in before["published_PRs"] and
            140 not in before["fully_completed_eligible_PRs"],
            "fresh current23/11 PR140 preimages required")
    require(before.get("current_original_head") == ORIGINAL_HEAD and
            before.get("current_original_budget") == "2/5" and
            before.get("current_new_central_proof_search_turns") == 0,
            "preserve original target/budget without new central proof search")
    template = read_json(template_body)
    require(template.get("schema") == "pr140-final-program3-conditional-fields-template/v1" and
            template.get("preparation_only") is True,
            "frozen conditional template role")
    native = completed_native(native_pin, inputs)
    goal_record = read_json(body_pin(goal_pin, inputs))
    require(goal_record.get("schema") == "ROOT-actual-goal-tool-response-record/v1" and
            goal_record.get("owner") == "ROOT" and
            type(goal_record.get("actual_recorder_PID")) is int and
            goal_record["actual_recorder_PID"] > 0,
            "genuine full ROOT goal response preservation")
    goal = goal_record["get_goal_response"]
    require(type(goal.get("goal")) is dict and goal["goal"].get("status") in ("active", "blocked") and
            type(goal["goal"].get("updatedAt")) is int and
            goal["goal"].get("threadId") == "01a0f08c-564b-7a51-bc3c-09cc9990d0fd",
            "literal actual unfinished ROOT goal response")
    render_time = utc(context["render_UTC"])
    observed_time = utc(context["goal_observed_UTC"])
    require(context["goal_observed_UTC"] == goal_record["UTC"],
            "actual dated goal observation agreement")
    require(render_time >= utc(native["UTC"]) and render_time >= observed_time,
            "no rendering before native completion or observed goal")
    require(type(context.get("render_PID")) is int and context["render_PID"] > 0,
            "actual rendering PID required")
    for key in ("native_reference", "goal_reference", "final_metadata_receipt_role"):
        require(type(context.get(key)) is str and context[key].startswith("audits/pr140_5100023/")
                and ".." not in context[key].split("/"), "explicit bounded receipt/reference role")
    out = copy.deepcopy(before)
    historical = out.setdefault("historical_preparation_snapshots", [])
    require(type(historical) is list, "preserve historical snapshot list")
    historical.append({
        "UTC": before.get("updated_UTC", before.get("UTC")),
        "status": "SUPERSEDED_DATED_PR140_ACTIVE_SNAPSHOT",
        "case_percent": before.get("current_PR_workflow_percent"),
        "fields": {key: copy.deepcopy(value) for key, value in before.items()
                   if key.startswith(("current_", "active_checkpoint_"))},
        "note": "The dated pre-completion snapshot is preserved as history; final rendering does not retroactively relabel its package, native or publication state."
    })
    prior = {key: copy.deepcopy(value) for key, value in before.items()
             if key.startswith("last_completed_")}
    require(prior["last_completed_native_correction_commit"] ==
            "6c0c941ff4eaa0abe5df9c37003a7eb555b3688f" and
            prior["last_completed_metadata_checkpoint_commit"] ==
            "fa9050ddaa5fa8b8696baedd56adbfd67b287a94",
            "preserve actual prior PR134 completion meaning")
    out.setdefault("historical_completed_case_records", []).append({
        "PR": 134, "fields": prior,
        "note": "Exact previous last-completed family preserved before PR140 replaces it."
    })
    for key in tuple(out):
        if key.startswith("last_completed_"):
            del out[key]
    out.update(copy.deepcopy(template["desired_fields_only_after_actual_acceptance"]))
    out.update({
        "UTC": context["render_UTC"], "updated_UTC": context["render_UTC"],
        "actual_final_metadata_preparer_PID": context["render_PID"],
        "current_native_disposition_checkpoint_commit": native["published_commit"],
        "current_native_completion_acceptance": context["native_reference"],
        "current_native_completion_acceptance_sha256": native_pin["sha256"],
        "current_original17_unchanged": True,
        "current_original17_unchanged_scope": "All17 frozen original audit archive bodies are preserved. Selected canonical working bodies were intentionally repaired; original17_unchanged is not a claim that all17 current canonical bodies equal the original submission.",
        "current_accepted_native_and_repair_installed_count": 23,
        "current_accepted_native_metadata_count": 14,
        "current_accepted_canonical_repair_count": 9,
        "current_remaining_required_steps": "No PR140 step remains once this exact final acceptance snapshot is accepted. The persistent program continues.",
        "last_completed_record": context["native_reference"],
        "last_completed_actual_native_readback": native["root_readback"],
        "last_completed_native_correction_commit": native["published_commit"],
        "last_completed_actual_final_gate": None,
        "last_completed_final_completion_readback": None,
        "last_completed_actual_writer_release": None,
        "last_completed_metadata_checkpoint_commit": None,
        "last_completed_writer_release_scope": "The completed native publication and installation operation barriers were released. Final metadata publication, installation, readback and its owned barrier release are attested separately after this transaction.",
        "last_completed_transaction_receipt_reference": {
            "native_acceptance": context["native_reference"],
            "native_acceptance_sha256": native_pin["sha256"],
            "actual_native_acceptance_UTC": native["UTC"],
            "actual_native_commit": native["published_commit"],
            "separate_final_metadata_receipt_role": context["final_metadata_receipt_role"],
            "metadata_commit": None, "final_metadata_readback": None,
            "meaning": "The transaction cannot identify its own future commit or acceptance in its committed postimage. The separately authenticated actual receipt supplies these identities after publication, local installation, full readback and owned barrier release."
        },
        "persistent_goal_status": goal["goal"]["status"],
        "persistent_goal_status_at_last_tool_read": goal["goal"]["status"],
        "persistent_goal_API_updatedAt": goal["goal"]["updatedAt"],
        "persistent_goal_API_last_observed_UTC": context["goal_observed_UTC"],
        "persistent_goal_status_observation_source": context["goal_reference"],
        "persistent_goal_status_observation_sha256": goal_pin["sha256"],
        "persistent_goal_status_observation_is_dated_ROOT_readback": True,
        "persistent_goal_complete": False,
        "program_snapshot_semantics": "FINAL_ACCEPTANCE_STATE",
        "program_snapshot_UTC_semantics": "Actual final metadata preparation time; not the time of a future publication, installation or acceptance.",
        "program_snapshot_authority_condition": "These final acceptance postimages become authoritative only after exact final metadata publication, local installation, full public/local readbacks and owned barrier release are accepted in the separately authenticated actual receipt. The false pending flags describe the accepted end state and do not claim that this rendering performed the transaction.",
        "advance_to_next_PR_authorized_now": True,
        "next_step": "Once this exact final metadata acceptance and its owned barrier release are authenticated, perform fresh ascending literal-original-status intake after PR140. Preserve skip8 and leave nonclaimed statuses untouched.",
        "current_bounded_priority_support_for_qualified_resolution_note": True,
        "current_absolute_priority_established": False,
        "current_exclusive_theorem_novelty_over_later_note": False,
        "current_independent_discovery_established": False,
        "current_copying_or_collaboration_inferred": False,
        "current_novelty_established": False
    })
    require(out["fully_completed_eligible_PRs"] == before["fully_completed_eligible_PRs"] + [140] and
            out["published_PRs"] == before["published_PRs"] + [140],
            "only PR140 joins completed and published lists")
    for key in ("closed_without_publication_PRs", "accepted_partial_prior_result_PRs",
                "accepted_partial_priority_unestablished_PRs", "skipped_since_last_completion",
                "status_only_skips_before_PR134_completion"):
        require(out.get(key) == before.get(key), "unrelated program fact changed: " + key)
    when = context["render_UTC"]
    paragraph = (
        "\n### " + when + " — PR140 final acceptance snapshot\n\n"
        "This proposed final snapshot becomes authoritative only after its exact metadata publication, local installation, full readbacks and owned barrier release are accepted in the separate actual receipt. "
        "The genuine ROOT native completion " + context["native_reference"] + " binds actual native commit " + native["published_commit"] + "; all 23 native/repair postimages are installed and fully verified. "
        "The 17 original audit archive bodies remain unchanged; selected canonical working bodies intentionally contain the accepted repairs. "
        "Paper DOI " + DOI + ", tracker range " + SHEET_RANGE + ", and original-head merge " + MERGE_COMMIT + " are actual completed facts. "
        "The accepted end state is 24 completed of the dated 99 eligible cases (24.24%) and 12 publications, with PR140 at 100%. PR134 remains a completed 100% historical case with its actual native 6c0c941 and metadata fa9050dd receipts preserved. "
        "The original imported effort remains 2/5 with zero new central proof-search turns. "
        "The qualified k405 result concerns even least period N >= 4 and distinct vertices on a strictly nested nondegenerate confocal elliptical caustic 0 < lambda < b^2, including primitive stars and either orientation, using full-line, unweighted, unprimed antipedals; the circle is treated separately. The source's least-period interpretation is explicitly qualified. "
        "The bounded priority audit credits Ferudun's exact later overlap (DOI 10.5281/zenodo.23092466): the documented September 30 project PR precedes the specific October 1 deposit. No absolute or exclusive priority, independent discovery, copying or collaboration is inferred. "
        "R1 reviewed its original manifest " + R1_PACKAGE + "; the adopted title correction was followed by fresh clean R2 review of final manifest " + FINAL_PACKAGE + ". Extensive AI use and unrefereed status are disclosed; conventional human peer review is not claimed. "
        "The persistent goal remains " + goal["goal"]["status"] + " and unfinished according to the full fresh ROOT response. PR135–139 remain untouched status-only skips. "
        "This transaction's own final commit and readback identities are unset in its postimage and supplied afterward by " + context["final_metadata_receipt_role"] + ". "
        "Fresh ascending original-status-only intake after PR140 is authorized only once that actual final receipt and owned barrier release are authenticated; no later intake is claimed here.\n"
    )
    outputs = {
        FILES[0]: (json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"),
        FILES[1]: append_body(preimages[FILES[1]], paragraph),
        FILES[2]: append_body(preimages[FILES[2]], paragraph)
    }
    return outputs
