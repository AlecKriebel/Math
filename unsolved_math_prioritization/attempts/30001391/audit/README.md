# Portable independent audit

Problem 30001391 / OWR-4137-007, Degree Bounds for Degenerate Herman Rings.

Verdict: **unsolved for the intended unrestricted periodic target; restricted conclusions accepted after independent written review.** The concrete correction is a Yang equation locator. Other edits make the proof and scope more explicit.

Read `AUDIT_REPORT.md` and `EXACT_CORRECTIONS.md`. `AUDIT_RESULT.json` is the concise machine-readable disposition. `AUDIT_MANIFEST.json` binds all audit files to author manifest SHA-256 `63df37afcb5592e0bde27cf8e66383025710e5fcc685d38afb954a37275d48b8`.

Replay with Python 3.10 or later, standard library only:

    python independent_checks.py /path/to/frozen/submission
    python verify_audit.py /path/to/frozen/submission

For the original sibling layout, the arguments may be omitted. The first command replays the frozen author's controls and the independent finite controls. The second checks both the audit and the exact frozen author manifest. Neither is a mathematical theorem prover.

The audit is self-contained scholarly exposition plus checks and integrity metadata. It contains no source PDFs, extracted article text, source screenshots, source corpora, or private coordination inventories. Original author files were preserved; no remote write was performed by the auditor.
