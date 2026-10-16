# Frozen artifact attack plan

UTC: 2026-10-16T05:18:48.908137+00:00. Completion estimate: 5% of artifact audit; original research effort remains 1/5.

Scope: PR888 / PID30005079 only, exact head a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7. This is a source/package/reproduction audit, not an independent full mathematical verdict or publication acceptance. Native target pair read before this plan; source proof, audit acceptance verdicts, executable source, and original check results have not yet been read.

Native target: construct an explicit nontrivial canonical degeneration of a Fano variety whose entropy-minimizing valuation is nondivisorial. Necessary mathematical ingredients include valid Fano construction, nontrivial canonical degeneration, global entropy minimizer identification, and nondivisoriality. Executable checks can cover only their demonstrated finite arithmetic/analytic conditions.

Planned attacks, fixed before source acceptance verdicts:
1. Authenticate all 21 actual immutable Git blobs at head against extracted bytes, SHA256, length, modes and tree inventory. Record exact original before/after pins.
2. Read every executable and launcher fully before running; identify child invocation, dependencies, output writes, assertion use, working-directory assumptions, and result provenance.
3. Replay each original claimed check with the actual normal interpreter and optimized interpreter in a private copy. Capture return codes, output, generated files, assertion counts, and child optimization/isolation behavior.
4. Check all original package, source, publication, edition, and patch inventories and links against their stated scopes; reconstruct reversible patches where supported.
5. Challenge malformed hashes, duplicate JSON keys, path traversal, empty inventories, omitted/missing sources, modified proof, modified checker, damaged patches, stale results and extra files. Record precise tested controls and limitations without inferring general security.
6. Inspect numerical certificates (exact versus floating-point versus claimed precision); locate the precise mathematical statements actually tested and unsupported global/infinite invariants. Add bounded independent checks only where material.
7. Freeze own preliminary artifact assessment before reading original acceptance verdicts, then compare their statements against evidence.
8. Write a self-contained report and safe hash manifest; exclude private scratch, raw primary/native corpus data, renders, credentials and private absolute paths. Hash manifest explicitly excludes itself and report provides its external SHA256 and size.

No candidate modification, Git mutation, remote operation, publication, external communication, corpus expansion, or PDF authoring. Read-only Git is invoked with gc.auto=0. All executable replay and adversarial mutation occur inside this audit's own private_tmp. Parent alone receives findings.
