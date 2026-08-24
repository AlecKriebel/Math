# Changelog

## bioRxiv submission and archival support -- 23 August 2026

- Preserved the title and both principal collision theorems; narrowed the final
  abstract verifier sentence so it names the checks actually performed.
- Made the stationary-root, Fourier normalization, unrestricted theta map,
  effective-edge conventions, exact rank minors, tree-model embeddings, and
  implicit-function arguments explicit in the manuscript.
- Corrected the theta figure so the leaf-2 edge no longer visually overlaps the
  core edge; added biological scope, ORCID, keywords/MSC, contribution, funding,
  competing-interest, code/data, and AI-assistance statements.
- Hardened every verifier against certificate-label, topology, algebraic-field,
  interval, minima, sidecar, and optimized-mode failure paths. The simple
  certificate generator now checks its own exact square-root isolating interval.
- Regenerated all verifier transcripts and all three PDFs after the final edits.
- Made this directory the unambiguous sole current package; the parent draft,
  verifier, certificates, and ZIP are now described as historical only.
- Added a dated audit of official bioRxiv scope and upload guidance, reusable
  metadata worksheet, and final approval checklist.
- Added `CITATION.cff` with author ORCID and preferred manuscript citation.
- Added an MIT license for executable verifier/build code and a separate file
  documenting manuscript, certificate, transcript, and bioRxiv-license
  boundaries.
- Added a placeholder-driven Zenodo metadata template without selecting an
  author-controlled manuscript or mixed-package license.
- Added a deterministic, commit-pinned release builder with dirty-tree,
  cache/bytecode, required-file, archive-integrity, and double-build checks.
  Archives carry an internal full-commit/version provenance record and per-file
  SHA-256 manifest; combined and per-archive checksum sidecars are emitted.
- Assigned release version `1.0.0` and the immutable tag
  `k2p-k3p-theta-biorxiv-v1.0.0`; no bioRxiv or Zenodo DOI was minted.

## Focused verifier convention check -- 13 August 2026

- Added the exact rational five-coordinate 3-sunlet convention check directly to `verify_k2p_displayed_trees.py`, so the focused verifier now visibly substantiates the Lemma 4.1 convention claim in the clarification note.
- Refreshed the focused and complete verification transcripts, checksums, and package archive.

No mathematical parameter, certificate value, collision calculation, or conclusion changed.

## Displayed-tree clarification revision -- 12 August 2026

This is a clarification and verification revision. No mathematical parameter or conclusion changed.

- Assigned `S` explicitly to both arcs `p->r2` and `p->r3` everywhere the construction is introduced.
- Assigned `T` explicitly to both arcs `q->r2` and `q->r3` everywhere the construction is introduced.
- Replaced the inaccurate description "four pendant rooted edges" with "four common K-edges" in the technical summary. The distinct phrase "suppressed pendant edge" remains where it correctly describes the effective leaf-1 edge after root suppression.
- Derived the common Fourier factor `K_x K_(y+z) K_y K_z = K_x^2 K_y K_z` from the labelled descendants of the four `K`-edges.
- Added the complete four-switching table and derived the four terms defining `M` from the retained parents at `r2` and `r3`.
- Added `verify_k2p_displayed_trees.py`, which literally deletes the unselected incoming reticulation arcs and reconstructs descendant sets, edge labels, and monomials from graph data.
- Added an independent exact ordinary-state pruning check for the simple `Q(sqrt(71))` witness. It compares all 64 network probabilities with the comparison tree, Fourier inversion, and the stored certificate.
- Recorded the exact source-convention cross-check reproducing all five displayed Fourier coordinates in Lemma 4.1 of arXiv:2607.12919v2.
- Corrected the technical summary's edge placement, common-edge terminology, K3P reuse of `M`, replay instructions, and public-status wording.
- Corrected confidentiality and notification language to match the public repository and recorded the pre-clarification public history without rewriting it.
- Added diagnostic fingerprints `M_(A,C)=151/1440` and `M_(C,C)=71/1600`.

Unchanged results include the simple and strict continuous-time K2P witnesses, the matrix `M`, factors `P` and `R`, comparison-tree vectors, minimum pattern probability, induction-order diagnosis, K2P rank and collision-family results, the K3P witness, the K3P rank/Jacobian calculation, and the analytic continuous-time K3P extension.
