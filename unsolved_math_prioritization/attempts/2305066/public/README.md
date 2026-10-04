# Function Theory 5.66: existing negative solution verified

- Catalogue ID: **2305066**; code: **AMR-022-5066**; queue rank: **579**.
- Recommended status: **already_solved**, using **1/5** substantive attempt turns.
- Answer: an infinite Blaschke product can have a dense set of values with finite fibers, including nonzero values arbitrarily close to zero.
- Attribution: **Kenneth Stephenson, 1988**. This package is a source-status correction and theorem-level verification, not a new discovery.

Read `PROOF.md` for the full implication, an elementary almost-everywhere Frostman-shift argument, and the finite-level Rouche lemma. `SOURCE_GATE.md` records exact primary-source locations and retrieval limits; `ATTEMPT_LOG.md` records the one substantive verification turn.

Reproduce the finite controls with Python 3.10+:

    python3 verify.py
    python3 verify_manifest.py

`CHECKS.json` is the captured control output. These finite checks are not a proof of the infinite construction. Only the authored text, source metadata, and small control programs are included here; source documents are linked rather than redistributed.
