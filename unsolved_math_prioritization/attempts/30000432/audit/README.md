# Independent audit of UnsolvedMath 30000432

Verdict: the partial mathematical claims pass; the original problem remains unsolved, 5/5. Two author-verifier coverage gaps are documented and independently guarded. Read `AUDIT.md` before interpreting the results.

The `author/` subtree contains all ten original frozen files unchanged. `AUTHOR_HARDENING.patch` is separate and has not been applied there.

Run with Python 3 and its standard library from any working directory:

    python /absolute/path/independent_verify.py
    python -O /absolute/path/independent_verify.py
    python /absolute/path/run_checks.py

The first two commands require the recursive manifest and run the full independent geometry and algebra controls. `--quick` is an explicitly smaller sample used only for semantic mutation controls. The full harness replays normal, optimized and relocated full runs; reproduces the original author's own controls; exercises new mutations; demonstrates the two original gaps; and tests the separate patch on temporary copies.

Do not save outputs or bytecode inside this packet. It intentionally rejects unlisted files and directories. The manifest is authenticated by the separately delivered archive receipt, not by self-hashing.

No external dependency, network access, source PDF, dataset, or original corpus is needed for replay. Full corpus/source inspection is a recorded audit action, not reconstructed from distributed copies of those materials.
