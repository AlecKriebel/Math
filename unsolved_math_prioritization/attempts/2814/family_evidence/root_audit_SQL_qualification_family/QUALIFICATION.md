# PR40 actual SQLite connection qualification

The retained original audit and its actual root replay used SQLite URI
`mode=ro` only. The helper did not request `immutable=1` and did not execute
`PRAGMA query_only`. Any earlier process wording that attributes those
additional settings to this audit must be read with this correction.

The exact source is `primary_scope_family/audit_original.py`, SHA256
`5b4f6e0bfd5be4381057899d17dd7310b5957742b87ddfeecd57e9d97bd8489f`.
Line20 calls
`sqlite3.connect('file:'+str(sqlpath)+'?mode=ro',uri=True)` and performs only
the two SQL SELECT queries shown in SOURCE_READ_CHECKS.json. Line47 records
`raw_corpus.sql_open_mode` as `ro`. The actual root CAPTURE.json, SHA256
`f3be854e90fb2fda20fcbc57b1e18a5f888fef85f7b299dbf53cb93841baecbd`,
binds that exact helper and successful exit0. Its actual RESULT.json, SHA256
`80ead0ed19cedba57c7440d79b77b51ed913e28d8ff3192b490d9e5c69416f8a`,
explicitly reports `raw_corpus.sql_open_mode: "ro"`.

This is a read-only SQLite connection. The exact 149,266,659-byte raw corpus
and all15,458 SQL payload/report-join comparisons remain supported by the
retained source and actual result. No assertion that this run enabled the two
additional settings is supported. A later separately captured audit may use
them, but must not retroactively change the configuration of this run.

This adjacent note corrects present interpretation only. The closed97-member
primary family is unchanged; its REPORT.md already describes read-only SQL.
This task found no literal `immutable` or `query_only` assertion in that closed
family and does not falsely attribute one to its report. The current package
must bind this qualification alongside the actual source/capture/result.
No helper or new database query was executed for this note, and no
mathematical defect, new solution, paper or DOI follows from the correction.
Original effort stays0/5; new substantive and audit attempts remain0.
