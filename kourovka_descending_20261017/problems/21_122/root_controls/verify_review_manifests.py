#!/usr/bin/env python3
"""Read-only check that accepted supporting reviews still describe current files."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks = []
    receipts = []

    def check(path, expected, receipt):
        path = Path(path)
        if not path.is_absolute():
            if path.parts[0] == ROOT.parent.parent.name:
                path = ROOT.parents[2] / path
            else:
                path = ROOT / path
        current = sha256(path.read_bytes()).hexdigest()
        assert current == expected, (str(path), expected, current, receipt)
        checks.append({"path": str(path.relative_to(ROOT)), "sha256": current,
                       "receipt": receipt})

    def read(relative):
        receipts.append(relative)
        return json.loads((ROOT / relative).read_text())

    relative = "topological_review/RECEIPT.json"
    data = read(relative)
    assert data["verdict"] == "PASS" and not data["complete_21_122_solution"]
    for entry in data["inputs"] + data["outputs"]:
        check(entry["path"], entry["sha256"], relative)
    relative = "topological_review/secondary/RECEIPT.json"
    data = read(relative)
    assert data["result"] == "PASS" and not data["full_problem_solution"]
    check(data["input"]["path"], data["input"]["sha256"], relative)
    for path, expected in data["files_sha256"].items():
        check(path, expected, relative)
    relative = "structural/central_countermodel_review/review_receipt.json"
    data = read(relative)
    assert data["verdict"] == "VERIFIED_ROUTE_OBSTRUCTION_NO_SUBSTANTIVE_OBJECTION"
    for name, key in (("CENTRAL_NONPOLYNOMIAL.md", "audited_proof_sha256"),
                      ("check_central_countermodel.py", "audited_checker_sha256"),
                      ("central_countermodel_results.json", "audited_author_results_sha256")):
        check("structural/"+name, data[key], relative)
    for name, expected in data["review_artifact_sha256"].items():
        check("structural/central_countermodel_review/"+name, expected, relative)
    relative = "abelian_extraction_review/INPUT_MANIFEST.json"
    data = read(relative)
    for entry in data["files"]:
        check(entry["source"], entry["sha256"], relative)
        check(entry["snapshot"], entry["sha256"], relative)
    relative = "abelian_extraction_review/OUTPUT_MANIFEST.json"
    data = read(relative)
    for entry in data["files"]:
        check("abelian_extraction_review/"+entry["relative_path"], entry["sha256"], relative)
    relative = "structural/route_review/review_receipt.json"
    data = read(relative)
    assert data["verdict"] == "VERIFIED_SUPPORTING_STRUCTURAL_DEDUCTIONS_AND_ROUTE_COUNTERMODELS"
    assert not data["substantive_objections"]
    for name, expected in data["audited_author_sha256"].items():
        check("structural/"+name, expected, relative)
    for name, expected in data["review_artifact_sha256"].items():
        check("structural/route_review/"+name, expected, relative)
    relative = "counterexample_review/RECEIPT.json"
    data = read(relative)
    assert data["verdict"] == "PASS" and not data["complete_21_122_solution"]
    check("counterexample_review/INPUT_MANIFEST.json", data["input_manifest_sha256"], relative)
    check("counterexample_review/OUTPUT_MANIFEST.json", data["output_manifest_sha256"], relative)
    for name, expected in data["proof_hashes"].items():
        check("counterexample/"+name, expected, relative)
    for relative in ("counterexample_review/INPUT_MANIFEST.json",
                     "counterexample_review/OUTPUT_MANIFEST.json"):
        data = read(relative)
        for entry in data["files"]:
            check(entry["path"], entry["sha256"], relative)
    relative = "counterexample_review/law_branch_secondary/RECEIPT.json"
    data = read(relative)
    assert data["verdict"] == "PASS" and not data["full_problem_solved"]
    check(data["input"]["path"], data["input"]["sha256"], relative)
    for name, expected in data["files"].items():
        check("counterexample_review/law_branch_secondary/"+name, expected, relative)
    output = {"utc": datetime.now(timezone.utc).isoformat(), "result": "PASS",
              "scope": "Current hashes for supporting partial reviews only; no full21.122 resolution or originality inference",
              "review_receipts": receipts, "hash_checks": len(checks), "checks": checks}
    if args.output:
        with args.output.open("x") as handle:
            json.dump(output, handle, indent=2)
            handle.write("\n")
    print(json.dumps({"result": "PASS", "hash_checks": len(checks), "receipts": len(receipts)}))


if __name__ == "__main__":
    main()
