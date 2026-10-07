# Crossings in square tilings — partial packet

Problem 10000051 / AMR-099-0051. **PARTIAL, NOT SOLVED.** Five substantive mathematical approaches; the original fair-color lower bound and small-mesh limit are not proved.

`CANDIDATE.md` contains the exact model, complete proofs of the partial results, the precisely credited external dependency, and the remaining gaps. `TURN_LEDGER.md` records the approaches in actual chronological order. `SOURCE_METADATA.json` records public primary-source hashes, sizes, URLs and inspection scope, without redistributing those sources.

Run these exact checks from any directory with Python 3:

    python checks/exact_crossings.py
    python checks/verify_rational.py

The commands above assume the working directory is this packet directory. They require only the standard library and write their deterministic result JSON files beside the scripts. All 128 colorings of the seven-square example are checked. Additional checks use exact rational arithmetic. Decimal diagnostics in the dyadic JSON are not used as proofs. These finite checks cannot establish the general conjectures.

`SELF_REVIEW.md` is an author self-check, not independent mathematical peer review. `FROZEN_MANIFEST.json` records the exact delivered bytes, excluding its own self-referential hash.
