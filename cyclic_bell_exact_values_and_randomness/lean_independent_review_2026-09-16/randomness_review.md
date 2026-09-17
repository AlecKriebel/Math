# Independent adversarial-randomness review

Reviewed 2026-09-16 (Pacific). This is a source/statement audit of the **extracted delivered ZIP**, not an endorsement of its recorded self-audits. Root reviewer owns build/axiom replay. Completion of this bounded audit: 100%.

## Verdict

No blocking mismatch, circular privacy assumption, or weakened adversarial model was found in the randomness, binary benchmark, private-MUB, or one-input portions inspected. The actual endpoint statements correspond to the pinned manuscript. This conclusion is contingent on root's independent clean compilation and axiom audit and does not certify portions assigned to other reviewers.

## Definitions and adversarial scope

- `CyclicBell/GeneralTripartite.lean:16` defines Eve's finite POVM using only arbitrary positive matrices and completeness. There is no hidden projectivity, rank-one, uniformity, saturation, or privacy assumption. `TripartiteOn` at line 21 has arbitrary finite local dimensions and an actual positive trace-one ABE mixed state.
- `GeneralTripartite.lean:48` uses the actual tripartite Born trace, and `tripartiteBehavior_instrument` at line 121 proves equivalence with the postmeasurement sandwich and entrywise partial trace. Thus the success probability is not merely an abstract behavior assigned a physical interpretation.
- `GeneralCommutingGuessing.lean:14` allows arbitrary bounded positive self-adjoint Eve effects on an arbitrary complete complex Hilbert space. `CommutingEveOn` at line 21 imposes Alice/Bob/Eve cross-party commutation, not same-party commutation. `tripartiteToCommuting` at line 91 explicitly purifies any finite mixed ABE state and lifts all three parties. Its behavior equality is proved at line 132.
- `GeneralAdversarialValues.lean:15`, `:28`, and `:31` define actual finite, closure, and commuting adversarial domains. In particular `GuessQa = closure GuessQ` is taken on the **full extended array before equality with the Bell maximum is imposed**. `GeneralExtendedBehavior.lean:87` then defines the equality slice, and line 92 takes its success supremum. No saturation is hidden in validity definitions.
- `GuessQ_subset_GuessQa` and `GuessQ_subset_GuessQc` are proved (`GeneralAdversarialValues.lean:61`, `:63`). These are precisely the inclusions used by the finite counterexamples. A general `GuessQa ⊆ GuessQc` theorem is not supplied here, but neither the manuscript's randomness bounds nor their Lean proofs need it. It would be incorrect to report this missing ancillary inclusion as a gap in these endpoint bounds.

## Guessing lower bounds and entropy

- `GeneralAdversarialValues.lean:150` embeds the **same finite witness and actual deterministic POVM** into all three domains. The interval helper at line 162 gets nonemptiness from that witness and boundedness from normalization; it does not exploit the default value of a supremum over an empty or unbounded real set.
- `first_value_conditioned_guessing_bounds` and its second-family counterpart (`GeneralAdversarialValues.lean:186`, `:197`) give the manuscript's explicit all-d lower bound and a probability upper bound of one. The strict gap is proved at lines 208 and 216. The general d=4 floor is separately evaluated as 1/12, rather than being confused with the stronger 3/32 witness peak.
- `GeneralAdversarialEntropy.lean:24` and `:40` prove the stronger d=4 lower bound 3/32 in each model. The entropy map is explicitly antitone on positive probabilities at line 58; lines 65 and 74 correctly conclude **upper bounds** on value-only worst-case entropy. They do not claim that 3/32 is the exact worst adversarial optimum or that the displayed entropy upper bound is attained by the worst adversary.
- `GeneralPOVMMaximum.lean:23` proves every arbitrary finite POVM has Gram factors; compactness is established with a bound derived from completeness (`:57`), not by assuming a bounded feasible set. Fixed-realization maxima are established at `:103` and `:189`, with the full observed marginal preserved. `GeneralNestedGuessing.lean:70`, `:103`, `:112` identify the flattened finite-q supremum with the outer supremum of these fixed-realization maxima. No maximum over all dimensions/realizations is claimed.
- There is no analogous nested-max-attainment theorem for infinite qc Eve, nor should one silently infer it. The encoded qc quantity is an outer supremum over extended correlations with a particular Eve POVM, matching the manuscript's stated adversarial optimization domain; the witness lower bound is unaffected.
- `GeneralConsequences.lean:99` and `:112` rule out a vanishing deficit-only upper bound even on the restricted d-by-d finite witness class. This suffices to refute a purported uniform bound on all strategies. Their positive-tolerance quantifier avoids a loophole that would arise from checking only exactly zero tolerance.

## Binary benchmark

- `GeneralBinary.lean:92` derives both SOS residual equations from actual scalar saturation and normalized purification. `binary_on_state_structure` (`:167`) derives matching, square, and anticommutator relations **on the state**. It does not strengthen these to unjustified global anticommutation.
- `binary_private_moments` (`GeneralBinary.lean:235`) obtains all three nontrivial operator-valued moments. `binary_saturation_privacy` (`:319`) proves the actual conditional Eve matrices are rhoE/4 under only Hermitian involution, cross-party commutation, normalization and scalar saturation.
- `GeneralBinaryCertification.lean:100` connects this to arbitrary finite tensor-product PVM strategies, with the actual purification and instrument. `BinaryPrivacyAt` (`:124`) quantifies over all compatible finite purifications. The universal result at `:136` and explicit feasible attainment at `:152` prevent vacuity concerns.
- `GeneralConsequences.lean:70` proves success 1/4 for every complete Eve POVM after saturation. The exact binary entropy arithmetic is at `:125`. These are appropriately finite-purification privacy statements, whereas the universal Bell value is separately extended to q/qa/qc.

## One-input and private-MUB results

- `GeneralOneInput.lean:15` encodes ordinary nonnegative, normalized, nonsignalling finite-input/finite-output data. Zero-probability marginals are handled at `:24` and `:40`, rather than divided by implicitly nonzero probabilities.
- The hidden variable proof reconstructs all inputs, not just a target table (`:116`). `storedPurification` (`:164`) is the literal coherent flagged pure state. Grouping projectors have positivity, idempotence, orthogonality and completeness (`:138`–`:159`); Eve uses such grouping projectors at `:207`. The endpoint at `:230` proves normalization, the full Born behavior, and perfect guessing for every input. The party-swapped endpoint is in `GeneralPartySwap.lean` and feeds both directions of `GeneralBinaryCertification.lean:249`.
- `GeneralOperational.lean:31` proves that the coefficient-matrix reduction is the actual partial trace, including the conjugation convention. Its private-MUB composition theorem at `:106` has precisely the paper's private-reference, matching and **on-state** MUB sandwich hypotheses. It concludes target privacy and does not assume it. The proof through coefficient matrices differs from the paper's test-operator presentation but is a valid equivalent proof. It does not assert necessity, a low-setting construction, or full-space MUB identities.
- `GeneralConsequences.lean:36` states the operator-Fourier privacy criterion for the actual measurement instrument, with the zeroth mode derived from PVM completeness. It does not replace operator privacy by scalar observed uniformity.

## Checks and limits

Read the cited endpoint definitions and their proof chains against manuscript model definitions (lines 233–294), randomness interpretation (1098–1183), one-input/binary/private-MUB section (1227–1345), and binary proof (1785–1897). Also inspected the finite-POVM compactness and nested-supremum bridges. A targeted forbidden-token scan of the assigned modules found no `axiom`, `sorry`, `admit`, `opaque`, `unsafe`, `native_decide`, or `implemented_by` occurrences; the root replay remains the authoritative machine check. No files in the delivered package were modified and no separate concurrent build was run.
