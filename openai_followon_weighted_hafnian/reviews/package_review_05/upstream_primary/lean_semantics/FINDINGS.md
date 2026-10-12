# Independent pinned Lean semantics review

Reviewed pin: `adc7f1241b42e322a6451854ab7e4b4c146bf78a` in `/Users/alec/Desktop/math`, read-only. No previous review, follow-on package, or ComparatorChallenges source was read. All copied third-party material is under this review's ignored `primary_reading/`. The companion `source_receipt.json` pins every copied source by SHA-256 and lists inspection limits.

## Result

The actual declaration `OAI.MatchingFPRAS.thm_main : MainStatement` is in `lean/OAI/Combinatorics/MatchingCount/Main.lean:21`; the exact specification is its sibling `Model.lean:94`. Its graph/count/machine interface faithfully states a uniform unweighted simple-graph FPRAS. No circular FPRAS premise, weakened count, or zero-time oracle was found in the interface and execution/probability/runtime bridges inspected. This is a source-semantic result, **not independent kernel verification or a complete hand verification of its 415 imported OAI modules**.

Two limits are material when using it downstream:

* The zero clause is `Z G = 0 → every tape outputs 0`. It does not state the converse. An unsuccessful tape on a positive-count graph is allowed to output zero. Exact feasibility/zero detection needs a separate justified procedure if that stronger requirement is asserted.
* The exported theorem is approximate counting. It does not export an approximate uniform sampler for perfect matchings of the input graph. Internal sampler statements concern weighted, enlarged source/replica systems and require their own hypotheses; a downstream original-graph sampler needs a proven applicable reduction or a separately established theorem.

## Exact source specification and assumptions

`GraphInput` (`Model.lean:8`) consists of arbitrary `n : ℕ`, a finite set of pairs in `Fin n × Fin n`, and `increasing : ∀ e ∈ edges, e.1 < e.2`. This rules out loops and repeated unordered edges while allowing every finite simple undirected graph after labelling. `Perfect` (`:14`) requires the selected edge set to lie in the input edges and exactly one selected incident edge at every vertex. `perfectMatchings` is the edge powerset filtered by that predicate; `Z` (`:23`) is its natural-number cardinality. The count is therefore the ordinary exact unweighted count, not an approximation specification assumed as a field.

`encodeInput` (`:38`) serializes binary `n`, edge cardinality and sorted endpoint pairs, followed by reduced numerator/denominator encodings of rational `ε,δ`. The fixed alphabet is `Fin 8`. `RandomMachine` (`:45`) has finitely many control states and a table taking only current state, current symbol and one Boolean coin; an action writes a symbol or moves the tape. `run` (`:70`) is exactly the fold of these ticks. `Outputs` (`:74`) requires halt and the actual rational word on the tape's right side. This is neither a high-level arithmetic operation charged one tick nor a separate graph-dependent machine.

`MainStatement` chooses **one** `A`, `C`, and degree `d` before quantifying all graph inputs and positive rational parameters with `ε<1` and `δ<1/2`. Its budget is

`C * (length(encodeInput G ε δ) + ceil_nat(1/ε) + clog_2(ceil_nat(1/δ)) + 1)^d`.

For every tape of that length it requires a nonnegative rational halted output; for zero counts every tape must output encoded zero; and at least a `1-δ` fraction of the `2^t` tapes must give an output between `(1-ε)Z` and `(1+ε)Z`. The finite tape fraction is the probability under independent fair Boolean bits. The bound includes the binary lengths of the rational parameters, polynomial dependence on `ε^{-1}`, and logarithmic dependence on `δ^{-1}`. The formal interface is for `δ<1/2`; extending a counting consequence to `δ<1` by calling at, for example, `min(δ,1/4)` is elementary but is not a new declared Lean theorem here.

There are no external hypotheses on `thm_main` itself. The source proof invokes the constructed machine and internal lemmas, rather than assuming a matching-count FPRAS. The source statement does not assume connectedness, even order, a supplied matching, or nonzero count.

## Inspected support chain

`Main.lean:22–30` instantiates `LiteralPhysical.mainProgram.machine` and combines `mainTime_bound`, `mainProgram_outputs`, and `mainProgram_success`.

* `Machines/Wrapper.lean` defines `mainProgram := wrap LiteralAlgorithm.algorithmRealizer`. Packing, actual online execution, erasure/unpacking and the resulting physical cost are explicitly connected.
* `Machines/PhysicalProgram.lean` defines `Program` with a finite supported state set, and `Program.Realizes` by actual transition implementation, equality of all rational output expectations, and a worst-case experiment cost. `PhysicalRestriction.lean` restricts the table to the finite supported states; `PhysicalProgramSeal.lean` proves actual machine tape equality, halting, and finite fair-tape mean transport.
* `Graphs/AdaptiveStream.lean` defines finite `Experiment` trees (`done/read/delay`), their worst-case branch cost and fair expectation. `Machines/OnlineTree.lean` requires an actual program execution witness, rather than treating a function's name or declared cost as implementation. `TreeTyped.lean` ties deterministic realization to execution. `Complexity/TreePolynomial.lean` bounds execution cost **plus output encoded size**.
* `Algorithm/Algorithm.lean` parses the raw encoding, returns 1 on the empty graph, returns 0 on odd or too-sparse graphs, and otherwise runs the constructed experiment. `AlgorithmLaw.lean` relates this computation to `FiniteTrial.guardedAmplifiedBitOutput`; it then proves proper output and the success event. `Complexity/OriginalCost.lean` derives the algorithm bound from parser, materialization, computation and rational output costs. `Complexity/PhysicalCost.lean` converts these into the physical tape-machine polynomial.
* `Trial.Parameters` in `Probability/AdaptiveLaw.lean` contains order, parity, tolerance and an explicit cooling schedule admissibility condition. It contains **no FPRAS, sampler or mixing oracle field**. `Algorithm/SortedList.lean:239` supplies those parameters using a least admissible schedule and its bound.
* `Algorithm/GuardProbability.lean` gives an observable certificate, sampler total-variation comparison, and a guarded trial failure bound of `1/10`; `Tapes/GuardBits.lean` transports the law to finite bits and amplifies using an odd median. Its `guardedOutput` returns zero on a failed guard. That is compatible with the one-way zero clause and does not establish the converse.
* `Graphs/Evolve.lean` contains ordinary finite-chain density and squared-L1 mixing statements. `Sampling/PM.lean` uses `MatchingOn` (from `Graphs/ColoredEdge.lean:42`), the exactly-one incident-edge predicate, and defines matching product weight, partition sum, and normalized Gibbs law. These definitions do not substitute a different combinatorial object for perfect matchings.

Boundary checks in `Sampling/Endpoints2.lean` prove `Z=1` for `n=0`, `Z=0` for odd `n`, and `Z=0` when `2|E|<n`. The latter guard ensures that materializing all vertices occurs only when `n` is controlled by the explicit sparse input length; a huge binary `n` with few edges does not silently force exponential materialization in the inspected cost bridge.

The nearby `PerfectMatching/Main.lean` proves entropy/count bounds in the `MatchingEntropy` namespace and is not the FPRAS endpoint. `PerfectMatching/Model.lean` also defines a compressed-multiplicity count for a separate deterministic approximation development. Neither that presence nor the internal rational activities upgrades `MatchingCount.Model.MainStatement` to a rational weighted-hafnian FPRAS.

## Validation receipt and remaining limits

The full `OAI` import closure of `MatchingCount/Main.lean` was copied and hashed: 415 Lean modules. A literal word scan over that closure found no `sorry`, `admit`, `axiom`, or `unsafe` tokens. This is a source text scan, not an elaborator/parser check, dependency axiom extraction or verification of the imported Mathlib library. The receipt separates manually inspected files/excerpts from the copied/scanned remainder.

Pinned toolchain is `leanprover/lean4:v4.34.1`; the manifest pins Mathlib at `d13f23b723b8a846827a245b89c10fc7d3f11612`. This review did not run Lean, Lake, a checker, a proof build, or `#print axioms`, and installed nothing. A read-only availability check found local Lean/Lake entrypoints but no `Main.olean`, `Model.olean`, or Mathlib umbrella `.olean` at the original clone's usual cache paths. Cache absence is not a mathematical counterexample or proof failure.

Strongest independently established result of this subreview: the named theorem's **source specification** is the claimed semantic simple-graph counting FPRAS and the inspected support bridges encode actual computation/probability/cost rather than an assumed conclusion. Remaining independent validation: kernel-check the exact pinned source/dependency environment and validate the full mathematical dependency proof, especially the central mixing/congestion argument. No claim here certifies the follow-on theorem or its full package.
