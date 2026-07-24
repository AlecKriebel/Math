# Research log: compact digit-3 carry algebra

## 2026-07-24 10:34 PDT — exact A,Q reduction

- Rewrote each signed phase histogram with
  `A=C-sum sigma*L` and
  `Q=C/3-sum sigma*1[L=2]`.
- Proved and mechanically replayed
  `F=A+(3Q-A)omega` on all twenty displayed rows.
- Derived the complete alternating prefix lattice:
  even-length prefixes constrain `A` one power of three more strongly than
  `Q`; odd-length prefixes constrain them equally.
- Interpreted exactness as the signed-cardinality equality
  `n0-target=n1=n2`.

## 2026-07-24 10:34 PDT — delayed E1-origin row

- Found that the second-digit-zero `E1(origin)` row is not an exact zero.
  It becomes a genuine nineteenth equation at digit 3.
- All 42 grouped forms have multiplicity `+/-3`; division by three makes
  the digit-3 equation linear.
- Verified that this row is independent of the rank-18 first layer,
  reducing the affine dimension from 36 to 35.
- Its digit-4 successor is quadratic, with polar rank 16 before and 14
  after restriction to the delayed hyperplane.
- Derived 22 disjoint local blocks: twelve singletons and ten
  three-cycles.

## 2026-07-24 10:34 PDT — exact delayed-origin count

- Reduced the full exact row to
  `-sum_12 omega^a + (1-omega)sum_10 omega^b=0`.
- Two independent finite counts agree:
  exactly 30 orientation-histogram pairs and 596,095,200 of `3^22`
  orientations solve the row.
- Added an optional `digit3_exact_row7` solver mode using both the exact
  cardinality equalities and the 30-pair orientation table.

## 2026-07-24 10:34 PDT — sparse solver benchmarks

- Built an affine carry model with 3,044 variables and 2,018 constraints.
- Built a sparse original-trit histogram model.  Its baseline digit-3
  form has 2,078 variables and 1,031 constraints; explicitly exposing the
  first 18 rows and delayed nineteenth row gives 2,099 variables and 1,052
  constraints.
- A 180-second baseline digit-3 run ended `UNKNOWN` after 1,341,326
  branches and 18,835 conflicts, at about 517 MB peak RSS.
- A 180-second `digit3_exact_row7` run (before adding the 30-pair table)
  also ended `UNKNOWN`, after 1,288,082 branches and 20,056 conflicts, at
  about 508 MB peak RSS.
- These are bounded negative solver results, not exclusions.

## 2026-07-24 10:34 PDT — degree-3 XL audit

- Eliminated the delayed linear row and derived 18 exact carry cubics on
  35 variables with `floor(S/3)=binom(S,3) mod 3`.
- Formed 666 XL rows from the cubics and all affine multiples of the 18
  digit-2 quadrics over 8,401 reduced monomials.
- Exact `F_3` ranks are: full 666, cubic projection 648, degree-at-most-two
  intersection 18, degree-at-most-one intersection 0, constant
  intersection 0.
- Therefore degree 3 yields no refutation and no new quadratic or linear
  consequence beyond the original quadric span.
