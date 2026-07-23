# Status

Last updated: 2026-07-23T19:32:06Z

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

The strongest current candidate is a **fixed-cardinality, marginal-consistent
three-point moment/SOS feasibility problem**.  Unlike the standard
variable-cardinality Bachoc--Vallentin relaxation, fixing \(N=41\) makes the
exact triple-to-pair marginal relation linear.  No exact infeasibility
certificate has yet been found.

Other active incompatible routes are:

1. rank-aware Gram/nullspace inequalities, including a degree-two sign kernel
   of rank at most 20;
2. compatible local-cap/link bounds rather than isolated cap occupancy bounds;
3. unrestricted numerical construction searches for 41--44 points, followed
   by exact reconstruction if a genuine candidate appears;
4. hybrid finite reductions with a proved continuous covering or interval
   branch-and-bound certificate.

Ordinary two-point LP is now **certifiably blocked**: an exact mass-41
pseudo-distance distribution satisfies every Gegenbauer moment inequality and
has no off-diagonal atom at the contact value.

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
- Exact ordinary-LP barrier proof:
  [`proofs/two_point_lp_barrier.md`](proofs/two_point_lp_barrier.md)
- Exact barrier verifier:
  [`verifiers/verify_two_point_barrier.py`](verifiers/verify_two_point_barrier.py)
- Exact fixed-\(D_5\) saturation lemma:
  [`proofs/d5_saturation.md`](proofs/d5_saturation.md)
- Exact quadratic-kernel constraints and counterexamples:
  [`proofs/rank_kernel_barriers.md`](proofs/rank_kernel_barriers.md)
- Reproducible construction round:
  [`experiments/construction_round1.md`](experiments/construction_round1.md)
- Imported discovery-only numerical 41-point near miss:
  [`experiments/input/spherical_codes_5_41.txt`](experiments/input/spherical_codes_5_41.txt)

## Claims surviving adversarial audit

- The 40 stored vectors are distinct.
- Every stored vector has squared norm 2 before normalization.
- Every distinct stored pair has integer dot product at most 1, hence normalized
  inner product at most \(1/2\).
- Boundary equality is accepted: many pairs have inner product exactly
  \(1/2\).

These statements currently have a direct proof and a separate exact checker;
a second human/agent audit is still pending.

- The mass-41 two-point witness has exact total mass and pair-count parity.
- Its normalized Gegenbauer moments are positive through degree 53 by rational
  recurrence and in all higher degrees by an explicit analytic tail bound.
- The fixed \(D_5\) code is saturated against adding one point; its exact
  covering value is \(\sqrt{2/5}\).
- The finite-field and \(D_6\) examples exactly refute generic sign/rank
  shortcuts, while the split harmonic-factor Ky Fan inequalities remain valid
  for every actual rank-five Gram matrix.

## Failed or rejected claims

- “An extremal 40-point configuration must be \(D_5\), antipodal, or unique”:
  **refuted** by the known \(D_5,L_5,Q_5,R_5\) examples.
- “A generic PSD relaxation of the Gram constraints proves the desired upper
  bound”: **rejected** because it discards the essential rank-at-most-5
  condition unless an additional mechanism recovers it.
- “A floating-point SDP objective below 41 is itself a proof”: **rejected**;
  exact or directed-interval dual feasibility is required.
- “Positive diagonal, nonpositive off-diagonal entries, rank below half the
  order, and at most one negative eigenvalue are mutually incompatible”:
  **refuted** by the analogous quadratic kernel of the exact \(D_6\) root code.
- The first low-degree public Lasserre-code trial did not reach an SDP: exact
  symmetry-basis generation raised `UndefRefError` under the resolved
  Julia/Nemo environment.  This is an environment failure, not evidence about
  feasibility or the bound.
- “Failure to append one point to \(D_5\) proves the global upper bound”:
  **refuted**; it proves saturation of one fixed configuration only.
