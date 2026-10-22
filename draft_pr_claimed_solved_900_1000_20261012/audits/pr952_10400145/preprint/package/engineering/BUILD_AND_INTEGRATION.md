# PR952 engineering handoff

This folder supplies finite package verification and inert operational predicates. It supplies **no independent mathematical review credit, no full-package acceptance, and no executable service adapter**. All original33 files and the independently authored math checker retain exact bytes. No source PDFs, third-party extracts/images, raw corpus, private source records or credentials are public inputs. Host Python/stdlib/OS and nonconcurrent source replacement remain trust roots; resource bounds are not an OS sandbox.

## Authenticate before running

Receive the SHA256 of this folder's `MANIFEST.json` through the external handoff, authenticate it, then verify its explicit `files` and `explicit_public_allowlist`. A sidecar obtained with the same mutable files is informational. Authenticate `verify_package.py` separately against the verified manifest before execution. All driver launches use `python -I -S -B`; optimized outer launches add `-O` or `-OO`. The shipped math checker SHA is `ff44cdce74d36b40995843f7bc450e31fcac532163f3a411da51f3244ea82601`.

## Closed package construction

Root selects every public file deliberately. Do not recursively copy the audit or any private evidence folder. Include these paths in the new closed package:

- `checks/independent_math.py`: exact shipped checker bytes.
- `original/unsolved_math_prioritization/attempts/10400145/` and all33 exact originals with regular single-link mode0644.
- The current paper and specifically selected source-free proof/review/provenance/support files. Include the final verifier and test source bytes in the package for inspection.

Create `PACKAGE_MANIFEST.json` with precisely these fields. `files` lists every regular package file except the manifest itself; every entry has exact integer `bytes`, lowercase `sha256`, and `mode: "100644"`. No permissive defaults or type coercions are allowed.

```json
{
  "schema": "pr952-sourcefree-package-v1",
  "version": 1,
  "problem_id": 10400145,
  "original_head": "989a532ae1d50894190d010a0a02ba8c3d71ee05",
  "files": {"EXACT_CANONICAL_PATH": {"bytes": 123, "sha256": "ROOT_FILLS_64_LOWER_HEX", "mode": "100644"}},
  "archives": {}
}
```

If any listed payload is a ZIP, `archives` must contain that exact path mapped to its complete expanded regular-file map in the same entry schema. Nested ZIP members are finite opaque bytes; no recursive execution or extraction occurs. The outer verification ZIP contains exactly `files` plus `PACKAGE_MANIFEST.json`; entries have Unix creator3, exact type/mode0100644 and zero low attributes. Optional explicit directories use040755/attribute0x10, contain no data and correspond to implied nonempty ancestors. Stored ZIP entries are convenient; deflated entries must stay below the bounded200:1 ratio. Reject aliases including implied directory aliases, duplicate paths, traversal and noncanonical names. The verifier validates the complete ZIP metadata before any decompression, then externally authenticates the embedded manifest before payload reads, and authenticates all payload bytes before constructing any replay snapshot.

Compute the final manifest hash independently; root publishes this and the verifier hash outside the mutable package. First verify a directory:

```
python -I -S -B EXTERNALLY_AUTHENTICATED_VERIFIER --root CLOSED_PACKAGE --manifest-sha256 EXTERNAL_MANIFEST_SHA --run-checkers --work-dir OWN_EMPTY_WORK_PARENT
```

Then hash the finished ZIP independently and replay it cold:

```
python -I -S -B EXTERNALLY_AUTHENTICATED_VERIFIER --archive FINAL_ZIP --archive-sha256 EXTERNAL_ZIP_SHA --manifest-sha256 EXTERNAL_MANIFEST_SHA --run-checkers --work-dir OWN_WORK_PARENT
```

Repeat cold execution with outer `-O`, outer `-OO`, and env2 (`PYTHONOPTIMIZE=2`, hostile `PYTHONPATH`/user site and a different working directory). The driver forces children to `-I -S -B` and runs the fixed four stages under normal/O/OO, requiring exact per-stage stdout equality across these three inner modes. Preserve raw output and startup observations for every outer run; do not normalize away fields. The final ZIP and tree must reproduce identical manifests and payloads. Root's future whole-freeze schema must bind these receipts and the exact PDF/ZIP/descriptor/operations/review/disposition files together.

## Run the meaningful inert profile

`test_profile.py` takes `--originals`, `--verifier-sha256`, and `--work-dir`. Authenticate test source first. It builds private owned fixtures, authenticates all original inputs, performs the full four-mode cold replay, tests byte/schema/namespace/object/resource/ZIP guards and executes certificate mutants directly under normal/O/OO to ensure semantic checks are exercised beyond stale hashes. It preserves no source corpus. Run this harness itself under normal/O/OO as well; its verifier compilation uses the actual harness optimization. Capture every launch's stdout/stderr/return code, including any failure, as distinct evidence. `test_observations.py` takes the external SHA256 of `observation_checks.py` as its sole argument and is also run in normal/O/OO.

## Precise scope and limits

Supported child stages are independent_math, original author bootstrap/packet, original algebra audit, and original source-bridge finite algebra. No original source-dependent full launcher is executed. Every receipt keeps Linux legacy full/bwrap/EROFS, primary-source inspection and topology reproof as NOT_RUN, whole-filesystem readonly untested, and human/formal/full-paper certification false. Current receipts are new portable finite observations and never replace or relabel historical receipts. The independent checker corroborates finite algebra and identities; paper proofs and cited topology require separate review.

The bounded subprocess wrapper caps output and wall time of its direct child. It is not a memory/process tree or filesystem sandbox. Installed Python/stdlib/OS and nonconcurrent inputs are explicit assumptions. Inputs must remain stable while inspected; this profile does not claim race-resistant operation against an adversarial host account. No code claims publication readiness.
