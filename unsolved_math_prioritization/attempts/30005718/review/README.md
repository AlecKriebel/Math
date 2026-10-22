# Independent review of 30005718

Read `INDEPENDENT_REVIEW.md` for the full mathematical audit and limitations. Verdict: scoped PASS, original unresolved, 5/5 author turns. No publication is authorized or implied by this verdict.

The 41 frozen author files are in `author/`. They match commit `b31d30a0651f3a9f1310a0473a20a6b2204fc624`, folder `unsolved_math_prioritization/attempts/30005718`, exactly. `REMOTE_BINDINGS.json` and the author's manifests bind these inputs. Keep the review beside its `author/` directory, or provide a directory/symlink with that name to the same unchanged inputs.

## Replay

With Python 3 and SymPy available:

    python independent_check.py

The complete local run has 202,120 assertions. A portable run without the four raw source PDFs and optional `NEWTON_CERTIFICATE.json` has 202,115 assertions; all mathematical controls are identical. The optional source count explicitly records what was available. The report contains the source audit; omission of local PDFs does not mean that a portable replay re-read those sources.

For author replay, run `python author/checks/verify_turn1.py` through `verify_turn5.py` and compare stdout against `author/checks/turnN_output.json`. The aggregate author total is 1,508,018 exact assertions. `AUTHOR_REPLAY_RECEIPT.json` records exact matches from the review.

The optional complete Newton certificate can be regenerated with:

    python author/checks/verify_turn5.py --dump NEWTON_CERTIFICATE.json

Its canonical bytes, excluding the trailing newline, have SHA-256 `63f530185b41356c61167ba5cd16b5a3d1d70bb837cd4d8b86c9bb4b00e29e2b`. The independent checker regenerates the same vectors by a scalar Cayley-Hamilton recurrence and explicit binomial transform; it imports no author code.

The independent checker writes the explicit second Gaussian correction to `GAUSSIAN_SECOND_CORRECTION.txt`. This is finite algebra supporting the separate analytic review, not a substitute for uniform remainder estimates.

## Public artifact boundary

`REVIEW_MANIFEST.json` lists the review deliverables. The author packet has its own final manifest. The source PDFs, extracted text, screenshots, optional one-megabyte Newton dump, local recovery/operational files, and temporary portable-run directory are outside the review deliverables. Do not republish third-party source PDFs.

Frozen author files saying review pending are historical snapshots. This later additive review supplies the current verdict. The source conjecture remains unresolved despite eventual ULC and the certified fixed-width bands.
