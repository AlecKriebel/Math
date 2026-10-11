"""Read-only integrity/replay comparison for this independent method review.

This certifies bytes and enumeration, not any analytical capacity conclusion.
Run with the existing runtime; no candidate program is imported or re-executed.
"""
from pathlib import Path
from hashlib import sha256
import json

here = Path(__file__).resolve().parent
packet = here.parent / "snapshot/unsolved_math_prioritization/attempts/2303016"
edges = []
for manifest_name in ["TURN_1_MANIFEST.json", "FINAL_FROZEN_MANIFEST.json",
                      "PUBLICATION_MANIFEST.json", "final_review/REVIEW_MANIFEST.json"]:
    manifest_path = packet / manifest_name
    manifest = json.loads(manifest_path.read_text())
    entries = manifest["files"]
    assert len({entry["path"] for entry in entries}) == len(entries)
    for entry in entries:
        relative = Path(entry["path"])
        assert not relative.is_absolute() and ".." not in relative.parts
        content = (manifest_path.parent / relative).read_bytes()
        assert len(content) == entry["bytes"]
        assert sha256(content).hexdigest() == entry["sha256"]
        edges.append({"manifest": manifest_name, "path": entry["path"]})
inventory = {path.relative_to(packet).as_posix(): path for path in packet.rglob("*") if path.is_file()}
publication = json.loads((packet / "PUBLICATION_MANIFEST.json").read_text())
expected = {entry["path"] for entry in publication["files"]} | {"PUBLICATION_MANIFEST.json"}
assert set(inventory) == expected
source_seal = json.loads((here / "BASELINE_SEAL.json").read_text())
for entry in source_seal["files"]:
    assert sha256((here / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
for entry in source_seal["primary_pdfs"]:
    assert sha256((here / entry["private_path"]).read_bytes()).hexdigest() == entry["sha256"]
replays = []
for name, expected_path in [("author", packet / "TURN_1_CHECKS.json"),
                            ("historical", packet / "final_review/CHECKS.json")]:
    output = here / "private_replays" / (name + ".stdout")
    error = here / "private_replays" / (name + ".stderr")
    exit_file = here / "private_replays" / (name + ".exit")
    assert exit_file.read_text().strip() == "0"
    assert error.read_bytes() == b""
    assert output.read_bytes() == expected_path.read_bytes()
    replays.append({"name": name, "exit": 0, "byte_exact": True,
                    "stdout_sha256": sha256(output.read_bytes()).hexdigest(),
                    "stderr_bytes": 0, "parsed_output": json.loads(output.read_text())})
print(json.dumps({"status": "PASS", "target_files": len(inventory),
                  "manifest_edges": len(edges), "baseline_hashes_match": True,
                  "primary_pdf_hashes_match": True, "replays": replays,
                  "scope": "Closed target inventory, all four manifest edges, exact replay output, and pre-candidate baseline hashes; no analytical theorem certified by finite computation."},
                 indent=2, sort_keys=True))
