#!/usr/bin/env python3
"""Read-only, offline verifier for the authored PR1131 priority audit package.

Uses only the standard library, reads only the explicitly supplied directory,
prints JSON, and performs no network access or writes. It checks integrity and
internal arithmetic/scope consistency, not novelty or the manuscript's proof.
No assert statements are used, so checks remain active with -O and -OO.
"""
import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--expected-manifest-sha256", required=True)
    args = parser.parse_args()
    package = args.package.resolve(strict=True)
    require(package.is_dir(), "package is not a directory")
    manifest_path = package / "MANIFEST.json"
    require(not manifest_path.is_symlink(), "manifest may not be a symlink")
    manifest_bytes = manifest_path.read_bytes()
    digest = hashlib.sha256(manifest_bytes).hexdigest()
    require(digest == args.expected_manifest_sha256, "external manifest pin mismatch")
    manifest = json.loads(manifest_bytes)
    expected_members = {
        "PRIORITY_REPORT.md", "PINNED_SCOPE.json", "SOURCE_INVENTORY.json",
        "SEARCH_LOG.json", "OUTCOME.json", "verify_priority.py",
    }
    require(manifest["schema"] == "pr1131-priority-audit-manifest-v1", "schema mismatch")
    entries = manifest["entries"]
    require(len(entries) == len(expected_members), "entry count mismatch")
    require({e["file"] for e in entries} == expected_members, "manifest member mismatch")
    require({x.name for x in package.iterdir()} == expected_members | {"MANIFEST.json"}, "unexpected member")
    for entry in entries:
        require(Path(entry["file"]).name == entry["file"], "nonlocal entry")
        member = package / entry["file"]
        require(member.is_file() and not member.is_symlink(), "member must be a regular file")
        contents = member.read_bytes()
        require(len(contents) == entry["bytes"], "size mismatch: " + entry["file"])
        require(hashlib.sha256(contents).hexdigest() == entry["sha256"], "hash mismatch: " + entry["file"])

    scope = json.loads((package / "PINNED_SCOPE.json").read_bytes())
    outcome = json.loads((package / "OUTCOME.json").read_bytes())
    sources = json.loads((package / "SOURCE_INVENTORY.json").read_bytes())
    searches = json.loads((package / "SEARCH_LOG.json").read_bytes())
    require(scope["head"] == "bacae693a1f2a33c89565b0bd716620885831289", "head changed")
    require(scope["base"] == "f6caddda8f8be2cdb3e91494325d8f7f365bc3fc", "base changed")
    require(len(scope["files"]) == 8, "not all eight input files pinned")
    require({Path(x["path"]).name for x in scope["files"]} == {
        "ACCEPTANCE.json", "MANIFEST.json", "MATHEMATICAL_AUDIT.md", "PROOF.md",
        "README.md", "SOURCE_METADATA.json", "SOURCE_REVIEW.md", "STATUS.json",
    }, "input member set changed")
    proof = next(x for x in scope["files"] if x["path"].endswith("/PROOF.md"))
    require(proof["sha256"] == "791ec6c1f849840785afd8ce15e4460b396e108bc2b203d93993cfb0a6103340", "proof identity changed")
    require(outcome["verdict"] == "BOUNDED_NO_BLOCKING_PRIOR_THEOREM_RECOVERED", "unexpected verdict")
    require(outcome["exhaustive_novelty_certified"] is False, "unjustified exhaustive claim")
    require(outcome["mathematical_correctness_certified"] is False, "scope inflation")
    require(outcome["prior_even_cycle_mechanism_verified"] is True, "prior even-cycle credit omitted")
    require(outcome["prior_uniform_odd_cycle_threshold_verified"] is True, "prior uniform threshold omitted")
    require(outcome["prior_elementary_whisker_bound"] == "alpha > 24", "earlier consequence omitted")
    require(outcome["exact_pr_bounds_already_implied_by_verified_prior_theorem"] is False, "unsupported prior full implication")
    require(Fraction(17, 4) < 24 < 25, "bound ordering failed")
    require(Fraction(4, 3) < 2, "forest improvement ordering failed")

    x = Fraction(9, 4)
    exponential_upper = sum((x ** k / math.factorial(k) for k in range(13)), Fraction())
    exponential_upper += (x ** 13 / math.factorial(13)) / (1 - x / 14)
    require(exponential_upper == Fraction(191714244173193067, 20206532637491200), "exponential bound arithmetic")
    require(Fraction(19, 2) - exponential_upper == Fraction(247815882973333, 20206532637491200), "exponential margin arithmetic")
    require(exponential_upper < Fraction(19, 2), "exponential bound not strict")
    require(x * (Fraction(19, 2) + 1) == Fraction(189, 8) < 24, "cutoff arithmetic")
    require(Fraction(81, 4) < 24 and 2 - 2 * x / 24 == Fraction(29, 16) > Fraction(3, 2), "other source cutoffs")
    require(searches["negative_search_is_absence_certificate"] is False, "search overclaim")
    require(any(s.get("name") == "hhk2023.pdf" and s.get("sha256") == "ea5801394f0f50c8a6fd28296787091d9607b50deb7931ad3b3a068092d001cd" for s in sources["captures"]), "published dependency identity missing")
    require(any(s.get("name") == "owr2023.pdf" and s.get("sha256") == "320d7e903924249d1f57536cdf67491b3b5f89de8401c9a7c07800b09ee750c7" for s in sources["captures"]), "original source identity missing")
    print(json.dumps({
        "verdict": "PASS", "manifest_sha256": digest,
        "public_members_checked": len(entries), "pinned_inputs": len(scope["files"]),
        "exact_arithmetic_certificate": "exp(9/4) < 19/2; (9/4)(19/2+1) < 24",
        "read_only_offline": True, "literature_absence_certified": False,
        "mathematical_correctness_certified": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
