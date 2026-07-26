#!/usr/bin/env python3
"""Verify the publication-sized order-12 k=4 DoubleLex LRAT package.

The accepted LRAT is stored as a zstd stream because its uncompressed
228,381,671-byte form exceeds GitHub's per-file limit.  This verifier checks
all decisive bindings, decompresses into a private temporary directory,
checks the exact recovered bytes, and invokes the independently developed
LRAT checker on the exact accepted CNF.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile


PACKAGE = Path(__file__).resolve().parent
CAMPAIGN = PACKAGE.parents[1]

FORMULA = CAMPAIGN / "instances/order12_k4_connected_doublelex/instance.cnf"
COMPRESSED = PACKAGE / "proof.converted.lrat.zst"
PUBLICATION_MANIFEST = PACKAGE / "publication-manifest.json"
PUBLICATION_README = PACKAGE / "README.md"
CHECKER = CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check"
AUTHOR_CERTIFICATE = (
    CAMPAIGN
    / "certificates/order12_k4_doublelex_seed0_lrat/certificate.json"
)
AUTHOR_MANIFEST = (
    CAMPAIGN
    / "certificates/order12_k4_doublelex_seed0_lrat/artifact-manifest.json"
)
HOSTILE_REVIEW = (
    CAMPAIGN
    / "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/REVIEW.md"
)
HOSTILE_EVIDENCE = (
    CAMPAIGN
    / "reviews/order12_k4_doublelex_lrat_hostile_0814a4f4"
    / "hostile-evidence.json"
)

EXPECTED = {
    "publication_manifest": (
        PUBLICATION_MANIFEST,
        2_766,
        "409214887b0bae931af7cc1d03d0d1eaaf8de667f4adfa3d2e03d6b291c6f77b",
    ),
    "publication_readme": (
        PUBLICATION_README,
        2_720,
        "07f73c23dd194b7c3b06c9d4743ef3f637a1ff299a1a0d9d28bdb535da6f848f",
    ),
    "formula": (
        FORMULA,
        4_030_657,
        "14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7",
    ),
    "compressed_lrat": (
        COMPRESSED,
        64_288_636,
        "edc0f6b76bc96b2b26677f399566ae437cc47a6fc0cc921eaff81d77b72a50da",
    ),
    "checker": (
        CHECKER,
        36_520,
        "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
    ),
    "author_certificate": (
        AUTHOR_CERTIFICATE,
        15_723,
        "a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991",
    ),
    "author_manifest": (
        AUTHOR_MANIFEST,
        16_369,
        "846a646ba951569f50a76b562fdc8ec005dcf0f06ff57e48b4e3d4d330fbd607",
    ),
    "hostile_review": (
        HOSTILE_REVIEW,
        7_519,
        "fb95934b5d5acd75c9f6deb9142be3b903900f5abd02a5cc21d9884788f38395",
    ),
    "hostile_evidence": (
        HOSTILE_EVIDENCE,
        21_904,
        "2651f9d286582c068fb872acf862b82c4d4ab8e5fc07f6b99825b9335dd40b63",
    ),
}

LRAT_SIZE = 228_381_671
LRAT_SHA256 = (
    "0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263"
)


class VerificationError(RuntimeError):
    """Fail-closed publication verification error."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def require_regular_single_link(path: Path, label: str) -> os.stat_result:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise VerificationError(f"{label}: missing {path}") from error
    if not stat.S_ISREG(metadata.st_mode):
        raise VerificationError(f"{label}: not a regular file: {path}")
    if metadata.st_nlink != 1:
        raise VerificationError(
            f"{label}: expected one hard link, found {metadata.st_nlink}: {path}"
        )
    return metadata


def verify_binding(
    label: str, path: Path, expected_size: int, expected_sha256: str
) -> dict[str, object]:
    metadata = require_regular_single_link(path, label)
    if metadata.st_size != expected_size:
        raise VerificationError(
            f"{label}: size {metadata.st_size}, expected {expected_size}"
        )
    actual_sha256 = sha256_file(path)
    if actual_sha256 != expected_sha256:
        raise VerificationError(
            f"{label}: SHA-256 {actual_sha256}, expected {expected_sha256}"
        )
    try:
        display_path = str(path.relative_to(CAMPAIGN))
    except ValueError:
        display_path = f"<temporary>/{path.name}"
    return {
        "path": display_path,
        "size_bytes": metadata.st_size,
        "sha256": actual_sha256,
    }


def main() -> int:
    bindings = {
        label: verify_binding(label, *expected)
        for label, expected in EXPECTED.items()
    }

    zstd = shutil.which("zstd")
    if zstd is None:
        raise VerificationError(
            "zstd is required; install Zstandard 1.5.x and retry"
        )

    with tempfile.TemporaryDirectory(
        prefix="gamma-theta-doublelex-lrat-"
    ) as temporary:
        recovered = Path(temporary) / "proof.converted.lrat"
        with recovered.open("wb") as output:
            decompression = subprocess.run(
                [zstd, "-d", "--quiet", "--stdout", str(COMPRESSED)],
                check=False,
                stdout=output,
                stderr=subprocess.PIPE,
                timeout=600,
            )
        if decompression.returncode != 0:
            raise VerificationError(
                "zstd decompression failed: "
                + decompression.stderr.decode("utf-8", "replace")
            )
        if decompression.stderr:
            raise VerificationError(
                "zstd wrote unexpected stderr: "
                + decompression.stderr.decode("utf-8", "replace")
            )
        recovered_binding = verify_binding(
            "recovered_lrat", recovered, LRAT_SIZE, LRAT_SHA256
        )

        check = subprocess.run(
            [str(CHECKER), str(FORMULA), str(recovered)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=600,
        )
        stdout = check.stdout.decode("utf-8", "strict")
        if check.returncode != 0:
            raise VerificationError(
                f"lrat-check exited {check.returncode}: {stdout}"
            )
        if check.stderr:
            raise VerificationError(
                "lrat-check wrote unexpected stderr: "
                + check.stderr.decode("utf-8", "replace")
            )
        required_lines = {
            "c parsed a formula with 18381 variables and 115507 clauses",
            "c VERIFIED",
            (
                "c Added clauses = 471552.  Deleted clauses = 471427.  "
                "Max live clauses = 115507"
            ),
        }
        output_lines = set(stdout.splitlines())
        missing = sorted(required_lines - output_lines)
        if missing or stdout.splitlines().count("c VERIFIED") != 1:
            raise VerificationError(
                f"unexpected lrat-check success output; missing={missing!r}"
            )

    print(
        json.dumps(
            {
                "schema": "gamma-theta-doublelex-publication-verifier-v2",
                "verdict": "VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY",
                "bindings": bindings,
                "recovered_lrat": recovered_binding,
                "lrat_check": {
                    "exit_code": check.returncode,
                    "verified_marker_count": 1,
                    "stderr_bytes": len(check.stderr),
                },
                "claim_boundary": (
                    "This verifies UNSAT only for the exact DoubleLex CNF. "
                    "Transfer to graphs uses the separately reviewed "
                    "C-037/C-045 implication."
                ),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        OSError,
        subprocess.SubprocessError,
        UnicodeError,
        VerificationError,
    ) as error:
        print(f"REJECTED: {error}", file=os.sys.stderr)
        raise SystemExit(1)
