# Reproduction scope

The original five-pass proof/audit files and their original manifests remain unchanged. The portable additions do not change their mathematical assertions or the terminal UNSOLVED 5/5 status.

## Fresh computational replay

- The unchanged pass-5 exact script reruns the unchanged pass-1–4 exact scripts in temporary locations, verifies their sealed hashes and byte-identical outputs, and checks 51 final identities: 201 exact checks plus 14 quadrature comparisons in total.
- All five original positivity scripts are rerun and their outputs compared byte-for-byte with their frozen JSON records.
- The original pass-1 radial scaling checker and pass-1 audit checker are rerun and compared with their frozen output records.
- The original pass-5 audit is rerun and compared byte-for-byte: 57 additional algebraic, integrity, execution-record, and source-metadata controls. Its execution-record checks inspect the preserved historical report; this package separately reruns both scripts themselves.
- All mathematical checks from the pass-2–4 audit scripts are rerun using the explicit adapters in portable_audits. The resulting check lists must exactly equal the original lists after removing only the named source-document byte checks.

## Historical source verification, not replayed

The original pass-2 audit checked nine primary PDFs; pass 3 checked two; pass 4 checked one. The twelve source-document byte/hash checks are not rerun because no source documents are included. Their original successful records, bibliographic data, sizes, hashes, inspection locations, and retrieval limitations are retained as historical metadata. No source is downloaded by the public verifier or replay suite.

The adapters replace only these external-document reads/checks and the associated result descriptions. Original scripts remain available for comparison, and ADAPTATIONS.json names every omitted check and both the original script and omitted-block hashes. Reproduction does not treat omitted checks as passes.

## Scope limits

All replays are supplementary auxiliary computations. They do not independently certify analytical chain rules, compactness, admissibility, source theorem applications, or whole-domain regularity. Complete authored analytical proofs and their audits are retained for mathematical review.

The final acceptance chain recursively checks 85 bound entries across the first four original manifests and 30 record occurrences in the final manifest. Repeated references to the same file remain repeated chain records, not additional independent evidence. The package manifest lists each payload file once and is itself externally identified by SHA-256 in the build receipt.

## Optimization and execution guards

The public wrappers use explicit exceptions rather than removable assertions. Historical checkers are launched unoptimized; optimization inheritance is removed for their nested subprocesses. Output files must be freshly generated in each disposable copy. Six execution modes pass the full replay and reject all 66 invalid-input/execution cases. See [the packaging correction](PORTABILITY_FIX.md) and [the reproducible controls](test_release_guards.py). Direct optimized invocation of the preserved historical scripts is not the supported replay route.
