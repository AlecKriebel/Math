# 30005613: pure point spectrum on a quasi-conical domain

Status: complete author candidate, awaiting independent mathematical audit.
This packet is not a historical-novelty claim or a statement of human peer
review. The September 2026 primary literature still presents the target as
open. No remote repository changes were made while preparing this packet.

The proposed theorem constructs, in every dimension d >= 2, a connected
open tower of expanding cubes with shrinking positive windows whose
Dirichlet Laplacian has a complete eigenbasis and spectrum [0,infinity).
The proof controls finite-rank spectral projections and establishes their
completeness. It does not use trace-class invariance to discard singular
continuous spectrum.

The construction chooses cube widths as well as windows, as the original
Krejcirik--Lotoreichik construction permits. It is not a theorem for every
preassigned tower, smooth boundary, bounded domain, or Neumann Laplacian.

- PROOF.md contains the mathematical argument and exact scope.
- SOURCE_AUDIT.md records primary-source and repository checks.
- APPROACHES.md records the two substantive routes, with early stop at the
  complete candidate, within the five-route maximum.
- source_metadata.json contains only hashes, sizes, public identifiers,
  retrieval/inspection facts, and bounded verification results.
- verify.py and verification.json check exact bookkeeping and a finite
  projection model. They do not formally verify the infinite-dimensional
  mathematical proof or compute admissible apertures.
- MANIFEST.json freezes the authored packet files by SHA-256 and size.

Run `python verify.py` from this directory. Source PDFs, article text,
screenshots, original dataset entries, and private coordination records are
excluded from this packet.
