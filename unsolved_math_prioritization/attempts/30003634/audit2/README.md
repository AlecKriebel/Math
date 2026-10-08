# Independent second mathematical audit

Decision: **ACCEPT** the frozen author's explicit counterexample at `(m,n)=(3,1)` and its split-strand extensions at `n=1`.

Read `AUDIT_REPORT.md` for the mathematical review and `ACCEPTANCE.json` for the machine-readable decision. `SOURCE_CHECKS.json` contains only public source metadata and inspection scope. No copied scholarly source files are included.

## Reproduce

Requirements: Python 3.12 and SymPy 1.14.0 were used; no floating-point numerical package is needed. Obtain the separately supplied frozen author packet with manifest SHA-256 `d1e1467c6d36b6c62283af2ec50ddff8864020ad8a7c9e0ba9a6704dacb4246a`.

Run from any working directory:

```sh
python -B /path/to/this/audit/recovery_controls.py --author-packet /path/to/author/packet
python -B /path/to/this/audit/test_second_audit_replay.py --author-packet /path/to/author/packet
python -B /path/to/author/packet/test_replay.py
```

The first result must equal `RECOVERY_CONTROLS.json`, the second `PORTABLE_REPLAY.json`, and the third `RECOVERY_AUTHOR_REPLAY.json`. The controls wrapper sets the author-packet path in the independent reviewer checker, permitting relocation without changing the preserved original checker. It verifies every author manifest entry before doing mathematics. Neither reviewer checker nor controls imports author code.

`INDEPENDENT_RESULTS.json` and `RECOVERY_INDEPENDENT_RESULTS.json` are identical. `AUTHOR_REPLAY.json` and `RECOVERY_AUTHOR_REPLAY.json` are identical. The duplicates preserve both the original saved outputs and their finalization replays. The author software test is explicitly distinguished from the independent mathematical recomputations.

`MANIFEST.json` fixes the files, sizes, and SHA-256 hashes in this audit packet. The separate freeze receipt records the manifest and archive hashes. The packet carries no assertion of formal theorem verification, historical novelty, or external human review.
