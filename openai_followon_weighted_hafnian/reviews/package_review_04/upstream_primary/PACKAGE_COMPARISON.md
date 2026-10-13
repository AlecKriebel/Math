# Review 04 — independent upstream and formal dependency comparison

Verdict: **PASS for the pivotal upstream dependency and its representation in
the frozen v4 package. No blocking substantive mathematical gap or material
dependency-scope mismatch found.** This verdict is limited to the work below;
it is not a blanket release verdict for the complete package.

The independent primary reconstruction was saved before opening the package's
research audits. The original independent receipt was created at
2026-10-07 06:10:24 UTC; `INDEPENDENT_PRIMARY_FINDINGS.md` was created at
06:12:27 UTC. The first package comparison followed those writes. The receipt
was subsequently strengthened with exact Git-blob checks and additional trust
tokens; this post-comparison enhancement did not change the mathematical
findings. No earlier project review was used to form the source reconstruction.

## Exact reviewed version

Read-only primary checkout: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Every read source hash was compared to its exact pinned Git object, with zero
mismatches. The entire recursively imported OAI closure is 415 files,
3,091,883 bytes and 66,246 lines; its only external import root is Mathlib.

Frozen package root:
`/Users/alec/Documents/Math/openai_followon_weighted_hafnian/reviews/package_review_04/extracted`.

| Compared file | SHA-256 |
| --- | --- |
| `main.tex` | `25a9b9e5df03ea50c24812f5107bf3913ab352296faf6d5170e0372c4be8b9f4` |
| `research/UPSTREAM_PROOF_AUDIT.md` | `b9e6a3e7b56f839ee6a16186159c0a8a4a477b2b8712ede22c5a221639536ac1` |
| `research/FORMAL_SCOPE_AUDIT.md` | `7ba38637eca8365c036225c3f5e0844ef344afdb91eed77ad8b20e98206e9db1` |
| `DEPENDENCY_LEDGER.md` | `93b8989acd2dcb6bef836e389bf07539218339c99e42c366c80c044b4f7726ef` |
| `DEPENDENCY_REFERENCES.json` | `53bc3be03225bd1c21affa8c8f1b98f3786d8d7f8bf9a4362b2ddd0507b301d8` |
| `research/lean_source_inspection/STATIC_AUDIT_RECEIPT.json` | `3a473aa015a81d1bf6037f52e9c992505d954ea96a97b3b4fd8db21d7704914d` |
| `research/lean_source_inspection/audit_sources.py` | `28f25f3bb8a488fbf453daea6c0b5a49c479529e3d2af0bd3da14d0dbb34f4e9` |

The full file sizes and all source comparisons are in
`PACKAGE_COMPARISON_RECEIPTS.json`. Every one of the 415 package-recorded
Lean module hashes agrees with the independent source hash. The principal
manuscript, scope document and inspected entropy input hashes also agree.

## Pivotal comparison findings

1. **Correct base theorem.** The package uses the actual uniform unweighted
   finite-simple-graph FPRAS, with nonnegative rational output, relative error,
   logarithmic confidence cost, certain zero for zero counts, and every-tape
   polynomial bit time. It does not infer arbitrary compressed weights from
   internally weighted constructed graphs. Its parameter range extension by
   `min(delta,1/4)` is valid.

2. **Correct base proof route.** The saved upstream audit agrees with the
   primary reconstruction: logical two/four-hole injections and normalized
   relocation; finite partition-function bootstrap; exact subdivision and
   broken-path accounting; threshold capacity charging and bag inflation;
   fixed-label odd-arc quadrangulation; signed cell identity including
   context errors; repaired encodings by two perfect matchings; conditional
   rare-guide cancellation; additive pair energy; ordered ANOVA residual
   assignment with replication; all-functions product gap; fixed-bit sampling;
   annealing, scale restoration and confidence amplification. This is neither
   a near-perfect-chain proof nor an asserted canonical-path congestion bound.
   The parent task's initial route labels were historical and were explicitly
   corrected before this comparison.

3. **No lost rare-event factor.** Both the primary proof and package audit
   preserve `p_X` in demand mass and cancel its reciprocal only through the
   subsequent conditional Jensen step. There is no unsupported lower bound
   for the guide event. Closed/through patterns cover the same vertices, so
   the cycle swap is a complete discrepancy component, with at most `2N`
   representations per component.

4. **No unsupported two-coordinate-to-product leap.** The additive pair
   theorem is not promoted directly to an all-functions gap. The ordered
   predecessor projection places every residual component in a unique pair
   (its last two coordinates), yielding a collective residual bound. With
   `q=32L`, the `1/4` residual coefficient can be absorbed. The lazy spectral
   mixing bound uses the explicit product minimum mass. Unequal-tier swaps
   use Metropolis acceptance and are not falsely given acceptance one.

5. **Failed histories and bit time are covered.** The package's cited
   every-tape output bound is supported by the actual source theorem. The
   primary implementation clips the estimates and scales, uses a sampler
   requiring no balance promise, bounds update factor dependencies, and
   controls finite random-choice discrepancy without rejection loops.
   Thus the follow-on may bound failed estimates' output lengths by the
   runtime of the cited machine. This is a mathematical existence result
   with very large fixed exponents, not a practical implementation claim.

6. **Zero nuance is preserved.** Formal `MainStatement` promises
   `Z=0 -> output=0`, not the converse on every tape. The package says this
   explicitly, performs exact positive-support matching feasibility, and
   replaces a zero output on a feasible input by a positive rational before
   scaling. This strengthens the wrapper's zero-if-and-only-if statement
   without altering successful estimates. It is not an unsupported property
   attributed to the base theorem.

7. **Sampling dependency is valid.** The primary manuscript already gives
   an explicit edge-deletion uniform sampler with TV tolerance and time
   polynomial in inverse tolerance. The package acknowledges it and supplies
   a separately analyzed vertex-partner self-reduction. Its sampler does not
   rely on an internal bag-graph sampler as though that were an arbitrary
   input-weight sampler. The package never claims exact, pointwise
   almost-uniform, or logarithmic-in-inverse-TV sampling from the dependency.
   A complete reconstruction of the follow-on sampler itself is the parent's
   separate task.

8. **Entropy scope is not duplicated or overpromoted.** The companion's
   pointwise entropy and finite-weight variational brackets do not imply
   arbitrary relative error. Its deterministic binary-multiplicity count
   guarantee has factor `512^n`; the singleton-loop extension has factor
   `2^(18n)`. The package's distinction from the new relative-error
   consequence is accurate. This review did not redo the entire entropy
   proof or external novelty search.

9. **Formal claims remain within evidence.** The actual
   `OAI.MatchingFPRAS.thm_main` in `MatchingCount/Main.lean` has the full
   `Model.MainStatement` semantics; it is not the comparator `sorry` stub.
   Immediate machine cost, output-law and compiler bridge declarations were
   read. The package's source-only limitation matches this independent
   inspection. The comparator configuration lists permitted axioms
   `propext`, `Quot.sound`, `Classical.choice`, but that is not a compiled
   axiom-closure receipt. The metadata catalogue omits MatchingCount.Main,
   while the actual source, scope document and explicit comparator JSON
   exist; the formal audit correctly states this. No token scan or failed
   dependency probe is represented as a successful kernel build.

## Coverage and precise limits

Primary main manuscript: all pivotal proof sections analytically reconstructed,
including four-hole endpoints, hole relocation, even/odd internal deletion
patterns, endpoint consumption, central and cross-center factors, short and
length-three arcs, complementary diagonal identity, guide conditioning,
encoding inverse, ANOVA orthogonality, mixing, adaptive errors, and bit bounds.
Source bibliography and citation metadata were read for identity/attribution.

Exact independent finite checks: 96 rational four-hole cases; 52,380 local
broken-path cases; 182 signed cell identities on cycles of orders 4–12;
5,027 residual subset assignment cases. All passed. These support local
proof identities, not the full upstream FPRAS.

Actual Lean: top-level theorem/model and immediate execution bridges were read;
the complete OAI import closure was hashed, matched to Git and statically
scanned. No uncommented `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`,
`native_decide`, `ofReduceBool`, `implemented_by`, `partial`, `opaque`,
`run_tac`, or `run_cmd` appeared in that proof closure. The Lake configuration
has build-side patch commands outside that closure; the package correctly
requires the full pinned project and patches for a genuine build.

**No independent kernel build, compiled axiom closure, comparator execution,
or full upstream algorithm execution was performed.** This review inspected
static proof source, not every proof line in 415 modules. It does not certify
the follow-on as formalized and does not treat missing replay as proof failure.
No large dependencies were installed.

The parent's separately identified title scope issue remains outside this
dependency pass: the frozen v4 title lacks the word "nonnegative" although
the abstract and theorem correctly impose it. An explicit title repair is
appropriate before a complete release verdict. This observation does not
change the base proof or any theorem examined here.

No third-party sources were copied into public audit output. Only authored
reports, scripts and hash/test receipts were written in this owned directory.
No source clone, shared index, branch, Git history or publication state was
modified, and no external individual was contacted.

Relevant review completion at this final checkpoint: primary-source
dependency reconstruction 100%; assigned source/package comparison 100%.
Whole-project mathematical and publication percentages are not evaluated by
this scoped reviewer.
