#!/usr/bin/env python3
"""Standalone offline read-only byte/object/namespace custody, never scientific replay."""
from pathlib import Path, PurePosixPath
import ast
import base64
import hashlib
import json
import stat
import sys
import zipfile
import zlib

A = Path(__file__).resolve().parent
S = A.parents[1] / "sources"
TERMINALS = ["CLOSURE.json", "FINAL_SEAL.json", "OWNED_MANIFEST.json"]
CHECKS = 0


def need(ok, why):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise RuntimeError(why)


def load(p):
    return json.loads(p.read_bytes())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pin(p, expected):
    need(stat.S_ISREG(p.lstat().st_mode), "regular pinned file: " + str(p))
    b = p.read_bytes()
    need(len(b) == expected["bytes"], "whole byte count: " + str(p))
    need(hashlib.sha256(b).hexdigest() == expected["SHA256"], "whole SHA256: " + str(p))


def relsafe(name):
    q = PurePosixPath(name)
    need(type(name) is str and bool(name) and not q.is_absolute(), "relative member")
    need(".." not in q.parts and "." not in q.parts and "\\" not in name and "\0" not in name and ":" not in name, "safe member")
    return q


def namespace(root):
    files, dirs = [], []
    for p in sorted(root.rglob("*")):
        mode = p.lstat().st_mode
        rel = p.relative_to(root).as_posix()
        relsafe(rel)
        need(not stat.S_ISLNK(mode), "no symlink: " + rel)
        if stat.S_ISDIR(mode):
            dirs.append(rel)
        else:
            need(stat.S_ISREG(mode), "no special file: " + rel)
            files.append(rel)
    need(len(files) == len(set(x.casefold() for x in files)), "no case-colliding files")
    need(len(dirs) == len(set(x.casefold() for x in dirs)), "no case-colliding directories")
    return files, dirs


def same(x, y):
    need(type(x) is type(y), "literal JSON type")
    if type(x) is dict:
        need(list(x) == list(y), "whole object key order")
        for key in x:
            same(x[key], y[key])
    elif type(x) is list:
        need(len(x) == len(y), "whole array length")
        for left, right in zip(x, y):
            same(left, right)
    else:
        need(x == y, "whole literal JSON value")


class ObjectPairs(list):
    pass


def typed(value):
    if isinstance(value, ObjectPairs):
        return {"type": "object", "ordered_pairs": [[key, typed(item)] for key, item in value]}
    if type(value) is list:
        return {"type": "array", "items": [typed(item) for item in value]}
    names = {type(None): "null", bool: "boolean", int: "integer", float: "number", str: "string"}
    return {"type": names[type(value)], "literal_value": value}


def early():
    expected = [("INITIAL_SEAL.json", "087144bfa352a5236528c552ea4c31650da8a0b7ac0aa4fae746769b56717101"), ("OWN_PROOF_CONTROL_SEAL.json", "70820956f8fc2da8d8790b2ee01bf83221d6e37ee5d5fb5ad4e6dc627113c34d")]
    for name, digest in expected:
        need(sha(A / name) == digest, "immutable early seal")
        seal = load(A / name)
        item = seal["manifest"]
        p = Path(item["path"])
        need(p.parent == A, "early manifest boundary")
        pin(p, item)
        for entry in load(p)["files"]:
            q = Path(entry["path"])
            need(q.is_relative_to(A), "early payload boundary")
            pin(q, entry)


def source():
    need(sha(S / "SOURCE_READY.json") == "bd5708d6fa77da017786d34952a3d689b5b5fb2703086bc4d33a1093430ed4cb", "original READY")
    need(sha(S / "SOURCE_READY_SEAL.json") == "cf9ffb0b5f509af974aa3e7a368c2672e000f2665aecf772a0df57f658145287", "original source seal")
    original = load(A / "SOURCE_INPUT_MANIFEST.json")
    bindings = load(A / "SOURCE_CUSTODY_BINDINGS.json")
    entries = original["complete_source_files"]
    need(len(entries) == 101 and len(bindings["whole_file_bindings"]) == 101, "101 original source files")
    expected_files = [Path(e["path"]).relative_to(S).as_posix() for e in entries]
    files, dirs = namespace(S)
    need(files == sorted(expected_files), "exact complete source namespace")
    same(dirs, original["exact_complete_source_directories"])
    need(len(dirs) == 18, "18 source directories")
    copies = A / "raw/source-originals"
    copied_files, copied_dirs = namespace(copies)
    same(copied_files, files)
    same(copied_dirs, dirs)
    for entry, binding in zip(entries, bindings["whole_file_bindings"]):
        p = Path(entry["path"])
        rel = p.relative_to(S).as_posix()
        same(binding["original"], entry)
        need(binding["relative_path"] == rel, "source binding order/path")
        q = copies / rel
        need(Path(binding["copy"]["path"]) == q, "copy boundary")
        pin(p, entry)
        pin(q, binding["copy"])
        need(p.read_bytes() == q.read_bytes(), "source copy exact whole bytes")
    objects = load(A / "PROVIDED_SOURCE_OBJECTS.json")["whole_original_JSON_objects_in_source_path_order"]
    tapes = load(A / "ORIGINAL_JSON_TYPE_TAPES.json")["objects"]
    json_entries = [e for e in entries if Path(e["path"]).suffix == ".json"]
    need(len(objects) == len(tapes) == len(json_entries) == 50, "all50 original JSON objects")
    for entry, obj, tape in zip(json_entries, objects, tapes):
        p = Path(entry["path"])
        rel = p.relative_to(S).as_posix()
        need(obj["relative_path"] == tape["relative_path"] == rel, "all source object order")
        same(load(p), obj["original_whole_object"])
        same(typed(json.loads(p.read_bytes(), object_pairs_hook=ObjectPairs)), tape["whole_typed_ordered_JSON"])
    r = load(S / "SOURCE_READY.json")
    need(r["version_field_present"] is False and r["version"] is None, "native VERSION ABSENT")
    need(r["printed_title_date_version_inspected"] is False and r["printed_date"] is None and r["printed_version"] is None, "historical printed UNREAD false/null")
    need(r["source_programmes_executed"] is False, "source historical nonexecution")
    native = r["all_native_assets_in_original_order"]
    need([e["original_api_file_object"]["key"] for e in native] == ["paper.pdf", "cost-betti-source-and-verification.zip"], "whole native asset order")
    for entry in native:
        p = Path(entry["path"])
        need(p.is_relative_to(S), "native asset boundary")
        pin(p, entry)
        need(p.read_bytes() == Path(entry["transport_body_path"]).read_bytes(), "native whole response body")
        need("md5:" + hashlib.md5(p.read_bytes()).hexdigest() == entry["original_api_file_object"]["checksum"], "native MD5")
    need(Path(r["selected_actual_PDF"]["path"]).read_bytes() == (S / "published-source/asset-002/paper.pdf").read_bytes(), "embedded PDF whole byte equality")
    need(len(Path(r["controlling_TeX"]["extracted_path"]).read_bytes().splitlines()) == 198, "198 opaque TeX lines")
    return r


def archives():
    custody = load(S / "ARCHIVE_CUSTODY.json")
    need(len(custody["containers"]) == 1 and custody["whole_regular_payload_occurrences"] == 35, "one container35 regular occurrences")
    c = custody["containers"][0]
    archive_path = Path(c["input_path"])
    need(archive_path.is_relative_to(S), "archive boundary")
    need(sha(archive_path) == c["input_SHA256"], "original ZIP hash")
    with zipfile.ZipFile(archive_path) as z:
        infos = z.infolist()
        need(len(infos) == len(c["members"]) == 35, "all original central directory entries")
        need(len({i.filename.casefold() for i in infos}) == len(infos), "no ZIP case collision")
        for ordinal, (i, e) in enumerate(zip(infos, c["members"])):
            relsafe(i.filename)
            need(not i.is_dir() and not i.flag_bits & 1, "regular unencrypted ZIP payload")
            need(stat.S_IFMT(i.external_attr >> 16) in (0, stat.S_IFREG), "no archive symlink/special file")
            need(e["ordinal_zero_based"] == ordinal and e["original_member_name"] == i.filename, "original ZIP list order")
            body = z.read(i)
            q = Path(e["extracted_path"])
            need(q == Path(c["extraction_root"]) / i.filename and q.is_relative_to(S), "archive extraction boundary")
            need(len(body) == e["bytes"] == i.file_size, "native ZIP uncompressed size")
            need(body == q.read_bytes(), "ZIP whole source equality")
            need(hashlib.sha256(body).hexdigest() == e["SHA256"], "ZIP payload SHA256")
            need(format(zlib.crc32(body) & 0xffffffff, "08x") == e["CRC32"] == format(i.CRC, "08x"), "native ZIP CRC")
            need(i.compress_size == e["compressed_bytes"] and i.compress_type == e["compression_method"], "ZIP compression")
            need(i.external_attr == e["native_external_attr"] and i.create_system == e["native_create_system"] and i.flag_bits == e["native_flags"], "native central flags")
            same(list(i.date_time), e["native_date_time"])
    same(c["members"], custody["regular_payload_occurrences"])


def primary():
    index = A / "primary/RAW_HANDOFF_INDEX.owner-original.json"
    need(sha(index) == "b43f3491b60c226e814ce7c8ea9f0c9355a8a2dc1d16d81bea2a58456d8d1818", "whole handoff index")
    raw = load(index)
    bindings = load(A / "primary/SHARED_RAW_BINDINGS.json")
    need(raw["scientific_interpretations_or_results_included"] is False, "raw-only handoff")
    need(len(raw["raw_files"]) == len(bindings["whole56provided_raw_files"]) == 56, "56 whole provided raw files")
    for entry, binding in zip(raw["raw_files"], bindings["whole56provided_raw_files"]):
        same(entry, binding["owner_original"])
        p = Path(binding["scope_copy"]["path"])
        need(p.is_relative_to(A / "primary/shared-raw"), "scope-owned raw copy boundary")
        pin(p, entry)
        pin(p, binding["scope_copy"])
    need(bindings["own_primary_GET_count"] == 0 and type(bindings["own_primary_GET_count"]) is int, "zero own primary GET")
    failure = load(A / "FAILURE_HISTORY.json")
    same(raw["initial_transport_qualification"], failure["initial_owner_transport_qualification_literal"])
    same(raw["partial_first_additional_attempt"], failure["first_additional_attempt_whole_original_object"])
    api = load(A / "primary/shared-raw/primary/extra/openai-contents.hop0.body")
    body = base64.b64decode(api["content"])
    need(body == (A / "primary/openai-pinned.pdf").read_bytes(), "whole contents decoded PDF")
    need(hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest() == api["sha"], "native Git blob identity")


def safe_current_helper():
    tree = ast.parse(Path(__file__).read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name.split(".")[0] for alias in node.names] if isinstance(node, ast.Import) else [node.module]
            need(all(n in {"pathlib", "ast", "base64", "hashlib", "json", "stat", "sys", "zipfile", "zlib"} for n in names), "only declared stdlib imports")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            need(node.func.attr not in {"write_text", "write_bytes", "mkdir", "unlink", "rmdir", "rename", "replace", "touch", "system", "popen", "run", "Popen", "urlopen"}, "no writer/network/subprocess calls")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            need(node.func.id not in {"exec", "eval", "compile", "__import__", "open"}, "no dynamic execution or generic open")


def main():
    need(sys.argv[1:] in ([], ["--preseal"]), "only default closure or explicit preseal")
    preseal = sys.argv[1:] == ["--preseal"]
    safe_current_helper()
    manifest = load(A / "OWNED_MANIFEST.json")
    same(manifest["exact_root_terminal_controls"], TERMINALS)
    files, dirs = namespace(A)
    expected = [e["path"] for e in manifest["files"]]
    need(len(expected) == len(set(expected)), "unique manifest payloads")
    need(sorted(f for f in files if f not in TERMINALS) == sorted(expected), "strict complete owned file namespace; exact root controls only")
    same(dirs, manifest["directories"])
    for entry in manifest["files"]:
        relsafe(entry["path"])
        pin(A / entry["path"], entry)
    if not preseal:
        need(all(name in files for name in TERMINALS), "all3 exact terminal files present")
        final = load(A / "FINAL_SEAL.json")
        need(final["MANIFEST_SHA256"] == sha(A / "OWNED_MANIFEST.json"), "final manifest binding")
        need(final["CLOSURE_SHA256"] == sha(A / "CLOSURE.json"), "final actual closure binding")
        same(final["exact_root_terminal_controls"], TERMINALS)
        need(final["owned_payload_count"] == len(expected) and final["complete_actual_files"] == len(files) and final["complete_directories"] == len(dirs), "final complete namespace counts")
    early()
    source()
    archives()
    primary()
    verdict = load(A / "VERDICT.json")
    need(verdict["root137_comparison_gate"] == "CLOSED" and verdict["scientific_findings_sent_to_root"] is False, "closed comparison gate")
    need(verdict["publication_authority"] is False and verdict["production_authority"] is False and verdict["canonical_url"] is None and verdict["AA"] is None and verdict["follow_up"] is None, "literal null/false authority/followup")
    need(verdict["source_scientific_programmes_executed"] == [] and verdict["current_peer_or_root_scientific_findings_read"] is False, "no native execution or peer findings")
    print(json.dumps({"status": "PURE_CUSTODY_PASS_NOT_SCIENTIFIC_PROOF", "mode": "preseal" if preseal else "sealed", "checks": CHECKS, "owned_payloads": len(expected), "source_files": 101, "source_directories": 18, "ZIP_regular_occurrences": 35, "raw_handoff_files": 56, "PDF_pages": 6, "TeX_lines": 198, "network_requests": 0, "subprocesses": 0, "writes": 0, "scientific_execution": False, "root137_gate": "CLOSED"}, sort_keys=True))


if __name__ == "__main__":
    main()
