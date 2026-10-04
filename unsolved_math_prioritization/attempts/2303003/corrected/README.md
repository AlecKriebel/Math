# Function Theory Problem 3.3: known negative resolution

**2303003 / AMR-022-3003, rank 568. Recommended status: `already_solved`, `1/5`.**

The proposed −K/2 bound is false. Hayman's 1974 counterexample already answers the exact catalogue question. The original problem list's Update 3.3 says so, despite the catalogue's generated claim that the bound is still unknown.

[PROOF.md](PROOF.md) gives a complete fixed-parameter verification and a bounded, continuous version: u takes values in [−K,0), has infimum −K on every open semicircle, and is greater than −K/2 at every positive real point. The formula is credited to Hayman; no novelty claim is made. The separate best-constant question is not solved.

[Source gate](SOURCE_GATE.md) details exactly which primary pages were read, the inaccessible second page, the bibliography discrepancy, and the actual prior-attempt checks. [Research log](ATTEMPT_LOG.md) records the single substantive reconstruction.

## Reproduce

Run `python3 verify.py` using Python 3.10 or later and its standard library. It performs 16 exact rational/symbolic assertions and floating-point diagnostics. Compare its output with `verification.json`. Finite samples are not proof certificates for the analytic continuum claims. Those claims are proved in PROOF.md.

`SHA256SUMS` covers the authored files other than itself and the freeze manifest. `FROZEN_MANIFEST.json` also binds `SHA256SUMS`. Neither integrity mechanism establishes mathematical correctness.

The author packet is frozen for independent audit; no human-peer-review or formal-verification claim is made. Source papers, first-page previews, page renderings, datasets and private materials are not redistributed.
