"""Check native original PR packet identity, actual source pair, and attempt ledger."""
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import json
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[2]
PREFIX = "unsolved_math_prioritization/attempts/9500008/"
MANIFEST = json.loads((AUDIT / "snapshot_manifest.json").read_text())


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


def validate(packet):
    # Actual corpus full-record equality precedes original byte identity checks.
    p = load(packet / "source_record.json")
    r = load(packet / "prior_report.json")
    require(p == load(HERE / "raw_source_record.json"), "source full record differs from actual pinned corpus")
    require(r == load(HERE / "raw_prior_report.json"), "prior full report differs from actual present corpus report")
    qpath = ROOT / "unsolved_math_prioritization/queue.py"
    spec = importlib.util.spec_from_file_location("queue_readonly_packet", qpath)
    queue = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(queue)
    score = queue.score(p, r, load(ROOT / "unsolved_math_prioritization/policy.json"))
    readiness = load(packet / "readiness.json")
    require(score["statement_hash"] == readiness["statement_hash"], "literal statement hash mismatch")
    require(score["review_hash"] == readiness["review_hash"], "pure source/report pair hash mismatch")
    turns = load(packet / "turns.json")
    budget = readiness["budget"]
    require(turns["id"] == readiness["id"] == p["id"] == 9500008, "numeric identity mismatch")
    require(turns["count"] == len(turns["attempts"]) == budget["used"], "incoherent local attempt count")
    require(budget["maximum_substantive_attempts"] == 5, "five-attempt limit changed")
    require(0 <= turns["count"] <= budget["maximum_substantive_attempts"], "attempt limit exceeded")
    require([a["number"] for a in turns["attempts"]] == list(range(1, turns["count"] + 1)), "nonsequential attempt numbers")
    start = datetime.datetime.fromisoformat(budget["start_utc"].replace("Z", "+00:00"))
    deadline = datetime.datetime.fromisoformat(budget["deadline_utc"].replace("Z", "+00:00"))
    literature = datetime.datetime.fromisoformat(readiness["literature_checked_at"])
    require((deadline - start).total_seconds() == 7200 and start < literature < deadline, "original two-hour ledger bounds differ")
    require(turns["count"] == 2, "original local ledger no longer records two attempts")
    require([a["outcome"] for a in turns["attempts"]] == ["unresolved", "partial"], "original unresolved/partial outcomes changed")
    require(readiness["outcome"] == "unresolved", "full target disposition changed")
    verdict = load(packet / "review/verdict.json")
    require(verdict["full_problem_solved"] is False, "unproved full solution promoted")
    require(sha((packet / "PARTIAL.md").read_bytes()) == turns["attempts"][1]["sha256"] == readiness["reviewed_artifact_sha256"] == verdict["artifact_sha256"], "artifact seals disagree")
    expected = {x["path"]: x for x in MANIFEST["files"]}
    actual = {str(x.relative_to(packet)) for x in packet.rglob("*") if x.is_file()}
    require(actual == set(expected), "original packet member set mismatch")
    for rel, item in expected.items():
        b = (packet / rel).read_bytes()
        require(len(b) == item["size"] and sha(b) == item["sha256"], "original byte identity mismatch: " + rel)
        native = subprocess.check_output(["git", "show", MANIFEST["head"] + ":" + PREFIX + rel], cwd=ROOT)
        require(b == native, "native original Git blob differs: " + rel)
    diff = (AUDIT / "pr_input/diff.patch").read_bytes()
    require(len(diff) == MANIFEST["diff_bytes"] == 49891 and sha(diff) == MANIFEST["diff_sha256"], "original diff seal differs")
    native_diff = subprocess.check_output(["git", "diff", MANIFEST["base"], MANIFEST["head"]], cwd=ROOT)
    require(diff == native_diff, "native original full diff differs")
    native_paths = subprocess.check_output(["git", "diff", "--name-only", MANIFEST["base"], MANIFEST["head"]], cwd=ROOT, text=True).splitlines()
    require(native_paths == MANIFEST["changed_paths"] and len(native_paths) == 17, "native original seventeen paths differ")
    return {"passed": True, "original_members": len(actual), "changed_paths": len(native_paths),
            "local_ledger": "2/5 unresolved + partial", "raw_pair_and_statement_hashes": score,
            "scope": "Native original PR identity and actual source/accounting; no Brownian-law proof inferred from byte checks."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", nargs="?", type=Path, default=AUDIT / "source_snapshot")
    args = parser.parse_args()
    try:
        out = validate(args.packet.resolve())
    except Exception as exc:
        print(json.dumps({"passed": False, "reason": str(exc)}, indent=2))
        raise SystemExit(1)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
