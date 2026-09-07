#!/usr/bin/env python3
"""Fail closed on final TeX logs used to accept release PDFs."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


FORBIDDEN = (
    ("undefined references", re.compile(r"undefined references", re.I)),
    ("undefined citations", re.compile(r"undefined citations", re.I)),
    ("undefined reference warning", re.compile(r"LaTeX Warning: Reference", re.I)),
    ("undefined citation warning", re.compile(r"LaTeX Warning: Citation", re.I)),
    ("overfull box", re.compile(r"Overfull \\[hv]box", re.I)),
)


def problems(path: Path) -> list[str]:
    if not path.is_file():
        return ["missing log"]
    if path.stat().st_size == 0:
        return ["empty log"]
    text = path.read_text(encoding="utf-8", errors="replace")
    return [label for label, pattern in FORBIDDEN if pattern.search(text)]


def audit(paths: list[Path]) -> int:
    failures = [(path, problems(path)) for path in paths]
    failures = [(path, issues) for path, issues in failures if issues]
    if failures:
        for path, issues in failures:
            print(
                f"final TeX log audit failed: {path}: {', '.join(issues)}",
                file=sys.stderr,
            )
        return 1
    print(f"FINAL_TEX_LOG_AUDIT_PASS logs={len(paths)}")
    return 0


def journal_negative_control() -> int:
    """Exercise the CLI parser; release wiring is audited separately in source."""

    with tempfile.TemporaryDirectory(prefix="journal-log-gate-") as directory:
        root = Path(directory)
        logs = [
            root / "journal_manuscript.log",
            root / "journal_supplement.log",
            root / "journal_cover_letter.log",
        ]
        for path in logs:
            path.write_text(
                "This is pdfTeX.\nOutput written on accepted.pdf (1 page).\n",
                encoding="utf-8",
            )
        command = [sys.executable, str(Path(__file__).resolve()), *map(str, logs)]
        clean = subprocess.run(command, capture_output=True, text=True, check=False)
        if clean.returncode != 0:
            print("journal log negative control could not accept clean logs", file=sys.stderr)
            return 1
        print("CLEAN_JOURNAL_LOG_CLI_ACCEPTANCE_PASS logs=3")
        for box_kind in ("hbox", "vbox"):
            logs[1].write_text(
                "This is pdfTeX.\n"
                f"Overfull \\{box_kind} (12.0pt too wide) at lines 1--2\n",
                encoding="utf-8",
            )
            mutant = subprocess.run(command, capture_output=True, text=True, check=False)
            if mutant.returncode == 0 or "overfull box" not in mutant.stderr:
                print(
                    f"journal log CLI gate accepted the overfull-{box_kind} mutant",
                    file=sys.stderr,
                )
                return 1
            print(f"JOURNAL_OVERFULL_{box_kind.upper()}_CLI_REJECTION_PASS")
        logs[1].write_text(
            "This is pdfTeX.\n"
            "Overfull \\hbox (33.31522pt too wide) at lines 1--2\n",
            encoding="utf-8",
        )
        candidate = root / "candidate_journal.pdf"
        destination = root / "accepted_journal.pdf"
        candidate.write_bytes(b"synthetic journal candidate\n")
        boundary = subprocess.run(
            [
                "bash",
                "-ceu",
                '"$1" "$2" "$3" "$4" "$5"; cp "$6" "$7"',
                "journal-copy-boundary",
                sys.executable,
                str(Path(__file__).resolve()),
                *map(str, logs),
                str(candidate),
                str(destination),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if boundary.returncode == 0 or destination.exists():
            print("journal warning did not stop the simulated copy boundary", file=sys.stderr)
            return 1
        print("SIMULATED_JOURNAL_WARNING_PREVENTS_COPY_PASS")
    print("JOURNAL_LOG_GATE_CLI_MUTATION_PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="*", type=Path)
    parser.add_argument(
        "--journal-negative-control",
        action="store_true",
        help="prove that clean journal logs pass and an overfull mutant fails",
    )
    args = parser.parse_args()
    if args.journal_negative_control:
        if args.logs:
            parser.error("--journal-negative-control does not accept log paths")
        return journal_negative_control()
    if not args.logs:
        parser.error("provide at least one final TeX log")
    return audit(args.logs)


if __name__ == "__main__":
    raise SystemExit(main())
