#!/usr/bin/env python3
"""Read-only custody and review-contract closure; no source/program replay.

Default validates the terminal seal. --preseal omits only that terminal check.
--inputs-only checks inputs/contracts before the final owned manifest exists.
No branch writes files, contacts services, extracts archives, or runs children.
"""
from pathlib import Path, PurePosixPath
from hashlib import sha256, md5
from datetime import datetime, timezone
import json
import stat
import sys
import zipfile
import zlib

P = Path(__file__).resolve().parent
B = P.parents[1]
READY_HASH = "3833194084fd0343a18c5640400418893203c6e575272997c114bc326d34e2af"
INITIAL_HASH = "4fc8bb3e081a39e0b6b0a4bb4ee95cfe23d853b2b7e3e3ada083f4ad0bd3f5e0"
TERMINAL = {"OWNED_MANIFEST.json", "CLOSURE.json", "SEAL.json"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(body):
    return sha256(body).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def blob(body, size, expected, label):
    require(len(body) == size, label+": byte count")
    require(digest(body) == expected, label+": SHA256")


def safe_names(names):
    seen = set()
    for name in names:
        q = PurePosixPath(name)
        require(not q.is_absolute() and ".." not in q.parts and
                "\\" not in name and ":" not in name and bool(q.parts),
                "unsafe archive name")
        require(name.casefold() not in seen, "duplicate/case-colliding archive name")
        seen.add(name.casefold())


def execution_contract(rec):
    require(rec["exit_code"] == 0, "nonzero execution status")
    require(rec["command"][1:3] == ["-E", "-B"], "missing isolated Python flags")
    require(rec["timeout_seconds"] == 30, "unbounded execution receipt")


def rejected(label, function):
    try:
        function()
    except ValueError:
        return label
    raise ValueError("negative control escaped: "+label)


def main():
    args = sys.argv[1:]
    require(args in ([], ["--preseal"], ["--inputs-only"]), "unsupported arguments")
    skip_owned = args == ["--inputs-only"]
    skip_seal = bool(args)

    ready_path = B/"sources/SOURCE_READY.json"
    require(digest(ready_path.read_bytes()) == READY_HASH, "frozen SOURCE_READY")
    ready = read_json(ready_path)
    require(ready["record_id"] == 23331080 and ready["version"] == "1.0", "record/version")
    require(ready["publication_date"] == "2026-10-12" and
            ready["created"].startswith("2026-10-13"), "declared/created dates")
    require(ready["target_manuscript_scientifically_read"] is False and
            ready["source_programs_executed_or_scientifically_read"] is False,
            "historical acquisition flags changed")

    inputs = read_json(P/"INPUT_MANIFEST.json")
    frozen = inputs["all_original_source_files"]
    expected_paths = set()
    for rec in frozen:
        relative = rec["path"]
        target = B/relative
        require(target.is_file() and not target.is_symlink(), "missing/nonregular input")
        blob(target.read_bytes(), rec["bytes"], rec["SHA256"], relative)
        expected_paths.add(relative)
    actual_paths = {str(q.relative_to(B)) for q in (B/"sources").rglob("*") if q.is_file()}
    require(actual_paths == expected_paths and len(frozen) == 51, "source tree membership")

    api = read_json(B/"sources/record.raw.json")
    assets = ready["all_assets_in_original_order"]
    require([a["original_api_file_object"]["key"] for a in assets] ==
            ["positivity_loss.pdf", "verification_package.zip"], "native asset order")
    require(api["files"] == [a["original_api_file_object"] for a in assets],
            "whole native API file objects/order")
    for item in assets:
        body = Path(item["path"]).read_bytes()
        blob(body, item["bytes"], item["sha256"], item["path"])
        require(md5(body).hexdigest() == item["md5"] ==
                item["original_api_file_object"]["checksum"].removeprefix("md5:"),
                "native asset MD5")

    count, expanded = 0, 0
    with zipfile.ZipFile(B/"sources/verification_package.zip") as archive:
        members = archive.infolist()
        safe_names([z.filename for z in members])
        for member in members:
            require(not member.is_dir() and
                    stat.S_IFMT(member.external_attr >> 16) in (0, stat.S_IFREG),
                    "nonregular archive payload")
            body = archive.read(member)
            require(len(body) == member.file_size and
                    (zlib.crc32(body) & 0xffffffff) == member.CRC,
                    "native whole ZIP size/CRC")
            target = B/"sources/published-source"/member.filename
            require(target.is_file() and not target.is_symlink(), "missing extracted payload")
            require(target.read_bytes() == body, "whole extracted payload differs")
            count += 1
            expanded += len(body)
    require(count == ready["safe_regular_occurrences"] == 40 and
            expanded == ready["expanded_bytes_all_depths"] == 198877,
            "complete archive inventory")

    initial_path = P/"INITIAL_SEAL.json"
    require(digest(initial_path.read_bytes()) == INITIAL_HASH, "early initial seal changed")
    initial = read_json(initial_path)
    require(digest((P/"INITIAL_MANIFEST.json").read_bytes()) ==
            initial["INITIAL_MANIFEST_SHA256"], "initial manifest")
    for rec in read_json(P/"INITIAL_MANIFEST.json")["files"]:
        target = Path(rec["path"])
        require(target.is_relative_to(P), "initial binding outside own lane")
        blob(target.read_bytes(), rec["bytes"], rec["SHA256"], target.name)
    require(initial["before_foreign_code_results_triage_archived_current_peer_findings"]
            is True, "early independence declaration")

    raw_pdfs = 0
    for name in ("PRIMARY_FETCH_01.json", "PRIMARY_FETCH_02.json"):
        for rec in read_json(P/name):
            target = Path(rec["path"])
            require(target.is_relative_to(P), "primary body outside own lane")
            body = target.read_bytes()
            blob(body, rec["bytes"], rec["SHA256"], target.name)
            require(isinstance(rec["headers_in_received_order"], list), "ordered raw headers")
            if rec["PDF_magic"]:
                require(body.startswith(b"%PDF-") and rec["HTTP_status"] == 200,
                        "primary PDF transport/body")
                raw_pdfs += 1
    require(raw_pdfs == 4, "whole actual primary PDF count")
    renders = read_json(P/"PRIMARY_RENDER_RECEIPTS.json")
    for rec in renders:
        target = Path(rec["image_path"])
        require(target.is_relative_to(P) and rec["exit_code"] == 0, "primary render")
        require(digest(target.read_bytes()) == rec["image_SHA256"], "primary pixel binding")
    require(len(renders) == 7, "selected primary page count")

    calls = read_json(P/"EXACT_RUN_RECEIPTS.json")
    require([r["name"] for r in calls] == ["own-exact", "native-flow"], "bounded calls")
    for rec in calls:
        execution_contract(rec)
        script = Path(rec["command"][-1])
        require(script.is_relative_to(P), "execution outside own lane")
        require(digest(script.read_bytes()) == rec["script_SHA256"], "actual script binding")
        for stream in ("stdout", "stderr"):
            target = Path(rec[stream+"_path"])
            require(target.is_relative_to(P), "stream outside lane")
            require(digest(target.read_bytes()) == rec[stream+"_SHA256"], "stream binding")
        require(Path(rec["stderr_path"]).read_bytes() == b"", "unexpected verifier stderr")
    native = calls[1]
    require(Path(native["native_source_path"]).read_bytes() ==
            Path(native["command"][-1]).read_bytes(), "native isolated copy differs")
    require(digest(Path(native["generated_result_path"]).read_bytes()) ==
            native["generated_result_SHA256"], "native generated result")
    require(Path(native["generated_result_path"]).read_bytes() ==
            Path(native["stdout_path"]).read_bytes(), "native result/stdout discrepancy")
    own_result = read_json(P/"own-exact.stdout.json")
    native_result = read_json(P/"native-flow.stdout.json")
    require(own_result["verdict"] == "PASS" and own_result["identities_passed"] == 42
            and own_result["negative_controls_rejected"] == 6 and
            own_result["source_imports"] == [] and own_result["writes"] == [],
            "independent exact result contract")
    require(native_result["number_of_checks"] == 17 and
            native_result["negative_horizontal_coefficient_at_t_log2_over2"] == "-1/96",
            "native bounded exact result contract")

    verdict = read_json(P/"VERDICT.json")
    require(verdict["literal_verdict"] == "SUPPORTED_FULL_ORIGINAL_THEOREM" and
            verdict["full_original_quantified_claim_supported"] is True and
            verdict["narrowed_or_repaired_theorem_substituted"] is False and
            verdict["remaining_in_scope_gap"] is None, "full original scope contract")
    require(verdict["scientific_findings_sent_to_root"] is False and
            verdict["publication_authorized"] is False, "historical delivery/authority contract")
    gate = read_json(P/"ROOT_GATE_OPEN.json")
    require(gate["root117_gate"] == "OPEN" and
            gate["root_scientific_opinion_body_read"] is False and
            gate["all117_science_was_withheld_before_this_gate"] is True and
            gate["root_initial_seal_SHA256_reported_and_independently_hashed"] ==
            "1cce2ec5a33098612782123038c86767590626614c71f2d21abf0132f4c2edbe",
            "explicit root opening authority")

    controls = [
        rejected("corrupted-byte SHA", lambda: blob(b"X", 1, digest(b"Y"), "test")),
        rejected("wrong byte count", lambda: blob(b"X", 2, digest(b"X"), "test")),
        rejected("archive parent traversal", lambda: safe_names(["../escape"])),
        rejected("archive case collision", lambda: safe_names(["A", "a"])),
        rejected("false successful execution", lambda: execution_contract(
            {"exit_code": 1, "command": ["python", "-E", "-B"], "timeout_seconds": 30})),
        rejected("missing execution isolation", lambda: execution_contract(
            {"exit_code": 0, "command": ["python", "-O"], "timeout_seconds": 30}))]

    owned_count = None
    if not skip_owned:
        manifest = read_json(P/"OWNED_MANIFEST.json")
        owned_paths = set()
        for rec in manifest["files"]:
            target = P/rec["path"]
            require(target.is_relative_to(P) and target.is_file() and not target.is_symlink(),
                    "owned path invalid")
            blob(target.read_bytes(), rec["bytes"], rec["SHA256"], rec["path"])
            owned_paths.add(rec["path"])
        actual = {str(q.relative_to(P)) for q in P.rglob("*") if q.is_file()
                  and str(q.relative_to(P)) not in TERMINAL}
        require(actual == owned_paths, "unmanifested/missing owned files")
        owned_count = len(owned_paths)

    if not skip_seal:
        seal = read_json(P/"SEAL.json")
        for name, field in [("OWNED_MANIFEST.json", "OWNED_MANIFEST_SHA256"),
                            ("CLOSURE.json", "CLOSURE_SHA256"),
                            ("REPORT.md", "REPORT_SHA256"),
                            ("VERDICT.json", "VERDICT_SHA256"),
                            ("DERIVATION.md", "DERIVATION_SHA256")]:
            require(digest((P/name).read_bytes()) == seal[field], "terminal binding: "+name)
        require(seal["INITIAL_SEAL_SHA256"] == INITIAL_HASH and
                seal["SOURCE_READY_SHA256"] == READY_HASH and
                seal["completion_estimate_percent_bounded_review"] == 100,
                "terminal provenance/completion")
        closure = read_json(P/"CLOSURE.json")
        require(closure["result"]["verdict"] == "PASS" and closure["exit_code"] == 0,
                "actual captured preseal closure")
        require(closure["command"][-2:] == [str(P/"verify_closure.py"), "--preseal"]
                and closure["verifier_SHA256"] == digest(Path(__file__).read_bytes())
                and closure["stdout_SHA256"] == digest(closure["stdout"].encode())
                and closure["stderr"] == "" and
                json.loads(closure["stdout"]) == closure["result"],
                "actual read-only closure command/stream binding")

    print(json.dumps({"UTC": datetime.now(timezone.utc).isoformat(),
                      "verdict": "PASS", "mode": args[0] if args else "terminal-read-only",
                      "original_source_files": len(frozen), "whole_ZIP_payloads": count,
                      "whole_ZIP_expanded_bytes": expanded, "initial_payloads": 8,
                      "whole_primary_PDFs": raw_pdfs, "selected_primary_rasters": len(renders),
                      "owned_manifest_payloads": owned_count,
                      "custody_negative_controls_rejected": controls,
                      "programs_replayed": [], "network_requests": [], "writes": []}, indent=2))


if __name__ == "__main__":
    main()
