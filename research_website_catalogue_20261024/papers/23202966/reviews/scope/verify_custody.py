#!/usr/bin/env python3
"""Pure whole-byte/type/namespace custody only; no scientific replay.

Default is read-only: no network, subprocess, writes or project imports.
Only --preseal permits the two exact not-yet-created final control files.
"""
from pathlib import Path
import hashlib
import json
import stat
import sys
import zipfile

BASE = Path(__file__).resolve().parent
TERMINALS = ("MANIFEST.json", "CLOSURE.json", "FINAL_SEAL.json")
SOURCE_READY_SHA = "86264fb9c694c35abcdcae60fd15aaa617627204ceb8e0cd95b09947e4d893dc"
SOURCE_SEAL_SHA = "9a87a851ebab2735927edb66d350168fdb9d20e738ab6a9bc2e85b7f3a93ed63"
INITIAL_SHA = "9de330f9de3a7946d694cdf062b3fa05ec8b0d7ba135b771071a056e793571c1"
checks = 0


def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin_check(item):
    p = Path(item["path"])
    require(p.is_absolute() and p.is_file() and not p.is_symlink(), "pinned regular absolute file: " + str(p))
    b = p.read_bytes()
    require(len(b) == item["bytes"], "size: " + str(p))
    require(hashlib.sha256(b).hexdigest() == item["SHA256"], "SHA256: " + str(p))
    return p


def safe_relative(name):
    p = Path(name)
    require(isinstance(name, str) and name != "" and not p.is_absolute(), "relative path")
    require(str(p) == name and all(x not in ("", ".", "..") for x in p.parts), "safe path: " + name)
    return p


def namespace(root):
    files, dirs = [], []
    require(root.is_dir() and not root.is_symlink(), "regular root: " + str(root))
    for p in root.rglob("*"):
        mode = p.lstat().st_mode
        require(not stat.S_ISLNK(mode), "no symlink: " + str(p))
        rel = str(p.relative_to(root))
        if stat.S_ISDIR(mode):
            dirs.append(rel)
        else:
            require(stat.S_ISREG(mode), "regular namespace entry: " + str(p))
            files.append(rel)
    return sorted(files), sorted(dirs)


def typed_equal(a, b):
    require(type(a) is type(b), "literal JSON type")
    if isinstance(a, dict):
        require(list(a) == list(b), "original JSON key order")
        for k in a:
            typed_equal(a[k], b[k])
    elif isinstance(a, list):
        require(len(a) == len(b), "original JSON array length/order")
        for x, y in zip(a, b):
            typed_equal(x, y)
    else:
        require(a == b, "literal JSON scalar/null")


def contained(p, root):
    require(p.is_relative_to(root), "pinned path remains inside bound namespace")


def main():
    require(sys.argv[1:] in ([], ["--preseal"]), "only explicit --preseal is supported")
    preseal = sys.argv[1:] == ["--preseal"]
    manifest = load(BASE / "MANIFEST.json")
    require(manifest["schema"] == "scope_exact_namespace_manifest_23202966_v1", "manifest schema")
    require(manifest["exact_root_terminal_controls"] == list(TERMINALS), "only exact root terminal controls")
    names = [x["relative_path"] for x in manifest["files"]]
    require(len(names) == len(set(names)), "unique manifest paths")
    for x in manifest["files"]:
        rel = safe_relative(x["relative_path"])
        require(str(rel) not in TERMINALS, "only root controls excluded; nested terminal basenames stay included")
        p = BASE / rel
        pin_check({"path": str(p), "bytes": x["bytes"], "SHA256": x["SHA256"]})
    actual_files, actual_dirs = namespace(BASE)
    expected_terminals = ["MANIFEST.json"] if preseal else list(TERMINALS)
    require(actual_files == sorted(names + expected_terminals), "exact entire owned file namespace")
    require(actual_dirs == manifest["directories"], "exact entire owned directory namespace")
    if preseal:
        require(not (BASE / "CLOSURE.json").exists() and not (BASE / "FINAL_SEAL.json").exists(), "preseal cannot ignore existing terminal bodies")
    else:
        seal = load(BASE / "FINAL_SEAL.json")
        require(seal["schema"] == "scope_final_seal_23202966_v1", "final schema")
        require(seal["record_id"] == 23202966 and seal["sheet_row"] == 135, "target identity")
        require(seal["root135_gate"] == "CLOSED" and seal["scientific_findings_released"] is False, "closed comparison gate")
        require(seal["exact_root_terminal_controls"] == list(TERMINALS), "seal terminal scope")
        require(pin_check(seal["manifest"]) == BASE / "MANIFEST.json", "exact manifest path")
        require(pin_check(seal["closure"]) == BASE / "CLOSURE.json", "exact closure path")
        require(load(BASE / "CLOSURE.json")["status"] == "PASS", "preseal closure successful")

    binding = load(BASE / "ORIGINAL_SOURCE_BINDING.json")
    source = Path(binding["source_root"])
    copy = Path(binding["private_copy_root"])
    contained(copy, BASE)
    source_files, source_dirs = namespace(source)
    copy_files, copy_dirs = namespace(copy)
    source_names = [x["relative_path"] for x in binding["files"]]
    require(len(source_names) == 82 and len(set(source_names)) == 82, "82 originals =79payloads+3controls")
    require(source_files == sorted(source_names) == copy_files, "whole source and private copy namespace")
    require(source_dirs == binding["original_directories"] == copy_dirs, "whole source/private-copy directories")
    for x in binding["files"]:
        rel = safe_relative(x["relative_path"])
        original = pin_check(x["original"])
        copied = pin_check(x["exact_private_copy"])
        require(original == source / rel and copied == copy / rel, "exact original/copy path binding")
        require(original.read_bytes() == copied.read_bytes(), "whole original bytes unmodified")
    require(digest(source / "SOURCE_READY.json") == SOURCE_READY_SHA, "original READY pin")
    require(digest(source / "SOURCE_READY_SEAL.json") == SOURCE_SEAL_SHA, "original source seal pin")
    require(digest(BASE / "INITIAL_SEAL.json") == INITIAL_SHA, "independent paper-first initial unchanged")
    initial_manifest = pin_check(load(BASE / "INITIAL_SEAL.json")["manifest"])
    initial = load(initial_manifest)
    require(len(initial["files"]) == 23, "complete initial payload count")
    for x in initial["files"]:
        pin_check(x)

    interface = load(BASE / "SOURCE_INTERFACE.json")
    for x in interface["all_original_JSON_objects_and_native_API_objects_in_input_order"]:
        p = pin_check(x["original"])
        q = pin_check(x["exact_private_copy"])
        contained(p, source)
        contained(q, copy)
        typed_equal(load(p), x["whole_original_object"])
        typed_equal(load(q), x["whole_original_object"])
    typed_equal(load(source / "CUSTOM_VERDICT.json"), interface["whole_source_custom_verdict"])
    ready = load(source / "SOURCE_READY.json")
    require(ready["version_field_present"] is False and ready["version"] is None, "native ABSENT version preserved")
    require(ready["printed_title_date_version_inspected"] is False and ready["printed_date"] is None and ready["printed_version"] is None, "historical source UNREAD literal fields")
    require([x["native_key"] for x in binding["whole_native_assets_in_original_order"]] == ["README.md", "paper.pdf", "main.tex", "verification.zip"], "native asset order")
    for x in binding["whole_native_assets_in_original_order"]:
        p = pin_check(x["original"])
        b = p.read_bytes()
        require(hashlib.md5(b).hexdigest() == x["native_MD5"], "native MD5")
        require(x["whole_original_API_file_object"]["checksum"] == "md5:" + x["native_MD5"], "whole native checksum field")

    zpath = pin_check(binding["original_ZIP"])
    with zipfile.ZipFile(zpath) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        rows = binding["all28regular_payloads_in_native_central_directory_order"]
        require(len(infos) == len(rows) == 28, "all28 regular ZIP payloads")
        for info, x in zip(infos, rows):
            require(info.filename == x["filename"], "original ZIP member order/name")
            require(not info.flag_bits & 1, "no encrypted source member")
            require(stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG), "regular source ZIP member")
            actual = ["%08x" % info.CRC, info.file_size, info.compress_size, info.compress_type, info.flag_bits, list(info.date_time), info.external_attr, info.create_system]
            expected = [x[k] for k in ("CRC32", "file_size", "compress_size", "compress_type", "flag_bits", "date_time", "external_attr", "create_system")]
            require(actual == expected, "whole native ZIP central-directory fields")
            b = z.read(info)
            require(len(b) == info.file_size and hashlib.sha256(b).hexdigest() == x["body_SHA256"], "whole ZIP CRC/size/SHA256")
            p = pin_check(x["whole_extracted_source"])
            contained(p, source)
            require(p.read_bytes() == b, "whole ZIP/extracted original equality")

    primary = load(BASE / "PRIMARY_CUSTODY.json")
    for entry in primary["transports_in_receipt_path_order_not_claimed_global_request_order"]:
        p = pin_check(entry["receipt"])
        contained(p, BASE / "primary")
        obj = load(p)
        typed_equal(obj, entry["whole_original_transport_object"])
        for hop in obj["actual_requests"]:
            require(isinstance(hop["ordered_response_headers"], list), "ordered whole response headers")
            for key in ("whole_body", "whole_received_partial_body", "actual_sent_request_bytes"):
                if key in hop:
                    q = pin_check(hop[key])
                    contained(q, BASE / "primary")
    for entry in primary["failures_preserved_whole"]:
        p = pin_check(entry["receipt"])
        contained(p, BASE / "primary")
        typed_equal(load(p), entry["whole_original_failure_object"])
    pin_check(primary["critical_raw_share_index"])
    verdict = load(BASE / "VERDICT.json")
    require(verdict["follow_up"] is None and verdict["canonical_url"] is None and verdict["AA"] is None, "literal null boundaries")
    require(verdict["root135_comparison_gate"] == "CLOSED" and verdict["scientific_findings_released"] is False, "findings withheld")
    require(verdict["supplied_scientific_programmes_imported_or_executed"] == [], "no supplied scientific execution")
    return {"status": "PASS", "phase": "preseal" if preseal else "final", "custody_predicates": checks, "owned_payloads": len(names), "source_complete_files": 82, "source_manifest_payloads": 79, "native_assets": 4, "ZIP_regular_payloads": 28, "science_executed": False, "network_subprocess_writes_project_imports": False, "root135_gate": "CLOSED"}


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, separators=(",", ":")))
