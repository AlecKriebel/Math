# External audit package

This directory is designed to let three specialists inspect the result without reading the full manuscript first.

1. `theorem_summary.pdf` - two-page statement, scope, and contributions.
2. `proof_skeleton.pdf` - five-page dependency-ordered proof skeleton.
3. `exact_reduction.md` - the complete NP-hardness construction in compact algebraic form.
4. `yes_partition_1_1.json` and `no_partition_1_2.json` - one small YES and one small NO source instance.
5. `minimal_verifier.py` - independent exact checker for the compact source-instance files and YES witness.
6. `likely_failure_points.md` - the three most load-bearing places to attack.
7. `priority_comparison.md` - precise separation from the closest prior work.
8. `limitations.md` - every important nonclaim.

Run:

```bash
python external_audit/minimal_verifier.py external_audit/yes_partition_1_1.json
python external_audit/minimal_verifier.py external_audit/no_partition_1_2.json
```
