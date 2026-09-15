# Independent semantic audit of the offline candidate

Checkpoint: 2026-09-15 03:25 UTC (2026-09-14 Pacific).

Audit scope: manuscript correspondence, quantifiers, dependencies, hidden premises,
and omitted claims. This audit does not certify compilation. The parent task is
running the compiler and repairing source independently. Estimated completion of
this bounded semantic audit: 90%; estimated kernel certification established by
this audit itself: 0%. A percentage of compiled files is not a percentage of the
paper's mathematical difficulty.

## Conclusion

The package is **not a full formalization of the manuscript**, even if every
currently supplied candidate were to compile. Several mathematical statements
are absent, and a few advertised aggregate endpoints capture only part of the
corresponding manuscript theorem. The incoming documentation generally discloses
the large omissions; it must not be replaced by a blanket whole-paper claim.

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

## Gaps which remain even after successful compilation

### 1. Canonical polar positive-factor lemma is not formalized

Manuscript `lem:polar` quantifies over arbitrary bounded `C` in one of two
commuting unital *-algebras and uses its **canonical** polar partial isometry,
support projections, and modulus square roots. The code proves an alternate
half-polar identity adapted to the relative-unitary functional calculus.
`halfPolar_gap_identity` / `algebra_halfPolar_gap` assume the factor identities;
the following functional-calculus constructions discharge them for the cyclic
case, but do not construct the canonical polar decomposition for general `C`.

Repair: implement the full bounded-operator canonical polar factor and its
commutant/support properties, then the literal lemma; or explicitly label the
formalization as covering the major conclusions by alternate proofs while
excluding this named manuscript lemma. An alternate proof of `thm:exact` alone
does not certify every intermediate lemma in the manuscript.

### 2. General framework inclusion `Qqa ⊆ Qqc` is absent

The manuscript explicitly displays this inclusion. Only `Qq ⊆ Qqa` and
`Qq ⊆ Qqc` are supplied. Their conjunction does not imply the missing inclusion.

Repair: formalize an appropriate compactness/GNS/closedness argument for the
actual behavior sets, with explicit finite input/output assumptions as needed.
Do not add this inclusion as a model-validity field. This is separate work and
does not block the already designed specific Bell-value equality proofs.

### 3. Canonical source strategy and polar identification are absent

`GeneralSourceFourier.sourceBob` correctly spells out the source coefficient
sum using forward `X`, positive clock `Z`, and the integer triangular exponent.
The source coefficient DFT, two source Fourier sums, and qutrit expression are
written. There is no candidate showing that these source Bob matrices form the
stated order-d PVM encodings, nor their equality to `Q_y^T = conjugate(V_y)`.

The appendix's uniqueness-via-polar-deficits argument requires source-observable
unitarity first; the two Fourier sums alone cannot supply it. The existing
weighted-cycle permutation witness proves the value independently but does not
identify the distinct source-Z/source-X strategy.

Repair: construct the canonical source `W_y,H_y,V_y,Q_y`, prove order, full
spectrum and literal coefficient equality, then package the corresponding
actual state/PVM/Bell attainment theorem. In particular, do not infer source
unitarity merely from a first-harmonic sum attaining the desired numerical value.

### 4. Conditional phase-permutation theorem is only partially assembled

`conditional_permutation_theorem` concludes attainment, comparison with finite
coordinate competitors, and the `A0/Br` harmonics. Its supporting
`linear_permutation_harmonics` does include `A1/Br`; the generic cycle module
also includes the added-setting harmonics. However, the manuscript additionally
claims all local first moments, every added-setting correlator, and an operator
upper bound in the commuting framework.

`GeneralCycles.weighted_trace_zero` supplies zero weighted-cycle trace (found
in the implementation follow-up); the physical local-moment and aggregate
endpoint wrappers remain to be assembled. The general linear upper-bound proof
is matrix-only, unlike the specifically cyclic first bound. The orthonormal eigenvector package contains ingredients
for the full simple spectrum, but its endpoint does not literally state
one-dimensionality of every eigenspace.

Repair: use the existing zero-trace lemma to derive local moments for `d>=2`;
assemble both ordinary and
added first-harmonic invariances; expose simple spectrum explicitly from the
complete orthonormal eigenbasis/characteristic polynomial; generalize the
linear-factor SOS to arbitrary C*-algebras by the same continuous-factor route.
The scalar cap and phase/product hypotheses are legitimate because the paper's
theorem is itself conditional; do not remove or falsely advertise them.

### 5. Computational-MUB result needs correspondence wrappers

`GeneralExposure` proves a sound and stronger constant-diagonal obstruction:
if the eigenvalue's corresponding upper or lower Loewner difference is positive,
the matrix is scalar. The final source specialization spells out the displayed
diagonal phases. This is an alternative to the manuscript's Toeplitz/SVD proof.

For a literal manuscript claim, add the bridge from Hermitian spectral extrema
to the Loewner inequalities, membership/representation of the manuscript's
operator space, and the stated coefficientwise-exposure consequence. The
intermediate wraparound/SVD identities have not themselves been translated.
Do not present a coefficientwise spectral obstruction as a universal no-go
theorem for extra measurements or a joint Bell SOS.

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
