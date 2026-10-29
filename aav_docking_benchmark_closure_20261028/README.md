# AAV docking benchmark: closure assessment

Start with [CLOSURE_PLAN.md](CLOSURE_PLAN.md). This folder assesses how to finish the study; it does not report newly measured docking or binding performance.

Upstream: Wyattkriebel/AAV-Docking-Benchmark at commit e9d39e3ef1c58647c2bf9dea7dfc90f823198791. SOURCE_IDENTITY.json and SOURCE_TREE.json record the inspected version and file hashes. The three independent assessments and FINAL_REVIEW.md provide supporting checks.

## Replay the static audit

The local snapshot is excluded from publication to avoid duplicating upstream structures. Download the [pinned upstream source archive](https://github.com/Wyattkriebel/AAV-Docking-Benchmark/archive/e9d39e3ef1c58647c2bf9dea7dfc90f823198791.zip) and extract its contents into this folder's snapshot/ directory. Copy SOURCE_TREE.json to snapshot/TREE.json. Run `python3 code_audit/check_snapshot.py` from this folder. The recorded audit omitted upstream .gitignore; a full downloaded archive can include it. Its presence does not change the scientific checks.

The checker uses only Python's standard library. It does not execute the upstream docking program or validate experimental structures. Check its output against code_audit/checks.json and SNAPSHOT_VERIFICATION.json.

No external outreach was prepared or initiated. No upstream repository files were changed.
