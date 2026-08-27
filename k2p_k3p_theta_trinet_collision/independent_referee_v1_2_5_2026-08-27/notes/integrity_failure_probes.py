#!/usr/bin/env python3
"""Negative controls for the packet replay driver's fail-closed boundary."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile


AUDIT = Path(__file__).resolve().parents[1]
PACKET = (
    AUDIT
    / "packet_copy"
    / "k2p-k3p-theta-ai-referee-v1.2.5"
)


def run_case(name: str, mutation, diagnostic: str) -> None:
    with tempfile.TemporaryDirectory(prefix="v125-integrity-") as raw:
        copy = Path(raw) / "packet"
        shutil.copytree(PACKET, copy, symlinks=True)
        mutation(copy)
        completed = subprocess.run(
            ["bash", str(copy / "RUN_REFEREE_REPLAY.sh")],
            cwd=copy,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=120,
        )
    if completed.returncode == 0:
        raise RuntimeError(f"{name}: corrupted packet unexpectedly passed")
    if diagnostic not in completed.stdout:
        raise RuntimeError(
            f"{name}: expected diagnostic {diagnostic!r}\n{completed.stdout}"
        )
    print(f"PASS  {name}: {diagnostic}")


def alter_byte(packet: Path) -> None:
    path = packet / "AI_REFEREE_PROMPT.md"
    path.write_bytes(path.read_bytes() + b"\n")


def add_file(packet: Path) -> None:
    (packet / "UNMANIFESTED.txt").write_text("hostile extra file\n")


def delete_file(packet: Path) -> None:
    (packet / "REFEREE_REPORT_TEMPLATE.md").unlink()


def add_symlink(packet: Path) -> None:
    (packet / "materials" / "hostile-link").symlink_to("verify.py")


def main() -> None:
    run_case("manifest-listed byte change", alter_byte, "SHA-256 mismatch")
    run_case("unmanifested regular file", add_file, "Packet path-set mismatch")
    run_case("missing manifest-listed file", delete_file, "Packet path-set mismatch")
    run_case("symbolic link", add_symlink, "Symbolic link rejected")
    print("ALL PACKET INTEGRITY FAILURE PROBES PASSED")


if __name__ == "__main__":
    main()

