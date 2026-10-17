# Validation scope and replay

## What is checked

The standard-library validator verifies exact file membership, SHA-256 and byte counts, frozen proof/audit pins, full original-copy-map coverage, bounded claim flags, public-source metadata shape, local Markdown file links, UTF-8 text, and the absence of optimization-removable Python assertion statements. Symbolic links, special files, duplicate JSON keys, unexpected file types, escaping paths, and private-path/conversation markers are rejected.

The manifest is a local integrity seal, not a digital signature. Independent archive and manifest hashes must be retained outside the package to detect replacement of the complete package and its verification program. Embedded hardcoded artifact pins strengthen checks against a rehashed manifest alone.

## Three Python modes

The validator and exact-rational scalar replay are run under normal Python, -O, and -OO. Explicit runtime checks remain active in every mode. Each scalar run has an active failure control that forces a check false in an isolated copy. The retained replay evidence records all results. Run replay_diagnostics.py for a fresh execution; verify_bundle.py checks its recorded evidence but does not rerun the diagnostic.

Packaging negative controls cover altered and missing proofs, unexpected source-format files, scope-flag escalation, tampered frozen anchors even after manifest rehashing, duplicate JSON keys, duplicate manifest paths, escaping paths, symbolic links, false byte-count types, and altered replay results. Controls run only on isolated copies; accepted originals remain untouched.

The archive uses deterministic member ordering, zero timestamps, normalized ownership and permissions, and gzip metadata. Restoration admits safe regular files only, checks exact restored bytes, and reruns the validator in all three modes. The separate archive receipt records actual test outcomes and archive/manifest hashes.

## What is not checked

The scalar diagnostic replays only rational constants already used in the original proof. It does not verify the Haar completeness argument, operator identities, functional calculus, infinite frame sums, local commutation, source interpretation, or priority. Those claims are addressed by the full proof, independent audits, and adjudication. There is no numerical truncation argument or numerical approximation masquerading as proof.

A passing packaging test does not certify mathematical truth, literature-wide novelty, acceptance by a journal, publication, or any broader arbitrary-reindexing claim.

## Reviewed validator hardening

The reviewed package requires its exact 26-file membership and complete manifest schema, including the false publication flag and fixed disposition. Recorded replay check names, exact scalar values, optimization modes and stdout digests are checked. Nested pin records have explicit type, uniqueness and coverage checks. INPUT_MANIFEST.json is pinned to the original 4,200-byte seal; its 16 unedited non-manifest entries remain byte-identical. Only the five editorial/validator files identified in the integration report may differ from those input entries. The 10 original artifacts and all six nested pins are unchanged.

The expanded test harness exercises 26 cases in each of three Python modes (78 expected rejections), including re-sealed missing-reader, false-publication, falsified arithmetic, nested-pin, input-map and bibliographic-author changes. The separate archive receipt contains outcomes for the final bytes and restored package.
