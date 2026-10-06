"""Read-only exact checks for the separately appended v2 framing review."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import datetime
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
FAMILY = HERE.parent
AUDIT = FAMILY.parent
count = 0


def require(value, reason):
    global count
    if not value:
        raise ValueError(reason)
    count += 1


def pin(path):
    body = path.read_bytes()
    return {"path": str(path.relative_to(AUDIT)), "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}


manifest_path = FAMILY / "OUTPUT_MANIFEST.json"
require(pin(manifest_path)["sha256"] == "76c529cfd9c3161a401bd29955e5d1cccdb5507b0b9915f474c385183ddb6335", "frozen prior manifest")
manifest = json.loads(manifest_path.read_text())
require(len(manifest["files"]) == 12, "frozen prior membership")
frozen_before = []
for item in manifest["files"]:
    path = FAMILY / item["path"]
    actual = pin(path)
    require(actual["bytes"] == item["bytes"], "prior frozen bytes: " + item["path"])
    require(actual["sha256"] == item["sha256"], "prior frozen body: " + item["path"])
    frozen_before.append(actual)

original = AUDIT / "original_head_authentication_20261006" / "original_attempt" / "COUNTEREXAMPLE.md"
v2 = AUDIT / "repaired_diagnostics_v2" / "COUNTEREXAMPLE.md"
require(pin(original)["bytes"] == 10108 and pin(original)["sha256"] == "a9ea8220014aed7c082c995023a3bc7cdd10014544a85376d99267d908323266", "immutable original candidate")
require(pin(v2)["bytes"] == 10969 and pin(v2)["sha256"] == "0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f", "exact v2 candidate")

old = original.read_bytes()
new = v2.read_bytes()
old_prefix, old_tail = old.split(b"\nFinally, ", 1)
new_prefix, new_tail = new.split(b"\nFinally, ", 1)
old_changed, old_suffix = old_tail.split(b"\n## 7. Scope of the conclusion", 1)
new_changed, new_suffix = new_tail.split(b"\n## 7. Scope of the conclusion", 1)
require(old_prefix == new_prefix, "all proof through finite-time paragraph is unchanged")
require(old_suffix == new_suffix, "all historical-scope and concluding qualifications are unchanged")
require(old_changed != new_changed, "framing paragraph actually changed")
require(b"nonnegative" in new_changed and b"strict-positive" not in new_changed, "correct source index framing")
require(b"We assert no equality for this infimum" in new_changed, "time infimum equality excluded")
require(b"interchange no spatial supremum with a pointwise time limit" in new_changed, "order of operations preserved")

rejected = AUDIT / "repaired_diagnostics_v1" / "REJECTED_AFTER_HIGH_RESOLUTION_SOURCE_CHECK.json"
rejection = json.loads(rejected.read_text())
require(rejection["promotion_authorized_for_v1"] is False, "wrong diagnostic v1 rejected")
require(rejection["new_central_proof_search_turns"] == 0, "root repair is not a central proof turn")
require(rejection["pinned_pdf_sha256"] == "ed0ca54b5839cad99c88295b5b1a77bdeb6b7563bb8d2c7ccd412160bee7c168", "same source PDF")

s = Q(3, 4)
f = -(s - 1) * (s - 4) / (1 + s * s)
fp = (5 + 6 * s - 5 * s * s) / (1 + s * s) ** 2
radial_rate = f + 2 * s * fp
require(f == Q(-13, 25), "transient angular rate")
require(radial_rate == Q(2243, 625), "transient radial rate")
rates = [radial_rate, f, radial_rate, f, Q(-100)]
leading_sums = [max(sum(c, Q(0)) for c in combinations(rates, k)) for k in range(1, 6)]
require(leading_sums[3] == Q(3836, 625), "transient leading four sum")
require(leading_sums[3] > 0 and leading_sums[4] < 0, "transient nonnegative index is four")
require(leading_sums[3] - leading_sums[4] == 100, "transient denominator")
instant_dimension = 4 + leading_sums[3] / 100
require(instant_dimension == Q(63459, 15625), "exact instantaneous dimension")
require(instant_dimension - Q(203, 50) == Q(43, 31250), "strict transient excess")
require(instant_dimension > Q(203, 50), "finite-time spatial maximum need not equal asymptotic maximum")

root_control_path = AUDIT / "repaired_diagnostics_v1" / "FINITE_TIME_CONTROL.json"
root_control = json.loads(root_control_path.read_text())
require(root_control["s"] == str(s), "root control radius square")
require(root_control["f"] == str(f), "root control angular rate")
require(root_control["gprime"] == str(radial_rate), "root control radial rate")
require(root_control["twooscillator_instantaneous_dimension"] == str(instant_dimension), "root control dimension")

frozen_after = [pin(FAMILY / item["path"]) for item in manifest["files"]]
require(frozen_before == frozen_after, "all 12 prior offered artifacts unchanged")
require(pin(manifest_path)["sha256"] == "76c529cfd9c3161a401bd29955e5d1cccdb5507b0b9915f474c385183ddb6335", "prior manifest still unchanged")

result = {
    "schema": "pr111-v2-primary-source-framing-readback/v1",
    "completed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "actual_pid": os.getpid(),
    "all_pass": True,
    "checks": count,
    "candidate_v2_pin": pin(v2),
    "immutable_original_pin": pin(original),
    "unchanged_prior12_artifact_pins": frozen_after,
    "unchanged_prior_manifest_pin": pin(manifest_path),
    "program_pin": pin(Path(__file__)),
    "rejected_v1_record_pin": pin(rejected),
    "root_control_pin": pin(root_control_path),
    "exact_instantaneous_rates": list(map(str, rates)),
    "exact_leading_sums": list(map(str, leading_sums)),
    "exact_instantaneous_dimension": str(instant_dimension),
    "exact_excess_over_asymptotic_maximum": str(instant_dimension - Q(203, 50)),
    "analytic_small_time_argument": "In rotating orthonormal frames the diagonal logarithmic rates are time averages of continuous radial/angular coefficients, so they converge to these exact instantaneous rates as t decreases to zero. The strict index and dimension inequalities persist for sufficiently small positive times.",
    "mandatory_corrections": [],
    "new_central_proof_search_turns": 0,
    "priority_clearance": False,
    "publication_approval": False,
    "private_copyright_bodies_embedded": False,
}
(HERE / "CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"actual_pid": os.getpid(), "all_pass": True, "checks": count, "receipt_pin": pin(HERE / "CHECKS.json")}, indent=2))
