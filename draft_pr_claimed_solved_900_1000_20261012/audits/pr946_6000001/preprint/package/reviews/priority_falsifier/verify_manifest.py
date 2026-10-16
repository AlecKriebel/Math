"""Validate exact curated payload allowlist; private sources never enter it."""
from hashlib import sha256
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
EXPECTED = {
    "FULL_REPORT.md", "THEOREM_COMPARISON.md", "RESULT.json", "INPUT_AUTHENTICATION.json",
    "PRIMARY_AUTHENTICATION.json", "AJLS_PREVIEW_RECEIPT.json", "PUBLIC_RETRIEVAL.json",
    "SUPPLEMENTARY_RETRIEVAL.json", "QUERY_LEDGER.json", "SOURCE_READING_LOG.json",
    "RESEARCH_LOG.md", "check_inputs.py", "retrieve_public.py", "retrieve_extra.py",
    "verify_manifest.py",
}


def require(test, message):
    if not test:
        raise RuntimeError(message)


def main():
    require(sys.flags.optimize == 0, "Use normal Python")
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    rows = manifest["payloads"]
    require(len(rows) == len(EXPECTED) and {r["path"] for r in rows} == EXPECTED,
            "Exact allowlist mismatch")
    total = 0
    for item in rows:
        rel = Path(item["path"])
        require(not rel.is_absolute() and len(rel.parts) == 1, "Unsafe path")
        path = HERE / rel
        require(path.is_file() and not path.is_symlink(), "Nonregular payload")
        data = path.read_bytes()
        require(len(data) == item["bytes"] and sha256(data).hexdigest() == item["sha256"], str(rel))
        total += len(data)
    result = json.loads((HERE / "RESULT.json").read_text())
    require(result["pr"] == 946 and result["target_id"] == 6000001, "Scope")
    require(result["new_proof_responses"] == 0, "Budget")
    require(result["novelty_certified"] is False and result["acceptance_authorized"] is False,
            "Disposition")
    require(manifest["sealed_no_further_edits"] is True, "Seal marker")
    print(json.dumps({"payload_count": len(rows), "payload_bytes": total,
                      "exact_allowlist_size_sha256": "PASS", "private_raw_included": False,
                      "python_optimization_level": sys.flags.optimize}))


if __name__ == "__main__":
    main()
