#!/usr/bin/env python3
"""Black-box mutation audit of the hardened merger on final n=3 shards."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PYTHON = PROJECT.parent / ".venv/bin/python"
MERGER = PROJECT / "primary/merge_compact_probe_shards.py"
SUMMARIES = [PROJECT / "primary/certificates" /
             f"compact_probe_schema3_n3_compact_s{i}_summary.json"
             for i in range(4)]
PRIMARY = [PROJECT / "primary/certificates" /
           f"compact_probe_schema3_n3_compact_s{i}_replay.json"
           for i in range(4)]
INDEPENDENT = [HERE / "certificates" / f"independent_s{i}.json"
               for i in range(4)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(summaries, primary, independent, output):
    result = [str(PYTHON), str(MERGER)]
    for path in summaries:
        result += ["--summary", str(path)]
    for path in primary:
        result += ["--primary-replay", str(path)]
    for path in independent:
        result += ["--independent-replay", str(path)]
    result += ["--output", str(output)]
    return result


def execute(name, summaries, primary, independent, root):
    output = root / f"{name}_manifest.json"
    completed = subprocess.run(
        command(summaries, primary, independent, output), cwd=PROJECT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output_tail = completed.stdout[-2000:].replace(str(root), "<TEMP>")
    output_tail = re.sub(
        r"reviews/compact_probe_format/final_n3_cleanroom/tmp[^/\"']+",
        "<TEMP>", output_tail)
    return {
        "mutation": name,
        "accepted": completed.returncode == 0,
        "returncode": completed.returncode,
        "manifest_created": output.exists(),
        "output_tail": output_tail,
    }


def write_modified(source, target, mutate):
    payload = json.loads(source.read_text())
    mutate(payload)
    target.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    return target


def main():
    results = []
    with tempfile.TemporaryDirectory(dir=HERE) as temporary:
        root = Path(temporary)
        results.append(execute(
            "baseline", SUMMARIES, PRIMARY, INDEPENDENT, root))
        results.append(execute(
            "incomplete_shard_coverage", SUMMARIES[:3], PRIMARY[:3],
            INDEPENDENT[:3], root))
        results.append(execute(
            "duplicate_shard", [SUMMARIES[0], *SUMMARIES],
            [PRIMARY[0], *PRIMARY], [INDEPENDENT[0], *INDEPENDENT], root))
        results.append(execute(
            "missing_independent_replay", SUMMARIES, PRIMARY,
            INDEPENDENT[:3], root))

        wrong_sha = write_modified(
            INDEPENDENT[0], root / "wrong_summary_sha.json",
            lambda payload: payload.__setitem__("summary_sha256", "0" * 64))
        results.append(execute(
            "wrong_replay_summary_binding", SUMMARIES, PRIMARY,
            [wrong_sha, *INDEPENDENT[1:]], root))

        wrong_range = write_modified(
            INDEPENDENT[0], root / "wrong_range.json",
            lambda payload: payload.__setitem__("path_range", [0, 35]))
        results.append(execute(
            "wrong_independent_path_range", SUMMARIES, PRIMARY,
            [wrong_range, *INDEPENDENT[1:]], root))

        wrong_counts = write_modified(
            INDEPENDENT[0], root / "wrong_counts.json",
            lambda payload: payload["counts"].__setitem__(
                "ordinary_T", payload["counts"]["ordinary_T"] + 1))
        results.append(execute(
            "wrong_independent_counts", SUMMARIES, PRIMARY,
            [wrong_counts, *INDEPENDENT[1:]], root))

        wrong_status = write_modified(
            INDEPENDENT[0], root / "wrong_status.json",
            lambda payload: payload.__setitem__("status", "FALSE"))
        results.append(execute(
            "failed_independent_status", SUMMARIES, PRIMARY,
            [wrong_status, *INDEPENDENT[1:]], root))

        bad_schema = write_modified(
            SUMMARIES[0], root / "bad_schema_hash.json",
            lambda payload: payload.__setitem__(
                "schema_specification_sha256", "f" * 64))
        digest = sha(bad_schema)
        forged_primary = write_modified(
            PRIMARY[0], root / "forged_primary.json",
            lambda payload: payload.__setitem__("summary_sha256", digest))
        forged_independent = write_modified(
            INDEPENDENT[0], root / "forged_independent.json",
            lambda payload: payload.__setitem__("summary_sha256", digest))
        results.append(execute(
            "wrong_schema_specification", [bad_schema, *SUMMARIES[1:]],
            [forged_primary, *PRIMARY[1:]],
            [forged_independent, *INDEPENDENT[1:]], root))

    expected = {"baseline": True}
    for row in results:
        row["expected_acceptance"] = expected.get(row["mutation"], False)
        row["meets_expectation"] = (
            row["accepted"] == row["expected_acceptance"])
    unexpected = [row["mutation"] for row in results
                  if not row["meets_expectation"]]
    payload = {
        "schema": "compact-probe-final-n3-merger-mutations-v1",
        "status": "VERIFIED" if not unexpected else "FALSE",
        "scope": (
            "Black-box coverage, replay binding, range, count, status, and "
            "schema commitments. Relation semantics are tested separately "
            "by mutation_tests.py."),
        "merger": str(MERGER.relative_to(PROJECT)),
        "merger_sha256": sha(MERGER),
        "summary_sha256": [sha(path) for path in SUMMARIES],
        "primary_replay_sha256": [sha(path) for path in PRIMARY],
        "independent_replay_sha256": [sha(path) for path in INDEPENDENT],
        "results": results,
        "unexpected_results": unexpected,
        "implementation": str(Path(__file__).relative_to(PROJECT)),
        "implementation_sha256": sha(Path(__file__)),
    }
    output = HERE / "certificates/merger_mutations.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "tests": len(results),
        "unexpected": unexpected,
        "output": str(output.relative_to(PROJECT)),
        "output_sha256": sha(output),
    }, sort_keys=True))
    return 0 if not unexpected else 1


if __name__ == "__main__":
    sys.exit(main())
