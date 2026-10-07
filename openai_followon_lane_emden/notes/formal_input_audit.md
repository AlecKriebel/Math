# Independent formal-input audit: family 370

Checkpoint: 2026-10-06T21:34:49-07:00 (America/Los_Angeles).

**Strongest verified result:** the actual pinned source states the positive entire, globally C² unweighted Lane–Emden Liouville theorem with the exact strict subcritical hyperbola needed by this project; its definitions are genuine Euclidean differential/PDE conditions and contain no additional asserted pressure, localization, or energy hypotheses. Its 96-file OAI import closure was copied, hashed against pinned Git blobs, and scanned. **No theorem was locally elaborated or kernel/axiom checked.** No unconditional theorem claim should be certified by this source inspection alone.

Best-guess task-specific completion: formal-input semantic/assumption audit 85%; independent formal reproduction 15%; overall follow-on mathematical resolution and publication percentages are maintained by the lead researcher. The formal theorem build is outstanding because the required cached Mathlib environment is absent and insufficient disk space prevented safely fetching the umbrella import.

## Exact pinned evidence

- Read-only source: `/Users/alec/Desktop/math`; HEAD confirmed `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
- Upstream tracked source status for relevant proof, comparator, config, and scope paths was clean. No source clone files were changed.
- Actual module: `lean/OAI/Analysis/HenonEmden/Main.lean`; import: `OAI.Analysis.HenonEmden.UniformEnergy`.
- Actual unweighted declaration: `OAI.HenonLaneEmden.lane_emden_nonexistence`, Main lines 19–39.
- Principal weighted declaration: `OAI.HenonLaneEmden.main_nonexistence`, Main lines 9–17; listed in `lean/formalization.yaml` lines 1222–1224.
- Main SHA-256: `f4e2f096a0243cf1190de46dda83d96e8d95fdeae5463b114f18c7222f7e8823`.
- Model SHA-256: `bbbe671e5bd3a8d9e58b1993686361854ec2dc9136ec3ab3ef1c01cac0c46957`.
- Exact Lean toolchain: `leanprover/lean4:v4.34.1`; installed binary reports Lean 4.34.1, arm64-apple-darwin24.6.0, release commit `5045d0056413266e57c625dcd7c365b10e377c52`.
- Exact Mathlib pin retained in minimal reproduction configuration and lock: `d13f23b723b8a846827a245b89c10fc7d3f11612`; dependency checkout HEAD independently matched during the attempt.
- Full 96-module hashes, extra source/config hashes, and the inspected Laplacian hash are recorded in `validation/formal_source_hashes.json`. All 96 source files matched the corresponding pinned Git blobs. Total OAI source bytes: 645,822. The import graph is acyclic and has no OAI imports outside this family; its only external root is `Mathlib`.

## Semantic agreement and exact gaps

Actual `Model.lean` defines `Space n := EuclideanSpace ℝ (Fin n)`. The `IsSolution` structure has exactly eight fields: continuity of u and v on all of Space n; `ContDiffOn ℝ 2` for each on the complement of {0}; strict positivity of each at every point; and the two equations away from zero with standard `Laplacian.laplacian` and `Real.rpow ‖x‖ A * Real.rpow (v x) p` (and the swapped equation). There is no pressure estimate, energy bound, Liouville hypothesis, Newton-representation assumption, or hidden regularity-at-infinity field. `Subcritical` is exactly `(n+A)/(p+1)+(n+B)/(q+1)>n-2`.

The unweighted Main declaration explicitly quantifies `n : ℕ`, `3≤n`, real p,q with `0<p`, `0<q`, and `1/(p+1)+1/(q+1)>(n-2)/n`. Its conclusion forbids the existence of functions `u,v : Space n → ℝ` that satisfy `ContDiff ℝ 2` globally, are strictly positive everywhere, and obey `-Δu=v^p`, `-Δv=u^q` everywhere. It has no boundedness restriction. It therefore contains the intended positive, bounded-entire input for p,q>1 as a strict subcase, if its proof is validated.

The proof of the unweighted declaration sets A=B=0, multiplies the hyperbola inequality by n>0, applies the weighted theorem, obtains continuity and off-origin regularity from the global C² assumptions, and removes the weights by `Real.rpow_zero`. This specialization is mathematically direct; the formulas do not exchange p and q or their associated components.

The source closure defines no replacement Laplacian or custom Laplacian instance. Pinned Mathlib `Mathlib/Analysis/InnerProductSpace/Laplacian.lean`, inspected after cloning dependencies, defines the instance through the canonical covariant tensor and proves `laplacian_eq_iteratedFDeriv_orthonormalBasis`, expressing it as the sum of the second derivatives in an orthonormal basis (lines 133–174; standard-basis identity lines 191–195). This is the usual Euclidean Laplacian, with no unusual sign or normalization. Source SHA-256: `095462454e91ffe43c6b3a190f7643e52d6664cbbbb44cbb49ef44308c521715`. This semantic source was inspected, not compiled locally.

The exact follow-on gaps are substantive:

1. Nonnegative solutions are not the theorem's quantifier. A separate strong maximum principle argument must show any nonzero nonnegative classical pair is strictly positive in both components; the zero pair must remain allowed. That transfer is not formalized by Main.
2. Arbitrary-domain estimates, gradient estimates, exterior decay, half-space nonexistence, and fixed bounded-domain Dirichlet compactness are absent from these Main declarations. A validated input Liouville theorem would not make the entire requested follow-on package formalized.
3. The formal declaration gives a suitable PDE statement, but until the actual proof compiles and its axiom closure is checked, absence of explicit source holes does not establish proof validity. Independently audited analytic arguments remain necessary if no formal reproduction is available.

## Comparator and trust audit

`ComparatorChallenges/HenonEmden.lean` intentionally proves its challenge theorem with `sorry`. It is not the proof. Its import, namespace, `Space`, `IsSolution`, and `Subcritical` prefix are byte-identical to actual `Model.lean`. The challenge config selects `OAI.Analysis.HenonEmden.Main` and `OAI.HenonLaneEmden.main_nonexistence`; permitted axioms are only `propext`, `Quot.sound`, and `Classical.choice`; `enable_nanoda` is false. The config does not separately select the unweighted corollary, so both declarations should be checked in a reproduction.

Source-level scan of all 96 copied OAI files found zero occurrences of `axiom`, `sorry`, `admit`, `unsafe`, `opaque`, `native_decide`, `implemented_by`, or `extern`. `validation/formal_source_trust_scan.json` preserves the exact scan terms and result. This is only a textual/source trust scan, not the transitive axiom set of the elaborated theorem. No `#print axioms` result exists. The use of classical/noncomputable analysis is expected; the allowed classical axioms are not extra PDE assumptions.

Upstream `lean/README.md` recommends building small portions of the large library and notes an unrelated Linux mmap limitation. `lean/ComparatorChallenges/README.md` requires Comparator, Landrun, and Lean4Export. None of those executables was installed/on PATH at audit time; Comparator/Nanoda/Lean4Export were not run. The root repository README explicitly describes mixed verification stages and directs readers to manuscript-specific citations; it does not certify every result merely from its catalogue entry.

## What the local attempt did and did not do

A minimal copied package was prepared at ignored `validation/formal_build/`, retaining the exact OAI source content while avoiding the many unrelated upstream Lake packages and compatibility patches. Dependencies were cloned under this owned folder. `lake update` began compiling only the cache tool's infrastructure. The auto-cache hook was stopped before the full Mathlib cache download: available disk was approximately 2.4 GiB, while the proof's unchanged `Model.lean` imports the whole Mathlib umbrella. A full artifact fetch risked exhausting the shared filesystem.

`lake env lean OAI/Analysis/HenonEmden/Model.lean` was then actually attempted and failed at its first line with `unknown module prefix 'Mathlib'` because the dependency artifacts were missing. This is an environment failure, not evidence against the proof. Logs: `validation/formal_update.log` and `validation/formal_model_elaboration_attempt.log`. No HenonEmden OAI source was elaborated; no target `.olean` was produced; no target axiom closure was printed. The disposable owned `.lake` dependency/cached infrastructure tree (approximately 692 MiB) was removed, restoring available space to approximately 2.9 GiB. Shared or third-party files were not deleted.

An initial directory-selection mistake made one `lake update` attempt in the research repository root; it exited immediately because no Lake configuration existed and created no `.lake`. Its log was moved into the dedicated project as `validation/formal_wrong_directory_attempt.log`. No source or shared Git state was mutated.

## Reproduction artifacts

- `validation/formal_prepare.py`: extracts the exact pinned import closure directly from read-only Git objects, copies upstream Lean license, uses the exact toolchain and minimal Mathlib pin, and creates the axiom audit file. Running this script was checked to reproduce the same 96 module/hash pairs.
- `validation/formal_lean_dependency_lock.json`: minimal dependency lock generated by the attempt; unrelated packages are omitted, exact Mathlib/transitive pins retained.
- `validation/formal_AxiomAudit.lean`: prints both actual declarations and both transitive axiom lists when their imports are built; it was prepared but not run.
- `validation/formal_build/README.md`: detailed local recipe and explicit unverified status; the copied build directory is ignored by project policy.

When sufficient storage is available, run `formal_prepare.py` (which preserves the lock), then run `MATHLIB_NO_CACHE_ON_UPDATE=1 lake update`, then use `MATHLIB_CACHE_DIR="$PWD/cache" lake exe cache get`, `lake build OAI.Analysis.HenonEmden.Main`, and `lake env lean AxiomAudit.lean` from the copied folder. Store resulting logs, exit codes, source hashes, and the exact printed axiom lists. A passing build plus permitted axioms would validate the source proof in that Lean/Mathlib environment; the analytic semantic interpretation and follow-on transfers must still be audited.

No Git mutations, publication, external communication, or release action was performed by this audit agent. Later upstream corrections/priority are not resolved by this audit; all conclusions above are pinned to the specified input version.
