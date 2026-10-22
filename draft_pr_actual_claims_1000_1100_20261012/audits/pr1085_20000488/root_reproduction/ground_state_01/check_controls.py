#!/usr/bin/env python3
"""Independent finite regression controls; analytic proofs are in the review.

Uses only the standard library. It checks frozen-byte custody, exact rational
constant margins, boundary signs/Jacobians, cutoff signs, and deliberate
mutations. Finite probes are not used as proofs of continuum inequalities.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
HEAD = "5e23f0c801d23976830657d2eef2b32bdc7da05a"
NAMES = ["MANIFEST.json", "MATHEMATICAL_AUDIT.md", "MATHEMATICAL_REPORT.md",
         "README.md", "SOURCE_METADATA.json", "STATUS.json"]


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def validate_package(files, pins):
    require(set(files) == set(NAMES), "exact six-file membership")
    for name in NAMES:
        require(hashlib.sha256(files[name]).hexdigest() == pins[name]["sha256"],
                "SHA256 " + name)
        require(len(files[name]) == pins[name]["size"], "byte size " + name)
    manifest = json.loads(files["MANIFEST.json"])
    require(manifest["member_count"] == 6 and set(manifest["members"]) == set(NAMES),
            "manifest membership")
    for row in manifest["entries"]:
        name = row["file"]
        require(hashlib.sha256(files[name]).hexdigest() == row["sha256"],
                "internal manifest hash " + name)
        require(len(files[name]) == row["bytes"], "internal manifest bytes " + name)
    status = json.loads(files["STATUS.json"])
    for key in ["embedded_eigenvalues_excluded", "all_coupling_graph_absence",
                "general_higher_dimensional_nongraph_classification",
                "historical_novelty_certified", "current_open_status_certified"]:
        require(status[key] is False, "forbidden stronger conclusion " + key)
    require(status["general_target_resolved_by_this_work"] is True,
            "negative answer is distinguished from scope limitations")


def rejected(fn):
    try:
        fn()
    except (RuntimeError, ValueError, KeyError):
        return True
    return False


def run():
    files = {name: (HERE / "frozen" / name).read_bytes() for name in NAMES}
    pins = json.loads((HERE / "INPUT_PINS.json").read_text())["files"]
    validate_package(files, pins)
    git_rows = []
    for name in NAMES:
        path = "unsolved_math_prioritization/attempts/20000488/" + name
        data = subprocess.check_output(["git", "show", HEAD + ":" + path], cwd=ROOT)
        require(data == files[name], "PR Git blob equality " + name)
        git_rows.append(name)

    # Exact rational margin: e^(1/25) <= 1/(1-1/25) = 25/24.
    # The analytic series comparison proves this upper bound, strictly here.
    upper_defect = F(1, 5000) * F(25, 24) * 10
    lower_coercivity = F(1250, 2501)
    require(upper_defect == F(1, 480), "absence upper coefficient")
    require(lower_coercivity > F(1, 3), "coercivity > 1/3")
    require(upper_defect < lower_coercivity, "explicit beta=1 absence margin")
    require(F(1, 250) < F(1, 3), "report's weaker exact margin")

    # Ground-state coefficient is -beta*(1+nu_y); the flat lower normal is -1.
    beta = F(7, 3)
    normals = [F(-1), F(-4, 5), F(0), F(4, 5), F(1)]
    defects = [1 + ny for ny in normals]
    require(all(d >= 0 for d in defects), "defect sign on all selected normals")
    require(defects[0] == 0 and all(d > 0 for d in defects[1:]), "flat/nonflat defect")
    for ny in normals:
        require(-beta * ny - beta == -beta * (1 + ny), "normal coefficient identity")

    # Graph slope 3/4 has s=5/4, nu_y=-4/5; the Jacobian is essential.
    s, ny = F(5, 4), F(-4, 5)
    require((1 + ny) * s == s - 1 == F(1, 4), "graph boundary Jacobian")
    require((1 + ny) != s - 1, "omitted-Jacobian mutation detected")
    require((1 - ny) * s != s - 1, "normal-sign mutation detected")

    # Exact finite probes of the all-function coercivity, independent of package text.
    # Infinite-dimensional validity is established by the triangle-square derivation.
    probes = 0
    grid = [F(-2), F(-1, 2), F(0), F(1, 3), F(3)]
    g = [F(1, 3), F(-2, 3), F(2, 3)]  # squared norm exactly 1
    G2 = sum(z*z for z in g)
    require(G2 == 1, "unit slope vector")
    for a0 in grid:
        for a1 in grid:
            for b in grid:
                a = [a0, a1, F(2, 5)]
                left = sum(z*z for z in a) + b*b
                bulk = sum((z-t*b)**2 for z, t in zip(a, g)) + b*b
                require(left <= 2*(1+G2)*bulk, "coercivity exact probe")
                probes += 1
    # Complex vectors split into independent real and imaginary probes.
    require(probes == 125, "finite probe coverage")

    # Formal log-range ell=400, beta=1, B>=1/100: pi<22/7 suffices.
    B = F(1, 100)
    linear_energy = F(2, 200)
    log_energy_upper = F(44, 7*400)
    require(linear_energy / 2 - B < 0, "m=1 trial negativity")
    require(log_energy_upper / 2 - B < 0, "m=2 trial negativity")
    # Doubling the defect sign makes both positive: it must not pass binding.
    require(linear_energy / 2 + B > 0 and log_energy_upper / 2 + B > 0,
            "binding sign mutation detected")

    mutations = {}
    bad = dict(files)
    bad["MATHEMATICAL_REPORT.md"] += b"\nfalse unsupported claim\n"
    mutations["changed_report_bytes"] = rejected(lambda: validate_package(bad, pins))
    bad = dict(files)
    status = json.loads(bad["STATUS.json"])
    status["embedded_eigenvalues_excluded"] = True
    bad["STATUS.json"] = json.dumps(status).encode()
    badpins = dict(pins)
    badpins["STATUS.json"] = {"sha256": hashlib.sha256(bad["STATUS.json"]).hexdigest(),
                              "size": len(bad["STATUS.json"])}
    altered_manifest = json.loads(bad["MANIFEST.json"])
    for row in altered_manifest["entries"]:
        if row["file"] == "STATUS.json":
            row["sha256"] = badpins["STATUS.json"]["sha256"]
            row["bytes"] = badpins["STATUS.json"]["size"]
    bad["MANIFEST.json"] = json.dumps(altered_manifest).encode()
    badpins["MANIFEST.json"] = {"sha256": hashlib.sha256(bad["MANIFEST.json"]).hexdigest(),
                                "size": len(bad["MANIFEST.json"])}
    mutations["changed_status_even_with_repin"] = rejected(lambda: validate_package(bad, badpins))
    bad = dict(files)
    bad.pop("SOURCE_METADATA.json")
    mutations["missing_member"] = rejected(lambda: validate_package(bad, pins))
    require(all(mutations.values()), "all deliberate package mutations rejected")

    return {"result": "PASS", "git_authenticated_files": git_rows,
            "exact_absence_upper": str(upper_defect),
            "exact_coercivity_lower": str(lower_coercivity),
            "exact_margin_lower": str(lower_coercivity-upper_defect),
            "matrix_rational_probes": probes, "mutations_rejected": mutations,
            "limitations": "Finite guards supplement the independent analytic proof; no numerical spectral premise or omitted author computation replay."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
