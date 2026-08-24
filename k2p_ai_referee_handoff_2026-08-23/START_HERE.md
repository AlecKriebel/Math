# K2P-SAME post-submission AI referee handoff

This folder is a self-contained copy prepared for an independent journal-style
review of the article, supplement, mathematical proof, verifier code, exact
finite certificates, and clean-room replay for the principal positive-domain
K2P classification.

Nothing in this handoff asks the referee to confirm the authors' conclusion.
The neutral assignment is in `AI_REFEREE_PROMPT.md`.  A referee may conclude
PASS, FAIL, or UNVERIFIED for each layer and may recommend accept, hold, or
reject for the scientific result.

## Package layout

- `AI_REFEREE_PROMPT.md`: the complete neutral referee assignment.
- `SUBMISSION_BINDING.json`: current article, supplement, source, commit, and
  computational-evidence bindings, with unresolved human release fields left
  explicitly null.
- `EXPECTED_RESULTS.json`: reference assertions to test, not accepted facts.
- `VERDICT_TEMPLATE.md`: a structured independent report template.
- `papers/`: convenient copies of both PDFs and a literature index.
- `materials/k2p_principal_d_plus_submission_referee/`: a byte-exact copy of
  the sealed 448-member computational referee tree, plus five current
  execution dependencies consumed by submission-layer replayers but omitted
  from the old inner archive.  Two have byte-identical sealed portable copies;
  three do not.  All five are bound to the current source commit by
  `SUBMISSION_BINDING.json` and the outer manifest, and the referee is asked to
  scrutinize this distinction explicitly.
- `PACKAGE_MANIFEST.json`: an outer SHA-256 ledger binding this handoff.
- `verify_handoff.py`: independent outer-ledger and inner-ledger verification.
- `test_handoff_mutations.py`: adversarial mutations of the outer ledger.
- `check_manuscript_build.py`: isolated five-source manuscript build and
  fail-closed generated-input checks.
- `setup_environment.sh`: creates an isolated Python environment with the
  exact locked NetworkX and SymPy versions.
- `run_all_verifiers.py`: one entrypoint for the compact or exhaustive suites.
- `build_handoff_manifest.py` and `build_handoff_archive.py`: deterministic
  package producers for independent inspection and reproduction.
- `reference_qualification/`: the copied 21/21 clean quick-run ledger and its
  per-command hashed logs.  This is reference evidence only; rerun it.

The article and supplement PDFs are at:

```text
materials/k2p_principal_d_plus_submission_referee/
  proof_compression_submission/output/
    K2P_SAME_Principal_Domain_Article.pdf
    K2P_SAME_Reader_Supplement.pdf
```

## First-use commands

Run these from this folder in an isolated copy:

```sh
python3 -B verify_handoff.py
python3 -B test_handoff_mutations.py
./setup_environment.sh
materials/k2p_principal_d_plus_submission_referee/.venv/bin/python -B run_all_verifiers.py --list
materials/k2p_principal_d_plus_submission_referee/.venv/bin/python -B run_all_verifiers.py --quick
materials/k2p_principal_d_plus_submission_referee/.venv/bin/python -B run_all_verifiers.py --full
```

The quick suite includes package integrity, clean manuscript compilation,
submission-layer checks and mutations, the final theorem quick replay, and
the outer release mutations.  The full suite first runs the quick suite and
then performs primitive regeneration through the authoritative 35-layer full
replay.

The frozen reference full replay passed in 5,172.89 seconds on an M1 MacBook
Pro, with maximum resident set size 1,960,001,536 bytes.  This is reference
telemetry, not a promised runtime on another machine.  Allow several hours,
at least 4 GB RAM, and ample temporary disk space.  The source requires Python
3.10 or newer.  The locked Python dependencies are NetworkX 3.5 and SymPy
1.14.0.  Clean TeX reproduction additionally requires Tectonic; missing it
must be reported as an unverified document-build gate, not silently ignored.

Verifier outputs are written below `referee_outputs/`, which is deliberately
outside the immutable handoff ledger.  Do not edit files in `materials/` while
auditing.  If an experimental mutation is needed, use a disposable copy.

Stored PASS reports and hashes establish provenance only.  They do not prove
that a graph generator is exhaustive, a certificate implication is valid, or
an implementation matches the mathematics.  The referee prompt therefore
requires code inspection and independent falsification in addition to replay.
