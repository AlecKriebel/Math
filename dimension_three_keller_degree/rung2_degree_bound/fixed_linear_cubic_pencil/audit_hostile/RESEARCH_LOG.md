# Hostile audit log: horizontal fixed-linear primitive cubic pencil

## 2026-07-25T06:05Z — audit opened

- Checked the exact taxonomy scope before reading the internal proof:
  \(e=1,a=3,b=1\), a minimal coprime cubic pair, and the rank-two
  restriction condition along \(h=0\).
- Reconstructed the relative-algebraic-closure implication, the
  scaling-variable descent, and the \(h\)-valuation independently.
- Confirmed that the complement of horizontality is the rank-one
  \(2\times4\) determinantal locus and that its vertical member is unique.

## 2026-07-25T06:10Z — verifier defects corrected

- Both supplied exact scripts passed in ordinary execution.
- The SymPy script also passed under optimized Python because all
  assertions were erased.  Added a fail-closed `__debug__` guard.
- Added a strict GP wrapper.  Added fake-executable tests proving that the
  wrapper rejects a diagnostic, trailing output, and a nonzero exit.
- Reconstructed finite-field polynomial arithmetic independently and
  checked 64 horizontal kernel samples, 128 determinant-polarization
  samples, and both vertical witnesses.

## 2026-07-25T06:15Z — proof and boundary audit complete

- Confirmed that \(E_8\) and \(E_7\) isolate exactly the cubic and
  quadratic third components.
- Confirmed the fibrewise plane exit uses only the established degree-four
  plane case and Ax--Grothendieck.
- Verified geometric integrality/minimality of both vertical witnesses.
- Corrected the phrase “codimension-one escape”: the determinantal
  exceptional locus has codimension three for fixed \(h\); the prime
  divisor used by the valuation is codimension one.
- Final verdict: **PASS**, conditional on the two banked inputs stated in
  `REPORT.md`.
