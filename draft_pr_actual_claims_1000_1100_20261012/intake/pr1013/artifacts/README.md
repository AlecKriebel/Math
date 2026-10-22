# Two-loop SLE: accepted scoped partial progress

Read ACCEPTANCE.md, REPORT.md and AUDIT.md. Six scoped propositions and elementary consequences of a credited ARS theorem survive independent audit with the stated hypothesis/scope repairs. The full embedded-pair comparison remains unresolved after 5/5 substantive approaches.

REPORT.md, AUDIT.md, CORRECTIONS.md, REPORT_CORRECTIONS.patch, the safe check_exact.py and audit_exact.py, and public source metadata are copied exactly from the accepted corrected derivative. Historical acceptance and prior-record hashes are separately labeled. The full old report, historical harnesses/logs, source PDFs/text, corpora, private coordination and QUEUE are excluded. No mathematical extension is attempted during packaging.

Authenticate BOOTSTRAP.py against its SHA-256 supplied outside this directory before execution. The bootstrap binds the manifest, verifier and controls; the manifest binds every remaining file, including acceptance and pre-seal receipts. Set all delivered files to 0444 and the directory to 0555; execute as actual UID=EUID=1000:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B BOOTSTRAP.py --controls .

Repeat with -O and -OO before BOOTSTRAP.py. Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0 were used. Installed Python/dependency implementations are trusted and not byte-pinned by this delivery. DEPENDENCY_RUNNER.py adds only the interpreter's installed purelib directory without enabling site or .pth startup processing; version checks must pass. This is not a hermetic dependency audit.

Whole stdout/stderr is compared with mode-specific pinned references byte-for-byte; all three outputs also receive recursive type-exact JSON comparison. Stable virtual compilation labels avoid generating identifying paths; no output normalization is performed. Semantic mutants and the intentional failure are checked at their intended conditions. The 297 high-precision numerical diagnostics are separate from 42,097 independent exact mathematical checks.

CHECK_RUNS.json captures fresh reference executions. PREPARATION_STAGE/RECEIPT/CONTROLS describe the pre-seal stage. The final seal authenticates those files; final external receipts bind the whole final packet and are kept outside it to avoid circular self-hashes. VERIFICATION.md lists tested boundaries and NOT_RUN stages.
