# Independent audit of binary wreath shortest laws

Verdict: **PASS for the scoped partial claims. The general problem remains unresolved.**

`AUDIT.md` gives the mathematical and source review. `CORRECTIONS.md` records that no mandatory correction was found and lists essential scope safeguards. `INDEPENDENT_RESULTS.json` records the independently reproduced finite checks. `SOURCE_AUDIT.json` records source and corpus bindings without source text.

Run from any directory, using Python 3.10 or newer without `-O`:

    python replay_audit.py --author /path/to/author/safe_output

The author directory must contain the exact ten frozen files. For the exact audit replay, also place the original QUESTIONS_1200005_AUTHOR_SAFE_FREEZE.zip in the author directory's parent; its pin and every member are checked. The independent verifier enumerates the candidates, builds fresh tree-permutation counterevaluations, cross-checks the author certificate streams, and replays the author controls. No network or third-party packages are needed. Expect roughly a minute, depending on the machine.

The core finite proof is independent of the author implementation: fixed-alphabet enumeration, a separate dynamic program, breadth-first tree portraits, and direct leaf actions. The later cross-check phase is explicitly identified in code. The audit's current-public-source inspection is a human-readable review record, not an offline claim that the internet has remained unchanged.

No author bytes were modified, and no remote write was performed. The safe audit contains no source PDF, extract, raw imported dataset, or private coordination.
