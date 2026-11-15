#!/usr/bin/env python3
"""Read-only custody/record closure. No proof certification or program reruns."""
from pathlib import Path
import hashlib
import json
import sys

A = Path(__file__).resolve().parent
TERMINAL = {"MANIFEST.json", "CLOSURE.json", "SEAL.json"}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(Path(path).read_text())


def check_pin(entry):
    path = Path(entry["path"])
    need(path.is_file() and not path.is_symlink(), "missing/nonregular pin: " + str(path))
    data = path.read_bytes()
    need(len(data) == entry["bytes"], "byte count: " + str(path))
    need(hashlib.sha256(data).hexdigest() == entry["SHA256"], "SHA256: " + str(path))
    return data


def all_file_names(root):
    names = set()
    for path in root.rglob("*"):
        need(not path.is_symlink(), "unexpected symlink: " + str(path))
        if path.is_file():
            names.add(str(path))
    return names


def exact_membership(actual, entries):
    expected = [entry["path"] for entry in entries]
    need(len(expected) == len(set(expected)), "duplicate manifest members")
    need(actual == set(expected), "exact file membership mismatch")


def whole_result(actual, expected):
    need(actual == expected, "whole native result mismatch")


def rejects(function):
    try:
        function()
    except ValueError:
        return True
    raise ValueError("negative control was accepted")


def main():
    manifest = read_json(A / "MANIFEST.json")
    exact_membership(
        all_file_names(A) - {str(A / name) for name in TERMINAL}, manifest["files"]
    )
    for entry in manifest["files"]:
        check_pin(entry)

    baseline = read_json(A / "INPUT_BASELINE.json")
    exact_membership(all_file_names(Path(baseline["source_root"])), baseline["files"])
    for entry in baseline["files"]:
        check_pin(entry)
    need(len(baseline["files"]) == 232, "source baseline size")

    inputs = read_json(A / "INPUT_MANIFEST.json")
    for key in ["frozen_complete_source_baseline", "source_ready", "source_custody_seal",
                "target_PDF", "target_controlling_TeX", "research_instructions",
                "full_203_goal", "root_gate_authority", "initial_seal",
                "initial_reconstruction", "initial_read_record",
                "whole_primary_bodies_and_all_transports_bound_by"]:
        check_pin(inputs[key])
    need(len(check_pin(inputs["target_controlling_TeX"]).splitlines()) == 263,
         "controlling TeX line count")
    initial = read_json(A / "INITIAL_SEAL.json")
    for key in ["INITIAL_RECONSTRUCTION", "INITIAL_READ_RECORD", "INPUT_BASELINE"]:
        check_pin(initial[key])
    need(initial["root_science_gate_open"] is False, "initial historical gate altered")
    need(initial["scientific_findings_sent_to_root"] is False, "initial exposure altered")
    need(initial["SOURCE_READY_SHA256"] == inputs["source_ready"]["SHA256"],
         "initial source association")

    native = read_json(A / "NATIVE_REPRODUCTION.json")
    need(native["programme_runs"] == len(native["records"]) == 2, "native run count")
    for record in native["records"]:
        code = check_pin({"path": record["native_original_path"],
                          "bytes": record["native_programme_bytes"],
                          "SHA256": record["native_programme_SHA256"]})
        need(code == Path(record["isolated_byte_identical_copy"]).read_bytes(),
             "native copied code changed")
        expected = json.loads(check_pin({"path": record["whole_native_expected_path"],
                                        "bytes": record["whole_native_expected_bytes"],
                                        "SHA256": record["whole_native_expected_SHA256"]}))
        whole_result(json.loads(record["stdout_original"]), expected)
        whole_result(record["complete_parsed_result"], expected)
        need(record["whole_parsed_output_equals_whole_native_expected"] is True,
             "native whole-object comparison field")
        need(record["exit_code"] == 0 and record["stderr_original"] == "",
             "native execution status")
        need(record["command"][1:3] == ["-I", "-B"], "native isolation flags")
        need(record["source_body_fully_inspected_before_execution"] is True,
             "native read-before-run record")
        need(record["source_writes"] is False and record["network_requests"] == [],
             "native side effects record")

    primary = read_json(A / "PRIMARY_READ_RECORD.json")
    need(len(primary["primary_bodies"]) == 6, "primary PDF body count")
    for record in primary["primary_bodies"]:
        need(check_pin(record["whole_native_body"]).startswith(b"%PDF-"),
             "actual primary body is not a PDF")
        check_pin(record["derived_extract"])
        chain = json.loads(check_pin(record["whole_transport_chain"]))
        need(chain[-1]["SHA256"] == record["whole_native_body"]["SHA256"],
             "primary final-hop identity")
        need(chain[-1]["HTTP_status"] == 200 and chain[-1]["is_PDF"] is True,
             "primary actual successful final response")
        for raster in record["fresh_critical_rasters_personally_viewed"]:
            check_pin(raster)
    responses = []
    for acquisition in primary["whole_acquisition_chains"]:
        chain = json.loads(check_pin(acquisition["whole_chain"]))
        need(len(chain) == len(acquisition["responses"]), "transport chain length")
        for actual, entry in zip(chain, acquisition["responses"]):
            body = check_pin(entry["body"])
            receipt = json.loads(check_pin(entry["whole_receipt"]))
            need(receipt == actual, "whole receipt and chain differ")
            need(actual["bytes"] == len(body) and
                 actual["SHA256"] == hashlib.sha256(body).hexdigest(),
                 "native response body identity")
            need(isinstance(actual["ordered_response_headers"], list), "header order lost")
            need(actual["is_PDF"] == body.startswith(b"%PDF-"), "false PDF label")
            responses.append(actual)
    need(len(responses) == primary["actual_native_HTTP_responses"] == 15,
         "native primary transport response count")
    need(sum(x["HTTP_status"] >= 400 for x in responses) ==
         primary["failed_HTTP_responses"] == 2, "failed transport history")

    verdict = read_json(A / "VERDICT.json")
    need(verdict["decision"] == "SUPPORTED_FULL_ORIGINAL_CLAIM", "literal verdict changed")
    need(verdict["follow_up"] is None, "follow-up changed")
    need(verdict["historical_priority"]["status"] == "UNRESOLVED", "priority limit lost")
    for entry in verdict["evidence"].values():
        check_pin(entry)

    # In-memory controls reject corrupted evidence without modifying any payload.
    corrupt = dict(inputs["target_PDF"], SHA256="0" * 64)
    controls = [rejects(lambda: check_pin(corrupt)),
                rejects(lambda: exact_membership(
                    all_file_names(Path(baseline["source_root"])), baseline["files"][:-1])),
                rejects(lambda: whole_result(native["records"][0]["complete_parsed_result"],
                    dict(native["records"][0]["complete_parsed_result"], invented_extra=True))),
                rejects(lambda: need(Path(A / "private-primary/rs-accepted.pdf").read_bytes()
                                     .startswith(b"%PDF-"), "failed body cannot be PDF"))]
    result = {"status": "PASS", "record_id": 23423736, "lane": "analytic",
              "source_files_checked": len(baseline["files"]),
              "owned_payload_files_checked": len(manifest["files"]),
              "initial_seal_and_source_binding_checked": True,
              "primary_PDF_bodies_checked": len(primary["primary_bodies"]),
              "native_primary_HTTP_responses_checked": len(responses),
              "failed_HTTP_responses_preserved": 2,
              "whole_native_result_records_checked": len(native["records"]),
              "in_memory_negative_controls_rejected": len(controls),
              "source_or_review_writes": False, "network_requests": [],
              "scientific_programmes_executed": [],
              "scope": "Pure custody and recorded whole-result consistency; not a machine proof or certificate of personal reading/priority."}
    if (A / "CLOSURE.json").exists():
        need(read_json(A / "CLOSURE.json")["read_only_verifier_result"] == result,
             "closure result differs")
    if (A / "SEAL.json").exists():
        seal = read_json(A / "SEAL.json")
        for entry in seal["bindings"].values():
            check_pin(entry)
        need(seal["status"] == "COMPLETE_INDEPENDENT_ANALYTIC_REVIEW_SEALED",
             "seal status")
    return result


if __name__ == "__main__":
    try:
        print(json.dumps(main(), sort_keys=True, indent=2))
    except (ValueError, KeyError, OSError, TypeError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}))
        sys.exit(1)
