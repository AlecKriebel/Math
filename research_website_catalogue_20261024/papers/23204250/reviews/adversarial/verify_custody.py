"""Offline read-only custody; never execute scientific or project code.

Default checks the exact final file AND directory namespace. --preseal checks
fixed input/interfaces before final terminals; it does not claim that closure.
"""
import hashlib
import io
import json
from pathlib import Path
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
INITIAL_SHA = "0bb3e61e8f3451b76dc14383c3c54ee0f7682c429d02e019758dfe95e1a53518"
READY_SHA = "13d913127abab98d78c3758516884b09f7e4849b5e6c07a3e0fd44c502147ec9"
CORE_AUTHORIZED_SHA = "405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0"
TERMINALS = {"MANIFEST.json", "FINAL_SEAL.json"}
checks = 0


def need(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


def raw(path):
    p = Path(path)
    need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), "ordinary file: " + str(p))
    return p.read_bytes()


def own(name):
    p = Path(name)
    need(not p.is_absolute() and ".." not in p.parts, "owned relative path")
    return ROOT / p


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pinned(path, binding):
    data = raw(path)
    need(len(data) == binding["bytes"], "whole size: " + str(path))
    need(digest(data) == binding["SHA256"], "whole SHA256: " + str(path))
    return data


def load(path):
    return json.loads(raw(path))


def literal(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def same(a, b, label):
    need(literal(a) == literal(b), "whole ordered typed literal: " + label)


def namespace(folder):
    files, directories = [], []
    for path in sorted(folder.rglob("*")):
        need(not path.is_symlink(), "no symlink")
        mode = path.lstat().st_mode
        name = path.relative_to(folder).as_posix()
        if stat.S_ISREG(mode):
            files.append(name)
        elif stat.S_ISDIR(mode):
            directories.append(name)
        else:
            raise RuntimeError("Nonordinary namespace entry: " + str(path))
    return files, directories


def differences(actual, expected, path=""):
    result = []
    if type(actual) is not type(expected):
        result.append({"path": path, "kind": "TYPE", "whole_actual": actual, "whole_original_expected": expected})
    elif isinstance(actual, dict):
        if list(actual) != list(expected):
            result.append({"path": path, "kind": "KEY_LIST_OR_ORDER", "whole_actual": list(actual), "whole_original_expected": list(expected)})
        for key in actual.keys() & expected.keys():
            result.extend(differences(actual[key], expected[key], path + "/" + key))
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            result.append({"path": path, "kind": "LIST_LENGTH", "whole_actual": len(actual), "whole_original_expected": len(expected)})
        for i, (a, b) in enumerate(zip(actual, expected)):
            result.extend(differences(a, b, path + "/" + str(i)))
    elif actual != expected:
        result.append({"path": path, "kind": "VALUE", "whole_actual": actual, "whole_original_expected": expected})
    return sorted(result, key=lambda r: r["path"])


def main():
    preseal = sys.argv[1:] == ["--preseal"]
    need(preseal or sys.argv[1:] == [], "only optional --preseal is supported")
    initial_bytes = raw(ROOT / "INITIAL_SEAL.json")
    need(digest(initial_bytes) == INITIAL_SHA, "immutable initial and actual hand-worked results seal")
    initial = json.loads(initial_bytes)
    need(len(initial["payloads"]) == 128, "complete128 initial payloads")
    for name, pin in initial["payloads"].items():
        pinned(own(name), pin)

    protected = load(ROOT / "PROTECTED_INPUTS.json")
    need(len(protected["files"]) == 122 and len(protected["core_files"]) == 18, "source104 plus qualified core18")
    need(protected["core_qualification"] == "17original plus sole separately root-authorized405b checkpoint helper", "qualified core, not18all-original")
    need(any(r["SHA256"] == CORE_AUTHORIZED_SHA and r["path"] in protected["core_files"] for r in protected["files"]), "sole authorized checkpoint helper actual SHA")
    for row in protected["files"]:
        data = pinned(row["path"], row)
        need(raw(own(row["copy"])) == data, "whole protected blob identity")
    source = protected["source_namespace"]
    files, dirs = namespace(Path(source["path"]))
    same(files, source["files"], "complete unchanged source file namespace")
    same(dirs, source["directories"], "complete unchanged source directory namespace")
    need(len(files) == 104 and len(dirs) == 13, "actual source104/13")

    protocol = load(ROOT / "SOURCE_PROTOCOL_BINDINGS.json")
    def protocol_walk(value):
        if isinstance(value, dict):
            if "copy" in value and "whole_literal_object" in value:
                same(json.loads(pinned(own(value["copy"]), value)), value["whole_literal_object"], "entire original protocol object")
            for child in value.values():
                protocol_walk(child)
        elif isinstance(value, list):
            for child in value:
                protocol_walk(child)
    protocol_walk(protocol)
    ready = protocol["whole_SOURCE_READY"]["whole_literal_object"]
    need(protocol["whole_SOURCE_READY"]["SHA256"] == READY_SHA, "actual immutable READY pin")
    need(ready["version_field_present"] is False and ready["version"] is None, "native version ABSENT; wrapper null retained")
    need(ready["printed_date"] is None and ready["printed_version"] is None, "historical unread printed fields")
    need(type(ready["source_programmes_executed"]) is list and ready["source_programmes_executed"] == [], "historical empty-list execution flag")
    same([r["original_api_file_object"]["key"] for r in ready["all_native_assets_in_original_order"]], ["paper.pdf", "tsp-verification.zip", "tsp-source.zip"], "actual native asset order")

    archive_binding = load(ROOT / "NATIVE_ARCHIVE_LITERAL_BINDINGS.json")
    payloads = 0
    for archive in archive_binding["archives"]:
        data = pinned(archive["whole_original_archive"]["path"], archive["whole_original_archive"])
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            need(z.comment.hex() == archive["archive_comment_hex"], "whole ZIP comment")
            need(len(z.infolist()) == len(archive["members_in_original_order"]), "whole ZIP member count/order")
            for member, expected in zip(z.infolist(), archive["members_in_original_order"]):
                data = z.read(member)  # CRC checked by zipfile, no extraction/write.
                actual = {}
                for key in expected:
                    if key == "date_time": actual[key] = list(member.date_time)
                    elif key == "comment_hex": actual[key] = member.comment.hex()
                    elif key == "extra_hex": actual[key] = member.extra.hex()
                    elif key == "is_dir": actual[key] = member.is_dir()
                    elif key == "whole_payload_SHA256": actual[key] = digest(data)
                    elif key == "extracted": actual[key] = expected[key]
                    else: actual[key] = getattr(member, key)
                same(actual, expected, "whole original member metadata and payload")
                if not member.is_dir():
                    payloads += 1
                    need(raw(expected["extracted"]) == data, "whole extracted native payload")
    need(payloads == archive_binding["regular_payload_occurrences"] == 35, "all35 regular payload occurrences")

    records = []
    for name in ["RAW_PRIMARY_HANDOFF_01.json", "RAW_PRIMARY_HANDOFF_02.json"]:
        handoff = load(ROOT / name)
        need(handoff["raw_only_no_interpretations_notes_findings_or_control_results"] is True, "raw-only peer boundary")
        for row in handoff["records"]:
            records.append(row)
            output = json.loads(pinned(row["whole_transport_stdout"]["path"], row["whole_transport_stdout"]))
            pinned(row["whole_transport_stderr"]["path"], row["whole_transport_stderr"])
            same(output["whole_terminal_body"], row["whole_actual_body"], "whole raw terminal binding")
            for hop in output["hops_in_actual_order"]:
                transport = json.loads(pinned(hop["whole_transport"]["path"], hop["whole_transport"]))
                same(transport, hop["whole_literal_transport"], "entire ordered transport/header/null object")
                request = transport["actual_prepared_and_sent_request_buffer"]
                pinned(request["path"], request)
                if transport["body"] is not None:
                    pinned(transport["body"]["path"], transport["body"])
    need(len(records) == 32 and len({r["label"] for r in records}) == 32, "complete32 raw acquisition records")
    native_primary = load(ROOT / "PRIMARY_NATIVE_PIN_COMPARISON.json")
    inventory_path = Path(source["path"]) / "published-source/asset-002/receipts/upstream_source_hashes.json"
    inventory = load(inventory_path)
    same(native_primary["whole_original_native_inventory"], inventory, "literal original upstream hash inventory")
    rows = native_primary["all12_direct_actual_primary_comparisons"]
    need(len(rows) == len(inventory["sha256"]) == len({r["native_key"] for r in rows}) == 12, "all12 unique native primary keys")
    need(native_primary["remaining_native_keys"] == [], "no missing native primary bodies")
    for row in rows:
        data = pinned(row["whole_actual_body"]["path"], row["whole_actual_body"])
        need(digest(data) == row["expected_native_SHA256"] == inventory["sha256"][row["native_key"]], "direct actual full primary/native hash")

    native = load(ROOT / "NATIVE_EXECUTION_COMPARISON.json")
    normal = pinned(own(native["normal"]["whole_stdout"]["path"]), native["normal"]["whole_stdout"])
    original = pinned(own(native["original_expected"]["path"]), native["original_expected"])
    actual, expected = json.loads(normal), json.loads(original)
    same(actual, native["whole_actual_literal_object"], "entire actual native output")
    same(expected, native["whole_original_expected_literal_object"], "entire historical expected output")
    delta = differences(actual, expected)
    same(delta, native["all_whole_interface_differences_without_field_deletion_or_coercion"], "complete native interface comparison, no removed field")
    need({r["path"] for r in delta} == {"/checked_utc", "/python"}, "only exact runtime-context differences")
    need((normal == original) is native["whole_stdout_byte_identity"] is False, "whole native buffers honestly not byte-identical")
    need(pinned(own(native["normal"]["whole_stderr"]["path"]), native["normal"]["whole_stderr"]) == b"", "whole actual stderr empty")
    need(native["normal"]["actual_process_exit_code"] == 0 and native["normal"]["optimization_flag"] == 0 and native["normal"]["assertions_enabled"] is True, "actual normal exit/optimization/assertions")
    need(native["optimized_executed"] is False, "no native optimized replay")
    checker = raw(ROOT / "native-replay/tsp_reduction_check.py")
    need(checker == raw(Path(source["path"]) / "published-source/asset-002/checks/tsp_reduction_check.py"), "unchanged whole selected checker; no execution")
    need(digest(checker) == actual["script_sha256"], "actual native self-hash")

    verdict = load(ROOT / "CUSTOM_VERDICT.json")
    same(verdict["native_execution"]["whole_original_expected_literal_object"], expected, "verdict complete original native object")
    same(verdict["native_execution"]["whole_actual_literal_object"], actual, "verdict complete actual native object")
    same(verdict["whole_literal_historical_source_custom_verdict"], protocol["CUSTOM_VERDICT.json"]["whole_literal_object"], "whole historical custom dictionary")
    same(verdict["native_identity_and_history"]["whole_original_native_assets_in_actual_order"], ready["all_native_assets_in_original_order"], "whole native original asset objects")
    need(verdict["root_science_gate"] == "CLOSED" and verdict["followup"] is None and verdict["canonical_AA_assignment_authority"] is False and verdict["publication_authority"] is None and verdict["root_adoption"] is None, "separate root gate and false/null authorities")

    if not preseal:
        manifest_bytes = raw(ROOT / "MANIFEST.json")
        manifest = json.loads(manifest_bytes)
        seal = load(ROOT / "FINAL_SEAL.json")
        need(seal["status"] == "FINAL", "final seal status")
        need(len(manifest_bytes) == seal["manifest"]["bytes"] and digest(manifest_bytes) == seal["manifest"]["SHA256"], "entire final manifest pin")
        same(seal["exact_root_terminals"], sorted(TERMINALS), "exact root terminal exclusions only")
        files, dirs = namespace(ROOT)
        need(set(files) == set(manifest["payloads"]) | TERMINALS, "strict complete owned ordinary-file namespace")
        same(dirs, manifest["directories"], "strict complete owned directory namespace")
        need(len(manifest["payloads"]) == seal["payload_files"] and len(files) == seal["actual_files"] and len(dirs) == seal["directories"], "whole final namespace counts")
        for name, pin in manifest["payloads"].items():
            need(name not in TERMINALS, "only exact root terminal exclusion, nested names remain payloads")
            pinned(own(name), pin)
        pinned(ROOT / "CUSTOM_VERDICT.json", seal["custom_verdict"])
        need(seal["initial_seal_SHA256"] == INITIAL_SHA, "immutable initial pin in final seal")
    print(json.dumps({"custody_status": "PASS", "mode": "preseal fixed bindings only" if preseal else "final complete namespace", "checks": checks, "source_files": 104, "protected_paths": 122, "native_ZIP_regular_payload_occurrences": payloads, "raw_primary_records": len(records), "native_primary_pins": 12, "scientific_programmes_executed_by_this_helper": [], "network": False, "writes": False, "root_science_gate": "CLOSED"}, indent=2))


if __name__ == "__main__":
    main()
