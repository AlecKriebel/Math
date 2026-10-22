# Reproduce the independent cycle-set audit

Read AUDIT.md and ACCEPTANCE.json first. The accepted disposition is unsolved, five approaches used, with independently reviewed restricted arguments. The upper assertion is prior work. No formal proof or novelty claim is made.

The public bundle separates three roles:

- historical_revision2/ is the unchanged author seal before the narrow ledger semantic correction.
- corrected/ is the accepted author slice. Only its verifier differs from historical_revision2; mathematical bytes are identical.
- audit/ supplies the full independent review, actual ledger patch, additional checker, results and independently pinned replay.

Before execution compare all external pins against the separately delivered receipt. Do not accept a manifest merely because it is self-consistent.

With trusted Python 3 and standard library, use absolute paths and run as nonroot:

    python3 -I -B corrected/freeze/bootstrap.py corrected/packet
    python3 -I -B -O corrected/freeze/bootstrap.py corrected/packet
    python3 -I -B -OO corrected/freeze/bootstrap.py corrected/packet
    python3 -I -B audit/freeze/bootstrap.py audit/packet
    python3 -I -B -O audit/freeze/bootstrap.py audit/packet
    python3 -I -B -OO audit/freeze/bootstrap.py audit/packet

The paths above are relative examples of the archive layout; replace them with absolute paths when executing from another directory. The audit replay runs the independent subset-DP checker and compares its mathematical output with the pinned result. No downloads or third-party packages are required, and -B avoids bytecode writes.

To reproduce the old/new semantic checks, use a writable temporary directory for disposable mutation copies (the sealed inputs stay read-only):

    python3 -I -B audit/packet/check_ledger_correction.py historical_revision2 corrected
    python3 -I -B audit/packet/extra_integrity_checks.py historical_revision2

The first script establishes 42 old direct acceptances, 42 corrected direct rejections and 84 fixed-bootstrap rejections. The second records additional historical parser controls and the originally discovered semantic boundary. Those historical direct acceptances are repaired in corrected/ and are not successful authenticity attacks.

INTEGRITY_RESULTS.json includes the full independently reexecuted author matrices, original-seal and actual-patch checks, supplementary parser tests and semantic correction controls. INDEPENDENT_RESULTS.json records the three independent mathematical modes. Source PDFs, extracts, rendered pages, corpus records and private coordination are excluded.

The hash manifests certify bytes under the specified static-file threat model. They do not prove the infinite mathematical claims, the correctness of every imported theorem, the authenticity of a replacement receipt, or safety under a compromised runtime.
