# Runtime-path and clean-delivery audit

## Result

PASS. The accepted runtime-provenance/path finding is closed.

- Clean package: no `.venv`, `review_runs`, caches, symlinks, special
  objects, or runtime output.
- Integrity is run before runtime creation.
- Reserved path components are checked with `lstat`.
- Creation/opening is descriptor-relative with `O_NOFOLLOW|O_DIRECTORY`,
  inode verification, and `0700` enforcement.
- Lock handling is relative to a held real directory descriptor.

Fresh disposable mutations:

- runner: eight of eight symlink/wrong-type substitutions rejected;
- integrity checker: the same eight of eight rejected;
- outside-target writes: zero;
- clean path modes: four of four `0700`;
- pre-existing real `0777` paths: tightened to `0700`; and
- failed outer integrity: no `review_runs` created.

The remaining concurrent same-UID swap possibility after setup descriptors
close is informational defense in depth outside the repaired pre-existing-path
threat model.
