# Independent reproducibility audit criteria

Sealed UTC: 2026-10-12T21:47:47.875395+00:00
Target: PR 436 / KOU21.60 / upstream ID 2569, frozen head c7805ab0804f50c6f4b0d1dda99e433dbb702ae2.
Scope: source integrity, executable evidence, code/output agreement, reproducibility and computational scope. No fresh candidate proof search; the author's five proof-attempt responses are exhausted.

This criterion was written before reading historical audit conclusions or current peer conclusions.

## Falsifiable acceptance criteria

1. Recompute SHA-256 for every frozen file and compare each binding with the root receipt. Do not treat reported metadata as evidence. Check whether historical manifests cover their claimed files, including self-binding or omissions.
2. Read every executable and controlling mathematical/status/report file in the 26-file frozen payload. Identify dependencies, absolute paths, mutable output destinations, random seeds, finite test coverage, essential assertions and whether the textual claims exceed executable evidence.
3. Copy original bytes into private fixtures; run each original entry point in normal and optimized Python where feasible. Capture command, interpreter, dependency versions, timestamps, exit status, stdout/stderr, output hashes and actual outcomes. Never repair sealed/original script bytes or allow them to write in the frozen source folder.
4. Compare newly generated output bytes and mathematical fields against the historical output. Investigate non-determinism, omitted validation, and environment-dependent or private-path behavior.
5. Apply meaningful fault-injection and boundary controls. An exit code of zero is insufficient if optimization removed the checks; a removed essential assertion is a negative finding even if the unmodified script happens to succeed. Quantify actual checks, not inflated filler counts.
6. Keep finite arithmetic certification distinct from claims about general representation theory or semiperfectness. Independent checks may verify constructions already claimed, but may not become further author proof-search turns.
7. Record raw failures and exact remaining gaps. Classify material defects candidly, without forcing either rejection or acceptance. Suggest a focused verification repair only if warranted.

Success for this audit means a reproducible, independently inspectable record with source bindings, real executions, negative/positive controls, scope limitations and a typed result. Success does not itself establish the mathematical theorem.

Completion estimate: 5% of this reproducibility audit; no mathematical verdict yet.
