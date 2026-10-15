#!/usr/bin/env python3
"""Close and measure self-excluded administrative records after native logging ends."""
import datetime
import hashlib
import json
import pathlib
import stat
import sys

base = pathlib.Path(__file__).resolve().parent
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest = json.loads((base/"FINAL_SEAL_MANIFEST.json").read_text())
verification = json.loads((base/"FINAL_SEAL_VERIFICATION.json").read_text())
assert verification["status"] == "PASS_INDEPENDENT_COMPLETE_NAMESPACE_AND_INPUT_VERIFICATION"
admin = set(manifest["administrative_non_self_hashing_exclusions"])
closure = "FINAL_CLOSURE_RECORD.json"
assert closure in admin and not (base/closure).exists()
measured = []
for rel in sorted(admin-{closure}):
    path = base/rel
    assert path.is_file() and not path.is_symlink()
    path.chmod(0o444)
    data = path.read_bytes()
    measured.append({"relative_path":rel,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
                     "mode":format(stat.S_IMODE(path.stat().st_mode),"04o")})
for label in ("final_seal", "final_verify"):
    r = json.loads((base/"private"/(label+".command.json")).read_text())
    assert r["exit_code"] == 0
    for stream in ("stdout", "stderr"):
        path = pathlib.Path(r[stream]["path"])
        data = path.read_bytes()
        assert len(data) == r[stream]["bytes"] and hashlib.sha256(data).hexdigest() == r[stream]["sha256"]
    assert r["input_pins_before"] == r["input_pins_after"]
for entry in manifest["files"]:
    path = base/entry["relative_path"]
    data = path.read_bytes()
    assert len(data) == entry["bytes"] and hashlib.sha256(data).hexdigest() == entry["sha256"]
    assert stat.S_IMODE(path.stat().st_mode) == 0o444
current = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
assert current == {r["relative_path"] for r in manifest["files"]} | (admin-{closure})
exe = pathlib.Path(sys.executable).resolve()
exe_data = exe.read_bytes()
result = {"start_utc":started,"closed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "status":"PASS_FINAL_READONLY_FILE_CLOSURE", "completion_percent":100,
          "manifested_files_reverified":len(manifest["files"]),"administrative_records_measured":measured,
          "final_file_count_including_this_record":len(current)+1,
          "closure_process":{"argv":sys.orig_argv,"cwd":str(pathlib.Path.cwd()),
                             "python_executable":{"path":str(exe),"bytes":len(exe_data),"sha256":hashlib.sha256(exe_data).hexdigest()}},
          "self_pin_rule":"This final record does not contain its own hash. Its actual final bytes, hash and 0444 mode must be measured externally and reported to the parent.",
          "scope":"All review files and administrative records are now measured 0444; source-only gate and all 31 named originals passed independent unchanged checks. Review complete, no blocking finding. No publication/merge/external communication performed.",
          "permissions_limit":"Modes are reversible and directories remain at separately recorded modes; this is not immutable storage."}
target = base/closure
target.write_text(json.dumps(result,indent=2)+"\n")
target.chmod(0o444)
