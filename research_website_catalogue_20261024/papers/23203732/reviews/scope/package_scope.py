#!/usr/bin/env python3
"""Explicit new scope evidence packaging; copies original bytes, never executes them."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

A = Path(__file__).resolve().parent
S = A.parents[1] / "sources"


def pin(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "SHA256": hashlib.sha256(b).hexdigest()}


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def write(name, obj):
    p = A / name
    require(not p.exists(), "new output only: " + name)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def typed(value):
    if isinstance(value, ObjectPairs):
        return {"type": "object", "ordered_pairs": [[key, typed(item)] for key, item in value]}
    if type(value) is list:
        return {"type": "array", "items": [typed(item) for item in value]}
    names = {type(None): "null", bool: "boolean", int: "integer", float: "number", str: "string"}
    return {"type": names[type(value)], "literal_value": value}


class ObjectPairs(list):
    pass


def package():
    now = datetime.now(timezone.utc).isoformat()
    inputs = json.loads((A / "SOURCE_INPUT_MANIFEST.json").read_bytes())
    out = A / "raw/source-originals"
    out.mkdir(parents=True, exist_ok=False)
    for rel in inputs["exact_complete_source_directories"]:
        (out / rel).mkdir(exist_ok=False)
    bindings, objects, tapes = [], [], []
    for original in inputs["complete_source_files"]:
        p = Path(original["path"])
        require(pin(p) == original, "original source whole pin")
        rel = p.relative_to(S).as_posix()
        q = out / rel
        body = p.read_bytes()
        q.write_bytes(body)
        require(q.read_bytes() == body, "whole source copy")
        bindings.append({"relative_path": rel, "original": original, "copy": pin(q)})
        if p.suffix == ".json":
            obj = json.loads(body)
            objects.append({"relative_path": rel, "original_whole_object": obj})
            tapes.append({"relative_path": rel, "original_byte_pin": original, "whole_typed_ordered_JSON": typed(json.loads(body, object_pairs_hook=ObjectPairs))})
    write("SOURCE_CUSTODY_BINDINGS.json", {"UTC": now, "complete_original_source_root": str(S), "scope_copy_root": str(out), "whole_file_bindings": bindings, "complete_relative_directories": inputs["exact_complete_source_directories"], "source_files": 101, "payloads": 98, "exact_source_root_terminals": inputs["source_exact_terminals"], "source_modified": False, "historical_UNREAD_flags_retained": True, "archived_narrative_bodies_copied_opaque_not_read_as_opinions": True})
    write("PROVIDED_SOURCE_OBJECTS.json", {"UTC": now, "whole_original_JSON_objects_in_source_path_order": objects, "authoritative_raw_byte_copies": "raw/source-originals", "no_field_projection_or_normalization": True})
    write("ORIGINAL_JSON_TYPE_TAPES.json", {"schema": "JSON_all_key_pairs_array_order_and_literal_types_v1", "objects": tapes, "raw_byte_copies_authoritative": True, "duplicates_if_present_retained_in_ordered_pairs": True})
    ready = json.loads((S / "SOURCE_READY.json").read_bytes())
    write("MANUSCRIPT_OBSERVATIONS.json", {"UTC": now, "native_version_field_present": False, "native_version_original": None, "native_version_state": "ABSENT", "printed_date_observed": "October 6, 2026", "printed_version_line_present": False, "printed_version": None, "native_publication_date_original": ready["publication_date"], "native_created_original": ready["created"], "native_updated_original": ready["updated"], "all_native_assets_whole_in_original_order": ready["all_native_assets_in_original_order"], "native_license_whole_original_field": ready["native_license_metadata_whole_field"], "authored_note_code_audit_text_rights": "CC BY 4.0 according to deposited README; no MIT claim", "full_PDF_pages_read": 6, "full_controlling_TeX_lines_read": 198, "fresh_own_manuscript_rasters_viewed": 6, "fresh_own_primary_rasters_viewed": 8, "embedded_PDF_whole_byte_equal": True, "source_acquisition_historical_false_null_flags_modified": False, "new_observations_not_backdated_into_source": True})
    primary_reads = [
        {"role": "OpenAI pinned complete theorem/proof", "PDF": "primary/openai-pinned.pdf", "physical_pages": [[1,27]], "total_body_pages": 27, "read_kind": "complete scientific manuscript", "scope": "Theorem1.1 and every compression/deployment/transfer/expansion/planar/rank/conclusion proof"},
        {"role": "Gaboriau2002 published", "PDF": "primary/gaboriau-2002.pdf", "physical_pages": [[1,2],[13,15],[33,38]], "total_body_pages": 58, "read_kind": "complete critical ranges only", "scope": "global measure hypotheses, dimension Properties1.2, Cor3.16, Properties3.15, Cor3.23, historical question"},
        {"role": "Gaboriau2000 author PDF", "PDF": "primary/shared-raw/primary/extra-v3/gaboriau-2000-author.hop0.body", "physical_pages": [[8,11]], "total_body_pages": 58, "read_kind": "complete critical ranges only", "scope": "graphing/cost/infimum/fixed-price definitions, finite-class correction"},
        {"role": "Gaboriau FAQ", "PDF": "primary/shared-raw/primary/extra-v2/gaboriau-faq.hop0.body", "physical_pages": [[1,1]], "total_body_pages": 5, "read_kind": "complete critical page only", "scope": "historical questions and exact locators"},
        {"role": "Gaboriau lecture notes", "PDF": "primary/shared-raw/primary/extra-v2/gaboriau-notes.hop0.body", "physical_pages": [[19,23]], "total_body_pages": 62, "read_kind": "complete critical ranges only", "scope": "Theorem2.64 and distinct Question2.65 assertions; actual printed date October3,2025"},
        {"role": "PSV arXiv1811.06929v1", "PDF": "primary/shared-raw/primary/extra-v3/psv-v1-pdf.hop0.body", "physical_pages": [[1,1],[22,25]], "total_body_pages": 31, "read_kind": "complete critical ranges only", "scope": "front16Nov2018 and all Remark6.6 across24–25 plus terminology"},
        {"role": "Lueck arXiv-labelled v1 body", "PDF": "primary/shared-raw/primary/extra-v3/lueck-v1-pdf.hop0.body", "physical_pages": [[1,1],[8,20]], "total_body_pages": 94, "read_kind": "complete critical ranges only", "scope": "Theorem1.11, group/cellular definitions, reduced Hilbert quotient §2.3 at18–19; literal2003margin/2018title dates both retained"},
        {"role": "Hatcher author PDF", "PDF": "primary/shared-raw/primary/extra-v2/hatcher-author.hop0.body", "physical_pages": [[3,3],[353,356],[375,377]], "total_body_pages": 560, "read_kind": "contents and complete critical ranges only", "scope": "Whitehead4.5, Hurewicz4.32, homology Whitehead4.33 and simple-connectedness boundary"}
    ]
    for item in primary_reads:
        item["whole_body"] = pin(A / item["PDF"])
    codes = ["verification/check_fox.py", "verification/finite_boundary_check.py", "verification/verify_constants.py", "verification/verify_exact.py"]
    support = ["README.md", "DEPENDENCIES.md", "verification/check_fox_results.json", "verification/constants_certificate.json", "verification/exact_certificate.json", "verification/finite_boundary_results.json", "reproducibility/clean_reproduction.json", "reproducibility/software_versions.json", "reproducibility/upstream_tex_adaptation.json", "upstream/UPSTREAM_MANIFEST.json"]
    base = S / "published-source/asset-002"
    ledger = {"UTC": now, "record_id": 23203732, "root_gate": "CLOSED", "initial_whole_ledger_retained": pin(A / "INITIAL_READ_LEDGER.json"), "paper_first_initial": pin(A / "INITIAL_SEAL.json"), "own_proof_results_before_foreign_or_native_science": pin(A / "OWN_PROOF_CONTROL_SEAL.json"), "primary_actual_read_ranges": primary_reads, "all8_primary_rasters_personally_viewed": True, "primary_raster_actual_numeric_pages_control_over_descriptive_filenames": True, "supplied_code_bodies_fully_read_statically_after_own_results_seal": [pin(base / name) for name in codes], "supplied_support_or_historical_result_bodies_read_after_own_results_seal": [pin(base / name) for name in support], "pinned_actual_INPUTS_and_references_and_figure_source_read_not_executed": True, "supplied_scientific_imports_or_executions": [], "native_replay_owner": "sol_exact11_safety_audit only; current replay result not read by scope", "own_only_scientific_execution": pin(A / "OWN_CONTROL_EXECUTION.json"), "archived_narrative_review_priority_or_triage_bodies_read": [], "author_audit_assertions_seen_in": ["actual full manuscript", "README.md", "DEPENDENCIES.md"], "author_audit_assertions_used_as_independent_proof": False, "current_peer_root_findings_read": False, "prior_metadata_only_acquisition": True, "prior_unrelated_excluded_row134_opinion_exposure": True, "prior_record137_scientific_opinion_exposure": False, "own_primary_GETs": 0, "Fox_actual_paper_body_read": False, "Fox_access_limit": "Preserved HTTP200 Client Challenge HTML, not paper; prefix derivation is self-contained", "page_read_timestamps": "Only run/phase timestamps were captured; per-page wall-clock timestamps are not invented", "scientific_findings_sent_to_root": False}
    write("READ_LEDGER.json", ledger)
    write("CODE_AND_EXECUTION_LEDGER.json", {"UTC": now, "current_own_code": [pin(A / name) for name in ["prepare_initial.py", "own_exact_controls.py", "derive_primary_views.py", "package_scope.py"]], "all_owned_current_code_fully_read_before_its_actual_execution": True, "source_or_scientific_helpers_imported_or_executed": [], "ordinary_Poppler_derivations_only_separate_from_own_math_control": True, "actual_own_math_execution": json.loads((A / "OWN_CONTROL_EXECUTION.json").read_bytes()), "actual_primary_derivation_stdout": '{"decoded_PDF_byte_equal": true, "Git_blob_SHA1_matches": true, "fresh_own_primary_rasters": 8, "own_primary_GETs": 0}\n', "actual_primary_derivation_stderr": "", "actual_primary_derivation_exit_code": 0, "first_and_current_own_control_results_same_no_rerun": True, "supplied_static_checker_limit": "Uses asserts; -O may remove predicates. No optimized native validation is claimed here.", "terminal_helper_source_read_and_closure_record": "CLOSURE.json once final, no scientific execution"})
    families = [
        ("group_and_J_embedding", "normal form and reduced words", "INITIAL_DERIVATIONS Families1,3; exact free-basis inverse controls", "verified original fixed group/presentation", None),
        ("actions_and_ergodicity", "Bernoulli cylinders plus finite-height sections", "INITIAL Family2; actual OpenAI §2", "verified all positive M for action lemma", None),
        ("two_layer_tree", "free reduced alternating words", "INITIAL Family4; bounded cyclic-label falsifiers", "uniform actual degree100 proof", "finite enumeration only degrees2–5/length≤8"),
        ("infinite_tree_kernel", "layer energies and coset decomposition", "INITIAL Family5; finite-path negative control", "injective right S and t−1", "no bounded inverse or spectral-gap claim"),
        ("ordered_boundary", "lifted prefix derivatives in noncommutative ring", "INITIAL Family6; own full ordered ring controls", "all coordinates/d1d2/injection verified", None),
        ("integral_asphericity", "simply connected acyclic CW + Hurewicz/Whitehead", "INITIAL Family7; actual Hatcher critical statements", "original2Dcomplex K(Γ,1)", None),
        ("auxiliary_tree_of_spaces", "contractible Bass–Serre tree of mapping cylinders", "OWN_UNIVERSAL_PROOF; final CW generator-elimination clarification", "independent auxiliary topology route", "does not replace edge-map control for L2 dimensions"),
        ("all_degree_reduced_dimension", "faithful finite Hilbert-module dimension", "INITIAL Family8; actual Gab2002/Lueck interfaces", "every beta_n vanishes", None),
        ("graphing_upper_and_cost_infimum", "Borel complete t-section + exact height induction", "INITIAL Families9,11; own height negative controls", "full original M>100 upper bound and infimum1", "no attained minimum asserted"),
        ("exact_parameter", "unbounded integer and rational inequalities", "OWN_EXACT_RESULTS; initial Family10", "alpha2^-61 and eta alpha/100 admissible", "arithmetic alone is not positive-cost proof"),
        ("external_positive_cost", "compression/deployment/finite rank/planar shortening", "full27actualOpenAIpages; PRIMARY_INTERFACE_AUDIT", "exact original theorem body/proof interfaces checked", "external attribution retained, not new target discovery"),
        ("classical_invariance_and_credit", "actual published statement/hypothesis and v1credit bodies", "Gab2002Cor3.16/3.23; Gab2000I.5; PSVv1Remark6.6", "nonergodic scope and historical credit retained", "Fox paper unavailable; explicit direct derivation sufficient; no global priority audit"),
        ("custody_and_exposure", "whole bytes/types/order/namespace with early seals", "SOURCE_INPUT/RAW bindings/READ ledger/terminal helper", "original historical fields and independent chronology retained", "root137comparison CLOSED; no consensus proof")
    ]
    write("FAMILY_LEDGER.json", {"UTC": now, "single_independent_scope_lane": True, "different_mechanisms_not_additional_reviewers": True, "families": [{"family": f, "mechanism": m, "checkable_evidence": e, "status": st, "exact_limit_or_remaining_gap": gap} for f,m,e,st,gap in families], "substantive_defect_found": False, "follow_up": None})
    owner = json.loads((A / "primary/RAW_HANDOFF_INDEX.owner-original.json").read_bytes())
    write("FAILURE_HISTORY.json", {"UTC": now, "whole_owner_raw_index": pin(A / "primary/RAW_HANDOFF_INDEX.owner-original.json"), "initial_owner_transport_qualification_literal": owner["initial_transport_qualification"], "first_additional_attempt_whole_original_object": owner["partial_first_additional_attempt"], "source_failures_whole_retained_in": "raw/source-originals and original source", "own_display_failure": {"operation": "oversized text display of FAQ1/Gab2000pages8–11/notes19–23", "observed_result": "Output exceeded the available model context and was truncated", "scientific_content_counted_as_read_from_failed_call": False, "bounded_followup": "All required pages reread in bounded separate calls; no repeated GET or derivative needed"}, "primary_raster_label_qualification": {"openai-planar": "numeric physical14 is transfer proposition", "openai-rank": "numeric physical18 is planar lemma", "all8_outputs_personally_viewed": True}, "Fox_attempt": "HTTP200 Client Challenge HTML retained, no paper claimed, no bypass", "Lueck_actual_dual_date_strings": ["arXiv:math/0310489v1 31 Oct 2003", "October 24, 2018"], "own_scientific_control_first_run": "exit0; first streams retained; no rerun or result overwrite", "native_supplied_scientific_execution_in_this_lane": False, "extended_repair_or_source_rewrite": False, "no_failure_history_removed": True})
    write("VERDICT.json", {"UTC": now, "record_id": 23203732, "sheet_row": 137, "review_family": "Independent scientific scope/source-interface lane", "literal_custom_verdict": "PASS — full original theorem and exact primary dependency interfaces checked; no substantive defect found in this independent scope lane.", "full_original_scope_preserved": True, "claim": "Original101-generator100-relator complex is a finite2D K(Γ,1); all group and every essentially-free-pmp action relation Betti numbers vanish; specified X and all Y_M are free ergodic pmp; original M>100 upper bound implies group infimum cost1; pinned OpenAI theorem supplies Bernoulli cost≥1+1/(100·2^61).", "proof_record": ["INITIAL_DERIVATIONS.md", "OWN_UNIVERSAL_PROOF.md", "DERIVATIONS.md", "PRIMARY_INTERFACE_AUDIT.md"], "substantive_defect_found": False, "narrower_replacement_used": False, "native_version_field_present": False, "native_version_original": None, "native_version_state": "ABSENT", "printed_date": "October 6, 2026", "printed_version_present": False, "printed_version": None, "follow_up": None, "source_scientific_programmes_executed": [], "own_bounded_control_checks": 82947, "current_peer_or_root_scientific_findings_read": False, "archived_narrative_opinions_used_as_proof": False, "formalized_or_human_refereed_claim": False, "priority_certified": False, "root137_comparison_gate": "CLOSED", "scientific_findings_sent_to_root": False, "publication_authority": False, "production_authority": False, "canonical_url": None, "AA": None, "contacts_or_prepared_outreach": False, "source_site_Git_Sheet_core_redirect_deploy_mutations": False})
    with (A / "RESEARCH_LOG.md").open("a") as f:
        f.write("\n" + now + " —80%: Resumed after checkpoint0ed782deb0839a792e110ad752d495a890f07b6a; prior pause106files/8dirs/65% retained honestly. Full critical primary reading and8 fresh primary rasters completed while file writes were paused. Whole raw owner transport/failure history retained, zero primary GETs. Complete source copies, literal objects/type tapes, final independent derivations/report/verdict and ledgers now packaged. INITIAL087144 and OWN708209 unchanged. Default pure offline custody helper/full-read/closure/seal remain. Root137 CLOSED; findings withheld.\n")
    print(json.dumps({"source_copies": len(bindings), "whole_JSON_objects": len(objects), "primary_read_bodies": len(primary_reads), "scope_progress_percent": 80, "root_gate": "CLOSED"}))


if __name__ == "__main__":
    if sys.argv[1:] != ["--package"]:
        raise SystemExit("Inert by default; explicit --package copies and writes scope evidence only")
    package()
