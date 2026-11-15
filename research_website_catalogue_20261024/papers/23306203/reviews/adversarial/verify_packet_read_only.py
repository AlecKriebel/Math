#!/usr/bin/env python3
"""Pure offline custody closure. No scientific imports, replay, network or writes."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile
import zlib

E = Path(__file__).resolve().parent
S = E.parent.parent / "sources"
CHECKS = 0


def require(value, label):
    global CHECKS
    CHECKS += 1
    if not value:
        raise ValueError(label)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def whole_file(o, path=None):
    p = Path(path if path is not None else o["path"])
    require(p.is_file() and not p.is_symlink(), "regular file " + str(p))
    b = p.read_bytes()
    require(len(b) == o["bytes"], "whole size " + str(p))
    require(sha(b) == o["SHA256"], "whole SHA256 " + str(p))
    return b


def load(p):
    return json.loads(p.read_text())


def main():
    preseal = sys.argv[1:] == ["--preseal"]
    require(not sys.argv[1:] or preseal, "only optional --preseal is accepted")
    original = load(E / "INPUT_MANIFEST.json")["whole_source_directory"]
    for o in original:
        whole_file(o)
    require(len(original) == 66, "all 66 original source files")
    require({str(p) for p in S.rglob("*") if p.is_file()} ==
            {o["path"] for o in original}, "exact source file set")

    ready = load(S / "SOURCE_READY.json")
    require(sha((S / "SOURCE_READY.json").read_bytes()) ==
            "7f0b73ce3dc22426cd7f5db2037e2932594454c21c58dca9d9bfab06a7bcc60e",
            "original SOURCE_READY pin")
    require(sha((S / "SOURCE_READY_SEAL.json").read_bytes()) ==
            "0d679ce38d996c2e0aa90cb9bce1c1fde84b0d2a625054af3c9e2491f2576720",
            "original source seal pin")
    for fn, pin in [("INITIAL_SEAL.json", "4195c9d00e917e7f1d13f408ca3d0a0c8023ddf228b3b6a593f5bdd4d868643c"),
                    ("OWN_PROOF_RESULTS_SEAL.json", "5c875d010efed5fb49c3e14b5e897e0ba5d88aae261e5a90cfdd885fd442cfd6")]:
        require(sha((E / fn).read_bytes()) == pin, "early independence seal " + fn)
        for o in load(E / fn).get("files", []):
            whole_file(o)

    custody = load(E / "SOURCE_CUSTODY.json")
    require(custody["native_whole_source_ready_object"] == ready,
            "whole original ready object retained")
    for o in custody["literal_native_copies"]:
        b = whole_file(o, E / o["copy_path"])
        require(b == Path(o["original_path"]).read_bytes(), "literal native copy")
    require(len(custody["literal_native_copies"]) == 21, "whole native copy set")

    objects = {}
    for o in ready["whole_native_API_objects"]:
        objects[o["role"]] = json.loads(whole_file(o))
    require(objects["record"] == objects["latest"], "whole latest record agreement")
    require(objects["record"]["swh"] == {} and
            objects["latest"]["swh"] == {}, "empty SWH objects")
    require(objects["versions-page001"]["hits"]["hits"][0]["swh"] is None,
            "version SWH null remains distinct")
    f = objects["files"]
    require(type(f["entries"]) is list and f["order"] == [] and
            f["default_preview"] is None, "files list empty order null preview")
    require([x["key"] for x in objects["record"]["files"]] ==
            ["focal_product_support.zip", "focal_product_period_criterion.pdf"],
            "ZIP then PDF native order")
    require(ready["source_programmes_executed"] == [] and
            ready["source_scientific_proofs_code_results_triage_reviews_or_opinions_read"] is False,
            "historical acquisition flags not rewritten")
    transports = load(S / "ALL_TRANSPORT_RECEIPTS.json")
    require(len(transports) == 7 and
            [x["HTTP_status"] for x in transports] == [200, 301, 200, 200, 200, 200, 200],
            "all actual native transports")
    require(transports == custody["seven_actual_transport_receipts_whole"],
            "whole transports not flattened")
    for t in transports:
        whole_file({"path": t["body_path"], "bytes": t["bytes"], "SHA256": t["SHA256"]})
        require(type(t["response_headers_in_received_order"]) is list,
                "ordered opaque native header pairs")
    require(ready["failed_transports_preserved_whole"] == [], "native empty failure history")

    archive = load(S / "ARCHIVE_CUSTODY.json")
    require(archive == custody["whole_original_archive_custody_object"],
            "whole archive custody object")
    require(archive["whole_regular_payload_occurrences"] == 13 and
            archive["recursive_archive_container_count"] == 1 and
            archive["nested_archive_count"] == 0, "entire archive scope")
    checked_members = 0
    for c in archive["containers"]:
        whole_file({"path": c["input_path"], "bytes": c["input_bytes"],
                    "SHA256": c["input_SHA256"]})
        with zipfile.ZipFile(c["input_path"]) as z:
            infos = z.infolist()
            require(len(infos) == len(c["members"]), "whole ZIP member list")
            for i, m in zip(infos, c["members"]):
                b = z.read(i)
                require(i.filename == m["original_member_name"], "member name order")
                require(len(b) == i.file_size == m["bytes"], "member size")
                require(sha(b) == m["SHA256"], "member whole SHA256")
                require(i.CRC == zlib.crc32(b) & 0xffffffff == int(m["CRC32"], 16),
                        "member full-read CRC32")
                require((i.compress_size, i.compress_type, i.external_attr,
                         i.create_system, i.flag_bits, list(i.date_time)) ==
                        (m["compressed_bytes"], m["compression_method"],
                         m["native_external_attr"], m["native_create_system"],
                         m["native_flags"], m["native_date_time"]), "native ZIP metadata")
                require(b == Path(m["extracted_path"]).read_bytes(), "whole extracted bytes")
                require(b == (E / "native-isolated" / i.filename).read_bytes(),
                        "isolated native bytes unchanged")
                checked_members += 1
    require(checked_members == 13, "all original payloads")

    replay = load(E / "NATIVE_REPLAY.json")
    expected = Path(replay["expected_original_path"]).read_bytes()
    require(len(expected) == 932 and sha(expected) == replay["EXPECTED_SHA256"],
            "entire native expected bytes")
    require(json.loads(expected) == replay["whole_expected_object"], "entire native expected object")
    require([r["mode"] for r in replay["runs"]] == ["normal", "optimized"],
            "exactly two saved selected runs")
    for r in replay["runs"]:
        out = (E / ("NATIVE_" + r["mode"] + ".stdout")).read_bytes()
        err = (E / ("NATIVE_" + r["mode"] + ".stderr")).read_bytes()
        require(r["exit_code"] == 0 and err == b"", "saved native successful execution")
        require(out == expected and json.loads(out) == replay["whole_expected_object"],
                "whole native comparison, not counts only")
        require(sha(out) == r["stdout_SHA256"] and sha(err) == r["stderr_SHA256"],
                "saved stream hashes")
    require(replay["isolated_and_original_payloads_unchanged"] is True,
            "saved native copy custody")
    for o in load(E / "OWN_RENDER_RECEIPT.json")["rasters"]:
        b = whole_file(o, E / o["path"])
        require(b == (S / "rasters" / Path(o["path"]).name).read_bytes(),
                "own fresh raster matches initially read fresh raster")

    for receipt in sorted((E / "cache/primary").glob("*.receipt.json")):
        r = load(receipt)
        for key in ("body", "headers"):
            if r[key] is not None:
                whole_file(r[key], E / r[key]["path"])
        if r["body"] is None:
            require(r["curl_exit_code"] != 0, "failed primary fetch not invented success")

    owned_count = None
    if not preseal:
        manifest = load(E / "MANIFEST.json")
        seal = load(E / "SEAL.json")
        require(sha((E / "MANIFEST.json").read_bytes()) == seal["MANIFEST_SHA256"],
                "final manifest seal")
        entries = manifest["owned_files"]
        for o in entries:
            whole_file(o, E / o["path"])
        require({str(p.relative_to(E)) for p in E.rglob("*") if p.is_file()} ==
                {o["path"] for o in entries} | {"MANIFEST.json", "SEAL.json"},
                "exact owned file set")
        owned_count = len(entries)
        require(sha((E / "VERDICT.json").read_bytes()) == seal["VERDICT_SHA256"],
                "literal verdict seal")
        require(sha((E / "REPORT.md").read_bytes()) == seal["REPORT_SHA256"],
                "whole report seal")
    print(json.dumps({"status": "PASS_READ_ONLY_CUSTODY", "mode": "preseal" if preseal else "final",
                      "checks": CHECKS, "source_inputs": len(original),
                      "original_ZIP_payloads": checked_members, "owned_payloads": owned_count,
                      "scientific_code_imported_or_executed": False,
                      "network_or_file_writes": False}, indent=2))


if __name__ == "__main__":
    main()
