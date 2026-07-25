# Research log: level-five primitive branch

All timestamps are UTC.

## 2026-07-25T10:58:00Z — search opened

- Kept the existing \(W_4\) certificate unchanged.
- Generalized the quotient-tower evaluator to four inverse points, so the
  deepest norm is taken from an \(81\)-dimensional finite algebra.
- The immediate target is a modular specialization where the first four
  discriminant norms and all leading/reconstruction guards are units while
  the fourth inverse-level norm vanishes simply.
- A finite collection of successful levels would not prove the all-iterate
  statement; the computation is intended to expose a repeatable primitive
  divisor mechanism.

## 2026-07-25T11:02:00Z — evaluator repaired and cross-level replayed

- Registered the dynamically loaded level-four arithmetic module before
  execution, fixing the dataclass import failure.
- Added an explicit inverse-depth control.
- At depth three, the new loop exactly reproduced the entire banked
  \(p=1009,s=801\) level-four profile, including all nine reconstruction
  guards.
- Added a fast search path that omits diagnostic norm determinants but uses
  the same quotient tower.  It agrees with the full profile at depth four.

## 2026-07-25T11:14:00Z — modular branch found

- Complete small-prime scans at \(p=7,11,13,17,19\) found no usable zero.
  These are search provenance only.
- At \(p=23,s=3\), the deepest norm vanished.  The full diagnostic profile
  was
  \[
  (10,22,10,4,0),\quad
  (2,14,19,11,1),\quad
  (18,14,5,2,8,21,13,13,7,8,17,12).
  \]
  Hence every lower discriminant, cubic leading coefficient, and
  reconstruction denominator is a unit.
- Modulo \(23^2\), the values at \(s=3,26,49\) were
  \((460,299,138)\), giving derivative \(16\neq0\pmod {23}\).
- Scalar dual-number reconstruction found the vanishing sheet
  \((10,22,13,1)\), with \(\Delta\)-derivative \(18\neq0\), and final
  simple/double roots \(1,22\).

## 2026-07-25T11:23:41Z — candidate theorem packaged

- Wrote `RESULT.md` with the localization, norm-valuation, inertia, and
  \(S_3^{81}\)-kernel arguments.
- Added deterministic primary verifier and regression tests.
- A source-specific collision sweep of arXiv, MathOverflow, Tao's blog,
  Secret Blogging Seminar, and public X indexing found no level-five or
  all-iterate computation for this map.  This does not guarantee worldwide
  priority.
- Independent hostile replay was launched in a separate audit directory.

## 2026-07-25T11:34:30Z — independent hostile audit passed

- A fresh regular-representation implementation rebuilt the quotient tower
  at ranks \(1,3,9,27,81\) without importing the primary W5 or W4
  arithmetic.
- It independently reproduced every discriminant, leading, guard, and
  prime-square norm, and checked the scalar sheet, localization,
  norm-valuation, tame inertia, and \(S_3^{81}\) kernel arguments.
- Twelve fail-closed mutations passed.  Strict runtime was \(6.37\) seconds
  with about \(18.9\) MiB peak resident memory.
- The audit caught one factual wording error: the first draft called the
  map “degree-three,” conflating generic degree three with total degree
  seven.  The result was corrected before promotion; the theorem and
  arithmetic were unchanged.
