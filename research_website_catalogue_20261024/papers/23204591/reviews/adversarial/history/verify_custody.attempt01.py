#!/usr/bin/env python3
"""Offline read-only custody, not scientific execution or proof validation.

Default requires the exact complete final file/directory namespace. --preseal
checks the same fixed source/interface bindings before final terminals exist;
its output explicitly does not claim a final owned-namespace closure.
"""
import hashlib
import io
import json
from pathlib import Path
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
INITIAL_SHA = "1f210d9ef32baff54b623d26c1a5f44da27d9bb94bf4b2cdb4271398ae216567"
SOURCE_READY_SHA = "b2ecdf3cb3933244d975519bc388193eb17cbbac1cd9ef234cc8bc264e8259cb"
EXACT_FINAL_TERMINALS = {"MANIFEST.json", "FINAL_SEAL.json"}
checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


def raw(path):
    p = Path(path)
    require(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), "ordinary file: " + str(p))
    return p.read_bytes()


def own(name):
    p = Path(name)
    require(not p.is_absolute() and ".." not in p.parts, "owned relative path: " + name)
    return ROOT / p


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_pin(path, binding):
    b = raw(path)
    require(len(b) == binding["bytes"], "size: " + str(path))
    require(sha(b) == binding["SHA256"], "SHA256: " + str(path))
    return b


def load(path):
    return json.loads(raw(path))


def literal(value):
    # Ordered serialization distinguishes object key/list order, bool/int,
    # strings, nulls, missing keys and nested native heterogeneous objects.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def same(left, right, label):
    require(literal(left) == literal(right), "whole ordered literal: " + label)


def namespace(folder):
    files, directories = [], []
    for p in sorted(folder.rglob("*")):
        require(not p.is_symlink(), "no symlink: " + str(p))
        mode = p.lstat().st_mode
        rel = p.relative_to(folder).as_posix()
        if stat.S_ISREG(mode):
            files.append(rel)
        elif stat.S_ISDIR(mode):
            directories.append(rel)
        else:
            raise RuntimeError("nonordinary namespace entry: " + str(p))
    return files, directories


def zip_member(info, body, extracted):
    return {
        "filename": info.filename, "date_time": list(info.date_time),
        "compress_type": info.compress_type, "comment_hex": info.comment.hex(),
        "extra_hex": info.extra.hex(), "create_system": info.create_system,
        "create_version": info.create_version, "extract_version": info.extract_version,
        "reserved": info.reserved, "flag_bits": info.flag_bits, "volume": info.volume,
        "internal_attr": info.internal_attr, "external_attr": info.external_attr,
        "header_offset": info.header_offset, "CRC": info.CRC,
        "compress_size": info.compress_size, "file_size": info.file_size,
        "is_dir": info.is_dir(), "whole_payload_SHA256": sha(body),
        "extracted": extracted,
    }


def main():
    preseal = sys.argv[1:] == ["--preseal"]
    require(preseal or sys.argv[1:] == [], "only optional --preseal is supported")
    initial_bytes = raw(ROOT / "INITIAL_SEAL.json")
    require(sha(initial_bytes) == INITIAL_SHA, "immutable initial proof/results seal")
    initial = json.loads(initial_bytes)
    require(len(initial["payloads"]) == 114, "whole114 initial payloads")
    for name, binding in initial["payloads"].items():
        verify_pin(own(name), binding)

    protected = load(ROOT / "PROTECTED_INPUTS.json")
    require(len(protected["files"]) == 110, "complete110 protected paths")
    require(len(protected["core_files"]) == 18, "qualified core18 paths")
    require(protected["core_qualification"] == "17original plus sole separately root-authorized405b checkpoint helper", "core qualification")
    for binding in protected["files"]:
        b = verify_pin(binding["path"], binding)
        require(raw(own(binding["copy"])) == b, "whole protected blob copy")
    ns = protected["source_namespace"]
    files, directories = namespace(Path(ns["path"]))
    same(files, ns["files"], "complete unchanged source file namespace")
    same(directories, ns["directories"], "complete unchanged source directory namespace")
    require(len(files) == 92 and len(directories) == 10, "source92/10")

    protocol = load(ROOT / "SOURCE_PROTOCOL_BINDINGS.json")
    def protocol_walk(value):
        if isinstance(value, dict):
            if "copy" in value and "whole_literal_object" in value:
                b = verify_pin(own(value["copy"]), value)
                same(json.loads(b), value["whole_literal_object"], "entire source/native protocol object")
            for child in value.values():
                protocol_walk(child)
        elif isinstance(value, list):
            for child in value:
                protocol_walk(child)
    protocol_walk(protocol)
    ready_wrapper = protocol["whole_SOURCE_READY"]
    require(ready_wrapper["SHA256"] == SOURCE_READY_SHA, "actual SOURCE_READY pin")
    ready = ready_wrapper["whole_literal_object"]
    require(type(ready["source_programmes_executed"]) is list and ready["source_programmes_executed"] == [], "historical empty-list execution flag")
    require(ready["printed_date"] is None and ready["printed_version"] is None, "historical unread printed fields stay null")
    require(ready["version_field_present"] is True and ready["version"] == "1.0.0", "native version present1.0.0")
    native_names = [a["original_api_file_object"]["key"] for a in ready["all_native_assets_in_original_order"]]
    same(native_names, ["README.md", "verification-supplement.zip", "source.zip", "paper.pdf"], "actual native asset order")

    archives = load(ROOT / "NATIVE_ARCHIVE_LITERAL_BINDINGS.json")
    payload_count = 0
    for archive in archives["archives"]:
        data = verify_pin(archive["whole_original_archive"]["path"], archive["whole_original_archive"])
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            require(z.comment.hex() == archive["archive_comment_hex"], "whole ZIP comment")
            require(len(z.infolist()) == len(archive["members_in_original_order"]), "ZIP original full member count")
            for info, expected in zip(z.infolist(), archive["members_in_original_order"]):
                body = z.read(info)  # zipfile validates original CRC while reading.
                same(zip_member(info, body, expected["extracted"]), expected, "whole ordered ZIP member metadata/payload")
                if not info.is_dir():
                    payload_count += 1
                    require(raw(expected["extracted"]) == body, "whole extracted native payload")
    require(payload_count == archives["regular_payload_occurrences"] == 19, "all19 native payload occurrences")

    primary_copy_count = 0
    for name in ["RAW_PRIMARY_COPY_BINDINGS_01_02.json", "RAW_PRIMARY_COPY_BINDINGS_03.json", "RAW_PRIMARY_COPY_BINDINGS_04.json"]:
        copied = load(ROOT / name)
        require(copied["raw_only_no_findings_received"] is True and copied["no_primary_GETs_by_this_lane"] is True, "raw-only acquisition boundary")
        for row in copied["copies"]:
            verify_pin(own(row["local_copy"]), row["original_binding"])
            require(row["whole_byte_identity"] is True, "literal raw copy identity")
            primary_copy_count += 1
    primary = load(ROOT / "PRIMARY_NATIVE_PIN_COMPARISON.json")
    expected_hashes = load(ROOT / "native-replay/SOURCE_HASHES.json")
    same(primary["whole_original_native_SOURCE_HASHES"], expected_hashes, "literal original source pin inventory")
    require(primary["remaining_native_keys_not_yet_acquired"] == [], "no missing native critical source pins")
    require(len(primary["comparisons"]) == len(expected_hashes["files"]) == 15, "all15 native primary bindings")
    require(len({r["native_key"] for r in primary["comparisons"]}) == 15, "unique native primary keys")
    for row in primary["comparisons"]:
        b = verify_pin(row["actual_owned_body"]["path"], row["actual_owned_body"])
        require(sha(b) == expected_hashes["files"][row["native_key"]] == row["native_expected_SHA256"], "direct independent actual primary/native pin")

    native = load(ROOT / "NATIVE_EXECUTION_COMPARISON.json")
    normal = verify_pin(own(native["normal"]["stdout"]["path"]), native["normal"]["stdout"])
    optimized = verify_pin(own(native["optimized"]["stdout"]["path"]), native["optimized"]["stdout"])
    expected = verify_pin(own(native["original_expected"]["path"]), native["original_expected"])
    require(normal == optimized == expected, "whole actual normal/-O/original expected buffers")
    require(native["normal"]["optimization_flag"] == 0 and native["optimized"]["optimization_flag"] == 1, "optimization flags distinct0/1")
    require(native["normal"]["process_exit_code"] == native["optimized"]["process_exit_code"] == 0, "actual process exits0/0")
    require(native["normal"]["assertions_enabled"] is True and native["optimized"]["assertions_enabled"] is False, "assertion-disabled optimized diagnostic")
    require(native["optimized"]["mathematical_verification"] is False, "no optimized mathematical validation")
    for label, body in [("normal", normal), ("optimized", optimized), ("original_expected", expected)]:
        same(json.loads(body), native[label + "_complete_literal_object"], "whole native result " + label)
    for label in ["normal", "optimized"]:
        require(verify_pin(own(native[label]["stderr"]["path"]), native[label]["stderr"]) == b"", "whole actual empty stderr")
    checker = raw(ROOT / "native-replay/restriction_geometry_check.py")
    require(sha(checker) == native["selected_original_programme_SHA256"], "unchanged selected native checker")
    original_checker = Path(ns["path"]) / "published-source/asset-003/restriction_geometry_check.py"
    require(checker == raw(original_checker), "whole native checker copy identity; no execution")

    verdict = load(ROOT / "CUSTOM_VERDICT.json")
    same(verdict["whole_literal_native_expected_result"], json.loads(expected), "verdict whole native result")
    same(verdict["whole_literal_source_custom_verdict"], protocol["CUSTOM_VERDICT.json"]["whole_literal_object"], "verdict whole historical custom dictionary")
    same(verdict["native_identity_observations"]["whole_original_assets_in_native_order"], ready["all_native_assets_in_original_order"], "whole heterogeneous original native assets")
    same(verdict["native_identity_observations"]["native_asset_order_names"], native_names, "own native names derived from actual nested schema")
    require(verdict["followup"] is None and verdict["canonical_AA_assignment_authority"] is False and verdict["publication_authority"] is None and verdict["root_adoption"] is None, "separate null/false authority fields")
    require(verdict["root_science_gate"] == "CLOSED", "root gate remains closed")
    require(verdict["rights"]["MIT_instrument"] is None, "no invented MIT instrument")

    if not preseal:
        manifest_bytes = raw(ROOT / "MANIFEST.json")
        manifest = json.loads(manifest_bytes)
        seal = load(ROOT / "FINAL_SEAL.json")
        require(seal["status"] == "FINAL", "immutable final status")
        require(seal["manifest"]["bytes"] == len(manifest_bytes) and seal["manifest"]["SHA256"] == sha(manifest_bytes), "whole final manifest pin")
        same(seal["exact_root_terminals"], sorted(EXACT_FINAL_TERMINALS), "exact two root terminals only")
        files, directories = namespace(ROOT)
        require(set(files) == set(manifest["payloads"]) | EXACT_FINAL_TERMINALS, "strict complete final file namespace")
        same(directories, manifest["directories"], "strict complete final directory namespace")
        require(len(manifest["payloads"]) == seal["payload_files"] and len(files) == seal["actual_files"] and len(directories) == seal["directories"], "whole final counts")
        for name, binding in manifest["payloads"].items():
            require(name not in EXACT_FINAL_TERMINALS, "no root terminal as payload")
            verify_pin(own(name), binding)
        verify_pin(ROOT / "CUSTOM_VERDICT.json", seal["custom_verdict"])
        require(seal["initial_seal_SHA256"] == INITIAL_SHA, "final initial-seal pin")
    print(json.dumps({"custody_status": "PASS", "mode": "preseal fixed bindings only" if preseal else "final complete namespace", "checks": checks, "source_files": 92, "protected_paths": 110, "native_ZIP_regular_payload_occurrences": payload_count, "raw_primary_copy_references": primary_copy_count, "native_primary_pin_matches": 15, "scientific_programmes_executed_by_this_helper": [], "writes": False, "network": False, "root_science_gate": "CLOSED"}, indent=2))


if __name__ == "__main__":
    main()
