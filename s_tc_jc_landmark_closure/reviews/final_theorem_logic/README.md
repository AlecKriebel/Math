# Final-theorem logic review

This directory is an adversarial, theorem-level audit of the implication

```text
corrected fixed-full local classification  ==>  Outcome P.
```

It does not certify the still-running local atlas.  It identifies the exact
local closure contract that an independent atlas must satisfy and proves that,
once that contract is met, the already reviewed cut, bridge, root, and ordinary
triangle results promote to the sharp standard-strong JC theorem.

The principal files are:

- `REVIEW.md`: referee verdict and dependency-by-dependency audit;
- `PROMOTION_PROOF.md`: corrected local-to-global proof outline;
- `promotion_contract.json`: machine-readable release contract;
- `dependency_ledger.json`: current and conditional statuses;
- `UPSTREAM_REPLAY.md`: scoped replay record and its limits;
- `N4_SUPPORT_GATE.md`: exact proof that theta-2 size four is not reducible to
  the n=3 hard cover;
- `TERMINAL_EXTENSION_AUDIT.md`: proof and record contract for path-bound
  `A+p`/`A+p+q` closure without factorial n5/n6 boundary enumeration;
- `structural_checks.py`: exact regression and mutation checks for the logic;
- `n4_support_check.py`: exact support-count and deletion replay;
- `verify_all.sh`: deterministic replay.

Run from the project root:

```bash
bash reviews/final_theorem_logic/verify_all.sh
```

The structural checks are proof regressions, not substitutes for the missing
graph-to-algebra local relation certificate.
