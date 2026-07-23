# Status

Last updated: 2026-07-23T21:51:06Z

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

The strongest current candidate is a **four-point local-to-global route**
coupling very negative pairs, their forced positive wedges, local residual
rank, and the deep-pair graph.  Exact inequalities have already eliminated
the first ordinary-LP pseudo-distribution, but a strengthened rational witness
survives all aggregate constraints certified so far.  The missing ingredient
must retain more incidence or common-source information than a global
distance distribution.

Other active incompatible routes are:

1. rank-aware Gram/nullspace inequalities, including a degree-two sign kernel
   of rank at most 20 and an exact degree-two Tverberg partition at \(N=41\);
2. compatible local-cap/link and deep-pair graph bounds;
3. unrestricted numerical construction searches for 41--44 points, followed
   by exact reconstruction if a genuine candidate appears;
4. a maximum-volume-basis semialgebraic reduction with explicit rational
   conditioning and a boundary-safe finite cell cover.

The best independently generated unrestricted 41-point numerical candidate
currently has maximum inner product \(0.5155570516153127\). A separate public
benchmark reaches approximately \(0.514994652512\). Both exceed \(1/2\) and
are numerical near misses, not lower or upper bounds.

Ordinary two-point LP is now **certifiably blocked**: an exact mass-41
pseudo-distance distribution satisfies every Gegenbauer moment inequality and
has no off-diagonal atom at the contact value.

The entire fixed-cardinality two/three-point route, in the formulation
recorded here, is now **certifiably blocked**: one exact rational
pseudo-distribution satisfies every radial block in every harmonic degree and
every pair Gegenbauer inequality.  The proof uses exact finite checks through
harmonic degree 505 and rational parity-tail estimates thereafter.  It does
not extend to four-point consistency or to a rank-five Gram matrix.

The sharpest current separator is instead a four-point/common-source
inequality.  For
\[
 f(u)=u-\frac83u^2,\qquad
 r_{ij}=x_j-\langle x_i,x_j\rangle x_i,
\]
every genuine code satisfies
\[
 \frac1N\sum_i\left\|\sum_{j\ne i}f(g_{ij})r_{ij}\right\|^2\ge0.
\]
The strongest labeled 41-vertex pseudo-Gram object surviving all
\(3\times3\) minors and all degree-two BV blocks violates this inequality by
the exact amount
\(-105027064094021/15375000000000\).  Converting this separator into a
universal continuous-label bound remains the leading gap.

## Theorem-strength unresolved gaps

- No universal inequality excludes a 41-point code.
- No exact three-point or higher-point dual certificate below 41 is known here.
- The all-degree fixed-cardinality three-point pseudo-distribution proves that
  no contradiction can follow from only the complete pair/triple measure
  conditions formalized in this repository; four-point consistency, rank, or
  another genuinely stronger invariant is necessary.
- No complete interval, semialgebraic, or finite-cell exhaustion of all
  41-point codes is known here.
- No construction with 41 or more points is known here.
- No theorem justifies restricting a hypothetical extremizer to a contact
  graph, finite inner-product alphabet, symmetry class, rigidity class, or
  lattice.
- The compact maximum-volume formulation still has 154 intrinsic continuous
  dimensions; no complete interval tree or SOS infeasibility certificate has
  been produced.
- The aggregate four-point inequalities do not yet encode the incidence
  compatibility needed to eliminate their surviving rational witness.
- The residual-vector square above separates the best labeled pseudo-object,
  but no classification-free bound yet forces enough high closures among its
  deep--middle wedges for arbitrary real inner products.

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
- Fixed-\(41\) three-point formulation and exact pseudo-distributions:
  [`proofs/fixed41_three_point_formulation.md`](proofs/fixed41_three_point_formulation.md)
- All-degree exact three-point barrier:
  [`proofs/fixed41_bv_all_harmonics.md`](proofs/fixed41_bv_all_harmonics.md)
- Degree-two BV-surviving labeled object and its exact degree-three separator:
  [`proofs/degree2_bv_barrier.md`](proofs/degree2_bv_barrier.md)
- Exact local links and a contact-free maximal code:
  [`proofs/local_link_geometry.md`](proofs/local_link_geometry.md)
- Exact maximum-volume semialgebraic reduction:
  [`proofs/max_volume_semialgebraic_reduction.md`](proofs/max_volume_semialgebraic_reduction.md)
- Degree-two Tverberg constraint and exact rank-five barrier:
  [`proofs/tverberg_moment_barrier.md`](proofs/tverberg_moment_barrier.md)
- Exact antipodal upper bound and unrestricted deep-pair corollary:
  [`proofs/antipodal_bound.md`](proofs/antipodal_bound.md) and
  [`proofs/negative_tail_graph.md`](proofs/negative_tail_graph.md)
- Exact Pfender/local-hybrid inequalities and their surviving mass-41
  two-point witness:
  [`proofs/local_hybrid_barrier.md`](proofs/local_hybrid_barrier.md)
- Reproducible construction round:
  [`experiments/construction_round1.md`](experiments/construction_round1.md)
- Independent layer, higher-root-map, projective-line, and sharp
  deep-graph construction searches:
  [`experiments/construction_round2/RESULTS.md`](experiments/construction_round2/RESULTS.md)
- 152 unrestricted Riemannian augmented-Lagrangian trials and complete
  numerical diagnostics:
  [`experiments/construction_round3/README.md`](experiments/construction_round3/README.md)
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
- Contact-clique links have exact bounds \(15,7,4,2,0\), and every pair has at
  most seven common contact neighbors.
- Every antipodal five-dimensional kissing code has at most 40 points.
  Consequently the \(<-1/2\) graph of a hypothetical 41-code is triangle-free,
  has independence number at most 20, and has at least 23 edges.
- Every hypothetical 41-code admits the exact compact 190-variable
  maximum-volume formulation recorded in the semialgebraic certificate.
- The fixed-41 rational pair/triple pseudo-distribution passes all ordinary
  and Bachoc--Vallentin three-point harmonic inequalities at every degree,
  with unrestricted radial test functions.  An independent adversarial audit
  rederived the endpoint normalization, parity recurrence, finite/tail
  coverage, norm argument, and arbitrary-radial factorization and found no
  mathematical gap.
- Every genuine Gram source satisfies the exact residual-vector square
  inequality displayed above; its negative value on the labeled pseudo-object
  is independently recomputable in rational arithmetic.

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
- “An inclusion-maximal code must have contacts or a positive minimum contact
  degree”: **refuted** by an exact 26-point inclusion-maximal code whose
  contact graph is empty.
- “Matching first and second moments on three disjoint Tverberg parts is
  contradictory for a five-dimensional kissing code”: **refuted** by an exact
  18-point rank-five code partitioned into three regular simplices with common
  moments \(m=0,M=I/5\).
- “The fixed-\(41\) three-point relaxation is already infeasible at low
  degree, or eventually becomes infeasible at high harmonic degree”:
  **refuted** for the complete formulation used here by the all-degree exact
  rational pseudo-distribution.
