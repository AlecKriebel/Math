# Linked skeletons of convex four-polytopes: audited partial results

Target **30001138 / OWR-3385-009**, rank 666. Disposition: **unsolved after five approaches (5/5)**. No full solution, candidate resolution, novelty claim, or certificate of global current-literature open status is offered.

The original question concerns a nonsplit pair of disjoint cycles in a convex four-polytope's specified natural boundary embedding even though its abstract graph admits another linkless embedding. These two embedding claims must not be conflated. Zero linking number does not certify splitness.

## Accepted results and remaining gap

The independently audited exclusions cover simplicial convex four-polytopes, four-dimensional pyramids, all convex four-polytopes with at most six vertices, Cartesian products of two convex polygons, and the completely vertex-truncated four-simplex. The exact existence question remains unresolved outside these classes. Negative randomized minor searches remain inconclusive.

Read [the authored proof](author/PROOF_AND_PARTIALS.md), [five-approach log](author/APPROACH_LOG.md), [full independent audit](independent-audit/AUDIT.md), and [clarification supplement](independent-audit/CORRECTIONS.md). The audit accepts the exclusions and finds no mandatory mathematical correction. Its full report and the frozen author packet are preserved byte-for-byte, including dated pre-audit statements in the author README and log. Those statements are historical; the later audit is supplied here. The stacking and face-lattice arguments require boundary-sphere PL homeomorphisms preserving splitness, not a path through convex realizations.

The 2026 source is a report of a gap in the 2025 linearization proof, not a counterexample to its theorem. Neither that disputed proof nor an inference from some alternative embedding to the specified natural embedding is used. Cited deep theorems are established inputs, not newly re-proved here. The source search is bounded. The audit did not independently re-download the external corpus.

## Reproduce offline

Python 3.10 or later, standard library only; no network, source PDFs, or datasets required. From this directory:

    python verify_release.py

This verifies an exact file allowlist, byte counts and hashes, both frozen archives, equality of expanded files to every archive member, author and audit manifests, the archive binding, the author's exact finite checks and the separately implemented audit. Both replay outputs must equal their stored JSON results. Damaged minor/family controls and the failing four-cube facet-cover control are included in those computations. Integrity can be checked alone:

    python verify_release.py --integrity-only

These checks establish the stated finite certificates and preservation, not a formal verification of every mathematical proof or a full solution. The optional long randomized exploration is not run by this wrapper.

## Frozen artifacts

- Author archive: 26,737 bytes; 16 files; SHA-256 `78cdf14fddfa360a5cbb27d1b571e88bd4eed6e7410c6296de628b19f9770719`.
- Independent audit archive: 18,717 bytes; 10 files; SHA-256 `01d47732e475622e70a9eb05a90ba20d874878eaa70f3da648398a463fc99b2d`.

`PUBLICATION_MANIFEST.json` covers all other files in this directory. This publication contains authored mathematics, code, full safe audit material, and public verification metadata only. No third-party source PDFs/text, corpus contents, private sources, or private coordination files are included. The separate queue change alters this target's Status and Turns only; Findings, all links, the header, and every other byte are preserved. No queue command, merge, release, DOI, or outreach is part of this draft.
