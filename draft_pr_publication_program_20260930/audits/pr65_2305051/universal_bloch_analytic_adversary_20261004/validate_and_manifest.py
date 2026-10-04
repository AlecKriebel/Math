import ast
import datetime as dt
import hashlib
import json
import pathlib

root = pathlib.Path(__file__).resolve().parent
for p in root.glob("*.py"):
    ast.parse(p.read_text(), filename=str(p))
for p in root.glob("*.json"):
    json.loads(p.read_text())
for line in (root / "ACTUAL_COMMANDS.jsonl").read_text().splitlines():
    item = json.loads(line)
    assert item["pid"] > 0 and item["exit_code"] == 0
    assert (root / item["stdout"]).is_file()
    assert (root / item["stderr"]).is_file()
assert (root / "AAN1999_primary.pdf").read_bytes().startswith(b"%PDF-")
assert all(x["matches"] for x in json.loads((root / "INPUT_AUTHENTICATION.json").read_text()))
verdict = json.loads((root / "verdict.json").read_text())
assert verdict["reviewed_head"] == "5cc1602c05d79502defb07cec7027963149494d2"
assert verdict["author_reviews_read"] is False
entries = []
for p in sorted(root.iterdir()):
    if not p.is_file() or p.name in {"ARTIFACT_MANIFEST.json", "ACTUAL_COMMANDS.jsonl"}:
        continue
    body = p.read_bytes()
    entries.append({"path": p.name, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
manifest = {"generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "reviewed_head": verdict["reviewed_head"], "audit_family": verdict["family"],
            "artifacts": entries,
            "execution_receipts": "ACTUAL_COMMANDS.jsonl and commands/ contain real command receipts and streams; intentionally excluded from content hashing because final command completion appends its receipt after manifest creation",
            "self_excluded": "ARTIFACT_MANIFEST.json"}
(root / "ARTIFACT_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"validation": "passed", "artifact_count": len(entries), "manifest": "ARTIFACT_MANIFEST.json"}))
