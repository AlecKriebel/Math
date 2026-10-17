# Portable checkpoint verification

16 October 2026. Terminal mathematical status: **UNSOLVED 5/5**.

This is a packaging and computational reproduction report. The complete mathematical acceptance report and qualifications remain in the unchanged pass-5 audit directory.

## Preserved evidence

- 109 original authored or public-metadata artifacts, totaling 720,572 bytes, were copied byte-for-byte, including the frozen target, complete proofs and all original audit manifests.
- All original manifest record occurrences verify: 19, 21, 23 and 22 in passes 1–4 (85 total), and 30 in pass 5. These counts include repeated chain references, not independent mathematical results.
- No source research artifact was altered. No third-party source document, extracted source text, rendered source image, dataset content, private source, personal information, or private coordination file is included.

## Reproduced auxiliary computations

The public replay suite passed 12 direct jobs, plus four nested earlier exact replays:

- 201 exact checks and 14 quadrature comparisons, with byte-identical original exact outputs
- All five positivity-lane outputs byte-identical, including 28 checks in the final pass
- Original pass-1 scaling and audit outputs byte-identical
- 57 final audit controls with byte-identical output
- 15, 27 and 39 mathematical audit checks from passes 2, 3 and 4 respectively, matching their original check records exactly

The 12 historical third-party PDF byte/hash checks are explicitly excluded from fresh replay. Their previous results and public verification metadata are retained, and no excluded check is counted as a new pass. The original audit scripts are preserved; narrowly scoped portable adapters perform the mathematical checks without requiring the excluded documents.

[REPLAY_RESULTS.json](REPLAY_RESULTS.json) gives concise per-job outcomes. [REPLAY_SCOPE.md](REPLAY_SCOPE.md) describes the limits. Temporary clean copies are used for all script executions, and the package is verified unchanged afterward. No network access or external source download is required.

## Acceptance boundary

These checks validate preservation and the specified auxiliary computations. They do not prove E-6322 or establish a globally minimizing counterexample. They do not replace analytical peer review or justify dropping the hypotheses retained in the mathematical audits. Ball's broader adequate-growth program remains distinct from the fixed benchmark.

## Optimization-independent release controls

The wrappers were corrected without changing any accepted research artifact. Six normal/optimized/inherited-environment modes produced identical full replay results. All 66 negative controls were rejected, including independently resealed false final and nested exact identities, nonzero exits, zero exits without output and output mismatches. The 72-case matrix passed with the control harness itself launched under -OO. The original candidate files were unchanged. See [RELEASE_GUARD_RESULTS.json](RELEASE_GUARD_RESULTS.json) and [PORTABILITY_FIX.md](PORTABILITY_FIX.md).
