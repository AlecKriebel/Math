# Bell-setting Lean formalization — current continuation

**Partial, uncompiled proof source. The full paper has not been formally verified.**

Start with [CONTINUATION_STATUS.md](CONTINUATION_STATUS.md). It records what was
actually recovered, added, executed, and left unproved in the current session.
The build wrapper exited 127 because this runtime has no Lean/Lake installation.

The new source is [Bell/DeterministicGap.lean](Bell/DeterministicGap.lean): an
explicitly conditional reconstruction of the deterministic-gap multiplier
argument. All 23 previously recovered mathematical modules remain unchanged.
See [the argument](docs/DETERMINISTIC_GAP.md) and the current
[progress record](reports/session_20260910/progress.json).

The [offline environment handoff](environment/README.md) provides a self-contained
GitHub workflow and restore helper for the exact Linux Lean 4.19/Mathlib pins.
It was tested locally for transfer integrity, safety, syntax, and embedding, but
has not run on GitHub and has not yet produced a compiler bundle.

Historical continuation notes in `FORMALIZATION_STATUS.md`, `RECOVERY_STATUS.md`,
and `docs/` are retained, including their explicit missing-file limitations.
Their old declaration counts and test descriptions are historical, not fresh
proof evidence. The complete incoming archive is preserved in `preservation/`.

## Next compiler operation

After restoring the exact toolchain and dependency cache:

    bash scripts/check.sh

The wrapper builds the written subset and audits theorem axiom dependencies.
A successful subset check is not the missing universal two-input theorem.

## Independent non-Lean checks

    python3 scripts/exact_checks.py
    python3 scripts/sos_checks.py
    python3 scripts/sos_bareiss_check.py
    python3 scripts/deterministic_gap_checks.py
    python3 environment/test_handoff.py

Their actual current receipts are under `reports/session_20260910` and `reports/`.
No `sorry`, custom axiom, or native proof escape is used to fill the open targets.
That static source property does not establish that any tactic elaborates.
