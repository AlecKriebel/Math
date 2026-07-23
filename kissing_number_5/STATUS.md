# Status

Last updated: 2026-07-23T18:39:53Z

## Rigorous bounds

\[
\boxed{40\leq\tau(5)\leq44}.
\]

- Lower bound 40: **independently exact-verified** from the \(D_5\) root
  configuration.  See
  [`proofs/lower_bound_d5.md`](proofs/lower_bound_d5.md) and run
  `python3 verifiers/verify_d5.py certificates/d5_roots.json`.
- Upper bound 44: **imported published baseline**, due to the
  Bachoc--Vallentin three-point SDP as computed at high precision by
  Mittelmann--Vallentin.  This project has not yet reconstructed a standalone
  exact certificate for that bound.

No exact value has been established.

## Strongest candidate routes

There is not yet a theorem-strength leading route.  The initial portfolio is:

1. exactification and strengthening of the three-point SDP to an objective
   strictly below 41;
2. rank-aware Gram/nullspace inequalities that retain `rank(G) <= 5`;
3. compatible local-cap/link bounds rather than isolated cap occupancy bounds;
4. unrestricted numerical construction searches for 41--44 points, followed
   by exact reconstruction if a genuine candidate appears;
5. hybrid finite reductions with a proved continuous covering or interval
   branch-and-bound certificate.

## Theorem-strength unresolved gaps

- No universal inequality excludes a 41-point code.
- No exact three-point or higher-point dual certificate below 41 is known here.
- No complete interval, semialgebraic, or finite-cell exhaustion of all
  41-point codes is known here.
- No construction with 41 or more points is known here.
- No theorem justifies restricting a hypothetical extremizer to a contact
  graph, finite inner-product alphabet, symmetry class, rigidity class, or
  lattice.

## Reproducible artifacts

- Exact \(D_5\) coordinates:
  [`certificates/d5_roots.json`](certificates/d5_roots.json)
- Independent verifier:
  [`verifiers/verify_d5.py`](verifiers/verify_d5.py)
- Verifier tests:
  [`tests/test_verify_d5.py`](tests/test_verify_d5.py)

## Claims surviving adversarial audit

- The 40 stored vectors are distinct.
- Every stored vector has squared norm 2 before normalization.
- Every distinct stored pair has integer dot product at most 1, hence normalized
  inner product at most \(1/2\).
- Boundary equality is accepted: many pairs have inner product exactly
  \(1/2\).

These statements currently have a direct proof and a separate exact checker;
a second human/agent audit is still pending.

## Failed or rejected claims

- “An extremal 40-point configuration must be \(D_5\), antipodal, or unique”:
  **refuted** by the known \(D_5,L_5,Q_5,R_5\) examples.
- “A generic PSD relaxation of the Gram constraints proves the desired upper
  bound”: **rejected** because it discards the essential rank-at-most-5
  condition unless an additional mechanism recovers it.
- “A floating-point SDP objective below 41 is itself a proof”: **rejected**;
  exact or directed-interval dual feasibility is required.
