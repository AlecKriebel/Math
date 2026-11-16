#!/usr/bin/env python3
"""Offline read-only custody, not mathematical verification or native replay.

Default requires the exact sealed namespace. --preseal is an explicitly partial
binding check before either outer terminal exists. Neither mode writes anything.
Only Python standard library is imported; project/scientific code is never loaded.
"""
import hashlib
import json
from pathlib import Path
import stat
import sys
import zipfile
import zlib

HERE = Path(__file__).resolve().parent
CHECKS = 0
INITIAL = "72407df4df97b52cfdd42d8bb85b62945ba7c3d1982b1ca2ec851f627a401f17"
RESULTS = "c135e8c0fbf185815cbc0cd169921e52721b7fc6cc84f234fe78e81597f74df9"
CORE = "0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104"
GO = "f2df5de1ee52b02569585806e2c4725e2708c129ce6bc7be640268f05776874c"
RAW = "3ec453a4ed2cdfac4d71d7e516bac73e4b24a9037cab69ec614910a18c401b10"
TERMINALS = {"MANIFEST.json", "FINAL_SEAL.json"}


def need(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def readj(path):
    return json.loads(Path(path).read_bytes())


def local(name):
    p = HERE / name
    need(p.is_relative_to(HERE) and ".." not in p.parts, "local path escape")
    return p


def checked(row, base=None):
    p = (base / row["path"]) if base is not None else Path(row["path"])
    need(stat.S_ISREG(p.lstat().st_mode), "not ordinary file: " + str(p))
    b = p.read_bytes()
    need(type(row["bytes"]) is int and len(b) == row["bytes"], "length: " + str(p))
    need(sha(b) == row["SHA256"], "SHA256: " + str(p))
    return b


def literal(value):
    """Preserve types, absent keys, dictionary/list order, nulls and all values."""
    if isinstance(value, dict):
        return ("dict", tuple((k, literal(v)) for k, v in value.items()))
    if isinstance(value, list):
        return ("list", tuple(literal(v) for v in value))
    return (type(value).__name__, value)


def whole_equal(a, b, message):
    need(literal(a) == literal(b), message)


def inventory(root):
    files, dirs = set(), set()
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix()
        mode = p.lstat().st_mode
        need(stat.S_ISDIR(mode) or stat.S_ISREG(mode), "symlink/special namespace entry: " + rel)
        (dirs if stat.S_ISDIR(mode) else files).add(rel)
    return files, dirs


def namespace(actual_files, actual_dirs, files, dirs):
    need(actual_files == set(files), "exact ordinary file namespace")
    need(actual_dirs == set(dirs), "exact directory namespace")


def rejected(fn, message):
    try:
        fn()
    except ValueError:
        need(True, message)
    else:
        need(False, "negative control accepted: " + message)


def negative_controls():
    rejected(lambda: whole_equal({"x": 1}, {"x": True}, "integer/bool"), "typed value substitution")
    rejected(lambda: whole_equal({"a": None, "b": []}, {"b": [], "a": None}, "key order"), "ordered dictionary")
    rejected(lambda: whole_equal({"a": None}, {}, "null/absent"), "null versus absent")
    rejected(lambda: namespace({"x", "nested/MANIFEST.json"}, {"nested"}, {"x"}, set()), "nested terminal-name file")
    rejected(lambda: namespace({"x"}, {"empty"}, {"x"}, set()), "extra empty directory")
    rejected(lambda: need(b"original\n" == b"originaL\n", "whole buffer"), "single byte stdout change")


def main():
    need(sys.argv[1:] in ([], ["--preseal"]), "arguments")
    preseal = bool(sys.argv[1:])
    initial_bytes = local("INITIAL_SEAL.json").read_bytes()
    need(sha(initial_bytes) == INITIAL, "initial immutable seal")
    initial = json.loads(initial_bytes)
    for name, row in initial["payloads"].items():
        checked(dict(row, path=name), HERE)
    need(len(initial["payloads"]) == 124, "initial complete payload count")
    result_bytes = local("OWN_PROOF_CONTROL_SEAL.json").read_bytes()
    need(sha(result_bytes) == RESULTS, "actual own evidence immutable seal")
    result = json.loads(result_bytes)
    evidence_manifest = json.loads(checked(result["manifest"], HERE))
    for name, row in evidence_manifest["files"].items():
        checked(dict(row, path=name), HERE)
    need(len(evidence_manifest["files"]) == 2, "separate frozen proof/exposure")

    protected = readj(local("PROTECTED_INPUTS.json"))
    need(len(protected["files"]) == 115, "source plus qualified core paths")
    for row in protected["files"]:
        original = checked(row)
        copy = checked(dict(row, path=row["copy"]), HERE)
        need(original == copy, "opaque original-copy byte identity")
    source = protected["source_namespace"]
    sf, sd = inventory(Path(source["path"]))
    namespace(sf, sd, source["files"], source["directories"])
    need(len(sf) == 97 and len(sd) == 9, "whole source cardinalities")
    core = readj(local("QUALIFIED_CORE_AUTHORITY_BINDING.json"))
    core_bytes = checked(core["actual_root_contract_by_reference"])
    need(sha(core_bytes) == CORE, "exact neutral qualified core authority")
    core_literal = json.loads(core_bytes)
    whole_equal(core_literal, core["whole_literal_contract"], "whole qualified core contract")
    need(len(core_literal["files"]) == 18, "17 originals plus separately authorized checkpoint")
    for row in core_literal["files"]:
        checked(row)
    need(core_literal["original17_plus_sole_authorized405b_checkpoint"] is True, "qualified core meaning")
    need(core_literal["all18_original_unchanged_claim"] is False, "no eighteen-original assertion")

    protocol = readj(local("SOURCE_PROTOCOL_BINDINGS.json"))
    wrappers = [protocol["whole_SOURCE_READY"]] + protocol["whole_native_API_objects_in_original_role_order"]
    wrappers += [v for k, v in protocol.items() if k.endswith(".json")]
    need([x["role"] for x in protocol["whole_native_API_objects_in_original_role_order"]] == ["record", "latest", "versions-page001", "files"], "native API original role order")
    for row in wrappers:
        original = checked(row["original"])
        copy = checked({"path": row["copy"], "bytes": row["bytes"], "SHA256": row["SHA256"]}, HERE)
        need(original == copy, "whole native wrapper bytes")
        whole_equal(json.loads(original), row["whole_literal_object"], "whole original typed ordered object")

    archive = readj(local("NATIVE_ARCHIVE_LITERAL_BINDINGS.json"))
    need(len(archive["archives"]) == 1 and archive["regular_payload_occurrences"] == 33, "native ZIP and payload counts")
    for bound in archive["archives"]:
        checked(bound["whole_original_archive"])
        with zipfile.ZipFile(bound["whole_original_archive"]["path"]) as z:
            need(z.comment.hex() == bound["archive_comment_hex"], "whole ZIP comment")
            need(len(z.infolist()) == len(bound["members_in_original_order"]), "whole original ZIP order count")
            for info, row in zip(z.infolist(), bound["members_in_original_order"]):
                for key in ("filename", "compress_type", "create_system", "create_version", "extract_version", "reserved", "flag_bits", "volume", "internal_attr", "external_attr", "header_offset", "CRC", "compress_size", "file_size"):
                    need(getattr(info, key) == row[key], "literal ZIP metadata " + key)
                need(list(info.date_time) == row["date_time"] and info.comment.hex() == row["comment_hex"] and info.extra.hex() == row["extra_hex"] and info.is_dir() == row["is_dir"], "literal ZIP dates/comments/extra/type")
                payload = z.read(info)
                need(sha(payload) == row["whole_payload_SHA256"] and (zlib.crc32(payload) & 0xffffffff) == row["CRC"], "whole ZIP payload SHA and CRC")
                need(payload == Path(row["extracted"]).read_bytes(), "all extracted payload bytes, nested manifests included")

    replay = readj(local("NATIVE_EXECUTION_COMPARISON.json"))
    actual = checked(replay["normal"]["whole_stdout"], HERE)
    expected = checked(replay["original_expected"], HERE)
    stderr = checked(replay["normal"]["whole_stderr"], HERE)
    need(actual == expected and stderr == b"", "whole actual expected buffer identity and empty stderr")
    whole_equal(json.loads(actual), replay["whole_actual_literal_object"], "whole actual native typed object")
    whole_equal(json.loads(expected), replay["whole_original_expected_literal_object"], "whole original native typed object")
    need(replay["normal"]["actual_process_exit_code"] == 0 and replay["normal"]["optimization_flag"] == 0, "actual exit versus optimization flag")
    need(replay["native_normal_execution_count"] == 1 and replay["optimized_executed"] is False, "single native route, no optimized replay")
    need(sha(local("native-replay/check_realization.py").read_bytes()) == replay["selected_original_programme_SHA256"], "unchanged selected native body, not executed here")

    go = readj(local("PRIMARY_GO_METADATA_BINDING.json"))
    go_bytes = checked(go["exact_root_authority_by_reference"])
    need(sha(go_bytes) == GO, "actual root primary GO")
    whole_equal(json.loads(go_bytes), go["whole_literal_root_GO"], "whole literal root GO")
    raw = readj(local("RAW_PRIMARY_REFERENCE_BINDINGS_01.json"))
    raw_bytes = checked(raw["handoff_original_by_reference"])
    need(sha(raw_bytes) == RAW, "actual raw-only handoff")
    whole_equal(json.loads(raw_bytes), raw["whole_literal_raw_handoff"], "whole raw handoff transports")
    need(len(raw["referenced_original_raw_files"]) == 41, "complete listed raw file references")
    for row in raw["referenced_original_raw_files"]:
        checked(row)
    need(raw["primary_GETs_by_this_lane"] == 0 and raw["raw_bodies_copied_into_this_packet"] is False, "raw-only reference custody and zero own GETs")
    ledger = readj(local("PRIMARY_READ_LEDGER.json"))
    need(ledger["preexposure_initial_SHA256"] == INITIAL and ledger["preexposure_own_results_SHA256"] == RESULTS, "primary reading after exact evidence freezes")
    for row in ledger["items"]:
        checked(row["original_by_reference"])
        checked(row["own_reading_text"])

    negative_controls()
    verdict = readj(local("CUSTOM_VERDICT.json"))
    need(verdict["root_gate"] == "CLOSED" and verdict["followup"] is None and verdict["canonical_AA_assignment_authority"] is False and verdict["publication_authority"] is None and verdict["root_scientific_adoption"] is None, "no promotion authority")
    if preseal:
        need(not any(local(x).exists() for x in TERMINALS), "preseal is partial only, no outer terminals yet")
    else:
        seal = readj(local("FINAL_SEAL.json"))
        manifest = json.loads(checked(seal["manifest"], HERE))
        need(manifest["exact_outer_terminal_names"] == sorted(TERMINALS), "exact outer terminals only")
        need(seal["initial_SHA256"] == INITIAL and seal["own_results_SHA256"] == RESULTS, "final retains exact evidence freezes")
        for name, row in manifest["payloads"].items():
            checked(dict(row, path=name), HERE)
        af, ad = inventory(HERE)
        namespace(af, ad, set(manifest["payloads"]) | TERMINALS, manifest["directories"])
        checked(seal["whole_custom_verdict"], HERE)
        need(seal["root_gate"] == "CLOSED" and seal["followup"] is None, "final closed gate and no followup")
    print(json.dumps({"mode": "preseal-partial-binding-only" if preseal else "sealed-exact-namespace", "custody_checks": CHECKS, "native_executions_in_this_helper": 0, "network_subprocess_project_imports_or_writes": False, "root_gate": "CLOSED"}, sort_keys=True))


if __name__ == "__main__":
    main()
