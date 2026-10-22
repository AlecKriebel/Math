# Polyomino boundary lattice squares, ID 30001694

Status: five bounded approaches completed; universal conjecture not resolved. No novelty claim. Fresh independent-person audit is still required.

The original quantitative question is Tverberg's 2011 conjecture, restated as Conjecture C by Pettersson, Tverberg and Östergård (2014). Their published exhaustive result covers bounding boxes of side at most 13. The retained 4×4 computation is a smaller reproducibility and negative-control exercise, not a new computational frontier.

## Contents

- PROOFS.md: exact scope, five approach families, complete partial proofs, and exact missing statement for each
- SOURCE_VERIFICATION.json: inspected primary sources, public hashes/byte counts, and explicit retrieval limits
- PRIOR_ATTEMPT_CHECKS.json: bounded repository and available-history checks; no absence proof
- STATUS.json and RESEARCH_LOG.md: outcome, budget and dated findings
- compute.py: exhaustive 4×4-cell enumeration, boundary/side-pair implementation
- verify.py: complete replay with complement flood fill, dynamic programming and diagonal pairs
- test_checks.py: seven geometric and certificate-mutation tests
- computation/certificate.csv: one row for every admitted cell mask, including maximum-block and maximum-square witnesses
- computation/summary.json, verification.json, tests.txt: exact outputs
- MANIFEST.json and verify_manifest.py: allowlisted bytes and SHA-256 checks

No scholarly PDF, extracted source text, source image, raw dataset record, or private coordination material is included.

## Reproduce

Requires Python 3.10+ standard library. From this directory run:

    python compute.py
    python verify.py
    python -m unittest -v test_checks
    python verify_manifest.py

The deterministic certificate and JSON outputs are reproduced by the first two commands. The test transcript contains execution timing, so redirecting a new test run over tests.txt changes its byte hash; run tests without overwriting that retained log before verifying the frozen manifest. Python may create ordinary __pycache__ files; these are not payload artifacts and are ignored by the manifest file-list check.

Certificate coordinates list each square's four vertices in lexicographic rather than cyclic order. Squared side is the smallest of the six pairwise squared distances; the two diagonal squared distances equal twice that value. The bit for cell (x,y) is 4y+x. Every nonempty mask 1 through 65535 is examined with no symmetry quotient.

Live-page wording and raw prior AI reports remain uninspected. The target is grounded in the catalog identification plus the primary OWR statement. Publisher-indexed text of the 2014 paper was inspected, but its PDF body was not. These limitations are not silently treated as successful inspections.
