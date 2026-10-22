# Verification boundaries

A fixed externally authenticated bootstrap validates the whole final delivery, including every mathematical proof, audit, acceptance record, exact checker, reference stdout/stderr and labeled pre-seal receipt. The final manifest excludes only itself and the bootstrap to avoid cycles; the external bootstrap anchors the manifest and authenticates the verifier and test harness before executing them.

Fresh full stdout and stderr are pinned separately for normal, -O and -OO. Replay compares every byte without normalization and recursively checks exact JSON types and values. Identical reference bytes across modes are permitted for mode-independent original outputs; the execution mode is independently checked by the isolated launcher and recorded by the guard. A PASS token alone cannot satisfy validation.

The two unchanged mathematical checkers contain explicit failures, not optimization-disabled assert statements. Their 23+41 checks support the written analytic proofs but do not prove compactness, extremality, nonlinear existence, or the full source target. The guard tests 39 genuine algebra mutants per mode: 20 authored-checker mutations and 19 independent mutations. Each subprocess records UID/EUID, optimization level, file/directory modes, two actual write denials, and full output. Two additional deliberate failure runs test the explicit failure paths.

The mutation harness also tests every delivery member against the fixed external anchor, missing/extra/symlink/hardlink/FIFO paths, resealed altered mathematical prose, unauthenticated controls, malformed/duplicate/nonfinite JSON, schema and acceptance changes, nested type mismatches, stdout/stderr replacements, wrong exit types, and hostile environment/import paths. Before/after hashes cover the entire delivery and each mathematical fixture. The original integrity-only verifier is excluded.

Preparation receipts are historical pre-seal snapshots, explicitly labeled with their own stage. Final external validation is executed after the final seal and records that final inventory outside the packet; it is not circularly included in the inventory it attests. Stages not performed here are marked NOT_RUN: original integrity-verifier replay, historical audit-harness replay, new source search, source-body replay, dataset replay and formal proof-assistant verification.

No automatic tool result certifies mathematical prose or global source completeness. The external pins bind the unchanged reviewed text to the independent audit's scoped acceptance.
