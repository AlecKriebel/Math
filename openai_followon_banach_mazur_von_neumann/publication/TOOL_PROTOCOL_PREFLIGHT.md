# Publication-tool protocol preflight

Timestamp: 2026-10-07T05:54:45.793619+00:00

Read the repository's current zenodo_deposit_tool/README.md, deposit.example.json, manifest validator and command implementation, and ran only CLI help for the top-level and four subcommands. No actual manifest check, remote inspect, stage or publish action was executed; no credentials were read, displayed or copied. The mathematical/source gates are still incomplete, so no final deposit manifest is prepared.

The actual manifest must contain exactly metadata and files. File entries allow only path and optional name; paths resolve relative to the manifest, distinct simple remote filenames are required, and all local upload files must exist. The helper hashes local files with MD5 and SHA256. It verifies the exact remote file set and metadata before publication and requires the project's actually verified draft ID with --confirm-id. Use production by default; no --sandbox flag for the final preprint. The original separate check → stage → inspect → publish → inspect --check-doi order matches the current help.

The later upload payload must expose the paper PDF independently, alongside the source/reproducibility archive or archives; an outer upload-kit archive is not a substitute. A kit cannot be frozen or reviewed as final while the general theorem remains conditional. Publication/DOI/tracker readiness is not inferred from CLI help.

The example uses creator name Kriebel, Alec, ORCID0009-0001-9320-500X and license cc-by-4.0. Its example affiliation must be omitted because the human's explicit brief forbids inventing affiliations. This preflight records the example license without treating it as a previously selected final package license; make the final rights/attribution decision on the actual payload before publication. Licensed unchanged upstream Apache-2.0 material must retain its original attribution/license; local Roydor and arXiv PDFs lacking redistribution permission stay excluded.

State lookup is based on the absolute project-local manifest path and separates production from sandbox. Before any draft creation, check/reconcile this project's existing state and any ambiguous previous attempt. A reserved DOI is not publication. A successful publication receipt is retained before DOI resolver lookup; delayed resolver propagation must not trigger another deposit. If tracking fails after publication, reconcile only tracking. The Google Workspace tracker command/schema inspection remains a later step, after confirmed publication as the original brief requires.

Tool snapshots are hashed below so a later changed tool can be rechecked. No unrelated record, secret location or tracker was modified.
