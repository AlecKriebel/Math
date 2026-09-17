# Independent semantic audit of commuting-model closure infrastructure

Checkpoint: 2026-09-15T04:09:16.998252+00:00. Assigned semantic scope approximately 60% complete. The four existing infrastructure modules have been inspected; Reconstruction and ClosureContainment are not yet present. This report is read-only source review, not an independent assertion that active proof files have finished compiling.

## Preliminary finding

No circular limiting-positivity, limiting-realization, or quantum-model-closure assumption was found in these four modules. Their mechanism is the ordinary moment-kernel/GNS construction with explicit contraction control.

## Kernel realization and completion

PositiveKernel requires Hermitian scalar entries and nonnegative real quadratic forms for every finitely supported coefficient vector. It does not contain a Hilbert-space realization premise. KernelSpan gives the free finite span the seminorm derived from that quadratic form. The actual UniformSpace.Completion separates its zero-seminorm vectors and supplies a complete normed inner-product space. The embedded basis has exactly the supplied inner products and spans densely. This handles singular/degenerate kernels rather than presuming positive definiteness.

CompletionOperators applies the actual uniformly continuous completion map to a bounded linear operator. Its algebraic laws and inner symmetry are proved on the dense embedded pre-space, then extended by continuity. The input pre-space is allowed to be only seminormed, and boundedness ensures that null directions cannot produce nonzero completed outputs. The identities for idempotence, orthogonality, commutation and finite sums are actual operator equalities; no quantum-model membership is an assumption.

## Genuine ultralimits

ultraLimit is limUnder of a proper Ultrafilter. For every bounded complex family, compactness of its closed complex ball proves existence of a limit, and the actual convergence theorem is used before algebraic or positivity conclusions. The default value of limUnder for a nonconvergent family is therefore never being used as a limit theorem. Finite-sum interchange is finite continuity, and Gram PSD is preserved from eventual PSD of the original kernels. No convergence/PSD of the limiting kernel is supplied as a premise.

naturalUltrafilter is Mathlib's ultrafilter extension of atTop on natural numbers. Its order relation to atTop gives preservation of an ordinary convergent sequence's limit. This is not an assumed subsequence limit and does not require simultaneous sequential convergence of all word coordinates.

## Actual operator moments

MomentModel begins with actual CommutingOn PVM strategies in varying complete Hilbert spaces Hn. Generator norm bounds are derived from self-adjoint projection identities; arbitrary word products are bounded by one. Full polynomial Gram positivity is the squared norm of the actual finite linear combination of word vectors. The prepend quadratic contraction is derived from the source projector acting on that linear combination.

This last contraction is essential: it proves nullspace invariance and boundedness of the eventual left-generator operator, rather than merely assuming a bounded GNS representation exists. The bounded ultralimit transfers that quadratic inequality, normalization, Hermitian symmetry and positivity. Idempotence, same-setting orthogonality, both Alice/Bob finite completeness sums, and every cross-party commutator identity are preserved at arbitrary word contexts. No same-party different-setting commutation is introduced.

The empty/length-two moments are exactly the source behavior coordinates; their ordinary topological limit survives the natural ultrafilter. Thus the eventual reconstruction can recover the requested behavior without assuming a limiting realization.

## Universes and remaining assembly check

The kernel index and input alphabets in GNS/MomentModel are Type (the small universe), matching the existing Qq/Qqa/Qqc definitions. Qqc already quantifies H : Type; this is a size convention and imposes no finite Hilbert-dimension bound. The completed span of all finite words can be infinite dimensional, and the sequence allows varying source carriers and dimensions.

The final closure theorem is intended for finite input alphabets, as in the paper. This permits sequence extraction from the finite real behavior-coordinate topology. A theorem for arbitrary uncountable alphabets would require a different closure argument; no such generality is being credited here.

Still to inspect: construction of every completed PVM and its state; recovery of all behavior coordinates; use of actual source Qqc membership to choose varying carriers/instances; extraction of a sequence from topological closure; final Qqa subset Qqc without a closedness or realization premise. These are substantive endpoint obligations, not completed merely by the infrastructure above.

## Inspected source snapshots

- GeneralCoverageGNS.lean: `2a62284dd17e06fa02ed96ba91deaff0b34a6c74614b39e07306b3d6976872b5`
- GeneralCoverageCompletionOperators.lean: `21376760dee465d617411759de7e3c58bf1682a4adc1ba60ec1cf2910c7b25b6`
- GeneralCoverageUltralimit.lean: `bff088f1db485df7b4e79e2a7ca0527eaed1e416bae00a1ada0d7e124595c520`
- GeneralCoverageMomentModel.lean: `4927760e802f9875c87a67cc3972336ff5ed009f4a6c1090f8584a0b0fd1a988`

## Final endpoint inspection — 100% assigned semantic scope

2026-09-15T04:11:54.130702+00:00 — inspected GeneralCoverageReconstruction, GeneralCoverageClosureSequence and GeneralCoverageClosureContainment. No semantic blocker found. Their compiler integration is still being performed by the responsible agents; this read-only audit concerns mathematical definitions, premises and conclusions.

Reconstruction defines every limit generator by bounded completion of the actual linear prepend map, using the previously derived quadratic contraction. Dense-span matrix coefficient identities then give self-adjointness, idempotence, same-setting orthogonality, both parties' complete finite sums, and all cross-party commutators. The state is the empty-word vector; K([],[])=1 proves its norm is one. This constructs an actual CommutingOn structure. Its complete behavior is then identified with the empty/length-two limiting moments, without a limiting-strategy or operator-law premise.

ClosureSequence uses mem_closure_iff_seq_limit only with explicitly finite input alphabets. Its source sequence lies in the actual finite tensor Qq domain and is embedded through the existing proved finite-to-commuting inclusion. It permits a different carrier and all its instance data at every sequence index.

ClosureContainment proves a slightly stronger intermediate fact: any ordinarily convergent sequence from Qqc has a Qqc limit. It chooses the actual source realizations from each sequence membership, invokes the reconstructedModel, and proves equality at every real behavior coordinate through the complex moment identity. No finite-dimensional source carrier is required for that argument. The final conversion of sequential closedness to topological closedness explicitly assumes Finite α and Finite β; the fixed d outcomes are finite as well. Thus the ambient behavior space has the needed sequential topology. The paper's scenarios satisfy these assumptions.

Finally Qqa_subset_Qqc is closure_minimal applied to the existing, actual Qq_subset_Qqc embedding and the newly proved Qqc_isClosed theorem. The inclusion is independent of a Bell objective, value equality, attainment or a slice condition. There is no circular invocation of the target containment or an assumed realization of the limit. The theorem is not being advertised for arbitrary uncountable input alphabets.

The small Type carrier convention matches the original model definitions and does not impose a finite Hilbert dimension. No rank/full-support assumption, hidden nonzero Gram determinant, same-party commutation condition, or fixed source dimension was introduced. Degenerate kernels are handled by the separated completion.

Final inspected endpoint snapshots:

- GeneralCoverageReconstruction.lean: `ebc0065e14d33d0fd49d12c4a98d3b833aae67462e3aa6cb2ddf902927dc09b7`
- GeneralCoverageClosureSequence.lean: `5fe3a7a765cc457769aa65a238f526ff901a37be3e4b2acf8dd165312542c386`
- GeneralCoverageClosureContainment.lean: `f029b7bda24ea44166069e0b72f6292a1374e4f4a400eb2ea364d69fc2b12988`
