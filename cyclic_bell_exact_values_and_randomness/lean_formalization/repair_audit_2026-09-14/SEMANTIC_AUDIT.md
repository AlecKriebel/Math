# Independent semantic audit of the offline candidate

Checkpoint: 2026-09-15 03:25 UTC (2026-09-14 Pacific).

Audit scope: manuscript correspondence, quantifiers, dependencies, hidden premises,
and omitted claims. The initial independent audit preceded compilation; its
findings are preserved below with explicit repair status. Subsequent work added
and normally compiled the source coefficient/PVM/polar/attainment chain and
independently reviewed the repaired general polar, permutation, and exposure
coverage. The source endpoint axiom report contains only propext,
Classical.choice, and Quot.sound. Full clean package certification remains the
parent task's responsibility. A percentage of compiled files is not a
percentage of the paper's mathematical difficulty.

## Conclusion and current status

The **incoming offline package was not a full formalization**, even if all its
supplied candidates had compiled. Several named mathematical statements were
absent and some aggregate endpoints were incomplete. Follow-up modules now
repair the canonical polar lemma, the actual source coefficient strategy,
general commuting permutation bounds and local moments, and the exposure
correspondence. Exact source simple spectra now have a successful normal build and independent
semantic review in GeneralCoverageSourceSpectrum. The actual Qqa⊆Qqc
ultralimit/GNS construction has also been independently reviewed. Final clean
whole-package compilation and axiom verification remain parent release checks;
this report records semantic correspondence and bounded compilation evidence.

The inspected principal endpoint signatures do not contain an obvious circular
maximality assumption or hidden restriction to the displayed witness. The
written proof mechanisms for the first bound, support rigidity, and three-model
value assembly are mathematically coherent at the level inspected. This is
evidence about proof design, not evidence of Lean acceptance or a claim that all
1,132 candidate proofs were independently checked line by line.

## Source identity

The local manuscript really has SHA-256
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`
and Git blob `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
Both were recomputed from `../main.tex`, rather than accepted from the handoff.
Thus this candidate targets the actual current combined manuscript source.

## Principal chains inspected

### Physical validity and universal finite-dimensional bounds

`GeneralModel.StateOn` has a positive matrix and trace-one normalization.
`Measurement` has positivity, completeness, idempotence and orthogonality.
`StrategyOn` adds only state and measurement choices. None assumes the Bell
value, equality phases, target probabilities, or a desired support rank.
Zero outcome projectors remain allowed. Arbitrary finite local coordinate types
are used, not only `Ix d`. Empty local types cannot supply a trace-one state;
this does not create a vacuous witness because the explicit nonempty strategy
is separately constructed.

`first_physical_upper` derives encoded unitarity, uses tensor lifts to derive
cross-party commutation, and applies a mixed-state trace-positive SOS. Its
relative unitary is genuinely `A0† * A1`. The supporting `first_matrix_sos`
does not assume a favorable spectrum or that different Bob observables commute.

### Arbitrary-Hilbert first-family upper bound

`GeneralCommuting.first_cstar_sos` uses arbitrary C*-algebra unitaries and only
Alice/Bob commutation. `first_commuting_hilbert_bound` specializes to arbitrary
complete complex Hilbert spaces, without `FiniteDimensional` or a tensor
factorization assumption. The exact SOS is stronger than a scalar estimate.

The mechanism in `GeneralFunctionalCalculus` uses continuous functions
`h(z)=sqrt(norm z)` and `k(z)=z/h(z)`, with `k(0)=0`. The displayed norm argument
establishes continuity at zero, and the cross identity does not divide by a
vanishing value. Functional-calculus commutation is intended to follow from
unitary conjugation and uniqueness. Therefore the route does not silently
assume an invertible polar factor. Actual pinned Mathlib API elaboration remains
a compiler question.

### Support rigidity

`supported_multiplicity_rigidity` assumes an arbitrary finite physical strategy
and equality of its actual first augmented score. It concludes invariance under
both `U` and `U†`, equal positive root multiplicities on `aliceSupport`, and the
dimension formula. `aliceSupport` is the actual reduced-state support, not a
space chosen to make the conclusion true.

The examined dependency chain is:

1. `first_saturation_equations`: nonnegative SOS expectations vanish separately;
   a positive square root of the actual mixed state supplies its purification
   amplitude.
2. `equalitySupport_from_gap`: finite spectral zero transfer restricts that
   amplitude to the scalar equality set.
3. `polar_cancel_on_support`: a supported inverse cancels only on that set;
   the stabilizer puts `A†T` in the appropriate supported range.
4. `quantum_supported_routing`: Bob's actual transpose-lifted order-d observables
   provide the intertwiners, including `UT=T(DB0†)^2`.
5. `quantum_root_rank_lower`: adjacent polar phases supply the reflection
   relation and the order-d power equations.
6. `relative_reflection_rank`, full supported spectral decomposition, and
   `equal_ranks_from_lower_bounds`: rank inequalities and their sum force equal
   multiplicities.

The reflection or equality-spectrum hypotheses are not handed to the final
physical theorem by the caller. The rank lemma is consequently not being
misrepresented as the entire support theorem. No assertion is made on the
unused ambient complement.

### Model values and adversarial domains

`Qq` is the set of behaviors of arbitrary finite-dimensional mixed-state PVM
strategies. `Qqa` is its actual topological closure. `Qqc` is defined using
complete complex Hilbert spaces and commuting PVMs; the `Type` universe
convention is not a finite-dimensionality assumption.

`bellSupremum` is an actual real `sSup`, not a name for the desired constant.
`bellSupremum_of_attained_bound` explicitly supplies nonemptiness and boundedness.
`three_model_suprema` uses the finite-to-commuting inclusion, the commuting upper
bound, an actual finite attaining witness, and continuity to bound the closure.
This route validly avoids any dependency on the missing `Qqa ⊆ Qqc` theorem.

`GuessQa` takes the closure of *extended* finite correlations before restricting
to the maximal Bell-score slice. It is not defined as arbitrary extensions of a
closure-marginal, nor as the closure of finite saturators. The q and qc domains
contain actual Eve POVMs. The claimed guessing results are lower bounds, not an
assertion that the displayed witness is worst-case optimal.

## Semantic coverage gaps and repair status

### 1. Canonical polar positive-factor lemma — repaired

Independent follow-up review of `GeneralCoveragePolarCanonical` confirms that
`canonical_polar_hilbert_positive_factor_identity` uses literal nested CFC square
roots on an arbitrary complete complex Hilbert space. Its hypotheses give the
polar factorization and canonical initial-isometry defining property, which the
manuscript's assumed canonical polar decomposition supplies. It derives support
propagation to square roots via the C*-zero-norm identity, both transported
moduli via positive square-root uniqueness, and commutation from the stated
commutation with C. No cross identity, square-root commutation, inverse, or
nonzero-spectrum hypothesis is assumed. Thus the named conditional polar lemma
is covered; an independent existence theorem for canonical polar decomposition
is not asserted by this endpoint and is not required by the lemma's formulation.
The owning agent reports a successful normal build; final clean axiom audit is
still the parent task's responsibility.

### 2. General framework inclusion Qqa⊆Qqc — construction reviewed

GeneralCoverageClosureContainment now states the literal inclusion with only
finite Alice/Bob input assumptions, the scope of every scenario in the paper.
The independent review followed its actual dependency chain: bounded Gram
kernels of words in the source PVM projections are passed through an
ultrafilter extending atTop; finite quadratic forms preserve positivity.
GeneralCoverageGNS equips the algebraic word span with the resulting
seminorm/inner product and takes its separated Hilbert completion.

Prepending each PVM generator is proved contractive on the limiting kernel and
extends to a bounded operator. Dense-span arguments derive selfadjointness,
idempotence, same-input orthogonality, completeness, and cross-party
commutation. The empty word is normalized. Length-two moments reproduce the
ordinary behavior limit, giving an actual CommutingOn model. Finally sequential
closedness gives closedness for the finite behavior coordinate space, and
closure_minimal proves the desired inclusion. No limiting realization,
closedness, embedding, or desired correlation is assumed in a validity field.
The mathematical gap is repaired by this construction; final compiler/axiom
status belongs to the parent release audit.

### 3. Canonical source strategy — repaired

The repaired GeneralSourceFourier correctly spells out the source coefficient
sum using forward X, positive clock Z, and the integer triangular exponent.
Independent normal builds now check all d≥2 signs and the d−1 wraparound in
GeneralCoverageSourceWeyl, SourceInterpolation, and SourceLiteralInterpolation.
SourceFactors proves actual sourceBob unitarity from its literal coefficients,
not from a desired Bell value. SourceOrder proves its dth power equals identity
using all-n actual CFC covariance, the ordered noncommutative product identity,
and the scalar full orbit product.

GeneralCoverageSourceCanonical constructs the actual positive invertible H_y,
identifies it with both CFC.sqrt(L_y† L_y) and CFC.sqrt((1+W_y)†(1+W_y)), and
proves the exact source coefficient identity with the conjugate polar factor.
It also proves the literal Q_y=G(1+W_y†)Z† formula with an explicit two-sided
inverse G. Thus the missing coefficient/PVM-validity dependency is repaired
without circular reliance on Fourier-sum attainment.

GeneralCoverageSpectralMeasurement independently packages every order-d
unitary into positive complete pairwise orthogonal spectral PVMs with exact
encoding. GeneralCoverageSourceStrategy now compiles and instantiates these
with the actual source matrices, proving firstValue=M_d+1 using the actual
maximally entangled state and the two checked source Fourier sums. Full simple
spectra for W_y and sourceBob now pass a normal build in SourceSpectrum and an
independent semantic review: its actual normalized phase basis, clock-shift
action, unitary similarity, and transpose rank transfer preserve all source
phase and transpose conventions.
Final clean rebuild and transitive axiom reporting remain required.

### 4. Conditional phase-permutation theorem — repaired

Reviewed GeneralCoveragePermutation supplies `linear_cstar_sos` in an arbitrary
C*-algebra and reduced/augmented bounds on an arbitrary complete complex
Hilbert space. The scalar cap and phase/product assumptions remain explicit,
as required by the genuinely conditional manuscript theorem. Functional
factors are constructed by actual continuous functional calculus, including
zero affine factors; no unsupported factor identities are assumed.

`linear_permutation_local_moments_zero` states all local complex first moments
for both parties; `linear_permutation_all_harmonics_invariant` covers both
Alice inputs and every Bob input, including the added alignment input.
GeneralCoverageWitness independently exposes one-dimensional weighted-cycle
eigenspaces. These fill the missing aggregate semantic coverage; original
matrix witness and upper bounds remain valid supporting theorems.

### 5. Computational-MUB correspondence — repaired with an alternate proof

Reviewed GeneralCoverageExposure supplies the Hermitian spectral-to-Loewner
bridges, the real Fourier/diagonal operator-space representation, and
`computational_MUB_spectral_obstruction`: unless the operator is scalar, a
computational eigenvalue has spectral values strictly on both sides. It also
proves the actual computational-PVM coefficientwise saturation implication
using the maximally entangled Born trace, not a formal surrogate table.

The implementation uses the stronger constant-diagonal obstruction rather
than translating intermediate Toeplitz/SVD calculations line by line. It
establishes the manuscript's stated scientific conclusion with an alternative
proof. It does not claim a universal obstruction to extra measurements or a
joint Bell SOS, which would exceed the manuscript's coefficientwise scope.

### 6. Declared boundaries which are not missing new scientific claims

The external self-testing theorem cited by the settings appendix is prior work;
the candidate derives the displayed explicit phase-basis tables, anchor table
and observational entropy rather than formalizing that external theorem or
its isometry/convention transport. This needs a clear external-dependency
boundary, not a claim that canonical tables certify arbitrary realizations.

An exact worst-case value-conditioned guessing optimum and attainment for an
arbitrary-Hilbert Eve are not established. The paper claims lower bounds and
finite-dimensional privacy, so those absent stronger results should not be
invented as required endpoints. The binary finite-purification restriction
agrees with the manuscript framework's explicit finite-dimensional privacy
scope. Its actual `BinaryPrivacyAt` statement quantifies over all compatible
finite purifications, and witness/purification constructions make the claimed
achievable privacy nonvacuous.

## Acceptance conditions

1. A clean build must import every endpoint advertised as certified, with
   recorded actual axiom dependencies and no unproved mathematical premises.
2. Existing quantifiers and physical model definitions must survive repair;
   syntactic fixes must not silently weaken a universal or physical theorem.
3. Resolve the gaps above, or give an explicit claim-by-claim partial-coverage
   report. Compilation and full manuscript coverage are separate conditions.
4. Keep observational entropy, fixed-realization guessing, and value-conditioned
   adversarial bounds distinct in the reviewer guide.
5. After repairs, perform a second audit of changed endpoint signatures and the
   exact proof dependencies; this report concerns the incoming source design.

No outside communication or Git modification was performed by this audit agent.
The initial audit did not edit Lean source. A subsequent parent assignment asks
for new source/polar bridge implementation; its files and compiler evidence are
separate from this audit of the incoming candidate. No external scientific
novelty assessment was attempted.
