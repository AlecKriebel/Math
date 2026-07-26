# Research log — `D4-SF-21C`

## 2026-07-26 UTC

- Selected the canonical exact-\(\delta=4\) representative
  \(s^2=-5,\ h=(p-sq)(sp-q),\ R=(p-sq)^2(sp-q)\), corresponding to
  \(\kappa=-16/5\).
- Computed the full \(E_6\) contact variety with arbitrary binary lower
  summands.  Its highest-\(r\) equations force the degree-one contact
  variables to zero.  Four exact left-kernel compatibilities then force
  a two-parameter plane in the degree-two contact variables.
- Found a genuine three-chart rank split below \(E_6\): generic rank
  seven, rank six at \((m,n)\sim(1,3),(-1,6)\), and rank five at the
  origin.  No generic formula was reused on either boundary.
- On the generic chart, two \(E_5\) cubics have nonzero pure-power
  resultants.  Fresh solves give the constant obstruction \(-108/5\) on
  both rank-six directions.  The origin reaches two square \(E_4\)
  obstructions and collapses all nonlinear terms to the binary plane.
- The first SymPy implementation was mathematically correct but spent
  over ten minutes simplifying unused coefficients.  Replaced it with
  certified pivot-block solves and extraction of only the coefficients
  used in the proof; strict runtime is now under one minute on the M1
  host.
- Added an independent PARI/GP reconstruction over
  \(\mathbb Q(\sqrt{-5})\), including explicit left-kernel vectors and
  fresh solves in every chart.
- Terminal marker: `D4_SF_21C_FULL_STRICT_PASS`.
- A clean-room hostile audit independently reconstructed the orbit
  normalization, complete contact plane, both rank-drop directions,
  generic and boundary obstructions, origin collapse, and Moh exit.
  Markers `D4_SF_21C_CLEANROOM_LOWER_PASS` and
  `D4_SF_21C_CLEANROOM_TOP_PASS` pass.
- Promoted to a certified family-level exclusion.  This is one of the
  26 frozen high-incidence families, not a parent-row closure or a new
  universal degree bound.
