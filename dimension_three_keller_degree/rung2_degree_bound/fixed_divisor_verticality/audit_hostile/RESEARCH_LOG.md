# Hostile-audit log

All timestamps are UTC.

## 2026-07-25T06:42:00Z — field and valuation audit

- Reconstructed the relative-algebraic-closure argument for
  \(a=1,2,3\), including coprimality after binary substitution.
- Reproved the scaling descent by treating \(P\) as transcendental over
  the degree-zero field.
- Checked finite zeros, finite poles, infinity, and a degeneration in
  which another factor of \(h\) is shared with \(p\).
- Found no mathematical counterexample.

## 2026-07-25T06:47:00Z — determinant and exit audit

- Reconstructed the \(3+3+2\) polarization and adjugate orientation.
- Rechecked the quadratic-component exit and its degree-eight plane-fibre
  bound.
- Audited all three row corollaries and proved the three \(e=2\) frontier
  cases exhaustive.

## 2026-07-25T06:49:00Z — verifier defect found and corrected

- The PARI wrapper was not executable.
- A fake GP executable printing `FAIL` followed by the correct final
  sentinel exited successfully through the original wrapper.
- Patched the wrapper to reject explicit algebraic failures and restored
  executable mode.
- Added injected tests for `FAIL`, PARI diagnostics, trailing output, and
  nonzero exits.

## 2026-07-25T06:51:42Z — independent reconstruction complete

The dependency-free finite-field audit and all supplied/fail-closed
runner tests pass.  Final verdict: PASS after the verifier correction.
