# Exact-source selective Lean retry assessment

Checkpoint: 2026-10-07T05:51:05.571218+00:00. Best-guess completion toward independent kernel reproduction: **10%**. The authenticated source setup remains complete; successful dependency setup, MainResult compilation/import, and axiom interrogation remain unverified.

**Outcome: feasibility assessment stopped; no new theorem build or cache download was launched.** The initial storage improvement was transient. No live build, downloader, or tool session remains.

## Verified inputs and formal target

The retry preserved `/Users/alec/Desktop/math` read-only at upstream pin `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. A new verification of the 372 copied OAI modules in `research/lean_audit/build/OAI` found **zero SHA256 mismatches** against `import_closure.json`. The available read-only mathlib source checkout remains clean at `d13f23b723b8a846827a245b89c10fc7d3f11612`, with Lean toolchain `leanprover/lean4:v4.34.1`; the installed binary reports Lean 4.34.1, compiler commit `5045d0056413266e57c625dcd7c365b10e377c52`.

The actual target remains `OAI.Analysis.BoundedHochschild.MainResult`, declaration `OAI.BoundedHochschild.KadisonRingrose.main_result`. The existing `AxiomProbe.lean` requests actual axiom lists for `main_result`, `bounded_primitive`, `vanishing`, and `normal_tracial_primitive`. No comparator stubs or replacement theorem were built. As established by the static semantic audit, the declaration concerns ordinary bounded complex multilinear self-cochains on abstract complex Banach-predual `WStarAlgebra` objects; an arbitrary concrete operator-algebra corollary still needs the universal formal predual bridge described in `reviews/lean_independent.md`.

## Exact selective-cache conclusion

There are **123 direct `import Mathlib`** statements in the unchanged OAI closure. Pinned `Mathlib.lean` directly imports **8,529 `Mathlib.*` modules**; the exact mathematical umbrella closure contains **8,530 Mathlib modules including the umbrella**. Every corresponding Mathlib source is present, and every mathematical Mathlib source module belongs to that closure. An independent subagent confirmed these counts by parsing headers with nested-comment removal and public/private/meta import qualifiers, then traversing the graph.

The pinned official cache implementation retains a selected root and all transitive cache-covered imports (`Cache/Hashing.lean`, `insertDeps` and `HashMemo.filterByRootModules`; used by `Cache/Main.lean`). Thus `cache get Mathlib` cannot reduce the required mathematical module set. Selecting only C-star/von Neumann analysis modules or replacing `Mathlib.lean` would change the checked input and would not reproduce this source.

Each official module archive includes its compiled `.olean`, trace, interface, generated C, hashes, and present optional sidecars (`Cache/IO.lean`, `mkBuildPaths` and `packCache`). The standard client has no artifact-type extraction filter. Retaining fewer artifact types while keeping every required module might save storage, but **this assessment did not establish a supported, sufficient artifact subset for Lean 4.34.1**. The mathlib dependency packages add artifacts beyond the 8,530 mathematical modules.

## Storage evidence and exact stopped step

| Observation | Available or measured bytes |
|---|---:|
| Initial volume report | about 2.7 GiB available |
| Preflight at 2026-10-07T05:46:48.375703+00:00 | 1,290,461,184 available (about 1.202 GiB) |
| Read immediately after the reserve halt | 1,139,523,584 available (about 1.061 GiB) |
| Safety floor imposed by this retry | 1,073,741,824 available (1 GiB) |
| Subsequent outcome snapshot at 2026-10-07T05:49:37.604976+00:00 | 1,298,468,864 available |

These fluctuations occurred while this retry wrote approximately half a MiB of source/diagnostic material. They therefore defeat an assumption that the original 2.7 GiB remained available. At the post-halt observation, only **65,781,760 bytes (about 62.7 MiB)** remained above the safety floor.

The sole attempted dependency action was `python3 research/lean_audit/build/selective_retry/fetch_dependency_sources.py`, a bounded metadata/source assessment, not Lake dependency resolution or theorem compilation. It fetched three tiny pinned dependency source snapshots (Plausible, LeanSearchClient, ImportGraph), retaining only `.lean` files. Compressed tar data stayed in memory. Before the fourth package, its check for the 1 GiB reserve plus 64 MiB metadata budget failed, and the process exited 1 with:

```text
RuntimeError: Stopped: insufficient reserve for metadata-only source assessment
```

No mathlib history clone, mathlib cache archive download, cache extraction, `lake build`, or `AxiomProbe.lean` execution occurred in this retry. The three partial dependency-source directories do not constitute a complete build environment.

## Read-only runtime reuse check and quantified comparator

The original upstream Lean tree has no `.lake/build` or `.lake/packages`. The clean pinned bosonic-capacity mathlib checkout has source only. Targeted checks of the existing `universal_simultaneous_amplification/lean_formalization` and `phase5_exact_threshold/paper_db_extremality/symmetric_sector_lean` runtimes found compiled mathlib, but both use **Lean 4.19.0** and mathlib **`c44e0c8ee63ca166450922a373c7409c5d26b00b`**. They cannot be imported by the selected exact toolchain/pin. No exact-pinned compiled runtime was found in these targeted known locations; no exhaustive filesystem claim is made.

The historical runtime has 6,306 Mathlib `.olean` files totaling **4,219,377,520 logical bytes (about 3.930 GiB)**. Its Mathlib library-plus-IR artifacts total **4,752,337,934 logical bytes (about 4.426 GiB)** and **4,894,425,088 allocated bytes (about 4.558 GiB)**. `receipts/old_runtime_comparator.json` records the paths, version and exact totals.

**These historical totals are comparator evidence only, not a lower bound or safe estimate for the current pin.** Current pinned cache size and the minimum sufficient Lean 4.34.1 runtime footprint remain unmeasured. This report does not assert that the current minimum mathematically exceeds 2.7 GiB. It establishes that the standard module-selection route cannot shrink the umbrella closure, no reusable exact runtime was found in the checked locations, and a safe fitting route was not established before the available storage regressed. Launching an unknown full-cache extraction under that condition would risk repeating the documented disk-exhaustion failure.

## Strongest result and remaining gap

**MainResult remains uncompiled and unimported; none of the four axiom probes has produced an observed axiom list.** The strongest verified result is exact source authentication plus a checked explanation of why the official selective module cache cannot narrow the unchanged dependency graph. This retry supplies no kernel proof evidence for the vanishing claim or the rigidity consequences.

The exact remaining step is a successful build/import of the unchanged 372-module OAI closure against the selected complete mathlib environment, followed by successful axiom interrogation of all four declarations. Reopen the runtime route only after sufficient stable storage or a verified exact-pinned compiled runtime is available, or after a materially supported artifact-retention method supplies a measured sufficient footprint. This optional formal route does not satisfy or replace the separate Roydor primary-source gate.

## Preserved artifacts and custody

- `research/lean_audit/build/selective_retry/receipts/preflight.json`: initial bounded-retry disk/pin checkpoint.
- `research/lean_audit/build/selective_retry/receipts/outcome.json`: all 372 fresh source hash checks, exact pins, partial dependency-source hashes and stopped-step status.
- `research/lean_audit/build/selective_retry/receipts/old_runtime_comparator.json`: independently remeasured historical runtime totals.
- `research/lean_audit/build/selective_retry/fetch_dependency_sources.py`: bounded source-assessment mechanism, including the reserve guard.
- `research/lean_audit/build/selective_retry/receipts/leangz_ltar.rs` and `leangz_lgz.rs`: small public primary implementation references inspected for format feasibility, retrieved from the leangz master source; they were not compiled, installed or used as theorem evidence. Canonical source: [leangz implementation](https://github.com/digama0/leangz/tree/master/src).

All retry writes are inside the dedicated effort. Upstream and other researchers' files were read-only. No installations, Git commits, pushes, releases, manuscript edits, review-snapshot edits, or communication with external individuals occurred.
