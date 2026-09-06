# Local Math research preservation — 2026-09-05

This is a preservation checkpoint, not a claim that the recovered research is correct or ready to merge into current manuscripts.

The tar archives preserve unique files from six former Math clones, a linked worktree, and backup collections. Paths retain their original Documents folder names. Extract into a separate recovery directory, never over the current main checkout. The JSON manifests record original paths, byte sizes, SHA-256 checksums, archive locations, and Git blob IDs. Archive members were checked against their source checksums before publication.

Files marked `already_on_github` are omitted from archives because their exact Git blob is reachable from a verified existing GitHub branch or tag. These files can be recovered from those Git objects. Python virtual environments, interpreter caches, Git administrative directories, and Finder metadata are disposable and omitted. Explicitly private YBE material is excluded entirely. Files marked `retain_large` remain local because each exceeds GitHub's normal 100 MiB file limit.

The Borsuk clone has eight commits outside main at `83e6abf5e569164669689d7038357e31443ba875`. A self-contained incremental history bundle would add 1,262,036,016 bytes, so that history is excluded and the small original Borsuk clone remains local. Its six working-file changes are included in this PR.

The Borsuk working files include weighted-contact-coloring counterexamples and H4 mixed-deletion/negative-graph experiments. Universal-amplification files include threshold/catalyst searches, determinant checks, and potential-function experiments. STC-JC artifacts are historical v1.1.5 material, not replacements for v1.1.7. Remaining archives preserve Kissing-5 snapshots, K2P referee records, Ramsey certificates, and other historical outputs.

Author: Alec Kriebel, https://orcid.org/0009-0001-9320-500X

The universal-amplification clone also contained 41 historical reflog tips outside current GitHub history. `universal-reflog-history.bundle` preserves these under `recovered-universal-*` refs (approximately 0.65 MiB). Fetch all existing GitHub branches and tags before importing this incremental bundle.

Cleanup completed after remote checksum verification. `CLEANUP_RESULT.json` lists the exact oversized files retained. The Borsuk folder now contains Git metadata only, and still depends on the primary Math object store; recover working files from this PR or restore from Git when needed. Uploaded archive working copies and the temporary publishing repository were removed after the final metadata push.
