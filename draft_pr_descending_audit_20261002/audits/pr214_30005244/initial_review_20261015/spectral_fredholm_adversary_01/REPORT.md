# Independent spectral/Fredholm/Riesz adversarial report

PR214 / 30005244 / OWR-11101924-008; submitted head
36d5ef15098163e74bf14c2e696f560ce592affd; author turn count 2/5.

**Assigned-family verdict: PASS, with explicit application dependencies.** No
material error was found in the submitted abstract off-interval mechanism or in
its transfer to the continuum-support masks of TURN_2. This is not a full-source
solution, novelty, kernel-consistency, or ball-perturbation certification. Those
are separate audit families. No author repairs were made or searched for.

The checkable independent proof is INDEPENDENT_RECONSTRUCTION.md. It was sealed
before any inherited independent-review or FINAL_DISPOSITION verdict was read.
Those verdicts remained unread throughout this family's work. Reading order was
applicable instructions, submitted CANDIDATE and TURN_2, original OWR contribution
and primary CDN static passages, independent reconstruction, then additional
source rendering and adversarial finite-block computations.

## Target and primary source

The full original contribution is Martin Costabel, joint with Monique Dauge and
Khedijeh Nedaiasl, OWR 43/2022, printed 2580--2582 (PDF 70--72), DOI
<https://doi.org/10.4171/owr/2022/43>. It gives the diagonal-omitting cubic-grid
matrix, the comparison with A_kappa minus I/3, and asks for a precise description
and proof of the observed nonreal isolated-eigenvalue approximation outside the
static accumulation interval. It does not supply a regularity hypothesis in the
compact-support wording. This family certifies the functional-analysis step
under the hypotheses the submission explicitly states; the correct interpretation
of the source's particle scope remains with the source-scope audit family.

CDN arXiv:2302.13159v3 (22 October 2023), Sections 1.2, 1.6, 2.1--2.2 and
2.4, equations (3.41)--(3.42), Lemma 3.14, and Proposition 3.15 were read for
the imported static result. In particular Proposition 3.15 gives real bounds
Lambda_- <= -1/3 and Lambda_+ >= 2/3 for d=3, the finite-matrix numerical-range
bound, and the resolvent estimate. Lemma 2.7 and the matrix-valued discussion
identify the closed numerical-range interval of the bounded lattice operator.
Thus the exact interval, not rounded numerical endpoints, is a valid imported
input for this mechanism. The primary manuscript, not a secondary summary, was
used. The abstract analytic-Fredholm step was derived by a finite-dimensional
analytic Schur complement in the independent proof; no uninspected theorem
source was imported for that step.

## Claim-by-claim findings

| Claim or potential failure | Finding |
| --- | --- |
| B_h selfadjoint, spectrum in exact I_lat | Valid conditional on the CDN lattice input. Compression preserves its quadratic-form bound; adjoining zero is allowed because 0 is in the interval. |
| Matrix/common-space equivalence | Valid. The occupied-cell space is finite dimensional, the kernel maps into it and kills its orthogonal complement, and h^3 changes the squared vector norm by one scalar only. |
| Static strong convergence as a premise | The submission supplies a separate proof in CANDIDATE lines 79--116. This family read its mechanism but does not certify the lattice/kernel estimates independently; that is the kernel family. |
| Compact correction norm convergence as a premise | The submission supplies the separate Hilbert--Schmidt argument at lines 118--158. Exact finite-matrix identification is correct. Taylor and lattice estimates remain independently checked by the kernel family. |
| Strong static resolvent convergence, uniformly on spectral compact sets | Valid by the resolvent identity, common distance-to-I_lat bounds and finite nets. |
| Left compact multiplication | Valid by finite-rank approximation. |
| Right compact multiplication | Valid because selfadjointness supplies strong convergence of the adjoint resolvents. The submission expressly uses this at lines 202--206. Ordinary strong convergence alone would fail. |
| Analytic Fredholm connectedness/invertibility | Valid. C minus a bounded real interval is connected, and sufficiently large spectral parameter gives an invertible point. A local finite-dimensional Schur reduction gives isolated poles with finite-rank principal parts. |
| Uniform resolvent bounds/no pollution off I_lat | Valid by uniform norm convergence of the compact Fredholm factors and a Neumann-series inverse on every compact continuum-resolvent subset. |
| Norm convergence of Riesz projections | Valid. Integrate away the static resolvents, which are analytic throughout the disk; compact resolvent remainders converge in norm. Full resolvent norm convergence is neither claimed nor needed. |
| Algebraic multiplicity, defective clusters | Valid. Projection distance below one gives equal ranks. For a genuine resolvent pole the rank is the finite algebraic multiplicity, even for a defective eigenvalue. |
| Generalized subspaces | Valid for the total isolated cluster and in the two-sided gap sense. It does not preserve Jordan block structure or the individual subspaces of eigenvalues after splitting; the submission does not need those stronger statements. |
| Eigenvalue cluster convergence | Valid by repeating the argument for smaller circles and excluding the intervening compact annulus. |
| Escaping eigenvalues and subsequences | Uniform operator bounds prevent escape to infinity. The argument applies on every mesh sequence/subsequence satisfying the stated consistency premises; it says nothing universal for sequences that fail them. |
| TURN_2 continuum masks | Valid conditional on the nonreal ball eigenvalue and the dynamic L2-kernel premise. Strong static convergence and Hilbert--Schmidt convergence of the corrections suffice. Static norm convergence is not needed. |

## Zero eigenspaces and mask transfer

The common-space zero extensions have an **infinite-dimensional** zero
eigenspace. It would be erroneous to regard the globally extended static ball's
zero Riesz projection as rank three. TURN_2 explicitly constructs that rank-three
projection on L2(B), where the claimed static gap is proved, and uses global
extensions only later for a disk around a nonreal eigenvalue. Such a disk misses
I_lat and zero. The added zero complement contributes no Riesz rank to it, so
the transport argument is valid if the ball calculation is valid.

For the specific nested F_j, volume removal tends to zero and the masks converge
almost everywhere to the ball mask, apart from null sets. Hence M_j D M_j
converges strongly and strongly in the adjoints, with all spectra in
[-1/3,2/3]. Dominated convergence for the square-integrable dynamic kernel
gives Hilbert--Schmidt convergence. Apply the same independent abstract theorem.
The resulting nonzero off-real projection forces a nonreal eigenvalue on F_j.
This step neither asserts that the pathological F_j have consistent DDA voxels
nor infers a static operator-norm estimate from a volume bound.

## Falsification checks and exact remaining dependencies

The independent proof records explicit infinite-operator counterexamples to
four tempting weakenings: full norm resolvent convergence from strong static
convergence; right compact multiplication without strong adjoints; replacing
compact norm convergence by strong convergence of compact corrections; and
static norm convergence from small support removal. It also records the
elementary split of a defective Jordan block. None contradicts the submitted
argument, which uses the required stronger premises.

checks.py additionally realizes an off-interval defective cluster coupled to a
moving coordinate. All assertions passed. The cluster retains total algebraic
multiplicity two, while its Riesz-projection norm gap falls from about 0.02816
to 0.0001092 as the compact error falls from 1/16 to 1/4096. At the same time
the full resolvent norm gap stays above 0.1. Doubling the contour resolution
changes projections by less than 5.3e-15. These computations illustrate the
mechanism; the independent derivation is the proof. The first invocation with
the system Python lacked NumPy; the bundled runtime then ran the unchanged
check successfully. CHECK_RESULTS.json records the successful values.

Strongest independently verified result: the full abstract spectral theorem
and its mask-transport application under the explicit kernel/ball premises.
Exact remaining dependencies for the whole candidate: the static and dynamic
kernel-consistency estimates, the ball spectral/quantitative perturbation
argument, and the source-scope/novelty assessment. This report does not convert
those dependencies into assumptions about the final audit disposition.

Assigned audit-family completion estimate: **100%**. No broad priority audit,
external communication, provider state change, Git/index/ref mutation, queue or
shared-database update, author-input edit, paper/deposit/release, or tracker
mutation was performed.
