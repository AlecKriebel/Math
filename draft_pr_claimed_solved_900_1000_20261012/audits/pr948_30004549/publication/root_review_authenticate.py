#!/usr/bin/env python3
"""Authenticate a sealed whole review and current candidate before report intake."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", required=True)
    parser.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    if args.round not in ("06", "07", "08", "09"):
        raise ValueError("Explicit current review round required")
    program = Path(__file__).resolve().parents[3]
    audit = program / "audits/pr948_30004549"
    review = audit / ("reviews/full_package_" + args.round)
    core = program / "accept_pr948.py"
    core_bytes = core.read_bytes()
    if hashlib.sha256(core_bytes).hexdigest() != "3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823":
        raise ValueError("Pinned current operational core changed")
    namespace = {"__file__": str(core), "__name__": "_root_sealed_review_auth_"}
    exec(compile(core_bytes, str(core), "exec", dont_inherit=True, optimize=0), namespace)
    raw = namespace["read_regular"](review / "MANIFEST.json")
    if hashlib.sha256(raw).hexdigest() != args.manifest_sha256:
        raise ValueError("External review seal mismatch")
    manifest = namespace["strict_json"](raw)
    files, allowed = manifest["files"], manifest["explicit_public_allowlist"]
    if type(files) is not dict or type(allowed) is not list or len(allowed) != len(set(allowed)) or set(files) != set(allowed) or "MANIFEST.json" in files:
        raise ValueError("Exact explicit review closure required")
    for name, pin in files.items():
        if type(name) is not str or PurePosixPath(name).is_absolute() or PurePosixPath(name).as_posix() != name or any(p in ("", ".", "..") for p in name.split("/")):
            raise ValueError("Unsafe review payload path")
        namespace["read_regular"](review / name, pin=pin)
    context = namespace["capture_inventory"]("500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002")
    freeze_pin = "1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c"
    freeze = namespace["freeze_check"]((audit / "preprint/FREEZE.json").read_bytes(), freeze_pin, context)
    originals = namespace["original_check"]()
    if len(originals) != 24:
        raise ValueError("Original24 closure mismatch")
    output = {
        "schema": "pr948-root-sealed-entire-review-preintake-authentication-v1",
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "PASS_BYTES_BEFORE_FULL_REPORT_INTAKE",
        "round": args.round,
        "review_manifest_sha256": args.manifest_sha256,
        "public_payload_count": len(files),
        "public_payloads": files,
        "freeze_sha256": freeze_pin,
        "current_frozen_files": len(freeze["files"]),
        "current_external_evidence": len(freeze["evidence_files"]),
        "operations_inventory_sha256": context["inventory_sha256"],
        "original24": originals,
        "executed_root_authenticator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "All current seal payloads, frozen candidate, external evidence, all seven current operations and original24 authenticated before interpreting full report. This is integrity evidence, not an acceptance or mathematical verdict.",
    }
    target = audit / ("ROOT_FULL" + args.round + "_REPORT_AUTHENTICATION.json")
    with target.open("x") as stream:
        json.dump(output, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"status": output["status"], "round": args.round, "payloads": len(files), "utc": output["utc"]}))

if __name__ == "__main__":
    main()

