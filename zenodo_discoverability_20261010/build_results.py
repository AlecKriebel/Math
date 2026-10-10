"""Build a disk-only report of reviewed Zenodo metadata updates.

No client, token, network, Git, or mutation tool is used. Completion requires
all frozen approved public after receipts and a matching independent audit.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABELS = {
    "keywords": "subject terms",
    "language": "English language",
    "creators": "author metadata",
    "related_identifiers": "related links",
    "description": "description",
    "notes": "notes",
    "upload_type": "resource type",
    "publication_type": "preprint classification",
}
PROTECTED_METADATA = ("title", "publication_date", "version", "license", "access_right")


def read_json(path: Path):
    raw = path.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def artifact(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return path.name


def added_items(before, after, key=lambda value: value):
    old = {key(value) for value in before}
    return [value for value in after if key(value) not in old]


def sources_for(entry: dict, base: Path) -> list[dict]:
    sources = entry.get("sources", [])
    if not sources and entry.get("source_provenance"):
        provenance, _ = read_json(base / entry["source_provenance"])
        sources = [{"filename": provenance["filename"], "md5": provenance["verified_md5"],
                    "text_path": provenance["text_path"], "origin": provenance["origin"]}]
    return sources


def local_checks(before: dict, after: dict, approved: dict, patch: dict) -> dict[str, bool]:
    """Compare public snapshots directly; full rich-field audit is independent."""
    bn, an = before.get("native", {}), after.get("native", {})
    checks = {
        "published_same_record": str(before.get("id")) == str(after.get("id")) == str(approved["id"])
            and after.get("submitted") is True and after.get("state") == "done",
        "doi_unchanged": bool(before.get("doi")) and before.get("doi") == after.get("doi"),
        "concept_record_unchanged": bool(before.get("conceptrecid"))
            and before.get("conceptrecid") == after.get("conceptrecid"),
        "full_public_identity_and_version_history_unchanged": bool(before.get("identity"))
            and before.get("identity") == after.get("identity"),
        "file_names_checksums_sizes_unchanged": bool(before.get("files"))
            and before.get("files") == after.get("files"),
        "native_file_ids_settings_access_links_unchanged": "native_files" in before
            and "native_files" in after and before["native_files"] == after["native_files"],
        "native_pids_unchanged": "pids" in bn and bn.get("pids") == an.get("pids"),
        "native_access_unchanged": "access" in bn and bn.get("access") == an.get("access"),
        "native_custom_fields_unchanged": "custom_fields" in bn
            and bn.get("custom_fields") == an.get("custom_fields"),
        "original_title_date_version_license_access_unchanged": all(
            before["metadata"].get(field) == after["metadata"].get(field)
            for field in PROTECTED_METADATA),
        "reviewed_patch_hash_bound_in_receipt": after.get("verification", {}).get(
            "reviewed_patch_sha256") == approved["patch_sha256"],
        "publisher_verification_present": after.get("verification", {}).get(
            "same_record_doi_concept_version_history_files") is True,
    }
    # Frozen patch fields, all public before/after fields, and native rich data
    # are also checked by FINAL_RECEIPT_AUDIT; avoid reimplementing its documented
    # serializer exceptions here. Compare straightforward subject/language fields.
    if "keywords" in patch:
        checks["reviewed_subject_terms_present"] = after["metadata"].get("keywords") == patch["keywords"]
    if "language" in patch:
        checks["reviewed_language_present"] = after["metadata"].get("language") == patch["language"]
    for field in ("description", "notes", "upload_type", "publication_type"):
        if field in patch:
            checks[f"reviewed_{field}_present"] = after["metadata"].get(field) == patch[field]
    return checks


def build_report(base: Path) -> dict:
    approved, approved_hash = read_json(base / "APPROVED_PROPOSALS.json")
    catalog, catalog_hash = read_json(base / "SOURCE_CATALOG.json")
    entries = approved["records"]
    expected_papers = len(entries)
    if not expected_papers or len({e["id"] for e in entries}) != expected_papers:
        raise ValueError("The frozen approval must contain distinct paper records")
    if approved.get("remaining_content_reviews"):
        raise ValueError("Frozen approval still contains incomplete content reviews")
    catalog_by_id = {e["id"]: e for e in catalog}
    if len(catalog_by_id) != len(catalog):
        raise ValueError("Source catalog contains duplicate record IDs")
    included_ids = {e["id"] for e in entries}
    excluded = [{"id": e["id"], "title": e["title"],
                 "record_url": f"https://zenodo.org/records/{e['id']}",
                 "reason": e.get("reason", "outside approved paper scope"),
                 "catalog_status": e.get("status")}
                for e in catalog if e["id"] not in included_ids]
    missing_approved_catalog_ids = included_ids - set(catalog_by_id)
    if missing_approved_catalog_ids:
        raise ValueError(f"Approved papers missing from source catalog: {sorted(missing_approved_catalog_ids)}")
    if any(e.get("status") == "paper" for e in catalog if e["id"] not in included_ids):
        raise ValueError("Source catalog contains a paper without frozen approval")

    scope_path = base / "reviews/ALL_VERSIONS_SCOPE_EVIDENCE.json"
    scope, scope_hash = read_json(scope_path) if scope_path.exists() else ({}, None)
    owned_ids = set(scope.get("all_ids", catalog_by_id))
    scope_verified = (bool(scope) and len(owned_ids) == scope.get("all_versions_count")
                      and not scope.get("missing_original_ids"))
    unaccounted_owned_ids = sorted(owned_ids - set(catalog_by_id))
    if set(catalog_by_id) - owned_ids:
        raise ValueError("Source catalog contains IDs absent from the owned all-versions scope")

    audit_path = base / "reviews/FINAL_RECEIPT_AUDIT.json"
    audit, audit_hash = read_json(audit_path) if audit_path.exists() else ({}, None)
    audit_by_id = {e["id"]: e for e in audit.get("records", [])}
    inventory, inventory_hash = read_json(base / "INVENTORY.json")
    baseline_path = base / "reviews/ORIGINAL_BASELINE_HASHES.json"
    original_baselines, baseline_hash = read_json(baseline_path) if baseline_path.exists() else ({}, None)
    audit_tool_path = base / "audit_receipts.py"
    audit_tool_hash = hashlib.sha256(audit_tool_path.read_bytes()).hexdigest() if audit_tool_path.is_file() else None
    controls_path = base / "reviews/FINAL_RECEIPT_AUDIT_CONTROLS.json"
    controls, controls_hash = read_json(controls_path) if controls_path.exists() else ({}, None)
    audit_controls = audit.get("falsification_controls", {})
    controls_current = (audit_controls.get("all_passed") is True
                        and audit_controls.get("same_audit_tool") is True
                        and audit_controls.get("sha256") == controls_hash
                        and controls.get("all_passed") is True
                        and controls.get("audit_tool_sha256") == audit_tool_hash
                        and audit_tool_hash is not None
                        and audit.get("audit_tool_sha256") == audit_tool_hash
                        and audit_controls.get("count", 0) == len(controls.get("controls", [])) > 0)
    first_evidence_paths = {
        "first_staging_guard_stop": base / "receipts/23271172/first_staging_guard_stop.json",
        "draft_file_comparison": base / "reviews/FILES_DRAFT_REPRESENTATION_COMPARISON.json",
    }
    first_evidence_hashes = audit.get("first_record_representation", {}).get("evidence_sha256", {})
    first_evidence_current = (set(first_evidence_hashes) == set(first_evidence_paths)
                              and all(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == first_evidence_hashes[key]
                                      for key, path in first_evidence_paths.items()))
    native_audit_path = base / "reviews/NATIVE_FINAL_AUDIT.json"
    native_audit, native_audit_hash = read_json(native_audit_path) if native_audit_path.exists() else ({}, None)
    native_source_names = {"native_metadata.py", "native_views.py", "apply_reviewed.py", "baseline.py"}
    native_source_hashes = {"native_metadata.py": native_audit.get("source_sha256"),
                            **native_audit.get("related_source_sha256", {})}
    native_tests = native_audit.get("tests", [])
    native_audit_current = (native_audit.get("failed") == 0
                            and native_audit.get("passed") == len(native_tests) > 0
                            and all(test.get("passed") is True for test in native_tests)
                            and set(native_source_hashes) == native_source_names
                            and all((base / name).is_file()
                                    and hashlib.sha256((base / name).read_bytes()).hexdigest() == digest
                                    for name, digest in native_source_hashes.items()))
    audit_inputs_current = (audit.get("approved_manifest_sha256") == approved_hash
                            and audit.get("source_catalog_sha256") == catalog_hash
                            and audit.get("inventory_sha256") == inventory_hash
                            and baseline_hash is not None
                            and audit.get("original_baseline_manifest_sha256") == baseline_hash
                            and audit.get("all_versions_scope_evidence_sha256") == scope_hash)
    inventory_by_id = {e["id"]: e for e in inventory["records"]}
    records = []
    planned_fields, verified_fields = Counter(), Counter()

    for entry in entries:
        record_id = entry["id"]
        source_entry = catalog_by_id[record_id]
        patch_path = base / "patches" / f"{record_id}.json"
        patch_document, patch_hash = read_json(patch_path)
        patch = patch_document["metadata"]
        problems = []
        if source_entry.get("status") != "paper":
            problems.append("Approved source catalog entry is not classified as a paper")
        if patch_hash != entry["patch_sha256"]:
            problems.append("Patch hash differs from the frozen approval")
        if set(patch) != set(entry["patch_fields"]):
            problems.append("Patch field set differs from the frozen approval")
        protected = set(approved.get("protected_fields", []))
        if set(patch) & protected:
            problems.append("Patch includes a protected field")
        review_path = base / entry["independent_content_review"]
        review_hash = hashlib.sha256(review_path.read_bytes()).hexdigest() if review_path.is_file() else None
        if not review_path.is_file():
            problems.append("Independent content-review artifact is missing")
        before_path = base / "receipts" / str(record_id) / "before.json"
        after_path = before_path.with_name("after.json")
        before, before_hash = read_json(before_path)
        if original_baselines.get("records", {}).get(str(record_id), {}).get("sha256") != before_hash:
            problems.append("Public before receipt differs from the frozen original baseline hash")
        old_metadata = before["metadata"]
        if old_metadata["title"] != entry["title"]:
            problems.append("Approved title differs from the original public title")
        sources = sources_for(source_entry, base)
        if not sources:
            problems.append("No exact deposited-manuscript text is bound to this paper")
        source_summary = []
        known_files = {f["name"]: f for f in before["files"]}
        for source in sources:
            text_path = Path(source["text_path"])
            if not text_path.is_file():
                problems.append(f"Exact text artifact is missing: {source['filename']}")
            deposited = known_files.get(source["filename"])
            if not deposited or deposited["md5"] != source["md5"]:
                problems.append(f"Source checksum is not bound to the public PDF: {source['filename']}")
            source_summary.append({"filename": source["filename"], "md5": source["md5"],
                                   "text_artifact": artifact(text_path, base)})

        checks, after_hash, after = {}, None, None
        if after_path.exists():
            try:
                after, after_hash = read_json(after_path)
                checks = local_checks(before, after, entry, patch)
                problems.extend(f"Public receipt check failed: {key}" for key, passed in checks.items() if not passed)
            except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
                problems.append(f"After receipt is incomplete or invalid: {type(error).__name__}")
        public_status = "failed" if problems else ("verified" if after else "pending")
        audit_entry = audit_by_id.get(record_id, {})
        audit_receipt_hash = audit_entry.get("receipt_sha256", {})
        audit_after_hash = audit_receipt_hash.get("after") if isinstance(audit_receipt_hash, dict) else audit_receipt_hash
        audit_before_hash = audit_receipt_hash.get("before") if isinstance(audit_receipt_hash, dict) else before_hash
        allowed_receipt_names = {"before", "after", "stage", "publish", "native_staged",
                                 "native_published", "native_public_before_discard"}
        raw_receipts_current = (isinstance(audit_receipt_hash, dict)
                                and {"before", "after"} <= set(audit_receipt_hash)
                                and set(audit_receipt_hash) <= allowed_receipt_names
                                and all((before_path.parent / f"{name}.json").is_file()
                                        and hashlib.sha256((before_path.parent / f"{name}.json").read_bytes()).hexdigest() == digest
                                        for name, digest in audit_receipt_hash.items()))
        audit_bound = (audit_entry.get("status") == "pass"
                       and audit_after_hash == after_hash and audit_before_hash == before_hash
                       and audit_entry.get("patch_sha256") == patch_hash
                       and audit_entry.get("content_review_sha256") == review_hash
                       and audit_inputs_current and controls_current and raw_receipts_current
                       and first_evidence_current
                       and audit.get("status") in {"pending", "pass"}
                       and audit.get("first_record_representation", {}).get("status") == "pass")
        if audit_entry.get("status") in {"fail", "failed"}:
            problems.extend(f"Independent audit: {error}" for error in audit_entry.get("errors", []))
            public_status = "failed"

        old_terms = old_metadata.get("keywords", [])
        new_terms = patch.get("keywords", old_terms)
        old_links = old_metadata.get("related_identifiers", [])
        new_links = patch.get("related_identifiers", old_links)
        link_key = lambda link: (link["identifier"], link["relation"].lower())
        old_orcids = {creator.get("orcid") for creator in old_metadata.get("creators", [])
                      if creator.get("orcid")}
        orcids_added = [creator["orcid"] for creator in patch.get("creators", [])
                        if creator.get("orcid") and creator["orcid"] not in old_orcids]
        planned_fields.update(patch.keys())
        if public_status == "verified":
            verified_fields.update(patch.keys())
        records.append({
            "id": record_id, "title": entry["title"],
            "record_url": f"https://zenodo.org/records/{record_id}",
            "doi": before["doi"], "doi_url": f"https://doi.org/{before['doi']}",
            "status": public_status, "independently_verified": audit_bound,
            "changed_fields": list(patch),
            "specialist_terms_added": added_items(old_terms, new_terms, str.casefold),
            "specialist_terms_removed_or_rephrased": added_items(new_terms, old_terms, str.casefold),
            "subject_terms_after": new_terms,
            "related_identifiers_added": added_items(old_links, new_links, link_key),
            "related_identifiers_after": new_links,
            "orcid_identifiers_added": orcids_added,
            "language_added": patch.get("language") if not old_metadata.get("language") else None,
            "description_changed": "description" in patch,
            "notes_changed": "notes" in patch,
            "resource_type_change": {field: {"before": old_metadata.get(field), "after": patch[field]}
                                     for field in ("upload_type", "publication_type") if field in patch},
            "patch_artifact": artifact(patch_path, base), "patch_sha256": patch_hash,
            "before_receipt_artifact": artifact(before_path, base), "before_receipt_sha256": before_hash,
            "after_receipt_artifact": artifact(after_path, base) if after_path.exists() else None,
            "after_receipt_sha256": after_hash,
            "independent_content_review": artifact(review_path, base), "manuscript_sources": source_summary,
            "independent_content_review_sha256": review_hash,
            "independent_raw_receipt_evidence_current": raw_receipts_current,
            "independent_raw_receipt_evidence_hashes": audit_receipt_hash,
            "public_invariant_checks": checks, "independent_receipt_audit_status": audit_entry.get("status", "pending"),
            "errors": problems,
        })

    verified = [r for r in records if r["status"] == "verified"]
    pending = [r["id"] for r in records if r["status"] == "pending"]
    failed = [r["id"] for r in records if r["status"] == "failed"]
    independent_verified = [r for r in verified if r["independently_verified"]]
    complete = (len(verified) == expected_papers and not pending and not failed
                and len(independent_verified) == expected_papers
                and audit.get("approved_count") == expected_papers
                and audit.get("completed_count") == expected_papers
                and not audit.get("pending_ids") and not audit.get("failed_ids")
                and not unaccounted_owned_ids and scope_verified
                and audit.get("status") == "pass" and controls_current
                and first_evidence_current
                and native_audit_current
                and audit.get("first_record_representation", {}).get("status") == "pass")
    invariant_counts = Counter(key for record in verified for key, passed in record["public_invariant_checks"].items() if passed)
    excluded_inventory = {r["id"]: inventory_by_id.get(r["id"], {}) for r in excluded}
    for record in excluded:
        original = excluded_inventory[record["id"]]
        if not original:
            original = next((r for r in scope.get("new_since_inventory_or_previous_versions", []) if r["id"] == record["id"]), {})
        record["published_at_inventory"] = original.get("submitted") is True

    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "complete" if complete else ("needs_review" if failed or audit.get("status") == "fail" else "in_progress"),
        "complete": complete,
        "summary": {
            "approved_paper_records": expected_papers, "verified_public_updates": len(verified),
            "independently_verified_public_updates": len(independent_verified),
            "independent_receipt_audit_inputs_current": audit_inputs_current,
            "independent_receipt_audit_controls_current": controls_current,
            "independent_receipt_audit_global_status": audit.get("status", "missing"),
            "first_record_raw_representation_evidence_current": first_evidence_current,
            "native_metadata_route_audit_current": native_audit_current,
            "after_receipts_present": sum(r["after_receipt_artifact"] is not None for r in records),
            "pending_record_ids": pending, "failed_record_ids": failed,
            "excluded_records": len(excluded), "published_field_counts": dict(verified_fields),
            "owned_all_versions_records": len(owned_ids),
            "scope_records_accounted_for": len(catalog_by_id),
            "owned_all_versions_scope_verified": scope_verified,
            "unaccounted_owned_record_ids": unaccounted_owned_ids,
            "approved_field_counts": dict(planned_fields),
            "approved_specialist_term_additions": sum(len(r["specialist_terms_added"]) for r in records),
            "published_specialist_term_additions": sum(len(r["specialist_terms_added"]) for r in verified),
            "approved_related_links_added": sum(len(r["related_identifiers_added"]) for r in records),
            "published_related_links_added": sum(len(r["related_identifiers_added"]) for r in verified),
            "approved_orcid_additions": sum(len(r["orcid_identifiers_added"]) for r in records),
            "exact_deposited_pdf_texts_reviewed": sum(len(r["manuscript_sources"]) for r in records),
            "public_invariant_verified_counts": dict(invariant_counts),
        },
        "evidence": {
            "approved_proposals_artifact": "APPROVED_PROPOSALS.json", "approved_proposals_sha256": approved_hash,
            "approved_proposals_utc": approved.get("approved_utc"),
            "source_catalog_artifact": "SOURCE_CATALOG.json", "source_catalog_sha256": catalog_hash,
            "original_inventory_artifact": "INVENTORY.json", "original_inventory_sha256": inventory_hash,
            "original_baseline_manifest_artifact": artifact(baseline_path, base) if baseline_path.exists() else None,
            "original_baseline_manifest_sha256": baseline_hash,
            "all_versions_scope_artifact": artifact(scope_path, base) if scope_path.exists() else None,
            "all_versions_scope_sha256": scope_hash,
            "independent_receipt_audit_artifact": artifact(audit_path, base) if audit_path.exists() else None,
            "independent_receipt_audit_sha256": audit_hash,
            "independent_receipt_audit_generated_utc": audit.get("generated_utc"),
            "independent_receipt_audit_tool_sha256": audit_tool_hash,
            "independent_receipt_audit_controls_sha256": controls_hash,
            "first_record_raw_representation_evidence_hashes": first_evidence_hashes,
            "native_metadata_route_audit_artifact": artifact(native_audit_path, base) if native_audit_path.exists() else None,
            "native_metadata_route_audit_sha256": native_audit_hash,
            "native_metadata_route_audit_tests_passed": native_audit.get("passed", 0),
            "native_metadata_route_source_sha256": native_source_hashes,
        },
        "scope": "Published manuscript records, including the existing line-numbered qubit presentation. Supporting codebase, dataset, source, manifest deposits and the unpublished draft were excluded.",
        "method": "Manuscript-first specialist metadata proposals based on checksum-bound exact published PDF texts, independently cross-reviewed before metadata-only publication, with public before/after receipt comparisons and independent final auditing.",
        "impact": {"search_rank_improvement_measured": False, "readership_improvement_measured": False,
                   "statement": "The work improves metadata relevance and completeness. Actual search ranking, indexing uptake and expert readership improvement were not measured."},
        "records": records, "excluded": excluded,
    }


def cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    rows = ["# Zenodo paper discovery metadata results", "", f"Generated: {report['generated_utc']}", ""]
    if report["complete"]:
        rows += [f"**Complete: all {summary['approved_paper_records']} existing paper records have published metadata updates and matching independent public-receipt audits.**", ""]
    else:
        rows += [f"**Provisional — {summary['verified_public_updates']}/{summary['approved_paper_records']} public updates verified locally; "
                 f"{summary['independently_verified_public_updates']}/{summary['approved_paper_records']} have matching independent final audits.**", "",
                 "This report does not claim completion. It requires every approved final public receipt, a matching independent audit, and a scope disposition for every owned record.", ""]
        if summary["pending_record_ids"]:
            rows += ["Pending publication receipts: " + ", ".join(map(str, summary["pending_record_ids"])) + ".", ""]
        if summary["failed_record_ids"]:
            rows += ["Records requiring review: " + ", ".join(map(str, summary["failed_record_ids"])) + ".", ""]
        if summary["unaccounted_owned_record_ids"]:
            rows += ["Owned records awaiting scope disposition: " + ", ".join(map(str, summary["unaccounted_owned_record_ids"])) + ".", ""]
        if not summary["independent_receipt_audit_inputs_current"]:
            rows += ["The independent receipt audit awaits regeneration against the current approval, source catalog and ownership scope. Older audit results are not counted as matching final audits.", ""]
        if not summary["independent_receipt_audit_controls_current"]:
            rows += ["The independent audit and its falsification controls must be rerun against the current audit-tool bytes before final audit results are counted.", ""]
        if summary["independent_receipt_audit_global_status"] == "fail":
            rows += ["The independent receipt audit reports a global failure. Completion is blocked until that failure is resolved.", ""]
        if not summary["first_record_raw_representation_evidence_current"]:
            rows += ["The first publication's raw representation evidence must match the independent audit before final results are counted.", ""]
        if not summary["native_metadata_route_audit_current"]:
            rows += ["The native metadata workflow audit awaits passing tests bound to the current workflow source files before completion can be claimed.", ""]
    rows += [report["method"], "", report["impact"]["statement"], "",
             f"Scope: {summary['approved_paper_records']} approved paper records and {summary['excluded_records']} excluded records; "
             f"{summary['scope_records_accounted_for']}/{summary['owned_all_versions_records']} owned records accounted for.", "",
             "## Changes", "", "| Metadata field | Published and verified | Approved total |",
             "| --- | ---: | ---: |"]
    for field, count in sorted(summary["approved_field_counts"].items()):
        rows.append(f"| {cell(LABELS.get(field, field))} | {summary['published_field_counts'].get(field, 0)} | {count} |")
    rows += ["", f"Specialist term additions: {summary['published_specialist_term_additions']} verified / "
             f"{summary['approved_specialist_term_additions']} approved. Related links added: "
             f"{summary['published_related_links_added']} verified / {summary['approved_related_links_added']} approved. "
             f"Approved author ORCID additions: {summary['approved_orcid_additions']}. "
             f"Exact deposited PDF text sources reviewed: {summary['exact_deposited_pdf_texts_reviewed']}.", "",
             "## Preservation evidence", "",
             "For records marked verified, published before/after receipts verify the existing record DOI, concept record, complete version history, "
             "public PID set, original title/date/version/license/access, custom fields, and full native file identities, "
             "checksums, sizes, access and preview settings. The independent receipt audit also checks reviewed changes "
             "and preservation of all rich metadata outside the approved patch. No new record, DOI, version or file "
             "upload is part of this metadata workflow.", "",
             "| Public check | Verified records |", "| --- | ---: |"]
    for check, count in sorted(summary["public_invariant_verified_counts"].items()):
        if check.startswith("reviewed_") or check == "publisher_verification_present":
            continue
        rows.append(f"| {cell(check.replace('_', ' '))} | {count} |")
    rows += ["", "The report binds each result to its frozen approved patch hash, exact manuscript source, "
             "independent content review, and public receipts. Detailed evidence and receipt hashes are in [RESULTS.json](RESULTS.json).", "",
             "## Paper records", "", f"All {summary['approved_paper_records']} approved records are listed, including those still pending in a provisional report.", "",
             "| Paper | Status | Metadata fields | Added specialist terms |", "| --- | --- | --- | --- |"]
    for record in report["records"]:
        status = {"verified": "Public update verified", "pending": "Pending", "failed": "Needs review"}[record["status"]]
        if record["independently_verified"]:
            status += "; independent audit passed"
        fields = "; ".join(LABELS.get(field, field) for field in record["changed_fields"])
        terms = "; ".join(record["specialist_terms_added"]) or "Existing terms retained"
        rows.append(f"| [{cell(record['title'])}]({record['record_url']}) ({record['id']}) | "
                    f"{cell(status)} | {cell(fields)} | {cell(terms)} |")
    rows += ["", "## Excluded records", "", f"These {summary['excluded_records']} records were outside the authorized published-paper metadata scope.", "",
             "| Record | Reason |", "| --- | --- |"]
    for record in report["excluded"]:
        rows.append(f"| [{cell(record['title'])}]({record['record_url']}) ({record['id']}) | {cell(record['reason'])} |")
    errors = [(r["id"], error) for r in report["records"] for error in r["errors"]]
    if errors:
        rows += ["", "## Issues requiring review", ""]
        rows.extend(f"- {record_id}: {cell(error)}" for record_id, error in errors)
    rows += ["", "## Evidence files", "", "- [Frozen reviewed proposals](APPROVED_PROPOSALS.json)",
             "- [Exact manuscript source catalog](SOURCE_CATALOG.json)",
             "- [Original inventory](INVENTORY.json)",
             "- [Frozen original public baselines](reviews/ORIGINAL_BASELINE_HASHES.json)",
             "- [Final native metadata workflow audit](reviews/NATIVE_FINAL_AUDIT.json)",
             "- [Independent final receipt audit](reviews/FINAL_RECEIPT_AUDIT.md)",
             "- Per-paper before/after receipts and content-review paths are listed in [RESULTS.json](RESULTS.json).", ""]
    if report["evidence"]["all_versions_scope_artifact"]:
        rows.insert(-1, "- [All-versions ownership scope](reviews/ALL_VERSIONS_SCOPE_EVIDENCE.json)")
    return "\n".join(rows)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-complete", action="store_true",
                        help="Write the report, then exit nonzero unless every approved final receipt and audit passes")
    args = parser.parse_args(argv)
    report = build_report(HERE)
    for name, contents in (("RESULTS.json", json.dumps(report, indent=2, ensure_ascii=False) + "\n"),
                           ("RESULTS.md", render_markdown(report))):
        temporary = HERE / (name + ".tmp")
        temporary.write_text(contents)
        temporary.replace(HERE / name)
    print(json.dumps({"status": report["status"], "complete": report["complete"],
                      "verified": report["summary"]["verified_public_updates"],
                      "independently_verified": report["summary"]["independently_verified_public_updates"],
                      "pending": len(report["summary"]["pending_record_ids"]),
                      "failed": report["summary"]["failed_record_ids"],
                      "outputs": [str(HERE / "RESULTS.md"), str(HERE / "RESULTS.json")]}, indent=2))
    return 1 if args.require_complete and not report["complete"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
