# Physical models and their formal correspondences

The development uses independent source definitions for arbitrary finite outcome labels and for complex Hilbert spaces of local dimension at most two. The representation theorems connect these definitions to the fixed-qubit matrix model used by the main proof. Stochastic processing is separately defined by its actual weighted probabilities and connected to finite mixtures of physical projective strategies.

[The coverage map](CERTIFIED_COVERAGE.md) lists the named endpoints. [CERTIFICATION.md](../CERTIFICATION.md) identifies the full-project verification receipt; this document explains the mathematics and does not establish a separate certification run.

## Fixed-qubit matrix model

In [Quantum.lean](../Bell/Quantum.lean), a local operator is a complex 2×2 matrix, and a joint operator is indexed by `Fin 2 × Fin 2`. A state is a positive semidefinite joint matrix with trace one. A POVM is a positive semidefinite effect family whose sum is the identity. A PVM additionally satisfies idempotence and pairwise orthogonality. Zero effects, zero projectors, and identity projectors are allowed.

For architecture A, a complete behavior is

\[
 p(a,b\mid x,y)=\operatorname{Re}\operatorname{tr}\bigl(\rho(M_{a\mid x}\otimes N_{b\mid y})\bigr).
\]

The real part defines the ambient real-valued table even before positivity assumptions are supplied. On valid strategies, [Expectation.lean](../Bell/Expectation.lean) proves nonnegativity, normalization, and no-signaling.

`Bell.rawPOVM` and `Bell.rawPVM` are ranges of complete physical strategies. Their `convexPOVM` and `convexPVM` counterparts are ordinary convex hulls. They are not closed hulls by definition, nor are they independent entrywise or inputwise convexifications. `Bell.finite_projective_simulation` explicitly provides a finite index set, nonnegative weights of total mass one, and one projective strategy for every index, with equality of entire tables. Each branch may have its own joint state and both parties' full measurement families.

## Arbitrary finite outcome types

[FiniteLabels.lean](../Bell/FiniteLabels.lean) defines independent records `Bell.FiniteLabels.POVM α` and `PVM α`, with matrix effect functions on α itself. For input-dependent types `AO : Fin m → Type` and `BO : Fin n → Type`, its strategies contain these measurement records and the original physical joint state. Their behavior is directly defined by the matrix Born formula, not by first mapping into the cardinal model.

For each input, `Fintype.equivFin` supplies a bijection between its outcome type and the corresponding finite cardinal. Encoding evaluates an original effect at the inverse bijection; decoding evaluates a cardinal effect at the forward bijection. Positivity is unchanged, sums are invariant under the equivalence, and bijectivity preserves both idempotence and off-diagonal orthogonality. The measurement and strategy `encoding` equivalences have checked left and right inverse laws.

`Bell.FiniteLabels.behaviorEquiv` is a real linear equivalence of complete ambient behavior spaces. `Strategy.encode_behavior` and `ProjectiveStrategy.encode_behavior` prove exact agreement with physical strategy encoding. In particular:

- The state and every relabeled matrix effect are preserved.
- Both raw ranges transport exactly, not merely by a one-sided inclusion.
- Ordinary convex hulls transport exactly.
- `finite_mixture_transport` retains every coefficient of a finite mixture.

The principal `two_input_equality` and `at_most_two_input_equality` therefore apply to arbitrary finite input-dependent outcome types. Inputs in this source interface remain `Fin m` and `Fin n`; there is no separate claim here about an independent source model with arbitrary input-label types. The outcome types need only `Fintype` instances. General endpoints do not require nonempty outcome types or user-supplied decidable equality instances.

If an existing input has an empty outcome type, its normalized qubit POVM cannot exist. `no_strategy_of_empty_alice`, `no_strategy_of_empty_bob`, and `empty_hulls_of_no_strategy` make this case explicit. If there are no inputs on either side, there are no measurement obligations; `no_input_strategy` constructs a strategy from any state even when the unused outcome family is `Empty`. Having no inputs on only one side does not remove the other side's measurement obligations.

## Independent Hilbert-space source model

The source types in [HilbertCorrespondence.lean](../Bell/HilbertCorrespondence.lean) are finite-dimensional complex inner-product spaces E and F. Local effects are actual complex linear endomorphisms of E or F. A state density is an endomorphism of the algebraic tensor product E⊗F. In finite dimensions, the source tensor Hermitian form suffices for the positivity and trace statements used here.

The predicate `Bell.Hilbert.PositiveFor` expresses self-adjointness and nonnegativity using a source Hermitian form. `PositiveOperator` uses the given local inner product. The joint form is constructed in [HilbertCoordinates.lean](../Bell/HilbertCoordinates.lean) from source orthonormal bases. The theorems `tensorInner_tmul` and `tensorInner_basis_independent` prove its pure-tensor formula and independence of the chosen bases. Source state normalization uses `LinearMap.trace`, and source Born probabilities are

\[
 \operatorname{Re}\operatorname{tr}_{E\otimes F}
 \bigl(\rho\,\operatorname{TensorProduct.map}(M,N)\bigr).
\]

These predicates and probabilities do not assume the existence or positivity of an embedded qubit matrix. `basisMatrix_positive_iff`, `operatorMatrix_positive`, `State.coordinates_positive`, `State.coordinates_trace`, and `born_coordinates` provide the representation proofs from the source definitions.

For local dimension d≤2, [HilbertIsometry.lean](../Bell/HilbertIsometry.lean) constructs an actual complex linear isometry `Bell.Hilbert.linearIsometry` into `EuclideanSpace ℂ (Fin 2)`. Its coordinate, inner-product, norm, and injectivity theorems identify the map represented by the rectangular embedding matrix V, satisfying V†V=I.

## Complement allocation and exact joint probabilities

Embedding an effect as VMV† alone gives a family summing to VV†, rather than the ambient identity. [IsometricCompression.lean](../Bell/IsometricCompression.lean) corrects this using the orthogonal complement

\[
 C=I-VV^\dagger,\qquad
 \widetilde M_a=VM_aV^\dagger+\mathbf 1_{a=a_*}C,
\]

where a* is one existing declared outcome. No extra outcome label is added. The module proves positivity of C, its idempotence, and annihilation of embedded operators on both sides. It then proves normalized POVMs, idempotent and orthogonal PVMs, and the compression identity V†ṀₐV=Mₐ.

Both parties are embedded together. The joint state becomes

\[
 \widetilde\rho=(V\otimes W)\rho(V\otimes W)^\dagger.
\]

`tensor_isometry`, `tensor_compression`, `trace_embed_pairing`, and `born_padded` prove trace normalization and exact preservation of all joint Born probabilities, including the complement terms. `Bell.Hilbert.Strategy.toQubit_behavior` and its projective counterpart state equality of complete tables. The construction introduces no Hilbert space larger than a qubit locally.

There is a distinction between preserving a label and preserving a zero effect. Relabeling alone preserves the effect exactly. Under dimension expansion, the selected source label can receive a nonzero complement projector even if its original effect was zero. Its probabilities remain unchanged because the embedded state is supported on the image. The theorem is exact behavior preservation, not equality of operators living on different spaces.

A normalized joint source state forces both local dimensions to be positive, by `State.alice_finrank_pos` and `State.bob_finrank_pos`. On those nontrivial spaces, normalization of a local measurement forces an existing outcome. `Strategy.aliceSelected` and `bobSelected` therefore obtain the complement labels from the source strategy itself. The whole-strategy endpoints have no extra nonempty-output premise. This argument does not assert that an isolated measurement on a zero-dimensional space has nonempty outcomes: on that space the identity is zero. Instead, a normalized joint state on such a space is impossible. Empty input sets simply supply no labels and require no complement allocation for absent measurements.

## Reverse correspondence and scope of the dimension union

[HilbertReverse.lean](../Bell/HilbertReverse.lean) turns every qubit matrix strategy into genuine endomorphisms on complex C² and its tensor product, with the same behavior. The reverse model is not an alias for a matrix record; the source positivity and trace obligations are proved.

[HilbertSimulation.lean](../Bell/HilbertSimulation.lean) defines `Bell.Hilbert.Space` and raw behavior sets that range over allowed local carriers of dimension at most two. `rawPOVM_eq_matrix` and `rawPVM_eq_matrix` prove that this union has exactly the fixed-qubit matrix raw ranges. The corresponding ordinary convex hulls coincide as well. The reverse inclusion uses C², which belongs to the allowed dimension range.

This is not raw-set equality between all qubit behaviors and behaviors on one fixed one-dimensional carrier. It is also not an assertion that a source strategy and every projective simulation branch use the same state or the same lower-dimensional carrier. `Bell.Hilbert.Strategy.finite_projective_simulation` returns actual projective source-Hilbert strategies on C², selected by one finite common random variable.

[HilbertFiniteLabels.lean](../Bell/HilbertFiniteLabels.lean) composes the Hilbert and label conventions in one independent physical source model: endomorphism-valued POVMs/PVMs with arbitrary finite outcome types, a source tensor-product state, and direct source Born probabilities. Its two `toQubit_behavior` theorems retain the original outcome types. `Strategy.two_input_simulable` and `finite_projective_simulation` consume the principal equality for at most two inputs per party. The latter produces a finite mixture of complete `Bell.FiniteLabels.ProjectiveStrategy` records on the original labels. The separate `finite_source_projective_simulation` theorem returns actual source-Hilbert projective branches on C² with those same labels.

The composed model also defines its own raw sets by ranging over `Bell.Hilbert.Space`. Its `rawPOVM_eq_fixed`, `rawPVM_eq_fixed`, `convexPOVM_eq_fixed`, and `convexPVM_eq_fixed` identify these sets exactly with the independent finite-label qubit model. `Bell.HilbertFiniteLabels.at_most_two_input_equality` states the main equality directly in that composed model. As with the cardinal Hilbert union, this does not assert equality for one fixed smaller carrier.

## Stochastic processing and one common selector

A `Bell.StochasticChannel S T` in [StochasticProcessing.lean](../Bell/StochasticProcessing.lean) is a nonnegative row family K(t|s) with each row summing to one. A deterministic channel is any function S→T, including a many-to-one function. For finite source and target alphabets, the product weight

\[
 w(f)=\prod_{s\in S}K(f(s)\mid s)
\]

is nonnegative, sums to one, and has the original channel entries as marginals. `StochasticFamily.reconstruction` also covers dependent row-output types.

For two-party strategies, a selector chooses an output for every source label at every input on both parties simultaneously. `StochasticProcessing.behavior_decomposition` proves equality of whole tables under the same selector distribution. Each deterministic branch is an actual `StrategyMap`; merging mutually orthogonal projectors preserves a PVM. Thus `deterministic_branch_mem_rawPVM` and `mem_convexPVM` establish physical convex-PVM closure. The argument is not a separate mixture chosen for each observed input pair.

[FiniteStochastic.lean](../Bell/FiniteStochastic.lean) independently defines this operation on arbitrary finite source/target outcome types:

\[
 q(a,b\mid x,y)=\sum_{c,d}K_A(a\mid x,c)K_B(b\mid y,d)
 p(c,d\mid i_A(x),i_B(y)).
\]

The optional maps iA and iB select source inputs. `Bell.FiniteLabels.StochasticProcessing.encode_behavior` proves that this actual weighted table commutes with cardinal encoding. Its `behavior_decomposition`, `deterministic_branch_mem_rawPVM`, and `mem_convexPVM` transport the same global selector and physical branches back to the original target labels.

An empty source has one empty deterministic selector, of weight one. A nonempty source cannot have a normalized row into an empty target; `StochasticChannel.nonempty_iff` states the exact existence condition. Zero probabilities are allowed, and selecting a zero-probability entry gives a zero-weight branch. General stochastic processing preserves the ordinary PVM hull; no theorem claims that it preserves the raw PVM set.

## What remains outside these claims

These correspondences remove specific model-convention gaps. They do not turn the formalization into a proof of every sentence or unused auxiliary derivation in the manuscript. The retained SDP/KKT, general cone/rank, smooth-manifold/Hessian, and unused projective-bound limitations are listed in [the auxiliary coverage section](CERTIFIED_COVERAGE.md#auxiliary-mathematics-outside-the-certified-scope). The global optimum of the strengthened POVM witness is not asserted.
