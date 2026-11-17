# Public formal-scope audit excerpt

Original report: `agent_notes/lean_verification.md`.

Original SHA-256: `dca35fb43719a688df2e1d68f1c7f373737b69b82a980ef6922376010bb9f76b`.

This public excerpt removes only the unrelated operational incident section. No mathematical statement or formal-check limitation has been removed. The original report remains in the local research record. The unchanged substantive audit follows.

---

# Independent upstream Lean scope and reproduction audit

Recorded: 2026-10-06 21:14 PDT (2026-10-07 04:14 UTC), updated 21:16 PDT.

**Conclusion:** The actual source is present, its final theorem has the intended full-dimensional origin-symmetric logarithmic Wulff inequality as its statement, and the file contains no lexical `sorry`, `admit`, `axiom`, `unsafe`, `implemented_by`, or `native_decide`. Exact-toolchain installation succeeded. **Kernel compilation, imported-axiom extraction, and Comparator reproduction were not completed** because disk pressure interrupted dependency installation. No claim of independent formal verification is supported by this audit.

## Inputs actually examined

- Read-only upstream clone HEAD is `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; initial and final tracked-file status and diff were clean.
- Repository README: documents an OpenAI-produced collection at heterogeneous verification stages; existence in the release does not certify correctness.
- Lean README and Comparator README: recommend small targets; Comparator instructions require `comparator`, `landrun`, and `lean4export`, then cache acquisition and challenge run.
- `lean/docs/091.md` advertises every dimension `n≥1`, arbitrary origin-symmetric convex bodies with interior, no smoothness/unconditionality restrictions.
- `lean/formalization.yaml` names actual declaration `OAI.LogBrunnMinkowski.main` in `OAI/Geometry/LogVolume/BrunnMinkowski.lean` and the associated Comparator config.
- Original `lean-toolchain`, `lakefile.lean`, manifest and compatibility-patch inventory were read. The toolchain is `leanprover/lean4:v4.34.1`; exact Mathlib revision is `d13f23b723b8a846827a245b89c10fc7d3f11612`.
- Actual 24,490-line, 1,228,745-byte solution file SHA-256: `bb798d24c3506422bc6ebdf064b71e3a1cf0f5f77835dd1985da2ff18a2c43a5`.
- Comparator challenge and config were inspected. The challenge's final proof is intentionally `sorry`; this was not used as evidence for the actual proof.

Hashes of these files are in `verification/lean_pinned/source_hashes.json`. The solution copy is byte-identical to upstream. No original clone build was run.

## Exact theorem and semantic agreement

At original lines 24481–24486, `OAI.LogBrunnMinkowski.main` quantifies over:

1. A natural number `n` and proof `1≤n`.
2. Sets `K,L` in `EuclideanSpace ℝ (Fin n)`.
3. `IsConvexBody K` and `IsConvexBody L`, defined as compactness, real convexity and nonempty interior.
4. `OriginSymmetric K` and `OriginSymmetric L`, defined by membership equivalence `x∈K ↔ -x∈K` for every x.
5. A real `t` with `0≤t≤1`.

The conclusion is `(volume K)^(1-t) * (volume L)^t ≤ volume (logCombination K L t)`. Here volume is Mathlib's Lebesgue measure with `ENNReal` values and exponentiation is the `ENNReal` real-power operation. `support K u` is the real supremum of the inner products with points in K; compactness/nonemptiness ensure this is the ordinary support function. `wulff f` imposes `⟪x,u⟫≤f u` for every unit vector u. `logCombination` applies it to `support K u ^ (1-t) * support L u ^ t`, with real positive powers. Definitions and theorem agree with the comparator challenge, apart from administrative `noncomputable` placement.

The source proves positive support on unit vectors (lines 19095 ff.), finite positive body volume (lines 19162 ff.), origin in interior (lines 19087 ff.), support-Wulff recovery, and exact interpolation endpoints. These statements align with full-dimensional origin-symmetric bodies in the manuscript. There is no boundary smoothness assumption in the final theorem. It covers n=1 directly; the proposed follow-on's n≥2 lies within it. It supplies neither equality cases nor the PDE's regularity/existence theorem or the follow-on general-body uniqueness result.

## Internal proof route inspected

The main proof invokes `main_of_softVariance softVariance`. The following selected declarations and surrounding proofs were read to trace the route:

- `MainStatement` (line 19030), endpoint/support lemmas and `main_of_finite_slabs`.
- `SoftVarianceStatement` (line 20144): a covariance estimate for finite sums of even powers of linear forms under a regularized log-concave density, with n≥2, nonzero normals, positive widths, even q≥2, ε>0.
- `main_of_softVariance` (line 20208): separate dimension one and reduce all higher dimensions to finite slabs; positivity and nonzero normal hypotheses are explicitly supplied.
- `softVariance` (line 24468): chooses an actual moment potential via `ActualMoment.coordinates`; derives the covariance estimate from `MomentSlab.variance_from_moment`; converts source/law expectations by explicit lemmas.
- `ActualMoment.euclidean` and `.coordinates` (lines 24328 and 24370 ff.): existence, smoothness, positive definite Hessian, global cap, Monge–Ampère equation and smooth gradient inverse are established using earlier variational/regularity theorems.
- `CompactMomentVariational.exists_C11_global` (line 4742), `C11_to_C2` (line 8715), `C2_positive_MA` (line 8742), `C2_to_smooth` (line 24019), and `variance_from_moment` (line 18973): selected assumptions, conclusions and entry proofs were inspected.

This is a route/scope audit, not a line-by-line manual proof validation of the 24,490-line development. Imported theorem correctness and all internal proof terms remain unverified by this reproduction. The manual upstream manuscript audit performed elsewhere is separate evidence and must be described separately.

## Axioms and formal checking scope

The actual file has one import, `Mathlib`. Its final theorem has no additional explicit analytical hypothesis such as the desired inequality, a spectral gap, a moment-potential existence assumption, or an equality classification. It defines and proves its earlier propositions locally. Static lexical scanning found 183 `theorem`, 1,284 `lemma`, 277 `def`, 15 `abbrev`, and 4 `structure` declarations and zero aforementioned prohibited tokens. These facts cannot establish absence of imported axioms or `sorryAx` in the transitive proof.

The Comparator config permits only `propext`, `Quot.sound`, `Classical.choice` and has `enable_nanoda: false`. The desired actual `#print axioms OAI.LogBrunnMinkowski.main` is saved in `CheckAxioms.lean`, but was **not executed successfully** because no target object was built. Therefore the exact axiom dependency set of the compiled theorem is unknown in this audit. No independent kernel was run. No follow-on theorem is formalized here.

## Reproduction attempt and limitation

A minimal pinned copy was created entirely inside `verification/lean_pinned`, retaining the unchanged solution and exact original configurations. Its audit-created lakefile requires only pinned Mathlib and preserves `autoImplicit=false`; the minimal manifest retains Mathlib's eight transitive dependencies. Their pins were independently compared to the pinned Mathlib manifest fetched from its exact GitHub commit; every pin matches, including `Cli`.

`lake --version` successfully downloaded/installed exact Lean v4.34.1 and reported `Lake version 5.0.0-src+5045d00 (Lean version 4.34.1)`. The newly installed toolchain occupies approximately 2.7 GiB. `lake env lean --version` next entered full Mathlib cloning. During this download and a concurrent unrelated clone, available filesystem storage dropped to approximately 480 MiB. The audit-owned tool session was interrupted before attempting compilation; this is a preemptive storage limitation, not a Lean proof failure. A later measurement after processes stopped was 846 MiB free.

Read-only search found no exact existing Mathlib checkout in the Math workspace or Elan tree. `~/.cache/mathlib` contains 276 MiB of archives dated September 10 and an older `leantar-0.1.15`; compatibility with this exact revision/toolchain was not established, so it was not substituted. No unrelated cache or file was deleted. Exact install/dependency logs are retained. Reproduction commands are in the pinned-workspace README and require adequate storage before resuming.

## Strongest supported result and gap

Supported: exact source provenance, semantic agreement of declared theorem, absence of local lexical proof placeholders/axiom declarations, documented exact versions, successful toolchain installation, and a pinned reproduction setup.

Gap: actual kernel-check/build, successful `#print axioms`, Comparator run, and independent full proof validation were not reproduced. Any final paper or package must say that the upstream source supplies a Lean development whose scope was inspected, while independent formal rebuilding was incomplete. It must not say this audit formally certified the inequality or the follow-on theorem.
