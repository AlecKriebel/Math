#!/usr/bin/env python3
"""Independent read/recomputation; does not import or trust the sealer's pin code."""
import datetime
import hashlib
import json
import os
import pathlib
import stat

base = pathlib.Path(__file__).resolve().parent
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest_path = base/"FINAL_SEAL_MANIFEST.json"
manifest_data = manifest_path.read_bytes()
manifest = json.loads(manifest_data)
checks = []
for item in manifest["files"]:
    relative = pathlib.PurePosixPath(item["relative_path"])
    assert not relative.is_absolute() and ".." not in relative.parts
    path = base.joinpath(*relative.parts)
    assert not path.is_symlink() and path.is_file()
    with path.open("rb") as source:
        digest = hashlib.sha256()
        size = 0
        for chunk in iter(lambda:source.read(65536), b""):
            size += len(chunk)
            digest.update(chunk)
    actual = {"relative_path":relative.as_posix(),"bytes":size,"sha256":digest.hexdigest(),
              "mode":format(stat.S_IMODE(os.stat(path).st_mode),"04o")}
    assert actual == item, (item,actual)
    assert actual["mode"] == "0444"
    checks.append(actual)
assert len(checks) == manifest["manifested_file_count"]
excluded = set(manifest["administrative_non_self_hashing_exclusions"])
observed = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
assert observed - excluded == {r["relative_path"] for r in checks}
dirs = {p.relative_to(base).as_posix():format(stat.S_IMODE(os.stat(p).st_mode),"04o")
        for p in base.rglob("*") if p.is_dir()}
assert dirs == {r["relative_path"]:r["mode"] for r in manifest["directories"]}
for path in base.rglob("*"):
    assert not path.is_symlink()
original_checks = []
imports = json.loads((base/"private/released_input_manifest.json").read_text())
assert len(imports["inputs"]) == 31
for row in imports["inputs"]:
    expected = row["original"]
    path = pathlib.Path(expected["path"])
    data = path.read_bytes()
    actual = {"path":str(path.resolve()),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
              "mode":format(stat.S_IMODE(os.stat(path).st_mode),"04o")}
    assert actual == expected
    copy = pathlib.Path(row["local_copy"]["path"]).read_bytes()
    assert copy == data
    original_checks.append(actual)
gate = json.loads((base/"SOURCE_ONLY_FREEZE_MANIFEST.json").read_text())
gate_checks = []
for item in gate["reports"]+gate["private_evidence"]:
    path = pathlib.Path(item["path"])
    data = path.read_bytes()
    actual = {"path":str(path.resolve()),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
              "mode":format(stat.S_IMODE(os.stat(path).st_mode),"04o")}
    assert actual == item
    gate_checks.append(actual)
assert any(x["bytes"] == 600619 and x["sha256"] == "56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65" for x in gate_checks)
assert (base/".gitignore").read_text().splitlines() == ["private/", ""] or (base/".gitignore").read_text().splitlines() == ["private/"]
for label, wanted in (("INDEPENDENT_CHECK_RESULTS.json","PASS_INDEPENDENT_EXACT_FINITE_CHECKS"),
                      ("NEGATIVE_CONTROL_RESULTS.json","PASS_NEGATIVE_CONTROLS"),
                      ("PROVENANCE_CHECK_RESULTS.json","PASS_CORRECTED_PROVENANCE")):
    assert json.loads((base/label).read_text())["status"] == wanted
rebuild = json.loads((base/"REBUILD_COMPARISON_RESULTS.json").read_text())
assert rebuild["text_equal"] and all(rebuild["page_pixels_equal"])
manifest_pin = {"path":str(manifest_path),"bytes":len(manifest_data),"sha256":hashlib.sha256(manifest_data).hexdigest(),
                "mode":format(stat.S_IMODE(os.stat(manifest_path).st_mode),"04o")}
assert manifest_pin["mode"] == "0444"
result = {"start_utc":started,"completed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "status":"PASS_INDEPENDENT_COMPLETE_NAMESPACE_AND_INPUT_VERIFICATION", "manifest":manifest_pin,
          "verified_file_count":len(checks),"verified_files":checks,"verified_directory_count":len(dirs),
          "verified_named_original_count":31,"verified_named_originals":original_checks,
          "verified_original_source_only_entries":gate_checks,
          "pending_administrative_closure":sorted(excluded),
          "completion_percent":100,
          "limits":"Independent recomputation of bytes/hashes/modes and result consistency, not an additional human or formal mathematical certification. Later administrative captures require separate closure measurement."}
out = base/"FINAL_SEAL_VERIFICATION.json"
assert not out.exists()
out.write_text(json.dumps(result,indent=2)+"\n")
out.chmod(0o444)
print(json.dumps({"status":result["status"],"verified_files":len(checks),"named_originals":31,
                  "verification_bytes":out.stat().st_size,"verification_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"mode":"0444"}))
