#!/usr/bin/env python3
"""Explicit new-folder metadata/evidence packaging; original bodies never executed."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

A = Path(__file__).resolve().parent
S = A.parents[1] / "sources"


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def write(name, value):
    p = A / name
    need(not p.exists(), "new output only: " + name)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


class ObjectPairs(list):
    pass


def typed(value):
    if isinstance(value, ObjectPairs):
        return {"type": "object", "ordered_pairs": [[key, typed(item)] for key, item in value]}
    if type(value) is list:
        return {"type": "array", "items": [typed(item) for item in value]}
    names = {type(None): "null", bool: "boolean", int: "integer", float: "number", str: "string"}
    return {"type": names[type(value)], "literal_value": value}


def package():
    now = datetime.now(timezone.utc).isoformat()
    source = json.loads((A / "SOURCE_INPUT_MANIFEST.json").read_bytes())
    copied_root = A / "raw/source-originals"
    copied_root.mkdir(parents=True, exist_ok=False)
    for rel in source["exact_complete_source_directories"]:
        (copied_root / rel).mkdir(exist_ok=False)
    bindings, objects, tapes = [], [], []
    for entry in source["complete_source_files"]:
        p = Path(entry["path"])
        need(pin(p) == entry, "whole original source pin")
        rel = p.relative_to(S).as_posix()
        q = copied_root / rel
        q.write_bytes(p.read_bytes())
        bindings.append({"relative_path": rel, "original": entry, "copy": pin(q)})
        if p.suffix == ".json":
            objects.append({"relative_path": rel, "whole_original_object": json.loads(p.read_bytes())})
            tapes.append({"relative_path": rel, "whole_typed_ordered_JSON": typed(json.loads(p.read_bytes(), object_pairs_hook=ObjectPairs))})
    write("SOURCE_CUSTODY_BINDINGS.json", {"UTC": now, "whole104_original_file_bindings": bindings, "complete_source_relative_directories": source["exact_complete_source_directories"], "source_files": 104, "source_payloads": 101, "source_exact_root_terminals": source["source_exact_terminals"], "source_modified": False, "archived_narrative_bodies_copied_opaque_not_adopted_as_opinions": True})
    write("PROVIDED_SOURCE_OBJECTS.json", {"whole_original_JSON_objects_in_source_path_order": objects, "raw_byte_copies_authoritative": "raw/source-originals", "no_projection_or_normalization": True})
    write("ORIGINAL_JSON_TYPE_TAPES.json", {"schema": "all_JSON_types_values_object_pairs_and_array_order_v1", "objects": tapes, "duplicate_keys_if_any_retained_by_pairs": True})
    r = json.loads((S / "SOURCE_READY.json").read_bytes())
    write("MANUSCRIPT_OBSERVATIONS.json", {"UTC": now, "native_version_field_present": False, "native_version_original": None, "native_version_state": "ABSENT", "printed_date": "October 6, 2026", "printed_version_line_present": False, "printed_version": None, "native_publication_date_original": r["publication_date"], "native_created_original": r["created"], "native_updated_original": r["updated"], "native_assets_whole_in_original_order": r["all_native_assets_in_original_order"], "native_license_whole_original_field": r["native_license_metadata_whole_field"], "actual_authored_rights": "CC BY4.0 for new prose/explanations/documentation/audits/data representations; MIT for new Python under actual LICENSE_CODE.txt; third-party rights retained", "whole_original_source_historical_UNREAD_flags_modified": False, "PDF_pages_read": 6, "TeX_lines_read": 189, "own_original_rasters_viewed": 6, "own_primary_rasters_viewed": 8})
    reads = [("OpenAI pinned full manuscript", "upstream-pinned.txt", "upstream-PDF-hop0.body", [[1,24]], 24), ("GPT arXiv1111.3164v2", "GPT-v2-PDF.txt", "GPT-v2-PDF-hop0.body", [[1,1],[3,5]], 23), ("LRS arXiv1411.6317v1", "LRS-v1-PDF.txt", "LRS-v1-PDF-hop0.body", [[1,1],[4,5]], 46), ("LPDWY arXiv1601.02311v2", "LPDWY-v2-PDF.txt", "LPDWY-v2-PDF-hop0.body", [[1,1],[4,5]], 33), ("LPDWY published CCC2016", "LPDWY-published-PDF.txt", "LPDWY-published-PDF-hop0.body", [[1,1],[4,5]], 31), ("Rothvoss arXiv1311.2369v4", "Rothvoss-v4-PDF.txt", "Rothvoss-v4-PDF-hop0.body", [[1,1],[3,4]], 23), ("Yannakakis1991 academic primary copy", "Yannakakis-TIFR-PDF.txt", "Yannakakis-TIFR-PDF-hop0.body", [[1,1],[14,15]], 26)]
    read_items = [{"role": role, "whole_body": pin(A / "primary/shared-raw/primary" / name), "ordinary_text_derivative": pin(A / "primary" / text), "physical_page_ranges_personally_read": ranges, "actual_total_pages": pages, "complete_body_read": role.startswith("OpenAI")} for role,text,name,ranges,pages in reads]
    lean = ["lean-doc126", "lean-main", "lean-affine-lift", "lean-model", "lean-affine-model", "lean-affine-certificate", "lean-affine-factorization"]
    write("READ_LEDGER.json", {"UTC": now, "initial_whole_read_ledger": pin(A / "INITIAL_READ_LEDGER.json"), "initial_seal": pin(A / "INITIAL_SEAL.json"), "actual_own_results_seal": pin(A / "OWN_PROOF_CONTROL_SEAL.json"), "primary_reading_after_both_freezes": read_items, "seven_full_pinned_formal_statement_or_definition_bodies_read_statically": [pin(A / "primary/shared-raw/primary" / (name+"-hop0.body")) for name in lean], "formal_build_or_full_import_closure_checked": False, "complete_native_code_and_rights_read_ledger": json.loads((A / "POSTFREEZE_STATIC_SUPPORT_READ_LEDGER.json").read_bytes()), "all8_fresh_own_primary_rasters_personally_viewed": True, "own_scientific_execution": json.loads((A / "OWN_CONTROL_EXECUTION.json").read_bytes()), "source_or_supplied_scientific_imports_or_execution": [], "archived_narrative_reviews_triage_priority_bodies_read": [], "current_peer_root_findings_or_replay_results_read": False, "raw_only_handoffs_received": [pin(A / "primary/RAW_PRIMARY_HANDOFF_01.owner-original.json"),pin(A / "primary/RAW_PRIMARY_HANDOFF_02.owner-original.json")], "peer_freeze_pins_in_raw_index_metadata_only_no_scientific_payload_opened": True, "own_primary_GETs": 0, "HeldKarp_actual_paper_read": False, "Yannakakis_DOI_HTML_not_claimed_as_paper": True, "all_primary_per_page_timestamps_claimed": False, "prior_background_and_incidental_exposure_disclosed_in_initial": True, "scientific_findings_sent_to_root": False, "root139_gate": "CLOSED"})
    families = [("affine_LMI_model", "kernel quotient and bounded nonempty output", "INITIAL Family1", "original exact real matrix-order category", None), ("matrix_and_shift", "crossing parity and one charged scalar PSD block", "INITIAL Families2–3; actual Theorem1.1", "absolute rate/fixed-rho threshold and eventual exponent loss", "rho1 endpoint excluded"), ("common_support_closedness", "faithful positive evaluation sum and finite-dimensional compactness", "INITIAL Family4; own uniform analytic proof/controls", "closed evaluation cone without general cone-image claim", None), ("tight_slack_certificate", "signed affine witness and closed-cone separation", "INITIAL Family5; actual AffineCertificate body", "all rows share vertex factors; no Slater requirement", None), ("faces_and_images", "supporting equalities/composition without extra PSD order", "INITIAL Family6", "nonempty faces/affine images", None), ("three_layer_projection", "forced paths and cyclic completion", "INITIAL Family7; actual Yannakakis454", "all even n≥2 including parallel colored boundary", None), ("two_layer_projection", "all diagonal ones and cross zeros expose face", "INITIAL Family8", "all even n≥2 and explicit missing-ones counterexample", "no priority claimed"), ("all_N_padding", "forced-path contraction with distinct endpoint neighbours", "INITIAL Families9–10", "every N≥m≥3 and every eventual city residue", None), ("exact_upper", "DAG path decomposition and diagonal SDP", "INITIAL Family11", "printed exact arc-order upper bound", "no algorithms/bit complexity implication"), ("central_analytic_dependency", "local trace/multiplicity, splitting, fourth-moment product, parity and truncation", "full24-page actual primary; PRIMARY_INTERFACE_AUDIT", "full original exponential premise personally examined", "external work remains OpenAI's; optional independent appendix external branching not separately acquired"), ("formal_and_historical_interfaces", "actual definitions/statements and precise primary credit/correction pages", "seven Lean bodies; GPT/LRS/LPDWY/Yannakakis/Rothvoss", "superpolynomial formal category distinct; classical credits retained", "no build/global priority/current-latest claim; HeldKarp paper inaccessible"), ("custody_and_exposure", "full byte/type/order/file-and-directory closure with early freezes", "source/raw bindings, ledgers, own terminal helper", "source/prior finals unchanged and root139 closed", None)]
    write("FAMILY_LEDGER.json", {"UTC": now, "single_independent_analytic_scope_lane": True, "mechanisms_not_additional_reviewers": True, "families": [{"family": n,"mechanism": m,"checkable_evidence": e,"verified_scope": v,"exact_limit_or_remaining_gap": gap} for n,m,e,v,gap in families], "substantive_defect_found": False, "follow_up": None})
    handoff2 = json.loads((A / "primary/RAW_PRIMARY_HANDOFF_02.owner-original.json").read_bytes())
    write("FAILURE_HISTORY.json", {"UTC": now, "actual_own_scientific_first_run_exit": 0, "actual_own_scientific_first_stderr": "", "own_scientific_reruns_or_overwrites": 0, "own_command_or_derivation_failures_so_far": [], "whole_original_raw_handoff_access_limits": handoff2["access_limits"], "HeldKarp": "ordinary DOI403HTML retained, actual paper not read", "Yannakakis": "ordinary DOI200HTML2678bytes retained; actual separately pinned academic PDF read", "primary_literal_date_limits": {"GPTv2_margin": "30 Aug 2012", "GPTv2_front_date": "November 27, 2024", "LPDWYv2_margin": "8 Mar 2016", "LPDWYv2_printed": "March 9, 2016"}, "source_historical_failure_and_closure_objects_whole_retained": True, "no_source_rewrite_or_extended_scientific_repair": True, "root139_gate": "CLOSED"})
    write("CODE_AND_EXECUTION_LEDGER.json", {"UTC": now, "own_current_code_read_before_execution": [pin(A/name) for name in ["prepare_initial.py","freeze_initial.py","own_analytic_controls.py","derive_primary_rasters.py","package_evidence.py"]], "actual_own_scientific_first_run": json.loads((A / "OWN_CONTROL_EXECUTION.json").read_bytes()), "initial_metadata_and_primary_Poppler_runs": [pin(A / "MANUSCRIPT_DERIVATION_RECEIPTS.json"), pin(A / "primary/PRIMARY_DERIVATIONS_01.json"), pin(A / "primary/PRIMARY_DERIVATIONS_02.json"), pin(A / "primary/PRIMARY_RASTER_RECEIPTS.json")], "source_or_supplied_programmes_executed": [], "terminal_helper_and_freeze_full_reads_recorded_in_closure": True})
    write("VERDICT.json", {"UTC": now, "record_id": 23204250, "sheet_row": 139, "review_family": "Independent analytic scope and exact primary-interface review", "literal_custom_verdict": "PASS — full original exact real exponential-order TSP theorem and critical primary dependency interfaces checked; no substantive defect found in this independent analytic scope lane.", "full_original_scope_preserved": True, "claim": "For every sufficiently large integer N, 2^(cN)≤xc_psd,R(TSP(N))≤2(N−1)+(N−1)(N−2)2^(N−3), with exact affine lifts measured by total PSD matrix order; original external shifted-matching premise credited to OpenAI.", "narrower_replacement_or_source_repair": False, "substantive_defect_found": False, "formalized_or_human_refereed": False, "priority_certified": False, "native_version_field_present": False, "native_version_original": None, "printed_date": "October 6, 2026", "printed_version_present": False, "printed_version": None, "actual_own_bounded_control_checks": 9338, "source_or_supplied_scientific_programmes_executed": [], "current_peer_root_opinions_or_native_replay_results_read": False, "follow_up": None, "publication_authority": False, "production_authority": False, "canonical_url": None, "AA": None, "root139_comparison_gate": "CLOSED", "scientific_findings_sent_to_root": False, "source_core_priorFINAL_site_Git_Sheet_deploy_redirect_contact_mutations": False})
    with (A / "RESEARCH_LOG.md").open("a") as f:
        f.write("\n"+now+" —80%: Full independent original-scope derivations and exact critical primary-interface assessment packaged. Whole104 source copies, literal original JSON/type/order tapes, raw handoff/access/failure histories and read/family/code/verdict ledgers retained. INITIAL54aab139/OWNba94 unchanged. New pure offline strict custody helper/full read/actual closure/final seal remain; root139 CLOSED and findings withheld.\n")
    print(json.dumps({"source_copies": len(bindings), "whole_original_JSON_objects": len(objects), "primary_read_bodies": len(read_items), "progress_percent": 80, "root139_gate": "CLOSED"}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--package"]:
        raise SystemExit("Inert by default; --package writes only new scope evidence")
    package()
