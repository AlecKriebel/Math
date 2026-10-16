import hashlib
import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
ORIGINAL = BASE.parent / "original_source_authentication_20261004"
TREE = json.loads((ORIGINAL / "TARGET_ATTEMPT_TREE.json").read_text())
wanted = {"CANDIDATE.md", "source_record.json", "SOURCES.md"}
out = []
for item in TREE:
    if pathlib.Path(item["path"]).name not in wanted or "/review/" in item["path"]:
        continue
    path = ORIGINAL / "original" / item["path"]
    body = path.read_bytes()
    sha1 = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
    out.append({"original_head": "5cc1602c05d79502defb07cec7027963149494d2", "source_path": str(path),
                "repo_path": item["path"], "bytes": len(body), "expected_bytes": item["size"],
                "git_blob_sha1": sha1, "expected_git_blob_sha1": item["sha"],
                "sha256": hashlib.sha256(body).hexdigest(), "matches": len(body) == item["size"] and sha1 == item["sha"]})
assert len(out) == len(wanted) and all(x["matches"] for x in out)
(BASE / "INPUT_AUTHENTICATION.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
