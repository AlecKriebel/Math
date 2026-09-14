# Independent adversarial review: trust and build

Reviewer responsibility: independently audit Lean infrastructure reuse, theorem dependencies, theorem statement coverage, and clean-build evidence. This review is independent of the certificate arithmetic and physical-translation reviews.

## 2026-09-14, initial review (UTC)

The repository's pre-existing `qubit_povm_pvm_minimum_settings/bell_lean` project pins Lean `leanprover/lean4:v4.19.0` and mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Its checked-out mathlib HEAD matches the pin. Reusing the downloaded dependency packages is reasonable; importing that project's mathematical modules is unnecessary and would enlarge the dependency surface. A portable new project still needs its own toolchain, Lake configuration, manifest, and clean-build instructions.

An appropriate kernel certificate pattern already used in the repository is literal rational witnesses followed by `fin_cases` and `norm_num` equalities and sign proofs. Tactics construct proof terms which Lean checks. For the present sparse rank systems, checking each recurrence equation and applying a proved uniqueness theorem is preferable to generating a full inverse matrix. An external solver's success flag, native evaluation of rational comparisons, or a positivity hypothesis passed to the final theorem would not satisfy the request.

Exact finite witnesses only identify the intended scalar after the same operator, source, reward, rank ranges, and zero-extension conventions are defined in Lean and invertibility or uniqueness is proved. An arbitrary witness to a singular system does not establish the claimed inverse-defined scalar. Proving a positive rational list without this connection would leave Stage 1 incomplete.

The expected ordinary foundational dependencies are a subset of `propext`, `Classical.choice`, and `Quot.sound`. Every principal theorem must be checked with `#print axioms`; this transitive query is stronger than searching the source for admissions. Kernel-bypassing computational axioms such as `Lean.trustCompiler` are disallowed by the assignment even if an imported tactic makes them convenient. A source scan supplements the dependency query by flagging potentially problematic constructs; it does not prove a statement's interpretation.

The audit runner `tools/audit.py` records source hashes, build and query commands, exit codes, output hashes, exact checked statements, and axiom reports. Its `--clean` option removes only this project's `.lake/build`, preserving dependencies. It refuses a passing report if sources change during the audit. It must be given an independently reviewed principal-theorem list. At this initial checkpoint no principal theorem had yet been delivered, so there is no claimed completed Lean audit.

**Outstanding acceptance gaps:** all three requested stages remain unaudited. In particular, universal all-order positivity and the active-chain quadratic-form identity cannot be inferred from finite examples or from the absence of nonstandard axioms in unrelated auxiliary lemmas. The correspondence table must make those gaps explicit until their actual statements compile.

## Invertibility obligation: independent simplification

Direct algebra on the printed rows yields a simpler route than the manuscript's communicating-class argument. If the two absent boundary-neighbor entries are temporarily included in a formal interior row sum, then

```
1 − rowSum(Q)_k = (Nk+N+k²)/[Nk(k+1)] > 0.
```

All omitted neighbor entries are nonnegative on `2≤k<N`, so every actual row of `Q` is strictly substochastic. For the coefficient matrix `K=Hᵀ`, the interior bad-channel row has nonnegative entries and

```
1 − rowSum(K_bad)_k = (N+4k−1)/(2Nk) > 0.
```

The absolute good-channel row sum is at most `(N+1)/(2N)<1` for `N≥3`. Thus the standard finite maximum-absolute-coordinate argument proves uniqueness for `I−K`. A separate minimum-coordinate argument can prove inverse positivity for `I−Q`. These observations were independently simplified with symbolic rational algebra, and communicated as proof suggestions; they are **not** claimed as Lean-verified universal matrix bounds by this review. The support and boundary sums still require actual Lean proofs.

Initial inspection of `Definitions.lean` found the intended coefficient transposition, source, negative reward, and channel ranges correctly represented. `reducedScalar` deliberately uses mathlib's totalized nonsingular matrix inverse. Every claimed finite or all-order scalar identification must therefore carry an actual invertibility theorem, not just an arbitrary solution witness.

## Infrastructure contribution and independence disclosure

At the lead agent's request, this reviewer implemented `SymmetricSector/RowBounds.lean`. It proves the concrete coefficient matrix has every absolute row sum strictly below one for every `N≥3`, then applies the proved finite maximum-coordinate lemma in `Phase.lean` to obtain `coefficient_system_isUnit`. The bad-channel upper neighbor is bounded by the slightly larger nonnegative weight `(N−k−1)/(2N)`, giving row slack `(N+3k−1)/(2Nk)>0`; this avoids interpreting a negative absent top-row term as an actual entry. All single-rank sums are checked through elementary finite-sum lemmas.

A direct `lake env lean SymmetricSector/RowBounds.lean` check succeeded and printed exactly `[propext, Classical.choice, Quot.sound]` for `coefficient_system_isUnit`. This is a verified all-order invertibility result, not all-order scalar positivity. **This reviewer is the author of RowBounds and does not claim independent mathematical review of that module.** The lead was asked to have another reviewer inspect it. The final clean-build and transitive dependency audit remains a distinct mechanical responsibility.

The separate phase-linear-algebra agent subsequently inspected RowBounds independently and reported no issues with its majorization, boundary support, or all-order domain. That agent's review should be retained alongside this author disclosure.

## Independent inspection of finite margins and phase infrastructure

The finite-margin certificate uses externally discovered integer-grid lower witnesses. Lean proves each witness lies below the actual A.20 recurrence, verifies positivity of the witness and `lowerEll`, and then uses the positive-denominator monotonicity of division to bound every actual `betaTerm`. The maximum is explicitly over ranks `1≤j≤N−2`. The quantified finite positivity, exact `N=40` value, minimum over `40≤N≤287`, and strict separation for `41≤N≤287` match the manuscript statements. Certificate checks use `decide +kernel`, i.e. ordinary kernel reduction; no native-compiler evaluator appears in that certification path. Final build and dependency receipt remains necessary.

Independent inspection of `Phase.lean` found the full alternating inverse, rather than a first-excursion truncation, controlled by a finite weighted maximum principle. The exact Schur scalar identity retains the bad-channel occupation debt with its negative sign. The conditional theorem `phase_scalar_pos` has explicit positivity, contraction, source-envelope, first-phase, and debt assumptions. It is useful infrastructure and must not be reported as positivity of the manuscript scalar until the concrete hypotheses and scalar identification are proved.
