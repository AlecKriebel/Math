# Research log

All timestamps are UTC.

## 2026-07-26T10:10:25Z — blinded phase sealed

- Read only `FROZEN_TAXONOMY_v1.md` and `frozen_manifest_v1.json`.
- Derived the intrinsic row form \(H_4=uR(p,q)+vS(p,q)\).
- Classified the primitive conic pencils into five exact congruence charts.
- Routed every determinant, gcd, rank, resultant, and composite-pencil
  boundary.
- Recorded the division-free polynomial map to all 45 frozen coefficients.
- Sealed the result in `BLINDED_DERIVATION.md` before opening legacy work.

## 2026-07-26T10:12Z — legacy mechanism located

- Located `WORKING_LINE_TYPE_22.md` and the frozen exclusion audit.
- Confirmed the historical simultaneous-normalization failure and its later
  correction by joint-orbit packages.
- Matched the two unique-double-line legacy pencils to blinded charts
  `P11_1` and `P21`.
- Matched the other three blinded charts to the universal zero-cubic and
  quadratic-component exit.

## 2026-07-26T10:13Z — rank-two-restriction replay

- Reran the finite-outer-critical SymPy and PARI verifiers.
- Reran both \(F/G\) resonance verifiers and the independent exact audits.
- Reran marked-critical-infinity, remaining outer-infinity, and
  companion-at-infinity primary and hostile verifiers.
- All packages passed.

## 2026-07-26T10:15Z — rank-one-restriction replay

- Reran the open-orbit SymPy/PARI pair and clean-room hostile reconstruction.
- Reran unmarked triple, both marked mixed, marked triple, unmarked
  \(c^2=9\), and unmarked companion-at-infinity packages.
- The companion-at-infinity branch also passed its dependency-free sparse
  polynomial reconstruction.
- All packages passed.

## 2026-07-26T10:17Z — independent frozen bridge checks

- Wrote and ran `verify_blinded_bridge_sympy.py`.
- Wrote and ran `verify_blinded_bridge_pure.py`.
- Both independently returned:
  - \(D:S_2\to S_3\): rank/kernel/cokernel \(4/2/6\) on every chart;
  - \(D:S_3\to S_4\): \(10/0/5\) on `P111`, `P2_1`, `P3`;
  - \(D:S_3\to S_4\): \(8/2/7\) on `P11_1`, `P21`.
- Reran the top line-\((2,2)\) determinant-extraction regression and the
  separate quadratic-component exact checker; both passed.

## 2026-07-26T10:18:34Z — final verdict

- Smallest gap: absent post-freeze frozen-row and coefficient-pivot bridge.
- Repair: five-chart classification, complete boundary routing,
  division-free 45-coefficient map, dual exact bridge replay, and fresh
  terminal assembly replay.
- Verdict: **PASS**.

## 2026-07-26T10:25:10Z — strict full replay

- Added `verify_strict.sh` with frozen-input and audit-artifact hash checks,
  exact clean-room transcript checks, and the complete primary/hostile
  legacy command ledger.
- Ran it from a clean process.  It returned exactly:
  `PASS: strict post-freeze Q2-E0-A2-B2-D1-N2 bridge and full legacy replay`.
- Final verdict remains **PASS**.
