# Research log: signed coverage detector

## 2026-08-13 -- exact `g` obstruction and physical audit

- Derived the exact anchored geometric-union expectation

  ```text
  E g = (r-1) sum_u p_u(1-p_u)/(1+(r-1)p_u).
  ```

  For uniform fan-out `m`, this is
  `(r-1)(m-1)/(m+r-1)` and its formal depth-`L` collision error is
  `O(L/m)`.
- Proved uniqueness of the signed coverage representation

  ```text
  g = sum_i c_{ {i}} - c_V.
  ```

  Its positive and negative coverage masses are `m` and `1`.  A common
  signed difference has zero full-set value, so no nonzero affine
  normalization of `g` is such a difference.
- Proved the sharp unmatched-baseline identity

  ```text
  alpha*g = alpha*(m-1)*h_one + alpha*(h_one-h_all).
  ```

  Any realization needs the baseline coefficient `alpha*(m-1)`.  On the
  uniform batch its cost/signal ratio is exactly
  `(m+r-1)/(r-1)`, so it diverges at diffuse fan-out.
- Found a baseline-free abstract surrogate using a uniform `s`-subset law
  minus a same-marginal mixture of the full set and a uniform singleton.
  With common coefficient `m/s`, its exact batch multiplier is

  ```text
  (r-1)*m*(s-1)*(m-s)
  / [s*(m+r-1)*(m+(r-1)*s)].
  ```

  At fixed `s/m -> q`, this tends
  `(r-1)(1-q)/(1+(r-1)q)` with bounded coefficient cost.
- Audited physicality.  The two canonical coverage laws cannot be invariant
  laws of a finite connected geometric-OR dual: exact rank leakage rules
  out both the fixed-rank law and the singleton/full-set mixture.  They are
  therefore not ordinary full fixation harmonics.
- Proved an exact selector stopping-law realization.  On `K_m`, first hit
  of rank `s<=m-1` from a uniform singleton is uniform on `s`-sets.  Full
  rank is unreachable in a loopless dual, but one external selector on
  `K_(m+1)` makes the full source set a proper recurrent state and realizes
  `delta_V` as an ancestral exit law.
- Pinpointed why this is not yet a graph module: a dual exit law is not a
  forward harmonic.  Generator duality makes a coverage average harmonic
  when its ancestral law is invariant, not merely a hitting distribution.
  The rank stop is a nonlocal stopping surface in ancestral configuration
  space and needs a second ancestry memory/rank controller absent from the
  ordinary one-bit Moran graph.
- Audited the complete-harmonic chord variant.  The proposed geometric
  harmonic is the finite complete **Bd** harmonic, not the finite dB one;
  the genuine dB increment ratio has an explicit positive correction to
  `1/r`.  The chord bump has limiting batch mean
  `(r-1)^2/[r(1+r(r-1))]`, but its chord remains an external
  singleton/full-set control rather than a physical dB harmonic.
- Any future stopped augmented hitting realization must prove that the
  minus harmonic is actual removed control mass under both update rules.
  Raw positive terminal populations add and do not implement the signed
  difference.
- **CLOSED:** exact `g` or an affine normalization with common coefficients
  and response-scale baseline cost.
- **OPEN:** a physical common-control realization of the bounded-density
  signed surrogate.
