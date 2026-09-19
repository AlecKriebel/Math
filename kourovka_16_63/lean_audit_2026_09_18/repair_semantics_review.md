# Adversarial semantic review of source repairs

## Verdict and limits

**No mathematical statement weakening or hidden proof bypass was found in the reviewed repairs. The project remains a partial formalization.** This is a read-only semantic comparison against the user-supplied `kourovka_16_63_lean_source_2026-09-17.zip`, not a new build or a claim that every edited module compiles. No Lean process was started during this review because the parent was benchmarking memory-heavy checks.

The source-hash snapshot is `repair_semantics_snapshot.json` (UTC timestamp 2026-09-19T03:52:50.977446+00:00). It records every project mathematical module at the beginning of this comparison. Sources were still being repaired: `Certificates/Indexing.lean` and `Certificates/InnerWitness.lean` changed during review. Those modules require a final frozen-diff check before this report is used as release evidence. The report does not cover future edits merely because their filenames match.

## Statement and data preservation

- The exact `ExactOrders` and `NotebookAffirmative` targets still use ordinary mathlib `MulAut`; only the obsolete import in `Challenge.lean` was replaced. They remain proposition definitions, with no theorem constructing their witness.
- `RawCoefficients.lean`, `ExportedData.lean`, `Ambient/IntData.lean`, and `Finite/LieAutomorphisms.lean` were byte-identical to the supplied ZIP at inspection. In particular, the finite automorphism set was not replaced by a selected subgroup.
- All 62 ambient and lattice check-shard files retained their original theorem statement lines and finite index coverage (`repair_shard_integrity.json`). Introducing one universal index and then using `fin_cases` splits the original quantified goal; it does not remove cases. The remaining finite goal is still checked by reduction.
- The new `TableCertificate.row` partitions the original first-index list, and `raw_table_matches_exported` retains its exact original conclusion. Its final assembly enumerates all indices 0 through 30, rewrites all row proofs and closes by definitional equality. A fabricated row list would still need its stated equality to `Raw.coefficient` to pass Lean.
- Every generated `g0`, `g1`, ... expression definition, every `eval_N` vector statement, and every indexed generator-value statement in `IntegralGeneration.lean` is textually unchanged. The bulk diff is `decide` becoming `decide +kernel`. The general scalar-extension proof now explicitly supplies the two bracket functions to the existing map-evaluation theorem; it preserves the original conclusion and hypotheses.
- The selected-row and rational inverse-coefficient witness block moved from `InnerRank.lean` to `InnerWitness.lean` unchanged. The original namespace remains `Kourovka.Certificates.InnerRank`. The outer rank module imports that witness and the actual integral Jacobi theorem. This is a dependency split, not a replacement of actual inner derivations by abstract columns. Later edits to InnerWitness were not part of the frozen snapshot and need a final check.
- `ScaledData.LB` expands the existing `Bilinear R (V R)` abbreviation to the identical nested linear-map type; the bracket formula is unchanged.

## Counting and typeclass repairs

`ScalarKernel.Carrier c q` remains the entire subtype of elements annihilated by multiplication by c in `ZMod (c*q)`. The repaired `equivFin` still sends an element to its representative divided by q and sends t back to q*t. Positivity assumptions `hc : 0 < c` and `hq : 0 < q` remain explicit; `include hc hq` and proof-local `NeZero (c*q)` instances ensure they are available where needed. No field structure or inverse for a nonunit is assumed. The final prime-power theorem retains the same `hp : 0 < p`, `hv : v ≤ i`, entire-kernel subtype and cardinality `p^v`. Its boundary cases v=0 and v=i are retained. Typeclass repairs do not substitute a smaller kernel.

The row/column count proofs retain dimensions 465, 14415 and 961; replacing exhaustive reduction for products with `Fintype.card_prod` preserves those exact statements. Kernel transport and diagonal-kernel changes only expose map application or identity ring-hom evaluation. The two negative elementary-operation tests still reject multiplication by a nonunit modulo 9 and a same-coordinate shear.

## Other repaired proof families

Linear/bilinear changes explicitly invoke extensionality for the intended number of arguments and expose coercions before algebraic normalization. Alternation-to-skew proofs add commutative addition normalization. Lattice precision and weighted-flag proofs target a single occurrence when rewriting so that a hypothesis is not rewritten into its own intended goal. The weighted degree identity and lattice embedding are unchanged.

Finite nilpotency edits add the direct adapted-basis import and explicit scalar-ring arguments for `standardB`/`wordSpan`. They retain the same lower-central series and vanishing statements. Marking p-adic reduction/section definitions `noncomputable` is an implementation classification, not a mathematical axiom or a change in their functions. Kernel divisibility uses an explicit cast normalization.

The earlier dedicated `analytic_repair.md` reviews the four Analytic/BCH modules. Their exp/log factorization and homogeneous-degree injectivity hypotheses remain explicit; repairs do not discharge those mathematical obligations.

## Proof trust and release status

The mathematical source scan found no custom axiom declaration, admission, `native_decide`, unsafe declaration or kernel-check bypass. Matches to the word “external” were comments saying external execution is not trusted. This source observation must be supplemented with transitive axiom reports after successful compilation.

The pinned Lean 4.19.0 implementation was inspected locally at `Lean/Elab/Tactic/ElabTerm.lean:435–478`: `decide +kernel` follows `doKernel`, constructs the normal decide proof, and passes it to `mkAuxLemma` with asynchronous elaboration disabled. It is distinct from `+native`, and the implementation rejects combining the two. Thus this mass replacement is a kernel reduction scheduling repair, not a new native-computation axiom. Disabling asynchronous elaboration and increasing recursion/heartbeat or stack limits likewise do not weaken statements.

The updated serial builder invalidates the full selected local object closure, compiles from project sources, rejects failures/missing output, and checks that source hashes are unchanged during the run. It explicitly does not rebuild upstream dependency objects. The main runner still sets `complete_formalization: false` and `final_group_theorem_present: false`, and default execution reports `INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT`. A clean milestone build cannot truthfully be promoted to a complete Kourovka formalization.

Remaining central obligations are unchanged: instantiate the full finite Smith certificate and count; establish the concrete arbitrary-map/near-identity and integral exp/log correspondence; construct and prove the finite BCH group and both directions of the ordinary group/Lie automorphism correspondence; finally produce the unconditional group-existence theorem. These are substantial missing mathematics, not parser repairs.

## Required final check

After the parent freezes the sources, compare final hashes against the snapshot and review every newly changed mathematical file. Then use the parent compilation and axiom-audit records to report exactly which modules passed. No release should describe this package as a full formalization unless the missing target theorem and its actual mathematical bridges are supplied.

Checkpoint: semantic source comparison of the current repair mechanisms is 100% complete; final frozen-source verification remains pending. This percentage does not measure completion of the absent full formal proof.
