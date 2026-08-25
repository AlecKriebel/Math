# K3P release engineering

This directory selects every repository-derived archive payload member only
from blobs committed at `HEAD`.  Generated archive manifests, readmes, and
`SOURCE_BUILD.json` records are reconstructed deterministically and checked
against exact schemas and policy bytes.  Random working-tree files, symlinks,
and untracked research material cannot enter either archive.  Archive member
order, ownership, permissions, timestamps, gzip headers, ZIP timestamps, and
JSON manifests are canonicalized; the exact selected path sets are hash-locked.

The ordinary full suite performs fresh independent replay but deliberately
does **not** launch the hour-scale probe producer.  Only
`reproducibility/verify_regenerate_all.sh`, with the explicit environment
confirmation printed by that script, invokes long producers.

Canonical outputs are written below `release/dist/` and are intentionally
ignored by Git.  The full builder fails until the final article and supplement
PDFs are committed at the paths named in `RELEASE_FILESET.json`.  It never
creates a tag, GitHub release, DOI, license declaration, or journal upload.

Typical final sequence:

```bash
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
.venv/bin/python release/build_release.py compact
.venv/bin/python release/build_release.py full
.venv/bin/python release/verify_source_reproduction.py --kind article
.venv/bin/python release/verify_source_reproduction.py --kind supplement
```

Run the all-producer path once, unattended and without restarting it:

```bash
K3P_CONFIRM_FULL_REGENERATION=YES bash reproducibility/verify_regenerate_all.sh
```

`release/build_release.py envelope` is a pre-DOI asset-binding operation after
a local exact-HEAD tag exists and all clean-worktree transcripts,
source-reproduction reports, and independently validated journal packages have
been supplied explicitly.  It refuses the current `DRAFT_NOT_READY` submission
tree, arbitrary package files, and mislabeled journal archives.  The envelope
records DOI and license as unassigned and does not prove that a tag was pushed;
those are human-controlled external facts.
