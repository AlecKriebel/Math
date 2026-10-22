#!/usr/bin/env python3
"""Reproduce two earlier tool defects using exact-hash reconstructed byte copies.

No candidate mutation. Synthetic disposable fixtures; no corpus/PDF input or marker.
"""
import json
from pathlib import Path
import runpy
import shutil
import time

HERE = Path(__file__).resolve().parent
h = runpy.run_path(str(HERE / "guard_review.py"), run_name="guard_library_only")
Review, need, sha, put, encoded, index = [h[n] for n in ["Review", "need", "sha", "put", "encoded", "index"]]
review = object.__new__(Review)
review.full = False
review.start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
review.runroot = HERE / "private" / "fixed_defect_reproduction"
review.receipts = []
review.candidate = {f: (HERE.parent / f).read_bytes() for f in h["FILES"]}
need(not review.runroot.exists(), "own old fixture still exists")
review.runroot.mkdir(parents=True)
success = False
try:
    old_verifier = review.candidate["preprint/verify_package.py"].replace(
        b"                target.chmod(0o644)", b"            target.chmod(0o644)")
    old_assembler = review.candidate["local_tools/pr880_assemble.py"].replace(
        b'    require(not any(name == index_name or name.startswith(index_name + "/")\n'
        b'                    or index_name.startswith(name + "/") for name in blobs),\n'
        b'            "generated index file/directory collision")',
        b'    require(index_name not in blobs, "generated index destination collision")')
    # Final candidate descriptions were corrected without behavior changes.
    # Restore the exact earlier module prefix when reconstructing its old hash.
    old_prefix = (b'#!/usr/bin/env python3\n'
                  b'"""Authenticate all frozen PR880 originals and replay finite diagnostics. No mathematical or priority certificate.\n'
                  b'Authenticate startup bytes independently before execution. Standard library only.\n"""\n')
    old_assembler = old_prefix + b'import argparse\n' + old_assembler.split(b'import argparse\n', 1)[1]
    need(sha(old_verifier) == "3d4baafaa90d17746685a481a74d0267479888ade3c4f8fb9d09df8c1c4288ba", "old verifier reconstruction not exact")
    need(sha(old_assembler) == "608a5a6bb613bb52525cd07ff4db31fed785fd235e2e8c02d50df21971023286", "old assembler reconstruction not exact")
    blobs = review.original_fixture()
    old_blobs = dict(blobs)
    old_blobs["verify_package.py"] = old_verifier
    old_index = index(old_blobs)
    old_blobs["package_index.json"] = old_index
    root = review.runroot / "old_umask_fixture"
    review.write_tree(root, old_blobs)
    review.cli("old_verifier_umask022_positive", root / "verify_package.py", [sha(old_index), "--root", root, "--full"])
    for optimized in [False, True]:
        review.cli("old_verifier_umask077_failure_O" + str(optimized), root / "verify_package.py", [sha(old_index), "--root", root, "--full"],
                   expected="REJECTED", optimized=optimized, umask=0o077)
    old_tool = review.runroot / "old_assembler.py"
    put(old_tool, old_assembler)
    for kind in ["portable", "outer"]:
        bad = dict(blobs) if kind == "portable" else {"README.md": h["MARK"], "RESEARCH_LOG.md": h["MARK"], "CURRENT_PUBLICATION.json": b"{}\n", "verify_current_publication.py": review.candidate["local_tools/pr880_verify_current_publication.py"]}
        name = "package_index.json" if kind == "portable" else "PUBLICATION_MANIFEST.json"
        bad[name + "/x"] = h["MARK"]
        seed = review.runroot / (kind + "_seed")
        review.write_tree(seed, bad)
        _, path, pin = review.make_spec(seed, bad, kind, kind + "_spec")
        output = review.runroot / (kind + "_partial_output")
        review.cli("old_assembler_generated_index_child_" + kind, old_tool, [seed, path, pin, output], expected="REJECTED")
        count = sum(p.is_file() for p in output.rglob("*"))
        review.record("old_assembler_partial_materialization_" + kind, "historical_regression", count > 0,
                      output_files_after_failure=count, index_path_became_directory=(output / name).is_dir())
    success = True
finally:
    result = {"schema": "pr880-fixed-defect-reproduction-v1", "success": success,
              "scope": "Exact-hash reconstructed pre-fix tools against synthetic private fixtures; not final candidate or package.",
              "timestamp_utc": review.start, "harness_sha256": sha(Path(__file__).read_bytes()),
              "shared_guard_sha256": sha((HERE / "guard_review.py").read_bytes()),
              "old_verifier_sha256": sha(old_verifier), "old_assembler_sha256": sha(old_assembler),
              "receipts": review.receipts}
    put(HERE / "REGRESSION_REPRODUCTION.json", encoded(result))
    shutil.rmtree(review.runroot)
    print(json.dumps({"success": success, "receipt_count": len(review.receipts), "private_fixture_removed": not review.runroot.exists()}))
