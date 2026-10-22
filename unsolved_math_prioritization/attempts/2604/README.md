# Kourovka 21.95: scoped partial results

**ID 2604; rank 771. Unsolved, 5/5 approaches.** The original existence question remains unresolved. This draft publishes rigorous family exclusions, bounded finite collision certificates, and an independent audit. No solution, novelty or priority is claimed.

Start with [the author proofs](author/PROOFS.md) and [the independent audit](independent_audit/AUDIT_REPORT.md). The audit passes only their stated partial-results scope and requires no mathematical corrections.

## Retained scope

- Recognition compares against all finite groups using the abstract unlabelled Gruenberg–Kegel graph. Labelled equality supplies a sufficient collision; competing groups need not be almost simple.
- The infinite-family proofs exclude every S_n for n >= 5 and the explicitly represented characteristic-two symplectic natural-module field-semilinear groups. Exceptional graph automorphisms are outside the latter theorem.
- The PGL_2 census excludes exactly 183 odd-prime-power targets 5 <= q <= 1000, with witnesses searched up to 10000. The largest author witness is 461. There is no all-q theorem or claim of infinitely many partners for each target.
- Five sporadic outer-extension exclusions depend on stated literature results. The full imported classification proofs were not independently audited.
- The q=4 fixed-vector transvection test is vacuous; q=8 supplies 504 pairs. The independent audit also checks 5526 fixed-space dimensions by binary elimination. Finite checks support the written proofs rather than settling the original problem.

## Preserved history and additional provenance

Both frozen directories and their ZIP archives are preserved byte-for-byte. Author statements that audit was pending, and mathematical-audit statements excluding raw-corpus/repository provenance, describe their original checkpoints. They have not been silently rewritten.

The separate [provenance supplement](KOUROVKA_2604_PROVENANCE_SUPPLEMENT.json) adds later full-file corpus digest verification, immutable descriptor identity, the repository hash convention, selected-record inspection, and bounded current prior-attempt checks. Its explicit search and retrieval limits remain in force. It does not certify novelty, unseen prior work or full imported proofs, and does not broaden the mathematical audit.

## Offline replay

With Python 3 and its standard library, from any working directory:

    python3 /path/to/2604/verify_publication.py

The wrapper checks the complete recursive file/directory inventory, hashes, both original manifests, both ZIP byte pins and every member, the separate supplement, scoped status, author checks and independent author-comparison replay. It matches the stored VERIFICATION_RESULTS.json and changes no files. No network, source PDFs, datasets, GAP or Sage is needed. The subprocesses run with assertions enabled; the wrapper uses explicit failures for its own checks.

The only existing repository-file edit is this target's queue Status = unsolved and Turns = 5/5. All other queue bytes, including its pre-existing header, are preserved. This is a draft review checkpoint, not a merge, release or DOI.
