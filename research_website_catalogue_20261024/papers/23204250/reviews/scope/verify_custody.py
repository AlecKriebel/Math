#!/usr/bin/env python3
"""Standalone default offline read-only custody; never science/native replay."""
from pathlib import Path, PurePosixPath
import ast
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


def need(ok, reason):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise RuntimeError(reason)


def load(p):
    return json.loads(p.read_bytes())


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pin(p, expected):
    need(stat.S_ISREG(p.lstat().st_mode), "pinned regular file")
    b = p.read_bytes()
    need(len(b) == expected["bytes"], "whole byte count")
    need(hashlib.sha256(b).hexdigest() == expected["SHA256"], "whole SHA256")


def relative(name):
    need(type(name) is str and bool(name), "relative string")
    q = PurePosixPath(name)
    need(not q.is_absolute() and ".." not in q.parts and "\\" not in name and "\0" not in name and ":" not in name, "safe relative path")


def namespace(root):
    files, dirs = [], []
    for p in sorted(root.rglob("*")):
        mode = p.lstat().st_mode
        name = p.relative_to(root).as_posix()
        relative(name)
        need(not stat.S_ISLNK(mode), "no symlinks")
        if stat.S_ISDIR(mode):
            dirs.append(name)
        else:
            need(stat.S_ISREG(mode), "no special files")
            files.append(name)
    need(len(files) == len(set(n.casefold() for n in files)), "no file case collisions")
    need(len(dirs) == len(set(n.casefold() for n in dirs)), "no directory case collisions")
    return files, dirs


def same(x, y):
    need(type(x) is type(y), "literal JSON type")
    if type(x) is dict:
        need(list(x) == list(y), "whole original object key order")
        for key in x:
            same(x[key], y[key])
    elif type(x) is list:
        need(len(x) == len(y), "whole original array length")
        for a, b in zip(x, y):
            same(a, b)
    else:
        need(x == y, "whole literal value")


class ObjectPairs(list):
    pass


def typed(value):
    if isinstance(value, ObjectPairs):
        return {"type": "object", "ordered_pairs": [[key, typed(item)] for key, item in value]}
    if type(value) is list:
        return {"type": "array", "items": [typed(item) for item in value]}
    labels = {type(None): "null", bool: "boolean", int: "integer", float: "number", str: "string"}
    return {"type": labels[type(value)], "literal_value": value}


def early_seals():
    for name, sha in [("INITIAL_SEAL.json", "54aab1397c627cd08661c88b2fb2102910c15f325628ebb360455f15cd31d329"), ("OWN_PROOF_CONTROL_SEAL.json", "ba94acb1f8d28a51a73f6d4799f3bb5bfcbd8d93269aeb4d4aab34703610f391")]:
        need(digest(A / name) == sha, "immutable early seal")
        seal = load(A / name)
        p = Path(seal["manifest"]["path"])
        need(p.parent == A, "early manifest owned boundary")
        pin(p, seal["manifest"])
        for entry in load(p)["files"]:
            q = Path(entry["path"])
            need(q.is_relative_to(A), "early payload owned boundary")
            pin(q, entry)


def source():
    need(digest(S / "SOURCE_READY.json") == "13d913127abab98d78c3758516884b09f7e4849b5e6c07a3e0fd44c502147ec9", "original READY")
    need(digest(S / "SOURCE_READY_SEAL.json") == "94bd3bbf71c9fd618b6bf12616120aace2a6d3fe04707d6f73bb1bd787dd8ecf", "original source seal")
    initial = load(A / "SOURCE_INPUT_MANIFEST.json")
    binding = load(A / "SOURCE_CUSTODY_BINDINGS.json")
    entries = initial["complete_source_files"]
    need(len(entries) == len(binding["whole104_original_file_bindings"]) == 104, "all104 source files")
    fs, ds = namespace(S)
    expected = [Path(e["path"]).relative_to(S).as_posix() for e in entries]
    same(fs, sorted(expected))
    same(ds, initial["exact_complete_source_directories"])
    need(len(ds) == 13, "all13 source directories")
    copied = A / "raw/source-originals"
    cfs, cds = namespace(copied)
    same(cfs, fs)
    same(cds, ds)
    for entry, item in zip(entries, binding["whole104_original_file_bindings"]):
        p = Path(entry["path"])
        rel = p.relative_to(S).as_posix()
        q = copied / rel
        need(item["relative_path"] == rel and Path(item["copy"]["path"]) == q, "whole source copy path/order")
        same(item["original"], entry)
        pin(p, entry)
        pin(q, item["copy"])
        need(p.read_bytes() == q.read_bytes(), "whole original/copy bytes equal")
    objects = load(A / "PROVIDED_SOURCE_OBJECTS.json")["whole_original_JSON_objects_in_source_path_order"]
    tapes = load(A / "ORIGINAL_JSON_TYPE_TAPES.json")["objects"]
    json_entries = [e for e in entries if Path(e["path"]).suffix == ".json"]
    need(len(json_entries) == len(objects) == len(tapes) == 40, "all40 provided JSON objects")
    for entry, obj, tape in zip(json_entries, objects, tapes):
        p = Path(entry["path"])
        rel = p.relative_to(S).as_posix()
        need(obj["relative_path"] == tape["relative_path"] == rel, "provided object order")
        same(load(p), obj["whole_original_object"])
        same(typed(json.loads(p.read_bytes(), object_pairs_hook=ObjectPairs)), tape["whole_typed_ordered_JSON"])
    r = load(S / "SOURCE_READY.json")
    need(r["version_field_present"] is False and r["version"] is None, "native absent version, no default")
    need(r["printed_title_date_version_inspected"] is False and r["printed_date"] is None and r["printed_version"] is None, "historical source UNREAD flags")
    same(r["source_programmes_executed"], [])
    originals = load(A / "NATIVE_API_ORIGINALS.json")["all_whole_original_API_objects_in_actual_acquisition_order"]
    need(len(originals) == len(r["whole_native_API_objects"]) == 4, "four actual whole native API objects")
    for descriptor, obj in zip(r["whole_native_API_objects"], originals):
        p = Path(descriptor["path"])
        need(p.is_relative_to(S), "native body source boundary")
        pin(p, descriptor)
        same(descriptor, obj["whole_original_body_binding"])
        same(load(p), obj["whole_original_object"])
        same(typed(json.loads(p.read_bytes(), object_pairs_hook=ObjectPairs)), obj["whole_original_typed_order"])
        if descriptor["role"] == "record":
            need("version" not in load(p)["metadata"], "literal native edition field ABSENT")
    assets = r["all_native_assets_in_original_order"]
    need([x["original_api_file_object"]["key"] for x in assets] == ["paper.pdf", "tsp-verification.zip", "tsp-source.zip"], "original native asset order")
    for entry in assets:
        p = Path(entry["path"])
        need(p.is_relative_to(S), "asset boundary")
        pin(p, entry)
        need(p.read_bytes() == Path(entry["transport_body_path"]).read_bytes(), "whole native body equality")
        need("md5:"+hashlib.md5(p.read_bytes()).hexdigest() == entry["original_api_file_object"]["checksum"], "native checksum")
    need(len(Path(r["controlling_TeX"]["extracted_path"]).read_bytes().splitlines()) == 189, "opaque189 TeX lines")
    need(r["all_native_reader_total_pages"] == 6 and r["embedded_PDFs"] == [] and r["additional_controlling_TeX_sources"] == [], "whole original manuscript custody")


def archive_custody():
    a = load(S / "ARCHIVE_CUSTODY.json")
    need(len(a["containers"]) == 2 and a["whole_regular_payload_occurrences"] == 35 and a["nested_archive_count"] == 0, "two native ZIPs35 regular occurrences")
    all_members = []
    for c in a["containers"]:
        p = Path(c["input_path"])
        need(p.is_relative_to(S) and digest(p) == c["input_SHA256"], "whole original ZIP")
        with zipfile.ZipFile(p, "r") as z:
            infos = z.infolist()
            need(z.comment.hex() == c["original_archive_comment_hex"], "original whole ZIP comment")
            need(len(infos) == len(c["members"]) == len(c["whole_original_central_directory"]), "all native central entries")
            need(len(infos) == len({i.filename.casefold() for i in infos}), "no ZIP duplicate/case collisions")
            for ordinal, (i, e, original) in enumerate(zip(infos, c["members"], c["whole_original_central_directory"])):
                relative(i.filename)
                need(not i.is_dir() and not i.flag_bits & 1 and stat.S_IFMT(i.external_attr >> 16) in (0,stat.S_IFREG), "regular safe unencrypted payload")
                central = {"ordinal_zero_based": ordinal, "filename": i.filename, "original_filename": i.orig_filename, "is_directory": i.is_dir(), "bytes": i.file_size, "compressed_bytes": i.compress_size, "CRC32": format(i.CRC,"08x"), "flags": i.flag_bits, "compression": i.compress_type, "native_date_time": list(i.date_time), "external_attr": i.external_attr, "internal_attr": i.internal_attr, "create_system": i.create_system, "create_version": i.create_version, "extract_version": i.extract_version, "header_offset": i.header_offset, "extra_hex": i.extra.hex(), "comment_hex": i.comment.hex()}
                same(central, original)
                body = z.read(i)
                q = Path(e["extracted_path"])
                need(q == Path(c["extraction_root"])/i.filename and q.is_relative_to(S), "extracted path boundary")
                need(e["ordinal_zero_based"] == ordinal and e["original_member_name"] == i.filename, "original regular list order")
                need(body == q.read_bytes() and len(body) == e["bytes"] == i.file_size, "whole ZIP source equality and size")
                need(hashlib.sha256(body).hexdigest() == e["SHA256"], "ZIP SHA256")
                need(format(zlib.crc32(body)&0xffffffff,"08x") == e["CRC32"] == format(i.CRC,"08x"), "ZIP native CRC")
                need(i.compress_size == e["compressed_bytes"] and i.compress_type == e["compression_method"] and i.external_attr == e["native_external_attr"] and i.create_system == e["native_create_system"] and i.flag_bits == e["native_flags"], "all native regular flags/compression")
                same(list(i.date_time), e["native_date_time"])
                all_members.append(e)
    same(all_members, a["regular_payload_occurrences"])


def collect_pins(value, out):
    if type(value) is dict:
        if {"path","bytes","SHA256"} <= value.keys():
            out[value["path"]] = value
        else:
            for child in value.values():
                collect_pins(child, out)
    elif type(value) is list:
        for child in value:
            collect_pins(child, out)


def primary_custody():
    for number, sha, records_count in [("01","e653b03acde4be6b384ae067753bb657d2f47f8be14178d079c965efcc656863",12), ("02","f37a95b6f5ec8730c982616d2c3849b5fdcd0dd41abb8c6f50c360cec893d08a",20)]:
        index = A / "primary" / ("RAW_PRIMARY_HANDOFF_"+number+".owner-original.json")
        need(digest(index) == sha, "whole raw-only index")
        raw = load(index)
        need(raw["raw_only_no_interpretations_notes_findings_or_control_results"] is True and len(raw["records"]) == records_count, "raw-only finite records")
        expected = {}
        collect_pins(raw["records"],expected)
        if number == "01":
            collect_pins(raw["literal_original_native_hash_inventory"]["binding"],expected)
        binding = load(A / "primary" / ("SHARED_RAW_BINDINGS_"+number+".json"))
        need(binding["own_primary_GETs"] == 0 and type(binding["own_primary_GETs"]) is int, "zero scope GETs")
        items = binding["raw_only_records_and_inventory_binding_copied"] if number == "01" else binding["whole_listed_raw_files"]
        need(len(items) == len(expected), "all and only raw records/inventory pins, no peer payload")
        seen = set()
        for item in items:
            original = item["owner_or_native_original"] if number == "01" else item["owner_original"]
            same(original, expected[original["path"]])
            seen.add(original["path"])
            p = Path(item["scope_copy"]["path"])
            need(p.is_relative_to(A / "primary"), "raw scope-copy boundary")
            relative(p.relative_to(A).as_posix())
            pin(p, original)
            pin(p, item["scope_copy"])
        need(seen == set(expected), "complete unique raw pin namespace")
    failure = load(A / "FAILURE_HISTORY.json")
    raw2 = load(A / "primary/RAW_PRIMARY_HANDOFF_02.owner-original.json")
    same(failure["whole_original_raw_handoff_access_limits"],raw2["access_limits"])
    need(load(A / "METADATA_LOOKUP_FAILURE.json")["exit_code"] == 1, "actual metadata lookup failure retained")


def safe_current_source():
    tree = ast.parse(Path(__file__).read_text())
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            names = [x.name.split(".")[0] for x in node.names] if isinstance(node,ast.Import) else [node.module]
            need(all(n in {"pathlib","ast","hashlib","json","stat","sys","zipfile","zlib"} for n in names), "only declared standard library imports")
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
            need(node.func.attr not in {"write_text","write_bytes","mkdir","unlink","rmdir","rename","replace","touch","system","popen","run","Popen","urlopen"}, "no writer/network/subprocess calls")
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
            need(node.func.id not in {"exec","eval","compile","__import__","open"}, "no dynamic execution/generic open")


def main():
    need(sys.argv[1:] in ([],["--preseal"]), "only sealed default or explicit preseal")
    preseal = sys.argv[1:] == ["--preseal"]
    safe_current_source()
    m = load(A / "OWNED_MANIFEST.json")
    same(m["exact_root_terminal_controls"],TERMINALS)
    fs,ds = namespace(A)
    expected = [e["path"] for e in m["files"]]
    need(len(expected) == len(set(expected)), "unique owned manifest")
    same(sorted(n for n in fs if n not in TERMINALS),sorted(expected))
    same(ds,m["directories"])
    for e in m["files"]:
        relative(e["path"])
        pin(A/e["path"],e)
    if not preseal:
        need(all(n in fs for n in TERMINALS), "all3 exact root terminals")
        final = load(A / "FINAL_SEAL.json")
        need(final["MANIFEST_SHA256"] == digest(A/"OWNED_MANIFEST.json") and final["CLOSURE_SHA256"] == digest(A/"CLOSURE.json"), "final whole terminal bindings")
        same(final["exact_root_terminal_controls"],TERMINALS)
        need(final["owned_payload_count"] == len(expected) and final["complete_actual_files"] == len(fs) and final["complete_directories"] == len(ds), "final exact namespace counts")
    early_seals()
    source()
    archive_custody()
    primary_custody()
    v = load(A/"VERDICT.json")
    need(v["root139_comparison_gate"] == "CLOSED" and v["scientific_findings_sent_to_root"] is False, "closed root139 gate")
    need(v["publication_authority"] is False and v["production_authority"] is False and v["canonical_url"] is None and v["AA"] is None and v["follow_up"] is None, "literal authority/followup null/false")
    same(v["source_or_supplied_scientific_programmes_executed"],[])
    need(v["current_peer_root_opinions_or_native_replay_results_read"] is False,"no peer/current findings")
    print(json.dumps({"status":"PURE_CUSTODY_PASS_NOT_SCIENTIFIC_PROOF","mode":"preseal" if preseal else "sealed","checks":CHECKS,"owned_payloads":len(expected),"source_files":104,"source_directories":13,"native_assets":3,"ZIP_containers":2,"ZIP_regular_occurrences":35,"PDF_pages":6,"TeX_lines":189,"raw_handoff_records":32,"network_requests":0,"subprocesses":0,"writes":0,"scientific_execution":False,"root139_gate":"CLOSED"},sort_keys=True))


if __name__ == "__main__":
    main()
