# Reproduction boundary audit

2026-10-07 05:45:51 UTC. Scope: archive reproduction boundaries only. No theorem review,
external communication, publication, or edits to the publication package.

## Strongest verified finding

The v2 reproducer creates its temporary directory next to the requested receipt
and then copies its whole package root. For the exact README relative-output
command, the temporary directory is inside that root, so copying the root copies
the temporary destination recursively. This is a static finding; the faulty v2
copy was not executed by this audit. Completion estimate: 50% of this boundary
audit until the repaired v3 archive passes the harness.

## Repair requirements and adversarial review

The root agent's proposed repair is to copy only manifest-declared members plus
the manifest and reject output collisions. That fixes the recursion mechanism
provided the following conditions hold:

1. Validate each manifest member as a canonical relative file path before
   reading/copying it. Absolute paths, traversal components, aliases, and
   file/directory conflicts must not escape the package or clean-copy root.
2. Make an independent copy of regular payload bytes; do not preserve source
   symlinks. Parent-directory symlinks matter as well as leaf links.
3. Protect the manifest itself, all declared members, and symlink/hardlink aliases
   from receipt overwrite. Path resolution alone does not detect hardlinks.
4. Verify the actual bytes executed in the clean copy, either through a single
   read/hash/write operation or by rechecking copied hashes before execution.
   Parse and copy the same manifest bytes.
5. Resolve output once, validate its parent/type before computation, and describe
   the narrower manifest-declared copy accurately in the README.

An independent subordinate audit confirmed these requirements without running
or modifying the reproducer. Manifest tampering/malicious executable code is not
the security scope: this is protection against accidental boundary errors in the
authored package. The manifest is a consistency record, not a signature.

## Safe harness

`reproduction_boundary_harness.py` creates an extraction only beside itself,
refuses the known v2 archive and any `copytree` reproducer, and runs the exact
README command twice from the extraction. It also tests existing nested output
directories, absolute output paths, unlisted extras, each declared-member
collision, manifest collisions, normalized/absolute aliases, and symlink/hardlink
aliases. It hashes every protected original before and after every run. Collision
runs guard attempted payload writes: triggering the guard fails the test and
cannot be mistaken for native collision rejection. The guard targets accidental
writes in the authored parent process; it is not a hostile-code sandbox.

The archive input is never modified. The harness records successful-run evidence
in a separate JSON report alongside its disposable extraction. Execution awaits
the root agent's explicit notice that a repaired v3 archive is ready.

2026-10-07 05:45:51 UTC checkpoint: the harness passed a syntax check and a local
hardlink-write interception self-check without invoking any reproducer. The
protected canary remained byte-identical. Audit completion estimate remains 50%;
the exact README run and native rejection behavior of v3 remain unverified.

## Final v3 verdict

2026-10-07 05:47:58 UTC checkpoint. **PASS; no reproduction boundary blocker
found. Completion estimate: 100% of this scope-limited audit.**

The root agent authorized testing the repaired archive at
`publication/zenodo-upload-kit/source-and-verification.zip`, SHA256
`b49a3eaacd7d89024d8b43e9a37b74c68b9f235d3b26ff8dd5c2540e85562b5e`.
The harness completed at 2026-10-07 05:47:28 UTC with 39 recorded runs:

- The exact README command passed twice from inside the fresh extraction.
- Nested and absolute receipt destinations passed with an unlisted canary
  present; the receipt covered all three finite checks with return code zero and
  correct stdout hashes.
- All 35 collision destinations received native rejection: all 28 declared
  members, the manifest itself, payload/manifest symlink and hardlink aliases,
  plus absolute and lexically normalized aliases.
- Every protected original hash matched its baseline after every run. No
  collision-write guard intervention occurred. The source ZIP's hash was
  rechecked after the audit and remained unchanged.

Evidence is in
`v3-run-20261007T054657960966Z/boundary-harness-report.json`; its extraction and
receipts remain beside it for inspection. V2 was preserved and never executed.

Static inspection of the exact extracted v3 reproducer confirms that it reads,
hashes, and independently copies the same payload bytes, copies only the declared
payload and captured manifest, validates canonical relative member paths and
resolved internal regular sources, protects samefile aliases, and replaces the
receipt atomically. Internal source symlinks are dereferenced into independent
copied bytes; targets outside the package are rejected. This closes the reported
recursive-copy defect and the accidental-overwrite boundary within the tested
archive workflow. The evidence makes no additional theorem or security claim.
