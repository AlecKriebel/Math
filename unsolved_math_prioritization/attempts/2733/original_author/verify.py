#!/usr/bin/env python3
"""Fail-closed integrity and exact-arithmetic checks, not a geometry prover."""
import hashlib
import json
from pathlib import Path
import re
import sys

MEMBERS = {
    "README.md", "PROOF.md", "REPORT.md", "APPROACH_LOG.md", "STATUS.json",
    "SOURCE_AUDIT.json", "ARITHMETIC_CERTIFICATE.json", "verify.py",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Nonfinite JSON constant: " + value)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def add(*polys):
    result = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(poly, coefficient):
    return {m: coefficient * c for m, c in poly.items() if coefficient * c}


def multiply(a, b):
    result = {}
    for am, ac in a.items():
        for bm, bc in b.items():
            monomial = tuple(sorted(am + bm))
            result[monomial] = result.get(monomial, 0) + ac * bc
    return {m: c for m, c in result.items() if c}


def pi_polynomial(value):
    require(set(value) == {"pi", "constant"}, "Bad pi polynomial keys")
    require(all(type(v) is int for v in value.values()), "Noninteger coefficient")
    return add({("pi",): value["pi"]}, {(): value["constant"]})


def named_polynomial(value):
    require(all(type(v) is int for v in value.values()), "Noninteger coefficient")
    return add({tuple(sorted(k.split("*"))): v for k, v in value.items()})


def main():
    require(len(sys.argv) <= 2, "Usage: verify.py [package_directory]")
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parent
    require(root.is_dir() and not root.is_symlink(), "Not a real package directory")
    children = list(root.iterdir())
    require({p.name for p in children} == MEMBERS | {"MANIFEST.json"},
            "Unexpected or missing package member")
    require(all(p.is_file() and not p.is_symlink() for p in children),
            "All members must be regular nonsymlink files")

    manifest = read_json(root / "MANIFEST.json")
    require(set(manifest) == {"schema_version", "scope", "members"},
            "Unexpected manifest schema")
    require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 1,
            "Wrong manifest version")
    require(manifest["scope"] == "Authored analysis and public verification metadata only",
            "Wrong manifest scope")
    entries = manifest["members"]
    require(isinstance(entries, list) and len(entries) == len(MEMBERS),
            "Wrong manifest member count")
    seen = set()
    for entry in entries:
        require(isinstance(entry, dict) and set(entry) == {"name", "bytes", "sha256"},
                "Malformed manifest entry")
        name = entry["name"]
        require(isinstance(name, str) and name in MEMBERS and name not in seen,
                "Invalid or duplicate member name")
        seen.add(name)
        require(type(entry["bytes"]) is int and entry["bytes"] > 0,
                "Invalid byte count")
        require(isinstance(entry["sha256"], str) and
                re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None,
                "Invalid SHA-256")
        raw = (root / name).read_bytes()
        require(len(raw) == entry["bytes"], "Byte count mismatch: " + name)
        require(hashlib.sha256(raw).hexdigest() == entry["sha256"],
                "Hash mismatch: " + name)
    require(seen == MEMBERS, "Manifest coverage mismatch")

    status = read_json(root / "STATUS.json")
    require(type(status.get("problem_id")) is int and status["problem_id"] == 2733,
            "Wrong problem ID")
    require(status.get("problem_number") == "KP-1.74", "Wrong problem number")
    require(status.get("status") == "PARTIAL_FORMULATION_AUDIT_STALLED", "Wrong outcome")
    require(status.get("approaches_used") == 2 and status.get("approach_limit") == 5,
            "Wrong approach count")
    require(status.get("full_resolution") is False and status.get("novelty_claim") is False,
            "Overclaim in status")
    require(status.get("intended_nontrivial_part_a") == "unresolved" and
            status.get("part_b") == "unresolved", "Intended-problem overclaim")

    cert = read_json(root / "ARITHMETIC_CERTIFICATE.json")
    require(cert.get("schema_version") == 1, "Wrong certificate version")
    require(cert.get("part_b_proved") is False and
            cert.get("intended_part_a_proved") is False, "Certificate overclaim")
    unit = pi_polynomial(cert["unknot_ropelength"])
    saving = pi_polynomial(cert["strong_saving"])
    rhs = add(scale(unit, 2), scale(saving, -1))
    require(rhs == pi_polynomial(cert["unknot_pair_rhs"]), "Incorrect unknot RHS")
    margin = add(unit, scale(rhs, -1))
    require(margin == pi_polynomial(cert["literal_violation_margin"]),
            "Incorrect literal violation margin")
    require(unit == {("pi",): 2} and saving == {("pi",): 4, (): -4},
            "Wrong normalization or conjectured constant")
    require(type(cert["pi_strict_lower_bound"]) is int and
            cert["pi_strict_lower_bound"] == 3, "Unexpected assumed pi bound")
    require(margin[("pi",)] > 0 and
            margin[("pi",)] * cert["pi_strict_lower_bound"] + margin.get((), 0) > 0,
            "Positivity was not certified from the stated classical pi bound")

    chain = cert["chain_ropelength"]
    require(chain == {"m_pi": 4, "m": 4, "constant": -8}, "Wrong prior chain formula")
    one = {(): 1}
    pi = {("pi",): 1}
    m, n = {("m",): 1}, {("n",): 1}
    def chain_value(x):
        return add(scale(multiply(x, pi), chain["m_pi"]),
                   scale(x, chain["m"]), {(): chain["constant"]})
    deficit = add(chain_value(m), chain_value(n),
                  scale(chain_value(add(m, n, scale(one, -1))), -1))
    require(deficit == pi_polynomial(cert["chain_saving"]), "Incorrect chain subtraction")

    S, epsilon, s = {("S",): 1}, {("epsilon",): 1}, {("s",): 1}
    delta, c = {("delta",): 1}, {("c",): 1}
    denom = add(one, scale(delta, -1))
    length = add(S, epsilon, scale(s, -1))
    numerator = add(multiply(S, denom), scale(length, -1))
    require(numerator == named_polynomial(cert["splice_numerator_polynomial"]),
            "Incorrect splice identity")
    target = add(numerator, scale(multiply(c, denom), -1))
    require(target == named_polynomial(cert["target_numerator_polynomial"]),
            "Incorrect target-saving inequality expansion")

    audit = read_json(root / "SOURCE_AUDIT.json")
    require(audit.get("problem_id") == 2733, "Wrong source audit ID")
    require(audit["selected_record_verification"]["statement_match"] is True and
            audit["selected_record_verification"]["pair_match"] is True,
            "Source identity not marked verified")
    require(all(item["redistributed"] is False for item in audit["pdf_retrievals"]),
            "Source redistribution flag")
    print(json.dumps({"result": "PASS", "problem_id": 2733,
                      "checked_payload_files": len(MEMBERS),
                      "optimized_mode": not __debug__,
                      "scope": "Integrity and exact arithmetic only; no geometry proof",
                      "intended_part_a": "unresolved", "part_b": "unresolved"},
                     sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
