#!/usr/bin/env python3
"""Isolated bounded checks; these are not an analytic proof certificate."""
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
REPO = AUDIT.parents[2]
HEAD = "c09ef9df8b1f4642be0396ba6343344be8fa25b0"
PREFIX = "unsolved_math_prioritization/attempts/30003471/"

def sha(data):
    return hashlib.sha256(data).hexdigest()

snapshot = json.loads((AUDIT / "SOURCE_SNAPSHOT.json").read_text())
assert snapshot["head"] == HEAD
bound = []
for item in snapshot["files"]:
    local = (AUDIT / "original" / item["path"]).read_bytes()
    frozen = subprocess.check_output(
        ["git", "show", f"{HEAD}:{PREFIX}{item['path']}"], cwd=REPO)
    assert local == frozen
    assert len(local) == item["bytes"] and sha(local) == item["sha256"]
    bound.append({"path": item["path"], "bytes": len(local), "sha256": sha(local),
                  "matches_immutable_git_blob": True})
git_paths = subprocess.check_output(
    ["git", "ls-tree", "-r", "--name-only", HEAD, "--", PREFIX], cwd=REPO
).decode().splitlines()
assert sorted(x[len(PREFIX):] for x in git_paths) == sorted(x["path"] for x in bound)
(HERE / "SOURCE_BINDINGS.json").write_text(json.dumps({
    "immutable_head": HEAD, "repo_prefix": PREFIX, "files_bound": bound,
    "whole_prefix_file_set_matched": True,
    "primary_downloads": json.loads((HERE / "private" / "PRIMARY_DOWNLOADS.json").read_text()),
    "private_primary_bodies_excluded_from_public_review_manifest": True
}, indent=2) + "\n")

# This copied program was inspected in full before execution. It has no external
# calls and only prints its finite results. Execute it outside the frozen tree.
copy = HERE / "private" / "replayed_controls.py"
shutil.copyfile(AUDIT / "original" / "public" / "controls.py", copy)
replay = json.loads(subprocess.check_output(["python3", str(copy)], cwd=HERE))
expected = json.loads((AUDIT / "original" / "public" / "CONTROL_RESULTS.json").read_text())
assert replay == expected

# Independently express the three generators with exact Gaussian-integer
# arithmetic, and check their full basis relations and boundary symbols.
I = ((1, 0), (0, 1))
Z = ((0, 0), (0, 0))
C = (((0, -1j), (-1j, 0)), ((0, -1), (1, 0)), ((-1j, 0), (0, 1j)))
def plus(a,b):
    return tuple(tuple(a[i][j]+b[i][j] for j in range(2)) for i in range(2))
def times(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def scaled(s,a):
    return tuple(tuple(s*a[i][j] for j in range(2)) for i in range(2))
bases = [((1,0),(0,0)), ((0,1),(0,0)), ((0,0),(1,0)), ((0,0),(0,1))]
clifford = boundary_symbols = 0
for j in range(3):
    for k in range(3):
        assert plus(times(C[j], C[k]), times(C[k], C[j])) == (scaled(-2,I) if j == k else Z)
        clifford += 1
        if j != k:
            L = scaled(1j, times(C[j], C[k]))
            for m in C:
                chi = lambda a: scaled(-1, times(times(C[j], a), m))
                for a in bases:
                    assert plus(chi(times(L,a)), times(L,chi(a))) == Z
                    boundary_symbols += 1
assert times(times(C[0],C[1]),C[2]) == scaled(-1,I)

# A negative control separates arclength transport from the invalid substitute
# that uses equal affine weights at both endpoints. At an endpoint that
# substitute has speed ratio sin(beta)/sin(alpha), which can exceed 1.
alpha, beta = 2.6, 1.3
bad_ratio = math.sin(beta) / math.sin(alpha)
assert beta < alpha and bad_ratio > 1.8

result = {
    "immutable_file_bindings": len(bound),
    "copied_original_controls_equal_frozen_result": True,
    "copied_original_controls": replay,
    "independent_clifford_basis_relations_exact": clifford,
    "independent_boundary_symbol_basis_relations_exact": boundary_symbols,
    "equal_affine_weight_negative_control_speed_ratio": bad_ratio,
    "proof_has_arclength_transport_so_negative_control_does_not_refute_it": True,
    "analytic_proof_certified_by_computation": False,
    "historical_audit_conclusions_read": False
}
(HERE / "EVIDENCE_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k:v for k,v in result.items() if k != "copied_original_controls"}, indent=2))
