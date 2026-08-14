# Research log

All times are America/Los_Angeles.

## 2026-08-13 18:45 PDT

- Began the proof-first follow-up after the pure finite-tree rerooting route
  was closed.
- Restricted attention to the one natural nonlocal extension requested:
  size-biased dB survival spines and Bd trees conditioned on extinction or
  survival.  No tree enumeration or transform search was used.

## 2026-08-13 18:57 PDT

- Proved the general geometric first-success lemma
  `J^x_ij=r h(x)_i R_ij x_j`.
- Identified its two exact specializations: the first dB-surviving child and
  the first marked finite-Bd child.

## 2026-08-13 19:08 PDT

- Derived the complete positive mixed expansion of `h1`: every failed child
  is either unmarked or marked with a surviving Bd tree.  Expanding each
  survival event by its leftmost spine gives the requested mixed
  finite-tree/spine ensemble.
- Factored both sides of the endpoint comparison into their edge skeletons
  and normalized conditional subtree laws.

## 2026-08-13 19:20 PDT

- Derived the exact edge likelihood on the dB survival spine:
  `L_ij=z_j/(h_i+s_i(Kz)_i)`, `z=cq/s`.
- Its row mass is exactly `F_r(cq)_i/s_i`; hence normalization removes the
  unknown endpoint factor rather than proving its sign.

## 2026-08-13 19:34 PDT

- On the symbolic reversible two-cycle, proved that the two successive row
  masses have cycle product strictly larger than one off the homogeneous
  mode.  The gap factors as `(k-1)^2 Q(c,k)` over a positive denominator,
  with `Q` coefficientwise positive.
- This rules out a consistent type-preserving multiplicative spine density,
  including repair by a positive terminal coboundary.
- Reported the exact identity, factorization, and scope to the primary agent
  before preparing a commit.

## 2026-08-13 19:45 PDT

- Packaged the mixed-ensemble theorem, cocycle obstruction, exact symbolic
  verifier, and explicit limitation: arbitrary nonlocal allocations between
  spine positions remain open.
