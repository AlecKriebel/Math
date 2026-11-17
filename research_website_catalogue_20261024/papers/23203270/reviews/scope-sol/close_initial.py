"""Finite INITIAL closure of this lane only; no scientific program execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parents[3] / "papers/23203270/sources"
TERMINALS = ["INITIAL_MANIFEST.json", "INITIAL_SEAL.json"]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def object_record(path, base):
    st = path.lstat()
    result = {"path": str(path.relative_to(base)) if path != base else ".",
              "mode_octal": oct(stat.S_IMODE(st.st_mode))}
    if stat.S_ISDIR(st.st_mode):
        result.update(kind="directory", empty=not any(path.iterdir()))
    elif stat.S_ISREG(st.st_mode):
        b = path.read_bytes()
        result.update(kind="file", bytes=len(b), sha256=sha(b))
    else:
        raise ValueError(f"Unexpected nonregular object: {path}")
    return result

assert not any((LANE / name).exists() for name in TERMINALS), "Initial closure already exists"
authentication = json.loads((LANE / "SOURCE_AUTHENTICATION.json").read_text())
expected_sources = authentication["all_actual_entries"]
source_now = [object_record(p, SOURCE) for p in [SOURCE, *sorted(SOURCE.rglob("*"))]]
for actual, expected in zip(source_now, expected_sources, strict=True):
    assert all(actual[k] == expected[k] for k in actual), (actual, expected)

now = datetime.now(timezone.utc).isoformat()
images = [object_record(LANE / f"native-render/page-{i}.png", LANE) for i in range(1, 7)]
read_receipt = {
    "schema": "initial-original-only-personal-reading-receipt-v1",
    "recorded_utc": now,
    "complete_controlling_tex_read": True,
    "tex_lines": 362,
    "tex_bytes": 16724,
    "tex_sha256": "0950f3488e6b59b3ca68e066468fc49b99838be42f1ff8ff5fd6afef9fd04d6b",
    "complete_native_outer_pdf_text_read": True,
    "outer_pdf_pages": 6,
    "outer_pdf_sha256": "c579ec3442f4bcdf68ed737ad8bc65328682158845ed2e14e6636b2b119f52c6",
    "fresh_local_render": "pdftoppm -r 110 -png; native outer PDF input only",
    "personally_viewed_with_view_image": [1, 2, 3, 4, 5, 6],
    "fresh_render_images_before_readonly_mode_freeze": images,
    "full_native_api_metadata_description_read": True,
    "full_captured_native_page_text_read": True,
    "native_api_version_field_present": False,
    "native_html_displayed_version": "v1",
    "source_controls_and_all_source_bytes_modes_topology_authenticated": True,
    "packaged_audit_result_support_conclusion_contents_read": False,
    "imported_primary_mathematical_bodies_read": False,
    "native_scientific_program_bodies_semantically_inspected_or_executed": False,
    "pdf_tools_used_only_to_extract_inspect_render": True,
    "additional_child_agents": 0,
    "independent_reconstruction": "INITIAL_INDEPENDENT_RECONSTRUCTION.md",
    "independent_reconstruction_precedes_support_imports": True,
    "root_sent_scientific_mechanism_or_verdict_before_gate": False,
}
(LANE / "INITIAL_READ_RECEIPT.json").write_text(json.dumps(read_receipt, indent=2) + "\n")

log = LANE / "RESEARCH_LOG.md"
with log.open("a") as stream:
    stream.write(f"\nTerminal closure prepared at {now}. All source byte/mode/topology records "
                 "were rechecked unchanged immediately before closure. Payload files made "
                 "read-only, and image directory made read-only. Exact terminal controls "
                 "are INITIAL_MANIFEST.json and INITIAL_SEAL.json. INITIAL 100%; full "
                 "scientific review best guess 35%. Quiescent after closure pending root "
                 "checkpoint and explicit RESUME.\n")

for p in sorted(LANE.rglob("*")):
    if p.is_file():
        os.chmod(p, 0o444)
for p in sorted(LANE.rglob("*"), reverse=True):
    if p.is_dir():
        os.chmod(p, 0o555)

payload = [object_record(p, LANE) for p in [LANE, *sorted(LANE.rglob("*"))]]
assert all(e["path"] not in TERMINALS for e in payload)
manifest = {
    "schema": "finite-initial-manifest-v1",
    "utc": now,
    "lane_root": str(LANE),
    "scope": "Every lane payload object including root and every hidden, empty, or ignored object; no implicit exclusions",
    "exact_terminal_exclusions": [{"path": name, "kind": "file", "reason": "terminal control; INITIAL_SEAL pins INITIAL_MANIFEST, root message externally pins INITIAL_SEAL"} for name in TERMINALS],
    "entries": payload,
    "payload_files": sum(e["kind"] == "file" for e in payload),
    "payload_child_directories": sum(e["kind"] == "directory" and e["path"] != "." for e in payload),
    "payload_file_bytes": sum(e.get("bytes", 0) for e in payload),
    "source_namespace_unchanged_at_closure": True,
}
manifest_path = LANE / TERMINALS[0]
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
os.chmod(manifest_path, 0o444)
seal = {
    "schema": "finite-initial-seal-v1",
    "utc": now,
    "record_id": 23203270,
    "inventory_row": 188,
    "lane": "scope-sol",
    "lane_root": str(LANE),
    "phase": "INITIAL_ONLY",
    "status": "FROZEN_AWAIT_ROOT_CHECKPOINT_AND_EXPLICIT_RESUME",
    "manifest": object_record(manifest_path, LANE),
    "exact_terminal_exclusions": TERMINALS,
    "own_terminal_self_pin": "External root message supplies SHA256, byte count, and mode of this exact file; no circular self-hash claimed",
    "manifest_payload_files": manifest["payload_files"],
    "whole_files_including_two_terminal_controls": manifest["payload_files"] + 2,
    "whole_child_directories": manifest["payload_child_directories"],
    "original_source_files": 97,
    "original_source_child_directories": 12,
    "archive_members": 87,
    "embedded_pdfs": 0,
    "controlling_tex_complete": True,
    "native_pdf_complete_text_and_all_six_fresh_pages_personally_viewed": True,
    "native_metadata_description_complete": True,
    "native_api_version_field_present": False,
    "independent_initial_exact_claims_assumptions_reconstruction_boundaries_interfaces_and_checks_frozen": True,
    "packaged_support_or_imported_primary_bodies_examined": False,
    "native_scientific_code_executions": 0,
    "scientific_mechanisms_or_verdicts_sent_to_root_before_gate": False,
    "source_quiescence_rechecked": True,
    "initial_phase_completion_percent": 100,
    "full_scientific_review_best_guess_completion_percent": 35,
    "full_target_final_verdict": None,
    "authorization_for_resumption": "Root checkpoint and explicit RESUME required",
    "additional_work_authorized_now": False,
}
seal_path = LANE / TERMINALS[1]
seal_path.write_text(json.dumps(seal, indent=2) + "\n")
os.chmod(seal_path, 0o444)

all_now = [object_record(p, LANE) for p in [LANE, *sorted(LANE.rglob("*"))]]
payload_now = [e for e in all_now if e["path"] not in TERMINALS]
assert payload_now == payload
assert sum(e["kind"] == "file" for e in all_now) == seal["whole_files_including_two_terminal_controls"]
assert len(all_now) == len(payload) + 2
print(json.dumps({
    "manifest": object_record(manifest_path, LANE),
    "seal": object_record(seal_path, LANE),
    "payload_files": manifest["payload_files"],
    "whole_files": seal["whole_files_including_two_terminal_controls"],
    "whole_child_directories": seal["whole_child_directories"],
    "phase": seal["phase"], "status": seal["status"],
}, indent=2))
