# Independent replay and execution-hygiene audit

## Initial trust boundary

Before any author code was executed, all four externally supplied SHA-256 pins and byte counts were independently verified: original archive, external manifest, external bootstrap, and validation receipt. The archive's eleven-member inventory, regular-file types, names, sizes and hashes were checked. Working author files were compared byte-for-byte to these members. All author proof, scope, metadata and program files were read directly. No author executable was imported to perform the initial gate.

The original mathematical checker was replayed directly from verified bytes with Python -I -S -B, from a different current directory. Its output exactly matched the original RESULTS.json. A strict -I -S -B -O invocation deliberately failed with its explicit optimized-execution error. That is a successful fail-closed test, not an optimized computational pass. The original optional provenance checker reproduced its original output when supplied all three corpora and six PDFs.

## Defect and actual correction

The original external bootstrap launched its checker with -I -B, omitting -S. Its normal author-recorded success therefore did not establish no-site startup isolation for the child. We did not execute that original normal bootstrap during this review. This is an execution-hygiene defect against the requested strict replay protocol, not evidence of bad mathematics or observed compromise.

The corrected external bootstrap requires isolated/no-site/no-bytecode flags for itself and passes -I -S -B to its child. It also rejects symlinked entrypoints and symlink components in entrypoint/input paths. It retains explicit checks rather than assertions and deliberately rejects -O. Its external manifest pin is bound to the separately frozen corrected archive. Neither original archive nor original external file was altered.

The separate source-scope patch was fully read, pinned, applied with zero fuzz to a clean extracted derivative, and checked against each provided before/after digest. Its v1 PDF metadata was independently rehashed and textually verified. Subsequent derivative adjustments update review status, document the flags, and add derivative notes; mathematical sections and both original checker programs are unchanged. COMBINED_AUTHOR_CHANGES.patch and BOOTSTRAP_HARDENING.patch give the actual differences. CORRECTED_DERIVATIVE_BINDINGS.json identifies the exact accepted bytes.

## Actual tests

The corrected bootstrap verified all twelve corrected members and reproduced RESULTS.json exactly. Eighteen controls then passed: strict normal relocation amid hostile current-directory modules and startup environment; optimized fail-closed behavior; missing bytecode flag; archive, manifest, bootstrap and ancestor symlinks; truncation and same-size corruption; manifest mutation; changed checker; added entrypoint; traversal name; ZIP symlink; duplicate ZIP member; coherent archive/manifest substitution; and changed bootstrap rejected by an outer pin before any modified code ran. No hostile import marker or bytecode file was created.

Archive mutations are rejected by the complete archive or manifest pin before the deeper ZIP checks. These results do not pretend to exercise otherwise unreachable inner validation branches with trusted pins rewritten. A bootstrap's own hash must be checked externally before starting it; no self-verifying program can safely authorize arbitrary replacement startup code.

The independently authored mathematical checker and the control harness were also run under both -I -S -B and -I -S -B -O. Each normal/optimized pair produced byte-identical output. The control harness always launches the deliberately non-optimized author checker through the corrected bootstrap; this is distinct from the explicitly rejected optimized author mode.

The corrected optional provenance replay checked the three complete corpora and all seven PDFs, including v1. Textual source review is not represented as a consequence of hashing or of program replay.

## Limits

These are reproducible pin, path, startup and mutation controls. They are not an operating-system sandbox, proof against a malicious system Python or root process, formal certification of mathematics, or a literature-status oracle. The archive pin is necessary but does not make arbitrary unreviewed code safe; the pinned code was also read. No network or repository mutation is part of the checker programs or this audit.
