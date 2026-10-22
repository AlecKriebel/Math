# Independent audit bundle

Verdict: **scoped PASS; the general problem is not solved**.

Read `AUDIT_REPORT.md` for proof checks, exact boundaries, and the one optional wording clarification. `audit_summary.json` records the machine-readable disposition.

Reproduce the independent controls with Python 3.8 or later:

    python independent_verify.py --output /tmp/independent-results.json
    cmp /tmp/independent-results.json independent_results.json

Reproduce negative controls against the preserved author directory:

    python negative_controls.py --author-dir ../connected_20000826 --output /tmp/negative-results.json
    cmp /tmp/negative-results.json negative_control_results.json

Reproduce the author's original checks without changing its directory:

    python ../connected_20000826/verify.py --output /tmp/author-results.json
    cmp /tmp/author-results.json author_replay_results.json

Do not use optimized Python for the author program, which intentionally relies on assertions. The independent program also passes with `-O` because its conditions use explicit exceptions.

`input_integrity.json`, `dataset_integrity.json`, and `source_integrity.json` record independently recomputed byte metadata. `source_checks.json` records public URLs, inspected statements, and retrieval limits. `MANIFEST.json` covers the audit files except itself.

No source PDF, extract, screenshot, raw corpus record, or private coordination file is included. Computations are bounded controls and do not establish general connectedness.
