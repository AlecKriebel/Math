#!/usr/bin/env python3
"""Read-only sealed-evidence checks and bounded mathematical diagnostics.

Run python3 -B verify_audit.py [--live]. No proposal code is imported/executed.
The finite controls do not prove asymptotic estimates; see the written proof.
"""
from pathlib import Path
import argparse
import cmath
import hashlib
import json
import math
import subprocess


def exact_cdfs(n):
    assert n % 4 == 0
    m = n // 2
    counts = [(2 * k - m, math.comb(m, k)) for k in range(m + 1)]
    at_i = sum(c * d for x, c in counts for y, d in counts if x*x + y*y <= n)
    at_pi = sum(math.comb(n, k) for k in range(n + 1) if (2*k - n)**2 <= n)
    exp_cdf = 1 - math.exp(-1)
    return {
        "n": n,
        "conjugate_joint_cdf_at_1": at_i / 2**n,
        "independent_exponential_joint_cdf_at_1": exp_cdf**2,
        "joint_cdf_gap": at_i / 2**n - exp_cdf**2,
        "real_axis_cdf_at_1": at_pi / 2**n,
        "exponential_cdf_at_1": exp_cdf,
    }


def dist(angle):
    return abs(math.remainder(angle, 2 * math.pi))


def radial_sum(n, t):
    return n if t == 0 else math.expm1(2*n*t) / math.expm1(2*t)


def w(n, t, eta):
    eta = math.remainder(eta, 2*math.pi)
    if eta == 0:
        return 1 + 0j
    return ((1 - cmath.exp(2*n*t + 1j*n*eta)) /
            (radial_sum(n, t) * (1 - cmath.exp(2*t + 1j*eta))))


def covariance(n, t, theta, phi):
    a, b, c, d = [w(n, t, x) for x in
                   [2*theta, 2*phi, theta-phi, theta+phi]]
    v = [[0.0]*4 for _ in range(4)]
    v[0][0], v[1][1] = .5+.5*a.real, .5-.5*a.real
    v[0][1] = v[1][0] = .5*a.imag
    v[2][2], v[3][3] = .5+.5*b.real, .5-.5*b.real
    v[2][3] = v[3][2] = .5*b.imag
    v[0][2] = v[2][0] = .5*(c.real+d.real)
    v[0][3] = v[3][0] = .5*(d.imag-c.imag)
    v[1][2] = v[2][1] = .5*(d.imag+c.imag)
    v[1][3] = v[3][1] = .5*(c.real-d.real)
    return v


def finite_controls():
    cdfs = [exact_cdfs(n) for n in [16, 64, 256, 1024]]
    assert cdfs[-1]["joint_cdf_gap"] > .20
    # Actual conjugate symmetry, not an empirical assumption of independence.
    for n in [16, 64, 256]:
        coeffs = [1 if (17*j*j + 13*j + 7) % 11 < 6 else -1 for j in range(n)]
        theta = .731
        z = sum(x*cmath.exp(1j*j*theta) for j, x in enumerate(coeffs))
        minus = sum(x*cmath.exp(-1j*j*theta) for j, x in enumerate(coeffs))
        assert abs(z.conjugate()-minus) < 1e-12
    cov = []
    for n in [64, 1024, 16384]:
        h = n**(-.5)
        max_scaled_row_norm = 0.0
        good = 0
        for sign in [-1, 0, 1]:
            r = 1 + sign*n**(-1.1)
            t = math.log(r)
            for j in range(1, 81):
                theta = math.remainder(.371*j + .19, 2*math.pi)
                phi = math.remainder(.617*j + .83, 2*math.pi)
                angles = [2*theta, 2*phi, theta-phi, theta+phi]
                if min(map(dist, angles)) <= h:
                    continue
                good += 1
                v = covariance(n, t, theta, phi)
                row_norm = max(sum(abs(v[a][b]-(.5 if a == b else 0))
                                   for b in range(4)) for a in range(4))
                max_scaled_row_norm = max(max_scaled_row_norm, row_norm*math.sqrt(n))
                for eta in angles:
                    # Exact geometric-sum upper bound underlying estimate (F).
                    rho = r*r
                    bound = ((1+math.exp(2*n*t)) /
                             (radial_sum(n, t)*math.sqrt(2*rho*(1-math.cos(eta)))))
                    assert abs(w(n, t, eta)) <= bound*(1+1e-10)
        assert good > 100
        assert max_scaled_row_norm < 10
        cov.append({"n": n, "sampled_good_pairs": good,
                    "max_sqrt_n_times_covariance_row_error": max_scaled_row_norm})
    scales = []
    for n in [64, 1024, 16384, 10**6]:
        delta = .1*n**(-1.1)
        lo, hi = math.exp(-delta), math.exp(delta)
        assert 1-n**(-1.1) <= lo <= hi <= 1+n**(-1.1)
        psi0 = .5*math.log(n)
        forward = (.5*math.log(radial_sum(n, delta))-psi0)/delta
        backward = (psi0-.5*math.log(radial_sum(n, -delta)))/delta
        bound = delta*(n-1)**2/4
        for secant in [forward, backward]:
            assert abs(secant-(n-1)/2) <= bound*(1+1e-7)
            assert abs(secant-n/2) <= n**.9/20*(1+1e-7)
        scales.append({"n": n, "delta": delta, "forward_secant": forward,
                       "backward_secant": backward, "allowed_center_error": n**.9/20})
    # General Jensen root controls, including a double root on the circle.
    delta = .05
    logarithmic_radii = [0, 0, -math.log(2), math.log(2), -.5*delta, .5*delta]
    jensen = lambda t: sum(max(0, t-a) for a in logarithmic_radii)
    lower = (jensen(0)-jensen(-delta))/delta
    upper = (jensen(delta)-jensen(0))/delta
    n_open = sum(a < 0 for a in logarithmic_radii)
    assert lower <= n_open <= upper
    assert n_open == 2 and sum(a == 0 for a in logarithmic_radii) == 2
    return {"scope": "Finite diagnostics only; asymptotic proof is the written derivation.",
            "exact_binomial_counterexample_controls": cdfs,
            "uniform_covariance_samples": cov, "scale_samples": scales,
            "boundary_root_control": {"left_secant": lower, "open_roots": n_open,
                                      "right_secant": upper, "circle_multiplicity": 2}}


def verify_seal(root):
    manifest_bytes = (root/"SEALED_MANIFEST.json").read_bytes()
    seal = json.loads((root/"AUDIT_SEAL.json").read_text())
    assert hashlib.sha256(manifest_bytes).hexdigest() == seal["manifest_sha256"]
    manifest = json.loads(manifest_bytes)
    actual_paths = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
                          and p.name not in {"SEALED_MANIFEST.json", "AUDIT_SEAL.json"})
    assert actual_paths == sorted(f["path"] for f in manifest["files"])
    for item in manifest["files"]:
        path = root/item["path"]
        data = path.read_bytes()
        assert len(data) == item["bytes"], item["path"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"], item["path"]
    pin = json.loads((root/"LIVE_PR_PIN.json").read_text())
    for item in pin["files"]:
        data = (root/item["local_path"]).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest() == item["sha"]
    body = (root/"private_sources/pr1049_body.txt").read_bytes()
    assert hashlib.sha256(body).hexdigest() == pin["body_sha256"]
    repair = json.loads((root/"INPUT_REPAIR_PIN.json").read_text())
    assert hashlib.sha256((root/repair["snapshot_path"]).read_bytes()).hexdigest() == repair["sha256"]
    return {"sealed_files_checked": len(manifest["files"]),
            "pr_blob_identities_checked": len(pin["files"]), "head": pin["head"]}


def live_check(root):
    pin = json.loads((root/"LIVE_PR_PIN.json").read_text())
    pr = json.loads(subprocess.check_output(["gh", "api", "repos/AlecKriebel/Math/pulls/1049"]))
    files = json.loads(subprocess.check_output(["gh", "api", "repos/AlecKriebel/Math/pulls/1049/files?per_page=100"]))
    comparisons = {
        "head": pr["head"]["sha"] == pin["head"],
        "base": pr["base"]["sha"] == pin["base"],
        "body": hashlib.sha256(pr["body"].encode()).hexdigest() == pin["body_sha256"],
        "paths_blobs_statuses": sorted((f["filename"], f["sha"], f["status"]) for f in files)
            == sorted((f["path"], f["sha"], f["status"]) for f in pin["files"]),
    }
    return {"read_only": True, "current_state": pr["state"], "current_draft": pr["draft"],
            "current_merged": pr["merged"], "pin_comparisons": comparisons,
            "all_pin_comparisons_match": all(comparisons.values()),
            "ledger_refreshed": False, "mutation_performed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Also re-read PR1049 via GitHub CLI; no writes.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    result = {"seal": verify_seal(root), "finite_controls": finite_controls()}
    if args.live:
        result["live"] = live_check(root)
    print(json.dumps(result, indent=2))
    if args.live and not result["live"]["all_pin_comparisons_match"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
