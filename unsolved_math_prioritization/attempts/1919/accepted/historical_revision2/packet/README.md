# Reproduce the source-free packet

This is an unsolved-problem report with scoped elementary lemmas and counterexamples. Read REPORT.md and STATUS.json first. No novelty, complete resolution, formal proof, or independent-review claim is made.

Keep the packet/ and freeze/ directories side by side. Before executing, compare the external manifest, verifier, and bootstrap SHA-256 hashes with the separate trusted delivery receipt. A self-authored replacement manifest is not a trust anchor.

Run from any directory with a trusted Python 3 installation and standard library:

    python3 -I -B /absolute/path/freeze/bootstrap.py /absolute/path/packet
    python3 -I -B -O /absolute/path/freeze/bootstrap.py /absolute/path/packet
    python3 -I -B -OO /absolute/path/freeze/bootstrap.py /absolute/path/packet

The launcher authenticates the external manifest and verifier before executing the verifier. The verifier checks the exact file set, regular-file status, sizes and hashes before running finite mathematics checks. Python assertions are not used. No downloads, installations, writes, source files, or third-party packages are needed for replay. Isolated mode blocks local/PYTHONPATH import hijacking; -B prevents bytecode writes.

The external replay report records tests on an actual nonroot process and a frozen read-only layout, relocation, hostile environment/cwd controls, and malformed/corruption controls. Only temporary mutation copies are made writable. A passed replay checks finite diagnostics and bytes, not the infinite conjecture or the correctness of cited papers. Independent mathematical review is still pending.
