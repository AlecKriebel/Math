# Subcritical reinforcement v2: separate acceptance

Problem 30005453, rank 798. Read ACCEPTANCE.md for the decision and REPORT.md for
the targeted second analytic review. RESULT.json contains the machine-readable
classification. INPUT_BINDING.json identifies the immutable inputs.

The exact proposed-v2 bytes pass the bounded editorial-delta review and are
accepted for the explicitly corrected positive-equilibrium theorem. The literal
nonnegative-uniqueness statement is false. There is no novelty, priority, journal
acceptance, or publication-readiness claim.

The verifier code is standard-library Python. From a directory containing the
three named input ZIPs, run:

    python -B path/to/safe/code/verify_delta.py --input-dir . --output /tmp/delta.json
    python -B path/to/safe/code/targeted_checks.py --output /tmp/targeted.json
    python -B path/to/safe/code/replay_inputs.py --input-dir . --output /tmp/replays.json
    python -B path/to/safe/code/verify_package.py

Use output paths outside this frozen safe directory when replaying. The scripts
read input archives without changing them. replay_inputs.py uses temporary
extractions. verify_package.py checks this package's exact allowlist and hashes.
Computation is diagnostic and integrity-focused; the analytic review is not a
claim of numerical certification.

Only authored acceptance/report material, verification code and results, public
source metadata, and manifests are included. Source PDFs, extracts, images,
raw corpora, and private coordination material are excluded.
