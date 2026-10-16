# Adversarial operator-algebra / Fock-sector audit

**Verdict: PASS for this family.** No operator-algebra, Fock-domain, normalization, ordering, phase, adjoint, state-quantifier, or topology defect was found in the frozen `bounded_region_v2` proof. This verdict verifies the operator conclusion given the precise uniform free-leakage input identified below. It is not a replacement for the separate PDE-family verification of that input, and it makes no historical-priority or current-openness finding.

Problem 30006191 / OWR-14299085-005; claimed-solved draft PR 908. Original candidate remains **1/5**. This review is verification, not a new proof attempt.

## Exact input and independence

The reviewed author proof has 12,771 bytes and SHA-256 `2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350`. The package manifest hash is `828280cc131c38e1f651b48b655dff177f880ba3505bba54e049510d81827795`. All 25 files listed by that manifest match their declared bytes and hashes; including the manifest, the original packet has 26 files. The frozen proof hash remained unchanged at the final checkpoint.

Read order was: original proof; saved private statement/identity preflight; official primary report; independent reconstruction and independently authored finite-Fock controls; only then the old v2 audits and verification code. The independent reconstruction was saved before consulting those old reviews/code. They agree with this family's findings, but their verdicts were not premises of this review. The old legacy packet, private source directory, and historical-priority question were not processed.

All writes are confined to this review directory. No Git mutation, candidate/PR/Sheets edit, publishing, release, or outside communication was performed. Internal status updates to the coordinating agent were permitted by the assignment.

## Exact hypothesis and success criterion

The original claim fixes `h=-Delta` on `L^2(R^3)`, the interaction ball `Lambda=B(0,4)`, one smooth real even compactly supported plateau potential, and one normalized smooth compactly supported test function `f`. The Hamiltonians are the maximal sectorwise direct sums

    H^(sigma) = direct_sum_n [T_n + L_n(L_n-sigma)], sigma=0,1.

The explicit orthonormal packed Slaters `Psi_N` and `Xi_N=a^*(f)Psi_N` are allowed to vary with N. At `t_N=pi/(2N+1-sigma)`, success means

    ||[exp(it_N H)a(f)exp(-it_N H)-a(f)]Xi_N|| -> 2,
    ||exp(it_N H)a(f)exp(-it_N H)-a(f)|| -> 2.

The family audit also checks the maximal norm upper bound, both field-expression conventions, genuine state normalization, and preservation of fixed-vector strong continuity. A fixed-vector discontinuity would contradict Stone continuity and would be fatal. None is claimed.

## Mechanism and verified mathematical chain

The complete checkable reconstruction is in `INDEPENDENT_DERIVATION.md`. The route uses large local particle number to create a reference phase difference across adjacent sectors while the physical evolution remains close to the reference on two particular initial vectors. The operator norm permits these vectors to change with particle number.

| Step | Independent verification | Result |
|---|---|---|
| Density ordering | Coordinate number-density measure yields the ordered all-pair sum; CAR normal ordering removes exactly `V(0)L_n`. For the plateau this is `L_n^2` versus `L_n(L_n-1)`. | Pass; no missing diagonal, sign, or half coefficient. |
| Fock realization | A real bounded permutation-invariant potential on each sector is a bounded perturbation of its free Laplacian. Its norm may grow with n. The maximal direct-sum domain gives a self-adjoint Fock operator. | Pass; vacuum and one-particle edges covered. |
| Fixed observable and states | CAR proves norms of normalized creation/annihilation equal one. Disjoint supports imply `a(f)Psi_N=0`, unit `Xi_N`, and `a(f)Xi_N=Psi_N`. | Pass; no null or unnormalized witness. |
| Leakage moments | Independent particle-hole exterior expansion gives `||dGamma(q)Phi||^2=lambda^2+Tr(Pq(1-P)q)`, hence `Var<=lambda`. | Pass for Slaters, including non-diagonal compression; explicitly false for arbitrary states. |
| Reference comparison | The sector difference is `-M_n(2n-sigma-M_n)`, bounded on each sector by `2n M_n`. Strong Duhamel uses only the freely evolved reference Slater. | Pass; no interacting state is assumed Slater. |
| Adjacent-sector comparison | Moving unitaries to both initial vectors and telescoping yields the sum `E_(N+1)+E_N`. | Pass; neither error can be silently omitted. |
| Phase and overlap | The scalar gap is `2N+1-sigma`; free covariance uses `exp(ith)f` with inner products linear in the second variable. CAR reduces the overlap without requiring evolved-f orthogonality. | Pass for both conventions. |
| Annihilation conclusion | The conjugate dual matrix element tends to `-2`; unit-vector lower bound plus norm upper bound 2 gives both requested limits. | Pass; the actual `Xi_N` is a witness. |
| State-level statement | `omega_N(D_N^*D_N)=||D_N Xi_N||^2` tends to 4. | Pass on `B(Fock)`; no CAR invariance assumption. |
| Topology and quantifiers | Every fixed vector and every fixed normal state remain continuous; increasing N witnesses failure of uniformity over unit vectors. | Pass for the intended operator norm. |

The positive product in the state-level expression need not belong to CAR if invariance is unavailable. It is a bounded operator on Fock space, so its expectation in a genuine vector state on `B(Fock)` is well defined. Restriction gives a state on CAR whenever only CAR elements are evaluated. No proof of invariance or non-invariance is smuggled into the argument.

## Interface to the independent analytic family

The precise analytic input needed by the operator proof is original equation (6), uniformly for both the N- and N+1-particle initial Slaters:

    lambda_n(s) = <exp(-isT_n)Phi_n, M_n exp(-isT_n)Phi_n>
                <= C s^2 n^(5/3).

The CAR second moment and sector Duhamel then rigorously imply

    E_n(t) <= C [n^(11/6)t^2+n^(8/3)t^3],
    E_N(t_N)+E_(N+1)(t_N) <= C [N^(-1/6)+N^(-1/3)] -> 0.

These quantities are sufficient: no mixed-state comparison, probability-only control, interacting Slater preservation, or uniform-in-n bounded potential is needed. The independent analytic family must certify uniformity of that input and its continuum/domain justification. This review isolates that obligation and verifies every subsequent operator implication. There is no extra hidden operator requirement beyond it.

A useful quantitative consequence is

    ||D_N Xi_N+2Psi_N|| -> 0,

which follows directly from the scalar witness and the uniform norm bound; it confirms the limiting annihilation direction as well as its norm. This is a corollary of the reviewed evidence, not a newly attempted solution mechanism.

## Actual checks performed

The independent standard-library Python implementation constructs complete occupation-basis CAR matrices and exterior products without importing the original verification code. It uses deterministic seed 30006191. **148 controls passed**, with maximum positive-control residual **1.8874e-15** at tolerance 3e-11. The controls include:

- Ten complex non-diagonal occupied/leakage projection cases for first/second moments and exterior determinant counting identities.
- Full CAR on six modes and free covariance under a nontrivial mixing group.
- Both sector-phase conventions at generic and prescribed times, including explicit nonzero occupied overlap of the evolved test orbital.
- Density versus normal-ordering and vacuum/one-particle controls, exact adjoint witnesses, and vector-state values of four in the zero-kinetic reference model.
- Deliberate wrong covariance sign, wrong sector-phase sign, omitted normal-order shift, and a half-pair coefficient rejected by controls.
- Concrete rejection of a generic correlated-state variance bound and a comparison using only the N-sector error.
- Exact rational checks of the two decay exponents.

Finite-mode calculations test algebra, conventions, and normalization. They are not empirical evidence for continuum localization and do not establish the infinite-N theorem. The infinite-dimensional implications are the analytic deductions in the reconstruction.

The original author verifier was inspected and replayed with the local `python3`, without private-source arguments. It exited zero, and its stdout is saved as `AUTHOR_REPLAY.json`. This replay validates the public author manifest and its stated finite sanity checks, not private source PDFs. The default Python lacks NumPy; no installation was needed because this family's implementation is dependency free. The old NumPy/SciPy v2 controls were inspected, and their saved results read, but they were not rerun in this family. Old saved counts are not included in this family's 148 controls.

Reproduce this family's independent controls from any working directory by running `python3` on the absolute path to `independent_checks.py`. The output JSON is written next to that script. Input package integrity is recorded separately in `INPUT_INTEGRITY.json`.

## Adversarial findings, boundaries, and disposition

No critical, major, or minor mathematical defect was identified in this family's scope. No proof repair or additional proof attempt is required for the operator-algebra steps. The following tempting extensions are invalid or unsupported and remain explicitly outside the claim:

- The Slater variance bound cannot be transferred to arbitrary interacting states. A four-particle inside/outside superposition has mean leakage 1/4 but variance 15/16.
- The two-sector comparison cannot be reduced to one error. A phase flip on only the N+1 sector changes the matrix element by 2 while the N-sector error is zero.
- Fixed-vector SOT discontinuity and fixed-normal-state quadratic discontinuity are impossible for this self-adjoint conjugation. The sequence of witnesses escapes to increasing sectors.
- On each fixed adjacent-sector block norm continuity holds, with a bound by the free single-orbital norm difference plus sector-bounded perturbation errors. The failure is not visible at any one fixed particle number.
- No fixed-density thermodynamic result, all-potentials result, all-regions result, CAR non-invariance result, or d=1,2 result follows.

The source-scope check is detailed in reconstruction section 7, with the official primary report linked there. It admits the stated existential fixed-region norm-discontinuity witness. No source-imposed density constraint has been found that would exclude these states.

**Strongest family-verified result:** if the stated uniform free-leakage bound holds for the original two Slater families, the frozen theorem's complete annihilation norm, creation norm, and varying-vector-state conclusions follow rigorously for both sigma=0,1, while all fixed vectors and fixed normal states remain continuous. The whole claimed-solved disposition should combine this PASS with the independent continuum/PDE and source/provenance/priority-family dispositions. No new proof search was undertaken and the candidate budget remains 1/5.
