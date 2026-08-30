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

Typical local reseal sequence:

```bash
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
.venv/bin/python release/build_release.py compact
.venv/bin/python release/build_release.py full
.venv/bin/python release/verify_source_reproduction.py --kind article \
  --tectonic-cache-root "$HOME/Library/Caches/Tectonic"
.venv/bin/python release/verify_source_reproduction.py --kind supplement \
  --tectonic-cache-root "$HOME/Library/Caches/Tectonic"
```

These last two commands write the final-commit reports and four transcripts to
the ignored `release/source_reproduction_evidence/` asset directory.  The
referee-package builder requires, validates, copies, and outer-manifest-seals
all six files.  They cannot be tracked in the source commit they attest to
without creating a self-reference.  The release envelope likewise binds them
as explicit external assets.

The tracked cache inventory is refreshed only when the PDF resource bundle is
intentionally changed:

```bash
.venv/bin/python release/build_tectonic_cache_manifest.py \
  --cache-root "$HOME/Library/Caches/Tectonic"
```

After such a refresh, update the manifest SHA-256 in `RELEASE_FILESET.json` and
repeat both source reproductions.  Ordinary verification never modifies or
downloads the resource cache.

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

The direct Zenodo version 1.0.0 deposit is governed instead by
`release/zenodo/`, the deposited public manifest, and `SHA256SUMS`.  Those
files---not the journal-coupled pre-DOI envelope---bind the public assets.
Zenodo assigns the DOI at publication; the DOI remains authoritative record
metadata rather than being embedded in the immutable version 1.0.0 files.
