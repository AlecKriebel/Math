"""Audit provenance runner; reads only explicitly released inputs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent / "snapshot/unsolved_math_prioritization/attempts/30005303"
OUT = HERE / "reproductions"
OUT.mkdir(exist_ok=True)


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def binding(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": digest(data),
            "mode_at_read": oct(path.stat().st_mode & 0o777)}


start = utc()
final = json.loads((PACKET / "FINAL_PACKET_MANIFEST.json").read_bytes())
names = [entry["path"] for entry in final["files"]] + ["FINAL_PACKET_MANIFEST.json"]
assert len(names) == len(set(names)) == 19
assert not any(name.startswith("review/") for name in names)
inputs = [binding(PACKET / name) for name in sorted(names)]
observed = {Path(item["path"]).relative_to(PACKET).as_posix(): item for item in inputs}
for entry in final["files"]:
    found = observed[entry["path"]]
    assert found["sha256"] == entry["sha256"] and found["bytes"] == entry["bytes"]
first = json.loads((PACKET / "TURN_1_MANIFEST.json").read_bytes())
for entry in first["files"]:
    found = observed[entry["path"]]
    assert found["sha256"] == entry["sha256"] and found["bytes"] == entry["bytes"]
inputs.append(binding(PACKET / "PUBLICATION_MANIFEST.json"))
publication = json.loads((PACKET / "PUBLICATION_MANIFEST.json").read_bytes())
for entry in publication["files"]:
    if entry["path"] in observed:
        found = observed[entry["path"]]
        assert found["sha256"] == entry["sha256"] and found["bytes"] == entry["bytes"]
own_control = binding(HERE / "independent_controls.py")
source = binding(HERE / "tmp/pdfs/lauritzen_owr_2022_55.pdf")
read_receipt = {"recorded_utc": utc(), "authorized_packet_file_count": 19,
                "publication_manifest_read_for_binding_only": True,
                "candidate_inputs": inputs, "independent_source_pdf": source,
                "excluded_contents": ["review/ (all eight inherited files)",
                                      "PUBLICATION_SUMMARY.md", "other families",
                                      "root current reasoning", "priority search results"]}
(HERE / "INPUT_BINDINGS.json").write_text(json.dumps(read_receipt, indent=2, sort_keys=True) + "\n")

runs = []
tasks = [
    ("author_c4", PACKET / "checks/verify_turn1.py", PACKET / "checks/turn1_c4_output.json"),
    ("author_c6", PACKET / "checks/verify_c6.py", PACKET / "checks/turn1_c6_output.json"),
    ("author_closure", PACKET / "checks/verify_turn2.py", PACKET / "checks/turn2_output.json"),
    ("independent_controls", HERE / "independent_controls.py", HERE / "INDEPENDENT_CONTROLS_RESULT.json"),
]
for label, code, expected in tasks:
    argv = [sys.executable, str(code)]
    before = binding(code)
    started = utc()
    completed = subprocess.run(argv, cwd=HERE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    ended = utc()
    stdout_path, stderr_path = OUT / (label + ".stdout"), OUT / (label + ".stderr")
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    run = {"label": label, "argv": argv, "cwd": str(HERE),
           "start_utc": started, "end_utc": ended,
           "exit_code": completed.returncode, "code": before,
           "code_bytes_unchanged": before["sha256"] == binding(code)["sha256"],
           "stdout": binding(stdout_path), "stderr": binding(stderr_path),
           "expected_output": binding(expected),
           "stdout_matches_stored_bytes": completed.stdout == expected.read_bytes()}
    runs.append(run)
    assert completed.returncode == 0 and not completed.stderr
    assert run["code_bytes_unchanged"] and run["stdout_matches_stored_bytes"]
    print(label + ": exit 0, stderr empty, exact stored-output match", flush=True)

assert all(binding(Path(item["path"]))["sha256"] == item["sha256"] for item in inputs)
receipt = {"start_utc": start, "end_utc": utc(), "python_version": sys.version,
           "python_executable": sys.executable, "assertions_enabled": __debug__,
           "runner": binding(Path(__file__).resolve()), "independent_code_prebound": own_control,
           "author_assertions": 332 + 13520 + 550337,
           "candidate_inputs_unchanged": True, "runs": runs, "status": "PASS"}
(HERE / "REPRODUCTION_MANIFEST.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
