#!/usr/bin/env python3
"""Independently bridge final docstring-only tool corrections to tested behavior.

Reconstruct the preceding source hashes, compare ASTs excluding only their first
module-docstring node, and execute fresh synthetic positive assembly/outer paths.
No corpus/PDF input, marker, publication, or final paper/package is involved.
"""
import ast
from pathlib import Path
import runpy
import shutil
import time

HERE = Path(__file__).resolve().parent
h = runpy.run_path(str(HERE / "guard_review.py"), run_name="guard_library_only")
Review, need, sha, put, encoded, archive = [h[n] for n in ["Review", "need", "sha", "put", "encoded", "archive"]]
review = object.__new__(Review)
review.full = False
review.start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
review.runroot = HERE / "private" / "final_docstring_bridge"
review.receipts = []
review.candidate = {}
review.modules = {}
need(not review.runroot.exists(), "own bridge fixture already exists")
review.runroot.mkdir(parents=True)
old_prefix = (b'#!/usr/bin/env python3\n'
              b'"""Authenticate all frozen PR880 originals and replay finite diagnostics. No mathematical or priority certificate.\n'
              b'Authenticate startup bytes independently before execution. Standard library only.\n"""\n')
expected_old = {"local_tools/pr880_verify_current_publication.py": "465f9f4875740f282db18a13d1ea57137bb71708d3e87c1c6d8cf881d191abc6",
                "local_tools/pr880_assemble.py": "4523285345f0d9df2d8024db419769915494406e4446c27b882d005a62a8a893"}


def stripped(raw):
    tree = ast.parse(raw)
    need(tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant)
         and isinstance(tree.body[0].value.value, str), "leading module docstring missing")
    tree.body.pop(0)
    return ast.dump(tree, annotate_fields=True, include_attributes=False).encode()


success = False
bridges = []
try:
    review.freeze()
    for file, old_sha in expected_old.items():
        new = review.candidate[file]
        old = old_prefix + b'import argparse\n' + new.split(b'import argparse\n', 1)[1]
        need(sha(old) == old_sha, "preceding source reconstruction does not match receipt: " + file)
        need(stripped(old) == stripped(new), "change extends beyond module docstring: " + file)
        bridges.append({"path": file, "old_bytes": len(old), "old_sha256": sha(old), "new_bytes": len(new), "new_sha256": sha(new),
                        "old_leading_docstring": ast.get_docstring(ast.parse(old), clean=False),
                        "new_leading_docstring": ast.get_docstring(ast.parse(new), clean=False),
                        "stripped_ast_sha256": sha(stripped(new)), "docstring_only": True})
    blobs = review.original_fixture()
    root, portable, pin = review.materialize(blobs)
    # This positive/negative bridge is source-free. It authenticates fresh final
    # wrapper copies and executes both normal and optimized outer entry points.
    review.outer_tests(portable, archive(portable))
    success = True
finally:
    still = all((HERE.parent / f).read_bytes() == raw for f, raw in review.candidate.items())
    result = {"schema": "pr880-independent-docstring-bridge-v1", "scope": "Final docstring-only candidate bridge; synthetic paper fixtures and source-free replay only. No final whole-package clearance.",
              "success": bool(success and still), "timestamp_utc": review.start, "harness_sha256": sha(Path(__file__).read_bytes()),
              "shared_guard_sha256": sha((HERE / "guard_review.py").read_bytes()), "bridges": bridges,
              "final_candidate_files": [h["row"](f, raw) for f, raw in sorted(review.candidate.items())],
              "candidate_unchanged_during_bridge": still, "receipt_count": len(review.receipts), "receipts": review.receipts}
    put(HERE / "DOCSTRING_BRIDGE.json", encoded(result))
    shutil.rmtree(review.runroot)
    print(encoded({"success": result["success"], "receipt_count": len(review.receipts), "private_fixture_removed": not review.runroot.exists()}).decode(), end="")
