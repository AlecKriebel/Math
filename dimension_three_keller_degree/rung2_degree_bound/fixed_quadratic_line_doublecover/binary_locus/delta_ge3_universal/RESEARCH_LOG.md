# Research log — universal binary \(\delta\geq3\) atlas

## 2026-07-25 / 2026-07-26 UTC

- Corrected the task shorthand: \(R=(H_3)_3\) is a binary **cubic**,
  not a quartic.
- Fixed the five exhaustive fixed-divisor charts by the root multiset of
  the binary quadratic \(h\) relative to the two branch points:
  branch square, two branch roots, one branch root, doubled nonbranch
  root, and squarefree interior.
- Used \(\gamma=8h^2pq\) to reduce \(\delta\geq3\) to finitely many
  capped exponent tuples.  All divisibility conditions in the four
  coefficients of \(R\) are linear.
- Derived the generic exact signatures:
  2 BS, 4 TB (2 swap orbits), 6 OB, 4 DN (3 swap orbits), and 10 SF
  (4 cover-stabilizer orbits) at \(\delta=3\); 4 DN signatures (3
  swap orbits) at \(\delta=4\).
- Computed the four squarefree degree-four rank-locus factors.  After
  saturation by \(s(s^2-1)\), exactly three interior orbits remain, at
  \(\kappa=-16/5,16/5,16\).
- Corrected the doubled-nonbranch boundary normalization:
  `D4-DN-PL3` is \(R=(p+q)^2(p-2q)\), with gcd
  \(p(p+q)^3\).
- Separated the constant-dependent power fibre
  \(h=p^2,R=p^3\) from the independent Hilbert--Burch
  \(\delta\leq4\) table.
- Froze the primary denominator at
  \[
  17\text{ exact-}\delta=3
  +6\text{ exact-}\delta=4
  +1\text{ power fibre}.
  \]
- Fixed the counting convention: exact-\(\delta\) parameter endpoints
  and stabilizer jumps remain inside a displayed family; degeneration
  points are boundary arrows to already counted targets.  The retained
  specializations are listed explicitly in `denominator.json` and
  `NOTE.md`.
- Added two exact replays:
  `verify_incidence_sympy.py` gives the saturation-safe exhaustive
  enumeration, while `verify_incidence_pari.gp` directly checks
  homogeneous gcds in both affine charts for every pinned family,
  including the three algebraic interior orbits.
- Added a dependency-free manifest audit with an injected-fault check and
  a strict wrapper which rejects assertion-free Python and PARI error
  transcripts.

### Scope decision

This package is an incidence atlas inside the frozen parent row.  It
contains no Keller exclusion and makes no novelty or priority claim.
Reconciliation against a blinded independent enumeration was
intentionally deferred until after this primary denominator was frozen.
