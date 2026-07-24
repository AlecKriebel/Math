# Research log

## 2026-07-23

- Derived the exact coordinate identities for a point extending a
  six-point weighted support:
  \(\sum a_i=0\), \(\sum a_i^2=6/5\), and \(a_i\leq1/2\).
- Solved the associated box-section extremum exactly.  The threshold is
  \(\rho=(5+\sqrt{15})/20\); among the six endpoint-count cases, only two
  upper endpoints and three lower endpoints give a feasible vertex.
- Obtained the exact six-cap cover and its equality pattern.
- Attempted a sampled cap SDP.  The retained run failed at the solver stage
  and is explicitly excluded from the claims.
- Tested a scalar Delsarte refinement using the 30 ordered simplex pairs.
  Its best sampled degree-10 margin at \(N=41\) remained negative (about
  \(-4.71\)), so that mechanism was rejected as insufficient.
- Tested projection of the degree-1/2 harmonic kernel away from the simplex
  span.  Random feasible pairs gave positive residual off-diagonal entries,
  refuting the hoped-for universal nonpositive-sign lemma.
- Hardened the exact verifier so no proof check depends on Python
  assertions, and added valid/tampered subprocess tests under `python -O`.
