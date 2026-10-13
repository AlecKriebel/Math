#!/usr/bin/env python3
"""Verify the separate code copy changes only assertion control flow."""
import ast
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    spec = importlib.util.spec_from_file_location("repair_generator", HERE / "make_explicit_check_copy.py")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    provenance = json.loads((generator.REPAIRED / "REPAIR_PROVENANCE.json").read_text())
    results = []
    for row in provenance["scripts"]:
        original = (generator.SOURCE / row["path"]).read_bytes()
        repaired = (generator.REPAIRED / row["path"]).read_bytes()
        transformer = generator.ExplicitChecks(row["path"])
        expected_tree = transformer.visit(ast.parse(original.decode()))
        actual_tree = ast.parse(repaired.decode())
        same = ast.dump(expected_tree, include_attributes=False) == ast.dump(actual_tree, include_attributes=False)
        result = {"path": row["path"], "non_assert_code_preserved_in_ast": same,
                  "frozen_source_sha256_matches": generator.sha(original) == row["source_sha256"],
                  "repaired_sha256_matches": generator.sha(repaired) == row["repaired_sha256"],
                  "explicit_failure_branches": len(transformer.changed),
                  "remaining_assert_statements": sum(isinstance(n, ast.Assert) for n in ast.walk(actual_tree))}
        results.append(result)
    success = all(r["non_assert_code_preserved_in_ast"] and r["frozen_source_sha256_matches"]
                  and r["repaired_sha256_matches"] and not r["remaining_assert_statements"] for r in results)
    output = {"checked_utc": datetime.now(timezone.utc).isoformat(), "scripts": results,
              "all_equivalence_checks_passed": success,
              "meaning": "The repaired AST equals the source AST after only assert-to-if-not-raise transformation; comments/formatting differ."}
    (HERE / "REPAIR_EQUIVALENCE_RESULTS.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output))
    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
