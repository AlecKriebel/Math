# Independent audit and acceptance

Problem 10300034 / AMR-102-0034, rank 1005.

**Accepted without correction as an unsolved 5/5 approach-family packet.** Read AUDIT.md for the complete mathematical review, source applicability, and acceptance limits. This review does not claim a solution, historical novelty, or exhaustive current-status knowledge.

The author packet is unchanged. This package contains only original audit exposition, executable independent controls, acceptance records, and public verification metadata. It contains no source PDFs, source extracts, screenshots, corpus contents, or private coordination material.

## Files

- AUDIT.md: full mathematical and source-scope audit
- ACCEPTANCE.json: machine-readable scoped verdict
- exact_controls.py: independent rational/integer and finite-group/graph checks
- replay_audit.py: external author authentication, author and independent adversarial checks, optional full-input replay
- REPLAY_RESULTS.json: recorded reproducible output
- AUDIT_MANIFEST.json: byte counts and SHA-256 values for the audit payload

## Reproduction

Obtain the expected audit archive/manifest hashes independently before trusting executable audit files. The audit manifest records bytes; it does not authenticate itself. The replay driver independently pins the original author archive, bootstrap, manifest, and proof.

With Python 3 and the original author packet available, run:

    python3 -I -S -B exact_controls.py
    python3 -I -S -B -O exact_controls.py
    python3 -I -S -B -OO exact_controls.py

For the complete artifact and mathematical control replay:

    python3 -I -S -B replay_audit.py --author-root AUTHOR_ROOT --author-archive AUTHOR_ARCHIVE
    python3 -I -S -B -O replay_audit.py --author-root AUTHOR_ROOT --author-archive AUTHOR_ARCHIVE
    python3 -I -S -B -OO replay_audit.py --author-root AUTHOR_ROOT --author-archive AUTHOR_ARCHIVE

To reproduce the optional corpus and source-hash sections of REPLAY_RESULTS.json, append:

    --problems PROBLEMS_JSON --research-results RESEARCH_RESULTS_JSON --source-dir SOURCE_DIR

The two corpus arguments must refer to the complete externally supplied input files. SOURCE_DIR uses the original retained basenames recorded in the author materials. No corpus or paper content is included or emitted. If pdftotext is available, the driver additionally performs a fresh extraction in memory and records its hash. Its output may depend on the installed Poppler version; the recorded run reproduced every retained extraction exactly.

The driver performs all three optimization modes internally; running its entry point in all three modes also checks that its own validation does not depend on assertions. It never edits the original packet. It makes disposable temporary copies for mutations and read-only/relocation controls. The audit scripts themselves also run from a read-only copy. It requires a regular unprivileged Unix user for the unreadable-file controls and filesystem support for symlinks and FIFOs.

The original author manifest hash is 690e26d6f9b86e3c95ca74213a49f90c5f9fce5cd769c512bc3698904300e782; bootstrap hash is 203a1d8f5a9e49dc0eddfc4eff73c39751b07ceb029d544ac6b07d5e4a8f7f6e. The 24,236-byte author archive hash is 533268c19efeb1e024777bfca36afbb20ee4e9ee09ab0fd01c7d3fc0bfed8564.

Passing finite controls cannot establish the topology or the original universal existence assertion. That distinction is part of the acceptance, not an unresolved validation error. The full Lickorish PDF was unavailable; only the primary opening theorem text was inspected, and no full-paper inspection is claimed.
