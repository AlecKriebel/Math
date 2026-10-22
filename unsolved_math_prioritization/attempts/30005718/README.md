# Matrix ultra-log-concavity: problem 30005718

**Original problem: unsolved. Author budget: 5/5. Independent review: PASS for the explicitly scoped partial results.**

The strongest reviewed conclusion is eventual ultra-log-concavity of every original row, with an unspecified finite threshold. Exact all-size certificates cover lower indices k=4 through 63 and upper distances 1 through 40. These results do not settle every row: no effective threshold or rigorous overlap with the exact checks through n=500 is available. Historical novelty is not certified.

Read the [complete independent audit](review/INDEPENDENT_REVIEW.md), then the [frozen final author statement](FINAL_RESULT.md), [source gate](SOURCE_GATE.md), and TURN_1.md through TURN_5.md. The additive review supplies the current verdict; historically accurate pending-review fields in the 41 frozen author files are unchanged.

## Reproducibility

The author files exactly match commit b31d30a0651f3a9f1310a0473a20a6b2204fc624. Their final manifest SHA-256 is 69c4c24dde28eab7cb569ede2ce93d0bf326453aac88c6b897d0b2d926def6e0. The review includes all ten public deliverables unchanged, including the full written audit, independent checker, provenance bindings and exact receipts.

From this directory, run `python checks/verify_turn1.py` through `verify_turn5.py` and compare each stdout with `checks/turnN_output.json`. Together they contain 1,508,018 exact assertions. Run `python review/independent_check.py` with Python 3 and SymPy; the portable result matches `review/PORTABLE_CHECK_RECEIPT.json` (202,115 assertions). The `review/author` symlink points to this unchanged author packet, preserving the independent checker's original layout without duplicating it. On systems that do not restore Git symlinks, provide that directory link before replay.

The independent written audit separately checks the uniform analytic estimates. Finite controls and the 25 non-interval numerical diagnostics are not substitutes for those proofs. The full review receipt also records four source-PDF bindings and an optional generated certificate that are intentionally absent from this portable publication.

Raw source PDFs, extracted full text, page images, local operational files and the optional duplicate Newton dump are excluded. The optional Newton certificate is regenerable with `python checks/verify_turn5.py --dump NEWTON_CERTIFICATE.json`.
