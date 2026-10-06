#!/usr/bin/env python3
"""Reproduce exact-head diagnostics in ignored copies and count actual checks.

Input scripts and full replay outputs stay in tmp/. The persistent output is
our own measurement and comparison report. No source snapshot file is edited.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import runpy
import shutil
import sys
import contextlib
import ast


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_observed(script, mode, output_path):
    counts = Counter()
    resolved = str(script.resolve())
    def observer(frame, event, arg):
        if frame.f_code.co_filename == resolved:
            if mode == "verify_calls" and event == "call" and frame.f_code.co_name == "verify":
                counts[frame.f_back.f_lineno] += 1
        return observer
    with output_path.open("w") as output, contextlib.redirect_stdout(output):
        # First execute the exact unmodified standalone copy in both cases.
        if mode == "verify_calls": sys.setprofile(observer)
        try:
            namespace = runpy.run_path(resolved, run_name="__main__")
        finally:
            sys.setprofile(None)
        if mode == "assert_lines":
            # Source-line tracing counts generator resumptions as repeated
            # line events. A separate in-memory AST observer counts entry
            # into each actual assertion exactly once, including inline
            # assertions. The unmodified copy has already run above.
            class Probe(ast.NodeTransformer):
                def visit_Assert(self, node):
                    probe = ast.Expr(ast.Call(ast.Name("__audit_observe_assert__", ast.Load()),
                                              [ast.Constant(node.lineno)], []))
                    return [ast.copy_location(probe,node), node]
            tree = ast.fix_missing_locations(Probe().visit(ast.parse(script.read_text())))
            def record(lineno): counts[lineno] += 1
            observed_namespace = {"__name__":"__main__","__file__":resolved,
                                  "__audit_observe_assert__":record}
            exec(compile(tree,resolved,"exec"), observed_namespace)
    return namespace, dict(sorted(counts.items())), sum(counts.values())


def main():
    own = Path(__file__).resolve().parent
    snapshot = own.parent / "source_snapshot"
    files = sorted(p for p in snapshot.rglob("*") if p.is_file())
    before = {str(p.relative_to(snapshot)): sha(p) for p in files}
    assert len(files) == 13
    assert before["BASELINE.md"] == "9e0a930e61d849799c4395024c85d4f9c75b63ae2172321ef78ebf643f283c82"
    tmp = own / "tmp"
    author_dir, reviewer_dir = tmp / "author", tmp / "reviewer"
    author_dir.mkdir(parents=True, exist_ok=True)
    reviewer_dir.mkdir(parents=True, exist_ok=True)
    author = author_dir / "check_small_planes.py"
    reviewer = reviewer_dir / "independent_checks.py"
    shutil.copyfile(snapshot / "check_small_planes.py", author)
    shutil.copyfile(snapshot / "review/independent_checks.py", reviewer)
    assert sha(author) == before["check_small_planes.py"]
    assert sha(reviewer) == before["review/independent_checks.py"]
    author_ns, author_checks, author_count = run_observed(author, "assert_lines", author_dir / "stdout.txt")
    reviewer_ns, reviewer_checks, reviewer_count = run_observed(reviewer, "verify_calls", reviewer_dir / "stdout.txt")
    author_output = author_dir / "check_results.json"
    reviewer_output = reviewer_dir / "independent_checks.json"
    author_report = json.loads(author_output.read_text())
    reviewer_report = json.loads(reviewer_output.read_text())
    assert sha(author_output) == before["check_results.json"]
    assert sha(author_output) == before["review/check_results.json"]
    assert sha(reviewer_output) == before["review/independent_checks.json"]
    author_subsets = sum(p["all_point_subsets_checked"] for p in author_report["planes"])
    reviewer_subsets = sum(p["all_point_subsets"] for p in reviewer_report["planes"])
    assert author_subsets == reviewer_subsets == 8320
    # Independent analytic count of each actual verify() call. The formula is
    # derived from call sites and independently enumerated O/N counts.
    fresh = json.loads((own / "fresh_checks.json").read_text())
    expected_checks = {}
    for plane in fresh["planes"]:
        n, total = plane["n"], plane["point_subsets"]
        ordinary, nontrivial = plane["ordinary_blockers"], plane["nontrivial_blockers"]
        geometry = 2+n+n*(n-1)
        subset_loop = 2*total+2*ordinary+5*nontrivial
        final_checks = 8+3*(n+1)
        expected_checks[plane["q"]] = geometry+subset_loop+final_checks
    assert sum(expected_checks.values()) == reviewer_count == reviewer_report["assertions"] == 28072
    # 4 geometry asserts per order; 2 per nontrivial blocker, 1 alteration
    # assert per ordinary blocker; 3 final asserts per order.
    expected_author = sum(7+2*p["nontrivial_blockers"]+p["ordinary_blockers"]
                          for p in fresh["planes"])
    assert author_count == expected_author == 5344
    # Check the homogeneous author incidence system against our own affine
    # certificate under the explicit coordinate map, with no classification.
    certificates = json.loads((own / "fresh_certificates.json").read_text())
    coordinate_crosscheck = []
    for cert, plane in zip(certificates, fresh["planes"]):
        q = cert["q"]
        homogeneous_points, homogeneous_lines, _ = author_ns["projective_plane"](q)
        point_index = {tuple(p): i for i, p in enumerate(homogeneous_points)}
        permutation = []
        for point in cert["points"]:
            if point[0] == "affine":
                vector = (point[1], point[2], 1)
            elif point[0] == "slope":
                vector = (1, point[1], 0)
            else:
                vector = (0, 1, 0)
            first = next(x for x in vector if x)
            inverse = pow(first, -1, q)
            normalized = tuple(x*inverse % q for x in vector)
            permutation.append(point_index[normalized])
        assert len(set(permutation)) == len(permutation)
        def remap(mask):
            return sum(1 << permutation[i] for i in range(len(permutation)) if mask & (1 << i))
        mapped_lines = {remap(mask) for mask in cert["line_point_masks"]}
        assert mapped_lines == set(homogeneous_lines)
        author_plane = next(p for p in author_report["planes"] if p["q"] == q)
        reviewer_plane = next(p for p in reviewer_report["planes"] if p["q"] == q)
        assert author_plane["minimal_blocking_set_counts"] == plane["minimal_blocker_size_histogram"]
        assert reviewer_plane["minimal_blockers_by_size"] == plane["minimal_blocker_size_histogram"]
        coordinate_crosscheck.append({"q":q, "explicit_point_permutation":permutation,
                                     "all_lines_match":True})
    after = {str(p.relative_to(snapshot)): sha(p) for p in files}
    assert before == after
    result = {"utc":datetime.now(timezone.utc).isoformat(), "status":"pass",
              "snapshot_files":len(files), "snapshot_unchanged":before == after,
              "snapshot_sha256":after,
              "author":{"subsets":author_subsets,"result_bytes_match":True,
                        "executed_assert_statements":author_count,
                        "assert_count_method":"separate in-memory AST entry observer after unmodified replay",
                        "independent_expected_assert_statements":expected_author,
                        "by_source_line":author_checks},
              "reviewer":{"subsets":reviewer_subsets,"result_bytes_match":True,
                          "observed_verify_calls":reviewer_count,
                          "independent_expected_checks_by_order":expected_checks,
                          "by_call_source_line":reviewer_checks},
              "explicit_coordinate_crosscheck":coordinate_crosscheck,
              "limit":"Finite diagnostics reproduced exactly; no asymptotic proof inferred."}
    (own / "reproduction_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
