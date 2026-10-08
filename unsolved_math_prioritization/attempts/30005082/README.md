# Higher-Grassmannian partial boundaries: report and audit

Read ACCEPTANCE.md, REPORT.md, CORRECTION.md and INDEPENDENT_AUDIT.md. STATUS.json records exhausted 5/5 with the global comparison unfinished. The HN formula-defect claim is restricted to arXiv:2107.04264v2. No actual Escobar–Harada counterexample or global characterization is claimed.

Only authored mathematical material, safe standard-library checks, public source metadata and verification evidence are included. The full superseded original, source bodies, dataset contents, private logs and queue files are omitted. The historical attribution patch is superseded by the byte-identical corrected report.

Authenticate BOOTSTRAP.py using a SHA-256 value published outside this directory before execution, for example the draft PR body. That bootstrap pins the verifier, controls harness, and manifest. The manifest binds every remaining delivered file, including acceptance and pre-seal receipts. A self-consistent replacement manifest does not replace the external trust anchor.

For portable verification, use a directory owned by UID 1000. Set all files to 0444 and the directory to 0555, then run as UID=EUID=1000:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B -O BOOTSTRAP.py .
    python -I -S -B -OO BOOTSTRAP.py .

Use the authenticated --controls entry for integrity, schema/scope, direct comparator and hostile-environment tests:

    python -I -S -B BOOTSTRAP.py --controls .
    python -I -S -B -O BOOTSTRAP.py --controls .
    python -I -S -B -OO BOOTSTRAP.py --controls .

Actual write-denial probes are required, not only permission-bit checks. Semantic mutations run in disposable copies. run_math.py and run_independent.py wrap the unchanged authored algorithms in mode-specific output envelopes. The latter also compares the candidate's public functions against independently computed values. References contain full stdout and stderr; output normalization is NONE. No shell, network, third-party dependency or packet write is used by the portable validator.

CHECK_RUNS.json records fresh reference capture. PREPARATION_CONTROLS and PREPARATION_STAGE record a historical pre-seal run; their pins are not the final trust anchor. The final seal binds those files, and final evidence is recorded externally to avoid circular self-hashes.

Original-report replay, historical patch application, source-body replay, source-hash recheck, dataset replay, and formal proof-assistant verification are NOT_RUN. Finite regression checks do not establish all cited geometric results.
