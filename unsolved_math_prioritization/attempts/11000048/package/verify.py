#!/usr/bin/env python3
"""Offline integrity and finite scaling diagnostics, not a proof of the source theorem."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json


def main():
    root = Path(__file__).resolve().parent
    record = json.loads((root / "source_record.json").read_text())
    assert record["id"] == "11000048"
    assert record["problem_number"] == "AMR-109-0048"
    assert record["rank"] == 449
    assert record["proposed_outcome"] == "already_solved"
    assert record["turns_used"] == 0
    assert record["novelty_claim"] is False
    events = [json.loads(line) for line in
              (root / "turns.jsonl").read_text().splitlines() if line.strip()]
    assert events and all(event["substantive_turn"] is False for event in events)
    assert all(event["turns_used"] == 0 for event in events)
    assert len(record["sources"]) == 3
    assert record["sources"][1]["doi"] == "10.1007/s00039-010-0049-8"
    # Exact arithmetic checks of (delta + 1)/r < epsilon for the explicit
    # threshold r = floor((delta + 1)/epsilon) + 1. These finite cases merely
    # guard arithmetic/transcription; the all-scale argument is in the prose.
    checks = 0
    for delta in [Fraction(0), Fraction(1, 3), Fraction(1), Fraction(7, 2), Fraction(100)]:
        for epsilon in [Fraction(1), Fraction(1, 2), Fraction(1, 10), Fraction(1, 1000)]:
            ratio = (delta + 1) / epsilon
            threshold = ratio.numerator // ratio.denominator + 1
            for scale in [threshold, threshold + 1, 2 * threshold, 100 * threshold]:
                assert (delta + 1) / scale < epsilon
                checks += 1
    manifest_path = root / "MANIFEST.json"
    verified_files = []
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for filename, digest in manifest["sha256"].items():
            assert hashlib.sha256((root / filename).read_bytes()).hexdigest() == digest, filename
            verified_files.append(filename)
    forbidden = [p.name for p in root.rglob("*") if p.is_file()
                 and p.suffix.lower() in {".pdf", ".png", ".jpg", ".sqlite"}]
    assert not forbidden, forbidden
    print(json.dumps({"status": "pass", "substantive_turns": 0,
                      "exact_scaling_diagnostics": checks,
                      "manifest_files_verified": verified_files,
                      "limits": "No mechanical verification of the cited period or reduction theory."}, indent=2))


if __name__ == "__main__":
    main()
