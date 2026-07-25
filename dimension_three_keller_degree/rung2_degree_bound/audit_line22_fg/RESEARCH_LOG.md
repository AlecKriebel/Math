# Research log: hostile audit of line-(2,2) finite-companion F/G package

## 2026-07-25T05:38:51Z — audit opened (5%)

- Confirmed the worktree is on `main`.
- Read the two provisional notes and all four supplied SymPy/PARI
  implementations plus the strict PARI runner.
- Initial audit targets: joint-coordinate orbit coverage, all excluded
  specializations, raw `E_7`/`E_6` ranks and converses, square
  compatibilities, the lower `E_5` common-kernel exit, division safety,
  remaining-boundary accounting, and fail-closed behavior.
- No theorem or global documentation file will be modified.

## 2026-07-25T05:55:14Z — chart algebra passed; scope failure found (75%)

- All four supplied CAS files pass in ordinary mode.  The supplied strict
  PARI runner also passes normally and rejects a fake zero-exit `gp` that
  prints both a `***` diagnostic and the expected success sentinel.
- Both supplied SymPy scripts accept `python -O`, skip their `assert`
  certificates, return zero, and still print their success sentinel.  This
  is a fail-open packaging defect.
- Independently reconstructed the stabilizer of
  `span(x^2,yz)`: it consists of diagonal scalings and the `y,z` swap, so
  it only scales `u=p/q`; it cannot move `u=infinity`.
- Consequently the claim that every outer double cover has two finite
  critical points is false.  The omitted chart is
  `H4=((p-aq)^2,q^2,0)`, `R3=x(p-cq)`.  Common scaling preserves `[a:c]`.
- Direct exact weight blocks in that chart give
  `det(E7_{+/-2}) ~ (3a-c)(3a-2c)` and maximal-minor gcd
  `E7_{+/-1} ~ c(3a-c)(3a-2c)`.  Thus the omitted finite-companion
  resonances are `c=3a` and `c=3a/2`, with the separate triple endpoint
  `c=0`.
- The concrete datum
  `H4=((p-q)^2,q^2,0)`, `H3=(0,0,x(p-2q))`, `H2=0` satisfies exact
  `E8=E7=0`, has finite mixed companion, and belongs to none of the three
  boundaries listed in the note.
- An independent direct-determinant implementation passed the finite
  F-chart: raw `E7` rank 14; complete 12-dimensional raw kernels in the
  generic and `t=1/2` gauges; all four `E6` square obstructions; complete
  rank-eight lower `E6` converse; and the common rank-at-least-two `E5`
  column kernel.  No in-chart counterexample survived.
- Current verdict: PASS for the finite-critical F/G chart theorem; FAIL for
  the advertised full-moduli/exhaustive-boundary package.

## 2026-07-25T05:59:53Z — audit complete (100%)

- Wrote the full hostile-audit report with explicit PASS/FAIL findings,
  stabilizer proof, omitted-orbit classification, resonance factors, raw
  ranks, counterexamples to exhaustion, corrected boundary list,
  specialization/division ledger, and every required correction.
- Re-ran both independent exact audits and the fake-GP runner test
  successfully.
- A parallel provisional package now addresses only the marked-critical
  triple point `(a,c)=(0,0)`.  It was not audited here; the report clearly
  distinguishes that point from the rest of the omitted infinity chart.
- The theorem files and global documentation remain untouched.

## 2026-07-25T06:06:25Z — remediation verified

- The original full-row scope remains rejected, but the theorem files were
  narrowed to the finite-outer-critical chart and renamed accordingly.
- The missing outer-infinity chart, its two resonance ratios, all raw-rank
  strata, and the corrected exhaustive frontier are now explicit.
- Both supplied SymPy scripts now reject optimized mode before reaching any
  assertion-based certificate.  The corrected fault-injection test passes.
- The finite-chart SymPy, PARI/GP, independent direct-determinant audit, and
  fake-GP strict-runner test all pass after the wording and guard changes.
- Final release verdict: PASS for the finite-outer-critical,
  finite-companion theorem; FAIL for any claim to have closed the complete
  unique-double-line row.
