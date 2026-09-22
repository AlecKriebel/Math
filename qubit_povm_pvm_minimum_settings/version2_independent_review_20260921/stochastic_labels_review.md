# Independent stochastic, finite-label, and composed-model review

Date: 2026-09-21. Target: commit `5ec53ad70`. Completion: **100% of this bounded review**. No production file was changed. This review directly reads the current implementations; prior audit conclusions were not used as proof of correctness.

## Verdict

**No actionable mathematical or semantic defect found in the reviewed modules.** The new bridges close the previously identified stochastic-output and arbitrary finite-outcome interpretation gaps, and the composed Hilbert/label endpoint actually consumes both conventions on the same physical strategy. This conclusion is limited to these interfaces and their composition, not a fresh review of every prior rank-case proof or every new Hilbert-coordinate lemma.

## Source examined and findings

The following four production files were read in full and match the requested commit with no working-tree changes:

- `bell_lean/Bell/StochasticProcessing.lean` (252 lines).
- `bell_lean/Bell/FiniteLabels.lean` (300 lines).
- `bell_lean/Bell/FiniteStochastic.lean` (118 lines).
- `bell_lean/Bell/HilbertFiniteLabels.lean` (304 lines).

The independent contract files and relevant imports/model declarations were also inspected.

### Single shared random variable and channel quantifiers

`StochasticProcessing.lean:19–22` defines nonnegative normalized channel rows; no uniformity, positivity-away-from-zero, or nonempty-output assumption is imposed. `:52–69` constructs the product distribution on a complete deterministic function and proves normalization and reconstruction. The treatment of empty sources, impossible nonempty-to-empty channels, and zero row entries is explicit at `:73–113`.

The complete selector at `:148–167` fixes outputs for **every input and source outcome on both parties simultaneously**. Its weights depend on the channel and selector, not on the subsequently observed input pair or table entry. The joint reconstruction at `:183–204` proves the product of Alice's and Bob's channel probabilities, and `:207–226` reconstructs the entire behavior function with those same weights. Thus this is neither per-entry randomization nor a hidden contextual choice of decompositions. Optional deterministic input selection is local, with Alice's input map depending only on Alice's target input.

`deterministicMap` (`:169–173`) instantiates a genuine `StrategyMap`; branch membership uses its proved PVM coarsening, with projection merging and unused labels permitted (`:229–231`). Convex closure (`:235–244`) takes a real physical PVM hull as premise and concludes membership in the target physical PVM hull. The code correctly does **not** assert raw-PVM closure under a stochastic channel. Channels with shared external classical choices can be handled by further convex mixing; the individual channel map is the usual product of local kernels.

### Finite outcomes are transported physically and reversibly

`FiniteLabels.lean:17–24,103–119` defines independent normalized PSD matrix measurements and complete strategies on arbitrary finite outcome types, including input dependence and separate type universes. It does not define the source model as an alias of the target set whose equality is being asserted.

The effect encodings and inverses (`:29–91`) transport every outcome bijectively. The complete-table linear equivalence (`:122–128`) has both inverse laws; `finite_mixture_transport` (`:132–136`) preserves one common weight family. Both physical strategy classes have reversible encodings (`:140–207`). The raw-set equalities (`:215–232`) establish both inclusions, and the hull statements (`:234–262`) follow by the image of an ordinary convex hull under this linear equivalence.

Consequently `:264–274` is a legitimate transfer of the existing equality, with no circular assumption of the new outcome-label theorem. Empty alphabets are not accidentally excluded: normalized measurement nonexistence (`:53–62`), no-strategy/empty-hull consequences (`:275–293`), and the no-input case (`:295–298`) agree with the mathematical model.

### Finite-label stochastic processing is the actual channel formula

`FiniteStochastic.lean:44–60` independently defines the table by weighted sums over the original source types. It is not defined by conjugating the already-proved map and naming the result a physical formula. `:80–85` proves the commuting square by reindexing those sums; `:90–115` then transports the global-selector decomposition and physical PVM membership. Thus target-label preservation and stochastic processing are checked together.

### Both Hilbert and finite-outcome conventions apply to the same source

`HilbertFiniteLabels.lean:19–26,79–91` uses actual positive normalized endomorphisms on the source Hilbert spaces and the source tensor Born trace, with arbitrary outcome types. The map at `:125–133` composes outcome encoding, the Hilbert embedding, and outcome decoding; its conclusion is equality of the **original complete labeled table**. The projective analogue is `:159–170`.

The reverse construction is also present (`:184–203`), so `:246–285` proves raw-set and hull equality rather than only an embedding inclusion. The union is over dimension-bounded `Hilbert.Space` carriers. The simulation endpoints (`:215–242`) provide one finite random index selecting a complete state-and-measurement strategy. They correctly place branches on `QubitSpace`; they do not assert simulation within an unchanged one-dimensional carrier or using an unchanged state. The generic per-strategy embedding/simulation permits arbitrary source carrier universes, while the bundled union uses the ordinary `Type` carrier universe; this is a Lean packaging convention, not a physical restriction in the generic theorem.

No new theorem hypothesis supplies equality, local realizability, or stochastic closure as an oracle. These modules use the previously established matrix equality through explicitly proved transports; the foundational matrix theorem is upstream of these modules.

## Fresh independent composition contract

The new review-only file `contracts/StochasticHilbertLabels.lean` combines **all three bridges**. Its theorem starts with an arbitrary source Hilbert-space strategy of local dimension at most two, arbitrary finite input-dependent outcome types, at most two source inputs per party, and arbitrary local stochastic output channels (including optional input selection). It concludes a finite normalized nonnegative mixture of actual Hilbert PVM strategies on the original target label types. The right-hand side is explicitly expanded as a double sum of channel probabilities times the original tensor-operator Born trace.

This tests that the three interfaces compose without retaining a hidden fixed-label or fixed-source-carrier assumption and that their common-randomness conclusion is a whole-table statement. Additional fixtures cover empty-to-empty channels, rejection of a nonempty-to-empty channel, and an input-dependent alphabet that is empty at only one input.

Final execution: **PASS, exit 0** using `lake env lean ../version2_independent_review_20260921/contracts/StochasticHilbertLabels.lean`. The composed theorem reports only `propext`, `Classical.choice`, and `Quot.sound`; all boundary fixtures elaborate. See `contracts/StochasticHilbertLabels.log` and `contracts/StochasticHilbertLabels.receipt.json`. This is a fresh bounded contract execution against the available built imports, not a fresh build of every production source. A separate review fixture initially lacked its dependent `Fintype` instance; that review-only instance was supplied before the successful run.

## Limits

This review does not rebuild the full development, audit artifact packaging, or independently prove every imported Hilbert positivity/isometry lemma. It does not promote the alternate-proof formalization to certification of every original manuscript lemma. Within the reviewed stochastic/label/composition scope, no corrective production change is recommended.
