"""Read-only replay of actual Git and sealed priority-input authentication."""
from pathlib import Path
from hashlib import sha256
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
REPO = HERE.parents[4]
HEAD = "7d3adb0e500b0414a49a449e7981d34ade329427"
PROOF = "unsolved_math_prioritization/attempts/6000001/public/PROOF.md"
FAMILIES = {
    "classical_priority": "08b2a8ed4393b41b96ae894dcfa2398b62d138417976691f2533d5c34cc3baa6",
    "recent_priority": "b7c325b423cf92d6fc33789d10a8dc8d17ff578dae83144aaa8ec87af7c5617d",
}


def require(test, message):
    if not test:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def main():
    require(sys.flags.optimize == 0, "Run the normal Python runtime for this receipt")
    require(git("branch", "--show-current").decode().strip() == "main", "branch")
    require(sha256((AUDIT / "PRIORITY_FALSIFIER_CHARTER.md").read_bytes()).hexdigest() ==
            "b2a8c3e3f53bbf1cbe3c00ebc3af65f5a6d48acc8aa4a9685588d15e3e67d34b", "charter")
    original = json.loads((AUDIT / "ORIGINAL_SNAPSHOT.json").read_text())
    require(len(original["files"]) == 33, "original payload count")
    for path, digest in original["files"].items():
        require(sha256(git("show", HEAD + ":" + path)).hexdigest() == digest, path)
    proof = git("show", HEAD + ":" + PROOF)
    require(len(proof) == 17635 and sha256(proof).hexdigest() ==
            "a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2", "proof")
    rows = [row for row in git("show", HEAD + ":unsolved_math_prioritization/QUEUE.md").decode().splitlines()
            if "| 6000001 / AMR-059-0001 |" in row]
    require(len(rows) == 1 and "| claimed_solved | 4/5 |" in rows[0], "immutable target row")
    counts = {}
    for family, digest in FAMILIES.items():
        directory = HERE.parent / family
        raw = (directory / "MANIFEST.json").read_bytes()
        require(sha256(raw).hexdigest() == digest, family + " external seal")
        manifest = json.loads(raw)
        payloads = manifest.get("files", manifest.get("payloads"))
        require(len(payloads) == 10, family + " count")
        for item in payloads:
            data = (directory / item["path"]).read_bytes()
            require(len(data) == item["bytes"] and sha256(data).hexdigest() == item["sha256"], item["path"])
        counts[family] = len(payloads)
    print(json.dumps({"actual_git_original_payloads": 33, "family_payload_counts": counts,
                      "immutable_target_status": "claimed_solved", "declared_budget": "4/5",
                      "historical_native_events": "absent/not certified", "new_proof_responses": 0,
                      "python_optimization_level": sys.flags.optimize, "result": "PASS"}))


if __name__ == "__main__":
    main()
