# KP-1.65 independent audit package

The accepted object is the exact corrected ZIP identified in EXACT_ACCEPTANCE.json. Read EXACT_ACCEPTANCE.md for the short decision, INDEPENDENT_AUDIT.md for the mathematical and integrity review, and PRIMARY_SOURCE_REVIEW.md for the scholarly scope review.

The author archive is an immutable historical input. It is included with its original external manifest for provenance, not as the final accepted wording. The corrected archive is separately provided with a new external manifest. CORRECTION.patch records the actual authored-text and status changes. PATCH_REPLAY.json records successful application to a fresh author extraction and byte equality of all nine corrected files after regeneration of the internal manifest.

## Reproduce the diagnostic audit

From the audit directory after extracting the full audit ZIP:

    python verify_independent_audit.py --zip ../corrected_artifact/LAGRANGIAN_ELEMENTARY_2724_CORRECTED_SAFE.zip --manifest ../corrected_artifact/LAGRANGIAN_ELEMENTARY_2724_CORRECTED_EXTERNAL_MANIFEST.json

Repeat with python -O and python -OO. Substitute the two author_archive filenames to audit the original author bytes. These commands verify ZIP/member/internal-manifest integrity, status scope, baseline and relocated diagnostic runs, direct false premises, semantic mutations, and artifact-integrity negative controls.

The optional --catalog, --problems, and --reports arguments take separately available corpus files; all three must be supplied together. The optional --source-directory argument takes a directory of separately available PDF sources and matches them by SHA-256 rather than by private path. No corpus or source documents are distributed here. Skipped optional checks are explicitly marked performed=false.

The patch leaves verify_local_model.py unchanged. To reproduce internal-manifest regeneration after applying the patch, list every resulting top-level file except FILE_MANIFEST.json, sorted by filename. For each, record path as its filename, bytes as file length, and sha256 as the lowercase SHA-256 hex digest. Serialize the object with schema_version=1, self_excluded=true, and that files array using json.dumps(..., indent=2, sort_keys=True), followed by a newline. This is the same format as the author's manifest.

Recorded replays under normal, -O, and -OO interpreters are included for both artifacts. They bind the input archive hashes and mark the original problem unresolved. The independent harness's outputs agree across interpreter modes.

No numerical or finite symbolic test proves KP-1.65. The accepted mathematical claim is the written local diagnostic, with the boundary and isotopy limitations explicitly retained.
