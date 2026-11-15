"""Offline metadata/custody verification, with no writes or source execution.

This self-authored checker imports only Python's standard library. It hashes
scientific artifacts as opaque bytes, and reads native metadata and custody
objects as data. It does not evaluate mathematical or program content.
"""

import hashlib
import json
from pathlib import Path
import sys
import zipfile
import zlib


HERE = Path(__file__).resolve().parent
CHECKS = []


def check(condition, label):
    CHECKS.append({"check": label, "pass": bool(condition)})


def load(path):
    return json.loads(Path(path).read_bytes())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_binding(binding):
    path = Path(binding["path"])
    data = path.read_bytes()
    check(len(data) == binding["bytes"], "bytes:" + str(path))
    check(sha(data) == binding["SHA256"], "SHA256:" + str(path))


def typed_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(typed_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def structure(obj, pointer=""):
    row = {"JSON_pointer": pointer, "original_type": type(obj).__name__}
    if isinstance(obj, dict):
        row["original_keys_in_order"] = list(obj)
    if obj is None or isinstance(obj, (list, dict)) and len(obj) == 0:
        row["original_empty_or_null_value"] = obj
    rows = [row]
    if isinstance(obj, dict):
        for key, value in obj.items():
            token = str(key).replace("~", "~0").replace("/", "~1")
            rows.extend(structure(value, pointer + "/" + token))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            rows.extend(structure(value, pointer + "/" + str(index)))
    return rows


def main():
    expected = load(HERE / "EXPECTATIONS.json")
    whole = load(HERE / "WHOLE_SOURCE_BINDINGS.json")
    inputs = load(HERE / "INPUT_BINDINGS.json")
    inventory = load(HERE / "CUSTOM_OBJECT_TYPES_AND_KEYLISTS.json")
    source = Path(whole["source_root"])
    actual_paths = sorted(str(p.relative_to(source)) for p in source.rglob("*") if p.is_file())
    expected_paths = sorted(v["relative_path"] for v in whole["files"])
    check(actual_paths == expected_paths, "exact-whole-source-namespace")
    check(len(actual_paths) == 121, "source-files-121")
    check(not any(p.is_symlink() for p in source.rglob("*")), "no-source-symlinks")
    for binding in whole["files"]:
        verify_binding(binding)
    for binding in inputs["root_source_two_verdict_two_seal_bindings"]:
        verify_binding(binding)
    check(len(inputs["root_source_two_verdict_two_seal_bindings"]) == 6, "six-current-binding-lookups")
    for item in inputs["opaque_raw_copies"]:
        verify_binding(item["original"])
        verify_binding(item["copy"])
        check(Path(item["original"]["path"]).read_bytes() == Path(item["copy"]["path"]).read_bytes(),
              "raw-copy-exact:" + item["original"]["path"])
    check("private/" in (HERE / ".gitignore").read_text().splitlines(), "private-raw-ignore")

    ready = load(source / "SOURCE_READY.json")
    seal = load(source / "SOURCE_READY_SEAL.json")
    source_manifest = load(source / "SOURCE_READY_MANIFEST.json")
    for field, name in [("SOURCE_READY_SHA256", "SOURCE_READY.json"),
                        ("MANIFEST_SHA256", "SOURCE_READY_MANIFEST.json"),
                        ("CLOSURE_SHA256", "SOURCE_READY_CLOSURE.json"),
                        ("SOURCE_CUSTODY_PROOF_SHA256", "SOURCE_CUSTODY_PROOF.md"),
                        ("INPUT_MANIFEST_SHA256", "INPUT_MANIFEST.json")]:
        check(sha((source / name).read_bytes()) == seal[field], "source-seal:" + field)
    check(len(source_manifest["files"]) == 118, "source-manifest-payloads-118")
    check(set(actual_paths) == {v["path"] for v in source_manifest["files"]}
          | set(source_manifest["excluded_terminal_files"]), "manifest-plus-declared-terminals")
    for binding in source_manifest["files"]:
        data = (source / binding["path"]).read_bytes()
        check(len(data) == binding["bytes"] and sha(data) == binding["SHA256"],
              "source-manifest-payload:" + binding["path"])

    clearance = load(inputs["root_source_two_verdict_two_seal_bindings"][0]["path"])
    check(typed_equal(ready, clearance["source_ready_whole_original"]), "whole-source-ready-types-values-order")
    # Scientific verdicts and seals are used only as file bindings above.
    check(clearance["separate_code_instrument"] is None, "separate-code-instrument-null")
    check(clearance["authored_note_and_support_license"] == "CC BY4.0", "broad-CC-BY-root-literal")

    for item in inventory["source_custom_objects"]:
        verify_binding(item["original"])
        check(typed_equal(structure(load(item["original"]["path"])), item["structure"]),
              "source-custom-object-types-keys:" + item["original"]["path"])
    original_native_types = []
    native_objects = []
    duplicate_keys = []

    def pairs(pairs_list):
        result = {}
        for key, value in pairs_list:
            if key in result:
                duplicate_keys.append(key)
            result[key] = value
        return result

    for item in inventory["native_API_objects"]:
        verify_binding(item["original"])
        obj = json.loads(Path(item["original"]["path"]).read_bytes(), object_pairs_hook=pairs)
        rows = structure(obj)
        check(typed_equal(rows, item["whole_structure"]), "native-whole-keylist-types:" + item["role"])
        native_objects.append(obj)
        for row in rows:
            entry = {"role": item["role"], "JSON_pointer": row["JSON_pointer"],
                     "original_type": row["original_type"]}
            if "original_empty_or_null_value" in row:
                entry["original_empty_or_null_value"] = row["original_empty_or_null_value"]
            original_native_types.append(entry)
    check(not duplicate_keys, "no-native-JSON-duplicate-keys")
    check(typed_equal(original_native_types, load(source / "NATIVE_SCHEMA_TYPES.json")),
          "whole-original-native-type-tree")
    record, latest, versions, files = native_objects
    published = [record, latest] + versions["hits"]["hits"]
    for index, obj in enumerate(published):
        check("version" not in obj and "version" not in obj["metadata"], "native-version-ABSENT:" + str(index))
        check(obj["metadata"]["publication_date"] == "2026-10-15", "native-publication-date:" + str(index))
        check(obj["metadata"]["access_right"] == "open", "native-access-open:" + str(index))
        check(typed_equal(obj["metadata"]["license"], {"id": "cc-by-4.0"}), "native-license-object:" + str(index))
    check(ready["version_field_present"] is False and ready["version"] is None, "absence-not-null-version")
    check(type(versions["hits"]["total"]) is int and versions["hits"]["total"] == 1, "versions-total-integer-one")
    check(len(versions["hits"]["hits"]) == 1 and "next" not in versions["links"], "versions-one-no-next")
    check(type(record["swh"]) is dict and record["swh"] == {}, "record-swh-empty-object")
    check(type(latest["swh"]) is dict and latest["swh"] == {}, "latest-swh-empty-object")
    check(versions["hits"]["hits"][0]["swh"] is None, "versions-swh-null")
    order = ["five_centers.pdf", "five_centers.tex", "verification-package.zip"]
    check([x["key"] for x in record["files"]] == order, "record-file-array-order")
    check(type(files["entries"]) is list and [x["key"] for x in files["entries"]] == order, "native-entries-array-order")
    check(type(files["order"]) is list and files["order"] == [], "native-order-is-empty-list")
    check(files["default_preview"] is None, "native-default-preview-null")
    check(all(typed_equal(x["access"], {"hidden": False}) for x in files["entries"]), "file-access-hidden-false")
    check(len(ready["all_native_assets_in_original_order"]) == 3, "native-assets-three")
    check(ready["selected_actual_PDF"]["pages"] == 6, "sealed-PDF-pages-six")

    transports = load(source / "ALL_TRANSPORT_RECEIPTS.json")
    check([t["HTTP_status"] for t in transports] == [200, 301, 200, 200, 200, 200, 200, 200], "all-native-statuses")
    check(len(transports) == 8, "actual-native-HTTP-count-eight")
    for index, receipt in enumerate(transports):
        verify_binding({"path": receipt["body_path"], "bytes": receipt["bytes"], "SHA256": receipt["SHA256"]})
        check(type(receipt["actual_request_headers_in_sent_order"]) is list
              and type(receipt["response_headers_in_received_order"]) is list, "ordered-header-arrays:" + str(index))
    for path in source.glob("*.transport.json"):
        receipt = load(path)
        check(any(typed_equal(receipt, t) for t in transports), "whole-transport-object:" + path.name)
    check(transports[1]["HTTP_status"] == 301 and transports[1]["bytes"] == 99, "original-redirect-body-retained")

    archive = load(source / "ARCHIVE_CUSTODY.json")
    check(len(archive["containers"]) == 1 and archive["nested_archive_count"] == 0, "one-ZIP-no-nested")
    occurrences = archive["regular_payload_occurrences"]
    check(len(occurrences) == 64, "ZIP-occurrences-64")
    container = archive["containers"][0]
    with zipfile.ZipFile(container["input_path"]) as handle:
        entries = [(i, info) for i, info in enumerate(handle.infolist()) if not info.is_dir()]
        check(len(entries) == 64, "actual-ZIP-regular-entries-64")
        for occurrence, (ordinal, info) in zip(occurrences, entries):
            payload = handle.read(info)
            check(occurrence["ordinal_zero_based"] == ordinal and occurrence["original_member_name"] == info.filename,
                  "ZIP-native-order:" + str(ordinal))
            check(len(payload) == occurrence["bytes"] and sha(payload) == occurrence["SHA256"],
                  "ZIP-payload-bytes-SHA:" + str(ordinal))
            check(payload == Path(occurrence["extracted_path"]).read_bytes(), "ZIP-extracted-byte-equality:" + str(ordinal))
            crc = zlib.crc32(payload) & 0xffffffff
            check(format(crc, "08x") == occurrence["CRC32"] and crc == info.CRC, "ZIP-CRC:" + str(ordinal))
            check(info.file_size == len(payload) and info.compress_size == occurrence["compressed_bytes"]
                  and info.compress_type == occurrence["compression_method"], "ZIP-size-compression:" + str(ordinal))
            check(info.external_attr == occurrence["native_external_attr"]
                  and info.create_system == occurrence["native_create_system"]
                  and info.flag_bits == occurrence["native_flags"]
                  and list(info.date_time) == occurrence["native_date_time"], "ZIP-native-flags-time:" + str(ordinal))
        check(handle.comment.hex() == container["original_archive_comment_hex"], "ZIP-native-comment")
    check(Path(ready["selected_actual_PDF"]["path"]).read_bytes()
          == Path(ready["embedded_PDFs"][0]["extracted_path"]).read_bytes(), "standalone-archived-PDF-equal")
    check(Path(ready["actual_standalone_TeX_assets"][0]["path"]).read_bytes()
          == Path(ready["controlling_TeX"]["extracted_path"]).read_bytes(), "standalone-archived-TeX-equal")
    check(expected["scientific_assessment"] is None and expected["owner_editorial_folder_read"] is False,
          "metadata-scope-only")

    if (HERE / "SEAL.json").exists():
        own_seal = load(HERE / "SEAL.json")
        actual = sorted(str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file() and p.name != "SEAL.json")
        check(actual == sorted(x["relative_path"] for x in own_seal["files"]), "exact-sealed-support-namespace")
        for binding in own_seal["files"]:
            data = (HERE / binding["relative_path"]).read_bytes()
            check(len(data) == binding["bytes"] and sha(data) == binding["SHA256"],
                  "sealed-support:" + binding["relative_path"])
    failures = [c for c in CHECKS if not c["pass"]]
    print(json.dumps({"status": "PASS" if not failures else "FAIL", "checks": len(CHECKS),
                      "failures": failures, "optimized": not __debug__, "network_requests": 0,
                      "writes": 0, "project_or_supplied_code_executed": [],
                      "scientific_assessment": None}, indent=2))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
